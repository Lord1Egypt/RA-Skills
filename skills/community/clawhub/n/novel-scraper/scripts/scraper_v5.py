#!/usr/bin/env python3
"""
Novel Scraper V5 - 智能合并版

合并策略：
1. 以 V1.4.0 为基础（稳定可靠）
2. V4 功能作为可选增强（通过参数控制）
3. 智能降级（高级功能失败时自动 fallback）
4. 保持向后兼容（V1.4.0 参数继续有效）

核心改进：
- 章节号自动解析（默认启用，失败时 fallback 到 URL ID）
- 分页检测（默认检测，补全需启用 --complete）
- 质量验证（基础验证默认，深度验证可选）
- 连续性检查（默认启用，低成本）
"""

import re
import sys
import time
import random
import logging
import argparse
import subprocess
import json
from pathlib import Path
from urllib.parse import urlparse, urljoin

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False
    print("❌ 需要安装 BeautifulSoup: pip3 install beautifulsoup4")
    sys.exit(1)

# 配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
NOVELS_DIR = WORKSPACE / "novels"
CACHE_DIR = Path("/tmp/novel_scraper_cache")
STATE_DIR = WORKSPACE / "skills" / "novel-scraper" / "state"

for d in [NOVELS_DIR, CACHE_DIR, STATE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(NOVELS_DIR / "scraper.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

# 速率限制
RATE_LIMIT = {
    "interval": (2.0, 4.0),
    "retry_delay": (5.0, 10.0),
    "max_retries": 3,
}

# 内容黑名单
BLACKLIST = [
    "笔趣阁", "首页", "目录", "上一章", "下一章", "推荐本书",
    "加入书签", "章节错误", "投推荐票", "手机版", "APP 下载",
]

# 章节结束标记
END_MARKERS = ["本章完", "本章完结", "（本章完）", "(本章完)", "未完待续"]


def fetch_html(url, retries=3):
    """获取 HTML，带重试"""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Invalid URL scheme: {url}")
    if any(c in url for c in [";", "|", "&", "$", "`"]):
        raise ValueError(f"Unsafe URL: {url}")
    
    retry_delay = random.uniform(*RATE_LIMIT["retry_delay"])
    
    for attempt in range(retries):
        try:
            cmd = [
                "curl", "-s", "-L", "--max-time", "30",
                "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                url,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
            if result.returncode == 0:
                return result.stdout
            raise Exception(f"curl failed: {result.stderr}")
        except Exception:
            if attempt < retries - 1:
                logger.debug(f"第{attempt+1}次失败，等待{retry_delay:.1f}秒后重试...")
                time.sleep(retry_delay)
                retry_delay *= 1.5
            else:
                raise
    return None


def extract_chapter_number(title):
    """从标题解析章节号"""
    if not title:
        return None
    
    patterns = [
        r"第\s*(\d+)\s*章",
        r"(\d+)\.",
        r"(\d+)\s*章",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title)
        if match:
            return int(match.group(1))
    
    return None


def extract_content(html, url):
    """
    提取章节内容（自动检测分页）
    
    Args:
        html: HTML 内容
        url: 当前 URL
    
    Returns:
        (title, content, next_url)
    """
    soup = BeautifulSoup(html, "html.parser")
    
    # 查找内容区域
    content_div = soup.find("div", class_="con") or soup.find("div", id="content")
    
    if not content_div:
        return None, [], None
    
    # 清理无关元素
    for tag in content_div.find_all(["script", "style", "div", "span"], 
                                     class_=re.compile(r"nav|footer|header|ad|share")):
        tag.decompose()
    
    # 提取标题
    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else None
    
    if not title:
        title_match = re.search(r"<title>([^<]+)</title>", str(soup))
        if title_match:
            title = title_match.group(1).strip()
    
    # 提取段落
    paragraphs = []
    for p in content_div.find_all("p"):
        text = p.get_text(strip=True)
        if text and not any(word in text for word in BLACKLIST):
            paragraphs.append(text)
    
    # 分页检测（总是检测，智能判断）
    next_url = None
    # 查找包含"下一页"的链接（可能在 span 内）
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        if "下一页" in text or re.search(r"第\d+页", text):
            next_url = urljoin(url, a.get("href"))
            logger.debug(f"  分页链接：{next_url}")
            break
    
    return title, paragraphs, next_url


def check_content_quality(title, content, strict=False):
    """
    检查内容质量
    
    Args:
        title: 章节标题
        content: 内容段落列表
        strict: 是否严格模式（默认 False，只记录警告不阻止）
    
    Returns:
        {passed, issues, stats}
    """
    issues = []
    stats = {
        "paragraphs": len(content),
        "chars": sum(len(p) for p in content),
        "has_end_marker": False,
    }
    
    # 基础验证（默认启用，低成本）
    if stats["paragraphs"] < 3:
        issues.append(f"段落数过少 ({stats['paragraphs']})")
    
    # 结束标记检查（默认启用）
    full_text = "\n".join(content)
    for marker in END_MARKERS:
        if marker in full_text:
            stats["has_end_marker"] = True
            break
    
    # 严格模式额外检查
    if strict:
        if stats["chars"] < 1000:
            issues.append(f"字符数过少 ({stats['chars']})")
        
        if not stats["has_end_marker"]:
            issues.append("未找到章节结束标记")
    
    return {
        "passed": len(issues) == 0 or not strict,
        "issues": issues,
        "stats": stats,
    }


def save_chapters(chapters_data, book_name, merge_interval=10):
    """保存章节到文件"""
    if not chapters_data:
        logger.warning("⚠️ 没有内容可保存")
        return []
    
    saved_files = []
    
    for i in range(0, len(chapters_data), merge_interval):
        group = chapters_data[i:i + merge_interval]
        first_ch = group[0]["number"]
        last_ch = group[-1]["number"]
        
        if first_ch == last_ch:
            filename = f"{book_name}_第{first_ch}章.txt"
        else:
            filename = f"{book_name}_第{first_ch}-{last_ch}章.txt"
        
        filename = "".join(c for c in filename if c not in '<>:"/\\|？*')
        file_path = NOVELS_DIR / filename
        
        logger.info(f"💾 保存到 {file_path}...")
        
        with open(file_path, "w", encoding="utf-8") as f:
            for ch in group:
                f.write(f"\n{'=' * 60}\n")
                f.write(f"{ch['title']}\n")
                f.write(f"{'=' * 60}\n\n")
                for para in ch["content"]:
                    f.write(f"{para}\n\n")
        
        logger.info(f"✅ 保存完成 ({len(group)}章)")
        saved_files.append(file_path)
    
    return saved_files


def scrape_urls(urls, book_name=None, merge_interval=10, strict_quality=False):
    """
    智能抓取（V5 合并版）
    
    Args:
        urls: URL 列表 [(url, expected_ch_num), ...]
        book_name: 书名
        merge_interval: 合并间隔
        strict_quality: 是否严格质量验证（默认 False）
    
    Returns:
        saved_files: 保存的文件列表
    """
    logger.info("=" * 60)
    logger.info("📖 Novel Scraper V5 - 智能合并版")
    logger.info("=" * 60)
    logger.info(f"📝 预计抓取：{len(urls)}章")
    logger.info("📄 分页处理：自动检测并补全")
    
    if not book_name:
        book_name = "小说"
    
    chapters_data = []
    incomplete_chapters = []
    consecutive_failures = 0  # 连续失败计数器
    
    for idx, (url, expected_ch_num) in enumerate(urls, 1):
        logger.info(f"\n[{idx}/{len(urls)}] 第{expected_ch_num}章：{url}")
        
        # 检查缓存
        cache_key = f"ch_{url.replace('/', '_').replace(':', '_')}"
        cache_file = CACHE_DIR / f"{cache_key}.txt"
        
        if cache_file.exists():
            try:
                cached_data = cache_file.read_text(encoding="utf-8").split("\n", 1)
                if len(cached_data) == 2:
                    cached_title = cached_data[0]
                    cached_content = cached_data[1].split("\n")
                    logger.info(f"  💾 使用缓存 ({len(cached_content)}段)")
                    
                    ch_num = extract_chapter_number(cached_title)
                    chapters_data.append({
                        "number": ch_num if ch_num else expected_ch_num,
                        "title": cached_title,
                        "content": cached_content,
                    })
                    consecutive_failures = 0  # 重置失败计数
                    continue
            except Exception as e:
                logger.debug(f"缓存读取失败：{e}")
        
        # 抓取
        success = False
        for retry in range(RATE_LIMIT["max_retries"]):
            try:
                html = fetch_html(url)
                if not html:
                    raise Exception("无法获取页面")
                
                # 提取内容（自动检测分页）
                title, content, next_url = extract_content(html, url)
                
                # 跳过非小说内容（只有一页且没有章节号）
                parsed_ch_num = extract_chapter_number(title)
                if not parsed_ch_num and not next_url:
                    logger.info(f"  ⏭️ 跳过非小说内容：{title[:40]}...（无章节号且无分页）")
                    chapters_data.append({
                        "number": expected_ch_num,
                        "title": f"[跳过] {title}",
                        "content": ["[非小说内容，已跳过]"],
                    })
                    success = True
                    consecutive_failures = 0
                    break
                
                if not title:
                    title = f"第{expected_ch_num}章"
                
                if not content or len(content) < 3:
                    raise Exception(f"内容过少 ({len(content) if content else 0}段)")
                
                # 质量检查
                quality = check_content_quality(title, content, strict=strict_quality)
                
                if quality["issues"]:
                    for issue in quality["issues"]:
                        logger.warning(f"  ⚠️ {issue}")
                
                # 解析章节号（优先从标题，fallback 到预期）
                parsed_ch_num = extract_chapter_number(title)
                ch_num = parsed_ch_num if parsed_ch_num else expected_ch_num
                
                if parsed_ch_num and parsed_ch_num != expected_ch_num:
                    logger.info(f"  📝 章节号修正：{expected_ch_num} → {ch_num}")
                
                # 保存缓存
                cache_key = f"ch_{url.replace('/', '_').replace(':', '_')}"
                cache_file = CACHE_DIR / f"{cache_key}.txt"
                cache_file.write_text(f"{title}\n" + "\n".join(content), encoding="utf-8")
                
                chapters_data.append({
                    "number": ch_num,
                    "title": title,
                    "content": content,
                })
                
                logger.info(f"  ✅ 成功 ({len(content)}段) - {title[:40]}...")
                
                # 标记不完整（用于分页补全）
                logger.debug(f"  next_url={next_url}, has_end_marker={quality['stats']['has_end_marker']}")
                if next_url and not quality["stats"]["has_end_marker"]:
                    logger.info("  📄 检测到分页，标记待补全")
                    incomplete_chapters.append({
                        "url": url,
                        "ch_num": ch_num,
                        "title": title,
                        "content": content,
                        "next_url": next_url,
                    })
                
                success = True
                consecutive_failures = 0  # 成功，重置失败计数
                break
                
            except Exception as e:
                logger.warning(f"  ⚠️ 第{retry+1}次失败：{e}")
                if retry < RATE_LIMIT["max_retries"] - 1:
                    time.sleep(random.uniform(*RATE_LIMIT["retry_delay"]))
        
        if not success:
            consecutive_failures += 1
            logger.error(f"  ❌ 抓取失败 (连续失败 {consecutive_failures}/2)")
            
            # 连续失败 2 次，自动切换目录页模式
            if consecutive_failures >= 2:
                logger.warning("\n" + "=" * 60)
                logger.warning("⚠️  连续失败 2 次，检测到 URL ID 不连续")
                logger.warning("🔄 自动切换到目录页模式，获取正确的 URL 映射...")
                logger.warning("=" * 60)
                
                # 调用目录页脚本获取正确的 URL 映射
                try:
                    from pathlib import Path
                    import json
                    import subprocess
                    
                    # 运行 fetch_catalog.py
                    catalog_script = Path(__file__).parent / "fetch_catalog.py"
                    logger.info(f"📚 运行目录页脚本：{catalog_script}")
                    
                    result = subprocess.run(
                        ["python3", str(catalog_script)],
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    
                    if result.returncode != 0:
                        logger.error(f"❌ 目录页脚本失败：{result.stderr}")
                        raise Exception("目录页脚本执行失败")
                    
                    # 读取正确的 URL 映射
                    catalog_file = Path(__file__).parent / "state" / "book_4_catalog.json"
                    if not catalog_file.exists():
                        raise Exception("目录页文件不存在")
                    
                    with open(catalog_file, "r", encoding="utf-8") as f:
                        all_chapters = json.load(f)
                    
                    # 找到当前章节的正确 URL
                    current_ch_idx = next(
                        (i for i, ch in enumerate(all_chapters) if ch["number"] == expected_ch_num),
                        None
                    )
                    
                    if current_ch_idx is None:
                        logger.error(f"❌ 未在目录页找到第{expected_ch_num}章")
                        raise Exception(f"未找到第{expected_ch_num}章")
                    
                    # 获取剩余章节的正确 URL
                    remaining_chapters = all_chapters[current_ch_idx:]
                    remaining_urls = [(ch["url"], ch["number"]) for ch in remaining_chapters]
                    
                    logger.info(f"✅ 获取到 {len(remaining_urls)} 章的正确 URL")
                    logger.info(f"📝 从第{remaining_chapters[0]['number']}章开始继续抓取")
                    
                    # 递归调用，使用正确的 URL 列表
                    logger.info("\n" + "=" * 60)
                    logger.info("🔄 使用正确的 URL 继续抓取...")
                    logger.info("=" * 60)
                    
                    # 保存已抓取的章节
                    if chapters_data:
                        # 过滤掉失败的章节
                        chapters_data = [ch for ch in chapters_data if "[抓取失败]" not in ch.get("title", "")]
                    
                    # 递归抓取剩余章节
                    remaining_data = scrape_urls(
                        urls=remaining_urls,
                        book_name=book_name,
                        merge_interval=merge_interval,
                        strict_quality=strict_quality
                    )
                    
                    # 合并结果
                    chapters_data.extend(remaining_data)
                    break
                    
                except Exception as e:
                    logger.error(f"❌ 自动切换目录页模式失败：{e}")
                    logger.info("请手动运行：python3 scripts/fetch_catalog.py")
                    # 继续但不再尝试
        
        # 速率限制
        if idx < len(urls):
            time.sleep(random.uniform(*RATE_LIMIT["interval"]))
    
    # 分页补全（自动检测，智能处理）
    if incomplete_chapters:
        logger.info(f"\n🔄 检测到 {len(incomplete_chapters)} 个分页章节，自动补全...")
        
        for i, ch_info in enumerate(incomplete_chapters, 1):
            logger.info(f"  [{i}/{len(incomplete_chapters)}] 补全第{ch_info['ch_num']}章...")
            
            all_content = ch_info["content"][:]
            next_url = ch_info["next_url"]
            page_count = 1
            
            while next_url and page_count < 5:
                try:
                    logger.debug(f"    抓取第{page_count + 1}页：{next_url}")
                    html = fetch_html(next_url, retries=2)
                    if not html:
                        break
                    
                    _, page_content, next_url = extract_content(html, next_url)
                    
                    if not page_content:
                        break
                    
                    all_content.extend(page_content)
                    page_count += 1
                    time.sleep(random.uniform(1.0, 2.0))
                    
                except Exception as e:
                    logger.debug(f"    分页抓取失败：{e}")
                    break
            
            # 更新章节数据
            for j, ch in enumerate(chapters_data):
                if ch["number"] == ch_info["ch_num"]:
                    chapters_data[j]["content"] = all_content
                    logger.info(f"    ✅ 补全完成，共{len(all_content)}段")
                    break
            
            # 更新缓存
            cache_key = f"ch_{ch_info['url'].replace('/', '_').replace(':', '_')}"
            cache_file = CACHE_DIR / f"{cache_key}.txt"
            cache_file.write_text(f"{ch_info['title']}\n" + "\n".join(all_content), encoding="utf-8")
    
    # 连续性检查（默认启用，低成本）
    logger.info("\n🔗 检查章节连续性...")
    chapters_data.sort(key=lambda x: x["number"])
    
    gaps = []
    for i in range(1, len(chapters_data)):
        if chapters_data[i]["number"] - chapters_data[i-1]["number"] > 1:
            gap_start = chapters_data[i-1]["number"]
            gap_end = chapters_data[i]["number"]
            gaps.append((gap_start, gap_end))
            logger.warning(f"  ⚠️ 缺章：第{gap_start}章 - 第{gap_end}章")
    
    if not gaps:
        logger.info("  ✅ 章节连续")
    
    # 保存
    logger.info("\n" + "=" * 60)
    logger.info(f"✅ 完成！{len(chapters_data)}章")
    logger.info("=" * 60)
    
    saved_files = save_chapters(chapters_data, book_name, merge_interval)
    
    # 统计
    failed = sum(1 for ch in chapters_data if "抓取失败" in ch["title"])
    if failed:
        logger.warning(f"⚠️ 失败章节：{failed}章")
    
    if gaps:
        logger.info(f"⚠️ 缺章：{len(gaps)}处")
    
    return saved_files


def load_catalog():
    """加载目录数据"""
    catalog_file = STATE_DIR / "book_4_catalog.json"
    if not catalog_file.exists():
        return None
    with open(catalog_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_urls_by_chapter_range(data, start_ch, end_ch):
    """按章节号范围提取 URL（修复索引切片 bug）"""
    chapters = [c for c in data if start_ch <= int(c['number']) <= end_ch]
    if not chapters:
        return None, []
    # 返回正确章节号范围
    actual_start = chapters[0]['number']
    actual_end = chapters[-1]['number']
    urls = [(c['url'], int(c['number'])) for c in chapters]
    return (actual_start, actual_end), urls


def main():
    parser = argparse.ArgumentParser(description="📖 智能合并版小说抓取工具 V5")
    
    # V1.4.0 兼容参数
    parser.add_argument("--url", help="单章 URL")
    parser.add_argument("--urls", help="多章 URL（逗号分隔）")
    parser.add_argument("--book", "-b", help="书名")
    parser.add_argument("--merge-interval", type=int, default=10, help="每 N 章合并 (默认 10)")
    
    # V1.4.0 性能参数（保留但 unused，保持兼容）
    parser.add_argument("--memory-limit", type=int, default=2500, help="内存限制 MB")
    parser.add_argument("--auto-close", type=int, default=3, help="每 N 章释放内存")
    parser.add_argument("--retry", type=int, default=3, help="重试次数")
    
    # 新增：按章节号范围抓取（修复索引切片 bug）
    parser.add_argument("--chapters", help="章节号范围，格式：起始 - 结束 (例：301-400)")
    
    # 质量选项
    parser.add_argument("--strict", action="store_true",
                        help="严格质量验证（字符数 <1000 警告）")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="详细日志输出")
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 解析 URL 列表
    urls = []
    if args.url:
        urls = [(args.url, 1)]
    elif args.urls:
        url_list = [u.strip() for u in args.urls.split(",")]
        urls = [(url, i + 1) for i, url in enumerate(url_list)]
    elif args.chapters:
        # 按章节号范围抓取（正确方式！）
        try:
            parts = args.chapters.split('-')
            if len(parts) != 2:
                raise ValueError("格式应为：起始 - 结束")
            start_ch, end_ch = int(parts[0]), int(parts[1])
            if start_ch > end_ch:
                raise ValueError("起始章节号不能大于结束章节号")
        except ValueError as e:
            parser.error(f"--chapters 参数错误：{e}")
        
        # 加载目录
        catalog = load_catalog()
        if not catalog:
            parser.error("未找到目录文件，请先运行 fetch_catalog.py")
        
        # 提取 URL
        chapter_range, urls = extract_urls_by_chapter_range(catalog, start_ch, end_ch)
        if not urls:
            parser.error(f"未找到第{start_ch}-{end_ch}章的目录数据")
        
        actual_start, actual_end = chapter_range
        missing_count = (end_ch - start_ch + 1) - len(urls)
        logger.info(f"📋 章节号范围：{start_ch}-{end_ch}")
        logger.info(f"📋 实际抓取：{actual_start}-{actual_end} ({len(urls)}章)")
        if missing_count > 0:
            logger.warning(f"⚠️ 缺失{missing_count}章（网站目录中没有）")
    else:
        parser.error("需要指定 --url、--urls 或 --chapters")
    
    saved_files = scrape_urls(
        urls=urls,
        book_name=args.book,
        merge_interval=args.merge_interval,
        strict_quality=args.strict,
    )
    
    if saved_files:
        print(f"\n✅ 保存了 {len(saved_files)} 个文件:")
        for f in saved_files:
            print(f"  📁 {f}")
    else:
        print("\n❌ 没有保存任何文件")
        sys.exit(1)


if __name__ == "__main__":
    main()
