#!/usr/bin/env python3
"""
한국 정부지원사업 통합 수집 스크립트
Skills: korean-gov-programs v1.0.0

수집 소스:
  1. 기업마당(BizInfo) - 소상공인 지원사업  [✅ 동작]
  2. 기업마당(BizInfo) - 기술창업/R&D 필터  [✅ 동작]
  3. NIA 한국지능정보사회진흥원             [✅ 동작]
  4. 소상공인시장진흥공단(SEMAS)            [⚠️ JS 필요, 스킵]
  5. 중소벤처기업부(MSS)                    [⚠️ JS 필요, 스킵]
  6. K-Startup                              [⚠️ JS 필요, 스킵]
  7. Innopolis 연구개발특구진흥재단          [⚠️ JS 필요, 스킵]

출력 (APPEND 전용):
  {output}/soho_programs.jsonl   - 소상공인 지원사업
  {output}/gov_programs.jsonl    - 정부 R&D / 기술창업
  {output}/.checkpoint.json      - 체크포인트

사용법:
  python3 collect.py --output ./data
  python3 collect.py --output ./data --max-pages 5
"""

import sys
import os
import json
import time
import re
import argparse
import urllib.request
import urllib.parse
from datetime import datetime

# ── 상수 ──────────────────────────────────────────────────
SLEEP_SEC = 0.8

DEFAULT_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

