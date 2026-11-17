"""Flex Web Service client + XML parsers (read-only historical data).

Two-step handshake: SendRequest returns a ReferenceCode + statement URL,
GetStatement returns the report XML. Parsers convert the XML into typed
ib_common rows. Free of charge and covers history beyond the ~7-day
reqExecutions window.
"""
from __future__ import annotations
import re
import time
import xml.etree.ElementTree as ET
from datetime import date, datetime, timezone
import requests

from ib_common.redaction import redact_account_identifiers
from ib_common.schema import (
    Dividend,
    Execution,
    FlexCashTransaction,
    FlexDividendAccrual,
    FlexDividendDataset,
    FlexInstrument,
    FlexOpenPosition,
    FlexTrade,
)

_FLEX_BASE = (
    "https://ndcdyn.interactivebrokers.com/AccountManagement/FlexWebService"
)
_FLEX_HEADERS = {"User-Agent": "Python/3 ib-suite/0.1"}


class FlexServiceError(RuntimeError):
    """A credential-safe error returned by IBKR Flex Version 3."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"IBKR Flex error {code}: {message}")


class FlexQuerySchemaError(ValueError):
    """A credential-safe list of sections or fields absent from a Flex Query."""

    def __init__(
        self,
        missing_sections: list[str] | None = None,
        missing_fields: list[str] | None = None,
    ) -> None:
        """Build an error containing schema names but no statement values."""
        self.missing_sections = list(dict.fromkeys(missing_sections or []))
        self.missing_fields = list(dict.fromkeys(missing_fields or []))
        details: list[str] = []
        if self.missing_sections:
            details.append("sections: " + ", ".join(self.missing_sections))
        if self.missing_fields:
            details.append("fields: " + ", ".join(self.missing_fields))
        super().__init__("Flex Query schema is missing " + "; ".join(details))


def _redact_flex_message(message: str, sensitive_values: tuple[str, ...]) -> str:
    """Remove request credentials, identifiers, and URLs from a service message."""
    redacted = " ".join(message.split())
    for value in sorted(filter(None, sensitive_values), key=len, reverse=True):
        redacted = redacted.replace(value, "[REDACTED]")
    redacted = re.sub(r"https?://\S+", "[REDACTED_URL]", redacted)
    redacted = re.sub(
        r"(?i)\b(?:t|q)=[^&\s]+", "[REDACTED_PARAMETER]", redacted
    )
    return redact_account_identifiers(redacted)


def _raise_flex_error(
    root: ET.Element, sensitive_values: tuple[str, ...] = ()
) -> None:
    """Raise a sanitized service error when a Version 3 response failed."""
    raw_code = root.findtext("ErrorCode")
    if raw_code:
        stripped_code = raw_code.strip()
        code = stripped_code if stripped_code.isdigit() else "unknown"
        raw_message = root.findtext("ErrorMessage") or "Unknown Flex service error."
        message = _redact_flex_message(raw_message, sensitive_values)
        raise FlexServiceError(code, message)


def _parse_date(s: str) -> date:
    """Parse Flex date fields which may be 'YYYY-MM-DD' or 'YYYYMMDD'."""
    s = s.split(";")[0].strip()
    for fmt in ("%Y-%m-%d", "%Y%m%d"):
        try:
            return datetime.strptime(s[:10], fmt).date()
        except ValueError:
            continue
    return datetime.strptime(s[:10], "%Y-%m-%d").date()


def parse_flex_dividends(xml_text: str) -> list[Dividend]:
    """Extract dividend cash transactions into Dividend rows."""
    root = ET.fromstring(xml_text)
    out: list[Dividend] = []
    for ct in root.iter("CashTransaction"):
        if "Dividend" not in (ct.get("type") or ""):
            continue
        out.append(Dividend(
            symbol=ct.get("symbol", ""),
            ex_date=_parse_date(ct.get("dateTime", "1970-01-01")),
            pay_date=_parse_date(ct.get("settleDate")) if ct.get("settleDate") else None,
            gross=float(ct.get("amount", 0.0)),
            tax=0.0,
            currency=ct.get("currency", ""),
        ))
    return out


def _parse_datetime(value: str) -> datetime:
    """Parse a required Flex timestamp as UTC, tolerating date-only values."""
    normalized = value.strip()
    for fmt in (
        "%Y-%m-%d;%H:%M:%S",
        "%Y%m%d;%H%M%S",
        "%Y-%m-%d",
        "%Y%m%d",
    ):
        try:
            return datetime.strptime(normalized, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    raise ValueError(f"invalid Flex dateTime: {value!r}")


_DIVIDEND_SECTION_FIELDS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "AccountInformation": (
        ("AccountInformation",),
        ("accountId", "currency"),
    ),
    "CashTransactions": (
        ("CashTransaction",),
        (
            "accountId",
            "currency",
            "assetCategory",
            "fxRateToBase",
            "symbol",
            "description",
            "conid",
            "underlyingConid",
            "underlyingSymbol",
            "dateTime",
            "amount",
            "type",
            "tradeID",
            "code",
        ),
    ),
    "ChangeInDividendAccruals": (
        ("ChangeInDividendAccrual",),
        (
            "accountId",
            "currency",
            "assetCategory",
            "fxRateToBase",
            "symbol",
            "description",
            "conid",
            "date",
            "exDate",
            "payDate",
            "quantity",
            "tax",
            "fee",
            "grossRate",
            "grossAmount",
            "netAmount",
            "code",
            "reportDate",
        ),
    ),
    "OpenDividendAccruals": (
        ("OpenDividendAccrual",),
        (
            "accountId",
            "currency",
            "assetCategory",
            "fxRateToBase",
            "symbol",
            "conid",
            "exDate",
            "payDate",
            "quantity",
            "tax",
            "fee",
            "grossRate",
            "grossAmount",
            "netAmount",
            "code",
        ),
    ),
    "OpenPositions": (
        ("OpenPosition",),
        (
            "accountId",
            "currency",
            "assetCategory",
            "fxRateToBase",
            "symbol",
            "conid",
            "reportDate",
            "position",
            "multiplier",
            "markPrice",
            "positionValue",
            "side",
            "levelOfDetail",
        ),
    ),
    "FinancialInstrumentInformation": (
        ("SecurityInfo", "FinancialInstrumentInfo"),
        (
            "assetCategory",
            "symbol",
            "currency",
            "listingExchange",
            "description",
            "conid",
            "isin",
            "multiplier",
            "subCategory",
        ),
    ),
}

_DIVIDEND_SECTION_ALIASES: dict[str, tuple[str, ...]] = {
    "FinancialInstrumentInformation": (
        "SecuritiesInfo",
        "FinancialInstrumentInformation",
    ),
}


def _statement_scopes(root: ET.Element) -> list[ET.Element]:
    """Return each FlexStatement, or the root for a statement-shaped fragment."""
    statements = list(root.iter("FlexStatement"))
    return statements or [root]


def _section_rows(
    statement: ET.Element,
    section_name: str,
    row_names: tuple[str, ...],
) -> tuple[list[ET.Element], list[ET.Element]]:
    """Return matching section containers and their known record elements."""
    container_names = _DIVIDEND_SECTION_ALIASES.get(
        section_name, (section_name,)
    )
    if statement.tag in container_names:
        sections = [statement]
    else:
        sections = [
            section
            for container_name in container_names
            for section in statement.iter(container_name)
        ]
    if section_name == "AccountInformation":
        return sections, sections
    rows = [
        row
        for section in sections
        for row_name in row_names
        for row in section.iter(row_name)
    ]
    return sections, rows


def _is_relevant_cash_element(row: ET.Element) -> bool:
    """Return whether a cash row can prove dividend income or withholding."""
    transaction_type = (row.get("type") or "").casefold()
    return "dividend" in transaction_type or "withholding" in transaction_type


def _validate_dividend_schema(root: ET.Element) -> None:
    """Reject omitted Flex sections and selected fields without exposing values."""
    missing_sections: list[str] = []
    missing_fields: list[str] = []
    for statement in _statement_scopes(root):
        for section_name, (row_names, field_names) in _DIVIDEND_SECTION_FIELDS.items():
            sections, rows = _section_rows(statement, section_name, row_names)
            if not sections:
                missing_sections.append(section_name)
                continue
            validation_rows = rows
            if section_name == "CashTransactions":
                for row in rows:
                    if "type" not in row.attrib:
                        missing_fields.append("CashTransactions.type")
                validation_rows = [
                    row for row in rows if _is_relevant_cash_element(row)
                ]
            for row in validation_rows:
                missing_fields.extend(
                    f"{section_name}.{field_name}"
                    for field_name in field_names
                    if field_name not in row.attrib
                )
    if missing_sections or missing_fields:
        raise FlexQuerySchemaError(missing_sections, missing_fields)


def _required_section_value(
    element: ET.Element, section_name: str, field_name: str
) -> str:
    """Return one non-blank Flex field or raise a credential-safe schema error."""
    value = element.get(field_name)
    if value is None or not value.strip():
        raise FlexQuerySchemaError(
            missing_fields=[f"{section_name}.{field_name}"]
        )
    return value.strip()


def _present_section_value(
    element: ET.Element, section_name: str, field_name: str
) -> str:
    """Return a selected Flex field that may contain a blank row value."""
    value = element.get(field_name)
    if value is None:
        raise FlexQuerySchemaError(
            missing_fields=[f"{section_name}.{field_name}"]
        )
    return value.strip()


def _optional_section_text(
    element: ET.Element, section_name: str, field_name: str
) -> str | None:
    """Normalize a selected blank Flex text fact to None."""
    return _present_section_value(element, section_name, field_name) or None


def _optional_unselected_text(element: ET.Element, field_name: str) -> str | None:
    """Normalize a non-required blank or omitted Flex text fact to None."""
    value = element.get(field_name)
    return value.strip() if value is not None and value.strip() else None


def _optional_section_float(
    element: ET.Element, section_name: str, field_name: str
) -> float | None:
    """Parse a selected nullable numeric fact without echoing invalid content."""
    value = _present_section_value(element, section_name, field_name)
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        raise ValueError(
            f"Flex {section_name} field {field_name} is invalid"
        ) from None


def _section_date(
    element: ET.Element, section_name: str, field_name: str
) -> date:
    """Parse a required Flex date without echoing invalid content."""
    value = _required_section_value(element, section_name, field_name)
    try:
        return _parse_date(value)
    except ValueError:
        raise ValueError(
            f"Flex {section_name} field {field_name} is invalid"
        ) from None


def _optional_section_date(
    element: ET.Element, section_name: str, field_name: str
) -> date | None:
    """Parse a selected nullable Flex date, normalizing a blank value to None."""
    value = _present_section_value(element, section_name, field_name)
    if not value:
        return None
    try:
        return _parse_date(value)
    except ValueError:
        raise ValueError(
            f"Flex {section_name} field {field_name} is invalid"
        ) from None


def _section_datetime(
    element: ET.Element, section_name: str, field_name: str
) -> datetime:
    """Parse a required Flex timestamp without echoing invalid content."""
    value = _required_section_value(element, section_name, field_name)
    try:
        return _parse_datetime(value)
    except ValueError:
        raise ValueError(
            f"Flex {section_name} field {field_name} is invalid"
        ) from None


def _all_dividend_rows(
    root: ET.Element, section_name: str
) -> list[ET.Element]:
    """Collect all known row element names for one validated section."""
    row_names, _ = _DIVIDEND_SECTION_FIELDS[section_name]
    rows: list[ET.Element] = []
    for statement in _statement_scopes(root):
        _, statement_rows = _section_rows(statement, section_name, row_names)
        rows.extend(statement_rows)
    if section_name == "CashTransactions":
        return [row for row in rows if _is_relevant_cash_element(row)]
    return rows


def _statement_period(root: ET.Element) -> tuple[date | None, date | None]:
    """Return the conservative intersection of all statement coverage periods."""
    statements = list(root.iter("FlexStatement"))
    if not statements:
        return None, None
    starts = [
        _section_date(statement, "FlexStatement", "fromDate")
        for statement in statements
    ]
    ends = [
        _section_date(statement, "FlexStatement", "toDate")
        for statement in statements
    ]
    coverage_start = max(starts)
    coverage_end = min(ends)
    if coverage_start > coverage_end:
        raise ValueError("FlexStatement coverage periods do not overlap")
    return coverage_start, coverage_end


def _parse_cash_transaction(element: ET.Element) -> FlexCashTransaction:
    """Parse one validated CashTransactions record without changing signs."""
    section = "CashTransactions"
    return FlexCashTransaction(
        account_id=_required_section_value(element, section, "accountId"),
        currency=_required_section_value(element, section, "currency").upper(),
        asset_class=_present_section_value(
            element, section, "assetCategory"
        ).upper(),
        fx_rate_to_base=_optional_section_float(
            element, section, "fxRateToBase"
        ),
        symbol=_present_section_value(element, section, "symbol"),
        description=_optional_section_text(element, section, "description"),
        conid=_optional_section_text(element, section, "conid"),
        underlying_conid=_optional_section_text(
            element, section, "underlyingConid"
        ),
        underlying_symbol=_optional_section_text(
            element, section, "underlyingSymbol"
        ),
        ts=_section_datetime(element, section, "dateTime"),
        amount=_optional_section_float(element, section, "amount"),
        transaction_type=_required_section_value(element, section, "type"),
        trade_id=_optional_section_text(element, section, "tradeID"),
        code=_present_section_value(element, section, "code").upper(),
    )


def _parse_dividend_accrual(
    element: ET.Element, section: str
) -> FlexDividendAccrual:
    """Parse one validated changed or open dividend accrual record."""
    is_change = section == "ChangeInDividendAccruals"
    return FlexDividendAccrual(
        account_id=_required_section_value(element, section, "accountId"),
        currency=_required_section_value(element, section, "currency").upper(),
        asset_class=_required_section_value(
            element, section, "assetCategory"
        ).upper(),
        fx_rate_to_base=_optional_section_float(
            element, section, "fxRateToBase"
        ),
        symbol=_required_section_value(element, section, "symbol"),
        description=(
            _optional_section_text(element, section, "description")
            if is_change
            else _optional_unselected_text(element, "description")
        ),
        conid=_optional_section_text(element, section, "conid"),
        accrual_date=(
            _optional_section_date(element, section, "date")
            if is_change
            else None
        ),
        ex_date=_section_date(element, section, "exDate"),
        pay_date=_section_date(element, section, "payDate"),
        quantity=_optional_section_float(element, section, "quantity"),
        tax=_optional_section_float(element, section, "tax"),
        fee=_optional_section_float(element, section, "fee"),
        gross_rate=_optional_section_float(element, section, "grossRate"),
        gross_amount=_optional_section_float(element, section, "grossAmount"),
        net_amount=_optional_section_float(element, section, "netAmount"),
        code=_present_section_value(element, section, "code").upper(),
        report_date=(
            _optional_section_date(element, section, "reportDate")
            if is_change
            else None
        ),
    )


def _parse_open_position(element: ET.Element) -> FlexOpenPosition:
    """Parse one validated OpenPositions record without filtering it."""
    section = "OpenPositions"
    return FlexOpenPosition(
        account_id=_required_section_value(element, section, "accountId"),
        currency=_required_section_value(element, section, "currency").upper(),
        asset_class=_required_section_value(
            element, section, "assetCategory"
        ).upper(),
        fx_rate_to_base=_optional_section_float(
            element, section, "fxRateToBase"
        ),
        symbol=_required_section_value(element, section, "symbol"),
        conid=_optional_section_text(element, section, "conid"),
        report_date=_section_date(element, section, "reportDate"),
        quantity=_optional_section_float(element, section, "position"),
        multiplier=_optional_section_float(element, section, "multiplier"),
        mark_price=_optional_section_float(element, section, "markPrice"),
        position_value=_optional_section_float(element, section, "positionValue"),
        side=_required_section_value(element, section, "side").upper(),
        level_of_detail=_required_section_value(
            element, section, "levelOfDetail"
        ).upper(),
    )


def _parse_instrument(element: ET.Element) -> FlexInstrument:
    """Parse one validated FinancialInstrumentInformation record."""
    section = "FinancialInstrumentInformation"
    return FlexInstrument(
        asset_class=_required_section_value(
            element, section, "assetCategory"
        ).upper(),
        symbol=_required_section_value(element, section, "symbol"),
        currency=_required_section_value(element, section, "currency").upper(),
        listing_exchange=(
            value.upper()
            if (value := _optional_section_text(element, section, "listingExchange"))
            else None
        ),
        description=_optional_section_text(element, section, "description"),
        conid=_optional_section_text(element, section, "conid"),
        isin=(
            value.upper()
            if (value := _optional_section_text(element, section, "isin"))
            else None
        ),
        multiplier=_optional_section_float(element, section, "multiplier"),
        security_subtype=(
            value.upper()
            if (value := _optional_section_text(element, section, "subCategory"))
            else None
        ),
    )


def parse_flex_dividend_dataset(xml_text: str) -> FlexDividendDataset:
    """Parse all six required Flex dividend sections into typed raw records."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        raise ValueError("Flex dividend XML is invalid") from None
    _validate_dividend_schema(root)

    account_rows = _all_dividend_rows(root, "AccountInformation")
    base_currencies = {
        _required_section_value(row, "AccountInformation", "currency").upper()
        for row in account_rows
    }
    if len(base_currencies) != 1:
        raise ValueError("Flex AccountInformation field currency is inconsistent")
    statement_from_date, statement_to_date = _statement_period(root)

    change_section = "ChangeInDividendAccruals"
    open_section = "OpenDividendAccruals"
    return FlexDividendDataset(
        base_currency=next(iter(base_currencies)),
        statement_from_date=statement_from_date,
        statement_to_date=statement_to_date,
        cash_transactions=[
            _parse_cash_transaction(row)
            for row in _all_dividend_rows(root, "CashTransactions")
        ],
        dividend_accruals=[
            _parse_dividend_accrual(row, change_section)
            for row in _all_dividend_rows(root, change_section)
        ],
        open_dividend_accruals=[
            _parse_dividend_accrual(row, open_section)
            for row in _all_dividend_rows(root, open_section)
        ],
        open_positions=[
            _parse_open_position(row)
            for row in _all_dividend_rows(root, "OpenPositions")
        ],
        instruments=[
            _parse_instrument(row)
            for row in _all_dividend_rows(root, "FinancialInstrumentInformation")
        ],
    )


