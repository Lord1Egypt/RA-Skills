#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据整合脚本

合并专业教学标准、职业信息、职业映射（含ESCO/O*NET原始文档）等内容，输出Markdown格式combined_data.md

用法：
    python scripts/integrate_data.py \
        --major temp/major_info.json \
        --occupation temp/occupation_dict_data.json \
        --mapping temp/occupation_mapping_info.json \
        --output temp/combined_data.md
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


def json_to_md(data: Dict, section_name: str) -> str:
    """将JSON数据转换为Markdown格式
    
    Args:
        data: JSON数据字典
        section_name: 章节名称
    
    Returns:
        Markdown格式字符串
    """
    lines = [f"# {section_name}", ""]
    
    def format_value(value, indent=0, parent_has_raw=False):
        """递归格式化值为Markdown"""
        nonlocal lines
        prefix = "  " * indent
        
        if isinstance(value, dict):
            has_raw = 'raw_content' in value and value['raw_content']
            for k, v in value.items():
                if k == 'raw_content':
                    if v:
                        lines.append(f"{prefix}## 原始文档内容")
                        lines.append("")
                        for line in v.split('\n'):
                            lines.append(f"{prefix}{line}")
                        lines.append("")
                    continue
                if isinstance(v, (dict, list)) and v:
                    lines.append(f"{prefix}## {k}")
                    format_value(v, indent, has_raw)
                    lines.append("")
                elif isinstance(v, list) and not v:
                    if has_raw:
                        lines.append(f"{prefix}- {k}: （见上方原始文档内容）")
                    else:
                        lines.append(f"{prefix}- {k}: （空）")
                elif isinstance(v, dict) and not v:
                    lines.append(f"{prefix}- {k}: （空）")
                elif v is not None and v != '':
                    lines.append(f"{prefix}- {k}: {v}")
        elif isinstance(value, list):
            for i, item in enumerate(value, 1):
                if isinstance(item, dict):
                    lines.append(f"{prefix}### 项目 {i}")
                    format_value(item, indent + 1, 'raw_content' in item and item.get('raw_content'))
                    lines.append("")
                else:
                    lines.append(f"{prefix}{i}. {item}")
        elif isinstance(value, str):
            if '\n' in value:
                lines.append(f"{prefix}- {value[:100]}...")
            else:
                lines.append(f"{prefix}- {value}")
        else:
            lines.append(f"{prefix}- {value}")
    
    format_value(data)
    return "\n".join(lines)


def validate_combined_data(md_content: str) -> None:
    """验证MD文档包含必需章节
    
    Args:
        md_content: MD文档内容
    
    Raises:
        ValueError: 缺少必需章节时抛出异常
    """
    required_sections = ["# 专业教学标准", "# 职业信息"]
    
    missing = []
    for section in required_sections:
        if section not in md_content:
            missing.append(section)
    
    if missing:
        raise ValueError(f"MD文档缺少必需章节: {', '.join(missing)}")
    
    print("[OK] 数据完整性验证通过")


