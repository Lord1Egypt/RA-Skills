#!/usr/bin/env python3
"""
validate_slice.py — 单切片完整性校验与自检注释写入
用法: python validate_slice.py <slice_file_path> [--fix]
      --fix: 修复模式，将校验结果写入文件尾部的 SELF_CHECK 注释

必填字段 (14个):
  title, source_id, category, index, version, status, tags,
  embedding_hint, structural_context, hybrid_keywords, cross_refs,
  qa_pairs, multimodal_refs, human_review_required
"""

import sys
import os
import re
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    print("错误：缺少 pyyaml 依赖。请执行: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# ── 14 个必填 YAML 字段 ──
REQUIRED_FIELDS = [
    "title", "source_id", "category", "index", "version", "status",
    "tags", "embedding_hint", "structural_context", "hybrid_keywords",
    "cross_refs", "qa_pairs", "multimodal_refs", "human_review_required"
]

# ── 泛化词黑名单 ──
GENERIC_KEYWORDS = {
    "配置", "方法", "使用", "设置", "功能", "参数", "选项",
    "说明", "介绍", "操作", "步骤", "示例", "参考", "概述", "简介", "注意"
}

# ── 废弃命令模式 ──
DEPRECATED_PATTERNS = [
    (r'git\s+stash\s+save', 'git stash push -m'),
    (r'git\s+checkout\s+--orphan', 'git switch --orphan'),
    (r'docker\s+rm\s+-f\b', 'docker rm -f (use with caution)'),
]


def extract_real_yaml(content: str) -> tuple:
    """
    提取真正的元数据 YAML 块。
    文件可能有两个 --- 块：第一个是 AIGC 水印，第二个才是标准元数据。
    返回 (yaml_text, start_pos, end_pos) 或 (None, -1, -1)
    """
    parts = content.split('---')
    if len(parts) < 3:
        return None, -1, -1

    # 跳过第一个块（可能是 AIGC 水印或空）
    candidates = []
    for i in range(1, len(parts)):
        block = parts[i].strip()
        if not block:
            continue
        candidates.append((i, block))

    # 找包含 title 或 name 的块
    for idx, block in candidates:
        if 'title:' in block or ('name:' in block and 'knowledge-engineering' not in block):
            # 计算在原文中的位置
            prefix = '---'.join(parts[:idx]) + '---'
            start = len(prefix) + 1
            end = start + len(block)
            return block, start, end

    # 回退：返回第一个非空块
    if candidates:
        idx, block = candidates[0]
        prefix = '---'.join(parts[:idx]) + '---'
        start = len(prefix) + 1
        end = start + len(block)
        return block, start, end

    return None, -1, -1


def parse_yaml_safe(yaml_text: str) -> dict:
    """安全解析 YAML，返回 dict 或空 dict"""
    try:
        data = yaml.safe_load(yaml_text)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def check_field_completeness(data: dict) -> dict:
    """检查 14 个必填字段"""
    present = []
    missing = []

    for field in REQUIRED_FIELDS:
        if field in data and data[field] is not None:
            if isinstance(data[field], str) and not data[field].strip():
                missing.append(f"{field}(空值)")
            else:
                present.append(field)
        else:
            missing.append(field)

    return {
        "present": present,
        "missing": missing,
        "all_present": len(missing) == 0
    }


def check_content_rules(content: str, data: dict) -> list:
    """检查内容质量规则，返回警告列表"""
    warnings = []

    # 标题格式检查
    heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if heading_match:
        title = heading_match.group(1)
        if ' > ' not in title and not title.startswith('RAG-Ready'):
            warnings.append("heading_no_fullpath: 标题未使用 '一级 > 二级 > 当前' 全路径格式")

    # 零指代检查
    dangling_refs = re.findall(r'(?<!\w)(上述|如下|如前所述|this\s+one|前述)(?!\w)', content)
    if dangling_refs:
        warnings.append(f"dangling_references: 发现未锚定的指代词 {dangling_refs[:3]}")

    # 废弃标记检查
    if data.get('status') == 'deprecated':
        if '[!CAUTION]' not in content:
            warnings.append("deprecated_no_caution: status=deprecated 但正文缺少 [!CAUTION] 警告")

    # embedding_hint 质量
    hint = data.get('embedding_hint', '')
    if hint and len(str(hint)) > 200:
        warnings.append(f"embedding_hint_too_long: {len(str(hint))} 字 (上限 200)")

    # tags 覆盖检查
    tags = data.get('tags', [])
    if isinstance(tags, list) and len(tags) < 3:
        warnings.append("tags_insufficient: tags 少于 3 个，需覆盖领域+技术栈+动作")

    # hybrid_keywords 泛化词检查
    kw = data.get('hybrid_keywords', [])
    if isinstance(kw, list):
        generic_found = [k for k in kw if isinstance(k, str) and k in GENERIC_KEYWORDS]
        if generic_found:
            warnings.append(f"generic_keywords: 包含泛化词 {generic_found}")
        extracted = [k for k in kw if isinstance(k, str) and re.search(r'[._/]', k)]
        if len(extracted) < 2:
            warnings.append("hybrid_keywords_no_entity: 原文实体提取不足 2 个")

    # qa_pairs 检查
    qa = data.get('qa_pairs', [])
    if isinstance(qa, list):
        if len(qa) < 2:
            warnings.append("qa_pairs_insufficient: 不足 2 个")
        for i, pair in enumerate(qa):
            if isinstance(pair, dict) and 'type' not in pair:
                warnings.append(f"qa_pairs[{i}]: 缺少 type 字段")

    # 废弃命令扫描
    for pattern, replacement in DEPRECATED_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            warnings.append(f"deprecated_command: 发现 '{matches[0].strip()}'，替代: {replacement}")

    return warnings


def format_self_check(fatal_passed: bool, fatal_failed: list, warning_items: list) -> str:
    """生成 SELF_CHECK 注释"""
    failed_str = ', '.join(fatal_failed) if fatal_failed else 'none'
    warn_str = ', '.join(warning_items) if warning_items else 'none'

    if not fatal_passed:
        action = 'regenerate'
    elif warning_items:
        action = 'mark_review'
    else:
        action = 'pass'

    return f"""<!-- SELF_CHECK:
  fatal_passed={str(fatal_passed).lower()}
  fatal_failed=[{failed_str}]
  warning_items=[{warn_str}]
  action={action}
-->"""


def validate_slice(filepath: str, fix: bool = False) -> dict:
    """主校验函数"""
    path = Path(filepath)
    if not path.exists():
        return {"error": "file_not_found", "path": filepath}

    content = path.read_text(encoding='utf-8')

    # 提取 YAML
    yaml_text, yaml_start, yaml_end = extract_real_yaml(content)
    if yaml_text is None:
        return {
            "error": "no_yaml_found",
            "fatal_passed": False,
            "fatal_failed": ["YAML 元数据块未找到"]
        }

    data = parse_yaml_safe(yaml_text)
    if not data:
        return {
            "error": "yaml_parse_failed",
            "fatal_passed": False,
            "fatal_failed": ["YAML 解析失败"]
        }

    # 字段完整性
    field_check = check_field_completeness(data)

    # 内容质量
    warnings = check_content_rules(content, data)

    # 致命项
    fatal_failed = []
    if not field_check["all_present"]:
        fatal_failed.extend([f"missing_field:{f}" for f in field_check["missing"]])

    # 检查 AIGC 水印是否覆盖了标准 YAML
    if 'AIGC:' in content and 'title:' not in yaml_text:
        fatal_failed.append("AIGC_watermark_overwrites_YAML")

    fatal_passed = len(fatal_failed) == 0

    # 特殊检查：文件名路径规范
    filename = path.name
    if not re.match(r'^(api|config|guide|concepts|misc|multimodal)_\d{3}-', filename):
        if 'version_matrix' not in filename:
            warnings.append("filename_convention: 文件名不符合 {category}_{index}-xxx.md 规范")

    result = {
        "file": str(path),
        "fatal_passed": fatal_passed,
        "fatal_failed": fatal_failed,
        "warnings": warnings,
        "field_check": field_check,
        "yaml_keys_found": list(data.keys()),
        "action": "regenerate" if not fatal_passed else ("mark_review" if warnings else "pass")
    }

    # 写入自检注释
    if fix:
        self_check = format_self_check(fatal_passed, fatal_failed, warnings)

        # 移除已有的 SELF_CHECK
        content_no_check = re.sub(
            r'\n*<!-- SELF_CHECK:.*?-->\n*$', '', content, flags=re.DOTALL
        ).rstrip()

        new_content = content_no_check + '\n\n' + self_check + '\n'
        path.write_text(new_content, encoding='utf-8')
        result["self_check_written"] = True

    return result


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='单切片完整性校验')
    parser.add_argument('file', help='切片文件路径')
    parser.add_argument('--fix', action='store_true', help='写入 SELF_CHECK 注释')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    args = parser.parse_args()

    result = validate_slice(args.file, fix=args.fix)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "PASS" if result["fatal_passed"] else "FAIL"
        print(f"[{status}] {result['file']}")
        if result.get("fatal_failed"):
            print(f"  FATAL: {', '.join(result['fatal_failed'])}")
        if result.get("warnings"):
            print(f"  WARN:  {', '.join(result['warnings'])}")
        if result.get("action"):
            print(f"  ACTION: {result['action']}")
        if result.get("self_check_written"):
            print(f"  SELF_CHECK 已写入")

    sys.exit(0 if result.get("fatal_passed") else 1)