HEADERS = {
    "User-Agent": os.environ.get("GOV_SCRAPER_UA", DEFAULT_UA),
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


# ── 공통 유틸 ─────────────────────────────────────────────

def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def load_checkpoint(checkpoint_file: str) -> dict:
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_checkpoint(checkpoint_file: str, data: dict):
    with open(checkpoint_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_existing_titles(output_file: str) -> set:
    titles = set()
    if os.path.exists(output_file):
        with open(output_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        rec = json.loads(line)
                        titles.add(rec.get("title", ""))
                    except Exception:
                        pass
    return titles


def append_record(output_file: str, rec: dict):
    """APPEND 전용 — 기존 파일 절대 덮어쓰지 않음"""
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def fetch_url(url: str, timeout: int = 15) -> str | None:
    """urllib.request만 사용 (requests 라이브러리 미사용)"""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(charset, errors="replace")
    except Exception as e:
        log(f"  ⚠️  fetch 실패 {url[:80]}: {e}")
        return None


def make_record(
    title: str,
    category: str,
    source: str,
    url: str,
    amount: str = "",
    deadline: str = "",
    description: str = ""
) -> dict:
    return {
        "title": title,
        "category": category,
        "source": source,
        "url": url,
        "amount": amount,
        "deadline": deadline,
        "description": description,
        "collected_at": datetime.now().isoformat(),
    }


# ══════════════════════════════════════════════════════════════
# Source 1: 기업마당(BizInfo) — 소상공인 지원사업
# ══════════════════════════════════════════════════════════════

def crawl_bizinfo_soho(
    output_file: str,
    existing_titles: set,
    checkpoint: dict,
    max_pages: int = 10
) -> int:
    source = "기업마당(BizInfo)"
    category = "소상공인"
    base_url = "https://www.bizinfo.go.kr/sii/siia/selectSIIA200View.do"
    count = 0

    start_page = checkpoint.get("bizinfo_soho_page", 1)
    log(f"[BizInfo-소상공인] p{start_page}~{start_page + max_pages - 1} 수집...")

    for page in range(start_page, start_page + max_pages):
        url = f"{base_url}?rows=15&cpage={page}"
        html = fetch_url(url)
        if not html:
            break

        items = re.findall(
            r'<a[^>]+href=\s*"([^"]*selectSIIA200Detail[^"]*)"\s[^>]*>\s*\n?\s*([\w가-힣\(\)\[\]「」,\s·.\-\'/]+)',
            html
        )

        if not items:
            log(f"  p{page}: 데이터 없음, 종료")
            break

        deadlines = re.findall(r'(\d{4}-\d{2}-\d{2})\s*~\s*(\d{4}-\d{2}-\d{2})', html)

        new_on_page = 0
        for i, (href, raw_title) in enumerate(items):
            title = raw_title.strip()
            if not title or len(title) < 4 or title.isdigit():
                continue
            if title in existing_titles:
                continue

            full_url = f"https://www.bizinfo.go.kr{href}" if href.startswith("/") else href
            pid_m = re.search(r'pblancId=([^&"]+)', href)
            pid = pid_m.group(1) if pid_m else ""
            deadline = f"~{deadlines[i][1]}" if i < len(deadlines) else ""

            rec = make_record(title, category, source, full_url,
                              deadline=deadline,
                              description=f"pblancId={pid}" if pid else "")
            append_record(output_file, rec)
            existing_titles.add(title)
            count += 1
            new_on_page += 1

        log(f"  p{page}: {new_on_page}건 신규 (누적 {count}건)")
        checkpoint["bizinfo_soho_page"] = page + 1

        if new_on_page == 0:
            break
        time.sleep(SLEEP_SEC)

    return count


# ══════════════════════════════════════════════════════════════
# Source 2: 기업마당(BizInfo) — 기술창업/R&D 필터
# ══════════════════════════════════════════════════════════════

TECH_KEYWORDS = [
    '창업', '기술', 'R&D', '혁신', '스타트업', '벤처', '연구', '개발',
    '디지털', 'AI', 'ICT', '정보', '바이오', '제조', '스마트',
]


def crawl_bizinfo_gov(
    output_file: str,
    existing_titles: set,
    checkpoint: dict,
    max_pages: int = 5
) -> int:
    source = "기업마당(BizInfo) 기술창업"
    category = "기술창업"
    base_url = "https://www.bizinfo.go.kr/sii/siia/selectSIIA200View.do"
    count = 0

    start_page = checkpoint.get("bizinfo_gov_page", 1)
    log(f"[BizInfo-기술창업] p{start_page}~{start_page + max_pages - 1} 수집...")

    for page in range(start_page, start_page + max_pages):
        url = f"{base_url}?rows=15&cpage={page}"
        html = fetch_url(url)
        if not html:
            break

        items = re.findall(
            r'<a[^>]+href=\s*"([^"]*selectSIIA200Detail[^"]*)"\s[^>]*>\s*\n?\s*([\w가-힣\(\)\[\]「」,\s·.\-\'/]+)',
            html
        )

        if not items:
            break

        deadlines = re.findall(r'(\d{4}-\d{2}-\d{2})\s*~\s*(\d{4}-\d{2}-\d{2})', html)

        new_on_page = 0
        for i, (href, raw_title) in enumerate(items):
            title = raw_title.strip()
            if not title or len(title) < 4 or title.isdigit():
                continue
            if not any(kw in title for kw in TECH_KEYWORDS):
                continue
            if title in existing_titles:
                continue

            full_url = f"https://www.bizinfo.go.kr{href}" if href.startswith("/") else href
            deadline = f"~{deadlines[i][1]}" if i < len(deadlines) else ""

            rec = make_record(title, category, source, full_url, deadline=deadline)
            append_record(output_file, rec)
            existing_titles.add(title)
            count += 1
            new_on_page += 1

        log(f"  p{page}: {new_on_page}건 신규 (누적 {count}건)")
        checkpoint["bizinfo_gov_page"] = page + 1

        if new_on_page == 0 and len(items) == 0:
            break
        time.sleep(SLEEP_SEC)

    return count


# ══════════════════════════════════════════════════════════════
# Source 3: NIA 한국지능정보사회진흥원
# ══════════════════════════════════════════════════════════════

def crawl_nia(
    output_file: str,
    existing_titles: set,
    checkpoint: dict,
    max_pages: int = 5
) -> int:
    source = "NIA 한국지능정보사회진흥원"
    category = "정보화사업"
    cb_idx = "78336"
    base_url = f"https://www.nia.or.kr/site/nia_kor/ex/bbs/List.do?cbIdx={cb_idx}"
    view_url_tpl = "https://www.nia.or.kr/site/nia_kor/ex/bbs/View.do?cbIdx={cb}&bcIdx={bc}"
    count = 0

    start_page = checkpoint.get("nia_page", 1)
    log(f"[NIA] p{start_page}~{start_page + max_pages - 1} 수집...")

    for page in range(start_page, start_page + max_pages):
        url = f"{base_url}&pageNo={page}"
        html = fetch_url(url)
        if not html:
            break

        items = re.findall(
            r'onclick="doBbsFView\(\'(\d+)\',\'(\d+)\',\'[^\']*\',\'[^\']*\'\)[^"]*"[^>]+title="([^"]+)"',
            html
        )

        if not items:
            log(f"  p{page}: 패턴 없음 (구조 변경 가능)")
            break

        new_on_page = 0
        for cb, bc, raw_title in items:
            title = re.sub(r'^[\[\(][^\]\)]+[\]\)]\s*', '', raw_title)
            title = re.sub(r'-첨부파일\s*있음.*$', '', title)
            title = re.sub(r'\(새\s*글\).*$', '', title)
            title = title.strip() or raw_title.strip()

            if not title or len(title) < 3:
                continue
            if title in existing_titles:
                continue

            full_url = view_url_tpl.format(cb=cb, bc=bc)
            rec = make_record(title, category, source, full_url,
                              description=raw_title[:100])
            append_record(output_file, rec)
            existing_titles.add(title)
            count += 1
            new_on_page += 1

        log(f"  p{page}: {new_on_page}건 신규 (누적 {count}건)")
        checkpoint["nia_page"] = page + 1

        if new_on_page == 0:
            break
        time.sleep(SLEEP_SEC)

    return count


# ══════════════════════════════════════════════════════════════
# JS 렌더링 필요 소스 — 스킵 스텁
# ══════════════════════════════════════════════════════════════

def skip_js_required(name: str, url: str, checkpoint: dict):
    log(f"[{name}] ⚠️  JS 렌더링 필요 — 스킵")
    log(f"  Selenium/Playwright 환경에서 별도 수집 필요: {url}")
    checkpoint[name.lower().replace(" ", "_")] = "skipped_js_required"


# ══════════════════════════════════════════════════════════════
# 메인
# ══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="한국 정부지원사업 통합 수집 스크립트"
    )
    parser.add_argument(
        "--output", default="./data",
        help="출력 디렉토리 (기본: ./data)"
    )
    parser.add_argument(
        "--max-pages", type=int, default=10,
        help="소스당 최대 수집 페이지 수 (기본: 10)"
    )
    args = parser.parse_args()

    output_dir = os.path.abspath(args.output)
    os.makedirs(output_dir, exist_ok=True)

    soho_file       = os.path.join(output_dir, "soho_programs.jsonl")
    gov_file        = os.path.join(output_dir, "gov_programs.jsonl")
    checkpoint_file = os.path.join(output_dir, ".checkpoint.json")

    log("=" * 60)
    log("🔍 한국 정부지원사업 통합 수집 시작")
    log(f"   출력 디렉토리: {output_dir}")
    log("=" * 60)

    checkpoint = load_checkpoint(checkpoint_file)

    # 기존 데이터 로드 (중복 방지)
    soho_titles = load_existing_titles(soho_file)
    gov_titles  = load_existing_titles(gov_file)

    log(f"기존 soho_programs: {len(soho_titles)}건")
    log(f"기존 gov_programs:  {len(gov_titles)}건")
    log("")

    total_soho = 0
    total_gov  = 0

    # ── 소상공인 지원사업 ──────────────────────────────────

    log("── 소상공인 지원사업 ─────────────────────────────────")

    # BizInfo 소상공인
    try:
        n = crawl_bizinfo_soho(soho_file, soho_titles, checkpoint, args.max_pages)
        total_soho += n
        log(f"✅ BizInfo-소상공인: {n}건 추가")
    except Exception as e:
        log(f"❌ BizInfo-소상공인 오류: {e}")
        import traceback; traceback.print_exc()

    save_checkpoint(checkpoint_file, checkpoint)
    time.sleep(SLEEP_SEC)

    # SEMAS (스킵)
    skip_js_required(
        "SEMAS 소상공인시장진흥공단",
        "https://www.semas.or.kr/web/board/boardList.do",
        checkpoint
    )

    # ── 정부 R&D / 기술창업 ────────────────────────────────

    log("")
    log("── 정부 R&D / 기술창업 ───────────────────────────────")

    # BizInfo 기술창업
    try:
        n = crawl_bizinfo_gov(gov_file, gov_titles, checkpoint, args.max_pages // 2)
        total_gov += n
        log(f"✅ BizInfo-기술창업: {n}건 추가")
    except Exception as e:
        log(f"❌ BizInfo-기술창업 오류: {e}")
        import traceback; traceback.print_exc()

    save_checkpoint(checkpoint_file, checkpoint)
    time.sleep(SLEEP_SEC)

    # NIA
    try:
        n = crawl_nia(gov_file, gov_titles, checkpoint, args.max_pages // 2)
        total_gov += n
        log(f"✅ NIA: {n}건 추가")
    except Exception as e:
        log(f"❌ NIA 오류: {e}")
        import traceback; traceback.print_exc()

    save_checkpoint(checkpoint_file, checkpoint)

    # JS 필요 소스 스킵
    skip_js_required("MSS 중소벤처기업부",    "https://www.mss.go.kr/", checkpoint)
    skip_js_required("K-Startup",             "https://www.k-startup.go.kr/", checkpoint)
    skip_js_required("Innopolis 연구개발특구", "https://www.innopolis.or.kr/", checkpoint)
    skip_js_required("KISED 창업진흥원",       "https://www.kised.or.kr/", checkpoint)

    # ── 최종 저장 & 요약 ──────────────────────────────────
    save_checkpoint(checkpoint_file, checkpoint)

    log("")
    log("=" * 60)
    log(f"🏁 수집 완료")
    log(f"   소상공인 신규: {total_soho}건  (총 {len(soho_titles)}건)")
    log(f"   R&D/기술창업 신규: {total_gov}건  (총 {len(gov_titles)}건)")
    log(f"   출력: {output_dir}")
    log("=" * 60)
    log("")
    log("📝 JS 렌더링 필요 사이트 (Selenium/Playwright 필요):")
    log("   - SEMAS: https://www.semas.or.kr/web/board/boardList.do")
    log("   - MSS:   https://www.mss.go.kr/")
    log("   - K-Startup: https://www.k-startup.go.kr/")
    log("   - Innopolis: https://www.innopolis.or.kr/")
    log("   - KISED: https://www.kised.or.kr/")


if __name__ == "__main__":
    main()