def load_json(file_path: Path, required: bool = False) -> Dict:
    """
    加载JSON文件
    
    Args:
        file_path: JSON文件路径
        required: 是否为必需文件（缺失时抛出异常）
        
    Returns:
        解析后的字典，失败返回空字典
    """
    if not file_path.exists():
        msg = f"文件不存在: {file_path}"
        if required:
            raise FileNotFoundError(msg)
        print(f"[WARNING] {msg}")
        return {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if required and not data:
                raise ValueError(f"文件为空: {file_path}")
            return data
    except json.JSONDecodeError as e:
        msg = f"JSON解析失败 {file_path}: {e}"
        if required:
            raise json.JSONDecodeError(msg, e.doc, e.pos)
        print(f"[ERROR] {msg}")
        return {}
    except IOError as e:
        print(f"[ERROR] 读取文件失败 {file_path}: {e}")
        return {}


# =============================================================================
# 国际职业文档读取（从 fetch_local.py 迁移）
# =============================================================================

def build_esco_index(esco_dir: Path) -> Dict[str, List[Path]]:
    """构建ESCO文件名索引（一个代码可能对应多个文件）"""
    index = {}
    if esco_dir.exists():
        for f in esco_dir.glob("*.md"):
            # 文件名格式: {ISCO代码}.{序号}.md（如 7231.1.md）
            # 提取ISCO代码（点号前的部分）
            stem = f.stem
            if '.' in stem:
                isco_code = stem.split('.')[0]
            else:
                isco_code = stem
            
            if isco_code not in index:
                index[isco_code] = []
            index[isco_code].append(f)
    return index


def build_onet_index(onet_dir: Path) -> Dict[str, Path]:
    """构建O*NET文件名索引"""
    index = {}
    if onet_dir.exists():
        for f in onet_dir.glob("*.md"):
            code = f.stem
            index[code] = f
    return index


def find_esco_files(esco_dir: Path, esco_index: Dict[str, List[Path]], esco_code: str) -> List[Path]:
    """
    查找ESCO文件（一个代码可能对应多个文件）
    
    Args:
        esco_dir: ESCO文档目录
        esco_index: ESCO文件名索引
        esco_code: ESCO/ISCO代码（如 7231 或 2512.9）
    
    Returns:
        文件路径列表
    """
    code = esco_code.strip()
    
    exact_file = esco_dir / f"{code}.md"
    if exact_file.exists():
        return [exact_file]
    
    if '.' in code:
        isco_code = code.split('.')[0]
        if isco_code in esco_index:
            return sorted(esco_index[isco_code])
    
    if code in esco_index:
        return sorted(esco_index[code])
    
    return []


def find_onet_file(onet_index: Dict[str, Path], onet_code: str) -> Optional[Path]:
    """
    查找O*NET文件
    
    Args:
        onet_index: O*NET文件名索引
        onet_code: O*NET代码（如 49-3023.00）
    
    Returns:
        文件路径，如果未找到返回None
    """
    code = onet_code.strip()
    return onet_index.get(code)


def read_file(file_path: Path) -> Optional[str]:
    """读取文件内容（原始Markdown）"""
    if not file_path or not file_path.exists():
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except (IOError, OSError, UnicodeDecodeError, PermissionError) as e:
        print(f"[ERROR] 读取文件失败 {file_path}: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] 未知错误读取文件 {file_path}: {e}")
        raise


def parse_mapping_results(mapping_data: Dict) -> List[Dict]:
    """
    解析映射信息，提取mapping_results列表
    
    支持多种输入格式：
    - {'mappings': [...]}
    - {'mapping_results': [...]}
    - {'results': [...]}
    - {'occupation_mapping': {...}}
    - 直接是列表
    """
    if isinstance(mapping_data, list):
        return mapping_data
    elif isinstance(mapping_data, dict):
        for key in ('mapping_results', 'results', 'mappings'):
            if key in mapping_data:
                return mapping_data[key]
        if 'occupation_mapping' in mapping_data:
            return _convert_occupation_mapping_format(mapping_data)
    
    print("[WARNING] 未识别的映射信息格式")
    return []


def _convert_occupation_mapping_format(mapping_info: Dict) -> List[Dict]:
    """兼容occupation_mapping格式的转换"""
    occupation_mapping = mapping_info.get('occupation_mapping', {})
    results = []
    for china_code, data in occupation_mapping.items():
        if isinstance(data, dict):
            results.append({
                'china_code': china_code,
                'china_name': data.get('china_name', ''),
                'esco_code': data.get('esco_code', ''),
                'esco_name': data.get('esco_name', ''),
                'onet_code': data.get('onet_code', ''),
                'onet_name': data.get('onet_name', ''),
                'confidence': data.get('mapping_confidence', 'unknown'),
                'mapping_reason': data.get('mapping_reason', ''),
            })
    return results


def build_mapping_section(mapping_results: List[Dict]) -> str:
    """
    构建国际职业代码映射表格章节
    
    Args:
        mapping_results: 解析后的映射结果列表
    
    Returns:
        Markdown字符串
    """
    lines = [
        "# 国际职业代码映射",
        "",
        "| 中国代码 | 中国名称 | ISCO代码 | ESCO名称 | SOC代码 | O*NET名称 | confidence | mapping_reason |",
        "|----------|----------|----------|----------|---------|-----------|------------|----------------|",
    ]
    
    for m in mapping_results:
        lines.append(
            f"| {m.get('china_code', '')} | {m.get('china_name', '')} "
            f"| {m.get('esco_code', '')} | {m.get('esco_name', '')} "
            f"| {m.get('onet_code', '')} | {m.get('onet_name', '')} "
            f"| {m.get('confidence', '')} | {m.get('mapping_reason', '')} |"
        )
    
    lines.append("")
    return "\n".join(lines)


def build_occupation_sections(
    mapping_results: List[Dict],
    esco_dir: Path,
    esco_index: Dict[str, List[Path]],
    onet_index: Dict[str, Path],
) -> tuple:
    """
    按职业分节输出国际原始MD内容
    
    Args:
        mapping_results: 解析后的映射结果列表
        esco_dir: ESCO文档目录
        esco_index: ESCO文件名索引
        onet_index: O*NET文件名索引
    
    Returns:
        (markdown_sections: List[str], stats: Dict) 元组
    """
    sections = []
    stats = {"esco_found": 0, "esco_missing": 0, "onet_found": 0, "onet_missing": 0}
    
    for m in mapping_results:
        china_code = m.get('china_code', '')
        china_name = m.get('china_name', '')
        esco_code = m.get('esco_code', '')
        onet_code = m.get('onet_code', '')
        
        if not esco_code and not onet_code:
            continue
        
        lines = [f"# {china_code} {china_name}", ""]
        
        # ESCO文档部分
        if esco_code:
            lines.append("### ESCO文档")
            lines.append("")
            
            esco_files = find_esco_files(esco_dir, esco_index, esco_code)
            if esco_files:
                stats["esco_found"] += len(esco_files)
                print(f"[OK] 找到 {len(esco_files)} 个ESCO文档 (职业: {china_name}, 代码: {esco_code})")
                lines.append(f"**ESCO代码**: {esco_code}")
                lines.append("")
                for esco_file in esco_files:
                    content = read_file(esco_file)
                    if content:
                        lines.append(f"#### 文档 {esco_file.name}")
                        lines.append("")
                        lines.append(content)
                        lines.append("")
                    else:
                        print(f"[WARNING] 读取ESCO文件失败: {esco_file}")
            else:
                stats["esco_missing"] += 1
                print(f"[WARNING] 未找到ESCO文档: {esco_code}")
                lines.append(f"**状态**: 未找到文档（代码: {esco_code}）")
                lines.append("")
        
        # O*NET文档部分
        if onet_code:
            lines.append("### O*NET文档")
            lines.append("")
            
            onet_file = find_onet_file(onet_index, onet_code)
            if onet_file:
                stats["onet_found"] += 1
                print(f"[OK] 找到O*NET文档 (职业: {china_name}, 代码: {onet_code})")
                lines.append(f"**O*NET代码**: {onet_code}")
                lines.append("")
                content = read_file(onet_file)
                if content:
                    lines.append(f"#### 文档 {onet_file.name}")
                    lines.append("")
                    lines.append(content)
                    lines.append("")
                else:
                    print(f"[WARNING] 读取O*NET文件失败: {onet_file}")
            else:
                stats["onet_missing"] += 1
                print(f"[WARNING] 未找到O*NET文档: {onet_code}")
                lines.append(f"**状态**: 未找到文档（代码: {onet_code}）")
                lines.append("")
        
        sections.append("\n".join(lines))
    
    return sections, stats


def main():
    parser = argparse.ArgumentParser(
        description='整合职业数据',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python scripts/integrate_data.py \\
        --major temp/major_info.json \\
        --occupation temp/occupation_dict_data.json \\
        --mapping temp/occupation_mapping_info.json \\
        --output temp/combined_data.md
        """
    )
    
    parser.add_argument('--major', '-M', help='专业教学标准数据路径 (major_info.json)')
    parser.add_argument('--occupation', '-O', help='职业信息数据路径 (occupation_dict_data.json)')
    parser.add_argument('--mapping', help='ESCO/O*NET映射信息路径 (occupation_mapping_info.json)')
    
    parser.add_argument('--output', '-out', default='temp/combined_data.md', help='输出文件路径')
    
    args = parser.parse_args()
    
    # 确定项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    if not (args.major or args.occupation or args.mapping):
        print("[ERROR] 必须提供至少一个数据源参数: --major, --occupation, --mapping")
        return
    
    sections = []
    
    # 加载专业教学标准
    if args.major:
        major_path = project_root / args.major if not Path(args.major).is_absolute() else Path(args.major)
        major_data = load_json(major_path, required=True)
        if major_data:
            sections.append(json_to_md(major_data, "专业教学标准"))
            print(f"[OK] 加载专业教学标准: {major_path}")
    
    # 加载职业信息
    if args.occupation:
        occ_path = project_root / args.occupation if not Path(args.occupation).is_absolute() else Path(args.occupation)
        occ_data = load_json(occ_path, required=True)
        if occ_data:
            sections.append(json_to_md(occ_data, "职业信息"))
            print(f"[OK] 加载职业信息: {occ_path}")
    
    # 处理映射信息：生成国际职业代码映射表格 + 按职业分节的原始MD内容
    if args.mapping:
        mapping_path = project_root / args.mapping if not Path(args.mapping).is_absolute() else Path(args.mapping)
        mapping_raw = load_json(mapping_path, required=True)
        
        if mapping_raw:
            mapping_results = parse_mapping_results(mapping_raw)
            
            if mapping_results:
                # 构建索引
                esco_dir = project_root / "assets" / "esco_details_md"
                onet_dir = project_root / "assets" / "onet_details_md"
                esco_index = build_esco_index(esco_dir)
                onet_index = build_onet_index(onet_dir)
                
                # 生成映射表格
                sections.append(build_mapping_section(mapping_results))
                print(f"[OK] 生成国际职业代码映射表格 ({len(mapping_results)} 条)")
                
                # 生成按职业分节的原始MD内容
                occ_sections, stats = build_occupation_sections(
                    mapping_results, esco_dir, esco_index, onet_index
                )
                sections.extend(occ_sections)
                print(
                    f"[OK] 生成职业原始MD章节: "
                    f"ESCO({stats['esco_found']} found, {stats['esco_missing']} missing), "
                    f"O*NET({stats['onet_found']} found, {stats['onet_missing']} missing)"
                )
            else:
                print("[WARNING] 映射信息中无有效映射结果")
    
    # 添加元数据
    metadata = f"""---
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
数据格式: Markdown
---"""
    
    # 合并所有章节
    combined_md = metadata + "\n\n" + "\n\n---\n\n".join(sections)
    
    # 验证数据完整性
    validate_combined_data(combined_md)
    
    # 保存输出
    output_path = project_root / args.output if not Path(args.output).is_absolute() else Path(args.output)
    if output_path.suffix == '.json':
        output_path = output_path.with_suffix('.md')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(combined_md)
    
    print(f"\n[OK] 基础数据已整合到: {output_path}")
    print(f"     - 章节数量: {len(sections)}")
    print(f"     - 文件大小: {len(combined_md)} 字符")


if __name__ == '__main__':
    main()
