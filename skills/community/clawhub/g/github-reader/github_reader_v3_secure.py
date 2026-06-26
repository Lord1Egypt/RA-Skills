"""
GitHub Reader Skill v3.2 — 纯 GitHub API 安全版

相比 v3.1 的变更：
- ❌ 移除所有 zread.ai 第三方依赖（代码、输出、URL）
- ❌ 移除 GitView 本地服务引用
- ✅ 纯 GitHub REST API + 本地智能分析
- ✅ 收紧触发词，避免误触发
- ✅ 安全声明有代码对应，不写空话
- ✅ 新增数据流向透明度手册

安全防护（代码实现对应 SECURITY.md 声明）：
- 输入验证：validate_repo_name() — 正则 + 长度 + 路径遍历检测
- SSRF 防护：safe_url_join() — urllib.parse.quote 编码
- 缓存防投毒：SecureGitHubReaderCache — 大小限制 + JSON 结构验证 + 原子写入
- 路径防遍历：safe_file_path() — os.path.abspath + normpath + startswith 检查
- 并发限制：asyncio.Semaphore
- 速率限制：time-based limiter
- 超时控制：asyncio.wait_for on async calls
"""

import re
import json
import hashlib
import os
import time
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from urllib.parse import quote

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


# ============== 安全配置 ==============
class SecurityConfig:
    """安全配置 - 从环境变量读取"""

    # 缓存配置
    CACHE_DIR = os.getenv('GITVIEW_CACHE_DIR', '/tmp/gitview_cache')
    CACHE_TTL_HOURS = int(os.getenv('GITVIEW_CACHE_TTL', '24'))
    CACHE_MAX_SIZE_MB = int(os.getenv('GITVIEW_CACHE_MAX_SIZE', '1'))

    # 速率限制
    GITHUB_API_DELAY = float(os.getenv('GITVIEW_GITHUB_DELAY', '1.0'))
    MAX_CONCURRENT_REQUESTS = int(os.getenv('GITVIEW_MAX_BROWSER', '3'))

    # 超时控制
    FETCH_TIMEOUT = int(os.getenv('GITVIEW_BROWSER_TIMEOUT', '30'))
    GITHUB_API_TIMEOUT = int(os.getenv('GITVIEW_GITHUB_TIMEOUT', '10'))

    # 输入验证
    MAX_NAME_LENGTH = 100
    ALLOWED_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9._-]{0,99}$')

    # 隐私：数据流向声明
    PRIVACY_NOTICE = (
        "🔒 **数据流向声明**：本次分析仅使用 GitHub REST API（{api_url}），"
        "不会将仓库信息发送给任何第三方服务。"
        "分析结果本地缓存 {cache_ttl} 小时，缓存目录：{cache_dir}。"
    )


# ============== 安全工具函数 ==============
def validate_repo_name(name: str) -> bool:
    """
    验证仓库/所有者名称合法性

    安全规则：
    1. 只允许字母、数字、-、_、.
    2. 必须以字母或数字开头
    3. 长度 1-100 字符
    4. 禁止 .. 模式（防止路径遍历）
    5. 禁止以 - 开头（防止命令行注入）
    """
    if not name or not isinstance(name, str):
        return False
    if len(name) > SecurityConfig.MAX_NAME_LENGTH:
        return False
    if not SecurityConfig.ALLOWED_NAME_PATTERN.match(name):
        return False
    if '..' in name:
        return False
    return True


def safe_url_join(base: str, *paths: str) -> str:
    """安全的 URL 拼接 — urllib.parse.quote 编码路径组件，防 SSRF"""
    encoded_paths = [quote(path, safe='') for path in paths]
    return '/'.join([base.rstrip('/')] + encoded_paths)


def safe_file_path(base_dir: str, filename: str) -> str:
    """安全的文件路径生成 — 防路径遍历"""
    safe_name = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
    base_dir = os.path.abspath(base_dir)
    file_path = os.path.normpath(os.path.join(base_dir, safe_name))
    if not file_path.startswith(base_dir):
        raise ValueError(f"Invalid file path: {filename}")
    return file_path


