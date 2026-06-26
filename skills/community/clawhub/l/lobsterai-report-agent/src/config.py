"""
config.py - 路径配置与文件 I/O
===================================
所有路径均通过环境变量或 ~/.config/ 动态决定，不在 import 时执行 subprocess。
"""

import os, json as json_module
from typing import Dict, Any

# ============ 路径配置（惰性，不在 import 时执行 subprocess）============

CHARS_PER_PAGE = 950  # 每页字符数估算值


def _get_config_value(key: str, default: str) -> str:
    """优先读环境变量，否则用 default"""
    return os.environ.get(key) or default


def _default_chapters_dir() -> str:
    return os.path.join(os.path.expanduser("~"), ".config", "lobsterai-report-agent", "chapters")


def _default_output_dir() -> str:
    return os.path.join(os.path.expanduser("~"), ".config", "lobsterai-report-agent", "output")


def get_chapters_dir() -> str:
    """获取章节工作目录（可配置：环境变量 LOBAI_CHAPTERS_DIR）"""
    return _get_config_value("LOBAI_CHAPTERS_DIR", _default_chapters_dir())


def get_output_dir() -> str:
    """获取最终输出目录（可配置：环境变量 LOBAI_OUTPUT_DIR）"""
    return _get_config_value("LOBAI_OUTPUT_DIR", _default_output_dir())


# ---- 路径缓存（延迟到首次使用时）----
_paths_cache: Dict[str, str] = {}


def _load_paths() -> Dict[str, str]:
    """惰性构建所有路径，线程安全"""
    global _paths_cache
    if not _paths_cache:
        cd = get_chapters_dir()
        od = get_output_dir()
        os.makedirs(cd, exist_ok=True)
        os.makedirs(od, exist_ok=True)
        _paths_cache.update({
            'CHAPTERS_DIR': cd,
            'OUTPUT_DIR': od,
            'PLAN_FILE': os.path.join(cd, 'plan.json'),
            'PROGRESS_FILE': os.path.join(cd, 'progress.json'),
            'GLOSSARY_FILE': os.path.join(cd, 'glossary.json'),
            'REFERENCE_FILE': os.path.join(cd, 'reference_material.txt'),
            'OUTLINE_SNAPSHOT': os.path.join(cd, 'plan_outline_snapshot.md'),
            'CONFIG_FILE': os.path.join(cd, 'config.json'),
            'FINAL_DOC': os.path.join(od, '整合报告.docx'),
            'HASH_FILE': os.path.join(cd, 'content_hashes.json'),
            'MERMAID_TEMP': os.path.join(cd, 'mermaid_temp'),
            'MERMAID_PUPPETEER_CONFIG': os.path.join(cd, 'mermaid_temp', 'puppeteer_config.json'),
        })
    return _paths_cache


def _p(key: str) -> str:
    """取路径常量的简写"""
    return _load_paths()[key]


# ---- 兼容模块级属性的 __getattr__（支持 from config import CHAPTERS_DIR）----
def __getattr__(name: str):
    _paths = _load_paths()
    if name in _paths:
        return _paths[name]
    if name == 'CHARS_PER_PAGE':
        return CHARS_PER_PAGE
    raise AttributeError(f"module 'config' has no attribute '{name}'")


# ============ Mermaid CLI（惰性，不在 import 时执行）============

_mermaid_cli_cached: str = None


def get_mermaid_cli() -> str:
    """延迟查找 mmdc CLI，仅在首次需要渲染 mermaid 时调用"""
    global _mermaid_cli_cached
    if _mermaid_cli_cached is not None:
        return _mermaid_cli_cached
    import subprocess
    local_cli = os.path.join(os.path.dirname(__file__), 'node_modules', '@mermaid-js', 'mermaid-cli', 'src', 'cli.js')
    local_cli = os.path.normpath(local_cli)
    candidates = [
        ('local', [local_cli, '--version']),
        ('local_node', ['node', local_cli, '--version']),
        ('mmdc', ['mmdc', '--version']),
        ('npx_mmdc', ['npx', 'mmdc', '--version']),
    ]
    for name, cmd in candidates:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                _mermaid_cli_cached = local_cli if name in ('local', 'local_node') else cmd[0]
                return _mermaid_cli_cached
        except Exception:
            continue
    _mermaid_cli_cached = None
    return None


# ============ Config 文件读写 =============

def load_config() -> Dict[str, Any]:
    try:
        with open(_p('CONFIG_FILE'), 'r', encoding='utf-8') as f:
            return json_module.load(f)
    except Exception:
        pass
    return {
        "project_name": "", "topic": "", "audience": "",
        "doc_type": "可行性研究报告", "style": "专业严谨", "custom_constraints": ""
    }


def save_config(cfg: Dict[str, Any]) -> None:
    with open(_p('CONFIG_FILE'), 'w', encoding='utf-8') as f:
        json_module.dump(cfg, f, ensure_ascii=False, indent=2)


# ============ Plan 文件读写 =============

def load_plan() -> Dict[str, Any]:
    try:
        with open(_p('PLAN_FILE'), 'r', encoding='utf-8') as f:
            return json_module.load(f)
    except Exception:
        pass
    return make_default_plan()


