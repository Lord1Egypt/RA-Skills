#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
职业大典分块加载工具
优化版本：按需加载职业大类，减少token消耗
"""

import re
import json
from pathlib import Path
from typing import Optional, List

class OccupationDictionaryLoader:
    """
    职业大典智能加载器
    
    功能：
    1. 按需加载职业大类文件（替代完整文件加载）
    2. 根据职业代码自动识别所属大类
    3. 支持批量查询多个职业
    
    优化效果：
    - 完整文件: ~136K tokens
    - 单个大类: 2K-62K tokens（平均节省70-90%）
    """
    
    # 职业代码前缀到大类数字的映射
    CLASS_MAPPING = {
        '1-': ('1', 'class_1_党的机关_国家机关_群众团体和社会组织_企事业单位负责人.md'),
        '2-': ('2', 'class_2_专业技术人员.md'),
        '3-': ('3', 'class_3_办事人员和有关人员.md'),
        '4-': ('4', 'class_4_社会生产服务和生活服务人员.md'),
        '5-': ('5', 'class_5_农_林_牧_渔业生产及辅助人员.md'),
        '6-': ('6', 'class_6_生产制造及有关人员.md'),
    }
    
    def __init__(self, base_path: str = 'assets/occupation_dictionary_split'):
        """
        初始化加载器
        
        Args:
            base_path: 分块文件所在目录（相对于skill根目录）
        """
        self.base_path = Path(__file__).parent.parent / base_path
        self.split_info_path = self.base_path / 'split_info.json'
        self._cache = {}  # 缓存已加载的文件
        
        # 检查分块文件是否存在
        if not self.base_path.exists():
            print(f"[WARNING] 分块目录不存在: {self.base_path}")
            print("[HINT] 请运行 scripts/split_occupation_dict_v2.py 生成分块文件")
    
    def get_class_by_code(self, occupation_code: str) -> Optional[str]:
        """
        根据职业代码获取所属大类数字
        
        Args:
            occupation_code: 职业代码，如 "6-22-02" 或 "6-22-02-01"
        
        Returns:
            大类数字字符串（"1"-"6"），如果无法识别则返回None
        """
        # 提取代码前缀
        match = re.match(r'([1-6])-', occupation_code)
        if match:
            return match.group(1)
        return None
    
    def get_class_file(self, class_num: str) -> Optional[Path]:
        """
        获取大类文件路径
        
        Args:
            class_num: 大类数字（"1"-"6"）
        
        Returns:
            文件路径，如果不存在则返回None
        """
        for prefix, (num, filename) in self.CLASS_MAPPING.items():
            if num == class_num:
                filepath = self.base_path / filename
                if filepath.exists():
                    return filepath
                else:
                    print(f"[ERROR] 大类文件不存在: {filepath}")
                    return None
        return None
    
    def load_class_content(self, class_num: str, use_cache: bool = True) -> Optional[str]:
        """
        加载大类文件内容
        
        Args:
            class_num: 大类数字（"1"-"6"）
            use_cache: 是否使用缓存
        
        Returns:
            文件内容字符串
        """
        # 检查缓存
        if use_cache and class_num in self._cache:
            return self._cache[class_num]
        
        # 获取文件路径
        filepath = self.get_class_file(class_num)
        if not filepath:
            return None
        
        # 读取文件
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 存入缓存
            if use_cache:
                self._cache[class_num] = content
            
            return content
        except Exception as e:
            print(f"[ERROR] 读取文件失败: {e}")
            return None
    
    def load_by_occupation_code(self, occupation_code: str) -> Optional[str]:
        """
        根据职业代码智能加载对应大类文件
        
        Args:
            occupation_code: 职业代码，如 "6-22-02"
        
        Returns:
            对应大类文件的内容
        """
        class_num = self.get_class_by_code(occupation_code)
        if not class_num:
            print(f"[ERROR] 无法识别职业代码: {occupation_code}")
            return None
        
        content = self.load_class_content(class_num)
        if content:
            print(f"[OK] 已加载第{class_num}大类，用于查询职业 {occupation_code}")
            print(f"[INFO] 内容大小: {len(content)} 字符 (~{len(content)/4:.0f} tokens)")
        
        return content
    
    def load_multiple(self, occupation_codes: List[str]) -> dict:
        """
        批量加载多个职业代码对应的大类文件
        自动合并同一类文件，避免重复加载
        
        Args:
            occupation_codes: 职业代码列表
        
        Returns:
            字典 {职业代码: 对应大类内容}
        """
        results = {}
        loaded_classes = {}  # 缓存已加载的大类
        
        for code in occupation_codes:
            class_num = self.get_class_by_code(code)
            if not class_num:
                continue
            
            # 如果该大类已加载，直接使用缓存
            if class_num in loaded_classes:
                results[code] = loaded_classes[class_num]
            else:
                # 加载新大类
                content = self.load_class_content(class_num)
                if content:
                    loaded_classes[class_num] = content
                    results[code] = content
        
        return results
    
    def get_stats(self) -> dict:
        """
        获取分块统计信息
        
        Returns:
            统计信息字典
        """
        stats = {
            'total_classes': len(self.CLASS_MAPPING),
            'loaded_in_cache': len(self._cache),
            'class_sizes': {}
        }
        
        for class_num, (_, filename) in self.CLASS_MAPPING.items():
            filepath = self.base_path / filename
            if filepath.exists():
                size = filepath.stat().st_size
                stats['class_sizes'][class_num] = {
                    'filename': filename,
                    'size_bytes': size,
                    'size_kb': size / 1024,
                    'tokens': size / 4
                }
        
        # 计算平均大小
        if stats['class_sizes']:
            avg_tokens = sum(s['tokens'] for s in stats['class_sizes'].values()) / len(stats['class_sizes'])
            stats['avg_tokens'] = avg_tokens
        
        return stats

# 便捷函数
def get_occupation_dictionary(occupation_code: str) -> Optional[str]:
    """
    根据职业代码获取对应大类的职业大典内容（便捷函数）
    
    Args:
        occupation_code: 职业代码，如 "6-22-02"
    
    Returns:
        对应大类文件内容
    """
    loader = OccupationDictionaryLoader()
    return loader.load_by_occupation_code(occupation_code)

def get_occupation_dictionary_bulk(codes: List[str]) -> dict:
    """
    批量获取多个职业代码对应的职业大典内容（便捷函数）
    
    Args:
        codes: 职业代码列表
    
    Returns:
        字典 {职业代码: 对应大类内容}
    """
    loader = OccupationDictionaryLoader()
    return loader.load_multiple(codes)

if __name__ == '__main__':
    # 测试
    print("=" * 60)
    print("职业大典分块加载器测试")
    print("=" * 60)
    print()
    
    loader = OccupationDictionaryLoader()
    
    # 显示统计信息
    print("=== 分块统计 ===")
    stats = loader.get_stats()
    print(f"总大类数: {stats['total_classes']}")
    print(f"缓存中已加载: {stats['loaded_in_cache']}")
    print()
    
    for class_num, info in stats['class_sizes'].items():
        print(f"第{class_num}大类: {info['size_kb']:.1f} KB ({info['tokens']:.0f} tokens)")
    
    if 'avg_tokens' in stats:
        print(f"\n平均每个大类: {stats['avg_tokens']:.0f} tokens")
        print(f"相比完整文件 (336K tokens) 节省: {(1 - stats['avg_tokens']/336000)*100:.1f}%")
    
    print("\n" + "=" * 60)
    print("测试单职业加载")
    print("=" * 60)
    
    test_codes = ['6-22-02', '6-31-03', '4-08-05-05']
    for code in test_codes:
        print(f"\n测试: {code}")
        content = loader.load_by_occupation_code(code)
        if content:
            # 查找该职业在内容中的位置
            pattern = f"{code.replace('-', '-')}"
            matches = re.findall(pattern, content)
            print(f"  找到 {len(matches)} 处匹配")
    
    print("\n" + "=" * 60)
    print("测试批量加载")
    print("=" * 60)
    
    results = loader.load_multiple(test_codes)
    print(f"\n批量加载 {len(test_codes)} 个职业")
    print(f"实际加载 {len(set(loader.get_class_by_code(c) for c in test_codes))} 个大类文件")
    print("(6-22-02 和 6-31-03 同属第6大类，只加载一次)")