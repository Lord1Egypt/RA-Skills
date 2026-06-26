"""
mcp_connector/client.py
════════════════════════════════════════════════════════════════════════════════
IC Trade Navigator — Local Client  (request + display only)

PURPOSE
────────
This file is the ONLY entry point for users running the connector on their
local machine.  It orchestrates three steps:

  1. READ   — load part number(s) from local data/inventory.xlsx using the
              GenericErpReader (never reads pricing columns)
  2. FETCH  — call GET /v1/quote on the remote api_engine (sends only
              part_number, qty, lang — no ERP data)
  3. DISPLAY — merge remote market intelligence with local ERP stock and
               render a human-readable combined view

PRIVACY GUARANTEE
──────────────────
This module contains NO pricing logic, NO risk scoring, and NO scraper calls.
It only: (a) sends part numbers to the server, (b) receives sanitised market
data back, and (c) joins it with local stock counts for display.

Floor prices, purchase costs, and ERP financial data NEVER leave this machine.

USAGE
──────
  # Single quote — interactive
  python -m mcp_connector.client quote STM32L412CBU6 --qty 500 --lang zh-TW

  # Batch quote — reads from data/inventory.xlsx
  python -m mcp_connector.client batch data/inventory.xlsx

  # Batch quote with custom column mapping
  python -m mcp_connector.client batch myfile.xlsx \\
      --col-pn "Part Number" --col-qty "QTY" --col-status "Status"

  # Output as JSON (for ERP integration)
  python -m mcp_connector.client quote STM32L412CBU6 --json

ENVIRONMENT VARIABLES (set in .env or shell)
─────────────────────────────────────────────
  QUOTE_ENGINE_URL      — https://your-engine.example.com
  QUOTE_ENGINE_API_KEY  — your X-API-Key credential
  ERP_EXCEL_PATH        — path to your ERP Excel file (default: data/inventory.xlsx)
  CONNECTOR_TIMEOUT     — HTTP timeout in seconds (default: 15)
"""
from __future__ import annotations

import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mcp_connector.api_client import QuoteApiError, RemoteQuote, fetch_quote
from mcp_connector.config import config
from mcp_connector.erp_reader import ErpRecord
from mcp_connector.erp_reader_generic import ColumnMap, GenericErpReader
from mcp_connector.merger import MergedQuoteView, format_as_dict, format_as_text, merge

log = logging.getLogger("mcp_connector.client")

# ── Default inventory file path ───────────────────────────────────────────────
_DEFAULT_INVENTORY = Path("data") / "inventory.xlsx"

# ── Default column mapping for data/inventory.xlsx ───────────────────────────
# Users can override via CLI flags or by passing a custom ColumnMap.
DEFAULT_COLUMN_MAP = ColumnMap(
    part_number  = "Part Number",
    stock_qty    = "Stock Qty",
    supply_status= "Status",
    package      = "Package",
    date_code    = "Date Code",
)


# ════════════════════════════════════════════════════════════════════════════════
# QuoteClient — main façade
# ════════════════════════════════════════════════════════════════════════════════

