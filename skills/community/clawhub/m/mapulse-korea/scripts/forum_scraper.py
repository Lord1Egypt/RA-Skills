#!/usr/bin/env python3
"""
Mapulse Forum Scraper 🇰🇷
네이버 증권 종합 커뮤니티 데이터 수집 + 감성 분석

데이터 소스:
  1. 네이버 OpenTalk (실시간 채팅)
  2. 네이버 종목토론방 (종토방 게시판)
  3. 네이버 증권 뉴스 API
  4. 네이버 증권사 리서치
  5. 외국인/기관/개인 매매동향
  6. 네이버 실시간 시세

기능:
  - 종목 커뮤니티 종합 리포트
  - 산투자자 감성 분석 (매수/매도 비율)
  - 핫 키워드 추출
  - 증권사 리서치 요약
  - 기관/외국인 수급 동향
"""

import requests
import json
import re
import os
import time
from datetime import datetime
from collections import Counter

HEADERS_MOBILE = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
}
HEADERS_PC = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

STOCK_MAP = {
    "005930": "삼성전자", "000660": "SK하이닉스", "035420": "NAVER",
    "035720": "카카오", "373220": "LG에너지솔루션", "005380": "현대자동차",
    "000270": "기아", "068270": "셀트리온", "051910": "LG화학",
    "006400": "삼성SDI", "096770": "SK이노베이션", "047050": "포스코인터내셔널",
    "015760": "한국전력", "030200": "KT", "009150": "삼성전기",
    "055550": "신한지주", "105560": "KB금융", "086790": "하나금융지주",
    "066570": "LG전자", "003550": "LG", "034730": "SK",
    "028260": "삼성물산", "012330": "현대모비스", "036570": "엔씨소프트",
    "352820": "하이브", "263750": "펄어비스", "293490": "카카오게임즈",
    "247540": "에코프로비엠", "086520": "에코프로", "196170": "알테오젠",
}


# ═══════════════════════════════════════════
#  1. 네이버 OpenTalk + 리서치 + 매매동향 (SSR)
# ═══════════════════════════════════════════

def fetch_naver_ssr(ticker):
    """네이버 모바일 SSR __NEXT_DATA__ → OpenTalk + 리서치 + 매매동향 + 시세"""
    try:
        resp = requests.get(
            f"https://m.stock.naver.com/domestic/stock/{ticker}/discuss",
            headers=HEADERS_MOBILE, timeout=15
        )
        match = re.search(
            r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
            resp.text
        )
        if not match:
            return None

        queries = json.loads(match.group(1))["props"]["pageProps"]["dehydratedState"]["queries"]

        result = {"opentalk": [], "researches": [], "deal_trends": [], "total_infos": {}, "industry_compare": []}

        for q in queries:
            qk = q.get("queryKey", [{}])
            state = q.get("state", {}).get("data", {}).get("result", {})
            if not isinstance(state, dict):
                continue

            url_key = qk[0].get("url", "") if isinstance(qk[0], dict) else ""

            if "opentalk" in url_key:
                for m in state.get("recentMessages", []):
                    result["opentalk"].append({
                        "content": m.get("content", ""),
                        "nickname": m.get("nickname", ""),
                        "time": m.get("createTime", 0),
                    })

            if "integration" in url_key:
                for r in state.get("researches", []):
                    rid = r.get("id", "")
                    result["researches"].append({
                        "title": r.get("tit", ""),
                        "broker": r.get("bnm", ""),
                        "date": r.get("wdt", ""),
                        "target_price": r.get("rcnt", ""),
                        "id": rid,
                        "link": f"https://finance.naver.com/research/company_read.naver?nid={rid}" if rid else "",
                    })

                for d in state.get("dealTrendInfos", []):
                    result["deal_trends"].append({
                        "date": d.get("bizdate", ""),
                        "foreign": d.get("foreignerPureBuyQuant", "0"),
                        "foreign_ratio": d.get("foreignerHoldRatio", ""),
                        "institution": d.get("organPureBuyQuant", "0"),
                        "individual": d.get("individualPureBuyQuant", "0"),
                        "close": d.get("closePrice", ""),
                        "change": d.get("compareToPreviousClosePrice", ""),
                    })

                for info in state.get("totalInfos", []):
                    result["total_infos"][info.get("code", "")] = info.get("value", "")

                for comp in state.get("industryCompareInfo", []):
                    result["industry_compare"].append({
                        "name": comp.get("stockName", ""),
                        "code": comp.get("itemCode", ""),
                        "price": comp.get("closePrice", ""),
                        "change": comp.get("compareToPreviousClosePrice", ""),
                        "change_pct": comp.get("fluctuationsRatio", ""),
                    })

        return result
    except Exception as e:
        print(f"  ⚠️ SSR error: {e}")
        return None


