#!/usr/bin/env python3
"""Personal Knowledge Graph - Filesystem Scanner (Step 1)

通用文件系统扫描器。不硬编码任何用户特定的路径或目录名。
适配任何操作系统、任何目录结构。

Usage:
    python scan_filesystem.py --root /path/to/scan
    python scan_filesystem.py --root /path --config namespace_rules.yaml
    python scan_filesystem.py --root /path --dry-run
    python scan_filesystem.py --root /path --extract-metadata
"""

import os
import sys
import json
import hashlib
import argparse
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

# UTF-8 输出（跨平台兼容）
try:
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
    sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf-8', buffering=1)
except Exception:
    pass  # 某些环境不支持重设 stdout

# ============================================================
# 配置：文件分类（通用，不含用户特定路径）
# ============================================================

ONTOLOGY_DIR = os.path.dirname(os.path.abspath(__file__))
GRAPH_FILE = os.path.join(ONTOLOGY_DIR, "graph.jsonl")

# 知识文档（必定索引）
DOC_EXTS = {
    '.md', '.txt', '.docx', '.doc', '.pdf', '.rtf',
    '.xlsx', '.xls', '.pptx', '.ppt', '.csv', '.tsv',
    '.wps', '.et', '.dps',          # WPS Office 格式（文档/表格/演示）
    '.pages', '.numbers', '.key',   # macOS 办公格式
    '.odt', '.ods', '.odp',         # OpenDocument 格式
}

# 结构化定义文件（选择性索引）
SCHEMA_EXTS = {'.sql', '.ddl', '.yaml', '.yml', '.json', '.xml', '.graphql', '.proto'}

# 代码文件（只统计，不逐个索引）
CODE_EXTS = {
    '.py', '.js', '.ts', '.tsx', '.jsx', '.html', '.htm', '.css', '.scss',
    '.go', '.rs', '.java', '.kt', '.swift', '.c', '.cpp', '.h', '.hpp',
    '.rb', '.php', '.lua', '.r', '.R', '.jl', '.scala',
    '.sh', '.bash', '.zsh', '.fish', '.bat', '.ps1', '.cmd',
    '.toml', '.ini', '.cfg', '.conf', '.env.example',
    '.vue', '.svelte', '.astro',
}

# ============================================================
# 跳过规则（通用模式，不含用户特定目录名）
# ============================================================

# 跳过的目录名（精确匹配，全小写比较）
SKIP_DIR_NAMES = {
    # 包管理器依赖
    'node_modules', '__pycache__', 'site-packages',
    '.venv', 'venv', 'env', '.env',
    '.tox', '.nox', 'vendor', '.bundle',
    # 构建产物
    'dist', 'build', 'out', 'output', '_build',
    '.next', '.nuxt', '.output', '.svelte-kit',
    'target',  # Rust/Maven
    # 缓存
    '.cache', '.npm', '.yarn', '.pnpm-store', 'bun-cache',
    '.gradle', '.m2', '.cargo',
    # IDE 和工具
    '.git', '.svn', '.hg',
    '.idea', '.vscode', '.vs', '.fleet',
    # 系统
    '$recycle.bin', 'system volume information',
    '.trash', '.trashes',
}

# 跳过的路径片段（包含即跳过整个子树，小写比较）
SKIP_PATH_PATTERNS = [
    # 虚拟环境（各种命名）
    '/venv/', '/virtualenv/', '/site-packages/',
    '/.staging',
    # IM 缓存（通用模式，不限定具体 IM 软件）
    '/gamecaches/', '/appcache/', '/miniapp/',
    # 系统缓存（通用）
    '/cache/', '/caches/', '/tmp/', '/temp/',
    # 应用数据（通常不含用户知识）
    '/appdata/', '/application data/',
]

# 跳过的文件名（精确匹配）
SKIP_FILE_NAMES = {
    # 包管理器锁文件
    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'bun.lockb',
    'cargo.lock', 'poetry.lock', 'pipfile.lock', 'composer.lock',
    'gemfile.lock', 'flake.lock',
    # 系统文件
    '.ds_store', 'thumbs.db', 'desktop.ini', 'ehthumbs.db',
    # 编辑器临时文件
    '.swp', '.swo', '.swn',
}

