#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版敏感词检查工具（离线模式）
仅使用本地词库，不进行任何网络请求。
"""

import argparse
import json
import os
import re
import sys
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Set

# 添加技能目录到路径
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir))


class SensitiveWordsCheckerEnhanced:
    """增强版敏感词检查器"""
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        初始化检查器
        
        Args:
            data_dir: 数据目录路径，用于存储敏感词库和缓存
        """
        self.data_dir = data_dir or os.path.join(skill_dir, "data", "sensitive_words")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 文件路径
        self.local_file = os.path.join(self.data_dir, "local_sensitive_words.json")
        self.cache_file = os.path.join(self.data_dir, "cache_metadata.json")
        self.update_history_file = os.path.join(self.data_dir, "update_history.json")
        
        # 加载敏感词库
        self.sensitive_words = self._load_sensitive_words()
        self.check_results = []
        
        # 文档类型映射到检查级别
        self.document_type_levels = {
            'meeting_minutes': 'strict',      # 会议纪要：严格
            'speech': 'normal',               # 发言稿：正常
            'discussion_outline': 'normal',   # 讨论提纲：正常
            'work_report': 'strict',          # 工作汇报：严格
            'notification': 'strict',         # 通知：严格
            'request_report': 'strict',       # 请示报告：严格
            'resolution': 'strict',           # 决议：严格
            'decision': 'strict',             # 决定：严格
            'announcement': 'normal',         # 公告：正常
            'standard': 'normal'              # 规范：正常
        }
    
    def _load_sensitive_words(self) -> Dict[str, Dict[str, Any]]:
        """加载敏感词库（纯离线模式，仅使用本地词库）"""
        local_words = self._load_local_words()
        return local_words or self._get_default_words()
    
    def _load_local_words(self) -> Optional[Dict[str, Dict[str, Any]]]:
        """加载本地敏感词库"""
        try:
            if os.path.exists(self.local_file):
                with open(self.local_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and 'categories' in data:
                        return data['categories']
                    return data
        except Exception as e:
            print(f"加载本地敏感词库失败：{e}")
        return None
    
    def _save_local_words(self, words: Dict[str, Dict[str, Any]]):
        """保存本地敏感词库"""
        try:
            data = {
                'version': '1.0.0',
                'last_updated': datetime.now().isoformat(),
                'categories': words
            }
            with open(self.local_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存本地敏感词库失败：{e}")
    

    def _record_update_history(self):
        """记录更新历史"""
        try:
            history = []
            if os.path.exists(self.update_history_file):
                with open(self.update_history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            
            history.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'update',
                'categories_count': len(self.sensitive_words)
            })
            
            # 只保留最近100条记录
            if len(history) > 100:
                history = history[-100:]
            
            with open(self.update_history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"记录更新历史失败：{e}")
    
    def _get_default_words(self) -> Dict[str, Dict[str, Any]]:
        """获取默认敏感词库"""
        return {
            'political': {
                'level': 'high',
                'words': [
                    '台独', '藏独', '疆独', '港独',
                    '法轮功', '全能神',
                    '反党', '反社会主义',
                    '六四', '八九',
                    '文革', '大跃进',
                    '颜色革命', '和平演变',
                    '政治阴谋', '颠覆政权'
                ],
                'description': '政治敏感词，绝对禁止使用'
            },
            'economic': {
                'level': 'medium',
                'words': [
                    '经济崩溃',
                    '金融危机爆发',
                    '大规模失业',
                    '通货膨胀失控',
                    '股市崩盘',
                    '房地产泡沫破裂',
                    '债务危机',
                    '经济硬着陆'
                ],
                'description': '经济敏感词，谨慎使用'
            },
            'social': {
                'level': 'medium',
                'words': [
                    '群体性事件',
                    '暴力冲突',
                    '社会动荡',
                    '政府失能',
                    '抗议示威',
                    '警民冲突',
                    '社会矛盾激化',
                    '不稳定因素'
                ],
                'description': '社会敏感词，需要谨慎处理'
            },
            'internal': {
                'level': 'high',
                'words': [
                    '内部矛盾激化',
                    '领导决策失误',
                    '重大工作失误',
                    '未公开人事调整',
                    '内部通报',
                    '纪律处分',
                    '组织处理',
                    '保密事项'
                ],
                'description': '内部敏感词，避免公开讨论'
            },
            'military': {
                'level': 'high',
                'words': [
                    '军事机密',
                    '武器装备',
                    '军事部署',
                    '国防预算',
                    '军事演习',
                    '战略武器',
                    '军事基地',
                    '军事情报'
                ],
                'description': '军事敏感词，禁止公开讨论'
            }
        }
    
    def check_text(self, text: str, document_type: Optional[str] = None, 
                   level: Optional[str] = None) -> Dict[str, Any]:
        """检查文本中的敏感词
        
        Args:
            text: 要检查的文本
            document_type: 文档类型，用于自动确定检查级别
            level: 手动指定的检查级别（覆盖文档类型自动选择）
            
        Returns:
            Dict: 检查结果
        """
        self.check_results = []
        
        # 确定检查级别
        if level is None and document_type is not None:
            level = self.document_type_levels.get(document_type, 'strict')
        elif level is None:
            level = 'strict'
        
        # 根据检查级别确定要检查的敏感词类别
        categories_to_check = self._get_categories_by_level(level)
        
        # 检查每个类别
        for category, config in self.sensitive_words.items():
            if category not in categories_to_check:
                continue
                
            words = config.get('words', [])
            category_level = config.get('level', 'medium')
            
            for word in words:
                # 使用正则表达式查找敏感词
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
                            'suggestion': self._get_suggestion(category, word),
                            'document_type': document_type,
                            'check_level': level
                        }
                        self.check_results.append(result)
        
        # 统计结果
        return self._generate_summary(document_type, level)
    
    def _get_categories_by_level(self, level: str) -> List[str]:
        """根据检查级别获取要检查的类别"""
        if level == 'strict':
            return ['political', 'economic', 'social', 'internal', 'military', 'cyber_security']
        elif level == 'normal':
            return ['political', 'economic', 'social', 'internal']
        elif level == 'lenient':
            return ['political', 'internal']
        else:
            return ['political']  # 默认只检查政治敏感词
    
    def _get_suggestion(self, category: str, word: str) -> str:
        """获取修改建议"""
        suggestions = {
            'political': f"建议删除或替换敏感政治词汇'{word}'，使用官方规范表述",
            'economic': f"建议使用更稳妥的经济表述替代'{word}'，如'经济调整'、'市场波动'等",
            'social': f"建议模糊处理或使用建设性表述替代'{word}'，如'社会管理'、'社区协调'等",
            'internal': f"建议删除内部敏感信息'{word}'，避免公开讨论，使用'内部工作'、'组织安排'等表述",
            'military': f"建议删除军事敏感词'{word}'，使用'国防建设'、'军队工作'等表述",
            'cyber_security': f"建议使用'网络安全'、'信息保护'等表述替代'{word}'",
            'recent_events': f"建议使用'近期情况'、'当前工作'等表述替代'{word}'"
        }
        
        return suggestions.get(category, f"建议检查并修改敏感词汇'{word}'，确保符合政策要求")
    
    def _generate_summary(self, document_type: Optional[str], check_level: str) -> Dict[str, Any]:
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
            'document_type': document_type,
            'check_level': check_level,
            'sensitive_count': len(self.check_results),
            'high_count': high_count,
            'medium_count': medium_count,
            'low_count': low_count,
            'category_stats': category_stats,
            'results': self.check_results,
            'recommendation': self._get_recommendation(valid, high_count, medium_count),
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_recommendation(self, valid: bool, high_count: int, medium_count: int) -> str:
        """获取处理建议"""
        if not valid:
            return "文档包含高级别敏感词，必须修改后才能使用。建议：1) 删除敏感词；2) 使用官方规范表述；3) 重新组织内容。"
        elif medium_count > 0:
            return "文档包含中级别敏感词，建议修改以降低风险。可以：1) 使用更稳妥的表述；2) 模糊处理敏感内容；3) 提供建设性意见。"
        elif high_count == 0 and medium_count == 0:
            return "文档敏感词检查通过，可以正常使用。建议：1) 继续保持严谨表述；2) 关注政策动态；3) 定期更新敏感词库。"
        else:
            return "文档敏感词检查基本通过，建议进一步优化表达方式。"
    
    def force_update(self) -> bool:
        """
        联网更新已禁用（出于安全考虑）。
        请使用 --import 参数手动导入本地词库文件。
        """
        print("⚠️  联网自动更新功能已禁用（安全策略）。")
        print("    如需更新词库，请使用：--import <词库文件.json>")
        return False
    
    def export_words(self, output_file: str) -> bool:
        """导出敏感词库"""
        try:
            data = {
                'version': '1.0.0',
                'export_time': datetime.now().isoformat(),
                'categories_count': len(self.sensitive_words),
                'categories': self.sensitive_words
            }
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"敏感词库已导出到：{output_file}")
            return True
        except Exception as e:
            print(f"导出敏感词库失败：{e}")
            return False
    
    def import_words(self, import_file: str) -> bool:
        """导入敏感词库"""
        try:
            with open(import_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'categories' in data:
                self.sensitive_words = data['categories']
                self._save_local_words(self.sensitive_words)
                print(f"敏感词库已从 {import_file} 导入")
                return True
            else:
                print("导入文件格式不正确")
                return False
        except Exception as e:
            print(f"导入敏感词库失败：{e}")
            return False


def main():
    parser = argparse.ArgumentParser(description='增强版敏感词检查工具')
    parser.add_argument('--file', help='要检查的文件路径')
    parser.add_argument('--text', help='直接检查文本内容')
    parser.add_argument('--document-type', help='文档类型（自动确定检查级别）',
                       choices=['meeting_minutes', 'speech', 'discussion_outline', 
                               'work_report', 'notification', 'request_report',
                               'resolution', 'decision', 'announcement', 'standard'])
    parser.add_argument('--level', default=None,
                       choices=['strict', 'normal', 'lenient'],
                       help='手动指定检查级别（覆盖文档类型自动选择）')
    parser.add_argument('--output', help='输出报告文件路径')
    parser.add_argument('--detailed', action='store_true', help='显示详细报告')
    parser.add_argument('--force-update', action='store_true', help='强制更新敏感词库')
    parser.add_argument('--export', help='导出敏感词库到指定文件')
    parser.add_argument('--import', dest='import_file', help='从指定文件导入敏感词库')
    parser.add_argument('--data-dir', help='数据目录路径')
    
    args = parser.parse_args()
    
    # 创建检查器
    checker = SensitiveWordsCheckerEnhanced(args.data_dir)
    
    # 处理特殊命令
    if args.force_update:
        if checker.force_update():
            print("敏感词库更新成功")
        else:
            print("敏感词库更新失败")
        return
    
    if args.export:
        if checker.export_words(args.export):
            print("导出成功")
        else:
            print("导出失败")
        return
    
    if args.import_file:
        if checker.import_words(args.import_file):
            print("导入成功")
        else:
            print("导入失败")
        return
    
    # 检查输入
    if not args.file and not args.text:
        print("错误：必须指定文件或文本")
        parser.print_help()
        sys.exit(1)
    
    # 执行检查
    if args.file:
        # 读取文件内容
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except UnicodeDecodeError:
            # 尝试其他编码
            with open(args.file, 'r', encoding='gbk', errors='ignore') as f:
                text = f.read()
        except Exception as e:
            print(f"读取文件失败：{e}")
            sys.exit(1)
    else:
        text = args.text
    
    # 执行检查
    results = checker.check_text(text, args.document_type, args.level)
    
    # 打印结果
    print("\n" + "="*80)
    print("增强版敏感词检查报告")
    print("="*80)
    
    if results['valid']:
        print("✅ 检查结果：通过")
    else:
        print("❌ 检查结果：未通过")
    
    print(f"\n📄 文档类型：{results.get('document_type', '未指定')}")
    print(f"📊 检查级别：{results.get('check_level', 'strict')}")
    print(f"🕒 检查时间：{results.get('timestamp', '未知')}")
    
    print(f"\n📈 统计信息：")
    print(f"   总敏感词数：{results['sensitive_count']}")
    print(f"   高级别敏感词：{results['high_count']}")
    print(f"   中级别敏感词：{results['medium_count']}")
    print(f"   低级别敏感词：{results['low_count']}")
    
    # 按类别统计
    category_stats = results.get('category_stats', {})
    if category_stats:
        print(f"\n📋 按类别统计：")
        for category, count in category_stats.items():
            print(f"   {category}: {count}个")
    
    # 详细结果
    if args.detailed and 'results' in results:
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
        print(f"\n💡 处理建议：")
        for line in recommendation.split('。'):
            if line.strip():
                print(f"   • {line.strip()}")
    
    # 保存报告
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"\n📁 报告已保存到：{args.output}")
        except Exception as e:
            print(f"保存报告失败：{e}")
    
    print("\n" + "="*80)
    
    # 返回退出码
    if not results['valid']:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()