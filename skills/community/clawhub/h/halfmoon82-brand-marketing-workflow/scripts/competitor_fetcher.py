#!/usr/bin/env python3
"""竞品数据采集模块

输入（stdin JSON）:
  {
    "competitor_scope": ["UNIQLOZH public signals", "Notion public signals"],
    "brand_name": "Aurora Lane"
  }

输出（stdout JSON）:
  [
    {
      "competitor_name": "UNIQLOZH",
      "raw_text": "...(最多 6000 字符)...",
      "source_type": "jina" | "brave" | "none",
      "url_used": "...",
      "fetched_at": "2026-03-23T10:00:00",
      "fetch_ok": true,
      "error": null
    }
  ]
"""
from __future__ import annotations

import gzip
import json
import os
import sys
import tempfile
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config" / "competitor_targets.json"
EVIDENCE_DIR = BASE_DIR / "evidence"
OPENCLAW_JSON = Path.home() / ".openclaw" / "openclaw.json"

MAX_TEXT_LEN = 6000
HTTP_TIMEOUT = 20  # 秒

BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------

def _load_config() -> dict:
    """加载 competitor_targets.json，找不到则返回空 dict。"""
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _load_brave_key() -> str:
    """从 openclaw.json 读取 BRAVE_API_KEY，找不到则返回空字符串。"""
    try:
        cfg = json.loads(OPENCLAW_JSON.read_text(encoding="utf-8"))
        return cfg.get("env", {}).get("vars", {}).get("BRAVE_API_KEY", "")
    except Exception:
        return ""


def _cache_path() -> Path:
    """当日缓存文件路径。"""
    today = datetime.now().strftime("%Y%m%d")
    return EVIDENCE_DIR / f"competitor_cache_{today}.json"


def _load_cache() -> dict:
    """加载当日缓存，key 为竞品名称。带 TTL 检查（6小时）。"""
    path = _cache_path()
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                items = {item["competitor_name"]: item for item in data if "competitor_name" in item}
                # TTL 检查：6小时 = 21600秒
                TTL_SECONDS = 6 * 60 * 60
                now = datetime.now(timezone.utc).timestamp()
                valid_items = {}
                for name, item in items.items():
                    fetched_at = item.get("fetched_at", "")
                    if fetched_at:
                        try:
                            fetched_ts = datetime.fromisoformat(fetched_at.replace("Z", "+00:00")).timestamp()
                            if now - fetched_ts < TTL_SECONDS:
                                valid_items[name] = item
                            else:
                                print(f"[CACHE] TTL expired for {name}, will re-fetch", file=sys.stderr)
                        except Exception:
                            valid_items[name] = item  # 解析失败保留
                    else:
                        valid_items[name] = item
                return valid_items
        except Exception:
            pass
    return {}