# JSON 文件中跳过的（开发配置，不是知识内容）
SKIP_JSON_NAMES = {
    'package.json', 'tsconfig.json', 'jsconfig.json',
    '.eslintrc.json', '.prettierrc.json', 'tslint.json',
    'babel.config.json', '.babelrc',
    'launch.json', 'settings.json', 'extensions.json',
    'devcontainer.json', 'turbo.json', 'nx.json',
    'composer.json', 'deno.json',
}

# ============================================================
# 项目标记文件（用于检测项目边界）
# ============================================================

PROJECT_MARKERS = {
    # 文档项目
    'readme.md', 'readme', 'readme.txt', 'readme.rst',
    'claude.md', 'agents.md', 'gemini.md',
    'index.md', 'index.html',
    # 代码项目
    'package.json', 'cargo.toml', 'go.mod', 'pyproject.toml',
    'setup.py', 'setup.cfg', 'pom.xml', 'build.gradle',
    'makefile', 'cmakelists.txt', 'meson.build',
    'gemfile', 'requirements.txt',
    '.git',
}

# ============================================================
# 命名空间推断（通用逻辑，无硬编码映射）
# ============================================================

def load_namespace_rules(config_path):
    """从 YAML 配置文件加载自定义命名空间规则。"""
    if not config_path or not os.path.exists(config_path):
        return {}, set()
    try:
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = yaml.safe_load(f) or {}
        ns_map = cfg.get('namespace_map', {})
        expand = set(cfg.get('expand_children', []))
        return ns_map, expand
    except ImportError:
        print("[WARN] pyyaml 未安装，跳过配置文件加载。pip install pyyaml")
        return {}, set()


def safe_name(dirname):
    """将目录名转为安全的命名空间段。"""
    return dirname.lower().replace(' ', '-').replace('_', '-')


def detect_project_boundary(dirpath):
    """检测目录是否是一个项目的根目录。"""
    try:
        entries = {e.lower() for e in os.listdir(dirpath)}
    except OSError:
        return False
    return bool(entries & PROJECT_MARKERS)


class NamespaceInferrer:
    """通用命名空间推断器。"""

    def __init__(self, scan_root, ns_map=None, expand_children=None):
        self.scan_root = os.path.abspath(scan_root)
        self.ns_map = ns_map or {}          # 用户自定义映射
        self.expand = expand_children or set()  # 需要展开子目录的顶层目录
        self._project_cache = {}

    def infer(self, filepath):
        """推断文件的命名空间。"""
        rel = os.path.relpath(filepath, self.scan_root).replace('\\', '/')
        parts = rel.split('/')

        if len(parts) < 2:
            return 'uncategorized'

        top_dir = parts[0]

        # 1. 用户自定义映射优先
        if top_dir in self.ns_map:
            ns = self.ns_map[top_dir]
            if top_dir in self.expand and len(parts) >= 3:
                return f"{ns}/{safe_name(parts[1])}"
            return ns

        # 2. 自动推断：检测项目边界
        #    向下查找最近的项目标记，确定项目层级
        best_project_depth = 1  # 默认取第一层为项目
        for depth in range(1, min(len(parts), 4)):  # 最多看3层
            candidate = os.path.join(self.scan_root, *parts[:depth])
            if candidate not in self._project_cache:
                self._project_cache[candidate] = detect_project_boundary(candidate)
            if self._project_cache[candidate]:
                best_project_depth = depth

        # 用检测到的项目层级构建命名空间
        ns_parts = [safe_name(p) for p in parts[:best_project_depth]]
        return '/'.join(ns_parts)

    def infer_project_name(self, dirpath):
        """推断项目名称。"""
        rel = os.path.relpath(dirpath, self.scan_root).replace('\\', '/')
        parts = rel.split('/')
        # 返回最深的有意义的目录名
        for i in range(min(len(parts), 3) - 1, -1, -1):
            candidate = os.path.join(self.scan_root, *parts[:i+1])
            if detect_project_boundary(candidate):
                return parts[i]
        return parts[0]


# ============================================================
# 文件分类
# ============================================================

def classify_file(filepath):
    """分类文件，返回 'doc' | 'schema' | 'code' | None。"""
    name = os.path.basename(filepath).lower()

    if name in SKIP_FILE_NAMES:
        return None

    # 跳过隐藏文件（以 . 开头，但不是 .md 等有效扩展名的文件）
    if name.startswith('.') and not any(name.endswith(ext) for ext in DOC_EXTS | SCHEMA_EXTS):
        return None

    ext = os.path.splitext(name)[1].lower()

    if ext in DOC_EXTS:
        return 'doc'

    if ext in SCHEMA_EXTS:
        if ext == '.json' and name in SKIP_JSON_NAMES:
            return None
        return 'schema'

    if ext in CODE_EXTS:
        return 'code'

    return None


