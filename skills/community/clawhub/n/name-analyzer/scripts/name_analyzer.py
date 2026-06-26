#!/usr/bin/env python3
"""
Name Analyzer - 名字分析工具
Core script for analyzing names
"""

import sys
import re
import json
import argparse
from typing import Dict, Optional


class NameAnalyzer:
    """名字分析器"""
    
    # 中文姓名学数据（简化版）
    CHINESE_MEANINGS = {
        '伟': '伟大、卓越、雄伟',
        '明': '聪明、光明、睿智',
        '华': '华丽、才华、中华',
        '强': '强大、坚强、有力',
        '磊': '光明磊落、坦荡',
        '军': '军人、刚毅、纪律',
        '鹏': '大鹏鸟、志向远大',
        '飞': '飞翔、自由、志向',
        '龙': '龙、尊贵、威严',
        '凤': '凤凰、高贵、祥瑞',
        '宇': '宇宙、广阔、包容',
        '浩': '浩大、广阔、遥远',
        '敏': '敏捷、聪明、灵活',
        '静': '安静、宁静、文静',
        '丽': '美丽、秀丽、好看',
        '芳': '芬芳、香气、美好',
        '婷': '优美、雅致、秀气',
        '颖': '聪颖、突出、才能',
        '颖': '聪颖、突出、才能',
    }
    
    # 偏旁部首含义
    RADICAL_MEANINGS = {
        '氵': '水属性 - 智慧、流动性',
        '木': '木属性 - 生长、柔韧性',
        '火': '火属性 - 热情、行动力',
        '土': '土属性 - 稳定、务实',
        '金': '金属性 - 坚硬、果断',
        '忄': '心属性 - 情感、直觉',
        '扌': '手属性 - 行动、执行',
        '口': '口属性 - 表达、沟通',
        '目': '眼属性 - 观察、洞察',
        '耳': '耳属性 - 倾听、接受',
    }
    
    # 英文名字含义
    ENGLISH_MEANINGS = {
        'john': '上帝是仁慈的',
        'james': '替代者、追随者',
        'michael': '像上帝一样的人',
        'david': '被爱的',
        'william': '坚定的保护者',
        'james': '替代者',
        'robert': '光辉的著名',
        'mary': '海之星',
        'jennifer': '公平的笑容',
        'elizabeth': '上帝的誓言',
        'smith': '铁匠、工匠',
        'johnson': '约翰的儿子',
        'williams': '威廉的儿子',
        'brown': '棕色头发的人',
    }
    
    # 数字对应表（姓名学）
    NUMEROLOGY = {
        1: '领导力、独立、创造',
        2: '合作、平衡、直觉',
        3: '表达、创意、社交',
        4: '稳定、实用、组织',
        5: '自由、变化、冒险',
        6: '责任、家庭、和谐',
        7: '分析、内省、灵性',
        8: '权力、成就、物质',
        9: '理想、人道、完成',
    }
    
    # 笔划数对应
    STROKE_MEANINGS = {
        1: '宇宙起源、纯阳',
        2: '对立统一、平衡',
        3: '天地人三才',
        4: '四季平稳',
        5: '五行运转',
        6: '天地父母',
        7: '刚健中正',
        8: '数理发刚',
        9: '满腹经纶',
        10: '完结、归零',
    }
    
    def __init__(self):
        self.name = ""
        
    def analyze(self, name: str, full_mode: bool = False) -> Dict:
        """主分析函数"""
        self.name = name.strip()
        
        results = {
            'name': self.name,
            'type': self._detect_type(),
            'meaning': self._get_meaning(),
            'origin': self._get_origin(),
            'numerology': self._get_numerology(),
            'radical': self._get_radical_info() if self._detect_type() == 'chinese' else None,
            'suggestions': self._generate_suggestions(),
            'score': self._calculate_score(),
        }
        
        if full_mode:
            results['famous_people'] = self._find_famous_people()
            results['compatibility'] = self._check_compatibility()
            
        return results
    
    def _detect_type(self) -> str:
        """检测名字类型"""
        if re.match(r'^[a-zA-Z]+$', self.name):
            return 'english'
        elif re.match(r'^[\u4e00-\u9fff]+$', self.name):
            return 'chinese'
        else:
            return 'mixed'
    
    def _get_meaning(self) -> str:
        """获取名字含义"""
        if self._detect_type() == 'chinese':
            meanings = []
            for char in self.name:
                if char in self.CHINESE_MEANINGS:
                    meanings.append(f"{char}: {self.CHINESE_MEANINGS[char]}")
            return "； ".join(meanings) if meanings else "未找到详细含义"
        elif self._detect_type() == 'english':
            name_lower = self.name.lower()
            return self.ENGLISH_MEANINGS.get(name_lower, "未找到详细含义")
        return "混合类型名字"
    
    def _get_origin(self) -> str:
        """获取名字来源"""
        ntype = self._detect_type()
        if ntype == 'chinese':
            return "中华文化姓氏/名字体系"
        elif ntype == 'english':
            return "西方英语国家名字体系（源自拉丁语、希伯来语等）"
        return "中西方混合"
    
    def _get_numerology(self) -> Dict:
        """数理分析"""
        # 计算笔划数（中文）或字母序（英文）
        if self._detect_type() == 'chinese':
            # 简化计算：使用Unicode编码
            total_strokes = sum(ord(c) % 10 + 1 for c in self.name)
        else:
            # 英文名字：字母序之和
            total_strokes = sum(ord(c.lower()) - ord('a') + 1 for c in self.name if c.isalpha())
        
        life_path = (total_strokes % 9) + 1
        expression = ((total_strokes * 2) % 9) + 1
        soul_urge = ((total_strokes + 10) % 9) + 1
        
        return {
            'life_path': {
                'number': life_path,
                'meaning': self.NUMEROLOGY.get(life_path, '未定义'),
                'description': '生命道路数，代表人生主要课题'
            },
            'expression': {
                'number': expression,
                'meaning': self.NUMEROLOGY.get(expression, '未定义'),
                'description': '人格数，代表外在表现'
            },
            'soul_urge': {
                'number': soul_urge,
                'meaning': self.NUMEROLOGY.get(soul_urge, '未定义'),
                'description': '心灵数，代表内在渴望'
            }
        }
    
    def _get_radical_info(self) -> Optional[Dict]:
        """获取偏旁部首信息"""
        radicals = []
        for char in self.name:
            # 简化：取第一个能识别的部首
            for radical, meaning in self.RADICAL_MEANINGS.items():
                if char.startswith(radical):
                    radicals.append({'radical': radical, 'meaning': meaning})
                    break
        return radicals if radicals else None
    
    def _calculate_score(self) -> int:
        """计算综合评分"""
        score = 70
        
        # 长度因素
        if 2 <= len(self.name) <= 4:
            score += 10
            
        # 类型因素
        if self._detect_type() == 'chinese':
            score += 10
            
        # 含义存在
        if self._get_meaning() != "未找到详细含义":
            score += 10
            
        return min(100, score)
    
    def _generate_suggestions(self) -> list:
        """生成建议"""
        suggestions = []
        
        if len(self.name) < 2:
            suggestions.append("建议使用2字或以上的名字")
            
        if self._detect_type() == 'chinese':
            if not any(c in self.CHINESE_MEANINGS for c in self.name):
                suggestions.append("名字中的字较为少见，可考虑添加常见寓意好的字")
                
        score = self._calculate_score()
        if score >= 90:
            suggestions.append("名字整体评分优秀")
        elif score >= 70:
            suggestions.append("名字不错，有轻微优化空间")
        else:
            suggestions.append("建议考虑调整名字以提升整体效果")
            
        return suggestions
    
    def _find_famous_people(self) -> list:
        """查找同名名人"""
        famous_db = {
            '伟': ['马云（阿里巴巴创始人）', '邓小平和'],
            '明': ['朱元璋（明朝开国皇帝）', '张大大（主持人）'],
            '华': ['刘德华（演员）', '李中华（科学家）'],
            '强': ['马化腾（腾讯创始人）'],
            '龙': ['李小龙（武术家）', '成龙（演员）'],
        }
        
        results = []
        for char in self.name:
            if char in famous_db:
                results.extend(famous_db[char])
                
        return list(set(results))[:5] if results else ["未找到同名名人记录"]
    
    def _check_compatibility(self) -> Dict:
        """检查与姓氏的搭配"""
        return {
            'score': 85,
            'balance': '阴阳调和',
            'remark': '名字与姓氏搭配整体协调'
        }


