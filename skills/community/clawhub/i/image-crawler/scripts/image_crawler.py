#!/usr/bin/env python3
"""
通用图片采集工具
支持百度/Bing搜索引擎，关键词拓展，图片去重，进度监控，停滞检测。
Agent 通过 --json 模式解析输出来监控采集进度。
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
import html as html_mod
from pathlib import Path
from urllib.parse import quote, urlparse

try:
    import requests
except ImportError:
    print(json.dumps({"type": "error", "message": "requests 未安装，请运行: pip install requests"}))
    sys.exit(1)


# ─── 输出工具 ───────────────────────────────────────────────

class Reporter:
    """进度报告器，支持普通文本和 JSON 两种模式"""

    def __init__(self, json_mode=False):
        self.json_mode = json_mode

    def emit(self, data: dict):
        if self.json_mode:
            print(json.dumps(data, ensure_ascii=False), flush=True)
        else:
            t = data.get("type", "")
            if t == "start":
                print(f"\n{'='*55}")
                print(f"  图片采集任务")
                print(f"  关键词: {', '.join(data['keywords'])}")
                print(f"  目标: {data['target']} 张 | 引擎: {data['engine']}")
                print(f"  输出: {data['output']}")
                print(f"{'='*55}\n")
            elif t == "search":
                print(f"  🔍 [{data['engine']}] \"{data['keyword']}\" → {data['found']} 条结果")
            elif t == "progress":
                bar_len = 30
                pct = data["downloaded"] / max(data["target"], 1)
                filled = int(bar_len * pct)
                bar = "█" * filled + "░" * (bar_len - filled)
                eta = data.get("eta", "?")
                print(f"  [{bar}] {data['downloaded']}/{data['target']}"
                      f"  ✓{data['downloaded']} ✗{data['failed']} ⊘{data['dedup']}"
                      f"  {data['speed']:.1f}张/s  ETA {eta}")
            elif t == "stall":
                print(f"  ⚠️  {data['message']}")
            elif t == "error":
                print(f"  ❌ {data['message']}")
            elif t == "done":
                print(f"\n{'='*55}")
                print(f"  采集完成!")
                print(f"  成功: {data['total']} 张 | 失败: {data['failed']} | 去重: {data['dedup_removed']}")
                print(f"  耗时: {data['elapsed']:.1f}s | 目录: {data['output']}")
                print(f"{'='*55}\n")
            elif t == "info":
                print(f"  ℹ️  {data['message']}")


# ─── 去重器 ─────────────────────────────────────────────────

class Deduplicator:
    """
    图片去重器。
    - URL 去重：同一 URL 不重复下载
    - 内容 hash 去重：不同 URL 但内容相同的图片只保留一张
    - 跨次运行去重：hash 持久化到 .dedup_hashes.json
    """

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.hash_file = self.output_dir / ".dedup_hashes.json"
        self.url_set: set = set()
        self.hash_set: set = set()
        self.removed_count = 0
        self._load()

    def _load(self):
        if self.hash_file.exists():
            try:
                data = json.loads(self.hash_file.read_text())
                self.hash_set = set(data.get("hashes", []))
                self.url_set = set(data.get("urls", []))
            except Exception:
                pass

    def save(self):
        self.hash_file.write_text(json.dumps({
            "hashes": list(self.hash_set),
            "urls": list(self.url_set),
            "count": len(self.hash_set),
            "updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        }, ensure_ascii=False, indent=2))

    def url_seen(self, url: str) -> bool:
        if url in self.url_set:
            return True
        self.url_set.add(url)
        return False

    def check_file(self, filepath: str) -> bool:
        """返回 True 表示重复，文件会被删除"""
        try:
            h = hashlib.md5()
            with open(filepath, "rb") as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    h.update(chunk)
            digest = h.hexdigest()
            if digest in self.hash_set:
                os.remove(filepath)
                self.removed_count += 1
                return True
            self.hash_set.add(digest)
            return False
        except Exception:
            return False


# ─── 搜索引擎 ───────────────────────────────────────────────

class BaiduEngine:
    """百度图片搜索"""

    NAME = "baidu"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/125.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": "https://image.baidu.com/",
        })

    def search(self, keyword: str, count: int = 60) -> list:
        images = []
        page = 0
        per_page = 30
        max_pages = (count // per_page) + 2

        while len(images) < count and page < max_pages:
            try:
                resp = self.session.get(
                    "https://image.baidu.com/search/acjson",
                    params={
                        "tn": "resultjson_com", "ipn": "rj",
                        "ct": "201326592", "fp": "result",
                        "queryWord": keyword, "word": keyword,
                        "cl": "2", "lm": "-1", "ie": "utf-8", "oe": "utf-8",
                        "st": "-1", "ic": "0", "face": "0",
                        "istype": "2", "nc": "1",
                        "pn": page * per_page, "rn": per_page,
                    },
                    timeout=15,
                )
                if resp.status_code != 200:
                    break
                data = resp.json()
                items = data.get("data", [])
                if not items:
                    break
                for item in items:
                    url = item.get("thumbURL") or item.get("objURL")
                    if url and url.startswith("http"):
                        images.append(url)
            except Exception:
                break
            page += 1
            time.sleep(0.3)

        return images[:count]

    def download(self, url: str, filepath: str, timeout: int = 15) -> bool:
        try:
            resp = self.session.get(url, timeout=(5, timeout), stream=True)
            if resp.status_code != 200:
                return False
            ct = resp.headers.get("content-type", "")
            if "image" not in ct and "octet" not in ct:
                return False
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(8192):
                    if chunk:
                        f.write(chunk)
            if os.path.getsize(filepath) < 2000:
                os.remove(filepath)
                return False
            return True
        except Exception:
            if os.path.exists(filepath):
                os.remove(filepath)
            return False


class BingEngine:
    """Bing 图片搜索"""

    NAME = "bing"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
            "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        })

    def search(self, keyword: str, count: int = 60) -> list:
        images = []
        page = 0
        per_page = 35
        max_pages = (count // per_page) + 2

        while len(images) < count and page < max_pages:
            try:
                url = (f"https://www.bing.com/images/async"
                       f"?q={quote(keyword)}&first={page * per_page}"
                       f"&count={per_page}&mmasync=1")
                resp = self.session.get(url, timeout=20)
                if resp.status_code != 200:
                    break
                decoded = html_mod.unescape(resp.text)
                pattern = r'murl":"(https?://[^"]+\.(?:jpg|jpeg|png|webp))"'
                matches = re.findall(pattern, decoded, re.IGNORECASE)
                if not matches:
                    break
                for m in matches:
                    images.append(m.replace("\\/", "/"))
            except Exception:
                break
            page += 1
            time.sleep(0.5)

        return images[:count]

    def download(self, url: str, filepath: str, timeout: int = 15) -> bool:
        try:
            resp = self.session.get(
                url,
                headers={"Referer": "https://www.bing.com/images/search"},
                timeout=(5, timeout),
                stream=True,
            )
            if resp.status_code != 200:
                return False
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(8192):
                    if chunk:
                        f.write(chunk)
            if os.path.getsize(filepath) < 2000:
                os.remove(filepath)
                return False
            return True
        except Exception:
            if os.path.exists(filepath):
                os.remove(filepath)
            return False


# ─── 关键词拓展 ─────────────────────────────────────────────

def expand_keywords(base_keywords: list, custom_terms: list = None) -> list:
    """
    拓展关键词列表。
    - 保留原始关键词
    - 如果提供了 custom_terms，用每个 term 与每个 base 组合
    - 如果没有 custom_terms，使用通用修饰词
    """
    if custom_terms:
        # 始终保留原始关键词（空字符串代表不添加前缀）
        terms = [""] + [t for t in custom_terms if t]
    else:
        terms = [
            "", "高清", "实拍",
            "工作现场", "施工",
        ]

    expanded = []
    seen = set()
    for kw in base_keywords:
        for term in terms:
            combined = f"{term}{kw}".strip() if term else kw
            if combined not in seen:
                seen.add(combined)
                expanded.append(combined)
    return expanded


# ─── 主采集器 ───────────────────────────────────────────────

class ImageCrawler:

    def __init__(self, args):
        self.keywords = args.keywords
        self.target = args.count
        self.output_dir = Path(args.output)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.engine_name = args.engine
        self.do_expand = args.expand
        self.expand_terms = args.expand_terms
        self.min_size = args.min_size * 1024  # KB → bytes
        self.dl_timeout = args.timeout
        self.stall_timeout = args.stall_timeout
        self.progress_interval = args.progress_interval
        self.reporter = Reporter(json_mode=args.json)

        # 初始化引擎
        self.engines = []
        if self.engine_name in ("baidu", "both"):
            self.engines.append(BaiduEngine())
        if self.engine_name in ("bing", "both"):
            self.engines.append(BingEngine())

        # 去重器
        self.dedup = Deduplicator(str(self.output_dir))

        # 统计
        self.downloaded = 0
        self.failed = 0
        self.skipped_dedup = 0

    def _existing_count(self) -> int:
        """统计输出目录中已有的图片数"""
        exts = {".jpg", ".jpeg", ".png", ".webp"}
        return sum(1 for f in self.output_dir.iterdir()
                   if f.is_file() and f.suffix.lower() in exts
                   and not f.name.startswith("."))

    def _next_index(self) -> int:
        """获取下一个文件编号"""
        exts = {".jpg", ".jpeg", ".png", ".webp"}
        max_idx = 0
        pattern = re.compile(r"_(\d+)\.\w+$")
        for f in self.output_dir.iterdir():
            if f.is_file() and f.suffix.lower() in exts:
                m = pattern.search(f.name)
                if m:
                    max_idx = max(max_idx, int(m.group(1)))
        return max_idx + 1

    def collect_urls(self) -> list:
        """搜索并收集所有候选图片 URL"""
        # 关键词处理
        keywords = self.keywords
        if self.do_expand:
            keywords = expand_keywords(keywords, self.expand_terms)
            self.reporter.emit({
                "type": "info",
                "message": f"关键词拓展: {len(self.keywords)} → {len(keywords)} 个"
                           f" ({', '.join(keywords[:6])}{'...' if len(keywords) > 6 else ''})"
            })

        all_urls = []
        # 每个关键词分配的搜索量
        per_kw = max(self.target // max(len(keywords), 1), 30)

        for kw in keywords:
            for engine in self.engines:
                urls = engine.search(kw, count=per_kw)
                new_urls = [u for u in urls if not self.dedup.url_seen(u)]
                all_urls.extend(new_urls)
                self.reporter.emit({
                    "type": "search",
                    "engine": engine.NAME,
                    "keyword": kw,
                    "found": len(urls),
                    "new": len(new_urls),
                })
                if len(all_urls) >= self.target * 2:
                    break
            if len(all_urls) >= self.target * 2:
                break

        self.reporter.emit({
            "type": "info",
            "message": f"搜索完成，共 {len(all_urls)} 个不重复 URL，开始下载..."
        })
        return all_urls

    def run(self) -> dict:
        existing = self._existing_count()
        actual_target = self.target

        self.reporter.emit({
            "type": "start",
            "keywords": self.keywords,
            "target": actual_target,
            "engine": self.engine_name,
            "output": str(self.output_dir.absolute()),
            "existing": existing,
        })

        if existing > 0:
            self.reporter.emit({
                "type": "info",
                "message": f"目录已有 {existing} 张图片，将跳过重复内容"
            })

        urls = self.collect_urls()
        if not urls:
            self.reporter.emit({"type": "error", "message": "未搜索到任何图片 URL"})
            return self._summary(0)

        # 选择下载引擎（优先第一个）
        engine = self.engines[0]
        idx = self._next_index()
        start_time = time.time()
        last_success_time = start_time
        consecutive_fails = 0
        stall_warned = False

        for url in urls:
            if self.downloaded >= actual_target:
                break

            # 停滞检测
            elapsed_since_success = time.time() - last_success_time
            if elapsed_since_success > self.stall_timeout:
                self.reporter.emit({
                    "type": "error",
                    "message": f"连续 {int(elapsed_since_success)}s 无新图片，"
                               f"可能遇到反爬或网络问题，中断采集"
                })
                break
            if elapsed_since_success > self.stall_timeout * 0.5 and not stall_warned:
                stall_warned = True
                self.reporter.emit({
                    "type": "stall",
                    "message": f"已 {int(elapsed_since_success)}s 无新图片，继续尝试..."
                })

            # 反爬检测
            if consecutive_fails >= 15:
                self.reporter.emit({
                    "type": "error",
                    "message": f"连续 {consecutive_fails} 次下载失败，可能触发反爬机制，中断采集"
                })
                break

            # 确定文件名
            ext = ".jpg"
            parsed_path = urlparse(url).path.lower()
            for e in (".png", ".webp", ".jpeg"):
                if parsed_path.endswith(e):
                    ext = e
                    break
            filename = f"img_{idx:05d}{ext}"
            filepath = self.output_dir / filename

            # 下载
            ok = engine.download(url, str(filepath), self.dl_timeout)
            if ok:
                # 内容去重
                if self.dedup.check_file(str(filepath)):
                    self.skipped_dedup += 1
                    continue
                # 最小文件大小检查
                if os.path.exists(str(filepath)) and os.path.getsize(str(filepath)) < self.min_size:
                    os.remove(str(filepath))
                    self.failed += 1
                    consecutive_fails += 1
                    continue

                self.downloaded += 1
                idx += 1
                consecutive_fails = 0
                last_success_time = time.time()
                stall_warned = False
            else:
                self.failed += 1
                consecutive_fails += 1

            # 进度报告
            if self.downloaded % self.progress_interval == 0 and self.downloaded > 0:
                elapsed = time.time() - start_time
                speed = self.downloaded / max(elapsed, 0.1)
                remaining = actual_target - self.downloaded
                eta_sec = remaining / max(speed, 0.01)
                self.reporter.emit({
                    "type": "progress",
                    "downloaded": self.downloaded,
                    "target": actual_target,
                    "failed": self.failed,
                    "dedup": self.skipped_dedup,
                    "speed": round(speed, 2),
                    "eta": f"{int(eta_sec)}s" if eta_sec < 120 else f"{eta_sec/60:.1f}min",
                })

            time.sleep(0.15)

        # 保存去重数据
        self.dedup.save()
        return self._summary(time.time() - start_time)

    def _summary(self, elapsed: float) -> dict:
        result = {
            "type": "done",
            "total": self.downloaded,
            "failed": self.failed,
            "dedup_removed": self.skipped_dedup,
            "elapsed": round(elapsed, 1),
            "output": str(self.output_dir.absolute()),
        }
        self.reporter.emit(result)
        return result


# ─── CLI ─────────────────────────────────────────────────────

def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="图片采集工具 - 支持百度/Bing图片搜索",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 百度搜索，采集 100 张挖掘机图片
  python image_crawler.py -k 挖掘机 -n 100 -o ./images

  # 启用关键词拓展，使用自定义品牌词
  python image_crawler.py -k 挖掘机 -n 200 --expand --expand-terms 三一,卡特,小松

  # Bing 引擎，JSON 输出（供 agent 解析）
  python image_crawler.py -k excavator -n 50 -e bing --json

  # 多关键词采集
  python image_crawler.py -k 挖掘机 -k 装载机 -n 100 -o ./data
        """,
    )
    p.add_argument("-k", "--keywords", action="append", required=True,
                   help="搜索关键词（可多次指定）")
    p.add_argument("-n", "--count", type=int, default=100,
                   help="目标图片数量（默认 100）")
    p.add_argument("-o", "--output", default="./crawled_images",
                   help="输出目录（默认 ./crawled_images）")
    p.add_argument("-e", "--engine", choices=["baidu", "bing", "both"],
                   default="baidu", help="搜索引擎（默认 baidu）")
    p.add_argument("--expand", action="store_true",
                   help="启用关键词拓展")
    p.add_argument("--expand-terms", type=lambda s: s.split(","),
                   default=None, help="自定义拓展词（逗号分隔）")
    p.add_argument("--min-size", type=int, default=5,
                   help="最小文件大小 KB（默认 5）")
    p.add_argument("--timeout", type=int, default=15,
                   help="单张下载超时秒数（默认 15）")
    p.add_argument("--stall-timeout", type=int, default=60,
                   help="停滞超时秒数（默认 60）")
    p.add_argument("--progress-interval", type=int, default=10,
                   help="每 N 张输出一次进度（默认 10）")
    p.add_argument("--json", action="store_true",
                   help="JSON 格式输出（供程序解析）")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    crawler = ImageCrawler(args)
    result = crawler.run()
    sys.exit(0 if result["total"] > 0 else 1)


if __name__ == "__main__":
    main()