def file_title(filepath):
    """从文件名提取标题。"""
    name = os.path.basename(filepath)
    title, _ = os.path.splitext(name)
    return title


# ============================================================
# 元数据提取（可选功能）
# ============================================================

def extract_docx_metadata(filepath):
    """从 .docx 文件提取作者/标题等元数据。需要 python-docx。"""
    try:
        from docx import Document
        doc = Document(filepath)
        props = doc.core_properties
        meta = {}
        if props.author:
            meta['author'] = props.author
        if props.title and props.title.strip():
            meta['doc_title'] = props.title.strip()
        if props.subject:
            meta['subject'] = props.subject
        if props.keywords:
            meta['keywords'] = props.keywords
        return meta
    except Exception:
        return {}


def extract_pdf_metadata(filepath):
    """从 .pdf 文件提取元数据。需要 PyMuPDF。"""
    try:
        import fitz
        doc = fitz.open(filepath)
        meta = doc.metadata or {}
        result = {}
        if meta.get('author'):
            result['author'] = meta['author']
        if meta.get('title') and meta['title'].strip():
            result['doc_title'] = meta['title'].strip()
        if meta.get('subject'):
            result['subject'] = meta['subject']
        if meta.get('keywords'):
            result['keywords'] = meta['keywords']
        doc.close()
        return result
    except Exception:
        return {}


# ============================================================
# 重复检测
# ============================================================

class DuplicateDetector:
    """基于文件名+大小的轻量级重复检测。"""

    def __init__(self):
        self._seen = {}  # (filename, size) → first_path
        self.duplicates = []

    def check(self, filepath, size_bytes):
        """返回 True 如果文件疑似重复。"""
        key = (os.path.basename(filepath).lower(), size_bytes)
        if key in self._seen:
            self.duplicates.append((filepath, self._seen[key]))
            return True
        self._seen[key] = filepath
        return False


# ============================================================
# 实体构建
# ============================================================

def make_entity(entity_id, entity_type, graph, source, properties, labels=None, relations=None):
    """构建一条 graph.jsonl 记录。"""
    now = datetime.now(timezone.utc).isoformat()
    return {
        "op": "create",
        "ts": now,
        "entity": {
            "id": entity_id,
            "type": entity_type,
            "graph": graph,
            "labels": labels or [],
            "source": source,
            "properties": properties,
            "relations": relations or [],
            "created_at": now,
        }
    }


# ============================================================
# 扫描器
# ============================================================