def _required(trade: ET.Element, name: str) -> str:
    """Return one required Flex Trade attribute with a configuration hint."""
    value = trade.get(name)
    if value is None or not value.strip():
        raise ValueError(
            f"Flex Trade field {name!r} is missing; enable it in the Flex Query Trades section"
        )
    return value


def _present(trade: ET.Element, name: str) -> str:
    """Return an attribute that may be empty, rejecting an omitted query field."""
    value = trade.get(name)
    if value is None:
        raise ValueError(
            f"Flex Trade field {name!r} is missing; enable it in the Flex Query Trades section"
        )
    return value


def parse_flex_trade_records(xml_text: str) -> list[FlexTrade]:
    """Extract complete Flex execution rows for the trade-history skill."""
    root = ET.fromstring(xml_text)
    rows: list[FlexTrade] = []
    for trade in root.iter("Trade"):
        fx_text = trade.get("fxRateToBase")
        multiplier_text = (trade.get("multiplier") or "").strip()
        rows.append(FlexTrade(
            exec_id=_required(trade, "tradeID"),
            ts=_parse_datetime(_required(trade, "dateTime")),
            symbol=_required(trade, "symbol"),
            side=_required(trade, "buySell").upper(),
            quantity=abs(float(_required(trade, "quantity"))),
            price=float(_required(trade, "tradePrice")),
            commission=abs(float(_required(trade, "ibCommission"))),
            currency=_required(trade, "currency").upper(),
            commission_currency=_required(trade, "ibCommissionCurrency").upper(),
            multiplier=float(multiplier_text) if multiplier_text else 1.0,
            order_type=_present(trade, "orderType"),
            exchange=_required(trade, "exchange"),
            open_close=(trade.get("openCloseIndicator") or "").upper(),
            realized_pnl=float(_required(trade, "fifoPnlRealized")),
            fx_rate_to_base=float(fx_text) if fx_text not in (None, "") else None,
        ))
    return rows


