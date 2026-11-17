"""Pure reconciliation and calculation helpers for Flex dividend income."""
from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta
from math import isclose
from typing import Literal, TypeAlias

from ib_common.schema import (
    AnnualDividendEstimate,
    AnnualDividendHolding,
    DividendAttribution,
    DividendContribution,
    DividendIncomeLine,
    DividendIncomeReport,
    DividendIncomeSummary,
    DividendTotals,
    FlexCashTransaction,
    FlexDividendAccrual,
    FlexDividendDataset,
    FlexInstrument,
    FlexOpenPosition,
)


_EventKey: TypeAlias = tuple[str, str, str, date, date]
_AccrualSecondaryKey: TypeAlias = tuple[str, str, str, date, date]
_CashIdentity: TypeAlias = tuple[str, str, str]
_LifecycleAmbiguity: TypeAlias = tuple[str, date]
_MatchRank: TypeAlias = tuple[int, int]
_MATCH_TOLERANCE_DAYS = 3
_EXCHANGE_COUNTRIES = {
    "AEB": "NL",
    "AMEX": "US",
    "ARCA": "US",
    "ASX": "AU",
    "BATS": "US",
    "EBS": "CH",
    "FWB": "DE",
    "HKEX": "HK",
    "IBIS": "DE",
    "IBIS2": "DE",
    "IEX": "US",
    "LSE": "GB",
    "NASDAQ": "US",
    "NASDAQCM": "US",
    "NASDAQGM": "US",
    "NASDAQGS": "US",
    "NYSE": "US",
    "NYSEARCA": "US",
    "NYSEMKT": "US",
    "SEHK": "HK",
    "SGX": "SG",
    "SIX": "CH",
    "TSEJ": "JP",
    "TSX": "CA",
    "TSXV": "CA",
    "XETRA": "DE",
}
_ISO_COUNTRY_CODES = frozenset(
    """
    AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI
    BJ BL BM BN BO BQ BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN
    CO CR CU CV CW CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK
    FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM
    HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN
    KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK
    ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP
    NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW
    SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TF
    TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI
    VN VU WF WS YE YT ZA ZM ZW
    """.split()
)


def _normalized_symbol(symbol: str) -> str:
    """Normalize punctuation, whitespace, and case for deterministic fallback."""
    return "".join(character for character in symbol.upper() if character.isalnum())


def listing_country(exchange: str, isin: str) -> str:
    """Return a primary listing-market country, with absent-exchange ISIN fallback."""
    normalized_exchange = exchange.strip().upper()
    if normalized_exchange:
        return _EXCHANGE_COUNTRIES.get(normalized_exchange, "UNKNOWN")
    normalized_isin = isin.strip().upper()
    if (
        len(normalized_isin) == 12
        and normalized_isin[:2] in _ISO_COUNTRY_CODES
    ):
        return normalized_isin[:2]
    return "UNKNOWN"


def _event_key(accrual: FlexDividendAccrual) -> _EventKey:
    """Return the preferred conid event key or its symbol fallback key."""
    identity = (
        f"CONID:{accrual.conid}"
        if accrual.conid
        else f"SYMBOL:{_normalized_symbol(accrual.symbol)}"
    )
    return (
        accrual.account_id,
        identity,
        accrual.currency.upper(),
        accrual.ex_date,
        accrual.pay_date,
    )


def _accrual_secondary_key(
    accrual: FlexDividendAccrual,
) -> _AccrualSecondaryKey:
    """Return the conid-independent identity used for safe lifecycle fallback."""
    return (
        accrual.account_id,
        accrual.currency.upper(),
        _normalized_symbol(accrual.symbol),
        accrual.ex_date,
        accrual.pay_date,
    )


def _sum_optional(
    rows: list[FlexDividendAccrual], field_name: str
) -> float | None:
    """Sum one nullable lifecycle amount while preserving all-null input."""
    values = [getattr(row, field_name) for row in rows]
    known = [value for value in values if value is not None]
    return None if not known else sum(known)