class FileScanner:
    def __init__(self, scan_root, dry_run=False, extract_metadata=False,
                 ns_map=None, expand_children=None, skip_duplicates=True):
        self.scan_root = os.path.abspath(scan_root)
        self.dry_run = dry_run
        self.extract_metadata = extract_metadata
        self.skip_duplicates = skip_duplicates
        self.scan_id = f"scan-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        self.ns_inferrer = NamespaceInferrer(self.scan_root, ns_map, expand_children)
        self.dup_detector = DuplicateDetector()

        self.entities = []
        self.projects = {}

        self.stats = {
            'dirs_scanned': 0,
            'dirs_skipped': 0,
            'files_doc': 0,
            'files_schema': 0,
            'files_code': 0,
            'files_skipped': 0,
            'files_duplicate': 0,
            'metadata_extracted': 0,
        }

        self._doc_counter = 0
        self._project_counter = 0

    def _next_doc_id(self):
        self._doc_counter += 1
        return f"doc-{self._doc_counter:05d}"

    def _next_project_id(self):
        self._project_counter += 1
        return f"project-{self._project_counter:03d}"

    def _should_skip_dir(self, dirname):
        """目录名是否应跳过。"""
        low = dirname.lower()
        return (low in SKIP_DIR_NAMES
                or low.startswith('.')
                or low.endswith('.egg-info')
                or low.endswith('.dist-info'))

    def _should_skip_path(self, path):
        """路径是否包含应跳过的模式。"""
        normalized = path.replace('\\', '/').lower()
        return any(p in normalized for p in SKIP_PATH_PATTERNS)

    def scan(self):
        """执行扫描。"""
        print(f"扫描根目录: {self.scan_root}")
        print(f"扫描ID: {self.scan_id}")
        if self.extract_metadata:
            print(f"元数据提取: 已启用")
        print()

        source = {
            "type": "scan",
            "scan_id": self.scan_id,
            "target": "self",
            "path": self.scan_root.replace('\\', '/'),
        }

        for root, dirs, files in os.walk(self.scan_root):
            # 过滤目录
            original_count = len(dirs)
            dirs[:] = [d for d in dirs if not self._should_skip_dir(d)]
            self.stats['dirs_skipped'] += original_count - len(dirs)
            self.stats['dirs_scanned'] += 1

            if self._should_skip_path(root):
                dirs.clear()
                continue

            for filename in files:
                filepath = os.path.join(root, filename)
                category = classify_file(filepath)

                if category is None:
                    self.stats['files_skipped'] += 1
                    continue

                # 获取文件大小
                try:
                    size_bytes = os.path.getsize(filepath)
                except OSError:
                    self.stats['files_skipped'] += 1
                    continue

                # 重复检测
                if self.skip_duplicates and self.dup_detector.check(filepath, size_bytes):
                    self.stats['files_duplicate'] += 1
                    self.stats['files_skipped'] += 1
                    continue

                ns = self.ns_inferrer.infer(filepath)
                proj_name = self.ns_inferrer.infer_project_name(root)

                # 收集项目信息
                if ns not in self.projects:
                    self.projects[ns] = {
                        'name': proj_name,
                        'path': root.replace('\\', '/'),
                        'doc_count': 0,
                        'schema_count': 0,
                        'code_count': 0,
                    }

                if category == 'doc':
                    self.stats['files_doc'] += 1
                    self.projects[ns]['doc_count'] += 1
                    self._create_document(filepath, ns, source, size_bytes)
                elif category == 'schema':
                    self.stats['files_schema'] += 1
                    self.projects[ns]['schema_count'] += 1
                    self._create_document(filepath, ns, source, size_bytes)
                elif category == 'code':
                    self.stats['files_code'] += 1
                    self.projects[ns]['code_count'] += 1

        self._create_projects(source)
        print(f"\n扫描完成。")
        self._print_stats()

    def _create_document(self, filepath, namespace, source, size_bytes):
        """为一个文件创建 Document 实体。"""
        ext = os.path.splitext(filepath)[1].lower().lstrip('.')
        size_kb = round(size_bytes / 1024, 1)

        try:
            modified = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d')
        except OSError:
            modified = "unknown"

        props = {
            "title": file_title(filepath),
            "path": filepath.replace('\\', '/'),
            "format": ext if ext else "unknown",
            "size_kb": size_kb,
            "modified": modified,
        }

        # 可选：提取 .docx/.pdf 元数据
        if self.extract_metadata:
            meta = {}
            if ext == 'docx':
                meta = extract_docx_metadata(filepath)
            elif ext == 'pdf':
                meta = extract_pdf_metadata(filepath)
            if meta:
                props['metadata'] = meta
                self.stats['metadata_extracted'] += 1

        entity = make_entity(
            entity_id=self._next_doc_id(),
            entity_type="Document",
            graph=namespace,
            source=source,
            properties=props,
        )
        self.entities.append(entity)

    def _create_projects(self, source):
        """从收集的目录信息创建 Project 实体。"""
        for ns, info in sorted(self.projects.items()):
            total = info['doc_count'] + info['schema_count'] + info['code_count']
            if total == 0:
                continue
            entity = make_entity(
                entity_id=self._next_project_id(),
                entity_type="Project",
                graph=ns,
                source=source,
                properties={
                    "name": info['name'],
                    "status": "active",
                    "path": info['path'],
                    "doc_count": info['doc_count'],
                    "schema_count": info['schema_count'],
                    "code_count": info['code_count'],
                },
            )
            self.entities.append(entity)

    def _print_stats(self):
        """打印扫描统计。"""
        s = self.stats
        total_indexed = s['files_doc'] + s['files_schema']
        total_all = total_indexed + s['files_code'] + s['files_skipped']

        print(f"\n{'='*60}")
        print(f"扫描统计")
        print(f"{'='*60}")
        print(f"目录: 扫描 {s['dirs_scanned']}, 跳过 {s['dirs_skipped']}")
        print(f"文件总计: {total_all}")
        print(f"  文档文件 (已索引):  {s['files_doc']}")
        print(f"  Schema文件 (已索引): {s['files_schema']}")
        print(f"  代码文件 (仅统计):  {s['files_code']}")
        print(f"  跳过:               {s['files_skipped']}")
        if s['files_duplicate'] > 0:
            print(f"  其中重复文件:       {s['files_duplicate']}")
        if s['metadata_extracted'] > 0:
            print(f"  元数据提取:         {s['metadata_extracted']}")
        print(f"\n实体生成:")
        print(f"  Document 实体: {self._doc_counter}")
        print(f"  Project 实体:  {self._project_counter}")
        print(f"  总计:          {len(self.entities)}")

        # 按命名空间统计
        ns_stats = defaultdict(lambda: {'docs': 0, 'schemas': 0, 'code': 0})
        for ns, info in self.projects.items():
            ns_stats[ns]['docs'] = info['doc_count']
            ns_stats[ns]['schemas'] = info['schema_count']
            ns_stats[ns]['code'] = info['code_count']

        print(f"\n{'命名空间':<45s} {'文档':>6s} {'Schema':>8s} {'代码':>6s}")
        print(f"{'-'*45} {'-'*6} {'-'*8} {'-'*6}")
        for ns in sorted(ns_stats.keys()):
            info = ns_stats[ns]
            total = info['docs'] + info['schemas'] + info['code']
            if total > 0:
                print(f"{ns:<45s} {info['docs']:>6d} {info['schemas']:>8d} {info['code']:>6d}")

        # 报告重复文件
        if self.dup_detector.duplicates:
            print(f"\n疑似重复文件 (前10条):")
            for dup, orig in self.dup_detector.duplicates[:10]:
                print(f"  {os.path.basename(dup)}")
                print(f"    ← {orig}")
                print(f"    → {dup}")

    def write_output(self):
        """写入 graph.jsonl。"""
        if self.dry_run:
            print(f"\n[DRY RUN] 跳过写入。共 {len(self.entities)} 条实体待写入 {GRAPH_FILE}")
            return

        write_errors = 0
        with open(GRAPH_FILE, 'a', encoding='utf-8') as f:
            for entity in self.entities:
                try:
                    line = json.dumps(entity, ensure_ascii=False)
                    # 清理 surrogate 字符（Windows 文件名偶尔包含）
                    line = line.encode('utf-8', errors='surrogateescape').decode('utf-8', errors='replace')
                    f.write(line + '\n')
                except (UnicodeEncodeError, UnicodeDecodeError):
                    write_errors += 1
        if write_errors:
            print(f"  编码错误跳过: {write_errors}")

        print(f"\n已写入 {len(self.entities)} 条实体到 {GRAPH_FILE}")
        size_kb = os.path.getsize(GRAPH_FILE) / 1024
        print(f"文件大小: {size_kb:.1f} KB")


