#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
敏感词检查工具
检查文档中的敏感词，确保内容符合政策规定
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# 添加技能目录到路径
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir))


class SensitiveWordsChecker:
    """敏感词检查器"""
    
    def __init__(self):
        self.sensitive_words = self._load_sensitive_words()
        self.check_results = []
    
    def _load_sensitive_words(self) -> Dict[str, Dict[str, Any]]:
        """加载敏感词库"""
        # 这里可以从文件加载，这里先定义一些示例敏感词
        return {
            'political': {
                'level': 'high',
                'words': [
                    '台独', '藏独', '疆独', '港独',
                    '法轮功', '全能神',
                    '反党', '反社会主义',
                    '六四', '八九',
                    '文革', '大跃进'
                ],
                'description': '政治敏感词，绝对禁止使用'
            },
            'economic': {
                'level': 'medium',
                'words': [
                    '经济崩溃',
                    '金融危机爆发',
                    '大规模失业',
                    '通货膨胀失控'
                ],
                'description': '经济敏感词，谨慎使用'
            },
            'social': {
                'level': 'medium',
                'words': [
                    '群体性事件',
                    '暴力冲突',
                    '社会动荡',
                    '政府失能'
                ],
                'description': '社会敏感词，需要谨慎处理'
            },
            'internal': {
                'level': 'high',
                'words': [
                    '内部矛盾激化',
                    '领导决策失误',
                    '重大工作失误',
                    '未公开人事调整'
                ],
                'description': '内部敏感词，避免公开讨论'
            }
        }
    
    def check_text(self, text: str, level: str = 'strict') -> Dict[str, Any]:
        """检查文本中的敏感词
        
        Args:
            text: 要检查的文本
            level: 检查级别 (strict/normal/lenient)
            
        Returns:
            Dict: 检查结果
        """
        self.check_results = []
        
        # 根据检查级别确定要检查的敏感词类别
        categories_to_check = self._get_categories_by_level(level)
        
        # 检查每个类别
        for category, config in self.sensitive_words.items():
            if category not in categories_to_check:
                continue
                
            words = config.get('words', [])
            category_level = config.get('level', 'medium')
            
            for word in words:
                # 使用正则表达式查找敏感词（支持模糊匹配）
                pattern = re.escape(word)
                matches = list(re.finditer(pattern, text))
                
                if matches:
                    for match in matches:
                        # 获取上下文
                        start = max(0, match.start() - 20)
                        end = min(len(text), match.end() + 20)
                        context = text[start:end]
                        
                        # 如果是开头或结尾，添加标记
                        if start > 0:
                            context = "..." + context
                        if end < len(text):
                            context = context + "..."
                        
                        # 创建结果
                        result = {
                            'category': category,
                            'word': word,
                            'level': category_level,
                            'position': match.start(),
                            'context': context,
                            'description': config.get('description', ''),
                            'suggestion': self._get_suggestion(category, word)
                        }
                        self.check_results.append(result)
        
        # 统计结果
        return self._generate_summary()
    
    def check_file(self, file_path: str, level: str = 'strict') -> Dict[str, Any]:
        """检查文件中的敏感词
        
        Args:
            file_path: 文件路径
            level: 检查级别
            
        Returns:
            Dict: 检查结果
        """
        if not os.path.exists(file_path):
            return {
                'valid': False,
                'error': f"文件不存在：{file_path}",
                'results': []
            }
        
        try:
            # 根据文件类型读取内容
            if file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            elif file_path.endswith('.docx'):
                text = self._read_docx_file(file_path)
            else:
                # 尝试读取其他文本文件
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            
            return self.check_text(text, level)
            
        except Exception as e:
            return {
                'valid': False,
                'error': f"读取文件失败：{e}",
                'results': []
            }
    
    def check_directory(self, directory: str, level: str = 'strict') -> Dict[str, Any]:
        """检查目录下所有文件中的敏感词
        
        Args:
            directory: 目录路径
            level: 检查级别
            
        Returns:
            Dict: 检查结果
        """
        if not os.path.exists(directory):
            return {
                'valid': False,
                'error': f"目录不存在：{directory}",
                'results': []
            }
        
        all_results = []
        file_count = 0
        sensitive_files = 0
        
        # 遍历目录
        for root, dirs, files in os.walk(directory):
            for file in files:
                # 只检查文本相关文件
                if file.endswith(('.txt', '.docx', '.md', '.xml')):
                    file_path = os.path.join(root, file)
                    file_results = self.check_file(file_path, level)
                    
                    if file_results.get('sensitive_count', 0) > 0:
                        sensitive_files += 1
                        file_results['file_path'] = file_path
                        all_results.append(file_results)
                    
                    file_count += 1
        
        # 生成汇总报告
        total_sensitive = sum(r.get('sensitive_count', 0) for r in all_results)
        
        return {
            'valid': total_sensitive == 0,
            'file_count': file_count,
            'sensitive_files': sensitive_files,
            'total_sensitive': total_sensitive,
            'files': all_results
        }
    
    def _read_docx_file(self, file_path: str) -> str:
        """读取Word文档内容"""
        try:
            from docx import Document
            
            doc = Document(file_path)
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text
            
        except ImportError:
            print("警告：未安装python-docx库，无法读取Word文档")
            return ""
        except Exception as e:
            print(f"读取Word文档失败：{e}")
            return ""
    
    def _get_categories_by_level(self, level: str) -> List[str]:
        """根据检查级别获取要检查的类别"""
        if level == 'strict':
            return ['political', 'economic', 'social', 'internal']
        elif level == 'normal':
            return ['political', 'economic', 'social']
        elif level == 'lenient':
            return ['political']
        else:
            return ['political']  # 默认只检查政治敏感词
    
    def _get_suggestion(self, category: str, word: str) -> str:
        """获取修改建议"""
        suggestions = {
            'political': f"建议删除或替换敏感政治词汇'{word}'",
            'economic': f"建议使用更稳妥的经济表述替代'{word}'",
            'social': f"建议模糊处理或使用建设性表述替代'{word}'",
            'internal': f"建议删除内部敏感信息'{word}'，避免公开讨论"
        }
        
        return suggestions.get(category, f"建议检查并修改敏感词汇'{word}'")
    
    def _generate_summary(self) -> Dict[str, Any]:
        """生成检查结果汇总"""
        # 按级别统计
        high_count = len([r for r in self.check_results if r['level'] == 'high'])
        medium_count = len([r for r in self.check_results if r['level'] == 'medium'])
        low_count = len([r for r in self.check_results if r['level'] == 'low'])
        
        # 按类别统计
        category_stats = {}
        for result in self.check_results:
            category = result['category']
            category_stats[category] = category_stats.get(category, 0) + 1
        
        # 判断是否通过
        valid = high_count == 0  # 如果有高级别敏感词，则不通过
        
        return {
            'valid': valid,
            'sensitive_count': len(self.check_results),
            'high_count': high_count,
            'medium_count': medium_count,
            'low_count': low_count,
            'category_stats': category_stats,
            'results': self.check_results,
            'recommendation': self._get_recommendation(valid, high_count, medium_count)
        }
    
    def _get_recommendation(self, valid: bool, high_count: int, medium_count: int) -> str:
        """获取处理建议"""
        if not valid:
            return "文档包含高级别敏感词，必须修改后才能使用"
        elif medium_count > 0:
            return "文档包含中级别敏感词，建议修改以降低风险"
        elif high_count == 0 and medium_count == 0:
            return "文档敏感词检查通过，可以正常使用"
        else:
            return "文档敏感词检查基本通过，建议进一步优化"


