#!/usr/bin/env python3
"""
slice_generator.py — 切片计划生成器
用法: python slice_generator.py <source_file> <output_dir> [--json]

生成机械层面的切片计划（结构解析 + 拆分路由 + YAML 骨架）。
语义元数据（embedding_hint, qa_pairs, tags, hybrid_keywords）标为占位符，
由 Agent 在生成最终切片时填充。

输出:
  --json: JSON 格式的切片计划
  --stubs: 创建带 YAML 骨架的 .md 桩文件
  --report: 生成人类可读的拆分计划报告
"""

import sys
import os
import re
import json
import hashlib
from pathlib import Path
from collections import OrderedDict

# ── 可检查的 yaml 导入 ──
try:
    import yaml
except ImportError:
    yaml = None

# ── 分类路由关键词 ──
CATEGORY_KEYWORDS = {
    "api": [
        "函数", "方法", "接口", "API", "类定义", "签名", "参数列表",
        "返回值", "构造函数", "方法签名", "function", "method",
        "class", "def ", "async ", "返回类型", "回调函数",
        "模块", "module", "require", "export", "import",
        # 通用模块名
        "fs.", "path.", "http.", "https.", "os.", "crypto.",
        "buffer", "stream", "events", "process", "child_process",
        "net.", "dns.", "url.", "tls.", "zlib.", "readline.",
        # 语言通用 API 信号
        "模块系统", "模块化", "核心模块", "内置模块", "标准库",
        "命名空间", "包管理", "npm", "pipe", "promise",
        "异步", "sync", "await", "事件循环",
    ],
    "config": [
        "配置", "环境变量", "config", "参数说明", "启动参数",
        "配置文件", "yml", "yaml", "json配置", "环境", "env",
        "部署配置", "初始化参数", "全局设置"
    ],
    "guide": [
        "安装", "部署", "步骤", "教程", "操作指南", "故障排查",
        "如何", "使用方法", "快速开始", "入门", "示例",
        "实战", "演练", "配置指南", "常见问题", "FAQ"
    ],
    "concepts": [
        "概念", "原理", "架构", "设计", "模式", "概述",
        "介绍", "工作机制", "生命周期", "数据流", "核心思想",
        "定义", "术语", "设计理念", "抽象"
    ],
}


# ── 废弃命令检测 ──
DEPRECATED_COMMANDS = {
    'git stash save': 'git stash push -m',
    'git checkout --orphan': 'git switch --orphan',
}