def parse_flex_trades(xml_text: str) -> list[Execution]:
    """Extract trades into Execution rows."""
    root = ET.fromstring(xml_text)
    out: list[Execution] = []
    for tr in root.iter("Trade"):
        out.append(Execution(
            exec_id=tr.get("tradeID", ""),
            symbol=tr.get("symbol", ""),
            side=tr.get("buySell", ""),
            quantity=abs(float(tr.get("quantity", 0.0))),
            price=float(tr.get("tradePrice", 0.0)),
            commission=abs(float(tr.get("ibCommission", 0.0))),
            ts=datetime.combine(_parse_date(tr.get("tradeDate", "1970-01-01")),
                                datetime.min.time()),
        ))
    return out


def fetch_flex_report(token: str, query_id: str, http_get=requests.get,
                      poll_interval: float = 1.0, max_polls: int = 10) -> str:
    """Run the Flex two-step handshake and return raw statement XML."""
    sensitive_values = (token, query_id)
    try:
        send = http_get(
            f"{_FLEX_BASE}/SendRequest",
            params={"t": token, "q": query_id, "v": "3"},
            headers=_FLEX_HEADERS,
        )
        send.raise_for_status()
    except requests.RequestException as exc:
        message = _redact_flex_message(str(exc), sensitive_values)
        raise FlexServiceError(
            "transport", f"SendRequest failed: {message or 'request error'}"
        ) from None
    try:
        root = ET.fromstring(send.text)
    except ET.ParseError:
        raise FlexServiceError(
            "malformed_response", "SendRequest returned malformed XML."
        ) from None
    _raise_flex_error(root, (token, query_id))
    ref = root.findtext("ReferenceCode")
    url = (
        root.findtext("url")
        or root.findtext("Url")
        or f"{_FLEX_BASE}/GetStatement"
    )
    if not ref:
        raise FlexServiceError(
            "handshake", "SendRequest response omitted the reference code."
        )

    statement_root: ET.Element | None = None
    for _ in range(max_polls):
        try:
            stmt = http_get(
                url,
                params={"t": token, "q": ref, "v": "3"},
                headers=_FLEX_HEADERS,
            )
            stmt.raise_for_status()
        except requests.RequestException as exc:
            message = _redact_flex_message(
                str(exc), (token, query_id, ref)
            )
            raise FlexServiceError(
                "transport", f"GetStatement failed: {message or 'request error'}"
            ) from None
        try:
            statement_root = ET.fromstring(stmt.text)
        except ET.ParseError:
            raise FlexServiceError(
                "malformed_response", "GetStatement returned malformed XML."
            ) from None
        if "Statement generation in progress" in stmt.text:
            time.sleep(poll_interval)
            continue
        _raise_flex_error(statement_root, (token, query_id, ref))
        return stmt.text
    if statement_root is not None:
        _raise_flex_error(statement_root, (token, query_id, ref))
    raise FlexServiceError(
        "1019", "Statement generation did not complete within the polling limit."
    )
