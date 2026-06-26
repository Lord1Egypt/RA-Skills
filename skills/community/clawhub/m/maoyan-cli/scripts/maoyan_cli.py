#!/usr/bin/env python3
"""
猫眼电影 CLI：城市、影院筛选、影院列表、排片、电影搜索、某电影上映影院。输出 JSON。

数据源：cities / filterCinemas / moreCinemas(HTML) / shows / search / movie cinemas.json / asgard/movie 详情页(HTML)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.parse import urlencode

# -----------------------------------------------------------------------------
# 常量（便于维护与 AI 理解）
# -----------------------------------------------------------------------------

MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
)
BASE = "https://m.maoyan.com"
URLS = {
    "cities": f"{BASE}/dianying/cities.json",
    "filter": f"{BASE}/ajax/filterCinemas",
    "more_cinemas": f"{BASE}/ajax/moreCinemas",
    "shows": f"{BASE}/mtrade/cinema/cinema/shows.json",
    "search": f"{BASE}/apollo/ajax/search",
    "movie_cinemas": f"{BASE}/api/mtrade/mmcs/cinema/movie/cinemas.json",
    "movie_detail": f"{BASE}/asgard/movie",  # 详情页 HTML，路径 /asgard/movie/{movieId}
}
# 直达链接（打开即可选场/选座买票）
LINK_CINEMA_PAGE = f"{BASE}/mtrade/cinema/cinema"   # 某电影某影院某日期选场页
LINK_SEAT_PAGE = f"{BASE}/mtrade/cinema/seat"       # 某场次选座买票页（需 seqNo）


def _cinema_page_url(cinema_id: str, movie_id, date: str) -> str:
    return f"{LINK_CINEMA_PAGE}?{urlencode({'cinemaId': cinema_id, 'movieId': movie_id, 'date': date})}"


def _seat_url(seq_no: str, cinema_id: str, movie_id, date: str) -> str:
    return f"{LINK_SEAT_PAGE}?{urlencode({'seqNo': seq_no, 'cinemaId': cinema_id, 'movieId': movie_id, 'date': date})}"
DEFAULT_CI = "1"
TIMEOUT = 15

# -----------------------------------------------------------------------------
# HTTP 与输出
# -----------------------------------------------------------------------------


def fetch(url: str, *, method: str = "GET", data: dict | None = None) -> str:
    """请求 URL，返回响应正文。"""
    if data and method == "POST":
        body = urlencode(data).encode("utf-8")
        req = Request(url, data=body, headers={"User-Agent": MOBILE_UA}, method="POST")
    else:
        req = Request(url, headers={"User-Agent": MOBILE_UA})
    with urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read().decode("utf-8")


def fetch_json(url: str) -> dict:
    """GET 请求并解析 JSON。"""
    return json.loads(fetch(url))


def print_json(obj: dict) -> None:
    """统一 JSON 输出格式（indent=2, ensure_ascii=False）。"""
    print(json.dumps(obj, ensure_ascii=False, indent=2))


# -----------------------------------------------------------------------------
# moreCinemas HTML 解析（结构见 reference.md）
# -----------------------------------------------------------------------------

# 猫眼移动端：<a href="/shows/{id}"> 内 .title span=名称, .price=价格, .flex.line-ellipsis=地址, .distance=距离
_RE_BLOCK = re.compile(r'<a\s+href="/shows/(\d+)"[^>]*>([\s\S]*?)</a>', re.I)
_RE_NAME = re.compile(r'<div class="title[^"]*"[^>]*>\s*<span>([^<]+)</span>')
_RE_PRICE = re.compile(r'<span class="price">([^<]+)</span><span class="q">元起</span>')
_RE_ADDRESS = re.compile(r'<div class="flex line-ellipsis">([^<]+)</div>')
_RE_DISTANCE = re.compile(r'<div class="distance">([^<]+)</div>')


def parse_more_cinemas_html(html: str) -> list[dict]:
    """从 moreCinemas 返回的 HTML 解析影院列表。每项含 cinemaId, name, address, distance, price。"""
    out = []
    for m in _RE_BLOCK.finditer(html):
        cinema_id = m.group(1)
        block = m.group(2)
        name = (_RE_NAME.search(block).group(1).strip()[:80]) if _RE_NAME.search(block) else ""
        price_m = _RE_PRICE.search(block)
        price = (price_m.group(1).strip() + "元起") if price_m else ""
        addr_m = _RE_ADDRESS.search(block)
        address = (addr_m.group(1).strip()[:120]) if addr_m else ""
        dist_m = _RE_DISTANCE.search(block)
        distance = dist_m.group(1).strip() if dist_m else ""
        out.append({
            "cinemaId": cinema_id,
            "name": name,
            "address": address,
            "distance": distance,
            "price": price,
        })
    return out


# -----------------------------------------------------------------------------
# 电影详情页 HTML 解析（asgard/movie/{movieId}）
# -----------------------------------------------------------------------------

# 从 <meta name="share:wechat:message:title" content="《片名》猫眼购票评分X.X，上映信息" /> 等提取
_RE_DETAIL_TITLE_META = re.compile(
    r'<meta\s+name="share:wechat:message:title"\s+content="《([^》]+)》猫眼购票评分([\d.]+)[^"]*"',
    re.I,
)
_RE_DETAIL_DESC_META = re.compile(
    r'<meta\s+name="share:wechat:message:desc"\s+content="简介\|([^"]+)"',
    re.I | re.DOTALL,
)
_RE_DETAIL_ICON_META = re.compile(
    r'<meta\s+name="share:wechat:message:icon"\s+content="([^"]+)"',
    re.I,
)
_RE_DETAIL_PAGE_TITLE = re.compile(r'<title>([^_<]+)_购票', re.I)
_RE_DETAIL_CN_NAME = re.compile(r'<div class="movie-cn-name">\s*<h1[^>]*>([^<]+)</h1>\s*</div>', re.I)
_RE_DETAIL_EN_NAME = re.compile(r'<div class="movie-en-name">([^<]*)</div>', re.I)
_RE_DETAIL_CAT = re.compile(r'<span class="movie-cat">([^<]+)</span>', re.I)
_RE_DETAIL_SHOW_TIME = re.compile(r'<div class="movie-show-time">\s*<span>([^<]+)</span>\s*</div>', re.I)
_RE_DETAIL_SCORE = re.compile(r'<span class="score"[^>]*>([\d.]+)</span>', re.I)
_RE_DETAIL_SCORE_COUNT = re.compile(r'<div[^>]*>([\d,]+)\s*人评</div>', re.I)
_RE_DETAIL_ACTORS = re.compile(r'<div class="actors">([\s\S]*?)</div>', re.I)
_RE_DETAIL_ACTOR_LINK = re.compile(r'<a\s+href="/asgard/celebrity/\d+">([^<]+)</a>', re.I)
_RE_DETAIL_POSTER_IMG = re.compile(r'<img[^>]*class="[^"]*poster[^"]*"[^>]*\ssrc="([^"]+)"', re.I)
_RE_DETAIL_META_DESC = re.compile(r'<meta name="description" content="([^"]*)"', re.I)
_RE_DETAIL_META_KEYWORDS = re.compile(r'<meta name="keywords" content="([^"]*)"', re.I)
# 时长：从 "125分钟" 或 "2026-02-17 09:00中国大陆上映 / 125分钟" 中取
_RE_DETAIL_DUR = re.compile(r'(\d+)\s*分钟')


def parse_movie_detail_html(html: str, movie_id: str) -> dict:
    """从 asgard/movie 详情页 HTML 中正则匹配电影信息。返回 nm, enm, cat, actors, showTime, releaseInfo, durText, dur, sc, scoreCount, desc, posterUrl 等。"""
    out = {"id": movie_id, "nm": "", "enm": "", "cat": "", "actors": [], "showTime": "", "releaseInfo": "", "durText": "", "dur": None, "sc": "", "scoreCount": "", "desc": "", "posterUrl": "", "detailUrl": ""}
    # 分享用 meta（优先，格式稳定）
    m_title = _RE_DETAIL_TITLE_META.search(html)
    if m_title:
        out["nm"] = m_title.group(1).strip()
        out["sc"] = m_title.group(2).strip()
    m_desc = _RE_DETAIL_DESC_META.search(html)
    if m_desc:
        raw_desc = m_desc.group(1).strip().replace("\\n", "\n")
        out["desc"] = raw_desc[:2000] if len(raw_desc) > 2000 else raw_desc
    m_icon = _RE_DETAIL_ICON_META.search(html)
    if m_icon:
        out["posterUrl"] = m_icon.group(1).strip()
    # 页面内正文
    if not out["nm"]:
        m = _RE_DETAIL_PAGE_TITLE.search(html)
        if m:
            out["nm"] = m.group(1).strip()
    m_cn = _RE_DETAIL_CN_NAME.search(html)
    if m_cn:
        out["nm"] = m_cn.group(1).strip()
    m_en = _RE_DETAIL_EN_NAME.search(html)
    if m_en:
        out["enm"] = m_en.group(1).strip()
    m_cat = _RE_DETAIL_CAT.search(html)
    if m_cat:
        out["cat"] = m_cat.group(1).strip()
    m_show = _RE_DETAIL_SHOW_TIME.search(html)
    if m_show:
        raw_show = m_show.group(1).strip()
        out["showTime"] = raw_show
        # 拆成「上映/开播信息」与「时长文案」，避免混在一句里（如 "2019-10-06美国开播 / 45分钟"）
        if " / " in raw_show:
            part0, part1 = raw_show.split(" / ", 1)
            part0, part1 = part0.strip(), part1.strip()
            if _RE_DETAIL_DUR.search(part1):
                out["releaseInfo"] = part0
                out["durText"] = part1
            else:
                out["releaseInfo"] = raw_show
        else:
            out["releaseInfo"] = raw_show
    if not out["sc"]:
        m_sc = _RE_DETAIL_SCORE.search(html)
        if m_sc:
            out["sc"] = m_sc.group(1).strip()
    m_count = _RE_DETAIL_SCORE_COUNT.search(html)
    if m_count:
        out["scoreCount"] = m_count.group(1).strip()
    m_actors_block = _RE_DETAIL_ACTORS.search(html)
    if m_actors_block:
        block = m_actors_block.group(1)
        out["actors"] = [a.group(1).replace("\u00a0", " ").strip().rstrip(" /") for a in _RE_DETAIL_ACTOR_LINK.finditer(block)]
    if not out["posterUrl"]:
        m_poster = _RE_DETAIL_POSTER_IMG.search(html)
        if m_poster:
            out["posterUrl"] = m_poster.group(1).strip()
    m_meta_desc = _RE_DETAIL_META_DESC.search(html)
    if m_meta_desc and not out["desc"]:
        out["desc"] = m_meta_desc.group(1).strip()
    m_keywords = _RE_DETAIL_META_KEYWORDS.search(html)
    if m_keywords:
        out["keywords"] = m_keywords.group(1).strip()
    # 从 showTime 或 desc 中解析时长（分钟）
    dur_m = _RE_DETAIL_DUR.search(out["showTime"] or " " + (out.get("keywords") or "") + " " + out["desc"])
    if dur_m:
        out["dur"] = int(dur_m.group(1))
    out["detailUrl"] = f"{URLS['movie_detail']}/{movie_id}"
    return out


# -----------------------------------------------------------------------------
# 子命令：数据获取 + 输出
# -----------------------------------------------------------------------------


def cmd_cities(args: argparse.Namespace) -> None:
    """城市列表。支持 -q 过滤名称/拼音。"""
    raw = fetch_json(URLS["cities"])
    cities = raw.get("cts") or []
    if args.q:
        q = args.q.lower()
        cities = [c for c in cities if q in (c.get("nm") or "").lower() or q in (c.get("py") or "").lower()]
    print_json({"ok": True, "cities": cities} if cities else {"ok": False, "error": "未获取到城市列表", "cities": []})


def cmd_filter(args: argparse.Namespace) -> None:
    """影院筛选条件（品牌、行政区等）。用于 moreCinemas 的 brandId/districtId。"""
    raw = fetch_json(f"{URLS['filter']}?{urlencode({'ci': args.ci})}")
    print_json({"ok": True, "ci": args.ci, **raw})


def cmd_cinemas(args: argparse.Namespace) -> None:
    """影院列表（解析 moreCinemas HTML）。建议传 --lat/--lng（用户当前位置）以便按距离排序。"""
    day = args.day or datetime.now().strftime("%Y-%m-%d")
    params = {
        "day": day,
        "offset": args.offset,
        "limit": args.limit,
        "districtId": getattr(args, "districtId", "-1") or "-1",
        "lineId": "-1",
        "hallType": getattr(args, "hallType", "-1") or "-1",
        "brandId": getattr(args, "brandId", "-1") or "-1",
        "serviceId": "-1",
        "areaId": "-1",
        "stationId": "-1",
        "item": "",
        "updateShowDay": "false",
        "reqId": str(int(datetime.now().timestamp() * 1000)),
        "cityId": args.ci,
    }
    if args.lat and args.lng:
        params["lat"] = args.lat
        params["lng"] = args.lng
    html = fetch(f"{URLS['more_cinemas']}?{urlencode(params)}")
    cinemas = parse_more_cinemas_html(html)
    print_json({"ok": True, "day": day, "ci": args.ci, "cinemas": cinemas})


def cmd_shows(args: argparse.Namespace) -> None:
    """指定影院排片。输出中每部电影下每个日期含 cinemaPageUrl，每个场次含 seatUrl；场次价格用原价（originPrice）。"""
    params = {
        "cinemaId": args.cinema_id,
        "ci": args.ci,
        "userid": "",
        "channelId": "4",
        "yodaReady": "h5",
        "csecplatform": "4",
        "csecversion": "4.2.0",
    }
    raw = fetch_json(f"{URLS['shows']}?{urlencode(params)}")
    if raw.get("code") != 0:
        print(json.dumps({"ok": False, "error": raw.get("errMsg", str(raw))}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    data = raw.get("data") or {}
    cinema_name = data.get("cinemaName", "未知影院")
    cinema_id_out = str(data.get("cinemaId") or args.cinema_id)
    movies = data.get("movies") or []
    for m in movies:
        movie_id = str(m.get("id") or "")
        m["posterUrl"] = m.get("img") or ""
        for day_block in m.get("shows") or []:
            show_date = day_block.get("showDate") or day_block.get("dt") or ""
            day_block["cinemaPageUrl"] = _cinema_page_url(cinema_id_out, movie_id, show_date)
            for s in day_block.get("plist") or []:
                seq_no = s.get("seqNo")
                date_for_seat = s.get("dt") or show_date
                if seq_no:
                    s["seatUrl"] = _seat_url(str(seq_no), cinema_id_out, movie_id, date_for_seat)
                s["originPrice"] = s.get("vipPrice") or s.get("vipDisPrice")
    print_json({"ok": True, "cinemaId": cinema_id_out, "cinemaName": cinema_name, "ci": args.ci, "movies": movies})


def cmd_search(args: argparse.Namespace) -> None:
    """按关键词搜索电影。返回电影列表（含 id、nm、sc、posterUrl 封面图等），便于拿到 movieId 查上映影院。"""
    params = {"kw": args.kw, "cityId": args.ci, "stype": "-1"}
    raw = fetch_json(f"{URLS['search']}?{urlencode(params)}")
    movies_node = raw.get("movies") or {}
    lst = movies_node.get("list") or []
    total = movies_node.get("total", 0)
    for m in lst:
        m["posterUrl"] = m.get("img") or ""
    print_json({
        "ok": raw.get("success", False),
        "ci": args.ci,
        "keyword": args.kw,
        "total": total,
        "movies": lst,
    })


def cmd_detail(args: argparse.Namespace) -> None:
    """电影详情：请求 asgard/movie/{movieId} 详情页 HTML，用正则解析片名、评分、简介、类型、主演等。"""
    movie_id = str(args.movie_id)
    params = {"_v_": "yes", "channelId": "4", "ci": args.ci}
    if getattr(args, "cinemaId", None):
        params["cinemaId"] = args.cinemaId
    if args.lat:
        params["lat"] = args.lat
    if args.lng:
        params["lng"] = args.lng
    url = f"{URLS['movie_detail']}/{movie_id}?{urlencode(params)}"
    try:
        html = fetch(url)
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e), "movieId": movie_id}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    detail = parse_movie_detail_html(html, movie_id)
    print_json({"ok": True, "movieId": movie_id, "movie": detail})


def cmd_movie_cinemas(args: argparse.Namespace) -> None:
    """某部电影在某城市的上映影院列表。建议传 --lat/--lng（用户当前位置）以便按距离排序。"""
    day = args.day or datetime.now().strftime("%Y-%m-%d")
    hall_type_ids = args.hallTypeIds.strip().lower()
    if hall_type_ids in ("", "all"):
        hall_type_ids_json = '["all"]'
    else:
        ids = [x.strip() for x in hall_type_ids.split(",") if x.strip()]
        hall_type_ids_json = json.dumps(ids)
    params = {
        "limit": args.limit,
        "offset": args.offset,
        "showDate": day,
        "movieId": args.movie_id,
        "sort": args.sort,
        "cityId": args.ci,
        "ci": args.ci,
        "districtId": "-1",
        "lineId": "-1",
        "areaId": "-1",
        "stationId": "-1",
        "brandIds": "[-1]",
        "serviceIds": "[-1]",
        "hallTypeIds": hall_type_ids_json,
        "languageIds": '["all"]',
        "dimIds": '["all"]',
        "utm_term": "7.5",
        "client": "iphone",
        "channelId": "4",
        "yodaReady": "h5",
        "csecplatform": "4",
        "csecversion": "4.2.0",
    }
    if args.lat and args.lng:
        params["lat"] = args.lat
        params["lng"] = args.lng
    raw = fetch_json(f"{URLS['movie_cinemas']}?{urlencode(params)}")
    if raw.get("code") != 0 and not raw.get("success", False):
        err = raw.get("errMsg", raw.get("message", str(raw)))
        print(json.dumps({"ok": False, "error": err}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    data = raw.get("data") or {}
    cinemas = data.get("cinemas") or []
    paging = data.get("paging") or {}
    movie_id = str(args.movie_id)
    show_date = data.get("showDate") or day
    for c in cinemas:
        c["cinemaPageUrl"] = _cinema_page_url(str(c.get("id", "")), movie_id, show_date)
    print_json({
        "ok": True,
        "movieId": args.movie_id,
        "ci": args.ci,
        "showDate": show_date,
        "cinemas": cinemas,
        "paging": paging,
    })


# -----------------------------------------------------------------------------
# CLI 入口
# -----------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="猫眼电影 CLI：城市/影院筛选/影院列表/排片。输出 JSON。")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("cities", help="城市列表")
    p.add_argument("-q", help="按名称或拼音过滤")
    p.set_defaults(ci=DEFAULT_CI, run=cmd_cities)

    p = sub.add_parser("filter", help="影院筛选条件（品牌/区域 ID）")
    p.add_argument("ci", nargs="?", default=DEFAULT_CI, help="城市 ID")
    p.set_defaults(run=cmd_filter)

    p = sub.add_parser("cinemas", help="影院列表（分页）")
    p.add_argument("ci", nargs="?", default=DEFAULT_CI, help="城市 ID")
    p.add_argument("--day", help="日期 YYYY-MM-DD")
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--districtId", default="-1")
    p.add_argument("--brandId", default="-1")
    p.add_argument("--hallType", default="-1", help="影厅类型 ID，见 filter 子命令 hallType.subItems，-1 为全部")
    p.add_argument("--lat", help="纬度（建议传用户当前位置，便于按距离排序）")
    p.add_argument("--lng", help="经度（建议传用户当前位置，便于按距离排序）")
    p.set_defaults(run=cmd_cinemas)

    p = sub.add_parser("shows", help="影院排片")
    p.add_argument("cinema_id", help="影院 ID")
    p.add_argument("ci", nargs="?", default=DEFAULT_CI, help="城市 ID")
    p.set_defaults(run=cmd_shows)

    p = sub.add_parser("search", help="按关键词搜索电影")
    p.add_argument("kw", help="搜索关键词（片名等）")
    p.add_argument("ci", nargs="?", default=DEFAULT_CI, help="城市 ID")
    p.set_defaults(run=cmd_search)

    p = sub.add_parser("detail", help="电影详情（从详情页 HTML 正则解析）")
    p.add_argument("movie_id", help="电影 ID（可从 search 获得）")
    p.add_argument("ci", nargs="?", default=DEFAULT_CI, help="城市 ID")
    p.add_argument("--cinemaId", help="可选，影院 ID（用于带影院上下文打开详情）")
    p.add_argument("--lat", help="可选，纬度")
    p.add_argument("--lng", help="可选，经度")
    p.set_defaults(run=cmd_detail)

    p = sub.add_parser("movie-cinemas", help="某电影的上映影院列表")
    p.add_argument("movie_id", help="电影 ID（可从 search 子命令获得）")
    p.add_argument("ci", nargs="?", default=DEFAULT_CI, help="城市 ID")
    p.add_argument("--day", help="日期 YYYY-MM-DD")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--sort", default="distance", help="排序：distance / 价格等")
    p.add_argument("--hallTypeIds", default="all", help='影厅类型 ID，逗号分隔如 "1,2,3"，all 或不传为全部')
    p.add_argument("--lat", help="纬度（建议传用户当前位置，便于按距离排序）")
    p.add_argument("--lng", help="经度（建议传用户当前位置，便于按距离排序）")
    p.set_defaults(run=cmd_movie_cinemas)

    args = parser.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
