#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档修订历史管理器
自动记录文档的修订历史，生成独立的JSON/TXT文件
"""

import json
import os
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import sys

# 添加技能目录到路径
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir))


class RevisionHistoryManager:
    """文档修订历史管理器"""
    
    def __init__(self, history_dir: Optional[str] = None):
        """
        初始化修订历史管理器
        
        Args:
            history_dir: 历史文件存储目录
        """
        self.history_dir = history_dir or os.path.join(skill_dir, "data", "revision_history")
        os.makedirs(self.history_dir, exist_ok=True)
        
        # 支持的输出格式
        self.supported_formats = ['json', 'txt', 'md', 'csv']
    
    def generate_document_hash(self, content: str) -> str:
        """
        生成文档内容的哈希值，用于识别文档版本
        
        Args:
            content: 文档内容
            
        Returns:
            str: 文档哈希值
        """
        # 使用SHA-256生成哈希
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]
    
    def create_revision_record(self, 
                              document_path: str,
                              document_type: str,
                              author: str,
                              action: str = 'create',
                              changes: Optional[List[Dict]] = None,
                              metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        创建修订记录
        
        Args:
            document_path: 文档路径
            document_type: 文档类型
            author: 作者/操作者
            action: 操作类型 (create, modify, review, approve, publish)
            changes: 变更内容列表
            metadata: 额外元数据
            
        Returns:
            Dict: 修订记录
        """
        timestamp = datetime.now()
        
        # 读取文档内容（如果存在）
        content_hash = None
        if os.path.exists(document_path):
            try:
                with open(document_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    content_hash = self.generate_document_hash(content)
            except:
                content_hash = "unknown"
        
        # 构建修订记录
        record = {
            'id': self._generate_record_id(),
            'timestamp': timestamp.isoformat(),
            'document_path': document_path,
            'document_name': os.path.basename(document_path),
            'document_type': document_type,
            'content_hash': content_hash,
            'author': author,
            'action': action,
            'changes': changes or [],
            'metadata': metadata or {},
            'version': '1.0'
        }
        
        return record
    
    def save_revision_history(self, 
                             document_path: str,
                             records: List[Dict[str, Any]],
                             output_format: str = 'json',
                             include_all: bool = True) -> str:
        """
        保存修订历史到文件
        
        Args:
            document_path: 文档路径
            records: 修订记录列表
            output_format: 输出格式 (json, txt, md, csv)
            include_all: 是否包含所有记录（否则只包含最新记录）
            
        Returns:
            str: 保存的文件路径
        """
        if output_format not in self.supported_formats:
            output_format = 'json'
        
        # 生成文件名
        doc_name = os.path.splitext(os.path.basename(document_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{doc_name}_revision_history_{timestamp}.{output_format}"
        output_path = os.path.join(self.history_dir, filename)
        
        # 准备数据
        if not include_all and records:
            data = records[-1]  # 只保存最新记录
        else:
            data = {
                'document': document_path,
                'total_revisions': len(records),
                'first_revision': records[0]['timestamp'] if records else None,
                'last_revision': records[-1]['timestamp'] if records else None,
                'revisions': records
            }
        
        # 根据格式保存
        if output_format == 'json':
            self._save_as_json(output_path, data)
        elif output_format == 'txt':
            self._save_as_txt(output_path, data)
        elif output_format == 'md':
            self._save_as_markdown(output_path, data)
        elif output_format == 'csv':
            self._save_as_csv(output_path, data)
        
        return output_path
    
    def _save_as_json(self, filepath: str, data: Union[Dict, List]):
        """保存为JSON格式"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _save_as_txt(self, filepath: str, data: Union[Dict, List]):
        """保存为TXT格式"""
        with open(filepath, 'w', encoding='utf-8') as f:
            if isinstance(data, dict) and 'revisions' in data:
                # 完整历史
                f.write(f"文档修订历史\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"文档路径：{data.get('document', '未知')}\n")
                f.write(f"总修订次数：{data.get('total_revisions', 0)}\n")
                f.write(f"首次修订：{data.get('first_revision', '未知')}\n")
                f.write(f"最后修订：{data.get('last_revision', '未知')}\n\n")
                
                f.write("修订记录：\n")
                f.write("-" * 50 + "\n")
                for i, revision in enumerate(data['revisions'], 1):
                    f.write(f"\n{i}. 修订ID：{revision.get('id', '未知')}\n")
                    f.write(f"   时间：{revision.get('timestamp', '未知')}\n")
                    f.write(f"   操作：{revision.get('action', '未知')}\n")
                    f.write(f"   作者：{revision.get('author', '未知')}\n")
                    f.write(f"   文档类型：{revision.get('document_type', '未知')}\n")
                    
                    changes = revision.get('changes', [])
                    if changes:
                        f.write(f"   变更内容：\n")
                        for change in changes:
                            f.write(f"     - {change.get('description', '未知')}\n")
                    
                    metadata = revision.get('metadata', {})
                    if metadata:
                        f.write(f"   元数据：{json.dumps(metadata, ensure_ascii=False)}\n")
                    
                    f.write(f"   内容哈希：{revision.get('content_hash', '未知')}\n")
            elif isinstance(data, dict):
                # 单个记录
                f.write(f"修订记录详情\n")
                f.write("=" * 50 + "\n\n")
                for key, value in data.items():
                    f.write(f"{key}: {value}\n")
            else:
                # 列表格式
                for i, item in enumerate(data, 1):
                    f.write(f"记录{i}: {json.dumps(item, ensure_ascii=False)}\n\n")
    
    def _save_as_markdown(self, filepath: str, data: Union[Dict, List]):
        """保存为Markdown格式"""
        with open(filepath, 'w', encoding='utf-8') as f:
            if isinstance(data, dict) and 'revisions' in data:
                # 完整历史
                f.write("# 文档修订历史\n\n")
                f.write(f"**文档路径**：`{data.get('document', '未知')}`\n\n")
                f.write(f"**总修订次数**：{data.get('total_revisions', 0)}\n\n")
                f.write(f"**首次修订**：{data.get('first_revision', '未知')}\n\n")
                f.write(f"**最后修订**：{data.get('last_revision', '未知')}\n\n")
                
                f.write("## 修订记录\n\n")
                for i, revision in enumerate(data['revisions'], 1):
                    f.write(f"### {i}. 修订ID：{revision.get('id', '未知')}\n\n")
                    f.write(f"- **时间**：{revision.get('timestamp', '未知')}\n")
                    f.write(f"- **操作**：`{revision.get('action', '未知')}`\n")
                    f.write(f"- **作者**：{revision.get('author', '未知')}\n")
                    f.write(f"- **文档类型**：{revision.get('document_type', '未知')}\n")
                    
                    changes = revision.get('changes', [])
                    if changes:
                        f.write(f"- **变更内容**：\n")
                        for change in changes:
                            f.write(f"  - {change.get('description', '未知')}\n")
                    
                    metadata = revision.get('metadata', {})
                    if metadata:
                        f.write(f"- **元数据**：\n")
                        f.write(f"  ```json\n")
                        f.write(f"  {json.dumps(metadata, ensure_ascii=False, indent=2)}\n")
                        f.write(f"  ```\n")
                    
                    f.write(f"- **内容哈希**：`{revision.get('content_hash', '未知')}`\n\n")
            elif isinstance(data, dict):
                # 单个记录
                f.write("# 修订记录详情\n\n")
                f.write("| 字段 | 值 |\n")
                f.write("|------|-----|\n")
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        value_str = json.dumps(value, ensure_ascii=False)
                    else:
                        value_str = str(value)
                    f.write(f"| {key} | {value_str} |\n")
            else:
                # 列表格式
                f.write("# 修订记录列表\n\n")
                for i, item in enumerate(data, 1):
                    f.write(f"## 记录{i}\n\n")
                    f.write(f"```json\n")
                    f.write(f"{json.dumps(item, ensure_ascii=False, indent=2)}\n")
                    f.write(f"```\n\n")
    
    def _save_as_csv(self, filepath: str, data: Union[Dict, List]):
        """保存为CSV格式"""
        import csv
        
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            
            if isinstance(data, dict) and 'revisions' in data:
                # 写标题行
                writer.writerow([
                    'ID', 'Timestamp', 'Document', 'Document Type', 
                    'Action', 'Author', 'Content Hash', 'Changes Count'
                ])
                
                # 写数据行
                for revision in data['revisions']:
                    changes_count = len(revision.get('changes', []))
                    writer.writerow([
                        revision.get('id', ''),
                        revision.get('timestamp', ''),
                        revision.get('document_name', ''),
                        revision.get('document_type', ''),
                        revision.get('action', ''),
                        revision.get('author', ''),
                        revision.get('content_hash', ''),
                        changes_count
                    ])
            elif isinstance(data, list):
                # 写标题行（根据第一个记录动态生成）
                if data:
                    first_record = data[0]
                    headers = list(first_record.keys())
                    writer.writerow(headers)
                    
                    # 写数据行
                    for record in data:
                        row = [record.get(key, '') for key in headers]
                        writer.writerow(row)
    
    def load_revision_history(self, history_file: str) -> Optional[Union[Dict, List]]:
        """
        加载修订历史文件
        
        Args:
            history_file: 历史文件路径
            
        Returns:
            Union[Dict, List]: 历史数据
        """
        if not os.path.exists(history_file):
            return None
        
        try:
            if history_file.endswith('.json'):
                with open(history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # 对于非JSON格式，返回文件内容
                with open(history_file, 'r', encoding='utf-8') as f:
                    return {'content': f.read(), 'filepath': history_file}
        except Exception as e:
            print(f"加载修订历史失败：{e}")
            return None
    
    def get_document_history(self, document_path: str, max_records: int = 10) -> List[str]:
        """
        获取文档的历史文件列表
        
        Args:
            document_path: 文档路径
            max_records: 最大记录数
            
        Returns:
            List[str]: 历史文件路径列表
        """
        doc_name = os.path.splitext(os.path.basename(document_path))[0]
        pattern = f"{doc_name}_revision_history_*"
        
        history_files = []
        for file in os.listdir(self.history_dir):
            if file.startswith(f"{doc_name}_revision_history_"):
                history_files.append(os.path.join(self.history_dir, file))
        
        # 按修改时间排序（最新的在前）
        history_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        return history_files[:max_records]
    
    def compare_revisions(self, old_file: str, new_file: str) -> List[Dict]:
        """
        比较两个版本的差异
        
        Args:
            old_file: 旧版本文件路径
            new_file: 新版本文件路径
            
        Returns:
            List[Dict]: 差异列表
        """
        differences = []
        
        try:
            # 读取文件内容
            with open(old_file, 'r', encoding='utf-8') as f:
                old_content = f.read()
            
            with open(new_file, 'r', encoding='utf-8') as f:
                new_content = f.read()
            
            # 生成哈希
            old_hash = self.generate_document_hash(old_content)
            new_hash = self.generate_document_hash(new_content)
            
            if old_hash == new_hash:
                differences.append({
                    'type': 'unchanged',
                    'description': '文档内容未发生变化'
                })
                return differences
            
            # 简单比较：行数变化
            old_lines = old_content.splitlines()
            new_lines = new_content.splitlines()
            
            lines_added = len(new_lines) - len(old_lines)
            if lines_added > 0:
                differences.append({
                    'type': 'lines_added',
                    'description': f'增加了 {lines_added} 行内容'
                })
            elif lines_added < 0:
                differences.append({
                    'type': 'lines_removed',
                    'description': f'删除了 {-lines_added} 行内容'
                })
            
            # 字符数变化
            chars_added = len(new_content) - len(old_content)
            if chars_added > 0:
                differences.append({
                    'type': 'chars_added',
                    'description': f'增加了 {chars_added} 个字符'
                })
            elif chars_added < 0:
                differences.append({
                    'type': 'chars_removed',
                    'description': f'删除了 {-chars_added} 个字符'
                })
            
            # 内容哈希变化
            differences.append({
                'type': 'hash_changed',
                'description': f'内容哈希已变更：{old_hash[:8]}... → {new_hash[:8]}...'
            })
            
        except Exception as e:
            differences.append({
                'type': 'error',
                'description': f'比较文件时出错：{e}'
            })
        
        return differences
    
    def _generate_record_id(self) -> str:
        """生成记录ID"""
        timestamp = int(time.time() * 1000)
        random_part = hashlib.md5(str(timestamp).encode()).hexdigest()[:8]
        return f"REV_{timestamp}_{random_part}"


class DocumentRevisionTracker:
    """文档修订跟踪器（集成到文档生成流程中）"""
    
    def __init__(self, history_manager: RevisionHistoryManager):
        self.history_manager = history_manager
        self.current_revisions = {}  # 文档路径 -> 修订记录列表
    
    def track_document_creation(self, 
                               document_path: str,
                               document_type: str,
                               author: str,
                               metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        跟踪文档创建
        
        Args:
            document_path: 文档路径
            document_type: 文档类型
            author: 作者
            metadata: 额外元数据
            
        Returns:
            Dict: 创建记录
        """
        record = self.history_manager.create_revision_record(
            document_path=document_path,
            document_type=document_type,
            author=author,
            action='create',
            changes=[{'type': 'create', 'description': '文档创建'}],
            metadata=metadata
        )
        
        # 保存到内存
        if document_path not in self.current_revisions:
            self.current_revisions[document_path] = []
        self.current_revisions[document_path].append(record)
        
        # 立即保存历史文件
        history_file = self.history_manager.save_revision_history(
            document_path=document_path,
            records=self.current_revisions[document_path],
            output_format='json'
        )
        
        record['history_file'] = history_file
        return record
    
    def track_document_modification(self,
                                   document_path: str,
                                   document_type: str,
                                   author: str,
                                   changes: List[Dict],
                                   metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        跟踪文档修改
        
        Args:
            document_path: 文档路径
            document_type: 文档类型
            author: 作者
            changes: 变更内容列表
            metadata: 额外元数据
            
        Returns:
            Dict: 修改记录
        """
        record = self.history_manager.create_revision_record(
            document_path=document_path,
            document_type=document_type,
            author=author,
            action='modify',
            changes=changes,
            metadata=metadata
        )
        
        # 保存到内存
        if document_path not in self.current_revisions:
            self.current_revisions[document_path] = []
        self.current_revisions[document_path].append(record)
        
        # 立即保存历史文件
        history_file = self.history_manager.save_revision_history(
            document_path=document_path,
            records=self.current_revisions[document_path],
            output_format='json'
        )
        
        record['history_file'] = history_file
        return record
    
    def save_all_histories(self, output_format: str = 'json') -> List[str]:
        """
        保存所有文档的修订历史
        
        Args:
            output_format: 输出格式
            
        Returns:
            List[str]: 保存的文件路径列表
        """
        saved_files = []
        
        for doc_path, records in self.current_revisions.items():
            if records:
                history_file = self.history_manager.save_revision_history(
                    document_path=doc_path,
                    records=records,
                    output_format=output_format
                )
                saved_files.append(history_file)
        
        return saved_files
    
    def get_document_summary(self, document_path: str) -> Dict[str, Any]:
        """
        获取文档修订摘要
        
        Args:
            document_path: 文档路径
            
        Returns:
            Dict: 修订摘要
        """
        if document_path not in self.current_revisions:
            return {'revision_count': 0, 'latest_revision': None}
        
        records = self.current_revisions[document_path]
        if not records:
            return {'revision_count': 0, 'latest_revision': None}
        
        return {
            'revision_count': len(records),
            'first_revision': records[0]['timestamp'],
            'latest_revision': records[-1]['timestamp'],
            'latest_action': records[-1]['action'],
            'latest_author': records[-1]['author'],
            'revision_ids': [r['id'] for r in records]
        }


def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='文档修订历史管理器')
    parser.add_argument('--document', help='文档路径')
    parser.add_argument('--document-type', help='文档类型')
    parser.add_argument('--author', help='作者/操作者')
    parser.add_argument('--action', choices=['create', 'modify', 'review', 'approve', 'publish'],
                       default='create', help='操作类型')
    parser.add_argument('--changes', help='变更描述（JSON格式）')
    parser.add_argument('--metadata', help='额外元数据（JSON格式）')
    parser.add_argument('--output-format', choices=['json', 'txt', 'md', 'csv'],
                       default='json', help='输出格式')
    parser.add_argument('--load-history', help='加载历史文件')
    parser.add_argument('--list-history', action='store_true', help='列出文档历史文件')
    parser.add_argument('--compare', nargs=2, metavar=('OLD', 'NEW'), help='比较两个版本')
    parser.add_argument('--history-dir', help='历史文件存储目录')
    
    args = parser.parse_args()
    
    # 创建管理器
    manager = RevisionHistoryManager(args.history_dir)
    
    # 根据参数执行相应操作
    if args.load_history:
        # 加载历史文件
        history = manager.load_revision_history(args.load_history)
        if history:
            print(f"加载历史文件：{args.load_history}")
            print(json.dumps(history, ensure_ascii=False, indent=2))
        else:
            print(f"无法加载历史文件：{args.load_history}")
    
    elif args.list_history and args.document:
        # 列出文档历史
        history_files = manager.get_document_history(args.document)
        if history_files:
            print(f"文档 '{args.document}' 的历史文件：")
            for i, file in enumerate(history_files, 1):
                mtime = datetime.fromtimestamp(os.path.getmtime(file))
                print(f"{i}. {file} (修改时间：{mtime})")
        else:
            print(f"文档 '{args.document}' 无历史记录")
    
    elif args.compare:
        # 比较两个版本
        differences = manager.compare_revisions(args.compare[0], args.compare[1])
        print(f"比较结果：{args.compare[0]} ←→ {args.compare[1]}")
        for diff in differences:
            print(f"  • {diff['description']}")
    
    elif args.document and args.author and args.document_type:
        # 创建修订记录
        changes = []
        if args.changes:
            try:
                changes = json.loads(args.changes)
            except:
                changes = [{'type': 'manual', 'description': args.changes}]
        
        metadata = {}
        if args.metadata:
            try:
                metadata = json.loads(args.metadata)
            except:
                metadata = {'note': args.metadata}
        
        record = manager.create_revision_record(
            document_path=args.document,
            document_type=args.document_type,
            author=args.author,
            action=args.action,
            changes=changes,
            metadata=metadata
        )
        
        # 保存记录
        history_file = manager.save_revision_history(
            document_path=args.document,
            records=[record],
            output_format=args.output_format,
            include_all=False
        )
        
        print(f"创建修订记录：{record['id']}")
        print(f"保存到：{history_file}")
        print(json.dumps(record, ensure_ascii=False, indent=2))
    
    else:
        print("请提供有效的参数组合")
        parser.print_help()


if __name__ == "__main__":
    main()