def parse_headings(content: str) -> list:
    """解析所有 H1-H3 标题，返回 [(level, title, line_number), ...]"""
    headings = []
    for line_num, line in enumerate(content.split('\n'), 1):
        match = re.match(r'^(#{1,3})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            # 排除 URL 和空标题
            if '://' in title or not title:
                continue
            # 清理标题中的 Markdown 格式
            title = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', title)
            title = re.sub(r'`([^`]+)`', r'\1', title)
            headings.append((level, title, line_num))
    return headings


def find_atomic_units(content: str) -> list:
    """识别不可分割的代码块和表格，返回 [(type, start_line, end_line), ...]"""
    lines = content.split('\n')
    units = []
    in_code = False
    in_table = False
    code_start = 0
    table_start = 0

    for i, line in enumerate(lines, 1):
        # 代码块
        if line.strip().startswith('```'):
            if not in_code:
                in_code = True
                code_start = i
            else:
                in_code = False
                units.append(('code', code_start, i))
        # 表格
        elif re.match(r'^\|.+\|$', line.strip()):
            if not in_table:
                table_start = i
                in_table = True
        elif in_table:
            if not re.match(r'^\|.+\|$', line.strip()) and not re.match(r'^\|[\s\-\|:]+\|$', line.strip()):
                in_table = False
                units.append(('table', table_start, i - 1))

    # 收尾未闭合的表格
    if in_table:
        units.append(('table', table_start, len(lines)))

    return units


def classify_slice(title: str, content: str, headings_context: list) -> str:
    """根据标题和内容关键词分类"""
    title_lower = title.lower()
    content_lower = content.lower()[:500]

    scores = {cat: 0 for cat in CATEGORY_KEYWORDS}

    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower in title_lower:
                scores[cat] += 3
            if kw_lower in content_lower:
                scores[cat] += 1

    # 标题路径中包含关键词权重更高
    for level, h_title in headings_context:
        for cat, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in h_title.lower():
                    scores[cat] += 2

    # 代码块密度加权：代码块数 ≥ 1 且占比 > 10% → api +5
    code_block_count = len(re.findall(r'^```', content, re.MULTILINE)) // 2
    total_lines = content.count('\n') + 1
    if code_block_count >= 1:
        # 估算代码块内的实际代码行（取内容总行 80% 作为粗略上限）
        est_code_lines = min(code_block_count * 5, total_lines * 0.8)
        if est_code_lines / max(total_lines, 1) > 0.10:
            scores["api"] += 5

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "misc"


def estimate_tokens(text: str) -> int:
    """估算 token 数"""
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    code_chars = len(re.findall(r'`[^`]+`', text)) * 0.3
    total = chinese_chars * 1.5 + english_words * 1.3 + code_chars
    return int(total)


def split_sections(content: str) -> list:
    """
    按 H2 分节，然后在节内按语义边界进一步拆分。
    返回 [(section_title, section_content, start_line, heading_path), ...]
    每节不超过 700 字软上限。
    """
    lines = content.split('\n')
    headings = parse_headings(content)
    atomic_units = find_atomic_units(content)

    # 只取 H2 作为主拆分点
    h2_sections = [(level, title, line) for level, title, line in headings if level == 2]

    if not h2_sections:
        # 无 H2，整体作为一个节
        return [("全文", '\n'.join(lines), 1, ["全文"])]

    sections = []
    for i, (level, title, line) in enumerate(h2_sections):
        start = line
        end = h2_sections[i + 1][2] - 1 if i + 1 < len(h2_sections) else len(lines)
        section_lines = lines[start - 1:end]
        section_text = '\n'.join(section_lines)

        # 构建标题路径
        path = [title]
        for l, t, ln in reversed(headings):
            if ln < line and l < level:
                path.insert(0, t)
                break

        # 按字数拆分
        subsections = split_by_word_limit(section_text, path, atomic_units, lines, start)
        sections.extend(subsections)

    return sections


def split_by_word_limit(text: str, path: list, atomic_units: list,
                        all_lines: list, global_start: int) -> list:
    """
    在节内按 H3 + 字数软上限拆分，带回溯保护。
    返回 [(title, content, start_line, heading_path), ...]
    """
    lines = text.split('\n')
    local_headings = [(0, '', 0)]  # dummy root

    for local_line, line in enumerate(lines, 1):
        match = re.match(r'^###\s+(.+)$', line)
        if match:
            local_headings.append((3, match.group(1).strip(), local_line))

    local_headings.append((0, '', len(lines) + 1))

    # 无 H3 → 整节作为一个切片
    if len(local_headings) <= 2:
        word_count = len(re.findall(r'[\u4e00-\u9fff]', text)) + len(re.findall(r'[a-zA-Z]+', text))
        if word_count == 0:
            return []
        if word_count <= 700:
            return [(path[-1], text, global_start, path)]
        chunks = split_by_paragraph(text, path, atomic_units, global_start)
        return chunks

    subsections = []
    for i in range(1, len(local_headings)):
        lvl, title, start = local_headings[i]
        end = local_headings[i + 1][2] - 1 if i + 1 < len(local_headings) else len(lines)

        if i == 1 and not title:
            # 第一个 dummy heading, 合并到下一个
            continue

        sub_lines = lines[start - 1:end]
        sub_text = '\n'.join(sub_lines)
        word_count = len(re.findall(r'[\u4e00-\u9fff]', sub_text)) + len(re.findall(r'[a-zA-Z]+', sub_text))

        if word_count == 0:
            continue

        sub_path = path + [title] if title else path

        if word_count <= 700:
            subsections.append((title or path[-1], sub_text, global_start + start - 1, sub_path))
        else:
            # 超限：按空行段落边界拆分
            chunks = split_by_paragraph(sub_text, sub_path, atomic_units, global_start + start - 1)
            subsections.extend(chunks)

    return subsections


def split_by_paragraph(text: str, path: list, atomic_units: list, global_start: int) -> list:
    """按空行段落边界拆分，保护代码块和表格不被截断"""
    paragraphs = re.split(r'\n\s*\n', text)
    chunks = []
    current_chunk = []
    current_words = 0

    for para in paragraphs:
        para_words = len(re.findall(r'[\u4e00-\u9fff]', para)) + len(re.findall(r'[a-zA-Z]+', para))

        if current_words + para_words > 700 and current_chunk:
            chunks.append(current_chunk)
            current_chunk = [para]
            current_words = para_words
        else:
            current_chunk.append(para)
            current_words += para_words

    if current_chunk:
        chunks.append(current_chunk)

    result = []
    for i, chunk in enumerate(chunks):
        chunk_text = '\n\n'.join(chunk)
        chunk_title = path[-1] if path else "节选"
        if len(chunks) > 1:
            chunk_title += f" ({i + 1}/{len(chunks)})"
        result.append((chunk_title, chunk_text, global_start, path))

    return result


def generate_yaml_skeleton(source_id: str, title: str, category: str,
                           index: int, version: str = "unknown",
                           is_deprecated: bool = False) -> str:
    """生成 YAML frontmatter 骨架（语义字段留空）"""
    status = "deprecated" if is_deprecated else "active"

    return f"""---
title: "{title}"
source_id: "{source_id}"
category: "{category}"
index: {index:03d}
version: "{version}"
status: "{status}"
tags: [TODO: 领域, TODO: 技术栈, TODO: 动作]
embedding_hint: "TODO: ≤200字纯语义摘要，必须包含至少1个原文实体"
structural_context: "TODO: 根章节 → 二级章节 → 本切片标题 :: 关系类型"
hybrid_keywords: ["TODO:3~7个", "至少2个原文直接提取"]
cross_refs:
  depends_on: []
  related_to: []
qa_pairs: []
multimodal_refs: []
human_review_required: true
---"""
    # Note: human_review_required defaults to true until Agent fills content


def find_deprecated_commands(content: str) -> list:
    """扫描废弃命令"""
    found = []
    for cmd, replacement in DEPRECATED_COMMANDS.items():
        if cmd in content:
            found.append({"command": cmd, "replacement": replacement})
    return found


def detect_multimodal(content: str) -> dict:
    """检测多模态内容"""
    images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
    tables = re.findall(r'^\|.+\|$', content, re.MULTILINE)
    mermaid = re.findall(r'```mermaid', content)
    formulas = re.findall(r'\$\$', content)

    return {
        "images": len(images),
        "tables": len([t for t in tables if re.match(r'^\|[\s\-:]+\|$', t) is None]),
        "mermaid_diagrams": len(mermaid),
        "latex_formulas": len(formulas) // 2,
        "total_multimodal": len(images) + len(tables) // 2 + len(mermaid) + len(formulas) // 2,
    }


def scan_existing_slices(output_dir: str, source_id: str) -> dict:
    """扫描输出目录中已存在且通过校验的切片，用于断点续传。
    
    返回:
      {
        "found": 已存在的切片文件名集合,
        "completed_indices": 已完成校验的索引号列表,
        "total_existing": 已存在文件总数 (含未校验),
        "skipped_reason": {filename: "missing_check"|"fatal_failed"|"no_yaml" 等}
      }
    """
    result = {
        "found": set(),
        "completed_indices": [],
        "total_existing": 0,
        "skipped": {},
    }
    
    target_dir = Path(output_dir) / source_id
    if not target_dir.exists():
        return result
    
    # 递归收集所有 .md 文件
    existing_files = list(target_dir.rglob("*.md"))
    result["total_existing"] = len(existing_files)
    
    for fp in existing_files:
        rel_name = str(fp.relative_to(target_dir))
        basename = fp.name  # 纯文件名，用于与计划中的 filename 匹配
        try:
            raw = fp.read_text(encoding='utf-8')
        except Exception:
            result["skipped"][rel_name] = "read_error"
            continue
        
        # 检查 SELF_CHECK 注释
        check_match = re.search(
            r'<!--\s*SELF_CHECK:(.*?)-->', raw, re.DOTALL
        )
        if not check_match:
            result["skipped"][rel_name] = "missing_check"
            continue
        
        check_text = check_match.group(1)
        
        # 提取 fatal_passed
        fatal_match = re.search(r'fatal_passed\s*=\s*(true|false)', check_text)
        if not fatal_match:
            result["skipped"][rel_name] = "no_fatal_flag"
            continue
        
        if fatal_match.group(1) == "true":
            result["found"].add(rel_name)
            result["found"].add(basename)  # 同时加入纯文件名
            # 提取 index
            idx_match = re.search(r'index:\s*(\d+)', raw)
            if idx_match:
                result["completed_indices"].append(int(idx_match.group(1)))
        else:
            result["skipped"][rel_name] = "fatal_failed"
    
    return result


def generate_plan(source_path: str, output_dir: str, resume: bool = False) -> dict:
    """生成完整切片计划"""
    source = Path(source_path)
    if not source.exists():
        return {"error": "source_not_found", "path": source_path}

    content = source.read_text(encoding='utf-8')

    source_id = source.stem

    # ── 断点续传：扫描已存在的切片 ──
    resume_info = None
    if resume:
        resume_info = scan_existing_slices(output_dir, source_id)
    else:
        resume_info = {"found": set(), "completed_indices": [], "total_existing": 0, "skipped": {}}

    # 提取版本信息
    version = "unknown"
    if yaml:
        parts = content.split('---')
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1])
                if isinstance(fm, dict):
                    version = str(fm.get('version', 'unknown'))
            except Exception:
                pass

    # 检查是否有多模态内容
    multimodal_info = detect_multimodal(content)

    # 拆分节
    sections = split_sections(content)

    # 为每个节生成切片计划
    slices = []
    categories_count = {}

    for i, (sec_title, sec_content, start_line, path) in enumerate(sections, 1):
        category = classify_slice(sec_title, sec_content, [
            (1, p) for p in path
        ])

        # 检查废弃命令
        deprecated = find_deprecated_commands(sec_content)
        is_deprecated = len(deprecated) > 0

        # 全路径标题
        full_title = ' > '.join(path)

        # 文件名
        safe_title = re.sub(r'[\\/:*?"<>|#\[\]()]', '', sec_title)[:30]
        filename = f"{category}_{i:03d}-{safe_title}.md"

        # 统计字数（中英统一口径）
        word_count = len(re.findall(r'[\u4e00-\u9fff]', sec_content)) + len(re.findall(r'[a-zA-Z]+', sec_content))
        code_lines = len(re.findall(r'^```', sec_content, re.MULTILINE)) // 2

        slices.append({
            "index": i,
            "category": category,
            "title": full_title,
            "filename": filename,
            "heading_path": path,
            "start_line": start_line,
            "word_count": word_count,
            "code_block_count": code_lines,
            "deprecated_commands": deprecated,
            "is_deprecated": is_deprecated,
            "content": sec_content,
            "version": version,
        })

        categories_count[category] = categories_count.get(category, 0) + 1

    # 应用降级策略：某分类切片 ≤ 2 且总字数 < 1500
    for cat, count in list(categories_count.items()):
        if count <= 2:
            total_words = sum(s["word_count"] for s in slices if s["category"] == cat)
            if total_words < 1500 and count <= 1:
                # 单切片不建子目录
                for s in slices:
                    if s["category"] == cat:
                        s["directory"] = ""
            elif total_words < 1500 and count == 2:
                # 两切片且总字数 < 1500 → 合并到根目录
                for s in slices:
                    if s["category"] == cat:
                        s["directory"] = ""

    # ── 断点续传：过滤已完成的切片 ──
    skipped_indices = set(resume_info.get("completed_indices", []))
    slices_all = slices  # 保留完整列表用于统计
    remaining_slices = []
    for s in slices:
        if resume and s["filename"] in resume_info["found"]:
            skipped_indices.add(s["index"])
            continue
        remaining_slices.append(s)
    
    if resume:
        slices = remaining_slices
        categories_count = {}
        for s in slices:
            categories_count[s["category"]] = categories_count.get(s["category"], 0) + 1

    plan = {
        "source_id": source_id,
        "source_path": str(source),
        "output_dir": str(output_dir),
        "version": version,
        "total_slices": len(slices),
        "total_words": sum(s["word_count"] for s in slices),
        "multimodal_info": multimodal_info,
        "categories": categories_count,
        "slices": [
            {
                k: v for k, v in s.items() if k != "content"
            }
            for s in slices
        ],
        # 断点续传信息
        "resume_info": {
            "enabled": resume,
            "skipped_count": len([s for s in slices_all if s["filename"] in resume_info["found"]]),
            "skipped_indices": sorted(skipped_indices),
            "remaining_count": len(slices),
            "unverifiable": resume_info.get("skipped", {}),
        } if resume else None,
    }

    return plan


