#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多平台AI信息源 — 共享核心模块
================================
五个平台（快手 / 公众号 / B站 / 视频号 / 小红书）的 AI 爆款内容聚合逻辑全部收敛在此：
配置表 → 鉴权 → 日期预检 → 取数 → 归一化 → 聚类 → 统计 → 情报 → 渲染 → 订阅。

平台差异只体现在 PLATFORMS 配置表里，新增平台只需加一个表项。
接口契约详见 references/platforms.md。
"""

import json
import os
import re
import subprocess
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ─── 全局配置 ──────────────────────────────────────────────────────────────────────
ENV_KEY = "REDFOX_API_KEY"
CONFIG_FILE = Path.home() / ".qoder" / "apis" / "redfox.json"
DEFAULT_OUTPUT_DIR = Path.home() / "Downloads" / "QoderReports"

SKILL_NAME = "多平台AI信息源"
REPORT_PREFIX = "AI多平台日报"
PLIST_LABEL = "com.qoder.multi-ai-feed"
PLIST_DIR = Path.home() / "Library" / "LaunchAgents"
SUBSCRIBE_HOUR = 17          # 覆盖 15:00 / 16:00 两个数据更新边界
SUBSCRIBE_MINUTE = 0

API_KEY_DOC = "https://redfox.hk/login"
MORE_DATA_DOC = "https://redfox.hk/settings/api-keys?source=clawhub"

# ─── 终端颜色（非 tty / NO_COLOR 时自动降级为纯文本） ────────────────────────────────
_RAW_GREEN = "\033[92m"
_RAW_YELLOW = "\033[93m"
_RAW_RED = "\033[91m"
_RAW_CYAN = "\033[96m"
_RAW_BOLD = "\033[1m"
_RAW_RESET = "\033[0m"

_COLOR_ENABLED = sys.stdout.isatty() and not os.environ.get("NO_COLOR")

# 日志输出流：--json 模式下改到 stderr，让 stdout 只留 JSON 载荷
_LOG_STREAM = sys.stdout


def disable_color():
    """关闭 ANSI 颜色（Agent 聊天界面、重定向到文件时使用）"""
    global _COLOR_ENABLED
    _COLOR_ENABLED = False


def use_stderr_for_logs():
    """把进度日志切到 stderr，stdout 专供结构化输出"""
    global _LOG_STREAM
    _LOG_STREAM = sys.stderr
    disable_color()


def _c(code):
    return code if _COLOR_ENABLED else ""


def GREEN():
    return _c(_RAW_GREEN)


def YELLOW():
    return _c(_RAW_YELLOW)


def RED():
    return _c(_RAW_RED)


def CYAN():
    return _c(_RAW_CYAN)


def BOLD():
    return _c(_RAW_BOLD)


def RESET():
    return _c(_RAW_RESET)


def info(msg):
    _LOG_STREAM.write(f"{GREEN()}[✓]{RESET()} {msg}\n")
    _LOG_STREAM.flush()


def warn(msg):
    _LOG_STREAM.write(f"{YELLOW()}[!]{RESET()} {msg}\n")
    _LOG_STREAM.flush()


def error(msg):
    _LOG_STREAM.write(f"{RED()}[✗]{RESET()} {msg}\n")
    _LOG_STREAM.flush()


def step(msg):
    _LOG_STREAM.write(f"{CYAN()}[→]{RESET()} {msg}\n")
    _LOG_STREAM.flush()


def progress(msg):
    """\r 原地刷新的进度行；必须走 _LOG_STREAM，否则会污染 --json 的 stdout"""
    _LOG_STREAM.write(f"\r{msg}")
    _LOG_STREAM.flush()


def log_newline():
    """结束当前进度行"""
    _LOG_STREAM.write("\n")
    _LOG_STREAM.flush()


def require_requests():
    if not HAS_REQUESTS:
        error("缺少 requests 库，请安装: pip3 install requests")
        sys.exit(1)


# ─── 平台配置表 ────────────────────────────────────────────────────────────────────
# 字段说明：
#   kw_mode        batch = 一次传 keywords 数组；single = 逐个关键词请求 keyword
#   paging         是否支持 pageNum 翻页
#   page_size      单页条数
#   max_pages      翻页上限（paging=False 时无效）
#   primary_kw     batch 模式下是否额外携带 keyword 主关键词字段
#   time_style     dt_2359 / dt_2400 / date_excl / none
#   update_hour    每日数据更新时间（小时）
#   rank_field     组内排序主指标；engagement = 点赞+分享+评论
#   metrics        (字段, 中文标签, HTML 图标, 是否可缺省) 列表
#   primary        统计卡主指标定义
#   link           详情链接模板，None 表示平台不支持站外跳转
#   cover_fix      封面兼容处理策略
PLATFORMS = {
    "kuaishou": {
        "name": "快手",
        "short": "ks",
        "aliases": ("ks", "kuaishou", "快手", "快手ai"),
        "endpoint": "https://redfox.hk/story/api/parseWork/queryKsAiMsgs/batch",
        "source": "AI快手信息源-ClawHub",
        "kw_mode": "batch",
        "paging": True,
        "page_size": 200,
        "max_pages": 10,
        "primary_kw": False,
        "time_style": "dt_2359",
        "update_hour": 15,
        "rank_field": "engagement",
        "metrics": (
            ("likeCount", "点赞", "&#x1f44d;", False),
            ("shareCount", "分享", "&#x1f501;", False),
            ("commentCount", "评论", "&#x1f4ac;", False),
        ),
        "primary": {"field": "engagement", "avg_label": "平均互动", "total_label": "总互动"},
        "accent": "#FF4906",
        "accent_light": "#FF7A45",
        "link": "https://www.kuaishou.com/short-video/{photoId}",
        "referer": "https://www.kuaishou.com/",
        "cover_fix": "kuaishou",
        "unit": "条",
        "default_keywords": ("AI", "人工智能", "大模型", "GPT", "Agent", "AI绘画", "AI教程"),
        "notice": "快手数据每日 15:00 更新前一天内容。",
    },
    "gzh": {
        "name": "公众号",
        "short": "gzh",
        "aliases": ("gzh", "wechat", "公众号", "微信公众号"),
        "endpoint": "https://redfox.hk/story/api/parseWork/queryAiMsgs",
        "source": "AI公众号信息源-ClawHub",
        "kw_mode": "single",
        "paging": True,
        "page_size": 20,
        "max_pages": 5,
        "primary_kw": False,
        "time_style": "none",
        "update_hour": 16,
        "rank_field": "engagement",
        "metrics": (
            ("likeCount", "点赞", "&#x1f44d;", False),
            ("shareCount", "分享", "&#x1f501;", False),
            ("commentCount", "评论", "&#x1f4ac;", True),
        ),
        "primary": {"field": "engagement", "avg_label": "平均互动", "total_label": "总互动"},
        "accent": "#FF5722",
        "accent_light": "#FF8A65",
        "link": None,
        "referer": "https://mp.weixin.qq.com/",
        "cover_fix": None,
        "unit": "篇",
        "default_keywords": ("AI", "人工智能", "大模型", "GPT", "Agent", "AI绘画"),
        "notice": "公众号接口不支持时间过滤，返回的是当前收录的最新文章，日期仅用于报告标注。",
    },
    "bili": {
        "name": "B站",
        "short": "bili",
        "aliases": ("bili", "bilibili", "b站", "哔哩哔哩"),
        "endpoint": "https://redfox.hk/story/api/parseWork//queryBiliAiMsgs/batch",
        "source": "B站AI信息源-ClawHub",
        "kw_mode": "batch",
        "paging": False,
        "page_size": 200,
        "max_pages": 1,
        "primary_kw": True,
        "time_style": "dt_2400",
        "update_hour": 15,
        "rank_field": "likeCount",
        "metrics": (
            ("shareCount", "分享", "&#x1f517;", False),
            ("likeCount", "点赞", "&#x1f44d;", False),
            ("commentCount", "评论", "&#x1f4ac;", False),
        ),
        "primary": {"field": "likeCount", "avg_label": "平均点赞", "total_label": "总点赞"},
        "accent": "#FB7299",
        "accent_light": "#FB93B5",
        "link": "https://www.bilibili.com/video/{photoId}",
        "referer": "https://www.bilibili.com/",
        "cover_fix": None,
        "unit": "条",
        "default_keywords": ("AI",),
        "notice": "B站数据每日 15:00 更新前一天内容。",
    },
    "sph": {
        "name": "视频号",
        "short": "sph",
        "aliases": ("sph", "channels", "视频号", "微信视频号"),
        "endpoint": "https://redfox.hk/story/api/parseWork/querySphAiMsgs",
        "source": "AI视频号信息源-ClawHub",
        "kw_mode": "single",
        "paging": False,
        "page_size": 200,
        "max_pages": 1,
        "primary_kw": False,
        "time_style": "date_excl",
        "update_hour": 16,
        "rank_field": "engagement",
        "metrics": (
            ("likeCount", "点赞", "&#x1f44d;", False),
            ("shareCount", "分享", "&#x1f501;", False),
            ("commentCount", "评论", "&#x1f4ac;", False),
        ),
        "primary": {"field": "engagement", "avg_label": "平均互动", "total_label": "总互动"},
        "accent": "#FA9D3B",
        "accent_light": "#FBB96C",
        "link": None,
        "referer": "https://channels.weixin.qq.com/",
        "cover_fix": None,
        "unit": "篇",
        "default_keywords": ("AI",),
        "notice": "视频号作品不支持站外跳转，标题为纯文本。",
    },
    "xhs": {
        "name": "小红书",
        "short": "xhs",
        "aliases": ("xhs", "xiaohongshu", "rednote", "小红书"),
        "endpoint": "https://redfox.hk/story/api/parseWork/queryXhsAiMsgs",
        "source": "AI小红书信息源-ClawHub",
        "kw_mode": "single",
        "paging": False,
        "page_size": 50,
        "max_pages": 1,
        "primary_kw": False,
        "time_style": "date_excl",
        "update_hour": 16,
        "rank_field": "engagement",
        "metrics": (
            ("likeCount", "点赞", "&#x1f44d;", False),
            ("shareCount", "分享", "&#x1f501;", False),
            ("commentCount", "评论", "&#x1f4ac;", False),
        ),
        "primary": {"field": "engagement", "avg_label": "平均互动", "total_label": "总互动"},
        "accent": "#FF2442",
        "accent_light": "#FF5C74",
        "link": "https://www.xiaohongshu.com/explore/{photoId}",
        "referer": "https://www.xiaohongshu.com/",
        "cover_fix": None,
        "unit": "篇",
        "default_keywords": ("AI",),
        "notice": "小红书数据每日 16:00 更新前一天内容。",
    },
}

PLATFORM_ORDER = ("kuaishou", "gzh", "bili", "sph", "xhs")

ALL_ALIASES = ("all", "全部", "所有", "全平台", "*")


def get_platform(slug):
    return PLATFORMS[slug]


def resolve_platforms(spec):
    """把用户传入的平台串解析成 slug 列表（保持 PLATFORM_ORDER 顺序）"""
    if not spec:
        spec = "all"
    spec = str(spec).strip()
    if spec.lower() in ALL_ALIASES or spec in ALL_ALIASES:
        return list(PLATFORM_ORDER)

    tokens = [t.strip() for t in re.split(r"[,，、+/|]+", spec) if t.strip()]
    found = set()
    unknown = []
    for token in tokens:
        low = token.lower()
        if low in ALL_ALIASES:
            return list(PLATFORM_ORDER)
        matched = None
        for slug in PLATFORM_ORDER:
            cfg = PLATFORMS[slug]
            if low == slug or low == cfg["short"] or low == cfg["name"].lower() \
                    or low in [a.lower() for a in cfg["aliases"]]:
                matched = slug
                break
        if matched:
            found.add(matched)
        else:
            unknown.append(token)

    if unknown:
        valid = "、".join(
            f"{PLATFORMS[s]['name']}({PLATFORMS[s]['short']})" for s in PLATFORM_ORDER
        )
        raise ValueError(f"未知平台: {'、'.join(unknown)}。可选值: all、{valid}")

    return [s for s in PLATFORM_ORDER if s in found]


def spec_slug(slugs):
    """报告文件名用的平台标识"""
    if list(slugs) == list(PLATFORM_ORDER):
        return "all"
    return "+".join(PLATFORMS[s]["short"] for s in slugs)


# ─── API Key 管理（四级：CLI > 环境变量 > shell 配置 > 配置文件） ─────────────────────
def _read_key_from_shell_configs():
    shell_configs = [
        Path.home() / ".zshrc",
        Path.home() / ".bashrc",
        Path.home() / ".bash_profile",
        Path.home() / ".profile",
    ]
    pattern = re.compile(
        r'^\s*export\s+' + re.escape(ENV_KEY) + r'\s*=\s*["\']?([^"\' \n]+)["\']?',
        re.MULTILINE,
    )
    for cfg in shell_configs:
        if not cfg.exists():
            continue
        try:
            content = cfg.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        m = pattern.search(content)
        if m:
            return m.group(1).strip()
    return None


def get_api_key(cli_key=None):
    """CLI 参数 > 环境变量 > shell 配置文件 > ~/.qoder/apis/redfox.json"""
    if cli_key:
        return cli_key.strip()

    env_key = (os.environ.get(ENV_KEY) or "").strip()
    if env_key:
        return env_key

    shell_key = _read_key_from_shell_configs()
    if shell_key:
        return shell_key

    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            key = (data.get("api_key") or "").strip()
            if key:
                return key
        except (json.JSONDecodeError, OSError, AttributeError):
            pass
    return ""


def print_api_key_help():
    error(f"未检测到 {ENV_KEY}，请先配置 API Key：")
    if sys.platform == "win32":
        print(f"  Windows PowerShell: [Environment]::SetEnvironmentVariable('{ENV_KEY}', 'ak_你的密钥', 'User')")
    else:
        print(f"  macOS/Linux (zsh):  echo 'export {ENV_KEY}=ak_你的密钥' >> ~/.zshrc && source ~/.zshrc")
        print(f"  macOS/Linux (bash): echo 'export {ENV_KEY}=ak_你的密钥' >> ~/.bashrc && source ~/.bashrc")
    print(f"  命令行参数:         --api-key ak_你的密钥")
    print(f"  配置文件:           echo '{{\"api_key\":\"ak_你的密钥\"}}' > {CONFIG_FILE}")
    print(f"  免费注册获取 Key:   {API_KEY_DOC}")
    print()


# ─── 日期与可用性预检 ──────────────────────────────────────────────────────────────
def latest_available_date(update_hour):
    """每日 update_hour 更新前一天数据；未到更新时间则最新可查为前天"""
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    delta = timedelta(days=1) if now.hour >= update_hour else timedelta(days=2)
    return (midnight - delta).strftime("%Y-%m-%d")


def check_date_available(target_date_str, update_hour):
    """Returns (is_available, latest_date_str)"""
    latest = latest_available_date(update_hour)
    try:
        target = datetime.strptime(target_date_str, "%Y-%m-%d")
        latest_dt = datetime.strptime(latest, "%Y-%m-%d")
    except ValueError:
        return False, latest
    return target <= latest_dt, latest


def global_latest_date(slugs):
    """多平台共同的最新可查日期（取各平台最新可查日期的最小值）"""
    dates = [latest_available_date(PLATFORMS[s]["update_hour"]) for s in slugs]
    return min(dates) if dates else latest_available_date(15)


def print_data_unavailable_notice(query_date, slugs):
    """目标日期无数据时的提示（不调用任何接口，等待用户确认）"""
    out = _LOG_STREAM
    out.write("\n")
    out.write(f"⚠️ **{query_date} 数据尚未更新**\n\n")
    out.write("数据更新规则：\n")
    for s in slugs:
        cfg = PLATFORMS[s]
        out.write(f"  · {cfg['name']}: 每日 {cfg['update_hour']}:00 更新前一天数据，"
                  f"当前最新可查 {latest_available_date(cfg['update_hour'])}\n")
    out.write(f"\n是否需要改查 {global_latest_date(slugs)} 的数据？（或直接使用 --latest）\n\n")
    out.flush()


def parse_date_arg(date_val):
    """解析 YYYY-MM-DD 或 YYYY-MM-DD~YYYY-MM-DD，返回 (start_date, end_date, display_date)"""
    date_val = (date_val or "").strip()
    if "~" in date_val:
        start_date, end_date = [p.strip() for p in date_val.split("~", 1)]
        display_date = f"{start_date}~{end_date}"
    else:
        start_date = end_date = date_val
        display_date = date_val
    datetime.strptime(start_date, "%Y-%m-%d")
    datetime.strptime(end_date, "%Y-%m-%d")
    return start_date, end_date, display_date


def build_time_params(time_style, start_date, end_date):
    """按平台时间格式生成 (startTime, endTime)，不支持时间过滤的平台返回 (None, None)"""
    if time_style == "dt_2359":
        return f"{start_date} 00:00:00", f"{end_date} 23:59:59"
    if time_style == "dt_2400":
        return f"{start_date} 00:00:00", f"{end_date} 24:00:00"
    if time_style == "date_excl":
        next_day = (datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
        return start_date, next_day
    return None, None


# ─── 数据获取 ──────────────────────────────────────────────────────────────────────
def make_session(api_key):
    require_requests()
    session = requests.Session()
    session.verify = True
    session.headers.update({
        "Content-Type": "application/json",
        "X-API-KEY": api_key,
    })
    return session


def post_api(session, url, payload, label=""):
    """统一请求 + 错误处理。成功返回 list，失败返回 None"""
    try:
        resp = session.post(url, json=payload, timeout=30)
        result = resp.json()
    except Exception as e:
        warn(f"{label}请求失败: {e}")
        return None

    code = result.get("code")
    if code == 3108:
        warn(f"{label}限频，等待 5s...")
        time.sleep(5)
        try:
            resp = session.post(url, json=payload, timeout=30)
            result = resp.json()
            code = result.get("code")
        except Exception as e:
            warn(f"{label}重试失败: {e}")
            return None

    if code not in (200, 2000):
        if code in (3106, 3107):
            error(f"{label}API Key 错误 (code {code}): {result.get('msg', '')}")
        else:
            warn(f"{label}接口返回异常 (code {code}): {result.get('msg', '')}")
        return None

    data = result.get("data") or {}
    return data.get("list") or []


def _dedup_key(article):
    pid = article.get("photoId")
    if pid:
        return str(pid)
    url = article.get("url")
    if url:
        return str(url)
    title = article.get("title")
    return f"t:{title}:{article.get('userName')}" if title else ""


def fetch_platform(session, slug, keywords, target_count, start_time=None, end_time=None):
    """按平台配置抓取数据，去重后返回原始作品列表"""
    cfg = PLATFORMS[slug]
    label = f"[{cfg['name']}] "
    articles = []
    seen = set()

    def _collect(batch):
        new = 0
        for a in batch:
            key = _dedup_key(a)
            if not key or key in seen:
                continue
            seen.add(key)
            articles.append(a)
            new += 1
        return new

    def _progress(page, new):
        progress(f"  {CYAN()}[→]{RESET()} {cfg['name']} 第{page}页: "
                 f"新增{new}条, 累计{len(articles)}条        ")

    if not keywords:
        keywords = list(cfg["default_keywords"])

    if cfg["kw_mode"] == "batch":
        max_pages = cfg["max_pages"] if cfg["paging"] else 1
        for page in range(1, max_pages + 1):
            payload = {
                "keywords": keywords,
                "pageNum": page,
                "pageSize": cfg["page_size"],
                "source": cfg["source"],
            }
            if cfg.get("primary_kw"):
                payload["keyword"] = keywords[0]
            if start_time:
                payload["startTime"] = start_time
            if end_time:
                payload["endTime"] = end_time

            batch = post_api(session, cfg["endpoint"], payload, label)
            if batch is None:
                break
            if not batch:
                if page == 1:
                    log_newline()
                    warn(f"{cfg['name']}：关键词 {keywords} 暂无内容（当前仅搜索 AI 相关内容，"
                         f"更多内容请访问 {MORE_DATA_DOC}）")
                break

            new = _collect(batch)
            _progress(page, new)

            if not cfg["paging"]:
                break
            if new == 0 or len(batch) < cfg["page_size"]:
                break
            if len(articles) >= target_count:
                break
            time.sleep(0.3)
    else:
        for i, kw in enumerate(keywords):
            if len(articles) >= target_count:
                break
            max_pages = cfg["max_pages"] if cfg["paging"] else 1
            if cfg["paging"] and i > 0:
                max_pages = min(max_pages, 2)

            for page in range(1, max_pages + 1):
                payload = {
                    "keyword": kw,
                    "pageNum": page,
                    "pageSize": cfg["page_size"],
                    "source": cfg["source"],
                }
                if start_time:
                    payload["startTime"] = start_time
                if end_time:
                    payload["endTime"] = end_time

                batch = post_api(session, cfg["endpoint"], payload, label)
                if batch is None:
                    break
                if not batch:
                    if page == 1 and i == 0:
                        log_newline()
                        warn(f"{cfg['name']}：关键词 \"{kw}\" 暂无内容（当前仅搜索 AI 相关内容，"
                             f"更多内容请访问 {MORE_DATA_DOC}）")
                    break

                new = _collect(batch)
                _progress(page, new)

                if not cfg["paging"]:
                    break
                if new == 0 or len(batch) < cfg["page_size"]:
                    break
                if len(articles) >= target_count:
                    break
                time.sleep(0.3)

            if cfg["paging"] and len(articles) >= target_count * 0.75:
                break

    if articles:
        log_newline()
    return articles


# ─── 归一化 ────────────────────────────────────────────────────────────────────────
def engagement_of(article):
    return ((article.get("likeCount") or 0)
            + (article.get("shareCount") or 0)
            + (article.get("commentCount") or 0))


def rank_value(article, rank_field):
    if rank_field == "engagement":
        return engagement_of(article)
    return article.get(rank_field) or 0


def normalize_articles(slug, articles):
    """补齐详情链接、修复封面格式、兜底空值"""
    cfg = PLATFORMS[slug]
    out = []
    for raw in articles:
        a = dict(raw)
        pid = a.get("photoId") or ""

        url = a.get("url") or ""
        if (not url or url == "#") and cfg.get("link") and pid:
            url = cfg["link"].format(photoId=pid)
        a["url"] = url if url and url != "#" else ""

        cover = a.get("coverUrl") or ""
        if cover and cfg.get("cover_fix") == "kuaishou":
            cover = re.sub(r'\.(heif|heic|kvif|kpg)(?=[?#]|$)', '.jpg', cover, flags=re.IGNORECASE)
            cover = re.sub(r'/(heif|heic)/', '/jpg/', cover, flags=re.IGNORECASE)
        a["coverUrl"] = cover

        a["title"] = (a.get("title") or "").strip() or "无标题"
        a["userName"] = (a.get("userName") or "").strip() or "未知"
        a["_platform"] = slug
        out.append(a)
    return out


# ─── 自动聚类（六步，全平台共用） ────────────────────────────────────────────────────
STOP_WORDS = set("的了是在和与及或但对于从到被将把让给用有这那个也都还又不没"
                 "就才能会要可以怎么什么为什么怎样如何哪些多少一个一些这些那些"
                 "已经正在可能应该必须需要通过进行使用利用根据关于对于由于因为所以"
                 "虽然但是然而因此所以如果那么只要只有无论不管即使不仅而且")

GENERIC_TAGS = {"#AI", "#人工智能", "#ai", "AI", "ai", "人工智能", "#科技", "#技术",
                "#人工智能应用", "#智能", "科技", "技术", "AI工具"}

SPLIT_BLACKLIST = ("人工智能", "智能", "模型", "技术", "应用")


def extract_keywords(title):
    """从标题中提取 2-4 字中文关键词片段"""
    if not title:
        return []
    cleaned = re.sub(r'[^\u4e00-\u9fff\w]', ' ', title)
    segments = re.findall(r'[\u4e00-\u9fff]{2,4}', cleaned)
    return [s for s in segments if not all(ch in STOP_WORDS for ch in s)][:5]


def get_article_tags(article):
    """提取有效标签（type 优先、topic 补充），剔除泛标签"""
    tags = []
    atype = (article.get("type") or "").strip()
    if atype:
        for t in re.split(r'[,，]+', atype):
            t = t.strip()
            if t and t not in GENERIC_TAGS and t not in tags:
                tags.append(t)
    topic = (article.get("topic") or "").strip()
    if topic:
        for t in re.split(r'[,，\s]+', topic):
            t = t.strip()
            if t and t not in GENERIC_TAGS and t not in tags:
                tags.append(t)
    return tags


def cluster_articles(articles, rank_field="likeCount", top_n=5):
    """基于 type + topic 标签自动聚类，返回按数量降序的分类列表"""
    total = len(articles)
    if total == 0:
        return []

    min_group = 3 if total >= 60 else 2

    # 第一步：按首个有效标签分组
    topic_groups = defaultdict(list)
    for article in articles:
        tags = get_article_tags(article)
        topic_groups[tags[0] if tags else "其他"].append(article)

    # 第二步：大组按第二标签二次拆分
    split_threshold = max(total * 0.2, 25)
    for topic in [t for t, a in topic_groups.items() if len(a) > split_threshold and t != "其他"]:
        arts = topic_groups.pop(topic)
        for article in arts:
            tags = get_article_tags(article)
            topic_groups[tags[1] if len(tags) >= 2 else topic].append(article)

    # 第三步：合并小组，先尝试塞进已有大组
    final_groups = {}
    small_articles = []
    for topic, arts in topic_groups.items():
        if len(arts) >= min_group:
            final_groups[topic] = arts
        else:
            small_articles.extend(arts)

    still_orphan = []
    for article in small_articles:
        placed = False
        for tag in get_article_tags(article):
            if tag in final_groups:
                final_groups[tag].append(article)
                placed = True
                break
        if not placed:
            still_orphan.append(article)
    if still_orphan:
        final_groups.setdefault("其他", []).extend(still_orphan)

    # 第四步：过大组按标题高频词拆分（最多 3 轮）
    max_group_size = max(total * 0.3, 40)
    for _ in range(3):
        oversized = [(t, a) for t, a in final_groups.items() if len(a) > max_group_size]
        if not oversized:
            break
        for topic, arts in oversized:
            kw_counter = Counter()
            article_kw_map = {}
            for article in arts:
                kws = extract_keywords(article.get("title", ""))
                article_kw_map[id(article)] = kws
                kw_counter.update(kws)
            common_kws = [kw for kw, cnt in kw_counter.most_common(5)
                          if cnt >= 5 and kw not in topic
                          and f"#{kw}" not in GENERIC_TAGS
                          and f"#{kw}" not in final_groups
                          and kw not in SPLIT_BLACKLIST]
            if not common_kws:
                continue
            split_kw = common_kws[0]
            new_group, remaining = [], []
            for article in arts:
                (new_group if split_kw in article_kw_map.get(id(article), []) else remaining).append(article)
            if len(new_group) >= 5:
                final_groups[f"#{split_kw}"] = new_group
                final_groups[topic] = remaining

    # 第五步：分类数不足 5 个时继续拆最大组
    # 只允许拆出 final_groups 中尚不存在的标签：否则两个互为二级标签的组
    # （如 "教程"→"工具"→"教程"）会来回搬运文章，分类数永远不增长而死循环。
    for _ in range(5):
        if len(final_groups) >= 5:
            break
        largest_topic = max(final_groups, key=lambda k: len(final_groups[k]))
        largest_arts = final_groups[largest_topic]
        if len(largest_arts) < 6:
            break
        sub_groups = defaultdict(list)
        remain = []
        for article in largest_arts:
            second_tag = next((t for t in get_article_tags(article) if t != largest_topic), None)
            (sub_groups[second_tag] if second_tag else remain).append(article)
        candidates = {k: v for k, v in sub_groups.items()
                      if k not in final_groups and len(v) >= min_group}
        if not candidates:
            break
        best_sub = max(candidates, key=lambda k: len(candidates[k]))
        final_groups[best_sub] = candidates[best_sub]
        new_arts = list(remain)
        for k, v in sub_groups.items():
            if k != best_sub:
                new_arts.extend(v)
        if new_arts:
            final_groups[largest_topic] = new_arts
        else:
            final_groups.pop(largest_topic, None)

    final_groups = {k: v for k, v in final_groups.items() if v}

    # 第六步：输出，按数量降序，组内按平台主指标降序
    clusters = []
    for category, arts in sorted(final_groups.items(), key=lambda x: -len(x[1])):
        if not arts:
            continue
        sorted_arts = sorted(arts, key=lambda a: rank_value(a, rank_field), reverse=True)
        clusters.append({
            "category": category,
            "count": len(sorted_arts),
            "articles": sorted_arts[:top_n],
        })
    return clusters


# ─── 统计与格式化 ──────────────────────────────────────────────────────────────────
def format_number(n):
    """1234 -> 1.2k, 12345 -> 1.2w"""
    if n is None:
        return "0"
    n = int(n)
    if n >= 10000:
        return f"{n / 10000:.1f}w"
    if n >= 1000:
        return f"{n / 1000:.1f}k"
    return str(n)


def compute_stats(articles, slug):
    """平台级统计：总数、主指标均值/总和、头部作者"""
    cfg = PLATFORMS[slug]
    field = cfg["primary"]["field"]
    total = len(articles)
    if total == 0:
        return {
            "total": 0,
            "avg_primary": 0,
            "total_primary": 0,
            "top_author": "-",
            "total_engagement": 0,
            "avg_label": cfg["primary"]["avg_label"],
            "total_label": cfg["primary"]["total_label"],
        }

    values = [rank_value(a, field) for a in articles]
    values = [v for v in values if v]
    author_counter = Counter(a.get("userName") or "未知" for a in articles)

    return {
        "total": total,
        "avg_primary": (sum(values) // len(values)) if values else 0,
        "total_primary": sum(rank_value(a, field) for a in articles),
        "top_author": author_counter.most_common(1)[0][0] if author_counter else "-",
        "total_engagement": sum(engagement_of(a) for a in articles),
        "avg_label": cfg["primary"]["avg_label"],
        "total_label": cfg["primary"]["total_label"],
    }


def esc(text):
    """HTML 转义，防止标题中的引号/尖括号破坏结构"""
    if text is None:
        return ""
    return (str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;"))


def display_width(text):
    """终端显示宽度：全角/宽字符按 2 列计，其余按 1 列"""
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1
               for c in str(text))


def pad(text, width, align="<"):
    """按显示宽度补齐到 width，避免中英文混排导致表格错位"""
    text = str(text)
    gap = width - display_width(text)
    if gap <= 0:
        return text
    return " " * gap + text if align == ">" else text + " " * gap


def fit(text, width):
    """按显示宽度截断到 width，溢出部分以 … 结尾"""
    text = str(text)
    if display_width(text) <= width:
        return text
    kept, used = [], 0
    for ch in text:
        cw = 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
        if used + cw > width - 1:
            break
        kept.append(ch)
        used += cw
    return "".join(kept) + "…"


# ─── 终端输出 ──────────────────────────────────────────────────────────────────────
def print_platform_table(slug, clusters):
    cfg = PLATFORMS[slug]
    metric_labels = [m[1] for m in cfg["metrics"]]
    out = _LOG_STREAM

    w_no, w_title, w_author, w_metric = 6, 46, 16, 10
    rule = "─" * (w_no + w_title + w_author + w_metric * len(metric_labels))
    header = (pad("序号", w_no) + pad("标题", w_title) + pad("作者", w_author)
              + "".join(pad(lbl, w_metric, ">") for lbl in metric_labels))

    out.write("\n")
    out.write(f"{BOLD()}{'=' * display_width(rule)}{RESET()}\n")
    out.write(f"{BOLD()}  {cfg['name']}AI信息源 · 分类内容一览{RESET()}\n")
    out.write(f"{BOLD()}{'=' * display_width(rule)}{RESET()}\n\n")

    for cluster in clusters:
        out.write(f"  {CYAN()}{BOLD()}【{cluster['category']}】{RESET()} "
                  f"共 {len(cluster['articles'])} {cfg['unit']}展示 / "
                  f"{cluster['count']} {cfg['unit']}总计\n")
        out.write(f"  {YELLOW()}{rule}{RESET()}\n")
        out.write(f"  {YELLOW()}{header}{RESET()}\n")
        out.write(f"  {YELLOW()}{rule}{RESET()}\n")

        for j, article in enumerate(cluster["articles"], 1):
            cells = []
            for field, _lbl, _icon, optional in cfg["metrics"]:
                raw = engagement_of(article) if field == "engagement" else article.get(field)
                cells.append("-" if (optional and not raw) else format_number(raw))

            out.write("  " + pad(j, w_no)
                      + pad(fit(article.get("title") or "无标题", w_title - 2), w_title)
                      + pad(fit(article.get("userName") or "-", w_author - 2), w_author)
                      + "".join(pad(c, w_metric, ">") for c in cells) + "\n")
        out.write("\n")
    out.flush()


# ─── AI 情报调查 ───────────────────────────────────────────────────────────────────
# 调查报告的「来源」标注是固定文案而非平台标识；写成常量可避免 skill-source-duplicator
# 把它们当作 API source 值追加平台后缀。
FINDING_ORIGIN_API = "平台接口数据"
FINDING_ORIGIN_TITLE = "标题关键词分析"
FINDING_ORIGIN_INTERACTION = "互动数据分析"
FINDING_ORIGIN_AUTHOR = "作者统计"

INVESTIGATION_ENGINES = {
    "Baidu": {"url": "https://www.baidu.com/s?wd={keyword}", "region": "cn", "strength": "中文生态覆盖最广"},
    "WeChat": {"url": "https://wx.sogou.com/weixin?type=2&query={keyword}", "region": "cn", "strength": "微信公众号文章"},
    "Toutiao": {"url": "https://so.toutiao.com/search?keyword={keyword}", "region": "cn", "strength": "自媒体/热点追踪"},
    "Google": {"url": "https://www.google.com/search?q={keyword}", "region": "global", "strength": "全球索引最全+高级操作符"},
    "DuckDuckGo": {"url": "https://duckduckgo.com/html/?q={keyword}", "region": "global", "strength": "无追踪+Bangs直达"},
    "Brave": {"url": "https://search.brave.com/search?q={keyword}", "region": "global", "strength": "独立索引+无偏见"},
    "Sogou": {"url": "https://sogou.com/web?query={keyword}", "region": "cn", "strength": "微信+知乎内容"},
    "Bing INT": {"url": "https://cn.bing.com/search?q={keyword}&ensearch=1", "region": "cn", "strength": "中文界面+国际结果"},
}

SCENARIO_ENGINES = {
    "产品竞品分析": ["Baidu", "Google", "WeChat", "DuckDuckGo"],
    "热点事件追踪": ["Baidu", "Toutiao", "Google", "WeChat"],
    "人物背景验证": ["Baidu", "Google", "DuckDuckGo"],
    "用户口碑收集": ["WeChat", "Toutiao", "DuckDuckGo", "Brave"],
    "技术趋势调查": ["DuckDuckGo", "Google", "Brave"],
    "市场数据验证": ["Google", "Baidu", "Bing INT"],
}

CREDIBILITY_LEVELS = {
    "A": "官方/政府/权威媒体",
    "B": "行业媒体/专业平台",
    "C": "社交媒体/自媒体",
    "D": "匿名/未验证来源",
}

TOPIC_MODE_MAP = {
    "大模型": ("竞品情报调查", "产品竞品分析"),
    "GPT": ("竞品情报调查", "产品竞品分析"),
    "ChatGPT": ("竞品情报调查", "产品竞品分析"),
    "Agent": ("竞品情报调查", "技术趋势调查"),
    "智能体": ("竞品情报调查", "技术趋势调查"),
    "绘画": ("竞品情报调查", "用户口碑收集"),
    "创作": ("舆情事件调查", "用户口碑收集"),
    "动画": ("竞品情报调查", "用户口碑收集"),
    "教程": ("技术趋势调查", "技术趋势调查"),
    "教学": ("技术趋势调查", "技术趋势调查"),
    "Prompt": ("技术趋势调查", "产品竞品分析"),
    "提示词": ("技术趋势调查", "产品竞品分析"),
    "变现": ("舆情事件调查", "市场数据验证"),
    "副业": ("舆情事件调查", "用户口碑收集"),
}


def _match_mode(topic_name):
    for kw, (mode, scenario) in TOPIC_MODE_MAP.items():
        if kw in topic_name:
            return mode, scenario
    return "舆情事件调查", "热点事件追踪"


def _derive_findings(cluster, rank_field):
    """从平台数据中提取调查发现"""
    findings = []
    arts = cluster["articles"]
    if not arts:
        return findings

    top = arts[0]
    title = (top.get("title") or "无标题")[:40]
    top_rank = rank_value(top, rank_field)
    findings.append({
        "dimension": "头部内容",
        "discovery": f"{title} — 主指标 {format_number(top_rank)}",
        "source": FINDING_ORIGIN_API,
        "credibility": "B",
    })

    title_kw = Counter()
    for a in arts:
        for seg in extract_keywords(a.get("title", "")):
            if len(seg) >= 2:
                title_kw[seg] += 1
    if title_kw:
        top_kws = "、".join(kw for kw, _ in title_kw.most_common(3))
        findings.append({
            "dimension": "用户关注",
            "discovery": f"高频关键词：{top_kws}",
            "source": FINDING_ORIGIN_TITLE,
            "credibility": "C",
        })

    total_likes = sum(a.get("likeCount") or 0 for a in arts)
    total_comments = sum(a.get("commentCount") or 0 for a in arts)
    if total_likes > 0:
        ratio = total_comments / total_likes
        findings.append({
            "dimension": "互动特征",
            "discovery": f"总赞 {format_number(total_likes)}，评论率 {ratio * 100:.1f}%，"
                         + ("讨论活跃" if ratio > 0.15 else "以点赞为主"),
            "source": FINDING_ORIGIN_INTERACTION,
            "credibility": "B",
        })

    author_counter = Counter(a.get("userName") for a in arts if a.get("userName"))
    if author_counter:
        name, cnt = author_counter.most_common(1)[0]
        findings.append({
            "dimension": "核心作者",
            "discovery": f"@{name} 贡献 {cnt} 条作品",
            "source": FINDING_ORIGIN_AUTHOR,
            "credibility": "B",
        })

    return findings


def _derive_conclusions(cluster, findings, rank_field):
    conclusions = []
    topic_name = cluster["category"].lstrip("#")
    arts = cluster["articles"]

    if arts:
        top_likes = arts[0].get("likeCount") or 0
        if top_likes > 50000:
            conclusions.append(("confirmed",
                                f"{topic_name}话题有强流量表现，头部内容点赞 {format_number(top_likes)}+"))

    for f in findings:
        if f["dimension"] == "用户关注" and "高频关键词" in f["discovery"]:
            conclusions.append(("pending",
                                f"用户关注方向需跨平台验证：{f['discovery'].replace('高频关键词：', '')}"))

    if cluster["count"] <= 15:
        conclusions.append(("single", f"{topic_name}话题样本量较少（{cluster['count']}条），趋势待观察"))

    if not conclusions:
        conclusions.append(("confirmed", f"{topic_name}话题内容稳定，无异常信号"))
    return conclusions


def generate_intelligence_briefing(clusters, articles, slug, other_platform_names=()):
    """生成单平台 AI 情报调查报告"""
    if not clusters:
        return None

    cfg = PLATFORMS[slug]
    rank_field = cfg["rank_field"]
    total = len(articles)

    top_topics = []
    for cluster in clusters[:5]:
        top_art = cluster["articles"][0] if cluster["articles"] else None
        top_topics.append({
            "topic": cluster["category"],
            "count": cluster["count"],
            "ratio": round(cluster["count"] / total * 100, 1) if total else 0,
            "top_article": top_art,
            "top_metric": rank_value(top_art, rank_field) if top_art else 0,
            "metric_label": cfg["primary"]["avg_label"].replace("平均", ""),
        })

    emerging_topics = []
    for cluster in clusters:
        if cluster["count"] < max(total * 0.1, 1) and cluster["articles"]:
            avg_engagement = sum(engagement_of(a) for a in cluster["articles"]) / len(cluster["articles"])
            if avg_engagement > 1000:
                emerging_topics.append({
                    "topic": cluster["category"],
                    "count": cluster["count"],
                    "avg_engagement": int(avg_engagement),
                })

    author_counter = Counter()
    author_articles = defaultdict(list)
    for article in articles:
        author = article.get("userName") or "未知"
        author_counter[author] += 1
        author_articles[author].append(article)

    top_authors = []
    for author, count in author_counter.most_common(5):
        arts = author_articles[author]
        top_authors.append({
            "name": author,
            "article_count": count,
            "total_likes": sum(a.get("likeCount") or 0 for a in arts),
            "total_shares": sum(a.get("shareCount") or 0 for a in arts),
        })

    investigation_reports = []
    for cluster in clusters[:3]:
        topic_name = cluster["category"].lstrip("#")
        mode, scenario = _match_mode(topic_name)
        findings = _derive_findings(cluster, rank_field)
        investigation_reports.append({
            "topic": cluster["category"],
            "mode": mode,
            "scenario": scenario,
            "engines": SCENARIO_ENGINES.get(scenario, SCENARIO_ENGINES["热点事件追踪"]),
            "findings": findings,
            "conclusions": _derive_conclusions(cluster, findings, rank_field),
        })

    others = "、".join(other_platform_names) if other_platform_names else "其它平台"
    cross_platform_tips = [
        f"「{t['topic'].lstrip('#')}」— 建议同步核对 {others} 的同话题热度，"
        f"用 Baidu+WeChat+Toutiao 三引擎追踪国内全平台动态"
        for t in top_topics[:3]
    ]

    return {
        "platform": cfg["name"],
        "top_topics": top_topics,
        "emerging_topics": emerging_topics,
        "top_authors": top_authors,
        "investigation_reports": investigation_reports,
        "cross_platform_tips": cross_platform_tips,
    }


def print_intelligence_briefing(briefing):
    if not briefing:
        return

    print(f"\n{BOLD()}{'=' * 78}{RESET()}")
    print(f"{BOLD()}  {briefing['platform']} · AI情报调查 · 深度调查指引{RESET()}")
    print(f"{BOLD()}{'=' * 78}{RESET()}\n")

    if briefing["top_topics"]:
        print(f"  {CYAN()}{BOLD()}【热度TOP话题】{RESET()}")
        for i, topic in enumerate(briefing["top_topics"], 1):
            print(f"    {i}. {topic['topic']} — 占比{topic['ratio']}% · {topic['count']}条 · "
                  f"头部{topic['metric_label']} {format_number(topic['top_metric'])}")
        print()

    if briefing["emerging_topics"]:
        print(f"  {CYAN()}{BOLD()}【新兴起量信号】{RESET()}")
        for topic in briefing["emerging_topics"]:
            print(f"    🔥 {topic['topic']} — 虽仅{topic['count']}条但均互动{topic['avg_engagement']}+，值得深挖")
        print()

    if briefing["top_authors"]:
        print(f"  {CYAN()}{BOLD()}【核心达人】{RESET()}")
        for author in briefing["top_authors"]:
            print(f"    @{author['name']} — {author['article_count']}条作品, "
                  f"总赞{format_number(author['total_likes'])}, 总分享{format_number(author['total_shares'])}")
        print()

    if briefing["investigation_reports"]:
        print(f"  {CYAN()}{BOLD()}【TOP话题调查报告】{RESET()}")
        for report in briefing["investigation_reports"]:
            print(f"    ▸ {report['topic']} — {report['mode']} | {' + '.join(report['engines'])}")
            for f in report.get("findings", []):
                print(f"      [{f['credibility']}级] {f['dimension']}: {f['discovery']}")
            icons = {"confirmed": "✅", "pending": "⚠️", "denied": "❌", "single": "🔍"}
            for ctype, ctext in report.get("conclusions", []):
                print(f"      {icons.get(ctype, '·')} {ctext}")
        print()

    if briefing["cross_platform_tips"]:
        print(f"  {CYAN()}{BOLD()}【跨平台对比建议】{RESET()}")
        for tip in briefing["cross_platform_tips"]:
            print(f"    • {tip}")
    print()


# ─── HTML 渲染 ─────────────────────────────────────────────────────────────────────
def generate_article_items(slug, cluster):
    cfg = PLATFORMS[slug]
    items = ""
    for article in cluster["articles"]:
        title = esc(article.get("title") or "无标题")
        author = esc(article.get("userName") or "")
        cover = article.get("coverUrl") or ""
        url = article.get("url") or ""

        cover_html = ""
        if cover:
            cover_html = (f'<img class="article-cover" src="{esc(cover)}" alt="" loading="lazy" '
                          f'referrerpolicy="no-referrer" '
                          f'onerror="this.style.visibility=&apos;hidden&apos;">')

        title_html = (f'<a href="{esc(url)}" target="_blank" rel="noopener" class="article-title" '
                      f'title="{title}">{title}</a>'
                      if url else
                      f'<span class="article-title" title="{title}">{title}</span>')

        metrics_html = ""
        for field, label, icon, optional in cfg["metrics"]:
            raw = engagement_of(article) if field == "engagement" else article.get(field)
            if optional and not raw:
                continue
            metrics_html += (f'<span class="metric" title="{label}">{icon} '
                             f'{format_number(raw)}</span>')

        items += f'''
                <div class="article-item">
                    {cover_html}
                    <div class="article-info">
                        {title_html}
                        <div class="article-meta">
                            <span class="author">{author}</span>
                            <span class="metrics">{metrics_html}</span>
                        </div>
                    </div>
                </div>'''
    return items


def generate_category_cards(slug, clusters):
    cfg = PLATFORMS[slug]
    cards = ""
    for i, cluster in enumerate(clusters, 1):
        cards += f'''
        <div class="category-card reveal">
            <div class="card-header">
                <span class="card-number">{i:02d}</span>
                <h3 class="card-category">{esc(cluster["category"])}</h3>
                <span class="card-count">{cluster["count"]} {cfg["unit"]}</span>
            </div>
            <div class="card-body">{generate_article_items(slug, cluster)}
            </div>
        </div>'''
    return cards


def generate_intelligence_html(briefing):
    """情报调查板块 HTML（多源交叉验证样式）"""
    if not briefing:
        return ""

    topics_html = ""
    for i, topic in enumerate(briefing["top_topics"], 1):
        top_art = topic.get("top_article")
        top_title = esc((top_art.get("title") or "-")[:50]) if top_art else "-"
        topics_html += f'''
                <div class="intel-rank-item">
                    <span class="intel-rank-num">{i}</span>
                    <div class="intel-rank-info">
                        <span class="intel-rank-topic">{esc(topic["topic"])}</span>
                        <span class="intel-rank-detail">占比 {topic["ratio"]}% · {topic["count"]}条 · 头部: {top_title}</span>
                    </div>
                    <span class="intel-rank-metric">{format_number(topic["top_metric"])} {esc(topic["metric_label"])}</span>
                </div>'''

    emerging_html = ""
    for topic in briefing.get("emerging_topics", []):
        emerging_html += f'''
                <div class="intel-emerging-item">
                    <span class="intel-emerging-badge">起量信号</span>
                    <span class="intel-emerging-topic">{esc(topic["topic"])}</span>
                    <span class="intel-emerging-detail">{topic["count"]}条 · 均互动{format_number(topic["avg_engagement"])}+</span>
                </div>'''
    emerging_section = f'''
            <div class="intel-subsection">
                <h4 class="intel-subtitle">新兴起量信号</h4>
                <div class="intel-emerging-list">{emerging_html}
                </div>
            </div>''' if emerging_html else ""

    authors_html = ""
    for author in briefing.get("top_authors", []):
        authors_html += f'''
                <div class="intel-author-item">
                    <span class="intel-author-name">@{esc(author["name"])}</span>
                    <span class="intel-author-stats">{author["article_count"]}条 · 总赞{format_number(author["total_likes"])} · 总分享{format_number(author["total_shares"])}</span>
                </div>'''
    authors_section = f'''
            <div class="intel-subsection">
                <h4 class="intel-subtitle">核心达人</h4>
                <div class="intel-author-list">{authors_html}
                </div>
            </div>''' if authors_html else ""

    reports_html = ""
    icons = {"confirmed": "✅", "pending": "⚠️", "denied": "❌", "single": "🔍"}
    css_class = {"confirmed": "intel-conclusion-confirmed", "pending": "intel-conclusion-pending",
                 "denied": "intel-conclusion-denied", "single": "intel-conclusion-single"}
    for report in briefing.get("investigation_reports", []):
        findings_rows = ""
        for f in report.get("findings", []):
            cred = f["credibility"]
            findings_rows += f'''
                        <tr>
                            <td>{esc(f["dimension"])}</td>
                            <td>{esc(f["discovery"])}</td>
                            <td>{esc(f["source"])}</td>
                            <td><span class="intel-cred-badge intel-cred-{cred.lower()}">{cred}级</span></td>
                        </tr>'''

        conclusion_items = "".join(
            f'<li class="intel-conclusion-item {css_class.get(ctype, "")}">'
            f'{icons.get(ctype, "·")} {esc(ctext)}</li>'
            for ctype, ctext in report.get("conclusions", [])
        )

        reports_html += f'''
            <div class="intel-report-card reveal">
                <div class="intel-report-head">
                    <span class="intel-report-topic">{esc(report["topic"])}</span>
                    <span class="intel-report-mode">{esc(report["mode"])}</span>
                    <span class="intel-report-engines">{" + ".join(report["engines"])}</span>
                </div>
                <div class="intel-report-body">
                    <div class="intel-report-scenario">📋 调查场景: {esc(report.get("scenario", ""))}</div>
                    <table class="intel-findings-table">
                        <thead><tr><th>维度</th><th>发现</th><th>来源</th><th>可信度</th></tr></thead>
                        <tbody>{findings_rows}
                        </tbody>
                    </table>
                    <div class="intel-conclusion-title">关键结论</div>
                    <ul class="intel-conclusion-list">{conclusion_items}
                    </ul>
                </div>
            </div>'''

    cross_html = "".join(
        f'<div class="intel-cross-tip">{esc(tip)}</div>'
        for tip in briefing.get("cross_platform_tips", [])
    )
    cross_section = f'''
            <div class="intel-subsection">
                <h4 class="intel-subtitle">跨平台对比建议</h4>
                <div class="intel-cross-list">{cross_html}
                </div>
            </div>''' if cross_html else ""

    cred_ref_items = "".join(
        f'''
            <div class="intel-cred-ref-item">
                <span class="intel-cred-badge intel-cred-{level.lower()}">{level}级</span>
                <span class="intel-cred-ref-label">{desc}</span>
            </div>'''
        for level, desc in CREDIBILITY_LEVELS.items()
    )

    return f'''
        <div class="intelligence-section reveal">
            <div class="intel-header">
                <h2 class="intel-title">AI情报调查报告 · {esc(briefing["platform"])}</h2>
                <span class="intel-subtitle-badge">基于智能情报调查员 · 多源交叉验证</span>
            </div>
            <div class="intel-body">
            <div class="intel-subsection">
                <h4 class="intel-subtitle">热度TOP话题</h4>
                <div class="intel-rank-list">{topics_html}
                </div>
            </div>
{emerging_section}
{authors_section}
            <div class="intel-subsection">
                <h4 class="intel-subtitle">TOP话题调查报告</h4>
                {reports_html}
            </div>
{cross_section}
            <div class="intel-subsection">
                <h4 class="intel-subtitle">可信度标注规范</h4>
                <div class="intel-cred-ref">{cred_ref_items}
                </div>
            </div>
            </div>
        </div>'''


def generate_platform_section(result):
    """单个平台的完整分区（含统计条、分类卡片、情报板块）"""
    slug = result["slug"]
    cfg = PLATFORMS[slug]
    clusters = result["clusters"]
    stats = result["stats"]
    briefing = result.get("briefing")

    notice_html = ""
    if cfg.get("notice"):
        notice_html = f'<div class="platform-notice">ℹ️ {esc(cfg["notice"])}</div>'

    intel_html = generate_intelligence_html(briefing) if briefing else ""

    return f'''
    <section class="platform-section" data-platform="{slug}"
             style="--accent:{cfg["accent"]};--accent-light:{cfg["accent_light"]};
                    --accent-glow:{cfg["accent"]}26;--accent-border:{cfg["accent"]}4D;">
        <div class="platform-head">
            <h2 class="platform-name">{esc(cfg["name"])}AI信息源</h2>
            <span class="platform-badge">{stats["total"]} {cfg["unit"]} · {len(clusters)} 个分类</span>
        </div>
        {notice_html}
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-value">{len(clusters)}</div>
                <div class="stat-label">分类</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{stats["total"]}</div>
                <div class="stat-label">{cfg["unit"]}数</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{format_number(stats["avg_primary"])}</div>
                <div class="stat-label">{esc(stats["avg_label"])}</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{format_number(stats["total_primary"])}</div>
                <div class="stat-label">{esc(stats["total_label"])}</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{esc(stats["top_author"])}</div>
                <div class="stat-label">头部作者</div>
            </div>
        </div>
        <div class="cards-grid">{generate_category_cards(slug, clusters)}
        </div>
        {intel_html}
    </section>'''


def generate_overview_html(results):
    """跨平台总览卡片"""
    cards = ""
    for result in results:
        slug = result["slug"]
        cfg = PLATFORMS[slug]
        stats = result["stats"]
        clusters = result["clusters"]
        top_cat = clusters[0]["category"] if clusters else "-"
        top_art = clusters[0]["articles"][0] if clusters and clusters[0]["articles"] else None
        top_title = esc((top_art.get("title") or "-")[:32]) if top_art else "-"

        cards += f'''
        <a class="overview-card reveal" href="#sec-{slug}" data-goto="{slug}">
            <div class="overview-card-head">
                <span class="overview-dot"></span>
                <span class="overview-name">{esc(cfg["name"])}</span>
                <span class="overview-count">{stats["total"]} {cfg["unit"]}</span>
            </div>
            <div class="overview-metrics">
                <span>{len(clusters)} 个分类</span>
                <span>{esc(stats["total_label"])} {format_number(stats["total_primary"])}</span>
            </div>
            <div class="overview-top">TOP分类: {esc(top_cat)}</div>
            <div class="overview-title">头部: {top_title}</div>
        </a>'''
    return f'''
    <div class="overview-section">
        <h2 class="section-title">跨平台总览</h2>
        <div class="overview-grid">{cards}
        </div>
    </div>'''


def generate_cross_platform_html(results):
    """跨平台话题对比表"""
    if len(results) < 2:
        return ""

    topic_map = defaultdict(dict)
    for result in results:
        cfg = PLATFORMS[result["slug"]]
        for cluster in result["clusters"][:5]:
            key = cluster["category"].lstrip("#").strip()
            if key and key != "其他":
                topic_map[key][cfg["name"]] = cluster["count"]

    if not topic_map:
        return ""

    platform_names = [PLATFORMS[r["slug"]]["name"] for r in results]
    rows = sorted(topic_map.items(), key=lambda kv: -sum(kv[1].values()))[:12]

    head = "".join(f"<th>{esc(n)}</th>" for n in platform_names)
    body = ""
    for topic, per_platform in rows:
        cells = "".join(
            f'<td class="{"hit" if per_platform.get(n) else "miss"}">'
            f'{per_platform.get(n, "—")}</td>'
            for n in platform_names
        )
        body += f"<tr><td class=\"topic-cell\">{esc(topic)}</td>{cells}" \
                f"<td>{len(per_platform)}/{len(platform_names)}</td></tr>"

    return f'''
    <div class="cross-section reveal">
        <h2 class="section-title">跨平台话题对比</h2>
        <p class="section-desc">同一话题在不同平台的内容量（条/篇），覆盖平台数越多说明该话题越是全域热点。</p>
        <div class="cross-table-wrap">
        <table class="cross-table">
            <thead><tr><th>话题</th>{head}<th>覆盖</th></tr></thead>
            <tbody>{body}</tbody>
        </table>
        </div>
    </div>'''


def generate_report(results, display_date, nav_date, platform_slugs, intel_enabled=True):
    """生成统一多平台 HTML 报告"""
    template_path = Path(__file__).resolve().parent.parent / "assets" / "report_template.html"
    if template_path.exists():
        template = template_path.read_text(encoding="utf-8")
    else:
        warn("模板文件未找到，使用内置模板")
        template = get_fallback_template()

    try:
        dt = datetime.strptime(nav_date, "%Y-%m-%d")
        weekdays = ["一", "二", "三", "四", "五", "六", "日"]
        date_cn = f"{dt.year}年{dt.month}月{dt.day}日 星期{weekdays[dt.weekday()]}"
    except ValueError:
        date_cn = display_date

    total_count = sum(r["stats"]["total"] for r in results)
    category_count = sum(len(r["clusters"]) for r in results)
    total_engagement = sum(r["stats"]["total_engagement"] for r in results)

    tabs = '<button class="platform-tab active" data-filter="all">全部</button>'
    for r in results:
        cfg = PLATFORMS[r["slug"]]
        tabs += (f'<button class="platform-tab" data-filter="{r["slug"]}" '
                 f'style="--tab-accent:{cfg["accent"]}">{esc(cfg["name"])}</button>')

    sections = "".join(
        f'<div id="sec-{r["slug"]}">{generate_platform_section(r)}</div>'
        for r in results
    )

    html = template
    replacements = {
        "{{DATE}}": nav_date,
        "{{DATE_CN}}": date_cn,
        "{{DISPLAY_DATE}}": display_date,
        "{{PLATFORM_COUNT}}": str(len(results)),
        "{{TOTAL_COUNT}}": str(total_count),
        "{{CATEGORY_COUNT}}": str(category_count),
        "{{TOTAL_ENGAGEMENT}}": format_number(total_engagement),
        "{{PLATFORM_TABS}}": tabs,
        "{{OVERVIEW_SECTION}}": generate_overview_html(results),
        "{{CROSS_SECTION}}": generate_cross_platform_html(results),
        "{{PLATFORM_SECTIONS}}": sections,
        "{{REPORT_PREFIX}}": f"{REPORT_PREFIX}_{spec_slug(platform_slugs)}",
        "{{TIMESTAMP}}": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "{{SKILL_NAME}}": SKILL_NAME,
    }
    for key, value in replacements.items():
        html = html.replace(key, value)
    return html


def get_fallback_template():
    """模板文件缺失时的最小可用模板"""
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{SKILL_NAME}} - {{DISPLAY_DATE}}</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, sans-serif; background: #0f0f0f; color: #f0ece6; padding: 2rem; }
.header { text-align: center; padding: 2rem 0; }
.header h1 { font-size: 2rem; color: #FB7299; }
.header p { color: #9a9590; margin-top: 0.5rem; }
.stats { display: flex; justify-content: center; gap: 2rem; padding: 1rem; margin: 1rem 0; }
.stat-item { text-align: center; }
.stat-value { font-size: 1.5rem; font-weight: bold; color: #FB7299; }
.stat-label { font-size: 0.8rem; color: #9a9590; }
.cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 1.5rem; max-width: 1200px; margin: 2rem auto; }
.category-card { background: #1e1e1e; border-radius: 12px; overflow: hidden; }
.card-header { display: flex; align-items: center; gap: 0.8rem; padding: 1rem 1.2rem; background: #FB7299; }
.card-category { flex: 1; font-size: 1.1rem; font-weight: 700; color: #fff; }
.card-count { font-size: 0.8rem; color: #fff; background: rgba(0,0,0,0.2); padding: 0.2rem 0.6rem; border-radius: 10px; }
.card-body { padding: 0.8rem 1.2rem; }
.article-item { padding: 0.6rem 0; border-bottom: 1px solid #2a2a2a; display: flex; gap: 0.8rem; }
.article-cover { width: 72px; height: 72px; border-radius: 8px; object-fit: cover; flex-shrink: 0; }
.article-title { color: #f0ece6; text-decoration: none; font-size: 0.9rem; }
.article-meta { display: flex; justify-content: space-between; margin-top: 0.3rem; font-size: 0.75rem; color: #9a9590; }
.footer { text-align: center; padding: 2rem; color: #666; font-size: 0.8rem; }
</style>
</head>
<body>
<div class="header">
    <h1>{{SKILL_NAME}}</h1>
    <p>{{DATE_CN}} | {{PLATFORM_COUNT}} 个平台 · 共 {{TOTAL_COUNT}} 条内容</p>
</div>
<div class="stats">
    <div class="stat-item"><div class="stat-value">{{PLATFORM_COUNT}}</div><div class="stat-label">平台</div></div>
    <div class="stat-item"><div class="stat-value">{{TOTAL_COUNT}}</div><div class="stat-label">内容</div></div>
    <div class="stat-item"><div class="stat-value">{{CATEGORY_COUNT}}</div><div class="stat-label">分类</div></div>
    <div class="stat-item"><div class="stat-value">{{TOTAL_ENGAGEMENT}}</div><div class="stat-label">总互动</div></div>
</div>
{{OVERVIEW_SECTION}}
{{CROSS_SECTION}}
{{PLATFORM_SECTIONS}}
<div class="footer">Generated at {{TIMESTAMP}} by {{SKILL_NAME}}</div>
</body>
</html>'''


# ─── 订阅机制 ──────────────────────────────────────────────────────────────────────
def _subscription_args(platform_spec, keywords_spec, extra=None):
    script_path = os.path.abspath(Path(__file__).resolve().parent / "multi_ai_feed.py")
    args = ["/usr/bin/env", "python3", script_path,
            "--platform", platform_spec, "--latest", "--no-open"]
    if keywords_spec:
        args += ["--keywords", keywords_spec]
    if extra:
        args += list(extra)
    return script_path, args


def install_subscription(platform_spec="all", keywords_spec=None):
    """安装每日定时任务，参数固化当前的平台与关键词选择"""
    script_path, args = _subscription_args(platform_spec, keywords_spec)
    xml_args = "\n".join(f"        <string>{a}</string>" for a in args)

    if sys.platform == "darwin":
        PLIST_DIR.mkdir(parents=True, exist_ok=True)
        plist_path = PLIST_DIR / f"{PLIST_LABEL}.plist"
        log_path = str(Path.home() / "Library" / "Logs" / "qoder-multi-ai-feed.log")

        env_section = ""
        api_key = get_api_key()
        if api_key:
            env_section = f"""
    <key>EnvironmentVariables</key>
    <dict>
        <key>{ENV_KEY}</key>
        <string>{api_key}</string>
    </dict>"""

        plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{PLIST_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
{xml_args}
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>{SUBSCRIBE_HOUR}</integer>
        <key>Minute</key>
        <integer>{SUBSCRIBE_MINUTE}</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>{log_path}</string>
    <key>StandardErrorPath</key>
    <string>{log_path}</string>
    <key>RunAtLoad</key>
    <false/>{env_section}
</dict>
</plist>'''
        plist_path.write_text(plist_content, encoding="utf-8")
        try:
            subprocess.run(["launchctl", "unload", str(plist_path)], capture_output=True)
            subprocess.run(["launchctl", "load", str(plist_path)], check=True, capture_output=True)
            info(f"订阅成功! 每天 {SUBSCRIBE_HOUR:02d}:{SUBSCRIBE_MINUTE:02d} 自动生成多平台 AI 日报")
            info(f"平台范围: {platform_spec}" + (f" | 关键词: {keywords_spec}" if keywords_spec else ""))
            info(f"日报目录: {DEFAULT_OUTPUT_DIR}")
            info(f"日志: {log_path}")
            return True
        except subprocess.CalledProcessError as e:
            error(f"订阅安装失败: {(e.stderr or b'').decode(errors='ignore')}")
            return False

    cron_line = (f"{SUBSCRIBE_MINUTE} {SUBSCRIBE_HOUR} * * * "
                 + " ".join(_shell_quote(a) for a in args))
    try:
        subprocess.run(
            f'(crontab -l 2>/dev/null | grep -v "{PLIST_LABEL}"; '
            f'echo "{cron_line} # {PLIST_LABEL}") | crontab -',
            shell=True, check=True, capture_output=True,
        )
        info(f"订阅成功! 每天 {SUBSCRIBE_HOUR:02d}:{SUBSCRIBE_MINUTE:02d} 自动生成多平台 AI 日报 (crontab)")
        info(f"平台范围: {platform_spec}" + (f" | 关键词: {keywords_spec}" if keywords_spec else ""))
        info(f"日报目录: {DEFAULT_OUTPUT_DIR}")
        return True
    except subprocess.CalledProcessError:
        warn("自动配置 crontab 失败，请手动添加:")
        print(f"  {cron_line}")
        return False


def _shell_quote(value):
    import shlex
    return shlex.quote(str(value))


def remove_subscription():
    """卸载定时任务"""
    if sys.platform == "darwin":
        plist_path = PLIST_DIR / f"{PLIST_LABEL}.plist"
        if not plist_path.exists():
            warn("未找到订阅配置，无需取消")
            return False
        try:
            subprocess.run(["launchctl", "unload", str(plist_path)], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            pass
        plist_path.unlink(missing_ok=True)
        info("已取消订阅，定时任务已移除")
        return True

    script_path = os.path.abspath(Path(__file__).resolve().parent / "multi_ai_feed.py")
    try:
        subprocess.run(
            f'crontab -l 2>/dev/null | grep -v "{script_path}" | crontab -',
            shell=True, check=True, capture_output=True,
        )
        info("已取消订阅，crontab 任务已移除")
        return True
    except subprocess.CalledProcessError:
        warn("自动移除 crontab 失败，请手动执行: crontab -e")
        return False


def show_subscription():
    """查看当前订阅状态"""
    if sys.platform == "darwin":
        plist_path = PLIST_DIR / f"{PLIST_LABEL}.plist"
        if not plist_path.exists():
            warn("当前未安装订阅")
            return
        info(f"已安装订阅: {plist_path}")
        try:
            out = subprocess.run(["launchctl", "list"], capture_output=True, check=True).stdout.decode()
            for line in out.splitlines():
                if PLIST_LABEL in line:
                    print(f"  {line.strip()}")
        except subprocess.CalledProcessError:
            pass
        print(f"  执行时间: 每天 {SUBSCRIBE_HOUR:02d}:{SUBSCRIBE_MINUTE:02d}")
        return

    script_path = os.path.abspath(Path(__file__).resolve().parent / "multi_ai_feed.py")
    try:
        out = subprocess.run("crontab -l 2>/dev/null", shell=True, capture_output=True).stdout.decode()
    except Exception:
        out = ""
    lines = [l for l in out.splitlines() if script_path in l]
    if lines:
        info("已安装订阅:")
        for line in lines:
            print(f"  {line}")
    else:
        warn("当前未安装订阅")


# ─── 浏览器 ────────────────────────────────────────────────────────────────────────
def open_in_browser(url):
    try:
        if sys.platform == "darwin":
            subprocess.run(["open", url], check=False)
        elif sys.platform == "win32":
            os.startfile(url)  # noqa
        else:
            subprocess.run(["xdg-open", url], check=False)
        return True
    except Exception as e:
        warn(f"打开浏览器失败: {e}")
        return False


# ─── 单平台执行（供 CLI 编排调用） ──────────────────────────────────────────────────
def run_platform(session, slug, keywords, target_count, start_date, end_date,
                 other_platform_names=(), intel_enabled=True, top_n=5,
                 start_time=None, end_time=None):
    """抓取 → 归一化 → 聚类 → 统计 → 情报，返回单平台结果字典"""
    cfg = PLATFORMS[slug]

    available, latest = check_date_available(end_date, cfg["update_hour"])
    if not available:
        return {
            "slug": slug,
            "skipped": True,
            "reason": f"{cfg['name']} {end_date} 数据尚未更新（每日 {cfg['update_hour']}:00 更新前一天，"
                      f"当前最新可查 {latest}）",
            "latest": latest,
            "articles": [],
            "clusters": [],
            "stats": compute_stats([], slug),
            "briefing": None,
        }

    if cfg["time_style"] == "none":
        # 该平台接口不接受时间参数，显式传入也无效
        start_time, end_time = None, None
    elif not (start_time and end_time):
        start_time, end_time = build_time_params(cfg["time_style"], start_date, end_date)
    step(f"[{cfg['name']}] 扫描关键词: {list(keywords)}")
    if start_time:
        step(f"[{cfg['name']}] 时间范围: {start_time} ~ {end_time}")
    else:
        step(f"[{cfg['name']}] 该平台不支持时间过滤，返回最新收录内容")

    raw = fetch_platform(session, slug, list(keywords), target_count,
                         start_time=start_time, end_time=end_time)
    articles = normalize_articles(slug, raw)
    if not articles:
        return {
            "slug": slug,
            "skipped": False,
            "reason": f"{cfg['name']} 未获取到内容",
            "articles": [],
            "clusters": [],
            "stats": compute_stats([], slug),
            "briefing": None,
        }

    info(f"[{cfg['name']}] 扫描完成: {len(articles)} {cfg['unit']}")
    clusters = cluster_articles(articles, cfg["rank_field"], top_n=top_n)
    info(f"[{cfg['name']}] 聚类完成: {len(clusters)} 个分类")

    briefing = None
    if intel_enabled:
        briefing = generate_intelligence_briefing(clusters, articles, slug, other_platform_names)

    return {
        "slug": slug,
        "skipped": False,
        "reason": "",
        "articles": articles,
        "clusters": clusters,
        "stats": compute_stats(articles, slug),
        "briefing": briefing,
    }


def _slim_briefing(briefing):
    """情报摘要瘦身：去掉内嵌的完整作品对象，只保留标题与 ID"""
    if not briefing:
        return None
    slim = dict(briefing)
    slim["top_topics"] = [
        {
            "topic": t["topic"],
            "count": t["count"],
            "ratio": t["ratio"],
            "top_metric": t["top_metric"],
            "metric_label": t["metric_label"],
            "top_title": (t.get("top_article") or {}).get("title"),
            "top_id": (t.get("top_article") or {}).get("photoId"),
        }
        for t in briefing.get("top_topics", [])
    ]
    return slim


def results_to_json(results, display_date, platform_slugs):
    """归一化 JSON 输出，供 Agent 二次加工"""
    return {
        "skill": SKILL_NAME,
        "date": display_date,
        "platforms": [
            {
                "slug": r["slug"],
                "name": PLATFORMS[r["slug"]]["name"],
                "source": PLATFORMS[r["slug"]]["source"],
                "skipped": r.get("skipped", False),
                "reason": r.get("reason", ""),
                "total": r["stats"]["total"],
                "stats": {
                    "avg_primary": r["stats"]["avg_primary"],
                    "total_primary": r["stats"]["total_primary"],
                    "primary_label": r["stats"]["total_label"],
                    "top_author": r["stats"]["top_author"],
                    "total_engagement": r["stats"]["total_engagement"],
                },
                "clusters": [
                    {
                        "category": c["category"],
                        "count": c["count"],
                        "articles": [
                            {
                                "title": a.get("title"),
                                "author": a.get("userName"),
                                "url": a.get("url"),
                                "cover": a.get("coverUrl"),
                                "likeCount": a.get("likeCount") or 0,
                                "shareCount": a.get("shareCount") or 0,
                                "commentCount": a.get("commentCount") or 0,
                                "engagement": engagement_of(a),
                            }
                            for a in c["articles"]
                        ],
                    }
                    for c in r["clusters"]
                ],
                "intelligence": _slim_briefing(r.get("briefing")),
            }
            for r in results
        ],
        "requested_platforms": list(platform_slugs),
    }