def _reduce_accrual_lifecycle(
    rows: list[FlexDividendAccrual],
    *,
    confirmed_cash: list[FlexCashTransaction] | None = None,
    limitations: list[str] | None = None,
) -> list[FlexDividendAccrual]:
    """Collapse accrual rows, retaining payout reversals proven by cash."""
    unique_rows: list[FlexDividendAccrual] = []
    seen: set[str] = set()
    for row in rows:
        fingerprint = row.model_dump_json()
        if fingerprint not in seen:
            seen.add(fingerprint)
            unique_rows.append(row)

    raw_groups: dict[_EventKey, list[FlexDividendAccrual]] = defaultdict(list)
    for row in unique_rows:
        raw_groups[_event_key(row)].append(row)

    conid_keys_by_secondary: dict[
        _AccrualSecondaryKey, set[_EventKey]
    ] = defaultdict(set)
    for event_key, event_rows in raw_groups.items():
        if event_key[1].startswith("CONID:"):
            for row in event_rows:
                conid_keys_by_secondary[_accrual_secondary_key(row)].add(
                    event_key
                )
    coalesced_targets: dict[_EventKey, _EventKey] = {}
    for event_key, event_rows in raw_groups.items():
        if not event_key[1].startswith("SYMBOL:"):
            continue
        conid_keys = conid_keys_by_secondary.get(
            _accrual_secondary_key(event_rows[0]), set()
        )
        if len(conid_keys) == 1:
            coalesced_targets[event_key] = next(iter(conid_keys))

    groups: dict[_EventKey, list[FlexDividendAccrual]] = defaultdict(list)
    for row in unique_rows:
        event_key = _event_key(row)
        groups[coalesced_targets.get(event_key, event_key)].append(row)
    for event_key, event_rows in groups.items():
        merged_rows: list[FlexDividendAccrual] = []
        seen_facts: set[str] = set()
        for row in event_rows:
            fingerprint = row.model_copy(
                update={"conid": None}
            ).model_dump_json()
            if fingerprint not in seen_facts:
                seen_facts.add(fingerprint)
                merged_rows.append(row)
        groups[event_key] = merged_rows

    confirmed_by_key: dict[_EventKey, list[FlexCashTransaction]] = defaultdict(list)
    if confirmed_cash:
        group_items = list(groups.items())
        for cash in confirmed_cash:
            common = [
                (key, event_rows)
                for key, event_rows in group_items
                if key[0] == cash.account_id
                and key[2] == cash.currency.upper()
            ]
            if cash.conid:
                identity_matches = [
                    (key, event_rows)
                    for key, event_rows in common
                    if key[1] == f"CONID:{cash.conid}"
                ]
                if not identity_matches:
                    identity_matches = [
                        (key, event_rows)
                        for key, event_rows in common
                        if key[1].startswith("SYMBOL:")
                        and _normalized_symbol(event_rows[-1].symbol)
                        == _normalized_symbol(cash.symbol)
                    ]
            else:
                identity_matches = [
                    (key, event_rows)
                    for key, event_rows in common
                    if _normalized_symbol(event_rows[-1].symbol)
                    == _normalized_symbol(cash.symbol)
                ]
            exact = [
                (key, event_rows)
                for key, event_rows in identity_matches
                if key[4] == cash.ts.date()
            ]
            candidates = exact or [
                (key, event_rows)
                for key, event_rows in identity_matches
                if abs((key[4] - cash.ts.date()).days) <= _MATCH_TOLERANCE_DAYS
            ]
            if len(candidates) == 1:
                confirmed_by_key[candidates[0][0]].append(cash)

    reduced: list[FlexDividendAccrual] = []
    for event_key, event_rows in groups.items():
        representative = event_rows[-1]
        known_conid = next(
            (row.conid for row in reversed(event_rows) if row.conid), None
        )
        combined = representative.model_copy(
            update={
                "conid": known_conid,
                "quantity": _sum_optional(event_rows, "quantity"),
                "tax": _sum_optional(event_rows, "tax"),
                "fee": _sum_optional(event_rows, "fee"),
                "gross_rate": _sum_optional(event_rows, "gross_rate"),
                "gross_amount": _sum_optional(event_rows, "gross_amount"),
                "net_amount": _sum_optional(event_rows, "net_amount"),
            }
        )
        positive_event = any(
            value is not None and value >= 0.01
            for value in (
                combined.gross_amount,
                combined.net_amount,
            )
        )
        if positive_event:
            reduced.append(combined)
            continue

        event_cash = confirmed_by_key.get(event_key, [])
        positive_postings = [
            row
            for row in event_rows
            if any(
                value is not None and value > 0
                for value in (row.gross_amount, row.net_amount, row.gross_rate)
            )
        ]
        if not event_cash or not positive_postings:
            continue

        cash_amounts = [
            cash.amount for cash in event_cash if cash.amount is not None
        ]
        postings_with_amount = [
            row for row in positive_postings if row.gross_amount is not None
        ]
        amount_matches = [
            row
            for row in postings_with_amount
            if any(
                not _materially_different(row.gross_amount, cash_amount)
                for cash_amount in cash_amounts
            )
        ]
        if cash_amounts and postings_with_amount and not amount_matches:
            if limitations is not None:
                limitations.append(
                    f"Cash-confirmed dividend for {representative.symbol.strip()} "
                    "had a gross-amount discrepancy with its zeroed accrual "
                    "lifecycle; cash-only facts were retained."
                )
            continue
        candidates = (
            amount_matches
            if cash_amounts and postings_with_amount
            else positive_postings
        )
        retained = max(
            enumerate(candidates),
            key=lambda item: (
                item[1].accrual_date or date.min,
                item[1].report_date or date.min,
                item[0],
            ),
        )[1]
        reduced.append(retained)
    return reduced


def _best_date_indices(
    cash: FlexCashTransaction,
    candidates: list[tuple[int, FlexDividendAccrual]],
) -> tuple[list[int], int]:
    """Prefer exact payment dates, then candidates within three calendar days."""
    payment_date = cash.ts.date()
    exact = [index for index, row in candidates if row.pay_date == payment_date]
    if exact:
        return exact, 0
    tolerant = [
        index
        for index, row in candidates
        if abs((row.pay_date - payment_date).days) <= _MATCH_TOLERANCE_DAYS
    ]
    return tolerant, 1


def _best_accrual_candidates(
    cash: FlexCashTransaction,
    accruals: list[FlexDividendAccrual],
) -> list[tuple[int, _MatchRank]]:
    """Return all candidates in the best conid/symbol and date match tier."""
    common = [
        (index, row)
        for index, row in enumerate(accruals)
        if row.account_id == cash.account_id
        and row.currency.upper() == cash.currency.upper()
    ]
    if cash.conid:
        conid_indices, date_rank = _best_date_indices(
            cash,
            [(index, row) for index, row in common if row.conid == cash.conid],
        )
        if conid_indices:
            return [(index, (0, date_rank)) for index in conid_indices]

    normalized_cash_symbol = _normalized_symbol(cash.symbol)
    symbol_indices, date_rank = _best_date_indices(
        cash,
        [
            (index, row)
            for index, row in common
            if _normalized_symbol(row.symbol) == normalized_cash_symbol
            and not (cash.conid and row.conid)
        ],
    )
    return [(index, (1, date_rank)) for index in symbol_indices]


