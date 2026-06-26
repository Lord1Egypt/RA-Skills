#!/usr/bin/env python3
"""
news-monitor.py — 新闻盯盘守护进程

数据源（一期）：
  - 金十数据：https://www.jin10.com/flash_newest.js
    ⚠️  非官方接口，URL 和响应格式随时可能变化，做好降级处理
  - 华尔街见闻：https://api-one.wallstcn.com/apiv1/content/lives
    ⚠️  非官方接口，同上
  - RSS feeds：CoinDesk、CoinTelegraph、The Block、Decrypt（标准 RSS 2.0 / Atom）

核心逻辑：
  - 轮询间隔：由活跃警报中最小的 poll_interval 决定（默认 300s）
  - 去重：基于 (source + item_id/url) 的 MD5 hash，存在 state 文件中
    滚动窗口：每个警报保留最近 MAX_SEEN_HASHES=1000 个 hash
  - 关键词匹配：大小写不敏感，支持中英文
    keyword_mode: "any"（任一命中）| "all"（全部命中）
  - 命中后：openclaw agent --deliver 通知（复用 price-monitor 通知管道）
  - 单轮多命中时聚合为一条通知（M-04）
  - 无活跃 news alert 时自动退出并清理 PID 文件
  - 日志：RotatingFileHandler（512KB × 3）

用法：
  python3 news-monitor.py --agent laok
  python3 news-monitor.py --agent laok --alerts-file /path/to/alerts.json
"""

import argparse
import hashlib
import json
import logging
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

# 公共工具（deliver_message / atomic_write_json）
sys.path.insert(0, str(Path(__file__).parent))
from common import deliver_message, atomic_write_json  # noqa: E402

try:
    import requests
except ImportError:
    print("需要 requests: pip3 install requests")
    exit(1)

import os as _os

# ── Proxy 配置 ────────────────────────────────────────────────────────────────
# 从环境变量读取代理。MARKET_WATCH_PROXY 优先，其次标准变量，无则裸连。
def _get_proxy_config() -> dict:
    proxy_url = (
        _os.environ.get("MARKET_WATCH_PROXY")
        or _os.environ.get("HTTPS_PROXY")
        or _os.environ.get("https_proxy")
        or _os.environ.get("HTTP_PROXY")
        or _os.environ.get("http_proxy")
        or _os.environ.get("ALL_PROXY")
        or _os.environ.get("all_proxy")
    )
    if proxy_url:
        return {"http": proxy_url, "https": proxy_url}
    return {}
REQUEST_PROXIES = _get_proxy_config()

# ── Logging ────────────────────────────────────────────────────────────────────

log = logging.getLogger("news-monitor")
log.setLevel(logging.INFO)
_formatter = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%H:%M:%S")

MAX_LOG_BYTES    = 512 * 1024   # 512KB 单个日志文件上限
LOG_BACKUP_COUNT = 3            # 保留3个轮转备份，总约 2MB

# ── 全局配置 ──────────────────────────────────────────────────────────────────

HTTP_TIMEOUT      = 10          # 秒
MAX_SEEN_HASHES   = 1000        # 每个警报的去重 hash 滚动窗口上限
FAILURE_ALERT_SEC = 600         # 连续 10 分钟全部源失败才告警

# ── RSS 源定义（标准 RSS 2.0 / Atom）─────────────────────────────────────────

RSS_SOURCES: dict[str, str] = {
    "coindesk":      "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "cointelegraph": "https://cointelegraph.com/rss",
    "theblock":      "https://www.theblock.co/rss.xml",
    "decrypt":       "https://decrypt.co/feed",
}

ALL_SOURCES = ["jin10", "wallstreetcn"] + list(RSS_SOURCES.keys())

# ── HTTP 请求头（伪装浏览器）─────────────────────────────────────────────────

_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

BROWSER_HEADERS: dict[str, str] = {
    "User-Agent":      _UA,
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection":      "keep-alive",
}

JIN10_HEADERS: dict[str, str] = {
    **BROWSER_HEADERS,
    "Accept":          "application/json, text/javascript, */*; q=0.01",
    "Referer":         "https://www.jin10.com/",
    "Origin":          "https://www.jin10.com",
    "X-Requested-With": "XMLHttpRequest",
}