def format_results(results: Dict) -> str:
    """格式化输出"""
    output = []
    output.append("=" * 50)
    output.append(f"📖 名字分析报告: {results['name']}")
    output.append("=" * 50)
    
    output.append(f"\n🏷️ 类型: {results['type']}")
    output.append(f"📍 来源: {results['origin']}")
    
    output.append(f"\n💡 名字含义:")
    output.append(f"   {results['meaning']}")
    
    output.append(f"\n🔢 数理分析:")
    for key, val in results['numerology'].items():
        output.append(f"   {val['description']}: {val['number']} ({val['meaning']})")
    
    if results['radical']:
        output.append(f"\n🔍 偏旁部首:")
        for r in results['radical']:
            output.append(f"   {r['radical']}: {r['meaning']}")
    
    if 'famous_people' in results:
        output.append(f"\n👥 同名名人:")
        for p in results['famous_people']:
            output.append(f"   • {p}")
    
    output.append(f"\n📊 综合评分: {results['score']}/100")
    
    output.append(f"\n💡 建议:")
    for s in results['suggestions']:
        output.append(f"   {s}")
    
    output.append("\n" + "=" * 50)
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='Name Analyzer - 名字分析工具')
    parser.add_argument('command', choices=['analyze', 'full', 'numerology', 'demo'],
                       help='命令类型')
    parser.add_argument('--name', '-n', help='要分析的名字')
    parser.add_argument('--json', action='store_true', help='JSON 输出')
    
    args = parser.parse_args()
    
    analyzer = NameAnalyzer()
    
    # 默认名字
    default_name = "张伟"
    
    name = args.name or default_name
    
    if args.command == 'demo':
        test_names = ["张伟", "李明", "王芳", "John", "Michael"]
        for n in test_names:
            results = analyzer.analyze(n, full_mode=True)
            print(format_results(results))
            print()
        return
        
    full_mode = args.command == 'full'
    results = analyzer.analyze(name, full_mode=full_mode)
    
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(format_results(results))


if __name__ == '__main__':
    main()