def _match_accrual(
    cash: FlexCashTransaction,
    accruals: list[FlexDividendAccrual],
) -> tuple[FlexDividendAccrual | None, bool]:
    """Return one best-tier accrual and whether the best tier was ambiguous."""
    candidates = _best_accrual_candidates(cash, accruals)
    if len(candidates) == 1:
        return accruals[candidates[0][0]], False
    return None, len(candidates) > 1


def _associate_cash_to_accruals(
    cash_rows: list[FlexCashTransaction],
    accruals: list[FlexDividendAccrual],
) -> list[tuple[int | None, bool]]:
    """Assign accruals once, leaving same-rank many-to-one claims ambiguous."""
    results: list[tuple[int | None, bool]] = [
        (None, False) for _ in cash_rows
    ]
    claims: dict[int, list[tuple[int, _MatchRank]]] = defaultdict(list)
    for cash_index, cash in enumerate(cash_rows):
        candidates = _best_accrual_candidates(cash, accruals)
        if len(candidates) > 1:
            results[cash_index] = (None, True)
        elif len(candidates) == 1:
            accrual_index, rank = candidates[0]
            claims[accrual_index].append((cash_index, rank))

    for accrual_index, accrual_claims in claims.items():
        best_rank = min(rank for _, rank in accrual_claims)
        best_claims = [
            cash_index
            for cash_index, rank in accrual_claims
            if rank == best_rank
        ]
        if len(best_claims) == 1:
            winner = best_claims[0]
            results[winner] = (accrual_index, False)
            for cash_index, _ in accrual_claims:
                if cash_index != winner:
                    results[cash_index] = (None, True)
        else:
            for cash_index, _ in accrual_claims:
                results[cash_index] = (None, True)
    return results


def _is_dividend_cash(row: FlexCashTransaction) -> bool:
    """Identify positive dividend cash postings without treating tax as income."""
    return "dividend" in row.transaction_type.casefold() and bool(
        row.amount is not None and row.amount > 0
    )


def _cash_identity(row: FlexCashTransaction) -> _CashIdentity:
    """Return stable cash identity without mutable posting dates or trade IDs."""
    identity = (
        f"CONID:{row.conid}"
        if row.conid
        else f"SYMBOL:{_normalized_symbol(row.symbol)}"
    )
    return (
        row.account_id,
        identity,
        row.currency.upper(),
    )


def _is_reversal_code(code: str) -> bool:
    """Recognize Flex reversal and cancellation lifecycle codes."""
    return code.strip().upper() in {
        "CA",
        "CANCEL",
        "CANCELLATION",
        "RE",
        "REVERSAL",
    }


def _reduce_cash_lifecycle(
    rows: list[FlexCashTransaction],
    *,
    transaction_kind: Literal["DIVIDEND", "WITHHOLDING"],
    limitations: list[str] | None = None,
    ambiguity_events: set[_LifecycleAmbiguity] | None = None,
) -> list[FlexCashTransaction]:
    """Apply signed postings and coded reversals to stable cash identities."""
    unique: list[FlexCashTransaction] = []
    seen: set[str] = set()
    for row in rows:
        matches_kind = (
            "dividend" in row.transaction_type.casefold()
            if transaction_kind == "DIVIDEND"
            else _is_withholding_cash(row, require_deduction=False)
        )
        if not matches_kind or row.amount is None:
            continue
        fingerprint = row.model_dump_json()
        if fingerprint not in seen:
            seen.add(fingerprint)
            unique.append(row)
    groups: dict[_CashIdentity, list[FlexCashTransaction]] = defaultdict(list)
    for row in unique:
        groups[_cash_identity(row)].append(row)

    reduced: list[FlexCashTransaction] = []
    for event_rows in groups.values():
        active: list[tuple[FlexCashTransaction, float]] = []
        ordered_rows = sorted(event_rows, key=lambda row: row.ts)
        for row in ordered_rows:
            assert row.amount is not None
            raw_delta = row.amount if transaction_kind == "DIVIDEND" else -row.amount
            delta = -abs(raw_delta) if _is_reversal_code(row.code) else raw_delta
            if delta > 0:
                active.append((row, delta))
                continue
            if delta == 0 or not active:
                continue

            remaining_reversal = abs(delta)
            trade_matches = [
                index
                for index, (posting, _) in enumerate(active)
                if row.trade_id
                and posting.trade_id
                and posting.trade_id == row.trade_id
            ]
            if len(trade_matches) == 1:
                target_index = trade_matches[0]
            elif len(trade_matches) > 1:
                target_index = None
            else:
                amount_matches = [
                    index
                    for index, (_, amount) in enumerate(active)
                    if isclose(
                        amount,
                        remaining_reversal,
                        rel_tol=0.0,
                        abs_tol=1e-9,
                    )
                ]
                if len(amount_matches) == 1:
                    target_index = amount_matches[0]
                elif not amount_matches and len(active) == 1:
                    target_index = 0
                else:
                    target_index = None

            if target_index is None:
                if ambiguity_events is not None:
                    ambiguity_events.add(
                        (_normalized_symbol(row.symbol), row.ts.date())
                    )
                    ambiguity_events.update(
                        (_normalized_symbol(posting.symbol), posting.ts.date())
                        for posting, _ in active
                    )
                if limitations is not None:
                    limitations.append(
                        f"{transaction_kind.title()} cash reversal for "
                        f"{row.symbol.strip()} was ambiguous; candidate postings "
                        "were preserved."
                    )
                continue

            posting, amount = active[target_index]
            amount -= min(amount, remaining_reversal)
            if isclose(amount, 0.0, rel_tol=0.0, abs_tol=1e-9):
                active.pop(target_index)
            else:
                active[target_index] = (posting, amount)

        for posting, amount in active:
            output_amount = amount if transaction_kind == "DIVIDEND" else -amount
            reduced.append(posting.model_copy(update={"amount": output_amount}))
    reduced.sort(key=lambda row: (row.ts, row.symbol, row.trade_id or ""))
    return reduced


