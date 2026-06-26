from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from binance_web3 import BinanceWeb3Client, CHAIN_ALIASES, STAGE_ALIASES  # noqa: E402
from billing import BillingError, build_billing_client  # noqa: E402


TEXT = {
    "zh": {
        "title": "Meme 风控雷达",
        "summary_prefix": "风险摘要",
        "critical": "极高风险",
        "high": "高风险",
        "medium": "中风险",
        "low": "低风险",
        "signal_no_social": "缺少公开社媒链接",
        "signal_top10": "前十持仓集中度偏高",
        "signal_dev": "开发者持仓占比较高",
        "signal_sniper": "狙击地址占比较高",
        "signal_insider": "内部地址占比较高",
        "signal_bundler": "打包地址占比较高",
        "signal_liquidity": "流动性偏低",
        "signal_tax": "买卖税偏高",
        "signal_unverified": "合约未验证",
        "signal_audit_hit": "审计命中风险项",
        "signal_audit_missing": "暂无可用审计结果",
        "disclaimer": "仅供风控筛查参考，不构成投资建议。",
    },
    "en": {
        "title": "Meme Risk Radar",
        "summary_prefix": "Risk summary",
        "critical": "Critical risk",
        "high": "High risk",
        "medium": "Medium risk",
        "low": "Low risk",
        "signal_no_social": "No public social links found",
        "signal_top10": "Top-10 holder concentration is elevated",
        "signal_dev": "Developer holding ratio is elevated",
        "signal_sniper": "Sniper holding ratio is elevated",
        "signal_insider": "Insider holding ratio is elevated",
        "signal_bundler": "Bundler holding ratio is elevated",
        "signal_liquidity": "Liquidity is thin",
        "signal_tax": "Buy or sell tax is elevated",
        "signal_unverified": "Contract is not verified",
        "signal_audit_hit": "Audit reported active risk findings",
        "signal_audit_missing": "No usable audit result returned",
        "disclaimer": "For risk filtering only. Not investment advice.",
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def to_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def risk_bucket(score: int) -> str:
    if score >= 75:
        return "critical"
    if score >= 50:
        return "high"
    if score >= 25:
        return "medium"
    return "low"


def localize_level(level: str, lang: str) -> str:
    return TEXT[lang][level]


def flatten_audit_hits(audit: Dict[str, Any]) -> List[str]:
    hits: List[str] = []
    for item in audit.get("riskItems", []) or []:
        for detail in item.get("details", []) or []:
            if detail.get("isHit"):
                title = detail.get("title")
                if isinstance(title, str) and title:
                    hits.append(title)
    return hits


def calculate_score(token: Dict[str, Any], audit: Dict[str, Any], meta: Dict[str, Any], lang: str) -> Dict[str, Any]:
    signals: List[str] = []
    score = 0
    text = TEXT[lang]

    top10 = to_float(token.get("holdersTop10Percent")) or 0.0
    dev_percent = to_float(token.get("holdersDevPercent")) or 0.0
    sniper_percent = to_float(token.get("holdersSniperPercent")) or 0.0
    insider_percent = to_float(token.get("holdersInsiderPercent")) or 0.0
    bundler_percent = to_float(token.get("bundlerHoldingPercent")) or 0.0
    liquidity = to_float(token.get("liquidity")) or 0.0

    if top10 >= 80:
        score += 18
        signals.append(text["signal_top10"])
    elif top10 >= 65:
        score += 10
        signals.append(text["signal_top10"])

    if dev_percent >= 10:
        score += 14
        signals.append(text["signal_dev"])
    elif dev_percent >= 5:
        score += 8
        signals.append(text["signal_dev"])

    if sniper_percent >= 15:
        score += 12
        signals.append(text["signal_sniper"])
    elif sniper_percent >= 8:
        score += 6
        signals.append(text["signal_sniper"])

    if insider_percent >= 15:
        score += 12
        signals.append(text["signal_insider"])
    elif insider_percent >= 8:
        score += 6
        signals.append(text["signal_insider"])

    if bundler_percent >= 20:
        score += 8
        signals.append(text["signal_bundler"])

    if liquidity < 5_000:
        score += 14
        signals.append(text["signal_liquidity"])
    elif liquidity < 20_000:
        score += 8
        signals.append(text["signal_liquidity"])

    links = meta.get("links", []) or []
    if not links:
        score += 6
        signals.append(text["signal_no_social"])

    has_result = bool(audit.get("hasResult")) and bool(audit.get("isSupported"))
    if not has_result:
        score += 8
        signals.append(text["signal_audit_missing"])
    else:
        risk_level = int(audit.get("riskLevel") or 0)
        score += min(risk_level * 10, 35)

        extra_info = audit.get("extraInfo", {}) or {}
        buy_tax = to_float(extra_info.get("buyTax")) or 0.0
        sell_tax = to_float(extra_info.get("sellTax")) or 0.0
        if max(buy_tax, sell_tax) > 10:
            score += 15
            signals.append(text["signal_tax"])
        elif max(buy_tax, sell_tax) > 5:
            score += 8
            signals.append(text["signal_tax"])

        if extra_info.get("isVerified") is False:
            score += 8
            signals.append(text["signal_unverified"])

        if flatten_audit_hits(audit):
            score += 10
            signals.append(text["signal_audit_hit"])

    score = min(score, 100)
    bucket = risk_bucket(score)
    summary = f"{text['summary_prefix']}: {localize_level(bucket, lang)}"
    return {
        "score": score,
        "risk_level": localize_level(bucket, lang),
        "summary": summary,
        "signals": signals,
    }


def normalize_token(token: Dict[str, Any], audit: Dict[str, Any], meta: Dict[str, Any], lang: str) -> Dict[str, Any]:
    scored = calculate_score(token, audit, meta, lang)
    return {
        "symbol": token.get("symbol"),
        "name": token.get("name"),
        "contract_address": token.get("contractAddress"),
        "score": scored["score"],
        "risk_level": scored["risk_level"],
        "summary": scored["summary"],
        "signals": scored["signals"],
        "metrics": {
            "price": token.get("price"),
            "market_cap": token.get("marketCap"),
            "liquidity": token.get("liquidity"),
            "volume_24h": token.get("volume"),
            "holders": token.get("holders"),
            "holders_top10_percent": token.get("holdersTop10Percent"),
            "holders_dev_percent": token.get("holdersDevPercent"),
            "holders_sniper_percent": token.get("holdersSniperPercent"),
            "holders_insider_percent": token.get("holdersInsiderPercent"),
            "bundler_holding_percent": token.get("bundlerHoldingPercent"),
            "progress": token.get("progress"),
            "protocol": token.get("protocol"),
        },
        "audit": {
            "has_result": audit.get("hasResult"),
            "is_supported": audit.get("isSupported"),
            "risk_level_enum": audit.get("riskLevelEnum"),
            "risk_level": audit.get("riskLevel"),
            "risk_hits": flatten_audit_hits(audit),
            "extra_info": audit.get("extraInfo"),
        },
        "links": meta.get("links", []),
    }


def maybe_bill(call_name: str) -> Dict[str, Any]:
    client = build_billing_client()
    amount = os.getenv("SKILLPAY_PRICE_USDT", "0.002").strip()
    user_ref = os.getenv("SKILLPAY_USER_REF", "anonymous").strip() or "anonymous"
    result = client.charge(call_name, amount, user_ref, str(uuid4()))
    if not result.ok:
        raise BillingError(f"billing_failed:{result.code}:{result.message}")
    return result.to_dict()


def cmd_scan(args: argparse.Namespace) -> None:
    client = BinanceWeb3Client()
    chain_id = CHAIN_ALIASES[args.chain]
    rank_type = STAGE_ALIASES[args.stage]
    billing = maybe_bill("scan")
    tokens = client.meme_rush_scan(
        chain_id=chain_id,
        rank_type=rank_type,
        limit=args.limit,
        liquidity_min=args.min_liquidity,
    )

    results = []
    for token in tokens:
        contract_address = token.get("contractAddress")
        if not isinstance(contract_address, str) or not contract_address:
            continue
        try:
            audit = client.token_audit(chain_id, contract_address)
        except Exception:
            audit = {"hasResult": False, "isSupported": False, "riskItems": []}
        try:
            meta = client.token_meta(chain_id, contract_address)
        except Exception:
            meta = {}
        results.append(normalize_token(token, audit, meta, args.lang))

    payload = {
        "title": TEXT[args.lang]["title"],
        "chain": args.chain,
        "stage": args.stage,
        "lang": args.lang,
        "generated_at_utc": utc_now(),
        "billing": billing,
        "tokens": sorted(results, key=lambda item: item["score"], reverse=True),
        "disclaimer": TEXT[args.lang]["disclaimer"],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def cmd_audit(args: argparse.Namespace) -> None:
    client = BinanceWeb3Client()
    chain_id = CHAIN_ALIASES[args.chain]
    billing = maybe_bill("audit")
    audit = client.token_audit(chain_id, args.contract)
    meta = {}
    try:
        meta = client.token_meta(chain_id, args.contract)
    except Exception:
        meta = {}
    token = {
        "symbol": meta.get("symbol"),
        "name": meta.get("name"),
        "contractAddress": args.contract,
        "liquidity": None,
        "holdersTop10Percent": None,
        "holdersDevPercent": None,
        "holdersSniperPercent": None,
        "holdersInsiderPercent": None,
        "bundlerHoldingPercent": None,
    }
    payload = {
        "title": TEXT[args.lang]["title"],
        "chain": args.chain,
        "lang": args.lang,
        "generated_at_utc": utc_now(),
        "billing": billing,
        "token": normalize_token(token, audit, meta, args.lang),
        "disclaimer": TEXT[args.lang]["disclaimer"],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def cmd_health(_: argparse.Namespace) -> None:
    payload = {
        "ok": True,
        "service": "meme-risk-radar-skill",
        "generated_at_utc": utc_now(),
        "billing_mode": os.getenv("SKILLPAY_BILLING_MODE", "skillpay"),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Meme Risk Radar")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Scan meme tokens and return a risk-ranked report")
    scan.add_argument("--chain", choices=sorted(CHAIN_ALIASES), default="solana")
    scan.add_argument("--stage", choices=sorted(STAGE_ALIASES), default="new")
    scan.add_argument("--limit", type=int, default=10)
    scan.add_argument("--lang", choices=("zh", "en"), default="zh")
    scan.add_argument("--min-liquidity", type=float, default=None)
    scan.set_defaults(func=cmd_scan)

    audit = subparsers.add_parser("audit", help="Audit a single token contract")
    audit.add_argument("--chain", choices=sorted(CHAIN_ALIASES), default="solana")
    audit.add_argument("--contract", required=True)
    audit.add_argument("--lang", choices=("zh", "en"), default="zh")
    audit.set_defaults(func=cmd_audit)

    health = subparsers.add_parser("health", help="Health check")
    health.set_defaults(func=cmd_health)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
        return 0
    except BillingError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 2
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
