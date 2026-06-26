#!/usr/bin/env python3
"""
Novel Scraper - 轻量级小说抓取工具
针对低内存服务器优化，支持会话复用、自动内存监控、错误恢复

核心特性：
- 会话复用（每 3 章释放一次内存）
- 自动内存监控（>2.5GB 自动释放）
- 错误恢复（失败自动重试 3 次）
- 轻量级（复用 agent-browser）
- 智能滚动（内容不再增加时停止）
- 缓存系统（避免重复抓取）
"""

import json
import time
import hashlib
import logging
import random
import argparse
import re
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin
import subprocess

# 配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
SKILL_DIR = WORKSPACE / "skills" / "novel-scraper"
CONFIG_DIR = SKILL_DIR / "configs"
STATE_DIR = SKILL_DIR / "state"
LOG_DIR = SKILL_DIR / "logs"
CACHE_DIR = Path("/tmp/novel_scraper_cache")
NOVELS_DIR = WORKSPACE / "novels"

# 确保目录存在
for d in [CONFIG_DIR, STATE_DIR, LOG_DIR, CACHE_DIR, NOVELS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "scraper.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MemoryMonitor:
    """内存监控器 - 学习自成功案例"""
    
    def __init__(self, limit_mb=2500):
        self.limit_mb = limit_mb
    
    def check(self):
        """检查内存使用（通过/proc/meminfo）"""
        try:
            with open('/proc/meminfo', 'r') as f:
                mem_info = {}
                for line in f:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        mem_info[key.strip()] = int(value.strip().split()[0]) / 1024  # MB
            
            total = mem_info.get('MemTotal', 0)
            available = mem_info.get('MemAvailable', 0)
            used = total - available
            
            if used > self.limit_mb:
                logger.warning(f"⚠️ 内存过高 ({used:.0f}MB/{self.limit_mb}MB)，需要释放")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ 内存检查失败：{e}")
            return False


class CacheManager:
    """缓存管理器 - 支持章节级和页面级缓存"""
    
    def __init__(self, cache_dir=CACHE_DIR, use_cache=True):
        self.cache_dir = Path(cache_dir)
        self.use_cache = use_cache
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get_cache_key(self, url, page_num=None):
        """生成缓存键（MD5）"""
        if page_num is not None:
            # 页面级缓存
            key_str = f"{url}_page_{page_num}"
        else:
            # 章节级缓存
            key_str = url
        return hashlib.md5(key_str.encode()).hexdigest()[:16]
    
    def get(self, url, page_num=None):
        """从缓存获取内容"""
        if not self.use_cache:
            return None
        
        cache_key = self.get_cache_key(url, page_num)
        cache_file = self.cache_dir / f"{cache_key}.txt"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    lines = f.read().strip().split('\n')
                    if lines:
                        if page_num is not None:
                            # 页面级缓存直接返回内容
                            logger.info(f" 💾 使用页面缓存：{url} (第{page_num}页)")
                            return lines
                        else:
                            # 章节级缓存
                            logger.info(f" 💾 使用章节缓存：{url}")
                            book_name = None
                            author = None
                            if lines[0].startswith('BOOK:'):
                                book_info = lines[0].replace('BOOK:', '').split(':')
                                book_name = book_info[0] if len(book_info) > 0 else None
                                author = book_info[1] if len(book_info) > 1 else None
                                return {'book_name': book_name, 'author': author, 'content': lines[1:]}
                            return {'book_name': None, 'author': None, 'content': lines}
            except Exception as e:
                logger.warning(f" ⚠️ 缓存读取失败：{e}")
        return None
    
    def save(self, url, content, book_name=None, author=None, page_num=None):
        """保存到缓存"""
        if not self.use_cache:
            return
        
        cache_key = self.get_cache_key(url, page_num)
        cache_file = self.cache_dir / f"{cache_key}.txt"
        
        try:
            if page_num is not None:
                # 页面级缓存直接保存内容
                with open(cache_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(content))
            else:
                # 章节级缓存
                lines = content[:]
                if book_name:
                    lines.insert(0, f"BOOK:{book_name}:{author or ''}")
                with open(cache_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
        except Exception as e:
            logger.warning(f" ⚠️ 缓存保存失败：{e}")
    
    def clear_chapter_cache(self, url):
        """清除章节的所有缓存（包括页面缓存）"""
        cache_key = self.get_cache_key(url)
        # 清除章节级缓存
        chapter_file = self.cache_dir / f"{cache_key}.txt"
        if chapter_file.exists():
            chapter_file.unlink()
        # 清除页面级缓存
        for i in range(1, 11):  # 最多 10 页
            page_key = self.get_cache_key(url, i)
            page_file = self.cache_dir / f"{page_key}.txt"
            if page_file.exists():
                page_file.unlink()


class ProgressTracker:
    """进度追踪器 - 支持中断续抓"""
    
    def __init__(self, state_dir=STATE_DIR):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.progress_file = self.state_dir / "progress.json"
        self.progress = {"chapters": [], "last_url": None, "errors": []}
        self.load()
    
    def load(self):
        """加载进度"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    self.progress = json.load(f)
            except Exception as e:
                logger.warning(f" ⚠️ 进度加载失败：{e}")
    
    def save(self):
        """保存进度"""
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.progress, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning(f" ⚠️ 进度保存失败：{e}")
    
    def start_chapter(self, url, chapter_num):
        """开始抓取章节"""
        # 只在新章节时重置页码
        if self.progress.get("current_chapter") != chapter_num:
            self.progress["current_page"] = 1
        
        self.progress["last_url"] = url
        self.progress["current_chapter"] = chapter_num
        self.save()
    
    def complete_page(self, url, page_num, content_len):
        """完成一页抓取"""
        self.progress["current_page"] = page_num + 1
        self.progress["last_page_len"] = content_len
        self.save()
    
    def complete_chapter(self, url, chapter_num, title):
        """完成章节抓取"""
        self.progress["chapters"].append({
            "url": url,
            "title": title,
            "chapter": chapter_num,
            "time": datetime.now().isoformat()
        })
        self.save()
    
    def record_error(self, url, error, retry_count, chapter_num=None):
        """记录错误"""
        self.progress["errors"].append({
            "url": url,
            "chapter": chapter_num,
            "error": str(error),
            "retry_count": retry_count,
            "time": datetime.now().isoformat()
        })
        # 限制错误记录数量
        if len(self.progress["errors"]) > 100:
            self.progress["errors"] = self.progress["errors"][-100:]
        self.save()
    
    def get_resume_point(self, urls, book_url=None):
        """获取续抓起点"""
        completed_urls = [c["url"] for c in self.progress.get("chapters", [])]
        
        # 检查书籍上下文
        if book_url and self.progress.get("book_url"):
            if self.progress["book_url"] != book_url:
                logger.info(" 🔄 检测到新书，清空旧进度")
                self.clear()
                self.progress["book_url"] = book_url
                return 0, urls
        
        # 找到第一个未完成的 URL
        for i, (url, chapter_num) in enumerate(urls):
            if url not in completed_urls:
                logger.info(f" 🔄 发现未完成章节：{url} (第{chapter_num}章)")
                # 返回原始列表的切片，保持章节编号不变
                return i, urls[i:]
        
        logger.info(" ✅ 所有章节已完成")
        return len(urls), []
    
    def clear(self):
        """清空进度"""
        self.progress = {"chapters": [], "last_url": None, "errors": []}
        if self.progress_file.exists():
            self.progress_file.unlink()


class NovelScraper:
    """小说抓取器 - 整合成功案例的优秀实践"""
    
    def __init__(self, memory_limit_mb=2500, auto_close_interval=3, 
                 retry_times=3, wait_time=2, use_progress=True):
        self.memory_monitor = MemoryMonitor(limit_mb=memory_limit_mb)
        self.cache = CacheManager()
        self.progress = ProgressTracker() if use_progress else None
        self.auto_close_interval = auto_close_interval
        self.retry_times = retry_times
        self.wait_time = wait_time
        self.browser_target = None
        self.chapters_fetched = 0
        self.site_config = {}
        
        logger.info("📖 NovelScraper 初始化完成")
        logger.info(f"  内存限制：{memory_limit_mb}MB")
        logger.info(f"  释放间隔：每{auto_close_interval}章")
        logger.info(f"  重试次数：{retry_times}")
        logger.info(f"  缓存目录：{CACHE_DIR}")
        if self.progress:
            logger.info("  进度追踪：✅ 已启用")
    
    def load_site_config(self, domain):
        """加载网站配置"""
        config_file = CONFIG_DIR / "sites.json"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                configs = json.load(f)
                return configs.get(domain, {})
        return {}
    
    def browser_action(self, action, *args, **kwargs):
        """调用 browser 工具"""
        cmd = ["openclaw", "browser", action]
        
        # 特殊处理：url 是位置参数
        if args:
            cmd.extend(args)
        
        # 添加目标 ID
        if self.browser_target and action not in ["open", "navigate", "start"]:
            cmd.append(self.browser_target)
        
        # 添加其他参数
        for key, value in kwargs.items():
            if isinstance(value, bool):
                if value:
                    cmd.append(f"--{key}")
            else:
                cmd.extend([f"--{key}", str(value)])
        
        logger.debug(f"执行：{' '.join(cmd)}")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                               universal_newlines=True, timeout=60)
        
        if result.returncode != 0:
            raise Exception(f"browser 命令失败：{result.stderr}")
        
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"output": result.stdout}
    
    def close_browser(self):
        """关闭浏览器释放内存"""
        if self.browser_target:
            try:
                self.browser_action("close")
                logger.info("✅ 浏览器已关闭")
                self.browser_target = None
                time.sleep(1)
            except Exception as e:
                logger.error(f"❌ 关闭浏览器失败：{e}")
    
    def fetch_page(self, url):
        """打开页面"""
        try:
            result = self.browser_action("open", url)
            self.browser_target = result.get("targetId")
            logger.debug(f"浏览器目标：{self.browser_target}")
            return True
        except Exception as e:
            logger.error(f"❌ 打开页面失败：{e}")
            return False
    
    def get_snapshot(self):
        """获取页面快照"""
        result = self.browser_action("snapshot", format="aria")
        return result.get("output", "") or result.get("text", "")
    
    def scroll_page_smart(self, max_times=10, distance=600):
        """智能滚动 - 内容不再增加时停止（学习自成功案例）"""
        logger.info(" 📜 智能滚动...")
        
        # 注意：当前 browser 工具不支持 scroll 命令，使用备用方案
        # 直接获取内容
        content = self.get_content()
        logger.info(f" ✅ 获取内容 ({len(content)}段)")
        return content
    
    def get_title_from_snapshot(self, snapshot_text):
        """从快照提取章节标题"""
        lines = snapshot_text.split('\n')
        
        # 查找第一个 heading（通常是章节标题）
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('- heading'):
                match = re.search(r'heading "([^"]+)"', stripped)
                if match:
                    title = match.group(1).strip()
                    # 检查前几行是否包含"第 X 章"格式
                    '\n'.join(lines[max(0,i-5):i+5])
                    if '第' in title and '章' in title:
                        return title
                    # 如果是"推荐小说"等，也返回
                    if i < 20:  # 只在文档开头部分
                        return title
        return None
    
    def get_book_info(self, snapshot_text):
        """从快照提取书名和作者（学习自成功案例）"""
        lines = snapshot_text.split('\n')
        
        # 方法：从 breadcrumb 提取书名（heading 之前的最后一个非导航链接）
        book_name = None
        author = None
        
        # 导航链接黑名单
        nav_links = {'笔趣阁', '首页', '仙侠', '目录', '换肤', '阅读记录', '我的书架', '排行榜', '完本'}
        
        last_valid_link = None
        for i, line in enumerate(lines):
            # 找到 heading 就停止（heading 之前是面包屑）
            if 'heading' in line:
                break
            
            # 查找 link "文本" 格式
            match = re.search(r'link "([^"]+)"', line)
            if match:
                link_text = match.group(1)
                # 排除导航链接
                if link_text not in nav_links:
                    last_valid_link = link_text
        
        if last_valid_link:
            book_name = last_valid_link
            logger.info(f" 📚 从面包屑提取书名：{book_name}")
            return book_name, author
        
        return None, None
    
    def get_next_page_url(self, snapshot_text, base_url):
        """检测下一页链接（结合快照解析 + URL 推断）"""
        lines = snapshot_text.split('\n')
        
        # 方法 1: 尝试从快照中查找下一页 URL
        for i, line in enumerate(lines):
            if 'link "下一页"' in line:
                # 在后续行中查找 URL
                for j in range(i+1, min(i+10, len(lines))):
                    url_match = re.search(r'- /url: ([^\s]+)', lines[j].strip())
                    if url_match:
                        next_path = url_match.group(1)
                        return urljoin(base_url, next_path)
        
        # 方法 2: URL 推断（适用于 bqquge 等网站）
        # 匹配模式：/4/1962 或 /4/1962-2
        match = re.search(r'/(\d+)(?:-(\d+))?$', base_url)
        if match:
            chapter_id = match.group(1)
            page_num = match.group(2)
            
            if page_num is None:
                # 第一页，推断第二页
                next_url = re.sub(r'/\d+$', f'/{chapter_id}-2', base_url)
                logger.debug(f"推断下一页：{next_url}")
                return next_url
            else:
                # 已有页码，增加页码
                current_page = int(page_num)
                next_page = current_page + 1
                next_url = re.sub(r'-\d+$', f'-{next_page}', base_url)
                logger.debug(f"推断下一页：{next_url}")
                return next_url
        
        return None
    
    def _infer_next_page_url(self, base_url, current_page=None):
        """推断下一页 URL（不依赖快照）"""
        # 匹配模式：/4/1962 或 /4/1962-2
        match = re.search(r'/(\d+)(?:-(\d+))?$', base_url)
        if match:
            chapter_id = match.group(1)
            page_num = match.group(2)
            
            if page_num is None:
                # 第一页，推断第二页
                next_url = re.sub(r'/\d+$', f'/{chapter_id}-2', base_url)
                logger.debug(f"推断下一页：{next_url}")
                return next_url
            else:
                # 已有页码，增加页码
                current_page = int(page_num)
                next_page = current_page + 1
                next_url = re.sub(r'-\d+$', f'-{next_page}', base_url)
                logger.debug(f"推断下一页：{next_url}")
                return next_url
        return None
    
    def get_content(self):
        """获取页面内容（宽松过滤）"""
        snapshot_text = self.get_snapshot()
        lines = snapshot_text.split('\n')
        
        content = []
        blacklist = [
            '下载 APP', '扫码下载', 'SVIP 抢先看', '会员专享',
            '一秒记住', '推荐本书', '热门推荐：',
            '更新时间：', '最后更新：',
            '章节错误', '点此举报', '删除处理',
            '换肤', '阅读记录', '首页', '仙侠', '目录',
            '上一章', '下一页', '猜你喜欢', '笔趣阁'
        ]
        
        # 单字符过滤（如 ▷）
        single_char_blacklist = {'▷', '>', '<', '|', '/', '\\'}
        
        # 找到章节标题 heading 的位置
        heading_line_idx = -1
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('- heading "'):
                heading_line_idx = i
                break
        
        # 从 heading 之后开始处理
        start_idx = heading_line_idx if heading_line_idx >= 0 else 0
        
        for i in range(start_idx, len(lines)):
            line = lines[i].strip()
            
            # 解析 "- paragraph" 格式（文本在下一行的 StaticText 中）
            if line == '- paragraph':
                # 检查下一行是否有 StaticText
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    # 提取 StaticText "文本" 中的内容
                    match = re.search(r'- StaticText "([^"]+)"', next_line)
                    if match:
                        text = match.group(1).strip()
                        # 过滤：长度、黑名单、单字符、URL
                        if (len(text) >= 2 and  # 至少 2 个字符
                            not any(word in text for word in blacklist) and
                            text not in single_char_blacklist and
                            text.count('http') == 0):
                            content.append(text)
        
        return content
    
    def is_recommendation_page(self, snapshot_text):
        """检测是否是推荐页面 - 检查第一个 heading 是否是"推荐小说" """
        lines = snapshot_text.split('\n')
        
        # 查找第一个主 heading（文档开头部分）
        for i, line in enumerate(lines):
            if i > 30:  # 只检查前 30 行
                break
            stripped = line.strip()
            # 检查是否是顶层 heading（推荐页面的特征）
            if stripped.startswith('- heading "推荐小说"'):
                return True
            # 检查是否有章节标题（正常页面的特征）
            if 'heading' in stripped and '[level=1]' in stripped:
                return False
        
        return False
    
    def fetch_all_pages(self, first_url, chapter_num):
        """自动翻页抓取完整章节（支持页面级缓存和中断续抓）"""
        all_content = []
        current_url = first_url
        page_num = 1
        max_pages = 5  # 大多数网站每章 3-5 页
        
        while current_url and page_num < max_pages:
            logger.info(f" 📄 第{page_num}页...")
            
            # 检查页面缓存
            cached_page = self.cache.get(current_url, page_num)
            if cached_page:
                logger.info(f" ✅ 使用页面缓存 ({len(cached_page)}段)")
                all_content.extend(cached_page)
                
                # 更新进度
                if self.progress:
                    self.progress.complete_page(current_url, page_num, len(cached_page))
                
                # 获取下一页 URL（使用 URL 推断，不依赖快照）
                next_url = self._infer_next_page_url(current_url, page_num)
                
                if next_url:
                    delay = random.uniform(0.5, 1.5)
                    logger.info(f" ⏳ 等待{delay:.1f}秒...")
                    time.sleep(delay)
                    current_url = next_url
                    page_num += 1
                else:
                    logger.info(" ✅ 已是最后一页")
                    break
                continue
            
            # 无缓存，抓取新页面
            if page_num > 1:
                if not self.fetch_page(current_url):
                    logger.warning(f" ⚠️ 打开第{page_num}页失败")
                    break
                time.sleep(1)
            
            page_content = self.get_content()
            
            # 保存到页面缓存
            if page_content:
                self.cache.save(current_url, page_content, page_num=page_num)
                logger.info(f" 💾 保存页面缓存 ({len(page_content)}段)")
                
                # 更新进度
                if self.progress:
                    self.progress.complete_page(current_url, page_num, len(page_content))
            
            all_content.extend(page_content)
            
            snapshot_text = self.get_snapshot()
            next_url = self.get_next_page_url(snapshot_text, current_url)
            
            if next_url:
                delay = random.uniform(0.5, 1.5)
                logger.info(f" ⏳ 等待{delay:.1f}秒...")
                time.sleep(delay)
                current_url = next_url
                page_num += 1
            else:
                logger.info(" ✅ 已是最后一页")
                break
        
        logger.info(f" 📚 共{page_num - 1}页，{len(all_content)}段")
        return all_content
    
    def fetch_chapter(self, url, chapter_num=0):
        """抓取单章（带重试 + 缓存 + 进度追踪）"""
        logger.info(f"📖 抓取第{chapter_num}章：{url}")
        
        # 记录进度
        if self.progress:
            self.progress.start_chapter(url, chapter_num)
        
        # 检查章节缓存
        cached = self.cache.get(url)
        if cached:
            content = cached['content']
            book_name = cached.get('book_name')
            author = cached.get('author')
            title = content[0] if content and content[0].startswith('第') else f"第{chapter_num}章"
            logger.info(" 💾 使用章节缓存...")
            if book_name:
                logger.info(f" 📚 小说：{book_name} (缓存)")
            
            # 记录完成
            if self.progress:
                self.progress.complete_chapter(url, chapter_num, title)
            
            return {
                'title': title,
                'content': content[1:] if content and content[0].startswith('第') else content,
                'book_name': book_name,
                'author': author
            }
        
        for attempt in range(1, self.retry_times + 1):
            try:
                # 打开页面
                if not self.fetch_page(url):
                    logger.warning(f" ⚠️ 打开失败 (尝试 {attempt}/{self.retry_times})")
                    time.sleep(2)
                    continue
                
                time.sleep(self.wait_time)
                
                # 获取快照
                snapshot_text = self.get_snapshot()
                
                # 提取标题
                title = self.get_title_from_snapshot(snapshot_text)
                if not title:
                    title = f"第{chapter_num}章"
                
                # 提取书名和作者（仅第一章）
                book_name = None
                author = None
                if chapter_num == 1:
                    book_name, author = self.get_book_info(snapshot_text)
                
                # 自动翻页抓取完整章节
                content = self.fetch_all_pages(url, chapter_num)
                
                if content:
                    logger.info(f" ✅ 成功 ({len(content)}段) - {title}")
                    
                    # 保存到缓存
                    cache_data = [title] + content
                    self.cache.save(url, cache_data, book_name, author)
                    
                    self.chapters_fetched += 1
                    
                    # 记录完成进度
                    if self.progress:
                        self.progress.complete_chapter(url, chapter_num, title)
                    
                    # 检查是否需要释放内存
                    if self.chapters_fetched % self.auto_close_interval == 0:
                        logger.info(f" 🔄 已达{self.auto_close_interval}章，释放内存...")
                        self.close_browser()
                    
                    # 检查内存
                    if self.memory_monitor.check():
                        logger.info(" 🔄 内存过高，释放...")
                        self.close_browser()
                    
                    return {
                        'title': title,
                        'content': content,
                        'book_name': book_name,
                        'author': author
                    }
                else:
                    logger.warning(f" ⚠️ 无内容 (尝试 {attempt}/{self.retry_times})")
                    time.sleep(1)
            
            except Exception as e:
                logger.error(f" ❌ 错误：{e} (尝试 {attempt}/{self.retry_times})")
                # 记录错误
                if self.progress:
                    self.progress.record_error(url, e, attempt, chapter_num)
                time.sleep(2)
        
        logger.error(f" ❌ 抓取失败（重试{self.retry_times}次）")
        return {'title': f"第{chapter_num}章", 'content': [], 'book_name': None, 'author': None}
    
    def save_to_file(self, contents, output_path=None, book_name=None, author=None, auto_workspace=True):
        """保存到文件（学习自成功案例）"""
        if auto_workspace:
            if not book_name:
                book_name = contents[0].get('book_name', 'novel') if contents else 'novel'
            
            # 如果没有书名，使用默认值
            if not book_name or book_name == 'novel':
                book_name = '小说'
            
            first_ch = contents[0].get('chapter', 1)
            last_ch = contents[-1].get('chapter', first_ch)
            
            # 单章：小说名_第 X 章.txt；多章：小说名_第 X-Y 章.txt
            if first_ch == last_ch:
                filename = f"{book_name}_第{first_ch}章.txt"
            else:
                filename = f"{book_name}_第{first_ch}-{last_ch}章.txt"
            
            filename = "".join(c for c in filename if c not in '<>:"/\\|？*')
            output_path = NOVELS_DIR / filename
        
        logger.info(f"💾 保存到 {output_path}...")
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for item in contents:
                f.write(f"\n{'='*60}\n")
                f.write(f"{item['title']}\n")
                f.write(f"{'='*60}\n\n")
                for para in item['content']:
                    f.write(f"{para}\n\n")
        
        logger.info("✅ 保存完成")
        logger.info(f"📁 文件位置：{output_path}")
        return output_path
    
    def fetch_chapters(self, urls, output=None, book_name=None, auto_workspace=True):
        """抓取多章（会话复用）"""
        logger.info("=" * 60)
        logger.info(f"📖 开始抓取 {len(urls)} 章")
        logger.info("=" * 60)
        
        all_contents = []
        start_time = time.time()
        
        for i, (url, chapter_num) in enumerate(urls, 1):
            logger.info(f"\n[{i}/{len(urls)}]")
            result = self.fetch_chapter(url, chapter_num)
            all_contents.append({
                'chapter': chapter_num,
                'title': result.get('title', f"第{chapter_num}章"),
                'content': result.get('content', []),
                'url': url,
                'book_name': result.get('book_name'),
                'author': result.get('author')
            })
        
        self.close_browser()
        
        duration = time.time() - start_time
        logger.info("\n" + "=" * 60)
        logger.info(f"✅ 完成！用时 {duration:.1f}秒，平均每章 {duration/len(urls):.1f}秒")
        logger.info("=" * 60)
        
        if not book_name and all_contents:
            book_name = all_contents[0].get('book_name')
        
        self.save_to_file(all_contents, output, book_name, auto_workspace=auto_workspace)
        
        return all_contents


def main():
    parser = argparse.ArgumentParser(description='📖 轻量级小说抓取工具')
    parser.add_argument('--url', help='单章 URL')
    parser.add_argument('--urls', help='多章 URL（逗号分隔）')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--book', '-b', help='书名')
    parser.add_argument('--no-auto-save', action='store_true', help='禁用自动保存')
    parser.add_argument('--resume', '-r', action='store_true', help='中断续抓（从上次进度继续）')
    parser.add_argument('--memory-limit', type=int, default=2500, help='内存限制 MB')
    parser.add_argument('--auto-close', type=int, default=3, help='每 N 章释放内存')
    parser.add_argument('--retry', type=int, default=3, help='重试次数')
    parser.add_argument('--wait', type=int, default=2, help='等待时间秒')
    
    args = parser.parse_args()
    
    scraper = NovelScraper(
        memory_limit_mb=args.memory_limit,
        auto_close_interval=args.auto_close,
        retry_times=args.retry,
        wait_time=args.wait,
        use_progress=True  # 默认启用进度追踪
    )
    
    auto_save = not args.no_auto_save
    
    if args.url:
        result = scraper.fetch_chapter(args.url, 1)
        if result['content']:
            print(f"\n{result['title']}\n")
            print("\n".join(result['content'][:10]))
            if auto_save:
                # 优先使用命令行指定的书名，否则使用提取的书名
                book_name = args.book if args.book else result.get('book_name')
                scraper.save_to_file([{'chapter': 1, 'title': result['title'], 'content': result['content'], 
                                      'book_name': result.get('book_name')}], 
                                    args.output, book_name, auto_save)
    elif args.urls:
        urls = [(url.strip(), i+1) for i, url in enumerate(args.urls.split(','))]
        
        # 中断续抓
        if args.resume and scraper.progress:
            logger.info("🔄 启用中断续抓模式...")
            # 提取书籍 URL（从第一个章节 URL 推断）
            book_url = urls[0][0].rsplit('/', 1)[0] if urls else None
            start_idx, urls = scraper.progress.get_resume_point(urls, book_url)
            if start_idx > 0:
                logger.info(f" ✅ 跳过已完成的 {start_idx} 章")
        
        scraper.fetch_chapters(urls, args.output, args.book, auto_save)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
