#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 知识教学技能 - 知识更新脚本

功能:
- 添加新知识点
- 更新现有知识
- 删除知识条目
- 查看知识统计
- 导出知识报告
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List


class KnowledgeUpdater:
    """知识库更新器"""
    
    def __init__(self, knowledge_file: str):
        self.knowledge_file = knowledge_file
        self.backup_dir = Path(knowledge_file).parent / 'backups'
        self.backup_dir.mkdir(exist_ok=True)
        self.content = self._load_content()
        self.metadata = self._parse_metadata()
    
    def _load_content(self) -> str:
        """加载知识库内容"""
        with open(self.knowledge_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _save_content(self, content: str):
        """保存知识库内容"""
        with open(self.knowledge_file, 'w', encoding='utf-8') as f:
            f.write(content)
        self.content = content
    
    def _parse_metadata(self) -> dict:
        """解析知识库元数据"""
        metadata = {
            'version': '1.0.0',
            'last_update': datetime.now().strftime('%Y-%m-%d')
        }
        
        # 从文件头部解析版本信息
        version_match = re.search(r'> 版本: ([\d.]+)', self.content)
        if version_match:
            metadata['version'] = version_match.group(1)
        
        date_match = re.search(r'最后更新: ([\d-]+)', self.content)
        if date_match:
            metadata['last_update'] = date_match.group(1)
        
        return metadata
    
    def _backup(self):
        """创建备份"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = self.backup_dir / f'knowledge_base_{timestamp}.md'
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(self.content)
        
        print(f"备份已创建: {backup_file}")
        return backup_file
    
    def _update_metadata(self):
        """更新元数据"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 更新日期
        self.content = re.sub(
            r'最后更新: [\d-]+',
            f'最后更新: {today}',
            self.content
        )
    
    def get_sections(self) -> List[Dict]:
        """获取所有章节"""
        sections = []
        pattern = r'^## (\d+)\. (.+)$'
        
        for match in re.finditer(pattern, self.content, re.MULTILINE):
            sections.append({
                'number': match.group(1),
                'title': match.group(2),
                'start': match.start(),
                'end': match.end()
            })
        
        return sections
    
    def add_knowledge(self, category: str, title: str, content: str, 
                      position: str = 'end') -> bool:
        """添加新知识点
        
        Args:
            category: 知识分类（章节编号或名称）
            title: 知识标题
            content: 知识内容
            position: 插入位置 ('start', 'end', 'after:标题')
        
        Returns:
            是否成功
        """
        # 创建备份
        self._backup()
        
        # 查找目标章节
        sections = self.get_sections()
        target_section = None
        
        for section in sections:
            if category == section['number'] or category.lower() in section['title'].lower():
                target_section = section
                break
        
        if not target_section:
            print(f"错误: 未找到分类 '{category}'")
            return False
        
        # 构建新内容
        new_content = f"\n\n### {title}\n\n{content}\n"
        
        # 找到插入位置
        if position == 'start':
            insert_pos = target_section['end']
        elif position == 'end':
            # 找到章节结束位置
            next_section_start = len(self.content)
            for s in sections:
                if s['start'] > target_section['start']:
                    next_section_start = s['start']
                    break
            insert_pos = next_section_start - 1
        elif position.startswith('after:'):
            after_title = position[6:]
            # 查找指定标题后的位置
            pattern = rf'### {re.escape(after_title)}.*?(?=###|\Z)'
            match = re.search(pattern, self.content[target_section['start']:], re.DOTALL)
            if match:
                insert_pos = target_section['start'] + match.end()
            else:
                insert_pos = target_section['end']
        else:
            insert_pos = target_section['end']
        
        # 插入新内容
        new_file_content = (
            self.content[:insert_pos] + 
            new_content + 
            self.content[insert_pos:]
        )
        
        # 更新元数据并保存
        self._save_content(new_file_content)
        self._update_metadata()
        self._save_content(self.content)
        
        print(f"知识点已添加: {title}")
        return True
    
    def update_knowledge(self, title: str, new_content: str) -> bool:
        """更新现有知识点
        
        Args:
            title: 要更新的知识标题
            new_content: 新内容
        
        Returns:
            是否成功
        """
        # 创建备份
        self._backup()
        
        # 查找知识点
        pattern = rf'(### {re.escape(title)}\n)(.*?)(?=\n###|\n## |\Z)'
        match = re.search(pattern, self.content, re.DOTALL)
        
        if not match:
            print(f"错误: 未找到知识点 '{title}'")
            return False
        
        # 替换内容
        new_file_content = (
            self.content[:match.start(2)] + 
            f'\n{new_content}\n' + 
            self.content[match.end(2):]
        )
        
        # 更新元数据并保存
        self._save_content(new_file_content)
        self._update_metadata()
        self._save_content(self.content)
        
        print(f"知识点已更新: {title}")
        return True
    
    def delete_knowledge(self, title: str) -> bool:
        """删除知识点
        
        Args:
            title: 要删除的知识标题
        
        Returns:
            是否成功
        """
        # 创建备份
        self._backup()
        
        # 查找知识点
        pattern = rf'\n*### {re.escape(title)}\n.*?(?=\n###|\n## |\Z)'
        match = re.search(pattern, self.content, re.DOTALL)
        
        if not match:
            print(f"错误: 未找到知识点 '{title}'")
            return False
        
        # 删除内容
        new_file_content = self.content[:match.start()] + self.content[match.end():]
        
        # 更新元数据并保存
        self._save_content(new_file_content)
        self._update_metadata()
        self._save_content(self.content)
        
        print(f"知识点已删除: {title}")
        return True
    
    def search_knowledge(self, keyword: str) -> List[Dict]:
        """搜索知识点
        
        Args:
            keyword: 搜索关键词
        
        Returns:
            匹配的知识点列表
        """
        results = []
        
        # 搜索标题
        title_pattern = rf'### (.+{re.escape(keyword)}.+)'
        for match in re.finditer(title_pattern, self.content, re.IGNORECASE):
            results.append({
                'type': 'title',
                'title': match.group(1),
                'position': match.start()
            })
        
        # 搜索内容
        content_pattern = rf'(### [^\n]+)\n([^\n]*{re.escape(keyword)}[^\n]*)'
        for match in re.finditer(content_pattern, self.content, re.IGNORECASE):
            title = match.group(1).replace('### ', '')
            context = match.group(2)[:100] + '...' if len(match.group(2)) > 100 else match.group(2)
            
            # 避免重复
            if not any(r['title'] == title for r in results):
                results.append({
                    'type': 'content',
                    'title': title,
                    'context': context,
                    'position': match.start()
                })
        
        return results
    
    def get_statistics(self) -> Dict:
        """获取知识库统计信息"""
        sections = self.get_sections()
        
        # 统计各章节数量
        section_stats = []
        for section in sections:
            # 计算子章节数量
            section_content = self.content[section['end']:]
            next_section = len(self.content)
            for s in sections:
                if s['start'] > section['start']:
                    next_section = s['start']
                    break
            
            subsection_count = len(re.findall(r'^### ', 
                self.content[section['end']:next_section], re.MULTILINE))
            
            section_stats.append({
                'number': section['number'],
                'title': section['title'],
                'subsections': subsection_count
            })
        
        # 统计代码块数量
        code_blocks = len(re.findall(r'```', self.content)) // 2
        
        # 统计表格数量
        tables = len(re.findall(r'^\|.*\|$', self.content, re.MULTILINE))
        
        return {
            'version': self.metadata['version'],
            'last_update': self.metadata['last_update'],
            'total_sections': len(sections),
            'total_subsections': sum(s['subsections'] for s in section_stats),
            'code_blocks': code_blocks,
            'tables': tables,
            'sections': section_stats
        }
    
    def export_report(self, output_path: str) -> bool:
        """导出知识报告
        
        Args:
            output_path: 输出文件路径
        
        Returns:
            是否成功
        """
        stats = self.get_statistics()
        
        report = f"""# OpenClaw 知识库报告

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 基本信息

- **版本**: {stats['version']}
- **最后更新**: {stats['last_update']}
- **章节数**: {stats['total_sections']}
- **子章节数**: {stats['total_subsections']}
- **代码块数**: {stats['code_blocks']}
- **表格数**: {stats['tables']}

## 章节详情

| 章节 | 标题 | 子章节数 |
|------|------|----------|
"""
        
        for section in stats['sections']:
            report += f"| {section['number']} | {section['title']} | {section['subsections']} |\n"
        
        report += """
## 更新历史

请查看 backups 目录中的备份文件。

---
*本报告由 OpenClaw 知识教学技能自动生成*
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"报告已导出: {output_path}")
        return True
    
    def list_backups(self) -> List[str]:
        """列出所有备份"""
        backups = sorted(self.backup_dir.glob('knowledge_base_*.md'), reverse=True)
        return [str(b) for b in backups]
    
    def restore_backup(self, backup_file: str) -> bool:
        """恢复备份
        
        Args:
            backup_file: 备份文件路径
        
        Returns:
            是否成功
        """
        if not os.path.exists(backup_file):
            print(f"错误: 备份文件不存在: {backup_file}")
            return False
        
        # 创建当前状态的备份
        self._backup()
        
        # 恢复备份
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_content = f.read()
        
        self._save_content(backup_content)
        print(f"已恢复备份: {backup_file}")
        return True


def main():
    parser = argparse.ArgumentParser(description='OpenClaw 知识库更新工具')
    parser.add_argument('--knowledge', '-k',
                       default=os.path.join(os.path.dirname(__file__), '..', 'KNOWLEDGE_BASE.md'),
                       help='知识库文件路径')
    
    subparsers = parser.add_subparsers(dest='action', help='可用操作')
    
    # 添加知识
    add_parser = subparsers.add_parser('add', help='添加新知识点')
    add_parser.add_argument('--category', '-c', required=True, help='知识分类')
    add_parser.add_argument('--title', '-t', required=True, help='知识标题')
    add_parser.add_argument('--content', required=True, help='知识内容')
    add_parser.add_argument('--position', default='end', 
                           help='插入位置 (start/end/after:标题)')
    
    # 更新知识
    update_parser = subparsers.add_parser('update', help='更新知识点')
    update_parser.add_argument('--title', '-t', required=True, help='知识标题')
    update_parser.add_argument('--content', required=True, help='新内容')
    
    # 删除知识
    delete_parser = subparsers.add_parser('delete', help='删除知识点')
    delete_parser.add_argument('--title', '-t', required=True, help='知识标题')
    
    # 搜索知识
    search_parser = subparsers.add_parser('search', help='搜索知识点')
    search_parser.add_argument('--keyword', '-k', required=True, help='搜索关键词')
    
    # 统计信息
    stats_parser = subparsers.add_parser('stats', help='显示知识库统计')
    
    # 导出报告
    export_parser = subparsers.add_parser('export', help='导出知识报告')
    export_parser.add_argument('--output', '-o', required=True, help='输出文件路径')
    
    # 备份管理
    backup_parser = subparsers.add_parser('backup', help='备份管理')
    backup_parser.add_argument('--list', action='store_true', help='列出所有备份')
    backup_parser.add_argument('--restore', help='恢复指定备份')
    
    args = parser.parse_args()
    
    updater = KnowledgeUpdater(args.knowledge)
    
    if args.action == 'add':
        updater.add_knowledge(args.category, args.title, args.content, args.position)
    elif args.action == 'update':
        updater.update_knowledge(args.title, args.content)
    elif args.action == 'delete':
        updater.delete_knowledge(args.title)
    elif args.action == 'search':
        results = updater.search_knowledge(args.keyword)
        if results:
            print(f"找到 {len(results)} 个结果:")
            for r in results:
                print(f"  - [{r['type']}] {r['title']}")
                if 'context' in r:
                    print(f"    {r['context']}")
        else:
            print("未找到匹配的知识点")
    elif args.action == 'stats':
        stats = updater.get_statistics()
        print(f"知识库版本: {stats['version']}")
        print(f"最后更新: {stats['last_update']}")
        print(f"章节数: {stats['total_sections']}")
        print(f"子章节数: {stats['total_subsections']}")
        print(f"代码块数: {stats['code_blocks']}")
        print(f"表格数: {stats['tables']}")
    elif args.action == 'export':
        updater.export_report(args.output)
    elif args.action == 'backup':
        if args.list:
            backups = updater.list_backups()
            if backups:
                print("可用备份:")
                for b in backups:
                    print(f"  - {b}")
            else:
                print("暂无备份")
        elif args.restore:
            updater.restore_backup(args.restore)
        else:
            updater._backup()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