class QuoteClient:
    """
    Façade that wires together ERP reading, API fetching, and display.

    All intelligence (risk scoring, advisory generation, price validation)
    lives server-side.  This class only handles:
      • reading local inventory files
      • calling fetch_quote()
      • merging and formatting results

    Parameters
    ──────────
    inventory_path   Path to the local inventory Excel/CSV file.
    column_map       ColumnMap declaring which Excel columns hold what data.
    default_lang     Default advisory language (en | de | ja | zh-TW | fr | ko).
    """

    def __init__(
        self,
        inventory_path: str | Path = _DEFAULT_INVENTORY,
        column_map: ColumnMap = DEFAULT_COLUMN_MAP,
        default_lang: str = "en",
    ) -> None:
        self.inventory_path = Path(inventory_path)
        self.column_map     = column_map
        self.default_lang   = default_lang
        self._erp_reader    = GenericErpReader(column_map)

        # Log any config warnings at startup (missing keys, missing file)
        for warn in config.validate():
            log.warning("Config: %s", warn)

    # ── Single quote ──────────────────────────────────────────────────────────

    def quote(
        self,
        part_number: str,
        qty: int = 0,
        lang: str | None = None,
        customer_id: str = "",
    ) -> MergedQuoteView:
        """
        Fetch market data for one part number and merge with local ERP stock.

        Parameters
        ──────────
        part_number   IC part number (any case; normalised by server).
        qty           Requested quantity (0 = unspecified).
        lang          Advisory language; falls back to self.default_lang.
        customer_id   Opaque ID for server-side logging (optional).

        Returns
        ───────
        MergedQuoteView — combined market + local ERP data.

        Raises
        ──────
        QuoteApiError — engine is unreachable or returns an error.
        """
        effective_lang = lang or self.default_lang
        part_upper     = part_number.strip().upper()

        # ── Step 1: Read local ERP ────────────────────────────────────────────
        local = self._read_local(part_upper)

        # ── Step 2: Fetch from remote engine ─────────────────────────────────
        remote = fetch_quote(
            part_number = part_upper,
            qty         = qty,
            customer_id = customer_id,
            lang        = effective_lang,
        )

        # ── Step 3: Merge ─────────────────────────────────────────────────────
        return merge(remote, local, requested_qty=qty)

    # ── Batch quote (from BOM / inventory file) ───────────────────────────────

    def quote_batch(
        self,
        source_path: str | Path | None = None,
        lang: str | None = None,
        customer_id: str = "",
    ) -> list[tuple[str, MergedQuoteView | QuoteApiError]]:
        """
        Read all parts from an Excel/CSV file and quote them in sequence.

        Expected columns in the source file:
          Part Number — the IC model number (required)
          Stock Qty   — local available quantity (optional)
          Status      — supply / lifecycle status label (optional)

        Parameters
        ──────────
        source_path   Excel or CSV file path.  Defaults to data/inventory.xlsx.
        lang          Advisory language for all quotes in this batch.
        customer_id   Optional batch customer ID for server-side logging.

        Returns
        ───────
        List of (part_number, MergedQuoteView | QuoteApiError) tuples.
        Failed individual parts are returned as QuoteApiError, not raised.
        """
        path           = Path(source_path) if source_path else self.inventory_path
        effective_lang = lang or self.default_lang

        rows = self._load_batch_rows(path)
        if not rows:
            log.warning("No parts loaded from %s", path)
            return []

        results: list[tuple[str, MergedQuoteView | QuoteApiError]] = []

        for pn, qty in rows:
            log.info("Batch quoting: %s qty=%d", pn, qty)
            try:
                view = self.quote(pn, qty=qty, lang=effective_lang, customer_id=customer_id)
                results.append((pn, view))
            except QuoteApiError as exc:
                log.error("Failed to quote %s: %s", pn, exc)
                results.append((pn, exc))

        return results

    # ── Private helpers ───────────────────────────────────────────────────────

    def _read_local(self, part_number: str) -> ErpRecord:
        """
        Look up the part in the local ERP file.
        Returns an empty ErpRecord (source="unavailable") if file is missing
        or the part is not found — the batch never fails due to missing ERP.
        """
        if not self.inventory_path.exists():
            log.debug(
                "Local ERP file not found at %s — proceeding without local data.",
                self.inventory_path,
            )
            return ErpRecord(
                part_number=part_number,
                stock_qty=None,
                supply_status=None,
                source="unavailable",
            )

        try:
            result = self._erp_reader.lookup(part_number, str(self.inventory_path))
            # GenericErpReader.lookup returns ErpLookupResult; bridge to ErpRecord
            return ErpRecord(
                part_number=result.part_number,
                stock_qty=result.stock_qty,
                supply_status=result.supply_status,
                source=result.source_file if result.found else "not_found",
            )
        except Exception as exc:
            log.warning("ERP read error for %s: %s", part_number, exc)
            return ErpRecord(
                part_number=part_number,
                stock_qty=None,
                supply_status=None,
                source="error",
            )

    def _load_batch_rows(self, path: Path) -> list[tuple[str, int]]:
        """
        Load (part_number, qty) pairs from an Excel or CSV file.
        Uses GenericErpReader.read_all() to iterate every row.
        qty is taken from stock_qty if positive, else defaults to 0.
        """
        if not path.exists():
            log.error("Batch source file not found: %s", path)
            return []

        try:
            records = self._erp_reader.read_all(str(path))
        except Exception as exc:
            log.error("Failed to read batch file %s: %s", path, exc)
            return []

        rows: list[tuple[str, int]] = []
        for rec in records:
            if not rec.part_number:
                continue
            qty = int(rec.stock_qty) if rec.stock_qty and rec.stock_qty > 0 else 0
            rows.append((rec.part_number.strip().upper(), qty))

        return rows


# ════════════════════════════════════════════════════════════════════════════════
# Terminal display helpers
# ════════════════════════════════════════════════════════════════════════════════

def print_view(view: MergedQuoteView, as_json: bool = False) -> None:
    """Print a MergedQuoteView to stdout in Markdown or JSON format."""
    if as_json:
        print(json.dumps(format_as_dict(view), ensure_ascii=False, indent=2))
    else:
        print(format_as_text(view))


def print_batch_summary(
    results: list[tuple[str, MergedQuoteView | QuoteApiError]],
    as_json: bool = False,
) -> None:
    """Print a batch result set to stdout."""
    if as_json:
        output: list[dict[str, Any]] = []
        for pn, item in results:
            if isinstance(item, QuoteApiError):
                output.append({"part_number": pn, "error": str(item)})
            else:
                output.append(format_as_dict(item))
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    total   = len(results)
    errors  = sum(1 for _, v in results if isinstance(v, QuoteApiError))
    success = total - errors

    print(f"\n{'═' * 70}")
    print(f"  IC Trade Navigator — Batch Quote Summary")
    print(f"  {success}/{total} succeeded   {errors} failed")
    print(f"{'═' * 70}\n")

    for pn, item in results:
        if isinstance(item, QuoteApiError):
            print(f"✗ {pn}  →  ERROR: {item}")
            print()
        else:
            print(format_as_text(item))
            print()


