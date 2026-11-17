"""Read-only IBKR Flex dividend-income command-line entrypoint."""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import time
import uuid
import xml.etree.ElementTree as ET
from collections.abc import Callable
from datetime import date, timedelta
from pathlib import Path

import requests
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ib-gateway" / "scripts"))

from flex_fetch import (  # noqa: E402
    FlexQuerySchemaError,
    FlexServiceError,
    fetch_flex_report,
    parse_flex_dividend_dataset,
)
from ib_common.config import load_config  # noqa: E402
from ib_common.dividend_income import build_dividend_income_report  # noqa: E402
from ib_common.flex import parse_iso_date, select_flex_window  # noqa: E402
from ib_common.redaction import redact_account_identifiers  # noqa: E402

LOGGER = logging.getLogger("ib_dividend_income")
GUIDE = "flex-query-setup.md"


def _state(
    status: str,
    missing: list[str],
    run_id: str,
    *,
    message: str | None = None,
) -> dict[str, object]:
    """Build a stable JSON-safe setup state containing only schema names."""
    payload: dict[str, object] = {
        "status": status,
        "missing": missing,
        "guide": GUIDE,
        "run_id": run_id,
    }
    if message is not None:
        payload["message"] = message
    return payload


def _validation_missing(exc: ValidationError) -> list[str]:
    """Map validation locations to stable names without inspecting raw inputs."""
    locations = [
        tuple(error.get("loc", ()))
        for error in exc.errors(
            include_url=False,
            include_context=False,
            include_input=False,
        )
    ]
    if any(
        location[:2] == ("flex", "dividend_query_ids") for location in locations
    ):
        return ["flex.dividend_query_ids"]
    return ["config"]


def _sanitize(message: str, sensitive_values: tuple[str, ...] = ()) -> str:
    """Remove credentials, identifiers, URLs, parameters, and XML from log text."""
    normalized = " ".join(message.split())
    if "<" in normalized or ">" in normalized:
        return "sensitive response details redacted"
    for value in sorted(filter(None, sensitive_values), key=len, reverse=True):
        normalized = normalized.replace(value, "[REDACTED]")
    normalized = re.sub(r"https?://\S+", "[REDACTED_URL]", normalized)
    normalized = re.sub(
        r"(?i)\b(?:t|q)=[^&\s]+", "[REDACTED_PARAMETER]", normalized
    )
    normalized = re.sub(
        r"(?i)\b(?:reference[ _]?code)(?:\s*[:=]\s*|\s+)[^\s&,;]+",
        "reference_code=[REDACTED]",
        normalized,
    )
    return redact_account_identifiers(normalized)


def _log(
    level: int,
    event: str,
    *,
    run_id: str,
    fields: dict[str, object] | None = None,
) -> None:
    """Write one sanitized structured event without serializing report rows."""
    safe_fields = fields or {}
    suffix = " ".join(
        f"{key}={_sanitize(str(value))}" for key, value in safe_fields.items()
    )
    message = f"event={event} run_id={_sanitize(run_id)}"
    if suffix:
        message = f"{message} {suffix}"
    LOGGER.log(level, message)