def _reduce_dividend_cash_lifecycle(
    rows: list[FlexCashTransaction],
    *,
    limitations: list[str] | None = None,
    ambiguity_events: set[_LifecycleAmbiguity] | None = None,
) -> list[FlexCashTransaction]:
    """Reduce dividend cash postings and reversals to surviving payments."""
    return _reduce_cash_lifecycle(
        rows,
        transaction_kind="DIVIDEND",
        limitations=limitations,
        ambiguity_events=ambiguity_events,
    )


def _is_withholding_cash(
    row: FlexCashTransaction,
    *,
    require_deduction: bool = True,
) -> bool:
    """Identify a posted cash-tax deduction that can reconcile withholding."""
    transaction_type = row.transaction_type.casefold()
    is_tax = "withholding" in transaction_type or "tax" in transaction_type
    if not require_deduction:
        return is_tax and row.amount is not None
    return is_tax and bool(row.amount is not None and row.amount < 0)


def _reduce_withholding_cash_lifecycle(
    rows: list[FlexCashTransaction],
    *,
    limitations: list[str] | None = None,
    ambiguity_events: set[_LifecycleAmbiguity] | None = None,
) -> list[FlexCashTransaction]:
    """Reduce withholding postings and reversals to surviving deductions."""
    return _reduce_cash_lifecycle(
        rows,
        transaction_kind="WITHHOLDING",
        limitations=limitations,
        ambiguity_events=ambiguity_events,
    )


def _best_cash_date_indices(
    dividend: FlexCashTransaction,
    candidates: list[tuple[int, FlexCashTransaction]],
) -> tuple[list[int], int]:
    """Prefer same-day tax postings, then the bounded three-day tolerance."""
    payment_date = dividend.ts.date()
    exact = [index for index, row in candidates if row.ts.date() == payment_date]
    if exact:
        return exact, 0
    tolerant = [
        index
        for index, row in candidates
        if abs((row.ts.date() - payment_date).days) <= _MATCH_TOLERANCE_DAYS
    ]
    return tolerant, 1


def _best_withholding_candidates(
    dividend: FlexCashTransaction,
    withholding_rows: list[FlexCashTransaction],
) -> list[tuple[int, _MatchRank]]:
    """Return all withholding candidates in the dividend's best match tier."""
    common = [
        (index, row)
        for index, row in enumerate(withholding_rows)
        if _is_withholding_cash(row)
        and row.account_id == dividend.account_id
        and row.currency.upper() == dividend.currency.upper()
    ]
    if dividend.conid:
        conid_indices, date_rank = _best_cash_date_indices(
            dividend,
            [(index, row) for index, row in common if row.conid == dividend.conid],
        )
        if conid_indices:
            return [(index, (0, date_rank)) for index in conid_indices]
    normalized_symbol = _normalized_symbol(dividend.symbol)
    symbol_indices, date_rank = _best_cash_date_indices(
        dividend,
        [
            (index, row)
            for index, row in common
            if _normalized_symbol(row.symbol) == normalized_symbol
            and not (dividend.conid and row.conid)
        ],
    )
    return [(index, (1, date_rank)) for index in symbol_indices]


def _associate_withholdings(
    dividend_rows: list[FlexCashTransaction],
    cash_rows: list[FlexCashTransaction],
    *,
    limitations: list[str] | None = None,
    ambiguity_events: set[_LifecycleAmbiguity] | None = None,
) -> list[tuple[float | None, bool]]:
    """Assign each reduced withholding posting to at most one dividend cash row."""
    withholding_rows = _reduce_withholding_cash_lifecycle(
        cash_rows,
        limitations=limitations,
        ambiguity_events=ambiguity_events,
    )
    results: list[tuple[float | None, bool]] = [
        (None, False) for _ in dividend_rows
    ]
    claims: dict[int, list[tuple[int, _MatchRank]]] = defaultdict(list)
    for dividend_index, dividend in enumerate(dividend_rows):
        candidates = _best_withholding_candidates(dividend, withholding_rows)
        if len(candidates) > 1:
            results[dividend_index] = (None, True)
        elif len(candidates) == 1:
            withholding_index, rank = candidates[0]
            claims[withholding_index].append((dividend_index, rank))

    for withholding_index, withholding_claims in claims.items():
        best_rank = min(rank for _, rank in withholding_claims)
        best_claims = [
            dividend_index
            for dividend_index, rank in withholding_claims
            if rank == best_rank
        ]
        if len(best_claims) == 1:
            winner = best_claims[0]
            amount = withholding_rows[withholding_index].amount
            assert amount is not None
            results[winner] = (abs(amount), False)
            for dividend_index, _ in withholding_claims:
                if dividend_index != winner:
                    results[dividend_index] = (None, True)
        else:
            for dividend_index, _ in withholding_claims:
                results[dividend_index] = (None, True)
    return results


def _instrument_for(
    *,
    conid: str | None,
    symbol: str,
    currency: str,
    instruments: list[FlexInstrument],
) -> FlexInstrument | None:
    """Resolve instrument metadata when every best-tier row agrees on country."""
    def agreeing(rows: list[FlexInstrument]) -> FlexInstrument | None:
        """Return a representative only when country-relevant facts agree."""
        countries = {
            listing_country(row.listing_exchange or "", row.isin or "")
            for row in rows
        }
        return rows[0] if rows and len(countries) == 1 else None

    if conid:
        conid_matches = [row for row in instruments if row.conid == conid]
        if conid_matches:
            return agreeing(conid_matches)
    symbol_matches = [
        row
        for row in instruments
        if _normalized_symbol(row.symbol) == _normalized_symbol(symbol)
        and row.currency.upper() == currency.upper()
        and not (conid and row.conid)
    ]
    return agreeing(symbol_matches)