def _save_cache(results: list[dict]) -> None:
    """将结果写入当日缓存文件。"""
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    path = _cache_path()
    # 合并：加载已有缓存后覆盖/追加本次结果
    existing: dict = {}
    if path.exists():
        try:
            old = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(old, list):
                existing = {item["competitor_name"]: item for item in old if "competitor_name" in item}
        except Exception:
            pass
    for r in results:
        existing[r["competitor_name"]] = r
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(list(existing.values()), ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.rename(path)


def _http_get(url: str, headers: dict | None = None) -> str:
    """执行 HTTP GET，返回响应文本。支持 gzip。超时 20s。"""
    req = urllib.request.Request(url, headers=headers or {})
    req.add_header("User-Agent", "Mozilla/5.0 (compatible; BrandBot/1.0)")
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
        raw = resp.read()
        # 如果服务端返回 gzip，手动解压
        encoding = resp.headers.get("Content-Encoding", "")
        if encoding == "gzip":
            raw = gzip.decompress(raw)
        # 检测 charset
        content_type = resp.headers.get("Content-Type", "")
        charset = "utf-8"
        if "charset=" in content_type:
            charset = content_type.split("charset=")[-1].split(";")[0].strip()
        return raw.decode(charset, errors="replace")


def _filter_noise(text: str) -> str:
    """过滤竞品信号中的噪声内容（广告、导航栏、页脚等）。"""
    import re
    
    # 删除常见噪声模式
    noise_patterns = [
        r'\[广告\].*?\n',  # 广告标记
        r'跳转.*?\n',      # 跳转提示
        r'点击.*?查看.*?\n',  # CTA 噪声
        r'© \d{4}.*?\n',   # 版权页脚
        r'隐私政策|用户协议|联系我们|关于我们',  # 导航链接
        r'\d+\.\d+\.\d+.*?更新日志',  # 版本信息
    ]
    
    filtered = text
    for pattern in noise_patterns:
        filtered = re.sub(pattern, '', filtered, flags=re.IGNORECASE)
    
    # 删除过短的行（可能是导航项）
    lines = filtered.split('\n')
    meaningful_lines = [l for l in lines if len(l.strip()) > 15]
    
    return '\n'.join(meaningful_lines)


def _score_relevance(text: str, competitor_name: str) -> float:
    """评分文本与竞品的相关性（0-1）。"""
    if not text:
        return 0.0
    
    text_lower = text.lower()
    name_lower = competitor_name.lower()
    
    # 基础分数：品牌名出现次数
    name_count = text_lower.count(name_lower)
    base_score = min(name_count * 0.1, 0.3)  # 最多 0.3
    
    # 行业关键词加分
    industry_keywords = ['品牌', '营销', '策略', '产品', '市场', '用户', '增长', 
                        'brand', 'marketing', 'strategy', 'product', 'growth']
    keyword_hits = sum(1 for kw in industry_keywords if kw in text_lower)
    keyword_score = min(keyword_hits * 0.05, 0.4)  # 最多 0.4
    
    # 内容长度适中加分（太短=没信息，太长=噪声多）
    length = len(text)
    if 500 <= length <= 3000:
        length_score = 0.3
    elif length > 3000:
        length_score = 0.2
    else:
        length_score = 0.1
    
    return min(base_score + keyword_score + length_score, 1.0)


def _truncate(text: str) -> str:
    """截断到 MAX_TEXT_LEN 字符。"""
    if len(text) <= MAX_TEXT_LEN:
        return text
    return text[:MAX_TEXT_LEN] + "…[截断]"


def _filter_and_score(text: str, competitor_name: str) -> tuple[str, float]:
    """过滤噪声并评分相关性，返回 (filtered_text, relevance_score)。"""
    filtered = _filter_noise(text)
    score = _score_relevance(filtered, competitor_name)
    return filtered, score


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


# ---------------------------------------------------------------------------
# 核心采集逻辑
# ---------------------------------------------------------------------------

def fetch_via_jina(url: str) -> tuple[str, str]:
    """通过 jina.ai reader 获取页面文本。返回 (text, jina_url)。"""
    jina_url = f"https://r.jina.ai/{url}"
    text = _http_get(jina_url)
    return text, jina_url


def fetch_via_brave(query: str, brave_key: str) -> str:
    """通过 Brave Search API 搜索，将 title+description 拼成文本。

    注意：country/search_lang 参数在 Free tier 可能触发 422，故不传递。
    query 中若含中文字符，自动追加英文关键词提升命中率。
    """
    # 空串保护
    if not query or not query.strip():
        return {"fetch_ok": False, "error": "empty query", "raw_text": "", "source_type": "brave", "url_used": BRAVE_SEARCH_URL}

    # 若 query 含中文，构造英文补充查询以避免 422
    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in query)
    if has_chinese:
        words = query.split()
        latin_parts = [w for w in words if w and not any('\u4e00' <= c <= '\u9fff' for c in w)]
        if latin_parts:
            q = " ".join(latin_parts)
        elif words:
            q = query.split()[0]  # 退路：直接用第一个词
        else:
            q = "brand marketing"  # 完全兜底
        # 追加通用品牌营销关键词
        q = f"{q} brand marketing strategy"
    else:
        q = query

    params = urllib.parse.urlencode({
        "q": q,
        "count": 5,
    })
    full_url = f"{BRAVE_SEARCH_URL}?{params}"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": brave_key,
    }
    resp_text = _http_get(full_url, headers=headers)
    data = json.loads(resp_text)
    results = data.get("web", {}).get("results", [])
    parts: list[str] = []
    for r in results:
        title = r.get("title", "")
        desc = r.get("description", "")
        link = r.get("url", "")
        parts.append(f"【{title}】\n{desc}\n{link}")
    return "\n\n".join(parts)