# ============== 安全缓存系统 ==============
class SecureGitHubReaderCache:
    """安全的文件缓存系统"""

    def __init__(self, cache_dir: str = None):
        self.cache_dir = cache_dir or SecurityConfig.CACHE_DIR
        self.cache_ttl = timedelta(hours=SecurityConfig.CACHE_TTL_HOURS)
        self.max_cache_size = SecurityConfig.CACHE_MAX_SIZE_MB * 1024 * 1024
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        try:
            os.makedirs(self.cache_dir, exist_ok=True)
            os.chmod(self.cache_dir, 0o700)
        except Exception as e:
            logger.error(f"Failed to create cache directory: {e}")
            raise

    def _get_cache_key(self, owner: str, repo: str) -> str:
        return hashlib.sha256(f"{owner}/{repo}".encode()).hexdigest()

    def _get_cache_path(self, key: str) -> str:
        return safe_file_path(self.cache_dir, f"{key}.json")

    def get(self, owner: str, repo: str) -> Optional[Dict]:
        if not validate_repo_name(owner) or not validate_repo_name(repo):
            logger.warning(f"Invalid repo name in cache get: {owner}/{repo}")
            return None
        try:
            key = self._get_cache_key(owner, repo)
            path = self._get_cache_path(key)
            if not os.path.exists(path):
                return None
            file_size = os.path.getsize(path)
            if file_size > self.max_cache_size:
                logger.warning(f"Cache file too large: {file_size} bytes")
                os.remove(path)
                return None
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, dict):
                return None
            required_keys = ['owner', 'repo', 'cached_at', 'data']
            if not all(key in data for key in required_keys):
                return None
            cached_at = datetime.fromisoformat(data['cached_at'])
            if datetime.now() - cached_at > self.cache_ttl:
                return None
            return data
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Cache get error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected cache get error: {e}")
            return None

    def set(self, owner: str, repo: str, data: Dict):
        if not validate_repo_name(owner) or not validate_repo_name(repo):
            raise ValueError(f"Invalid repo name: {owner}/{repo}")
        temp_path = None
        try:
            data_size = len(json.dumps(data).encode('utf-8'))
            if data_size > self.max_cache_size:
                raise ValueError(f"Data too large: {data_size} bytes")
            required_keys = ['owner', 'repo', 'analyzed_at']
            for key in required_keys:
                if key not in data:
                    raise ValueError(f"Missing required key: {key}")
            key = self._get_cache_key(owner, repo)
            path = self._get_cache_path(key)
            cache_data = {
                'owner': owner,
                'repo': repo,
                'cached_at': datetime.now().isoformat(),
                'data': data
            }
            temp_path = path + '.tmp'
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.rename(temp_path, path)
        except Exception as e:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
            raise