def _patch_embedding_hint(filepath: str, slice_info: dict):
    """为桩文件填充基础的 embedding_hint，从标题+正文首段提取（≤80字）。
    
    仅在 hint 为 TEMPLATE_PLACEHOLDER 时替换，避免覆盖已人工填充的内容。
    正文优先从 slice_info['content'] 取，回退到文件内容提取（plan JSON 中 content 可能被排除）。
    """
    TEMPLATE_PLACEHOLDER = '"TODO: ≤200字纯语义摘要，必须包含至少1个原文实体"'
    
    # 提取标题
    title = slice_info.get("title", "")
    content = slice_info.get("content", "")
    
    # 如果 plan 中 content 被排除，从文件中提取正文
    if not content:
        try:
            raw = Path(filepath).read_text(encoding='utf-8')
        except Exception:
            return
        
        if TEMPLATE_PLACEHOLDER not in raw:
            return
        
        # 从文件正文中提取：跳过 YAML frontmatter 和标题行
        body = raw
        # 跳过 frontmatter
        parts = raw.split('---\n', 2)
        if len(parts) >= 3:
            body = parts[2]
        # 跳过标题行和模板头
        body = re.sub(r'^# .+\n', '', body, count=1)
        body = re.sub(r'\n> \[!INFO\].*\n', '\n', body, count=1)
        body = re.sub(r'^## 概念定义.*?(?=## 核心内容)', '', body, flags=re.DOTALL)
        body = re.sub(r'^## 使用场景.*?(?=## 核心内容)', '', body, flags=re.DOTALL)
        
        # 取「核心内容」段落
        core_match = re.search(r'## 核心内容\n(.*?)(?=\n## )', body, re.DOTALL)
        if core_match:
            content = core_match.group(1).strip()
        else:
            content = body.strip()
    else:
        try:
            raw = Path(filepath).read_text(encoding='utf-8')
        except Exception:
            return
        if TEMPLATE_PLACEHOLDER not in raw:
            return
    
    if not content:
        return
    
    # 清理常见模板标记
    clean = content.replace('\n', ' ').strip()
    # 取前 200 字符提取关键词
    first_section = clean[:200]
    
    # 构建基础 hint：标题关键词 + 正文首段摘要（≤80字）
    title_key = title.split(' > ')[-1] if ' > ' in title else title
    hint_text = f"{title_key}: {first_section}"
    # 限制 80 字（中文按字符算）
    if len(hint_text) > 80:
        hint_text = hint_text[:77] + "..."
    
    # 确保 JSON 安全
    hint_text = hint_text.replace('"', "'")
    
    new_raw = raw.replace(
        TEMPLATE_PLACEHOLDER,
        f'"{hint_text}"'
    )
    
    try:
        Path(filepath).write_text(new_raw, encoding='utf-8')
    except Exception:
        pass