WALLST_HEADERS: dict[str, str] = {
    **BROWSER_HEADERS,
    "Accept":  "application/json, text/plain, */*",
    "Referer": "https://wallstreetcn.com/",
    "Origin":  "https://wallstreetcn.com",
}

RSS_HEADERS: dict[str, str] = {
    **BROWSER_HEADERS,
    "Accept": "application/rss+xml,application/atom+xml,application/xml,text/xml,*/*;q=0.9",
}

# ── 数据源抓取 ─────────────────────────────────────────────────────────────────

def _make_hash(source: str, item_id: str) -> str:
    """生成 16 字符去重 hash（MD5 前缀）"""
    return hashlib.md5(f"{source}:{item_id}".encode()).hexdigest()[:16]


def _strip_html(text: str) -> str:
    """简单去除 HTML 标签"""
    return re.sub(r"<[^>]+>", " ", text or "").strip()


def fetch_jin10() -> list[dict]:
    """
    金十数据快讯
    ⚠️  非官方接口：URL 和响应格式随时可能变化。
        已知格式：JS 变量赋值 "var flash_newest={...};" 或直接 JSON
        字段：id（字符串）, content（快讯内容）, time（时间字符串）

    降级策略：
      1. 直接尝试解析为 JSON
      2. 用正则提取第一个 {...} 块再解析
      3. 两者均失败 → 静默跳过本轮（不影响其他数据源）
    """
    url = "https://www.jin10.com/flash_newest.js"
    try:
        resp = requests.get(url, headers=JIN10_HEADERS, proxies=REQUEST_PROXIES, timeout=HTTP_TIMEOUT)
        resp.raise_for_status()
        text = resp.text.strip()

        # 降级1：直接解析 JSON
        data: Optional[dict | list] = None
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            # 降级2：剥离 JS 变量赋值前缀（"var xxx={...};"）
            m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
            if m:
                try:
                    data = json.loads(m.group())
                except json.JSONDecodeError:
                    pass

        if data is None:
            log.debug("jin10: 无法解析响应，可能接口格式已变更，跳过本轮")
            return []

        # 支持多种响应结构
        raw_list: list = []
        if isinstance(data, list):
            raw_list = data
        elif isinstance(data, dict):
            # 尝试 {"data": [...]} 或 {"code":0, "data": [...]} 等常见结构
            raw_list = data.get("data", [])
            if not raw_list and isinstance(data.get("data"), dict):
                raw_list = data["data"].get("items", [])

        items = []
        for item in raw_list:
            item_id = str(item.get("id", "")).strip()
            content = _strip_html(item.get("content", "") or item.get("body", "")).strip()
            if not item_id or not content:
                continue
            items.append({
                "id":      item_id,
                "title":   content[:120],   # 快讯无独立标题，用正文前120字
                "content": content,
                "source":  "jin10",
                "hash":    _make_hash("jin10", item_id),
            })
        return items

    except requests.RequestException as e:
        log.debug(f"jin10 请求失败: {e}")
        return []
    except Exception as e:
        log.debug(f"jin10 解析异常（接口可能变更，需更新解析器）: {e}")
        return []