def print_check_results(results: Dict[str, Any], detailed: bool = False):
    """打印检查结果"""
    print("\n" + "="*60)
    print("敏感词检查报告")
    print("="*60)
    
    if 'error' in results:
        print(f"❌ 检查失败：{results['error']}")
        return
    
    if results.get('valid', False):
        print("✅ 敏感词检查通过！")
    else:
        print("❌ 敏感词检查未通过！")
    
    print(f"\n📊 检查统计：")
    print(f"   总敏感词数：{results.get('sensitive_count', 0)}")
    print(f"   高级别敏感词：{results.get('high_count', 0)}")
    print(f"   中级别敏感词：{results.get('medium_count', 0)}")
    print(f"   低级别敏感词：{results.get('low_count', 0)}")
    
    # 按类别统计
    category_stats = results.get('category_stats', {})
    if category_stats:
        print(f"\n📈 按类别统计：")
        for category, count in category_stats.items():
            print(f"   {category}: {count}个")
    
    if detailed and 'results' in results:
        sensitive_results = results['results']
        if sensitive_results:
            print(f"\n🔍 详细结果（{len(sensitive_results)}个）：")
            for i, result in enumerate(sensitive_results, 1):
                print(f"\n   {i}. 【{result['category']}】{result['word']}")
                print(f"      级别：{result['level']}")
                print(f"      位置：第{result['position']}个字符")
                print(f"      上下文：{result['context']}")
                print(f"      建议：{result['suggestion']}")
    
    # 处理建议
    recommendation = results.get('recommendation', '')
    if recommendation:
        print(f"\n💡 处理建议：{recommendation}")
    
    print("\n" + "="*60)