def create_stub_files(plan: dict) -> list:
    """创建带 YAML 骨架的桩文件"""
    output_dir = Path(plan["output_dir"]) / plan["source_id"]
    created = []

    for slice_info in plan["slices"]:
        # 确定目录
        if slice_info.get("directory") is not None and slice_info["directory"] == "":
            # 降级：放在根目录
            slice_dir = output_dir
        else:
            cat = slice_info["category"]
            slice_dir = output_dir / cat

        slice_dir.mkdir(parents=True, exist_ok=True)

        filepath = slice_dir / slice_info["filename"]

        yaml_str = generate_yaml_skeleton(
            source_id=plan["source_id"],
            title=slice_info["title"],
            category=slice_info["category"],
            index=slice_info["index"],
            version=slice_info.get("version", "unknown"),
            is_deprecated=slice_info.get("is_deprecated", False),
        )

        content = f"""{yaml_str}

# {slice_info["title"]}

> [!INFO] 📄 来源：{plan["source_id"]}.md | 🏷️ 分类：{slice_info['category']} | 📅 待填充

## 概念定义
TODO: 1~3 句话回答"是什么"

## 使用场景
TODO: 适用于什么问题/场景

## 核心内容
TODO: 方法、步骤、配置、代码

{slice_info.get("content", "")}

## 注意事项
TODO: 限制条件、边界情况、常见陷阱

## 相关链接
TODO: 通过 cross_refs 链接到前置依赖和相关概念切片
"""

        filepath.write_text(content, encoding='utf-8')

        # ── embedding_hint 兜底：用标题+正文首段替换占位符 ──
        _patch_embedding_hint(str(filepath), slice_info)

        created.append(str(filepath))

    return created


