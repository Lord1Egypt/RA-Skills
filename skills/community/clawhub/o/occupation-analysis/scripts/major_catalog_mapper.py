#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业目录映射模块

从职业教育专业目录.xlsx获取专业所属大类和类，用于定位专业教学标准MD文件。

数据结构（新版xlsx）：
| 列 | 内容 | 示例 |
|----|------|------|
| 0 | 大类代码 | 71 |
| 1 | 大类名称 | 电子与信息大类 |
| 2 | 类代码 | 7102 |
| 3 | 类名称 | 计算机类 |
| 4 | 专业代码 | 710204 |
| 5 | 专业名称 | 数字媒体技术应用 |
| 6 | 学制 | 中职 |
| 7 | 备注 | - |

文件命名规则：
- moe_pdfs_md/{类代码}{类名称}.md
- 如：moe_pdfs_md/7102计算机类.md
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re


def load_major_catalog(xlsx_path: Path) -> pd.DataFrame:
    """
    加载职业教育专业目录（新版扁平化结构）
    
    Args:
        xlsx_path: xlsx文件路径
    
    Returns:
        DataFrame with columns: [大类代码, 大类名称, 类代码, 类名称, 专业代码, 专业名称, 学制, 备注]
    """
    if not xlsx_path.exists():
        raise FileNotFoundError(f"专业目录文件不存在: {xlsx_path}")
    
    # 读取数据，使用第一行作为列名
    df = pd.read_excel(xlsx_path, header=0)
    
    # 重命名列为标准名称
    df.columns = ['大类代码', '大类名称', '类代码', '类名称', '专业代码', '专业名称', '学制', '备注']
    
    # 清理数据：去除空行
    df = df.dropna(subset=['专业代码'])
    
    # 确保专业代码为字符串
    df['专业代码'] = df['专业代码'].astype(str).str.zfill(6)
    
    return df


def get_category_from_major_code(catalog_df: pd.DataFrame, major_code: str) -> Optional[Dict]:
    """
    根据专业代码获取所属大类和类信息
    
    Args:
        catalog_df: 专业目录DataFrame
        major_code: 6位专业代码
    
    Returns:
        {'大类代码': xx, '大类名称': xx, '类代码': xxxx, '类名称': xx, '专业代码': xxxxxx, '专业名称': xx, '学制': xx} 或 None
    """
    if len(str(major_code)) != 6:
        major_code = str(major_code).zfill(6)
    
    result = catalog_df[catalog_df['专业代码'] == str(major_code)]
    if result.empty:
        return None
    
    row = result.iloc[0]
    return {
        '大类代码': row['大类代码'],
        '大类名称': row['大类名称'],
        '类代码': row['类代码'],
        '类名称': row['类名称'],
        '专业代码': row['专业代码'],
        '专业名称': row['专业名称'],
        '学制': row['学制']
    }


def get_md_file_path(category_info: Dict, moe_pdfs_md_dir: Path) -> Optional[Path]:
    """
    根据类代码获取对应的MD文件路径
    
    Args:
        category_info: get_category_from_major_code 返回的信息
        moe_pdfs_md_dir: moe_pdfs_md 目录路径
    
    Returns:
        MD文件路径，如果不存在返回 None
    """
    if not category_info:
        return None
    
    category_code = category_info['类代码']
    if not category_code:
        return None
    
    # 在 moe_pdfs_md 目录下查找匹配的文件
    # 文件名格式：{类代码}{类名称}.md，如 7102计算机类.md
    pattern = f"{category_code}*.md"
    matches = list(moe_pdfs_md_dir.glob(pattern))
    
    if matches:
        return matches[0]
    
    return None


def search_major_in_catalog(
    major_name: str,
    catalog_df: pd.DataFrame
) -> List[Dict]:
    """
    在专业目录中按名称搜索专业
    
    Args:
        major_name: 专业名称（支持模糊匹配）
        catalog_df: 专业目录DataFrame
    
    Returns:
        匹配的专业列表
    """
    results = catalog_df[catalog_df['专业名称'].str.contains(major_name, na=False)]
    return results.to_dict('records')


def get_major_category_mapping(
    xlsx_path: str = "assets/职业教育专业目录.xlsx",
    project_root: Optional[Path] = None
) -> Dict:
    """
    构建专业代码到大类/类的完整映射
    
    Args:
        xlsx_path: xlsx文件相对路径
        project_root: 项目根目录
    
    Returns:
        {专业代码: {大类代码, 大类名称, 类代码, 类名称, 专业名称, 学制}}
    """
    if project_root is None:
        project_root = Path(__file__).parent.parent
    
    xlsx_full_path = project_root / xlsx_path
    catalog_df = load_major_catalog(xlsx_full_path)
    
    mapping = {}
    for _, row in catalog_df.iterrows():
        mapping[row['专业代码']] = {
            '大类代码': row['大类代码'],
            '大类名称': row['大类名称'],
            '类代码': row['类代码'],
            '类名称': row['类名称'],
            '专业名称': row['专业名称'],
            '学制': row['学制']
        }
    
    return mapping


# 模块级缓存
_catalog_cache: Optional[pd.DataFrame] = None
_mapping_cache: Optional[Dict] = None


def get_catalog(xlsx_path: str = "assets/职业教育专业目录.xlsx") -> pd.DataFrame:
    """获取专业目录DataFrame（带缓存）"""
    global _catalog_cache
    if _catalog_cache is None:
        project_root = Path(__file__).parent.parent
        _catalog_cache = load_major_catalog(project_root / xlsx_path)
    return _catalog_cache


def get_mapping() -> Dict:
    """获取专业代码映射（带缓存）"""
    global _mapping_cache
    if _mapping_cache is None:
        _mapping_cache = get_major_category_mapping()
    return _mapping_cache


if __name__ == '__main__':
    # 测试
    project_root = Path(__file__).parent.parent
    catalog = load_major_catalog(project_root / "assets/职业教育专业目录.xlsx")
    
    print("=== 专业目录结构 ===")
    print(catalog.head(20).to_string())
    
    print("\n=== 搜索数字媒体技术 ===")
    results = search_major_in_catalog("数字媒体", catalog)
    for r in results:
        print(f"  {r['专业代码']} - {r['专业名称']} (类: {r['类代码']}, 学制: {r['学制']})")
    
    print("\n=== 查找专业所属类 ===")
    # 测试中职专业
    info = get_category_from_major_code(catalog, "710204")
    if info:
        print(f"  710204 -> {info['专业名称']} (类: {info['类代码']}{info['类名称']}, 学制: {info['学制']})")
        md_path = get_md_file_path(info, project_root / "assets/moe_pdfs_md")
        if md_path:
            print(f"  对应MD文件: {md_path.name}")
    
    # 测试高职专业
    info2 = get_category_from_major_code(catalog, "510204")
    if info2:
        print(f"  510204 -> {info2['专业名称']} (类: {info2['类代码']}{info2['类名称']}, 学制: {info2['学制']})")
        md_path2 = get_md_file_path(info2, project_root / "assets/moe_pdfs_md")
        if md_path2:
            print(f"  对应MD文件: {md_path2.name}")