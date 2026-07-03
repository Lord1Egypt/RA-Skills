#!/usr/bin/env python3
"""
batch_audit.py — 跨切片批量审计与终结校验
用法: python batch_audit.py <slice_directory> [--fix] [--json]

审计内容:
  1. 索引连续性 (per source_id)
  2. cross_refs 死链检测
  3. 孤立切片检测
  4. 废弃命令扫描
  5. 文件大小异常检测

--fix: 在审计目录下生成 batch_audit_report.md
"""

import sys
import os
import re
import json
import statistics
from pathlib import Path
from collections import defaultdict

try:
    import yaml
except ImportError:
    print("错误：缺少 pyyaml 依赖。请执行: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# ── 废弃命令模式 ──
DEPRECATED_PATTERNS = [
    (r'git\s+stash\s+save\b', 'git stash push -m'),
    (r'git\s+checkout\s+--orphan\b', 'git switch --orphan'),
    (r'docker\s+rm\s+-f\b', 'docker rm -f (use with caution)'),
    (r'git\s+diff-tree\s+--no-commit-id\b', 'git diff-tree --no-commit-id (deprecated in newer git)'),
]


def extract_real_yaml(content: str) -> dict:
    """提取真正的元数据 YAML 块"""
    parts = content.split('---')
    for i in range(1, len(parts)):
        block = parts[i].strip()
        if not block:
            continue
        if 'title:' in block:
            try:
                data = yaml.safe_load(block)
                return data if isinstance(data, dict) else {}
            except Exception:
                pass
    # 回退：尝试第二个非空块
    non_empty = [parts[i].strip() for i in range(1, len(parts)) if parts[i].strip()]
    for block in non_empty:
        try:
            data = yaml.safe_load(block)
            if isinstance(data, dict) and 'title' in data:
                return data
        except Exception:
            continue
    return {}


def scan_slices(root_dir: str) -> list:
    """递归扫描所有切片文件"""
    slices = []
    root = Path(root_dir)
    if not root.exists():
        return slices

    for path in root.rglob('*.md'):
        # 跳过非切片文件
        if path.name in ('SKILL.md', 'README.md', 'version_matrix.md', 'batch_audit_report.md'):
            continue
        # 文件名匹配：{category}_{index}-xxx.md 或 {index}-xxx.md（类别在目录名中）
        is_slice = bool(re.match(r'^\d{3}-', path.name)) or bool(re.match(r'^[\w]+_\d{3}-', path.name))
        is_ver_matrix = 'version_matrix' in path.name
        if not is_slice and not is_ver_matrix:
            continue

        try:
            content = path.read_text(encoding='utf-8')
        except Exception:
            continue

        data = extract_real_yaml(content)

        slices.append({
            "path": str(path),
            "filename": path.name,
            "size": path.stat().st_size,
            "data": data,
            "content": content,
            "source_id": data.get("source_id", ""),
            "category": data.get("category", "misc"),
            "index": data.get("index", 0),
            "cross_refs": data.get("cross_refs", {}),
        })

    return slices


def check_index_continuity(slices: list) -> dict:
    """按 source_id 分组检查索引连续性"""
    groups = defaultdict(list)
    for s in slices:
        groups[s["source_id"]].append(s)

    gaps = {}
    for sid, slist in groups.items():
        indices = sorted([s["index"] for s in slist if isinstance(s["index"], int) and s["index"] > 0])
        if not indices:
            continue
        expected = list(range(1, max(indices) + 1))
        missing = sorted(set(expected) - set(indices))
        duplicates = [n for n in indices if indices.count(n) > 1]
        gaps[sid] = {
            "total_files": len(slist),
            "indices": indices,
            "missing_indices": missing,
            "duplicate_indices": list(set(sorted(duplicates))),
            "continuous": len(missing) == 0 and len(duplicates) == 0
        }

    return gaps


def check_cross_refs(slices: list) -> dict:
    """检测 cross_refs 死链"""
    all_filenames = {s["filename"] for s in slices}
    dead_links = []

    for s in slices:
        refs = s.get("cross_refs", {})
        if not isinstance(refs, dict):
            continue

        depends = refs.get("depends_on", []) or []
        related = refs.get("related_to", []) or []

        for ref in depends + related:
            if isinstance(ref, str) and ref not in all_filenames:
                dead_links.append({
                    "from": s["filename"],
                    "to": ref,
                    "type": "depends_on" if ref in (depends or []) else "related_to"
                })

    return {
        "dead_links": dead_links,
        "total_dead": len(dead_links),
        "all_valid": len(dead_links) == 0
    }


def fuzzy_match_filename(target: str, candidates: set, threshold: float = 0.5) -> str:
    """模糊匹配文件名，返回最佳匹配或空字符串。
    
    策略：提取候选中的类别前缀+序号，再对标题部分做 token overlap。
    """
    if not target or not candidates:
        return ""
    
    # 提取 target 的类别前缀和序号
    target_lower = target.lower()
    target_tokens = set(re.split(r'[-_\s.]+', target_lower.replace('.md', '')))
    
    best_score = 0.0
    best_match = ""
    
    for cand in candidates:
        cand_lower = cand.lower().replace('.md', '')
        cand_tokens = set(re.split(r'[-_\s.]+', cand_lower))
        
        # Jaccard token overlap
        intersection = target_tokens & cand_tokens
        union = target_tokens | cand_tokens
        if not union:
            continue
        jaccard = len(intersection) / len(union)
        
        # 提取序号段（如 001, 005）进行匹配
        target_nums = re.findall(r'\d{2,}', target_lower)
        cand_nums = re.findall(r'\d{2,}', cand_lower)
        num_bonus = 0.3 if target_nums and cand_nums and any(n in cand_nums for n in target_nums) else 0.0
        
        score = jaccard + num_bonus
        if score > best_score and score >= threshold:
            best_score = score
            best_match = cand
    
    return best_match


def auto_fix_cross_refs(slices: list, dead_links: list, root_dir: str) -> int:
    """自动修正 cross_refs 死链：模糊匹配 → 更新 YAML → 写回文件。
    
    返回修正的链接数。
    """
    if not dead_links:
        return 0
    
    all_filenames = {s["filename"] for s in slices}
    fixed_count = 0
    
    # 按源文件分组死链
    by_file = defaultdict(list)
    for dl in dead_links:
        by_file[dl["from"]].append(dl)
    
    for src_filename, links in by_file.items():
        # 找到源文件路径
        src_path = None
        for s in slices:
            if s["filename"] == src_filename:
                src_path = s["path"]
                break
        if not src_path:
            continue
        
        try:
            raw = Path(src_path).read_text(encoding='utf-8')
        except Exception:
            continue
        
        new_raw = raw
        file_changed = False
        
        for link in links:
            old_ref = link["to"]
            # 模糊匹配修正文件名
            corrected = fuzzy_match_filename(old_ref, all_filenames)
            if corrected and corrected != old_ref:
                # 替换 YAML 中的引用：兼容多种 YAML 列表语法
                #   - "filename"          → 列表项引号包裹
                #   - filename            → 列表项无引号
                #   ["filename", ...]     → JSON-style 数组
                escaped = re.escape(old_ref)
                pats = [
                    # JSON-style 数组: [..., "filename", ...] 或 ["filename", ...]
                    #   ── ["\']? 消耗原有引号, 防止替换后出现 ""..."" 双引号
                    (rf'(\[.*?)["\']?\s*{escaped}\s*["\']?(.*?\])', rf'\g<1>"{corrected}"\g<2>'),
                    # YAML 列表项: - "filename" 或  - filename
                    (rf'^(\s*-\s*)["\']?\s*{escaped}\s*["\']?', rf'\g<1>"{corrected}"'),
                ]
                matched = False
                for pat, repl in pats:
                    new_raw, n = re.subn(pat, repl, new_raw, flags=re.MULTILINE)
                    if n > 0:
                        file_changed = True
                        fixed_count += n
                        matched = True
                        print(f"[FIX] {src_filename}: '{old_ref}' → '{corrected}'")
                        break
                # 兜底：字符串直接替换（适用于非标准格式）
                if not matched:
                    new_raw_before = new_raw
                    new_raw = new_raw.replace(old_ref, corrected)
                    if new_raw != new_raw_before:
                        file_changed = True
                        fixed_count += 1
                        print(f"[FIX] {src_filename}: '{old_ref}' → '{corrected}' (direct)")
        
        if file_changed:
            try:
                # 修改前备份原始内容
                bak_path = Path(src_path).with_suffix('.md.bak')
                Path(src_path).rename(bak_path)
                Path(src_path).write_text(new_raw, encoding='utf-8')
                bak_path.unlink()
            except Exception:
                pass
    
    return fixed_count


def find_orphans(slices: list) -> list:
    """查找未被任何其他切片引用的孤立切片"""
    referenced = set()
    for s in slices:
        refs = s.get("cross_refs", {})
        if not isinstance(refs, dict):
            continue
        for ref in (refs.get("depends_on", []) or []):
            referenced.add(ref)
        for ref in (refs.get("related_to", []) or []):
            referenced.add(ref)

    orphans = [s["filename"] for s in slices if s["filename"] not in referenced]
    return orphans


def scan_deprecated_commands(slices: list) -> list:
    """扫描所有切片中的废弃命令"""
    findings = []
    for s in slices:
        content = s.get("content", "")
        for pattern, replacement in DEPRECATED_PATTERNS:
            matches = re.findall(pattern, content)
            for match in matches:
                findings.append({
                    "file": s["filename"],
                    "command": match.strip() if isinstance(match, str) else str(match),
                    "replacement": replacement,
                    "path": s["path"]
                })
    return findings


def check_size_anomalies(slices: list) -> list:
    """检测文件大小异常（偏离均值 > 50%）"""
    sizes = [s["size"] for s in slices if s["size"] > 0]
    if len(sizes) < 3:
        return []

    avg = statistics.mean(sizes)
    anomalies = []
    for s in slices:
        if s["size"] > 0 and abs(s["size"] - avg) / avg > 0.5:
            anomalies.append({
                "file": s["filename"],
                "size_bytes": s["size"],
                "avg_bytes": int(avg),
                "deviation_pct": round((s["size"] - avg) / avg * 100, 1)
            })
    return anomalies


def generate_report(root_dir: str, index_gaps: dict, cross_ref_result: dict,
                    orphans: list, deprecated: list, size_anomalies: list,
                    total_files: int) -> str:
    """生成 Markdown 审计报告"""
    lines = [
        f"# 切片批量审计报告",
        f"",
        f"**审计目录**: `{root_dir}`  ",
        f"**审计时间**: 自动生成  ",
        f"**切片总数**: {total_files}",
        f"",
        f"## 1. 索引连续性",
        f"",
    ]

    if not index_gaps:
        lines.append("未检测到 source_id 分组信息。")
    else:
        for sid, info in index_gaps.items():
            status = "PASS" if info["continuous"] else "FAIL"
            lines.append(f"### {sid or '(无 source_id)'}  [{status}]")
            lines.append(f"- 文件数: {info['total_files']}")
            lines.append(f"- 索引范围: {min(info['indices']) if info['indices'] else 'N/A'} ~ {max(info['indices']) if info['indices'] else 'N/A'}")
            if info["missing_indices"]:
                lines.append(f"- **缺失索引**: {info['missing_indices']}")
            if info.get("duplicate_indices"):
                lines.append(f"- **重复索引**: {info['duplicate_indices']}")
            lines.append("")

    lines.append("## 2. Cross-Refs 死链检测")
    if cross_ref_result["all_valid"]:
        lines.append("PASS: 未发现死链。")
    else:
        lines.append(f"发现 {cross_ref_result['total_dead']} 条死链：")
        for dl in cross_ref_result["dead_links"]:
            lines.append(f"- `{dl['from']}` → `{dl['to']}` ({dl['type']})")
    lines.append("")

    lines.append("## 3. 孤立切片")
    if not orphans:
        lines.append("PASS: 未发现孤立切片。")
    else:
        lines.append(f"发现 {len(orphans)} 个孤立切片（未被任何其他切片引用）：")
        for o in orphans:
            lines.append(f"- `{o}`")
    lines.append("")

    lines.append("## 4. 废弃命令扫描")
    if not deprecated:
        lines.append("PASS: 未发现已知废弃命令。")
    else:
        lines.append(f"发现 {len(deprecated)} 处废弃命令：")
        for d in deprecated:
            lines.append(f"- `{d['file']}`: `{d['command']}` → 替代: `{d['replacement']}`")
    lines.append("")

    lines.append("## 5. 文件大小异常")
    if not size_anomalies:
        lines.append("PASS: 未发现大小异常。")
    else:
        lines.append(f"发现 {len(size_anomalies)} 个文件大小偏离均值 > 50%：")
        for a in size_anomalies:
            lines.append(f"- `{a['file']}`: {a['size_bytes']}B (均值 {a['avg_bytes']}B, 偏离 {a['deviation_pct']}%)")
    lines.append("")

    return '\n'.join(lines)


def audit(root_dir: str, fix: bool = False) -> dict:
    """主审计函数"""
    slices = scan_slices(root_dir)
    if not slices:
        return {"error": "no_slices_found", "directory": root_dir}

    total = len(slices)

    # 执行各项审计
    index_gaps = check_index_continuity(slices)
    cross_ref_result = check_cross_refs(slices)
    orphans = find_orphans(slices)
    deprecated = scan_deprecated_commands(slices)
    size_anomalies = check_size_anomalies(slices)

    # 判断整体状态
    all_continuous = all(info["continuous"] for info in index_gaps.values()) if index_gaps else True
    overall_pass = all_continuous and cross_ref_result["all_valid"] and not orphans

    result = {
        "directory": root_dir,
        "total_files": total,
        "overall_pass": overall_pass,
        "index_gaps": index_gaps,
        "cross_refs": cross_ref_result,
        "orphans": orphans,
        "deprecated_commands": deprecated,
        "size_anomalies": size_anomalies,
    }

    if fix:
        # ── 自动修正死链 ──
        if cross_ref_result.get("dead_links"):
            print(f"[FIX] 尝试自动修正 {cross_ref_result['total_dead']} 条死链 ...")
            n_fixed = auto_fix_cross_refs(slices, cross_ref_result["dead_links"], root_dir)
            result["cross_ref_fixed"] = n_fixed
            # 重新扫描以获取修正后的状态
            if n_fixed > 0:
                slices = scan_slices(root_dir)
                cross_ref_result = check_cross_refs(slices)
                result["cross_refs"] = cross_ref_result

        report = generate_report(
            root_dir, index_gaps, cross_ref_result,
            orphans, deprecated, size_anomalies, total
        )
        report_path = os.path.join(root_dir, "batch_audit_report.md")
        Path(report_path).write_text(report, encoding='utf-8')
        result["report_path"] = report_path

    return result


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='跨切片批量审计')
    parser.add_argument('directory', help='切片目录路径')
    parser.add_argument('--fix', action='store_true', help='生成审计报告')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    args = parser.parse_args()

    result = audit(args.directory, fix=args.fix)

    if args.json:
        # 清理不可序列化内容
        output = {k: v for k, v in result.items() if k not in ('index_gaps',)}
        output['index_summary'] = {
            sid: {'continuous': v['continuous'], 'missing': v.get('missing_indices', [])}
            for sid, v in result.get('index_gaps', {}).items()
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        status = "PASS" if result.get("overall_pass") else "FAIL"
        print(f"[{status}] 审计完成: {result['total_files']} 个切片")

        if result.get("index_gaps"):
            for sid, info in result["index_gaps"].items():
                icon = "PASS" if info["continuous"] else "WARN"
                missing_str = info.get("missing_indices", [])
                if info['continuous']:
                    idx_status = '连续'
                else:
                    idx_status = f'缺失 {missing_str}'
                print(f"  [{icon}] {sid}: 索引 {idx_status}")

        cr = result.get("cross_refs", {})
        if cr.get("dead_links"):
            print(f"  [FAIL] 死链: {len(cr['dead_links'])} 条")
            for dl in cr["dead_links"][:5]:
                print(f"    {dl['from']} → {dl['to']}")

        if result.get("orphans"):
            print(f"  [WARN] 孤立切片: {len(result['orphans'])} 个")

        if result.get("deprecated_commands"):
            print(f"  [WARN] 废弃命令: {len(result['deprecated_commands'])} 处")

        if result.get("size_anomalies"):
            print(f"  [WARN] 大小异常: {len(result['size_anomalies'])} 个")

        if result.get("report_path"):
            print(f"  报告已生成: {result['report_path']}")

    sys.exit(0 if result.get("overall_pass") else 1)