# ═══════════════════════════════════════════
#  2. 네이버 종목토론방 (종토방 게시판)
# ═══════════════════════════════════════════

def fetch_jongtobang(ticker, pages=3):
    """
    네이버 PC 종목토론방 크롤링 (cp949)
    https://finance.naver.com/item/board.naver?code=005930
    """
    all_posts = []

    for page in range(1, pages + 1):
        try:
            resp = requests.get(
                "https://finance.naver.com/item/board.naver",
                params={"code": ticker, "page": page},
                headers=HEADERS_PC, timeout=10
            )
            # 인코딩 자동 감지
            ct = resp.headers.get("content-type", "")
            enc_match = re.search(r'charset=([^\s;]+)', ct, re.I)
            enc = enc_match.group(1) if enc_match else "utf-8"
            text = resp.content.decode(enc, errors="replace")

            # type2 테이블에서 추출
            board = re.search(r'class="type2"(.*?)</table>', text, re.DOTALL)
            if not board:
                continue

            bt = board.group(1)

            # 行별로 파싱 (tr → td 구조: date | title | author | views | agree | disagree)
            rows = re.findall(r'<tr[^>]*>(.*?)</tr>', bt, re.DOTALL)
            for row in rows:
                # 링크+제목 추출
                link_match = re.search(
                    r'<a href="(/item/board_read\.naver\?[^"]+)"[^>]*title="([^"]+)"', row
                )
                if not link_match:
                    continue

                href, title_text = link_match.group(1), link_match.group(2)

                # 모든 td 내용 추출
                tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
                # Clean each td
                td_texts = [re.sub(r'<[^>]+>', '', td).strip() for td in tds]

                post = {
                    "title": title_text.strip(),
                    "source": "종토방",
                    "link": f"https://finance.naver.com{href}",
                }
                nid_match = re.search(r'nid=(\d+)', href)
                if nid_match:
                    post["nid"] = nid_match.group(1)

                # td order: [0]=date, [1]=title, [2]=author, [3]=views, [4]=agree, [5]=disagree
                if len(td_texts) >= 6:
                    post["date"] = td_texts[0].strip()
                    post["views"] = td_texts[3].strip().replace(",", "")
                    post["agree"] = td_texts[4].strip().replace(",", "")
                    post["disagree"] = td_texts[5].strip().replace(",", "")
                elif len(td_texts) >= 4:
                    post["date"] = td_texts[0].strip()
                    post["views"] = td_texts[-3].strip().replace(",", "") if len(td_texts) > 3 else ""

                all_posts.append(post)

            time.sleep(0.3)
        except Exception as e:
            print(f"  ⚠️ 종토방 page {page}: {e}")

    return all_posts


# ═══════════════════════════════════════════
#  3. 네이버 뉴스 API
# ═══════════════════════════════════════════

def fetch_naver_news(ticker, count=10):
    """네이버 모바일 증권 뉴스 (링크 생성 가능한 필드 포함)"""
    results = []
    try:
        resp = requests.get(
            f"https://m.stock.naver.com/api/news/stock/{ticker}",
            params={"pageSize": count, "page": 1},
            headers=HEADERS_MOBILE, timeout=10
        )
        if resp.status_code == 200:
            for item in resp.json():
                if isinstance(item, dict) and "items" in item:
                    for news in item["items"]:
                        title = news.get("titleFull", news.get("title", ""))
                        title = title.replace("&quot;", '"').replace("&amp;", "&").replace("&#039;", "'")
                        oid = news.get("officeId", "")
                        aid = news.get("articleId", "")
                        link = f"https://n.news.naver.com/mnews/article/{oid}/{aid}" if oid and aid else ""
                        results.append({
                            "title": title,
                            "source": news.get("officeName", ""),
                            "datetime": news.get("datetime", ""),
                            "link": link,
                            "officeId": oid,
                            "articleId": aid,
                        })
    except Exception as e:
        print(f"  ⚠️ News error: {e}")
    return results


# ═══════════════════════════════════════════
#  4. 실시간 시세
# ═══════════════════════════════════════════