# ════════════════════════════════════════════════════════════════════════════════
# CLI entry point
# ════════════════════════════════════════════════════════════════════════════════

def _parse_args(argv: list[str]) -> dict[str, Any]:
    """
    Minimal CLI argument parser (stdlib only — no argparse dependency).

    Supported commands
    ──────────────────
    quote <PART_NUMBER>         Single quote
      --qty <int>               Requested quantity (default 0)
      --lang <code>             Advisory language (default en)
      --inventory <path>        Override ERP Excel path
      --json                    Output as JSON

    batch [<EXCEL_PATH>]        Batch quote from Excel
      --lang <code>             Advisory language for all rows
      --col-pn <header>         Part number column header (default "Part Number")
      --col-qty <header>        Stock qty column header (default "Stock Qty")
      --col-status <header>     Status column header (default "Status")
      --json                    Output as JSON

    Usage examples
    ──────────────
    python -m mcp_connector.client quote STM32L412CBU6 --qty 500 --lang zh-TW
    python -m mcp_connector.client batch data/inventory.xlsx
    python -m mcp_connector.client batch data/bom.csv --col-pn MPN --col-qty QTY
    python -m mcp_connector.client quote GD32F103C8T6 --json
    """
    if len(argv) < 2:
        _usage_exit()

    cmd = argv[1].lower()
    flags: dict[str, Any] = {
        "command":    cmd,
        "part":       None,
        "qty":        0,
        "lang":       "en",
        "inventory":  None,
        "json":       False,
        "source":     None,
        "col_pn":     "Part Number",
        "col_qty":    "Stock Qty",
        "col_status": "Status",
    }

    i = 2
    while i < len(argv):
        tok = argv[i]
        if tok == "--qty"        and i + 1 < len(argv): flags["qty"]        = int(argv[i+1]); i += 2
        elif tok == "--lang"     and i + 1 < len(argv): flags["lang"]       = argv[i+1];      i += 2
        elif tok == "--inventory"and i + 1 < len(argv): flags["inventory"]  = argv[i+1];      i += 2
        elif tok == "--col-pn"   and i + 1 < len(argv): flags["col_pn"]    = argv[i+1];      i += 2
        elif tok == "--col-qty"  and i + 1 < len(argv): flags["col_qty"]   = argv[i+1];      i += 2
        elif tok == "--col-status"and i+1 < len(argv):  flags["col_status"]= argv[i+1];      i += 2
        elif tok == "--json":    flags["json"] = True;  i += 1
        elif not tok.startswith("--"):
            if cmd == "quote" and flags["part"] is None:
                flags["part"] = tok
            elif cmd == "batch" and flags["source"] is None:
                flags["source"] = tok
            i += 1
        else:
            print(f"Unknown flag: {tok}", file=sys.stderr)
            i += 1

    return flags


def _usage_exit() -> None:
    print(
        "\nIC Trade Navigator — Local Client\n\n"
        "Usage:\n"
        "  python -m mcp_connector.client quote <PART_NUMBER> [--qty N] [--lang CODE] [--json]\n"
        "  python -m mcp_connector.client batch [EXCEL_PATH] [--lang CODE] [--json]\n\n"
        "Advisory languages: en (default), de, ja, zh-TW, fr, ko\n",
        file=sys.stderr,
    )
    sys.exit(1)


def main(argv: list[str] | None = None) -> None:
    """CLI entry point.  Call directly or via  python -m mcp_connector.client."""
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s %(name)s — %(message)s",
    )

    flags = _parse_args(argv or sys.argv)
    cmd   = flags["command"]

    # ── Build column map from CLI flags ───────────────────────────────────────
    col_map = ColumnMap(
        part_number   = flags["col_pn"],
        stock_qty     = flags["col_qty"],
        supply_status = flags["col_status"],
    )

    inventory = flags["inventory"] or _DEFAULT_INVENTORY
    client    = QuoteClient(
        inventory_path = inventory,
        column_map     = col_map,
        default_lang   = flags["lang"],
    )

    # ── command: quote ────────────────────────────────────────────────────────
    if cmd == "quote":
        if not flags["part"]:
            print("Error: 'quote' command requires a part number.", file=sys.stderr)
            _usage_exit()
        try:
            view = client.quote(
                part_number = flags["part"],
                qty         = flags["qty"],
                lang        = flags["lang"],
            )
            print_view(view, as_json=flags["json"])
        except QuoteApiError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(2)

    # ── command: batch ────────────────────────────────────────────────────────
    elif cmd == "batch":
        results = client.quote_batch(
            source_path = flags["source"],
            lang        = flags["lang"],
        )
        print_batch_summary(results, as_json=flags["json"])

    else:
        print(f"Unknown command: {cmd!r}", file=sys.stderr)
        _usage_exit()


if __name__ == "__main__":
    main()