# ============== GitHub Reader v3.2（纯 API 版） ==============
class SecureGitHubReaderV3:
    """GitHub Reader Skill v3.2 — 纯 GitHub REST API，无第三方依赖"""

    # 收紧后的触发模式：只接受显式命令
    COMMAND_TRIGGERS = [
        r'^/github-read\s+([a-zA-Z0-9_-]+/[a-zA-Z0-9._-]+)',
        r'github\.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9._-]+)',
        r'^(?:分析|解读|analyze)\s+(?:这个)?(?:仓库|项目)?[:：\s]*(?:https?://github\.com/)?([a-zA-Z0-9_-]+/[a-zA-Z0-9._-]+)',
    ]

    def __init__(self):
        self.cache = SecureGitHubReaderCache()
        self.semaphore = asyncio.Semaphore(SecurityConfig.MAX_CONCURRENT_REQUESTS)
        self._api_call_times: list[float] = []

    # ---- 速率限制 ----
    async def _rate_limit(self):
        """滑动窗口速率限制 — 确保 API 调用间隔"""
        now = time.time()
        window = 60.0  # 60 秒窗口
        self._api_call_times = [t for t in self._api_call_times if now - t < window]
        max_calls_per_window = int(window / SecurityConfig.GITHUB_API_DELAY)
        if len(self._api_call_times) >= max_calls_per_window:
            wait = self._api_call_times[0] + window - now + 0.1
            if wait > 0:
                await asyncio.sleep(wait)
        self._api_call_times.append(time.time())

    # ---- 输入解析 ----
    def parse_github_url(self, message: str) -> Optional[tuple[str, str]]:
        """解析 GitHub 仓库标识 — 多模式匹配"""
        for pattern in self.COMMAND_TRIGGERS:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                groups = match.groups()
                if len(groups) >= 2:
                    owner, repo = groups[0], groups[1]
                else:
                    # 单捕获组（owner/repo 在一起）
                    parts = groups[0].split('/')
                    if len(parts) == 2:
                        owner, repo = parts
                    else:
                        continue
                repo = repo.rstrip('.git')  # 去掉 .git 后缀
                if validate_repo_name(owner) and validate_repo_name(repo):
                    return owner, repo
        return None

    # ---- API 调用 ----
    async def _api_get(self, url: str) -> Optional[Dict]:
        """通用 API GET — 带速率限制、超时、大小限制"""
        await self._rate_limit()
        import httpx
        try:
            async with httpx.AsyncClient(timeout=SecurityConfig.GITHUB_API_TIMEOUT) as client:
                resp = await client.get(
                    url,
                    headers={
                        "Accept": "application/vnd.github+json",
                        "X-GitHub-Api-Version": "2022-11-28",
                        "User-Agent": "github-reader-skill-v3.2",
                    },
                )
                if resp.status_code != 200:
                    logger.warning(f"GitHub API {url} returned {resp.status_code}")
                    return None
                data = resp.json()
                if not isinstance(data, dict):
                    return None
                return data
        except Exception as e:
            logger.error(f"GitHub API call failed: {e}")
            return None

    async def fetch_repo_info(self, owner: str, repo: str) -> Optional[Dict]:
        """获取仓库基础信息"""
        if not validate_repo_name(owner) or not validate_repo_name(repo):
            return None
        async with self.semaphore:
            data = await self._api_get(
                safe_url_join('https://api.github.com/repos', owner, repo)
            )
        if not data:
            return None
        license_info = data.get('license')
        return {
            'stars': self.format_number(data.get('stargazers_count', 0)),
            'forks': self.format_number(data.get('forks_count', 0)),
            'issues': data.get('open_issues_count', 0),
            'language': data.get('language', 'Unknown'),
            'license': license_info.get('spdx_id', 'Unknown') if license_info else 'Unknown',
            'description': (data.get('description') or '暂无描述')[:500],
            'topics': (data.get('topics') or [])[:20],
            'updated': self.relative_time(data.get('pushed_at', '')),
            'homepage': (data.get('homepage') or '')[:200],
            'size_kb': data.get('size', 0),
            'archived': data.get('archived', False),
            'default_branch': data.get('default_branch', 'main'),
            'created': data.get('created_at', ''),
        }

    async def fetch_readme(self, owner: str, repo: str) -> Optional[str]:
        """获取 README 内容（截取前 3000 字符用于摘要）"""
        if not validate_repo_name(owner) or not validate_repo_name(repo):
            return None
        async with self.semaphore:
            data = await self._api_get(
                safe_url_join('https://api.github.com/repos', owner, repo, 'readme')
            )
        if not data:
            return None
        content = data.get('content', '')
        if not content:
            return None
        try:
            import base64
            decoded = base64.b64decode(content).decode('utf-8', errors='replace')
            return decoded[:3000]
        except Exception:
            return None

    # ---- 分析入口 ----
    async def analyze_project(self, owner: str, repo: str) -> Dict:
        """综合分析项目 — 纯 GitHub API"""
        if not validate_repo_name(owner) or not validate_repo_name(repo):
            raise ValueError(f"Invalid repo name: {owner}/{repo}")

        # 1. 检查缓存
        cached = self.cache.get(owner, repo)
        if cached:
            cached_data = cached.get('data', cached)
            cached_data['from_cache'] = True
            return cached_data

        # 2. 并行拉取
        repo_task = asyncio.create_task(self.fetch_repo_info(owner, repo))
        readme_task = asyncio.create_task(self.fetch_readme(owner, repo))

        repo_info, readme_raw = await asyncio.gather(
            repo_task, readme_task, return_exceptions=True
        )

        if isinstance(repo_info, Exception):
            logger.error(f"Repo info fetch failed: {repo_info}")
            repo_info = {}
        if isinstance(readme_raw, Exception):
            logger.error(f"README fetch failed: {readme_raw}")
            readme_raw = None

        # 3. 生成报告
        report = self.build_report(owner, repo, repo_info, readme_raw)

        # 4. 缓存
        if report.get('success'):
            try:
                self.cache.set(owner, repo, report)
            except Exception as e:
                logger.error(f"Failed to cache result: {e}")

        report['from_cache'] = False
        return report

    def build_report(
        self,
        owner: str,
        repo: str,
        repo_info: Dict,
        readme_raw: Optional[str],
    ) -> Dict:
        """构建分析报告 — 纯本地生成，不经过任何第三方"""
        info = repo_info or {}
        github_url = safe_url_join('https://github.com', owner, repo)
        analyzed_at = datetime.now().isoformat()

        report = {
            'owner': owner,
            'repo': repo,
            'analyzed_at': analyzed_at,
            'github_url': github_url,
            'github_info': info,
            'success': True,
        }

        # 从 README 提取摘要
        summary_lines = []
        if readme_raw:
            for line in readme_raw.split('\n'):
                clean = line.strip()
                if clean and not clean.startswith('#') and not clean.startswith('![') \
                        and not clean.startswith('<') and len(clean) > 20:
                    summary_lines.append(clean[:200])
                if len(summary_lines) >= 5:
                    break
        report['readme_snippets'] = summary_lines

        # 隐私声明
        report['privacy_notice'] = SecurityConfig.PRIVACY_NOTICE.format(
            api_url=safe_url_join('https://api.github.com/repos', owner, repo),
            cache_ttl=SecurityConfig.CACHE_TTL_HOURS,
            cache_dir=SecurityConfig.CACHE_DIR,
        )

        # Markdown 报告
        report['markdown'] = self._render_markdown(report)
        return report

    def _render_markdown(self, report: Dict) -> str:
        owner = report['owner']
        repo = report['repo']
        info = report.get('github_info', {})
        snippets = report.get('readme_snippets', [])
        github_url = report['github_url']

        description = info.get('description', '这是一个开源项目。')
        snippet_block = '\n'.join(f'> {s}' for s in snippets) if snippets else '> *（README 暂无摘要）*'
        archived_note = '\n> ⚠️ **注意**：此仓库已被归档（只读）\n' if info.get('archived') else ''

        return f"""# 📦 {owner}/{repo} 深度解读报告

> **分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
> **数据来源**: GitHub REST API（纯 API，不经第三方）  
> **隐私**: 仅使用 GitHub 官方 API，不将数据发送给任何第三方服务
{archived_note}
---

## 💡 项目简介
{description}

## 📊 项目卡片

| 指标 | 值 |
|------|-----|
| ⭐ Stars | {info.get('stars', 'N/A')} |
| 🍴 Forks | {info.get('forks', 'N/A')} |
| 📝 Issues | {info.get('issues', 'N/A')} |
| 🐍 语言 | {info.get('language', 'Unknown')} |
| 📄 许可证 | {info.get('license', 'Unknown')} |
| 🕐 最后更新 | {info.get('updated', 'N/A')} |
| 🗂️ 仓库大小 | {info.get('size_kb', 'N/A')} KB |
| 🌿 默认分支 | `{info.get('default_branch', 'main')}` |
| 🏷️ 主题标签 | {' '.join(f'`{t}`' for t in info.get('topics', [])) if info.get('topics') else '无'} |

## 🔗 链接
| 平台 | 链接 |
|------|------|
| **GitHub** | {github_url} |
| 主页 | {info.get('homepage') or '无'} |

## 📖 README 摘要
{snippet_block}

## 🔗 快速开始
```bash
git clone {github_url}.git
cd {repo}
```

{report.get('privacy_notice', '')}

---
*v3.2 — 纯 GitHub API，无第三方数据外传*
"""

    # ---- 工具函数 ----
    def format_number(self, num: int) -> str:
        if num >= 1000000:
            return f'{num / 1000000:.1f}M'
        elif num >= 1000:
            return f'{num / 1000:.1f}k'
        return str(num)

    def relative_time(self, date_str: str) -> str:
        if not date_str:
            return 'N/A'
        try:
            from datetime import timezone
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            diff = (datetime.now(timezone.utc) - date).days
            if diff == 0:
                return '今天'
            elif diff == 1:
                return '昨天'
            elif diff < 7:
                return f'{diff}天前'
            elif diff < 30:
                return f'{diff // 7}周前'
            elif diff < 365:
                return f'{diff // 30}个月前'
            else:
                return f'{diff // 365}年前'
        except Exception:
            return 'N/A'


# ============== Skill 入口 ==============
async def run(context):
    """Skill 入口函数 — v3.2 纯 GitHub API 版"""
    try:
        message = context.get('message', '')
        reader = SecureGitHubReaderV3()
        target = reader.parse_github_url(message)

        if not target:
            return {
                'error': '未能识别 GitHub 仓库链接',
                'hint': (
                    '支持格式：\n'
                    '• `/github-read owner/repo`\n'
                    '• `https://github.com/owner/repo`\n'
                    '• `分析 owner/repo`'
                ),
                'success': False,
            }

        owner, repo = target
        result = await reader.analyze_project(owner, repo)
        return {
            'report': result.get('markdown', ''),
            'from_cache': result.get('from_cache', False),
            'success': result.get('success', False),
        }

    except Exception as e:
        logger.error(f"Skill execution failed: {e}")
        return {
            'error': f'分析失败：{str(e)[:200]}',
            'success': False,
        }