def _country_for(
    *,
    conid: str | None,
    symbol: str,
    currency: str,
    instruments: list[FlexInstrument],
) -> str:
    """Resolve listing country from uniquely associated instrument metadata."""
    instrument = _instrument_for(
        conid=conid,
        symbol=symbol,
        currency=currency,
        instruments=instruments,
    )
    if instrument is None:
        return "UNKNOWN"
    return listing_country(
        instrument.listing_exchange or "",
        instrument.isin or "",
    )


def _converted(value: float | None, rate: float | None) -> float | None:
    """Convert one known native amount only when Flex supplied an FX rate."""
    return None if value is None or rate is None else value * rate


def _materially_different(left: float, right: float) -> bool:
    """Return whether two posted monetary facts differ beyond one cent."""
    return not isclose(left, right, rel_tol=1e-6, abs_tol=0.01)


def _line_from_accrual(
    accrual: FlexDividendAccrual,
    *,
    status: Literal["REALIZED", "EXPECTED"],
    country: str,
) -> DividendIncomeLine:
    """Convert an accrual to one native and nullable base-currency line."""
    withholding_tax = None if accrual.tax is None else abs(accrual.tax)
    fee = None if accrual.fee is None else abs(accrual.fee)
    return DividendIncomeLine(
        symbol=accrual.symbol.strip(),
        payment_date=accrual.pay_date,
        status=status,
        gross=accrual.gross_amount,
        withholding_tax=withholding_tax,
        fee=fee,
        net=accrual.net_amount,
        currency=accrual.currency.upper(),
        fx_rate_to_base=accrual.fx_rate_to_base,
        base_gross=_converted(accrual.gross_amount, accrual.fx_rate_to_base),
        base_withholding_tax=_converted(
            withholding_tax, accrual.fx_rate_to_base
        ),
        base_fee=_converted(fee, accrual.fx_rate_to_base),
        base_net=_converted(accrual.net_amount, accrual.fx_rate_to_base),
        quantity=accrual.quantity,
        country=country,
    )


def _realized_line(
    cash: FlexCashTransaction,
    accrual: FlexDividendAccrual | None,
    *,
    country: str,
    cash_withholding: float | None,
    withholding_ambiguous: bool,
    accrual_ambiguous: bool = False,
) -> DividendIncomeLine:
    """Convert confirmed dividend cash and optional accrual facts to one line."""
    if accrual is not None:
        rate = (
            accrual.fx_rate_to_base
            if accrual.fx_rate_to_base is not None
            else cash.fx_rate_to_base
        )
        line = _line_from_accrual(
            accrual,
            status="REALIZED",
            country=country,
        )
        withholding_tax = (
            cash_withholding
            if cash_withholding is not None
            else line.withholding_tax
        )
        reconciled_net = line.net
        if cash_withholding is not None and (
            line.withholding_tax is None
            or _materially_different(cash_withholding, line.withholding_tax)
        ):
            reconciled_net = (
                line.gross - cash_withholding - line.fee
                if line.gross is not None and line.fee is not None
                else None
            )
        return line.model_copy(
            update={
                "symbol": cash.symbol.strip(),
                "payment_date": cash.ts.date(),
                "fx_rate_to_base": rate,
                "withholding_tax": withholding_tax,
                "net": reconciled_net,
                "base_gross": _converted(line.gross, rate),
                "base_withholding_tax": _converted(
                    withholding_tax, rate
                ),
                "base_fee": _converted(line.fee, rate),
                "base_net": _converted(reconciled_net, rate),
            }
        )
    unmatched_net = (
        None
        if withholding_ambiguous
        else (
            cash.amount - cash_withholding
            if cash.amount is not None and cash_withholding is not None
            else cash.amount
        )
    )
    # A confirmed positive dividend cash posting is itself gross income: the
    # withholding tax arrives on a separate row, so the cash amount is pre-tax.
    # When the cash could not be tied to any accrual and the match was not
    # ambiguous (e.g. a payment-in-lieu split whose single accrual was dropped as
    # a gross-amount discrepancy, or a re-issued amount with no surviving
    # accrual), the cash itself is the most reliable gross fact. Ambiguous
    # many-to-one matches stay null so competing cash cannot double-count one
    # dividend.
    unmatched_gross = (
        cash.amount
        if not accrual_ambiguous
        and cash.amount is not None
        and cash.amount > 0
        else None
    )
    return DividendIncomeLine(
        symbol=cash.symbol.strip(),
        payment_date=cash.ts.date(),
        status="REALIZED",
        gross=unmatched_gross,
        withholding_tax=cash_withholding,
        fee=None,
        net=unmatched_net,
        currency=cash.currency.upper(),
        fx_rate_to_base=cash.fx_rate_to_base,
        base_gross=_converted(unmatched_gross, cash.fx_rate_to_base),
        base_withholding_tax=_converted(cash_withholding, cash.fx_rate_to_base),
        base_fee=None,
        base_net=_converted(unmatched_net, cash.fx_rate_to_base),
        quantity=None,
        country=country,
    )


def _unique_dividend_cash(
    rows: list[FlexCashTransaction],
) -> list[FlexCashTransaction]:
    """Remove byte-for-byte duplicate cash facts before reliability checks."""
    unique: list[FlexCashTransaction] = []
    seen: set[str] = set()
    for row in rows:
        fingerprint = row.model_dump_json()
        if fingerprint not in seen:
            seen.add(fingerprint)
            unique.append(row)
    return unique