def fetch_realtime_price(ticker):
    """네이버 실시간 시세 polling API"""
    try:
        resp = requests.get(
            f"https://polling.finance.naver.com/api/realtime?query=SERVICE_ITEM:{ticker}",
            headers=HEADERS_MOBILE, timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            items = data.get("result", {}).get("areas", [{}])[0].get("datas", [])
            if items:
                d = items[0]
                return {
                    "name": d.get("nm", ""),
                    "price": d.get("nv", 0),
                    "prev_close": d.get("sv", 0),
                    "change": d.get("cv", 0),
                    "change_pct": d.get("cr", 0),
                    "status": d.get("ms", ""),  # CLOSE/TRADING
                }
    except:
        pass
    return None


# ═══════════════════════════════════════════
#  감성 분석
# ═══════════════════════════════════════════

BULLISH = [
    "매수", "상승", "오른다", "간다", "존버", "가즈아", "반등", "돌파",
    "신고가", "저점", "물타기", "추매", "기대", "ㄱㅈㅇ", "가자",
    "상한가", "급등", "폭등", "대박", "호재", "흑전", "갈거야",
    "사야", "담아", "모아", "버텨", "기회", "저가", "좋다",
]
BEARISH = [
    "매도", "하락", "내린다", "빠진다", "손절", "탈출", "폭락", "급락",
    "하한가", "물려", "걱정", "위험", "악재", "적자", "공매도",
    "떨어", "망", "끝", "도망", "패닉", "팔아", "던져",
    "망해", "절단", "쫄", "거품", "위기", "최악",
]


def analyze_sentiment(messages):
    """통합 감성 분석 (OpenTalk + 종토방)"""
    bull = bear = neutral = 0

    for msg in messages:
        text = msg.get("content", "") or msg.get("title", "")
        is_bull = any(w in text for w in BULLISH)
        is_bear = any(w in text for w in BEARISH)

        if is_bull and not is_bear:
            bull += 1
            msg["sentiment"] = "🟢"
        elif is_bear and not is_bull:
            bear += 1
            msg["sentiment"] = "🔴"
        else:
            neutral += 1
            msg["sentiment"] = "⚪"

    total = bull + bear
    ratio = bull / total if total > 0 else 0.5

    if ratio > 0.65:
        label = "🟢 강세 (매수 우세)"
    elif ratio > 0.55:
        label = "🟡 약 매수"
    elif ratio > 0.45:
        label = "⚪ 중립"
    elif ratio > 0.35:
        label = "🟡 약 매도"
    else:
        label = "🔴 약세 (매도 우세)"

    return {"bull": bull, "bear": bear, "neutral": neutral, "ratio": round(ratio, 2), "label": label}


def extract_keywords(messages, top_n=10):
    """핫 키워드"""
    words = Counter()
    stopwords = {"이거", "그거", "저거", "진짜", "아니", "이번", "오늘", "내일",
                 "어제", "근데", "그냥", "그래", "너무", "지금", "사람", "생각",
                 "하는", "있는", "한다", "한데", "같은", "이런", "저런", "그런",
                 "에서", "까지", "부터", "대한", "통해"}
    for msg in messages:
        text = msg.get("content", "") or msg.get("title", "")
        tokens = re.findall(r'[가-힣]{2,4}', text)
        for t in tokens:
            if t not in stopwords:
                words[t] += 1
    return words.most_common(top_n)


# ═══════════════════════════════════════════
#  종합 리포트
# ═══════════════════════════════════════════

def get_full_report(ticker):
    """종목 커뮤니티 종합 리포트"""
    name = STOCK_MAP.get(ticker, ticker)
    print(f"\n📊 {name} ({ticker}) 종합 커뮤니티 분석")
    print("=" * 50)

    # 1. SSR (OpenTalk + 리서치 + 수급)
    print("  🔍 네이버 OpenTalk + 리서치 + 수급...")
    ssr = fetch_naver_ssr(ticker) or {"opentalk": [], "researches": [], "deal_trends": [], "total_infos": {}, "industry_compare": []}
    print(f"     → OpenTalk {len(ssr['opentalk'])}건, 리서치 {len(ssr['researches'])}건")

    # 2. 종토방 게시판
    print("  🔍 네이버 종목토론방 (종토방)...")
    jongtobang = fetch_jongtobang(ticker, pages=3)
    print(f"     → 종토방 {len(jongtobang)}건")

    # 3. 뉴스
    print("  🔍 네이버 증권 뉴스...")
    news = fetch_naver_news(ticker)
    print(f"     → 뉴스 {len(news)}건")

    # 4. 실시간 시세
    print("  🔍 실시간 시세...")
    realtime = fetch_realtime_price(ticker)

    # 통합 감성 분석
    all_msgs = ssr["opentalk"] + jongtobang
    sentiment = analyze_sentiment(all_msgs)
    keywords = extract_keywords(all_msgs)

    return {
        "ticker": ticker,
        "name": name,
        "timestamp": datetime.now().isoformat(),
        "realtime": realtime,
        "sentiment": sentiment,
        "keywords": keywords,
        "opentalk": ssr["opentalk"],
        "jongtobang": jongtobang,
        "researches": ssr["researches"],
        "deal_trends": ssr["deal_trends"],
        "industry_compare": ssr["industry_compare"],
        "news": news,
        "sources_count": {
            "opentalk": len(ssr["opentalk"]),
            "jongtobang": len(jongtobang),
            "news": len(news),
            "researches": len(ssr["researches"]),
        },
    }


def format_report(r):
    """포맷된 리포트"""
    s = r["sentiment"]
    lines = [f"📊 *{r['name']} ({r['ticker']}) 커뮤니티 종합분석*", f"⏰ {r['timestamp'][:16]}", ""]

    # 시세
    if r["realtime"]:
        p = r["realtime"]
        arrow = "🔴" if p["change"] < 0 else "🟢" if p["change"] > 0 else "⚪"
        status = "장중" if p["status"] == "TRADING" else "장마감"
        lines.append(f"💰 {arrow} ₩{p['price']:,} ({p['change']:+,} / {p['change_pct']:+.2f}%) [{status}]")
        lines.append("")

    # 감성
    lines.extend([
        f"*🎭 투자자 감성:* {s['label']}",
        f"  🟢 매수 {s['bull']} | 🔴 매도 {s['bear']} | ⚪ 중립 {s['neutral']} (비율 {s['ratio']*100:.0f}%)",
    ])

    # 수급
    if r["deal_trends"]:
        d = r["deal_trends"][0]
        lines.extend([
            f"\n*📈 수급동향* ({d['date']})",
            f"  외국인: {d['foreign']} (보유 {d['foreign_ratio']})",
            f"  기관: {d['institution']}",
            f"  개인: {d['individual']}",
        ])

    # 키워드
    if r["keywords"]:
        kw = " ".join([f"#{w}({c})" for w, c in r["keywords"][:8]])
        lines.append(f"\n*🔥 핫 키워드:* {kw}")

    # 리서치 (with links)
    if r["researches"]:
        lines.append(f"\n*📋 증권사 리서치:*")
        for res in r["researches"][:4]:
            tp = f" (조회 {res['target_price']})" if res.get("target_price") else ""
            link = res.get("link", "")
            title_text = res['title'][:50]
            if link:
                lines.append(f"  • {res['broker']}: [{title_text}]({link}){tp}")
            else:
                lines.append(f"  • {res['broker']}: {title_text}{tp}")

    # 뉴스
    if r["news"]:
        lines.append(f"\n*📰 최신 뉴스:*")
        for n in r["news"][:5]:
            lines.append(f"  • [{n['source']}] {n['title'][:55]}")

    # 동종업계
    if r["industry_compare"]:
        lines.append(f"\n*🏭 동종업계:*")
        for c in r["industry_compare"][:5]:
            arrow = "🔴" if c["change"].startswith("-") else "🟢" if c["change"].startswith("+") else "⚪"
            lines.append(f"  {arrow} {c['name']}: ₩{c['price']} ({c['change']})")

    # OpenTalk
    if r["opentalk"]:
        lines.append(f"\n*💬 실시간 토론:*")
        for m in r["opentalk"][:6]:
            sent = m.get("sentiment", "⚪")
            content = m["content"].replace("\n", " ")[:55]
            lines.append(f"  {sent} {m['nickname']}: {content}")

    # 종토방 (with links + sorted by views for "hot posts")
    if r["jongtobang"]:
        # Sort by views to show hottest posts first
        sorted_posts = sorted(
            r["jongtobang"],
            key=lambda x: int(x.get("views", "0") or "0"),
            reverse=True
        )
        lines.append(f"\n*📝 종목토론방 (인기순):*")
        for p in sorted_posts[:6]:
            sent = p.get("sentiment", "⚪")
            title = p["title"][:45]
            views = p.get("views", "")
            link = p.get("link", "")
            v_str = f" (👁{views})" if views else ""
            if link:
                lines.append(f"  {sent} [{title}]({link}){v_str}")
            else:
                lines.append(f"  {sent} {title}{v_str}")

    # 요약
    sc = r["sources_count"]
    lines.append(f"\n📊 데이터: OpenTalk {sc['opentalk']} + 종토방 {sc['jongtobang']} + 뉴스 {sc['news']} + 리서치 {sc['researches']}")

    return "\n".join(lines)


# ─── CLI ───

if __name__ == "__main__":
    import sys

    ticker = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "demo" else "005930"

    print("=" * 55)
    print("🇰🇷 Mapulse Community Analyzer v2.0")
    print("  네이버 OpenTalk + 종토방 + 뉴스 + 리서치 + 수급")
    print("=" * 55)

    report = get_full_report(ticker)
    print()
    print(format_report(report))

    os.makedirs(DATA_DIR, exist_ok=True)
    outfile = os.path.join(DATA_DIR, f"community_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n💾 저장: {outfile}")