# ============================================================
# 主入口
# ============================================================

def main():
    global GRAPH_FILE

    parser = argparse.ArgumentParser(
        description="Personal Knowledge Graph - Filesystem Scanner (Step 1)",
        epilog="""
示例:
  python scan_filesystem.py --root ~/Documents
  python scan_filesystem.py --root D:/ --config namespace_rules.yaml
  python scan_filesystem.py --root /home/user --extract-metadata --dry-run
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('--root', required=True, help='扫描根目录（必需）')
    parser.add_argument('--config', help='命名空间规则配置文件（YAML，可选）')
    parser.add_argument('--dry-run', action='store_true', help='只统计不写入')
    parser.add_argument('--extract-metadata', action='store_true',
                        help='从 .docx/.pdf 提取作者/标题等元数据（需要 python-docx 和 PyMuPDF）')
    parser.add_argument('--no-dedup', action='store_true', help='禁用重复文件检测')
    parser.add_argument('--output', help=f'输出文件路径（默认: {GRAPH_FILE}）')
    args = parser.parse_args()

    if args.output:
        GRAPH_FILE = args.output

    ns_map, expand = load_namespace_rules(args.config)

    scanner = FileScanner(
        scan_root=args.root,
        dry_run=args.dry_run,
        extract_metadata=args.extract_metadata,
        ns_map=ns_map,
        expand_children=expand,
        skip_duplicates=not args.no_dedup,
    )
    scanner.scan()
    scanner.write_output()


if __name__ == '__main__':
    main()