def _holding_accruals(
    position: FlexOpenPosition,
    accruals: list[FlexDividendAccrual],
) -> list[FlexDividendAccrual]:
    """Associate trailing rate events with one current holding identity."""
    common = [
        row
        for row in accruals
        if row.account_id == position.account_id
        and row.currency.upper() == position.currency.upper()
    ]
    if position.conid:
        exact = [row for row in common if row.conid == position.conid]
        exact_secondary_keys = {
            (
                row.account_id,
                row.currency.upper(),
                _normalized_symbol(row.symbol),
                row.ex_date,
                row.pay_date,
            )
            for row in exact
        }
        fallback = [
            row
            for row in common
            if row.conid is None
            and _normalized_symbol(row.symbol) == _normalized_symbol(position.symbol)
            and (
                row.account_id,
                row.currency.upper(),
                _normalized_symbol(row.symbol),
                row.ex_date,
                row.pay_date,
            )
            not in exact_secondary_keys
        ]
        return exact + fallback
    return [
        row
        for row in common
        if _normalized_symbol(row.symbol) == _normalized_symbol(position.symbol)
    ]


def _effective_tax_rate(
    *,
    symbol: str,
    trailing_start: date,
    end_date: date,
    cash_rows: list[FlexCashTransaction],
    accruals: list[FlexDividendAccrual],
) -> float | None:
    """Calculate tax rate only when every trailing cash event is fully reliable."""
    ambiguity_events: set[_LifecycleAmbiguity] = set()
    symbol_cash = _unique_dividend_cash(
        [
            row
            for row in _reduce_dividend_cash_lifecycle(
                cash_rows,
                ambiguity_events=ambiguity_events,
            )
            if _is_dividend_cash(row)
            and trailing_start <= row.ts.date() <= end_date
            and _normalized_symbol(row.symbol) == _normalized_symbol(symbol)
        ]
    )
    if not symbol_cash:
        return None

    withholding_associations = _associate_withholdings(
        symbol_cash,
        cash_rows,
        ambiguity_events=ambiguity_events,
    )
    normalized_symbol = _normalized_symbol(symbol)
    if any(
        affected_symbol == normalized_symbol
        and trailing_start <= affected_date <= end_date
        for affected_symbol, affected_date in ambiguity_events
    ):
        return None
    gross_total = 0.0
    tax_total = 0.0
    matched_events: set[_EventKey] = set()
    for cash_index, cash in enumerate(symbol_cash):
        accrual, ambiguous = _match_accrual(cash, accruals)
        if ambiguous or accrual is None or accrual.gross_amount is None:
            return None
        if accrual.gross_amount <= 0:
            return None
        cash_tax, withholding_ambiguous = withholding_associations[cash_index]
        if withholding_ambiguous and accrual.tax is None:
            return None
        if cash_tax is not None:
            tax = cash_tax
        elif accrual.tax is not None:
            tax = abs(accrual.tax)
        else:
            tax = None
        if tax is None:
            return None
        event_key = _event_key(accrual)
        if event_key in matched_events:
            return None
        matched_events.add(event_key)
        gross_total += accrual.gross_amount
        tax_total += tax

    if gross_total <= 0:
        return None
    effective_rate = tax_total / gross_total
    return effective_rate if 0.0 <= effective_rate <= 1.0 else None


def _current_eligible_positions(
    positions: list[FlexOpenPosition],
) -> list[FlexOpenPosition]:
    """Return latest summary-level current long stock and fund positions."""
    candidates = [
        row
        for row in positions
        if row.asset_class.upper() in {"STK", "FUND"}
        and row.level_of_detail.upper() == "SUMMARY"
        and row.side.upper() == "LONG"
        and row.quantity is not None
        and row.quantity > 0
    ]
    if not candidates:
        return []
    latest_by_account: dict[str, date] = {}
    for row in candidates:
        latest_by_account[row.account_id] = max(
            row.report_date,
            latest_by_account.get(row.account_id, row.report_date),
        )
    latest = [
        row
        for row in candidates
        if row.report_date == latest_by_account[row.account_id]
    ]
    unique: list[FlexOpenPosition] = []
    seen: set[str] = set()
    for row in latest:
        fingerprint = row.model_dump_json()
        if fingerprint not in seen:
            seen.add(fingerprint)
            unique.append(row)
    return sorted(unique, key=lambda row: (row.symbol, row.account_id, row.conid or ""))


def _history_days_covered(
    history_start_date: date,
    history_coverage_end_date: date,
    end_date: date,
) -> int:
    """Measure the available intersection with the inclusive trailing year."""
    trailing_start = end_date - timedelta(days=364)
    overlap_start = max(history_start_date, trailing_start)
    overlap_end = min(history_coverage_end_date, end_date)
    if overlap_start > overlap_end:
        return 0
    return min(365, (overlap_end - overlap_start).days + 1)