def fetch_wallstreetcn() -> list[dict]:
    """
    华尔街见闻快讯
    ⚠️  非官方接口：响应结构可能随版本迭代变化。
        已知路径：data.items[].{id, title, summary}
                  data.list[].{id, title, summary} (备用)

    降级策略：尝试多种路径，均失败则静默跳过本轮
    """
    url = "https://api-one.wallstcn.com/apiv1/content/lives"
    params = {"channel": "global-channel", "limit": 20}
    try:
        resp = requests.get(url, headers=WALLST_HEADERS, params=params, proxies=REQUEST_PROXIES, timeout=HTTP_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        items_raw: list = []
        if isinstance(data, dict):
            nested = data.get("data", {})
            if isinstance(nested, dict):
                items_raw = (nested.get("items") or nested.get("list") or [])
            elif isinstance(nested, list):
                items_raw = nested
        elif isinstance(data, list):
            items_raw = data

        if not items_raw:
            log.debug("wallstreetcn: 无法解析响应结构，可能接口变更，跳过本轮")
            return []

        items = []
        for item in items_raw:
            item_id = str(item.get("id", "")).strip()
            title   = _strip_html(item.get("title", "") or "")
            summary = _strip_html(item.get("summary", "") or item.get("content", "") or "")
            content = (f"{title} {summary}").strip()
            if not item_id or not content:
                continue
            items.append({
                "id":      item_id,
                "title":   title or summary[:80],
                "content": content,
                "source":  "wallstreetcn",
                "hash":    _make_hash("wallstreetcn", item_id),
            })
        return items

    except requests.RequestException as e:
        log.debug(f"wallstreetcn 请求失败: {e}")
        return []
    except Exception as e:
        log.debug(f"wallstreetcn 解析异常（接口可能变更）: {e}")
        return []


def fetch_rss(source_name: str, feed_url: str) -> list[dict]:
    """
    解析标准 RSS 2.0 / Atom feed。
    使用标准库 xml.etree.ElementTree，无额外依赖。
    """
    headers = {**RSS_HEADERS, "Referer": feed_url}
    try:
        resp = requests.get(feed_url, headers=headers, proxies=REQUEST_PROXIES, timeout=HTTP_TIMEOUT)
        resp.raise_for_status()

        # 解析 XML
        root = ET.fromstring(resp.content)

        items_raw: list[ET.Element] = []
        # RSS 2.0: <rss><channel><item>...</item></channel></rss>
        channel = root.find("channel")
        if channel is not None:
            items_raw = channel.findall("item")
        else:
            # Atom: <feed xmlns="http://www.w3.org/2005/Atom"><entry>...</entry></feed>
            # ElementTree 用 {ns}tag 格式处理命名空间
            ns_atom = "http://www.w3.org/2005/Atom"
            items_raw = (
                root.findall(f"{{{ns_atom}}}entry") or
                root.findall("entry")                  # 无命名空间
            )

        items = []
        for entry in items_raw:
            # RSS 2.0 字段
            title = (entry.findtext("title") or "").strip()
            link  = (entry.findtext("link") or "").strip()
            desc  = (entry.findtext("description") or "").strip()
            guid  = (entry.findtext("guid") or "").strip()

            # Atom 字段 fallback
            ns_a = "http://www.w3.org/2005/Atom"
            if not title:
                title = (entry.findtext(f"{{{ns_a}}}title") or "").strip()
            if not link:
                link_el = entry.find(f"{{{ns_a}}}link")
                if link_el is not None:
                    link = link_el.get("href", "")
                    if not link:
                        link = (link_el.text or "").strip()
            if not guid:
                guid = (entry.findtext(f"{{{ns_a}}}id") or link).strip()
            if not desc:
                desc = (
                    entry.findtext(f"{{{ns_a}}}summary") or
                    entry.findtext(f"{{{ns_a}}}content") or ""
                ).strip()

            # 用 link 作为 guid 兜底
            if not guid and link:
                guid = link
            if not guid or not title:
                continue

            content = _strip_html(f"{title} {desc}").strip()

            items.append({
                "id":      guid,
                "title":   _strip_html(title),
                "content": content,
                "source":  source_name,
                "hash":    _make_hash(source_name, guid),
            })
        return items

    except requests.RequestException as e:
        log.debug(f"{source_name} 请求失败: {e}")
        return []
    except ET.ParseError as e:
        log.debug(f"{source_name} XML 解析失败: {e}")
        return []
    except Exception as e:
        log.debug(f"{source_name} 异常: {e}")
        return []


# ── 关键词匹配 ─────────────────────────────────────────────────────────────────

def keywords_match(item: dict, keywords: list[str], mode: str) -> list[str]:
    """
    返回命中的关键词列表（空列表 = 未命中）。
    大小写不敏感，支持中英文。
    mode: "any"（任一命中即返回）| "all"（全部命中才返回）
    """
    text = (item.get("title", "") + " " + item.get("content", "")).lower()
    matched = [kw for kw in keywords if kw.strip() and kw.strip().lower() in text]
    if mode == "any":
        return matched
    else:  # "all"
        return matched if len(matched) == len([kw for kw in keywords if kw.strip()]) else []


# ── 通知 ──────────────────────────────────────────────────────────────────────

SOURCE_DISPLAY = {
    "jin10":         "金十数据",
    "wallstreetcn":  "华尔街见闻",
    "coindesk":      "CoinDesk",
    "cointelegraph": "CoinTelegraph",
    "theblock":      "The Block",
    "decrypt":       "Decrypt",
}


def fire_news_alert(alert: dict, item: dict, matched_keywords: list[str]) -> None:
    ts          = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    source_name = SOURCE_DISPLAY.get(item["source"], item["source"])
    content     = item.get("content", "").strip()
    link        = item.get("link", "")

    msg = (
        f"[NEWS_ALERT 触发 · 需要你判断]\n\n"
        f"命中关键词：{', '.join(matched_keywords)}\n"
        f"来源：{source_name}\n"
        f"标题：{item['title'][:200]}\n"
        f"{'链接：' + link if link else ''}\n"
        f"触发时间：{ts}\n\n"
        f"{'正文内容：' + chr(10) + content[:2000] + chr(10) if content else ''}\n"
        f"设盘背景：\n{alert.get('context_summary', '（未记录）')}\n\n"
        f"你的任务：\n"
        f"1. 阅读完整新闻内容，结合设盘背景判断：这条新闻是否真的跟用户关心的事相关？\n"
        f"2. 关键词匹配只是粗筛，你需要做精筛——如果内容无关或重要性不足，忽略即可，不要打扰用户\n"
        f"3. 如果确实相关且重要：联系用户，附上你的分析和建议\n"
        f"4. 如果拿不准：宁可不发，避免噪音"
    )

    log.info(f"🔔 NEWS_ALERT: [{item['source']}] {item['title'][:60]} | kw={matched_keywords}")
    deliver_message(alert, msg)


def fire_news_alert_batch(
    alert: dict, matches: list[tuple[dict, list[str]]]
) -> None:
    """
    M-04: 单轮多命中时聚合为一条通知，避免通知轰炸。
    格式：列出所有命中的标题+来源，不逐条推送。
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_keywords = sorted({kw for _, matched in matches for kw in matched})

    items_text = ""
    for i, (item, matched) in enumerate(matches[:10], 1):
        source_name = SOURCE_DISPLAY.get(item["source"], item["source"])
        items_text += f"{i}. [{source_name}] {item['title'][:150]}\n"
    if len(matches) > 10:
        items_text += f"... 还有 {len(matches) - 10} 条\n"

    # 批量通知也附带每条新闻的正文摘要
    details_text = ""
    for i, (item, matched) in enumerate(matches[:10], 1):
        source_name = SOURCE_DISPLAY.get(item["source"], item["source"])
        content = item.get("content", "").strip()
        link = item.get("link", "")
        details_text += f"\n--- [{i}] [{source_name}] {item['title'][:150]} ---\n"
        if link:
            details_text += f"链接：{link}\n"
        if content:
            details_text += f"{content[:500]}\n"
    if len(matches) > 10:
        details_text += f"\n... 还有 {len(matches) - 10} 条未展示\n"

    msg = (
        f"[NEWS_ALERT 触发 · 本轮 {len(matches)} 条命中 · 需要你判断]\n\n"
        f"命中关键词：{', '.join(all_keywords)}\n"
        f"触发时间：{ts}\n\n"
        f"命中新闻：\n{details_text}\n\n"
        f"设盘背景：\n{alert.get('context_summary', '（未记录）')}\n\n"
        f"你的任务：\n"
        f"1. 逐条阅读以上新闻内容，结合设盘背景判断：哪些是真正相关的？哪些只是关键词碰巧命中的噪音？\n"
        f"2. 只把确实重要且相关的新闻告知用户，附上你的分析\n"
        f"3. 噪音直接过滤掉，不要打扰用户\n"
        f"4. 如果全部都是噪音 → 不联系用户"
    )

    log.info(
        f"🔔 NEWS_ALERT (batch {len(matches)}): {alert['id']} | kw={all_keywords}"
    )
    deliver_message(alert, msg)


def notify_failure(agent_id: str, alerts_file: Path, minutes: int) -> None:
    """连续抓取失败超过阈值，通知 agent（N-02: 从活跃警报读取路由信息）"""
    msg = (
        f"[NEWS_ALERT · 系统异常]\n\n"
        f"新闻监控已连续 {minutes} 分钟无法从任何数据源获取数据。\n"
        f"可能原因：网络代理故障 / 所有新闻 API 不可达。\n\n"
        f"你的任务：\n"
        f"1. 告知用户新闻监控程序取数异常\n"
        f"2. 检查网络和代理状态"
    )
    route_alert: dict = {"agent_id": agent_id}
    try:
        if alerts_file.exists():
            data = json.loads(alerts_file.read_text())
            active = [a for a in data.get("alerts", [])
                      if a.get("status") == "active" and a.get("type") == "news"]
            if active:
                route_alert = active[0]
    except Exception:
        pass
    deliver_message(route_alert, msg)


# ── 状态管理 ──────────────────────────────────────────────────────────────────

def load_state(state_file: Path) -> dict:
    if state_file.exists():
        try:
            with open(state_file) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_state(state_file: Path, state: dict) -> None:
    try:
        state_file.parent.mkdir(parents=True, exist_ok=True)
        # S-02: 原子写入状态文件
        atomic_write_json(state_file, state)
    except Exception as e:
        log.warning(f"状态文件写入失败: {e}")


def update_seen_hashes(state: dict, alert_id: str, new_hashes: list[str]) -> None:
    """追加新 hash，超出 MAX_SEEN_HASHES 则截断（滚动窗口）"""
    entry = state.setdefault(alert_id, {"last_checked": "", "seen_hashes": []})
    seen = entry["seen_hashes"]
    seen.extend(new_hashes)
    if len(seen) > MAX_SEEN_HASHES:
        entry["seen_hashes"] = seen[-MAX_SEEN_HASHES:]
    entry["last_checked"] = datetime.now().isoformat()


# ── 数据抓取协调 ──────────────────────────────────────────────────────────────

def fetch_all_sources(enabled_sources: set[str]) -> dict[str, list[dict]]:
    """抓取所有启用的数据源，返回 {source_name: [items]}"""
    results: dict[str, list[dict]] = {}

    if "jin10" in enabled_sources:
        results["jin10"] = fetch_jin10()

    if "wallstreetcn" in enabled_sources:
        results["wallstreetcn"] = fetch_wallstreetcn()

    for src_name, feed_url in RSS_SOURCES.items():
        if src_name in enabled_sources:
            results[src_name] = fetch_rss(src_name, feed_url)

    return results


# ── 主循环 ────────────────────────────────────────────────────────────────────

def _setup_logging(agent_id: str) -> None:
    log_file = Path(f"/tmp/market-watch-{agent_id}-news.log")
    handler = RotatingFileHandler(
        str(log_file), maxBytes=MAX_LOG_BYTES, backupCount=LOG_BACKUP_COUNT,
    )
    handler.setFormatter(_formatter)
    log.addHandler(handler)
    # stderr 同时输出（daemon.sh 的 > /dev/null 2>&1 会丢弃，不影响 RotatingFileHandler）
    console = logging.StreamHandler()
    console.setFormatter(_formatter)
    log.addHandler(console)


def run(agent_id: str, alerts_file: Path, state_file: Path) -> None:
    _setup_logging(agent_id)
    log.info(f"=== news-monitor start | agent={agent_id} ===")

    consecutive_fail_since: Optional[float] = None
    failure_notified = False
    pid_file = Path(f"/tmp/market-watch-{agent_id}-news.pid")

    while True:
        cycle_start = time.time()

        # ── 读取活跃新闻警报 ──────────────────────────────────────────────────
        try:
            data = json.loads(alerts_file.read_text()) if alerts_file.exists() else {"alerts": []}
        except Exception:
            data = {"alerts": []}

        alerts      = data.get("alerts", [])
        news_active = [a for a in alerts if a.get("status") == "active" and a.get("type") == "news"]

        # 无活跃新闻警报 → 自动退出
        if not news_active:
            log.info("无活跃新闻警报，守护进程自动退出")
            pid_file.unlink(missing_ok=True)
            return

        # ── 收集本轮需要的数据源 ──────────────────────────────────────────────
        all_needed: set[str] = set()
        for alert in news_active:
            srcs = alert.get("sources", ALL_SOURCES)
            all_needed.update(srcs)

        # ── 抓取所有源 ────────────────────────────────────────────────────────
        fetched = fetch_all_sources(all_needed)
        any_success = any(len(v) > 0 for v in fetched.values())

        if any_success:
            consecutive_fail_since = None
            failure_notified = False
        else:
            if consecutive_fail_since is None:
                consecutive_fail_since = time.time()
            elapsed_fail = time.time() - consecutive_fail_since
            if elapsed_fail >= FAILURE_ALERT_SEC and not failure_notified:
                notify_failure(agent_id, alerts_file, int(elapsed_fail / 60))
                failure_notified = True

        # ── 加载去重状态 ──────────────────────────────────────────────────────
        state = load_state(state_file)

        # ── 逐警报处理 ────────────────────────────────────────────────────────
        modified_alerts = False
        state_changed   = False

        for alert in news_active:
            alert_id   = alert["id"]
            keywords   = [kw.strip() for kw in alert.get("keywords", []) if kw.strip()]
            mode       = alert.get("keyword_mode", "any")
            alert_srcs = set(alert.get("sources", ALL_SOURCES))
            one_shot   = alert.get("one_shot", False)

            if not keywords:
                continue

            seen_hashes = set(state.get(alert_id, {}).get("seen_hashes", []))
            new_hashes: list[str] = []

            # M-04: 收集本轮所有命中项，最后聚合通知
            matches: list[tuple[dict, list[str]]] = []  # (item, matched_keywords)

            for src_name, items in fetched.items():
                if src_name not in alert_srcs:
                    continue
                for item in items:
                    h = item["hash"]
                    if h in seen_hashes:
                        continue
                    # 这是新 item，加入去重集
                    new_hashes.append(h)
                    seen_hashes.add(h)

                    matched = keywords_match(item, keywords, mode)
                    if matched:
                        matches.append((item, matched))
                        if one_shot:
                            break
                if matches and one_shot:
                    break

            # 更新去重 hash
            if new_hashes:
                update_seen_hashes(state, alert_id, new_hashes)
                state_changed = True

            # M-04: 聚合发送 — 1 条直接发，多条聚合
            if matches:
                if len(matches) == 1:
                    item, matched_kws = matches[0]
                    fire_news_alert(alert, item, matched_kws)
                else:
                    fire_news_alert_batch(alert, matches)

                # one_shot 触发后标记为 triggered
                if one_shot:
                    alert["status"]       = "triggered"
                    alert["triggered_at"] = datetime.now().isoformat()
                    modified_alerts = True
                    log.info(f"NEWS_ALERT {alert_id} triggered (one_shot), 已标记完成")

        # ── 持久化 ────────────────────────────────────────────────────────────
        if state_changed:
            save_state(state_file, state)

        if modified_alerts:
            data["alerts"] = alerts
            # S-02: 原子替换写入，防并发损坏
            try:
                atomic_write_json(alerts_file, data)
            except Exception as e:
                log.warning(f"写入 alerts 文件失败: {e}")

        # ── 周期日志 ──────────────────────────────────────────────────────────
        total_items = sum(len(v) for v in fetched.values())
        src_summary = " | ".join(f"{k}:{len(v)}" for k, v in sorted(fetched.items()))
        log.info(
            f"Poll done | items={total_items} [{src_summary}] "
            f"| active_alerts={len(news_active)}"
        )

        # ── 等待下一轮（取活跃警报中最小 poll_interval）────────────────────
        min_interval = min(
            (a.get("poll_interval", 300) for a in news_active),
            default=300,
        )
        elapsed = time.time() - cycle_start
        sleep_time = max(10.0, min_interval - elapsed)
        log.info(f"下次轮询 in {sleep_time:.0f}s")
        time.sleep(sleep_time)


# ── 入口 ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="News Monitor Daemon")
    parser.add_argument("--agent",       default="laok",  help="Agent ID")
    parser.add_argument("--alerts-file", default="",      help="自定义 alerts 文件路径")
    parser.add_argument("--state-file",  default="",      help="自定义状态文件路径")
    args = parser.parse_args()

    base_dir     = Path.home() / f".openclaw/agents/{args.agent}/private"
    alerts_file  = Path(args.alerts_file) if args.alerts_file else base_dir / "market-alerts.json"
    state_file   = Path(args.state_file)  if args.state_file  else base_dir / "news-monitor-state.json"

    alerts_file.parent.mkdir(parents=True, exist_ok=True)

    run(args.agent, alerts_file, state_file)
