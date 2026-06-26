"""FTSE 350 ticker list with GICS sector mappings.

Hardcoded dictionary of ~100 of the most liquid FTSE 350 constituents,
mapped to their GICS sector classification. Tickers use Yahoo Finance
format with .L suffix.

Usage:
    uv run scripts/ftse350.py                          → JSON array of {ticker, sector}
    uv run scripts/ftse350.py --sector Financials      → filtered by sector
    uv run scripts/ftse350.py --list-sectors           → JSON array of sector names
"""

import argparse
import json
import sys

from config import GICS_SECTORS

# Mapping of Yahoo Finance ticker → GICS sector
# ~100 of the most liquid FTSE 350 names across all 11 GICS sectors
FTSE350: dict[str, str] = {
    # --- Energy ---
    "BP.L": "Energy",
    "SHEL.L": "Energy",
    "CNE.L": "Energy",
    "HTG.L": "Energy",
    "ENQ.L": "Energy",
    "PMO.L": "Energy",
    "TLW.L": "Energy",
    # --- Materials ---
    "AAL.L": "Materials",
    "ANTO.L": "Materials",
    "RIO.L": "Materials",
    "GLEN.L": "Materials",
    "FRES.L": "Materials",
    "EVR.L": "Materials",
    "MNDI.L": "Materials",
    "CRH.L": "Materials",
    "CRDA.L": "Materials",
    # --- Industrials ---
    "RR.L": "Industrials",
    "BA.L": "Industrials",
    "EXPN.L": "Industrials",
    "RS1.L": "Industrials",
    "BNZL.L": "Industrials",
    "SMDS.L": "Industrials",
    "RMV.L": "Industrials",
    "SMIN.L": "Industrials",
    "IMI.L": "Industrials",
    "WEIR.L": "Industrials",
    "SDR.L": "Industrials",
    "BWNG.L": "Industrials",
    "MGGT.L": "Industrials",
    # --- Consumer Discretionary ---
    "NXT.L": "Consumer Discretionary",
    "IHG.L": "Consumer Discretionary",
    "WTB.L": "Consumer Discretionary",
    "JD.L": "Consumer Discretionary",
    "FRAS.L": "Consumer Discretionary",
    "ENT.L": "Consumer Discretionary",
    "BDEV.L": "Consumer Discretionary",
    "TW.L": "Consumer Discretionary",
    "DGE.L": "Consumer Discretionary",
    "BWY.L": "Consumer Discretionary",
    "PSN.L": "Consumer Discretionary",
    "BRBY.L": "Consumer Discretionary",
    # --- Consumer Staples ---
    "ULVR.L": "Consumer Staples",
    "RKT.L": "Consumer Staples",
    "TSCO.L": "Consumer Staples",
    "SBRY.L": "Consumer Staples",
    "ABF.L": "Consumer Staples",
    "BME.L": "Consumer Staples",
    "GRG.L": "Consumer Staples",
    "HLMA.L": "Consumer Staples",
    "OCDO.L": "Consumer Staples",
    # --- Health Care ---
    "AZN.L": "Health Care",
    "GSK.L": "Health Care",
    "SN.L": "Health Care",
    "HIK.L": "Health Care",
    "DPLM.L": "Health Care",
    "SPX.L": "Health Care",
    "DARK.L": "Health Care",
    # --- Financials ---
    "HSBA.L": "Financials",
    "BARC.L": "Financials",
    "LLOY.L": "Financials",
    "NWG.L": "Financials",
    "STAN.L": "Financials",
    "AV.L": "Financials",
    "LGEN.L": "Financials",
    "PRU.L": "Financials",
    "ADM.L": "Financials",
    "III.L": "Financials",
    "HL.L": "Financials",
    "PHNX.L": "Financials",
    "INVP.L": "Financials",
    "MNG.L": "Financials",
    # --- Information Technology ---
    "SAGE.L": "Information Technology",
    "KNOS.L": "Information Technology",
    "AVV.L": "Information Technology",
    "FDM.L": "Information Technology",
    "SGE.L": "Information Technology",
    "AUTO.L": "Information Technology",
    # --- Communication Services ---
    "VOD.L": "Communication Services",
    "REL.L": "Communication Services",
    "WPP.L": "Communication Services",
    "ITV.L": "Communication Services",
    "INF.L": "Communication Services",
    # --- Utilities ---
    "NG.L": "Utilities",
    "SSE.L": "Utilities",
    "SVT.L": "Utilities",
    "UU.L": "Utilities",
    "PNN.L": "Utilities",
    "CNA.L": "Utilities",
    "DRX.L": "Utilities",
    # --- Real Estate ---
    "LAND.L": "Real Estate",
    "BLND.L": "Real Estate",
    "SGRO.L": "Real Estate",
    "UTG.L": "Real Estate",
    "HMSO.L": "Real Estate",
    "GPE.L": "Real Estate",
}


def get_tickers(sector: str | None = None) -> dict[str, str]:
    """Return FTSE 350 ticker-to-sector mapping, optionally filtered by sector.

    Args:
        sector: GICS sector name to filter by. If None, returns all tickers.

    Returns:
        Dict mapping ticker string to sector string.
    """
    if sector is None:
        return dict(FTSE350)
    return {t: s for t, s in FTSE350.items() if s == sector}


def get_sector(ticker: str) -> str | None:
    """Return the GICS sector for a given ticker, or None if not found.

    Args:
        ticker: Yahoo Finance ticker (e.g. "HSBA.L").

    Returns:
        Sector string or None.
    """
    return FTSE350.get(ticker)


def main():
    parser = argparse.ArgumentParser(description="FTSE 350 ticker list with GICS sector mappings")
    parser.add_argument("--sector", help="Filter by GICS sector name (e.g., Financials)")
    parser.add_argument("--list-sectors", action="store_true", help="List all GICS sector names")
    args = parser.parse_args()

    if args.list_sectors:
        print(json.dumps(GICS_SECTORS, indent=2))
        return

    tickers = get_tickers(sector=args.sector)

    if args.sector and not tickers:
        print(json.dumps({"error": f"No tickers found for sector: {args.sector}"}))
        sys.exit(1)

    result = [{"ticker": t, "sector": s} for t, s in sorted(tickers.items())]
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