def _annual_estimate(
    *,
    dataset: FlexDividendDataset,
    accruals: list[FlexDividendAccrual],
    history_end_date: date,
    history_start_date: date,
    history_coverage_end_date: date,
    limitations: list[str],
) -> AnnualDividendEstimate:
    """Estimate annual holding income from unique trailing positive accrual rates."""
    trailing_start = history_end_date - timedelta(days=364)
    window_accruals = [
        row
        for row in accruals
        if trailing_start <= row.ex_date <= history_end_date
    ]
    trailing_rate_accruals = [
        row
        for row in window_accruals
        if row.gross_rate is not None
        and row.gross_rate > 0
    ]
    positions = _current_eligible_positions(dataset.open_positions)
    holdings: list[AnnualDividendHolding] = []
    denominator_values: list[float] = []
    denominator_complete = True
    for position in positions:
        position_accruals = _holding_accruals(position, trailing_rate_accruals)
        trailing_rate = sum(
            row.gross_rate
            for row in position_accruals
            if row.gross_rate is not None and row.gross_rate > 0
        )
        quantity = position.quantity
        assert quantity is not None
        estimated_gross = trailing_rate * quantity
        effective_tax_rate = _effective_tax_rate(
            symbol=position.symbol,
            trailing_start=trailing_start,
            end_date=history_end_date,
            cash_rows=dataset.cash_transactions,
            accruals=window_accruals,
        )
        estimated_net = (
            None
            if effective_tax_rate is None
            else estimated_gross * (1.0 - effective_tax_rate)
        )
        holdings.append(
            AnnualDividendHolding(
                symbol=position.symbol,
                quantity=quantity,
                currency=position.currency.upper(),
                fx_rate_to_base=position.fx_rate_to_base,
                trailing_gross_rate=trailing_rate,
                effective_tax_rate=effective_tax_rate,
                estimated_gross=estimated_gross,
                estimated_net=estimated_net,
                base_estimated_gross=_converted(
                    estimated_gross, position.fx_rate_to_base
                ),
                base_estimated_net=_converted(
                    estimated_net, position.fx_rate_to_base
                ),
            )
        )
        if position.position_value is None or position.fx_rate_to_base is None:
            denominator_complete = False
            limitations.append(
                f"Annual yield excludes an unavailable base market value for "
                f"{position.symbol}."
            )
        else:
            denominator_values.append(
                abs(position.position_value) * position.fx_rate_to_base
            )
        if estimated_gross > 0 and effective_tax_rate is None:
            limitations.append(
                f"Annual net estimate for {position.symbol} is unavailable because "
                "trailing realized withholding history is incomplete."
            )

    base_gross_values = [
        holding.base_estimated_gross
        for holding in holdings
        if holding.base_estimated_gross is not None
    ]
    estimated_base_gross = (
        0.0
        if not holdings
        else (sum(base_gross_values) if base_gross_values else None)
    )
    paying_holdings = [holding for holding in holdings if holding.estimated_gross > 0]
    net_complete = all(
        holding.base_estimated_net is not None for holding in paying_holdings
    )
    estimated_base_net = (
        sum(
            holding.base_estimated_net
            for holding in paying_holdings
            if holding.base_estimated_net is not None
        )
        if net_complete
        else None
    )
    eligible_base_market_value = (
        sum(denominator_values) if denominator_complete else None
    )
    numerator_complete = all(
        holding.base_estimated_gross is not None for holding in holdings
    )
    portfolio_yield = (
        estimated_base_gross / eligible_base_market_value
        if numerator_complete
        and estimated_base_gross is not None
        and eligible_base_market_value is not None
        and eligible_base_market_value > 0
        else None
    )
    history_days = _history_days_covered(
        history_start_date,
        history_coverage_end_date,
        history_end_date,
    )
    return AnnualDividendEstimate(
        holdings=holdings,
        estimated_base_gross=estimated_base_gross,
        estimated_base_net=estimated_base_net,
        eligible_base_market_value=eligible_base_market_value,
        portfolio_estimated_gross_yield=portfolio_yield,
        history_days_covered=history_days,
        complete_history=history_days == 365,
    )


def _totals(
    lines: list[DividendIncomeLine],
    *,
    base: bool,
) -> DividendTotals:
    """Aggregate known line components without substituting zero for nulls."""
    if not lines:
        return DividendTotals()
    prefix = "base_" if base else ""

    def component(name: str) -> float | None:
        """Sum known values for one component while retaining all-null state."""
        values = [getattr(line, f"{prefix}{name}") for line in lines]
        known = [value for value in values if value is not None]
        return None if not known else sum(known)

    return DividendTotals(
        gross=component("gross"),
        withholding_tax=component("withholding_tax"),
        fee=component("fee"),
        net=component("net"),
    )


def _group_totals(
    lines: list[DividendIncomeLine],
    *,
    field_name: Literal["currency", "country"],
    base: bool,
) -> dict[str, DividendTotals]:
    """Group dividend totals deterministically by one line attribution field."""
    grouped: dict[str, list[DividendIncomeLine]] = defaultdict(list)
    for line in lines:
        grouped[getattr(line, field_name)].append(line)
    return {
        key: _totals(grouped[key], base=base)
        for key in sorted(grouped)
    }


def _summary(
    realized: list[DividendIncomeLine],
    expected: list[DividendIncomeLine],
) -> DividendIncomeSummary:
    """Create status totals, attribution buckets, and realized contribution rank."""
    realized_country = [
        line for line in realized if line.fx_rate_to_base is not None
    ]
    expected_country = [
        line for line in expected if line.fx_rate_to_base is not None
    ]
    contributions: dict[str, float] = defaultdict(float)
    for line in realized:
        if line.base_net is not None:
            contributions[line.symbol] += line.base_net
    ranked = sorted(contributions.items(), key=lambda item: (-item[1], item[0]))
    return DividendIncomeSummary(
        realized=_totals(realized, base=True),
        expected=_totals(expected, base=True),
        by_currency=DividendAttribution(
            realized=_group_totals(
                realized, field_name="currency", base=False
            ),
            expected=_group_totals(
                expected, field_name="currency", base=False
            ),
        ),
        by_country=DividendAttribution(
            realized=_group_totals(
                realized_country, field_name="country", base=True
            ),
            expected=_group_totals(
                expected_country, field_name="country", base=True
            ),
        ),
        top_contributors=[
            DividendContribution(symbol=symbol, base_net=base_net)
            for symbol, base_net in ranked
        ],
    )