def renumber_indices(output_dir: str, dry_run: bool = False) -> dict:
    """全局索引重排：扫描输出目录，按 source_id + category 分组，
    重编号索引为连续整数，同步更新文件名和 YAML index 字段。
    
    Args:
        output_dir: 切片输出根目录
        dry_run: 仅预览，不实际修改文件
    
    Returns:
        {"renamed": [{old, new, reason}, ...], "total": int}
    """
    output = Path(output_dir)
    if not output.exists():
        return {"renamed": [], "total": 0, "error": "directory_not_found"}
    
    # 收集所有切片文件
    slices = []
    for fp in output.rglob("*.md"):
        if fp.name in ('SKILL.md', 'README.md', 'version_matrix.md', 
                       'batch_audit_report.md', 'retrieval_evaluation_report.md'):
            continue
        try:
            raw = fp.read_text(encoding='utf-8')
        except Exception:
            continue
        
        # 提取 YAML 元数据
        data = None
        parts = re.split(r'(?:^|\n)---[ \t]*\n', raw)
        for i in range(1, min(len(parts), 4)):
            block = parts[i].strip()
            if not block:
                continue
            try:
                parsed = yaml.safe_load(block)
                if isinstance(parsed, dict):
                    data = parsed
                    break
            except Exception:
                pass
        
        if not data or "title" not in data:
            continue
        
        slices.append({
            "path": str(fp),
            "dir": str(fp.parent),
            "filename": fp.name,
            "data": data,
            "raw": raw,
            "source_id": data.get("source_id", "unknown"),
            "category": data.get("category", "misc"),
            "index": int(data.get("index", 0)),  # 强制 int，防 YAML 前导零解析为 str
            "title": data.get("title", ""),
        })
    
    # 按 source_id + category 分组，按原 index 排序
    from collections import defaultdict
    groups = defaultdict(list)
    for s in slices:
        key = (s["source_id"], s["category"], s["dir"])
        groups[key].append(s)
    
    renamed = []
    
    for key, group in groups.items():
        # 按现有 index 排序
        group.sort(key=lambda x: x["index"])
        
        # 逐个重编号
        for new_idx, s in enumerate(group, 1):
            new_idx_padded = f"{new_idx:03d}"
            s_index = int(s["index"]) if not isinstance(s["index"], int) else s["index"]
            old_idx_padded = f"{s_index:03d}"
            
            if new_idx == s_index:
                continue  # 无需修改
            
            old_filepath = Path(s["path"])
            old_dir = old_filepath.parent
            
            # 构造新文件名：{category}_{newIndex}-{title}.md
            # 从旧文件名中提取标题部分（index 之后的-xxx）
            old_name = s["filename"]
            after_index = re.sub(rf'^{s["category"]}_{old_idx_padded}-', '', old_name)
            if after_index == old_name:
                # 尝试无类别前缀格式
                after_index = re.sub(rf'^{old_idx_padded}-', '', old_name)
                new_name = f"{new_idx_padded}-{after_index}"
            else:
                new_name = f"{s['category']}_{new_idx_padded}-{after_index}"
            
            new_filepath = old_dir / new_name
            
            # ── 更新文件内容中的 index 字段 ──
            new_raw = s["raw"]
            # 替换 YAML 中的 index 字段
            new_raw = re.sub(
                rf'^index:\s*{s["index"]}(\s*#.*)?$',
                f'index: {new_idx}',
                new_raw,
                flags=re.MULTILINE
            )
            
            rename_info = {
                "source_id": s["source_id"],
                "category": s["category"],
                "old_name": s["filename"],
                "new_name": new_name,
                "old_index": s["index"],
                "new_index": new_idx,
            }
            
            if not dry_run:
                try:
                    new_filepath.write_text(new_raw, encoding='utf-8')
                    # 删除旧文件（如果新旧文件名不同）：先 rename 为 .bak 再删
                    if old_name != new_name:
                        bak_path = old_filepath.with_suffix(old_filepath.suffix + '.bak')
                        try:
                            old_filepath.rename(bak_path)
                            bak_path.unlink()
                        except Exception:
                            pass
                except Exception as e:
                    rename_info["error"] = str(e)
            
            renamed.append(rename_info)
    
    return {"renamed": renamed, "total": len(renamed), "dry_run": dry_run}


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='切片计划生成器')
    parser.add_argument('source', nargs='?', help='源 Markdown 文件路径（--renumber 模式下可选）')
    parser.add_argument('output_dir', nargs='?', help='输出根目录（--renumber 模式下必选）')
    parser.add_argument('--json', action='store_true', help='输出 JSON 计划')
    parser.add_argument('--stubs', action='store_true', help='创建桩文件')
    parser.add_argument('--report', action='store_true', help='生成可读报告')
    parser.add_argument('--resume', action='store_true', help='断点续传：跳过已存在且通过校验的切片')
    parser.add_argument('--renumber', action='store_true', help='全局索引重排模式：扫描 output_dir 下所有切片，重编号索引')
    parser.add_argument('--dry-run', action='store_true', help='配合 --renumber，仅预览不实际修改')
    args = parser.parse_args()

    # ── 全局索引重排模式 ──
    if args.renumber:
        target_dir = args.output_dir or args.source  # 兼容 old: source 作 output_dir
        if not target_dir:
            print("ERROR: --renumber 需要指定切片目录路径")
            sys.exit(1)
        result = renumber_indices(target_dir, dry_run=args.dry_run)
        if result.get("error"):
            print(f"ERROR: {result['error']}")
            sys.exit(1)
        if result["dry_run"]:
            print(f"[DRY RUN] 将重排 {result['total']} 个文件:")
        else:
            print(f"[OK] 已重排 {result['total']} 个文件:")
        for r in result["renamed"]:
            err = f" (错误: {r['error']})" if r.get("error") else ""
            print(f"  {r['source_id']}/{r['category']}: "
                  f"{r['old_name']} (idx {r['old_index']}) → {r['new_name']} (idx {r['new_index']}){err}")
        sys.exit(0)

    if not args.source or not args.output_dir:
        parser.print_help()
        sys.exit(1)

    plan = generate_plan(args.source, args.output_dir, resume=args.resume)

    if plan.get("error"):
        print(f"ERROR: {plan['error']}: {plan.get('path')}")
        sys.exit(1)

    if args.stubs:
        created = create_stub_files(plan)
        print(f"创建 {len(created)} 个桩文件:")
        for f in created[:10]:
            print(f"  {f}")
        if len(created) > 10:
            print(f"  ... 共 {len(created)} 个")

    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    elif args.report:
        ri = plan.get("resume_info")
        if ri:
            print(f"=== 断点续传 ===")
            print(f"  已跳过: {ri['skipped_count']} 片 (索引: {ri['skipped_indices']})")
            print(f"  待生成: {ri['remaining_count']} 片")
            if ri.get("unverifiable"):
                print(f"  未校验文件:")
                for fn, reason in ri["unverifiable"].items():
                    print(f"    {fn} ({reason})")
            print()
        print(f"源文件: {plan['source_path']}")
        print(f"Source-ID: {plan['source_id']}")
        print(f"版本: {plan['version']}")
        print(f"总切片: {plan['total_slices']} | 总字数: {plan['total_words']}")
        print(f"分类分布: {plan['categories']}")
        if plan['multimodal_info']['total_multimodal'] > 0:
            print(f"多模态: 图片{plan['multimodal_info']['images']} 表格{plan['multimodal_info']['tables']} "
                  f"Mermaid{plan['multimodal_info']['mermaid_diagrams']} 公式{plan['multimodal_info']['latex_formulas']}")
        print()
        for s in plan['slices']:
            print(f"  {s['category']}_{s['index']:03d} | {s['word_count']}字 | {s['title'][:60]}")
            if s.get('deprecated_commands'):
                for dc in s['deprecated_commands']:
                    print(f"    ⚠ 废弃命令: {dc['command']} → {dc['replacement']}")
    else:
        print(f"计划生成完成: {plan['total_slices']} 个切片, {plan['total_words']} 字")
        print("使用 --stubs 创建桩文件, --json 输出 JSON, --report 打印报告")
