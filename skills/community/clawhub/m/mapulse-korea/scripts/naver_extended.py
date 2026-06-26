#!/usr/bin/env python3
"""
Mapulse — Naver Finance Extended API
m.stock.naver.com/api/stock/{ticker}/integration 확장 데이터

기존 market_data.py 의 Naver API를 보완:
  - 시가총액 (정확한 값)
  - 외인소진율
  - 52주 최고/최저
  - PER / EPS / 추정PER / 추정EPS
  - PBR / BPS
  - 배당수익률 / 주당배당금
"""

import requests
import re

NAVER_MOBILE_BASE = "https://m.stock.naver.com/api/stock"


def fetch_naver_integration(ticker):
    """Naver integration API — 시총, 외인소진율, 52주, PER/PBR/EPS, 배당
    
    Returns dict with structured fields:
      prev_close, open, high, low, volume, trade_value,
      market_cap, foreign_exhaustion,
      high_52w, low_52w,
      per, eps, est_per, est_eps,
      pbr, bps,
      div_yield, dps (주당배당금)
    """
    try:
        r = requests.get(
            f"{NAVER_MOBILE_BASE}/{ticker}/integration",
            timeout=8,
        )
        if r.status_code != 200:
            return None
        d = r.json()

        infos = d.get("totalInfos", [])
        if not infos:
            return None

        # key → value 매핑
        raw = {}
        for item in infos:
            key = item.get("key", "")
            value = item.get("value", "")
            raw[key] = value

        # 파싱 함수
        def parse_num(s):
            """'188,700' → 188700, '1,163조 8,008억' → None (문자열 유지)"""
            if not s:
                return None
            s = str(s).strip()
            # 순수 숫자 (쉼표 포함)
            cleaned = s.replace(",", "").replace("원", "").replace("배", "").replace("%", "")
            try:
                return float(cleaned)
            except ValueError:
                return None

        result = {
            "stock_name": d.get("stockName"),
            "item_code": d.get("itemCode"),
            # 기본 시세
            "prev_close": parse_num(raw.get("전일")),
            "open": parse_num(raw.get("시가")),
            "high": parse_num(raw.get("고가")),
            "low": parse_num(raw.get("저가")),
            "volume": parse_num(raw.get("거래량")),
            "trade_value": raw.get("대금"),  # "1,763,763백만" 형태, 문자열 유지
            # 시가총액 (문자열: "1,163조 8,008억")
            "market_cap_str": raw.get("시총"),
            # 외인소진율 (e.g. "49.56%")
            "foreign_exhaustion": parse_num(raw.get("외인소진율")),
            # 52주 범위
            "high_52w": parse_num(raw.get("52주 최고")),
            "low_52w": parse_num(raw.get("52주 최저")),
            # PER/EPS
            "per": parse_num(raw.get("PER")),
            "eps": parse_num(raw.get("EPS")),
            "est_per": parse_num(raw.get("추정PER")),
            "est_eps": parse_num(raw.get("추정EPS")),
            # PBR/BPS
            "pbr": parse_num(raw.get("PBR")),
            "bps": parse_num(raw.get("BPS")),
            # 배당
            "div_yield": parse_num(raw.get("배당수익률")),
            "dps": parse_num(raw.get("주당배당금")),
            # 원본 데이터 보존
            "_raw": raw,
        }
        return result

    except Exception:
        return None


def format_naver_extended(data, lang="ko"):
    """포맷: Naver 확장 데이터"""
    if not data:
        return ""

    name = data.get("stock_name", "")
    code = data.get("item_code", "")
    lines = [f"📋 *{name} ({code}) 상세정보*", ""]

    # 시가총액
    mcap = data.get("market_cap_str")
    if mcap:
        lines.append(f"📊 시총: {mcap}")

    # PER (실적 vs 추정)
    per = data.get("per")
    est_per = data.get("est_per")
    eps = data.get("eps")
    est_eps = data.get("est_eps")
    if per:
        per_line = f"📈 PER: {per:.2f}배"
        if eps:
            per_line += f" (EPS: {eps:,.0f}원)"
        if est_per:
            per_line += f" | 추정 {est_per:.2f}배"
            if est_eps:
                per_line += f" (EPS: {est_eps:,.0f}원)"
        lines.append(per_line)

    # PBR
    pbr = data.get("pbr")
    bps = data.get("bps")
    if pbr:
        pbr_line = f"📉 PBR: {pbr:.2f}배"
        if bps:
            pbr_line += f" (BPS: {bps:,.0f}원)"
        lines.append(pbr_line)

    # 배당
    div_yield = data.get("div_yield")
    dps = data.get("dps")
    if div_yield or dps:
        div_line = "💎 배당:"
        if dps:
            div_line += f" {dps:,.0f}원/주"
        if div_yield:
            div_line += f" ({div_yield:.2f}%)"
        lines.append(div_line)

    # 외인소진율
    fe = data.get("foreign_exhaustion")
    if fe is not None:
        lines.append(f"🌍 외인소진율: {fe:.2f}%")

    # 52주 범위
    h52 = data.get("high_52w")
    l52 = data.get("low_52w")
    if h52 and l52:
        lines.append(f"📐 52주: {l52:,.0f} ~ {h52:,.0f}원")

    # 당일 시세
    o = data.get("open")
    h = data.get("high")
    lo = data.get("low")
    if o and h and lo:
        lines.append(f"📊 시가: {o:,.0f} | 고가: {h:,.0f} | 저가: {lo:,.0f}")

    # 거래대금
    tv = data.get("trade_value")
    if tv:
        lines.append(f"💰 거래대금: {tv}")

    return "\n".join(lines)


# ──────────────────────────────────────────────
# Test
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  🇰🇷 Naver Finance Extended API Test")
    print("=" * 60)

    for ticker in ["005930", "000660", "035420"]:
        print(f"\n=== {ticker} ===")
        data = fetch_naver_integration(ticker)
        if data:
            print(format_naver_extended(data))
            # 주요 필드 확인
            print(f"\n  [Debug] per={data.get('per')}, est_per={data.get('est_per')}, "
                  f"pbr={data.get('pbr')}, div={data.get('div_yield')}, "
                  f"foreign={data.get('foreign_exhaustion')}")
        else:
            print("  ❌ Failed")

    print("\n" + "=" * 60)
    print("  ✅ Naver Extended API Test Complete")
    print("=" * 60)