def build_dividend_income_report(
    dataset: FlexDividendDataset,
    start_date: date,
    end_date: date,
    coverage_note: str | None = None,
    history_start_date: date | None = None,
    history_end_date: date | None = None,
) -> DividendIncomeReport:
    """Build a deterministic dividend report without I/O or external state.

    ``history_start_date`` is the theoretical inclusive beginning of the selected
    Flex window. It defaults to ``start_date`` for compatibility with callers that
    only need the original four-argument interface. ``history_end_date`` bounds
    annual trailing facts separately from the requested output range and defaults
    to ``end_date``.
    """
    effective_history_start = history_start_date or start_date
    effective_history_end = history_end_date or end_date
    if dataset.statement_from_date is not None:
        effective_history_start = max(
            effective_history_start, dataset.statement_from_date
        )
    history_coverage_end = effective_history_end
    if dataset.statement_to_date is not None:
        history_coverage_end = min(
            history_coverage_end, dataset.statement_to_date
        )
    limitations: list[str] = []
    dividend_cash = _reduce_dividend_cash_lifecycle(
        dataset.cash_transactions,
        limitations=limitations,
    )
    accruals = _reduce_accrual_lifecycle(
        dataset.dividend_accruals,
        confirmed_cash=dividend_cash,
        limitations=limitations,
    )
    realized_associations = _associate_cash_to_accruals(dividend_cash, accruals)
    withholding_associations = _associate_withholdings(
        dividend_cash,
        dataset.cash_transactions,
        limitations=limitations,
    )
    realized: list[DividendIncomeLine] = []

    for cash_index, cash in enumerate(dividend_cash):
        if not start_date <= cash.ts.date() <= end_date:
            continue
        accrual_index, ambiguous = realized_associations[cash_index]
        accrual = None if accrual_index is None else accruals[accrual_index]
        country = _country_for(
            conid=cash.conid,
            symbol=cash.symbol,
            currency=cash.currency,
            instruments=dataset.instruments,
        )
        cash_withholding, withholding_ambiguous = withholding_associations[
            cash_index
        ]
        accrual_tax = (
            abs(accrual.tax)
            if accrual is not None and accrual.tax is not None
            else None
        )
        if (
            cash_withholding is not None
            and accrual_tax is not None
            and _materially_different(cash_withholding, accrual_tax)
        ):
            limitations.append(
                f"Realized dividend for {cash.symbol.strip()} used posted "
                f"withholding cash because it materially differed from the "
                "accrual tax; annual effective tax also uses the posted amount."
            )
        realized.append(
            _realized_line(
                cash,
                accrual,
                country=country,
                cash_withholding=cash_withholding,
                withholding_ambiguous=withholding_ambiguous,
                accrual_ambiguous=ambiguous,
            )
        )
        if withholding_ambiguous:
            if accrual_tax is None:
                limitations.append(
                    f"Realized dividend for {cash.symbol.strip()} had ambiguous "
                    "withholding cash; tax and unmatched net were not inferred."
                )
            else:
                limitations.append(
                    f"Realized dividend for {cash.symbol.strip()} had ambiguous "
                    "withholding cash; accrual tax was retained without cash "
                    "reconciliation."
                )
        if ambiguous:
            limitations.append(
                f"Realized dividend for {cash.symbol.strip()} had an ambiguous "
                "accrual match; accrual details were excluded."
            )
        elif accrual is None:
            limitations.append(
                f"Realized dividend for {cash.symbol.strip()} had no reliable "
                "accrual match; accrual details were excluded."
            )

    open_accruals = _reduce_accrual_lifecycle(dataset.open_dividend_accruals)
    open_associations = _associate_cash_to_accruals(dividend_cash, open_accruals)
    paid_open_indices = {
        accrual_index
        for accrual_index, _ in open_associations
        if accrual_index is not None
    }
    expected: list[DividendIncomeLine] = []
    for open_index, accrual in enumerate(open_accruals):
        if not start_date <= accrual.pay_date <= end_date:
            continue
        if open_index not in paid_open_indices:
            country = _country_for(
                conid=accrual.conid,
                symbol=accrual.symbol,
                currency=accrual.currency,
                instruments=dataset.instruments,
            )
            expected.append(
                _line_from_accrual(
                    accrual,
                    status="EXPECTED",
                    country=country,
                )
            )

    realized.sort(key=lambda row: (row.payment_date, row.symbol))
    expected.sort(key=lambda row: (row.payment_date, row.symbol))
    for line in realized + expected:
        native_values = (line.gross, line.withholding_tax, line.fee, line.net)
        if line.fx_rate_to_base is None and any(
            value is not None for value in native_values
        ):
            limitations.append(
                f"{line.status.title()} dividend for {line.symbol} has no Flex "
                "FX rate; native values were retained and base values excluded."
            )
    annual_estimate = _annual_estimate(
        dataset=dataset,
        accruals=accruals,
        history_end_date=effective_history_end,
        history_start_date=effective_history_start,
        history_coverage_end_date=history_coverage_end,
        limitations=limitations,
    )
    resolved_coverage_note = coverage_note
    if resolved_coverage_note is None and not annual_estimate.complete_history:
        resolved_coverage_note = (
            f"Flex statement coverage from {effective_history_start.isoformat()} "
            f"through {history_coverage_end.isoformat()} intersects "
            f"{annual_estimate.history_days_covered} of the trailing 365 days; "
            "the annual estimate is an unscaled lower bound."
        )
    return DividendIncomeReport(
        start_date=start_date,
        end_date=end_date,
        base_currency=dataset.base_currency,
        realized_dividends=realized,
        expected_dividends=expected,
        summary=_summary(realized, expected),
        annual_estimate=annual_estimate,
        coverage_note=resolved_coverage_note,
        data_limitations=limitations,
    )