def make_default_plan() -> Dict[str, Any]:
    return {"project_name": "", "chapters": []}


def save_plan(plan: Dict[str, Any]) -> None:
    with open(_p('PLAN_FILE'), 'w', encoding='utf-8') as f:
        json_module.dump(plan, f, ensure_ascii=False, indent=2)


# ============ Glossary 文件读写 =============

def generate_glossary(txt_files=None, ref_text: str = "", max_terms: int = 80) -> Dict[str, Any]:
    """从参考资料和章节内容中生成术语表"""
    import re
    all_terms: Dict[str, int] = {}

    stopwords = {
        '以及', '包括', '可以', '通过', '根据', '按照', '为了', '由于', '其中',
        '其他', '相关', '以上', '以下', '对于', '并且', '或者', '等等',
        '本项目', '本公司', '本系统', '本章', '本节', '本文', '本案',
        '进行', '完成', '实现', '提供', '使用', '管理', '系统', '建设',
        '方案', '项目', '数据', '平台', '技术', '功能', '模块'
    }

    def extract_from_text(text: str):
        pattern = re.compile(r'[\u4e00-\u9fff]{4,}')
        for w in pattern.findall(text):
            if w not in stopwords and len(w) >= 4:
                all_terms[w] = all_terms.get(w, 0) + 1

    if ref_text:
        extract_from_text(ref_text)

    if txt_files:
        for f in (txt_files or []):
            try:
                extract_from_text(open(f, 'r', encoding='utf-8').read())
            except Exception:
                continue

    sorted_terms = sorted(all_terms.items(), key=lambda x: -x[1])[:max_terms]
    glossary = {
        "generated_at": _timestamp(),
        "total_ref_chars": len(ref_text),
        "terms": [{"term": t, "count": c} for t, c in sorted_terms]
    }
    with open(_p('GLOSSARY_FILE'), 'w', encoding='utf-8') as f:
        json_module.dump(glossary, f, ensure_ascii=False, indent=2)
    print(f"[GLOSSARY] 术语表已生成: {_p('GLOSSARY_FILE')}（共 {len(sorted_terms)} 个术语）")
    return glossary


def load_glossary() -> Dict[str, Any]:
    try:
        with open(_p('GLOSSARY_FILE'), 'r', encoding='utf-8') as f:
            return json_module.load(f)
    except Exception:
        return {"terms": []}


def glossary_to_prompt_text(glossary: Dict[str, Any], max_terms: int = 30) -> str:
    terms = glossary.get('terms', [])
    if not terms:
        return "（术语表暂无数据，完成 Batch A 后自动生成）"
    display = terms[:max_terms]
    lines = [f"- {t['term']}（出现{t['count']}次）" for t in display]
    suffix = f"\n（共 {len(terms)} 个术语，仅展示前 {max_terms} 个）" if len(terms) > max_terms else ""
    return '\n'.join(lines) + suffix


# ============ Reference 文件读写 =============

def load_reference() -> str:
    try:
        with open(_p('REFERENCE_FILE'), 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ""


def save_reference(text: str) -> None:
    with open(_p('REFERENCE_FILE'), 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"[REF] 参考资料已保存，共 {len(text)} 字符")


# ============ Progress 文件读写 =============

def load_progress() -> Dict[str, Any]:
    try:
        with open(_p('PROGRESS_FILE'), 'r', encoding='utf-8') as f:
            return json_module.load(f)
    except Exception:
        return {"total": 0, "completed": 0, "batches": [], "current": ""}


# ============ 大纲快照 =============

def save_outline_snapshot(plan: Dict[str, Any]) -> None:
    from datetime import datetime
    lines = [f"# 文档大纲快照（{datetime.now().strftime('%Y-%m-%d %H:%M')}）"]
    lines.append(f"\n项目：{plan.get('project_name', '未知项目')}\n")
    for ch in plan.get('chapters', []):
        lines.append(
            f"第{ch.get('seq','?')}章 | {ch.get('title','')} | "
            f"Batch {ch.get('batch','')} | 约{ch.get('word_count',0)}字 | "
            f"依赖:{ch.get('dependencies',[])}"
        )
    with open(_p('OUTLINE_SNAPSHOT'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"[SNAPSHOT] 大纲快照已保存: {_p('OUTLINE_SNAPSHOT')}")


def save_batch_snapshot(batch_label: str, batch_chapters) -> None:
    from datetime import datetime
    snapshot_file = f"{_p('CHAPTERS_DIR')}/snapshot_{batch_label}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    lines = [f"# {batch_label} 快照（{datetime.now().strftime('%Y-%m-%d %H:%M')}）"]
    for seq, fname, title, content, _ in batch_chapters:
        lines.append(f"\n---\n## 第{seq}章 {title}\n")
        preview = content[:300].replace('\n', ' ').strip()
        lines.append(f"[预览] {preview}...")
    with open(snapshot_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"[SNAPSHOT] 批次快照已保存: {snapshot_file}")


# ============ 内部工具 =============

def _timestamp() -> str:
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