def fetch_competitor(name: str, targets_cfg: dict, brave_key: str) -> dict:
    """采集单个竞品。"""
    target = targets_cfg.get(name, {})
    urls: list[str] = target.get("urls", [])
    search_query: str = target.get("search_query", f"{name} 品牌营销 OR 产品更新")

    fetched_at = _now_iso()

    # --- 尝试 jina ---
    if urls:
        for url in urls:
            try:
                text, jina_url = fetch_via_jina(url)
                text = _truncate(text.strip())
                # 过滤噪声并评分
                filtered_text, relevance_score = _filter_and_score(text, name)
                if len(filtered_text) >= 50:
                    return {
                        "competitor_name": name,
                        "raw_text": filtered_text,
                        "source_type": "jina",
                        "url_used": jina_url,
                        "fetched_at": fetched_at,
                        "fetch_ok": True,
                        "relevance_score": relevance_score,
                        "error": None,
                    }
            except Exception as e:
                print(f"[DEBUG] jina fetch failed for {url}: {e}", file=sys.stderr)

    # --- 尝试 Brave Search ---
    if brave_key:
        try:
            text = fetch_via_brave(search_query, brave_key)
            text = _truncate(text.strip())
            # 过滤噪声并评分
            filtered_text, relevance_score = _filter_and_score(text, name)
            if len(filtered_text) >= 50:
                return {
                    "competitor_name": name,
                    "raw_text": filtered_text,
                    "source_type": "brave",
                    "url_used": BRAVE_SEARCH_URL,
                    "fetched_at": fetched_at,
                    "fetch_ok": True,
                    "relevance_score": relevance_score,
                    "error": None,
                }
            # Brave 返回但内容太短
            return {
                "competitor_name": name,
                "raw_text": "",
                "source_type": "brave",
                "url_used": BRAVE_SEARCH_URL,
                "fetched_at": fetched_at,
                "fetch_ok": False,
                "error": "brave returned insufficient content",
            }
        except Exception as e:
            return {
                "competitor_name": name,
                "raw_text": "",
                "source_type": "brave",
                "url_used": BRAVE_SEARCH_URL,
                "fetched_at": fetched_at,
                "fetch_ok": False,
                "error": f"brave error: {e}",
            }

    # --- 无任何来源 ---
    return {
        "competitor_name": name,
        "raw_text": "",
        "source_type": "none",
        "url_used": "",
        "fetched_at": fetched_at,
        "fetch_ok": False,
        "error": "no url configured and no brave key available",
    }


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def main() -> int:
    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps([], ensure_ascii=False))
        return 0

    payload = json.loads(raw)
    competitor_scope: list[str] = payload.get("competitor_scope", [])

    if not competitor_scope:
        print(json.dumps([], ensure_ascii=False))
        return 0

    # 从 "UNIQLOZH public signals" → "UNIQLOZH"
    names: list[str] = [s.split()[0] for s in competitor_scope if s.strip()]

    targets_cfg = _load_config()
    brave_key = _load_brave_key()
    cache = _load_cache()

    results: list[dict] = []
    newly_fetched: list[dict] = []

    for name in names:
        if name in cache:
            # 命中缓存，直接使用
            results.append(cache[name])
        else:
            item = fetch_competitor(name, targets_cfg, brave_key)
            results.append(item)
            newly_fetched.append(item)

    # 持久化新采集的结果
    if newly_fetched:
        try:
            _save_cache(newly_fetched)
        except Exception as e:
            print(f"[WARN] cache write failed: {e}", file=sys.stderr)

    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