def print_directory_results(results: Dict[str, Any], detailed: bool = False):
    """打印目录检查结果"""
    print("\n" + "="*60)
    print("目录敏感词检查报告")
    print("="*60)
    
    if 'error' in results:
        print(f"❌ 检查失败：{results['error']}")
        return
    
    print(f"📁 目录检查统计：")
    print(f"   检查文件数：{results.get('file_count', 0)}")
    print(f"   包含敏感词文件：{results.get('sensitive_files', 0)}")
    print(f"   总敏感词数：{results.get('total_sensitive', 0)}")
    
    if results.get('valid', False):
        print("\n✅ 目录敏感词检查通过！")
    else:
        print("\n❌ 目录敏感词检查未通过！")
    
    # 详细文件列表
    if detailed and 'files' in results:
        files = results['files']
        if files:
            print(f"\n📋 包含敏感词的文件（{len(files)}个）：")
            for i, file_result in enumerate(files, 1):
                file_path = file_result.get('file_path', '未知文件')
                sensitive_count = file_result.get('sensitive_count', 0)
                print(f"   {i}. {file_path} - {sensitive_count}个敏感词")
    
    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description='敏感词检查工具')
    parser.add_argument('--file', help='要检查的文件路径')
    parser.add_argument('--text', help='直接检查文本内容')
    parser.add_argument('--directory', help='检查目录下所有文件')
    parser.add_argument('--output', help='输出报告文件路径')
    parser.add_argument('--level', default='strict',
                       choices=['strict', 'normal', 'lenient'],
                       help='检查级别')
    parser.add_argument('--detailed', action='store_true', help='显示详细报告')
    
    args = parser.parse_args()
    
    # 检查输入
    if not args.file and not args.text and not args.directory:
        print("错误：必须指定文件、文本或目录")
        parser.print_help()
        sys.exit(1)
    
    checker = SensitiveWordsChecker()
    
    # 执行检查
    if args.file:
        results = checker.check_file(args.file, args.level)
        print_check_results(results, args.detailed)
    elif args.text:
        results = checker.check_text(args.text, args.level)
        print_check_results(results, args.detailed)
    elif args.directory:
        results = checker.check_directory(args.directory, args.level)
        print_directory_results(results, args.detailed)
    
    # 保存报告
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"\n报告已保存到：{args.output}")
        except Exception as e:
            print(f"保存报告失败：{e}")
    
    # 返回退出码
    if not results.get('valid', False):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()