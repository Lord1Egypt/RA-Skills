"""知识库扫描范围限定（policy）—— 单一事实来源

背景（2026-11-05 实测事故）：
  一个 OCR 影子副本树（knowledge/知识库/，863 份 .md）被整体放进 knowledge/，
  导致 249 份「原件早已分析过的影子」重新入队 → 同一文档被分析两遍。
  该目录是 hermes pathmove 误放到 knowledge/ 下的（应在外层 knowledgehub/），已删除。

设计要点（v1.4.12 简化版）：
  1. **扫描范围 = 目录白名单，且在 glob 层限定**（不是扫完再过滤）。
     → 新增任何文件夹都**不会**进入分析范围，这是结构性保证，不靠过滤兜底。
     → 白名单与 AGENTS.md 声明的 knowledge/ 合法结构一一对应。
  2. **不做扩展名白名单** —— glob patterns 本身只匹配 10 种文档扩展名，重复限定是冗余。
  3. **不做体积上限** —— 实测 50MB 上限会误伤 17 份真实业务文件（研报/施工手册/PPT）。
  4. **不做影子兜底** —— knowledgehub/ 是另一套独立功能，与本 skill 无关联，不做耦合。
  5. 仅保留垃圾文件排除（.DS_Store / Office 锁文件 ~$），它们会被 glob 误匹配。

规则只在这里改一处。调用方（run_analysis.py / generate_catalog.py）不再各自实现扫描逻辑。
"""

import glob
import os

# ── 允许扫描的一级目录白名单（= AGENTS.md 声明的 knowledge/ 合法结构）────
SCAN_TOP_DIRS = (
    "Macro Financials",   # 投行研报
    "工程效能专家",        # 工程类知识
    "房产效能专家",        # 房产类知识
    "合同对比",            # 合同模板
    "文章目录",            # 文章索引
    "知识库搭建手册",      # 元知识（怎么搭KB）
    "临时",                # 临时参考
    "temp_docs",           # 待分析投递区
)

# ── 白名单根目录内的嵌套基础设施目录（永不含业务内容）────────────────
# 2026-11-06 补：glob 的 ** 不进入隐藏目录（.git/.venv/.analysis 等天然安全），
#   但「非隐藏的」基础设施目录会被扫到（node_modules/__pycache__/venv…）。
#   这些目录绝不含业务文档，排除它们不丢任何内容。
EXCLUDED_NESTED = (
    "node_modules", "__pycache__", "venv", "env", "site-packages",
    "dist-info", "eggs",
)

# ── 可被 glob 误匹配的垃圾文件 ────────────────────────────────────────
JUNK_NAMES = (".DS_Store", "Thumbs.db", "desktop.ini")
JUNK_PREFIXES = ("~$", ".~")   # Office/WPS 锁文件

# ── 文档扩展名（glob patterns）────────────────────────────────────────
DOC_PATTERNS = (
    "**/*.pdf", "**/*.doc", "**/*.docx",
    "**/*.xls", "**/*.xlsx", "**/*.ppt", "**/*.pptx",
    "**/*.md", "**/*.csv", "**/*.txt",
)


def within_knowledge(abs_path, knowledge_dir):
    """路径是否真在 knowledge/ 之内（realpath 消解符号链接后判定）。

    2026-11-06 修：ClawHub 扫描器指出「Automatic scanning can follow folder
    links outside the intended knowledge library, potentially including private
    text in scheduled Feishu messages」→ 实测 glob(recursive=True) 确实会跟随
    指向外部目录的符号链接。本函数用 realpath 两侧比对做兜底判定。
    """
    try:
        root = os.path.realpath(knowledge_dir)
        cand = os.path.realpath(abs_path)
    except (OSError, ValueError):
        return False
    return cand == root or cand.startswith(root + os.sep)


def scan_roots(knowledge_dir):
    """返回允许扫描的一级目录绝对路径列表（只存在的）。"""
    return [
        os.path.join(knowledge_dir, d)
        for d in SCAN_TOP_DIRS
        if os.path.isdir(os.path.join(knowledge_dir, d))
    ]


def is_junk(filename):
    """是否为垃圾/临时文件。"""
    if filename in JUNK_NAMES:
        return True
    return filename.startswith(JUNK_PREFIXES)


def scan_files(knowledge_dir):
    """扫描允许进入分析的文件 —— 唯一入口。

    扫描范围在 glob 层按目录白名单限定：白名单外的目录（含 .analysis/.trash/
    .interpret/.storage 以及任何未来新增的文件夹）根本不会被遍历。
    """
    files = []
    seen = set()
    for root in scan_roots(knowledge_dir):
        for pattern in DOC_PATTERNS:
            for f in glob.glob(os.path.join(root, pattern), recursive=True):
                if f in seen:
                    continue
                if is_junk(os.path.basename(f)):
                    continue
                # 符号链接防线：glob(recursive=True) 会跟随指向外部的目录链接
                # → 外部文件会进入分析队列并被推送飞书。用 realpath 兜底拒绝。
                if not within_knowledge(f, knowledge_dir):
                    continue
                # 嵌套基础设施目录排除：白名单根目录下的 node_modules/__pycache__/
                # venv 等永不含业务文档，扫进来只会污染分析队列。
                rel_parts = os.path.relpath(f, root).split(os.sep)[:-1]
                if any(part in EXCLUDED_NESTED for part in rel_parts):
                    continue
                seen.add(f)
                files.append(f)
    return files