def dividend_income(
    config_path: str,
    start: str,
    end: str,
    fetcher: Callable[[str, str], str] = fetch_flex_report,
    today: date | None = None,
    run_id: str | None = None,
) -> dict:
    """Fetch one strict Flex window and return a JSON-safe dividend report."""
    started = time.monotonic()
    resolved_run_id = run_id or uuid.uuid4().hex
    _log(logging.INFO, "run_started", run_id=resolved_run_id)

    try:
        cfg = load_config(config_path)
    except ValidationError as exc:
        missing = _validation_missing(exc)
        _log(
            logging.INFO,
            "setup_required",
            run_id=resolved_run_id,
            fields={"missing_count": len(missing)},
        )
        return _state(
            "setup_required",
            missing,
            resolved_run_id,
            message="Flex configuration is invalid",
        )
    if not cfg.flex.token:
        _log(logging.INFO, "setup_required", run_id=resolved_run_id)
        return _state("setup_required", ["flex.token"], resolved_run_id)

    if any(
        not query_id.strip() for query_id in cfg.flex.dividend_query_ids.values()
    ):
        _log(logging.INFO, "setup_required", run_id=resolved_run_id)
        return _state("setup_required", ["flex.dividend_query_ids"], resolved_run_id)

    if not cfg.flex.dividend_query_ids:
        _log(logging.INFO, "setup_required", run_id=resolved_run_id)
        return _state("setup_required", ["flex.dividend_query_ids"], resolved_run_id)

    start_date = parse_iso_date(start)
    end_date = parse_iso_date(end)
    if start_date > end_date:
        raise ValueError("--start-date must be on or before --end-date")
    resolved_today = today or date.today()
    history_end_date = min(end_date, resolved_today)
    required_start = min(
        start_date,
        history_end_date - timedelta(days=364),
    )
    required_days = (resolved_today - required_start).days + 1
    try:
        window, query_id, _ = select_flex_window(
            cfg.flex.dividend_query_ids,
            required_start,
            resolved_today,
            allow_partial=False,
        )
    except ValueError:
        _log(
            logging.INFO,
            "coverage_required",
            run_id=resolved_run_id,
            fields={"required_days": required_days},
        )
        return _state(
            "coverage_required",
            [f"flex.dividend_query_ids.{required_days}"],
            resolved_run_id,
        )

    _log(
        logging.INFO,
        "window_selected",
        run_id=resolved_run_id,
        fields={"window": window},
    )
    try:
        xml_text = fetcher(cfg.flex.token, query_id)
        dataset = parse_flex_dividend_dataset(xml_text)
    except FlexQuerySchemaError as exc:
        missing = exc.missing_sections + exc.missing_fields
        _log(
            logging.INFO,
            "query_update_required",
            run_id=resolved_run_id,
            fields={"missing_count": len(missing)},
        )
        return _state("query_update_required", missing, resolved_run_id)
    except (FlexServiceError, requests.RequestException, ET.ParseError) as exc:
        safe_error = _sanitize(str(exc), (cfg.flex.token, query_id))
        _log(
            logging.ERROR,
            "flex_service_error",
            run_id=resolved_run_id,
            fields={"error": safe_error},
        )
        return {
            "status": "error",
            "message": "Flex report retrieval failed; verify setup and service status",
            "run_id": resolved_run_id,
        }
    except (RuntimeError, ValueError) as exc:
        safe_error = _sanitize(str(exc), (cfg.flex.token, query_id))
        _log(
            logging.ERROR,
            "flex_processing_error",
            run_id=resolved_run_id,
            fields={"error": safe_error},
        )
        return {
            "status": "error",
            "message": "Flex report processing failed; verify query setup",
            "run_id": resolved_run_id,
        }

    _log(
        logging.INFO,
        "sections_parsed",
        run_id=resolved_run_id,
        fields={
            "cash_transactions": len(dataset.cash_transactions),
            "dividend_accruals": len(dataset.dividend_accruals),
            "open_dividend_accruals": len(dataset.open_dividend_accruals),
            "open_positions": len(dataset.open_positions),
            "instruments": len(dataset.instruments),
        },
    )
    _log(
        logging.INFO,
        "coverage_observed",
        run_id=resolved_run_id,
        fields={
            "from_date": dataset.statement_from_date or "unavailable",
            "to_date": dataset.statement_to_date or "unavailable",
            "history_end": history_end_date,
        },
    )
    if window.isdigit():
        theoretical_start = resolved_today - timedelta(days=int(window) - 1)
    elif window == "mtd":
        theoretical_start = resolved_today.replace(day=1)
    else:
        theoretical_start = date(resolved_today.year, 1, 1)
    report_model = build_dividend_income_report(
        dataset,
        start_date,
        end_date,
        history_start_date=theoretical_start,
        history_end_date=history_end_date,
    )
    matched_count = sum(
        line.gross is not None or line.quantity is not None
        for line in report_model.realized_dividends
    )
    _log(
        logging.INFO,
        "association_completed",
        run_id=resolved_run_id,
        fields={
            "realized_count": len(report_model.realized_dividends),
            "matched_count": matched_count,
            "unmatched_count": (
                len(report_model.realized_dividends) - matched_count
            ),
        },
    )
    _log(
        logging.INFO,
        "calculation_completed",
        run_id=resolved_run_id,
        fields={
            "realized_count": len(report_model.realized_dividends),
            "expected_count": len(report_model.expected_dividends),
            "annual_holding_count": len(report_model.annual_estimate.holdings),
            "history_days_covered": (
                report_model.annual_estimate.history_days_covered
            ),
            "limitation_count": len(report_model.data_limitations),
        },
    )
    report = report_model.model_dump(mode="json")
    report["run_id"] = resolved_run_id
    elapsed_ms = round((time.monotonic() - started) * 1000)
    _log(
        logging.INFO,
        "run_completed",
        run_id=resolved_run_id,
        fields={"elapsed_ms": elapsed_ms},
    )
    return report


def _configure_logging(level_name: str) -> None:
    """Configure one stderr-only handler at the requested verbosity."""
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    LOGGER.handlers.clear()
    LOGGER.addHandler(handler)
    LOGGER.setLevel(getattr(logging, level_name))
    LOGGER.propagate = False


def main(
    fetcher: Callable[[str, str], str] = fetch_flex_report,
) -> int:
    """Parse CLI flags, print one JSON object, and return a process status."""
    parser = argparse.ArgumentParser(
        description="Read-only IBKR Flex dividend income"
    )
    parser.add_argument("--config", required=True, help="path to config.yaml")
    parser.add_argument(
        "--start-date", required=True, help="inclusive YYYY-MM-DD start date"
    )
    parser.add_argument(
        "--end-date", required=True, help="inclusive YYYY-MM-DD end date"
    )
    parser.add_argument(
        "--log-level",
        choices=("INFO", "DEBUG"),
        default="INFO",
        help="stderr logging verbosity",
    )
    args = parser.parse_args()
    _configure_logging(args.log_level)
    run_id = uuid.uuid4().hex
    try:
        payload = dividend_income(
            args.config,
            args.start_date,
            args.end_date,
            fetcher=fetcher,
            run_id=run_id,
        )
    except (FileNotFoundError, PermissionError, IsADirectoryError, ValueError):
        _log(
            logging.ERROR,
            "cli_error",
            run_id=run_id,
            fields={"error": "invalid_local_input"},
        )
        payload = {
            "status": "error",
            "message": "Invalid local configuration or date range",
            "run_id": run_id,
        }
    print(json.dumps(payload, allow_nan=False))
    return 2 if "status" in payload else 0


if __name__ == "__main__":
    raise SystemExit(main())
