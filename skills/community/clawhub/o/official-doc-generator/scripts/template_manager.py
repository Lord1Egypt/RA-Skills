#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模板管理器
管理文档模板的创建、更新和使用
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# 添加技能目录到路径
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir))


class TemplateManager:
    """文档模板管理器"""
    
    def __init__(self, templates_dir: str = None):
        if templates_dir is None:
            # 默认模板目录
            self.templates_dir = Path(__file__).parent.parent / 'assets' / 'templates'
        else:
            self.templates_dir = Path(templates_dir)
        
        # 确保模板目录存在
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # 模板配置文件
        self.config_file = self.templates_dir / 'templates_config.json'
        self.templates_config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载模板配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"警告：加载模板配置失败，将创建新配置：{e}")
        
        # 默认配置
        return {
            'version': '1.0.0',
            'last_updated': datetime.now().isoformat(),
            'templates': {}
        }
    
    def _save_config(self):
        """保存模板配置"""
        self.templates_config['last_updated'] = datetime.now().isoformat()
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.templates_config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存模板配置失败：{e}")
    
    def list_templates(self, template_type: str = None) -> List[Dict[str, Any]]:
        """列出所有模板
        
        Args:
            template_type: 模板类型过滤
            
        Returns:
            List: 模板列表
        """
        templates = []
        
        # 从配置中获取模板信息
        config_templates = self.templates_config.get('templates', {})
        
        # 扫描模板目录
        for file_path in self.templates_dir.glob('*.docx'):
            if file_path.name == 'templates_config.json':
                continue
                
            template_name = file_path.stem
            template_info = config_templates.get(template_name, {})
            
            # 过滤模板类型
            if template_type and template_info.get('type') != template_type:
                continue
            
            # 获取文件信息
            stat = file_path.stat()
            
            template_data = {
                'name': template_name,
                'file_path': str(file_path),
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'type': template_info.get('type', 'unknown'),
                'description': template_info.get('description', ''),
                'version': template_info.get('version', '1.0.0'),
                'author': template_info.get('author', ''),
                'tags': template_info.get('tags', [])
            }
            templates.append(template_data)
        
        return templates
    
    def get_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """获取模板信息
        
        Args:
            template_name: 模板名称（不含扩展名）
            
        Returns:
            Dict: 模板信息，如果不存在返回None
        """
        template_path = self.templates_dir / f"{template_name}.docx"
        
        if not template_path.exists():
            return None
        
        # 从配置中获取模板信息
        config_templates = self.templates_config.get('templates', {})
        template_info = config_templates.get(template_name, {})
        
        # 获取文件信息
        stat = template_path.stat()
        
        return {
            'name': template_name,
            'file_path': str(template_path),
            'size': stat.st_size,
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'type': template_info.get('type', 'unknown'),
            'description': template_info.get('description', ''),
            'version': template_info.get('version', '1.0.0'),
            'author': template_info.get('author', ''),
            'tags': template_info.get('tags', []),
            'fields': template_info.get('fields', []),
            'usage': template_info.get('usage', '')
        }
    
    def create_template(self, source_file: str, template_name: str, 
                       template_type: str, description: str = '',
                       author: str = '', tags: List[str] = None,
                       fields: List[str] = None) -> bool:
        """创建新模板
        
        Args:
            source_file: 源文件路径
            template_name: 模板名称
            template_type: 模板类型
            description: 模板描述
            author: 作者
            tags: 标签列表
            fields: 字段列表
            
        Returns:
            bool: 是否创建成功
        """
        if not os.path.exists(source_file):
            print(f"错误：源文件不存在：{source_file}")
            return False
        
        # 检查模板是否已存在
        template_path = self.templates_dir / f"{template_name}.docx"
        if template_path.exists():
            print(f"错误：模板已存在：{template_name}")
            return False
        
        try:
            # 复制文件到模板目录
            shutil.copy2(source_file, template_path)
            
            # 更新配置
            templates = self.templates_config.get('templates', {})
            templates[template_name] = {
                'type': template_type,
                'description': description,
                'version': '1.0.0',
                'author': author,
                'tags': tags or [],
                'fields': fields or [],
                'created': datetime.now().isoformat(),
                'source_file': source_file
            }
            self.templates_config['templates'] = templates
            
            # 保存配置
            self._save_config()
            
            print(f"✅ 模板创建成功：{template_name}")
            return True
            
        except Exception as e:
            print(f"创建模板失败：{e}")
            # 清理失败的文件
            if template_path.exists():
                template_path.unlink()
            return False
    
    def update_template(self, template_name: str, source_file: str = None,
                       description: str = None, version: str = None,
                       author: str = None, tags: List[str] = None,
                       fields: List[str] = None) -> bool:
        """更新模板
        
        Args:
            template_name: 模板名称
            source_file: 新的源文件（可选）
            description: 新的描述（可选）
            version: 新的版本（可选）
            author: 新的作者（可选）
            tags: 新的标签（可选）
            fields: 新的字段（可选）
            
        Returns:
            bool: 是否更新成功
        """
        # 检查模板是否存在
        template_path = self.templates_dir / f"{template_name}.docx"
        if not template_path.exists():
            print(f"错误：模板不存在：{template_name}")
            return False
        
        templates = self.templates_config.get('templates', {})
        if template_name not in templates:
            print(f"错误：模板配置不存在：{template_name}")
            return False
        
        try:
            # 更新模板文件
            if source_file and os.path.exists(source_file):
                shutil.copy2(source_file, template_path)
                templates[template_name]['source_file'] = source_file
            
            # 更新配置信息
            if description is not None:
                templates[template_name]['description'] = description
            
            if version is not None:
                templates[template_name]['version'] = version
            
            if author is not None:
                templates[template_name]['author'] = author
            
            if tags is not None:
                templates[template_name]['tags'] = tags
            
            if fields is not None:
                templates[template_name]['fields'] = fields
            
            # 更新修改时间
            templates[template_name]['modified'] = datetime.now().isoformat()
            
            # 保存配置
            self.templates_config['templates'] = templates
            self._save_config()
            
            print(f"✅ 模板更新成功：{template_name}")
            return True
            
        except Exception as e:
            print(f"更新模板失败：{e}")
            return False
    
    def delete_template(self, template_name: str) -> bool:
        """删除模板
        
        Args:
            template_name: 模板名称
            
        Returns:
            bool: 是否删除成功
        """
        # 检查模板是否存在
        template_path = self.templates_dir / f"{template_name}.docx"
        if not template_path.exists():
            print(f"错误：模板不存在：{template_name}")
            return False
        
        try:
            # 删除文件
            template_path.unlink()
            
            # 删除配置
            templates = self.templates_config.get('templates', {})
            if template_name in templates:
                del templates[template_name]
                self.templates_config['templates'] = templates
                self._save_config()
            
            print(f"✅ 模板删除成功：{template_name}")
            return True
            
        except Exception as e:
            print(f"删除模板失败：{e}")
            return False
    
    def export_template(self, template_name: str, output_path: str) -> bool:
        """导出模板到指定位置
        
        Args:
            template_name: 模板名称
            output_path: 输出路径
            
        Returns:
            bool: 是否导出成功
        """
        # 检查模板是否存在
        template_path = self.templates_dir / f"{template_name}.docx"
        if not template_path.exists():
            print(f"错误：模板不存在：{template_name}")
            return False
        
        try:
            # 复制文件
            shutil.copy2(template_path, output_path)
            
            # 导出配置信息
            templates = self.templates_config.get('templates', {})
            template_info = templates.get(template_name, {})
            
            if template_info:
                config_output = Path(output_path).with_suffix('.json')
                with open(config_output, 'w', encoding='utf-8') as f:
                    json.dump(template_info, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 模板导出成功：{template_name} -> {output_path}")
            return True
            
        except Exception as e:
            print(f"导出模板失败：{e}")
            return False
    
    def import_template(self, template_file: str, config_file: str = None) -> bool:
        """导入模板
        
        Args:
            template_file: 模板文件路径
            config_file: 配置文件路径（可选）
            
        Returns:
            bool: 是否导入成功
        """
        if not os.path.exists(template_file):
            print(f"错误：模板文件不存在：{template_file}")
            return False
        
        # 获取模板名称
        template_name = Path(template_file).stem
        
        # 检查是否已存在
        template_path = self.templates_dir / f"{template_name}.docx"
        if template_path.exists():
            print(f"警告：模板已存在，将覆盖：{template_name}")
        
        try:
            # 复制文件
            shutil.copy2(template_file, template_path)
            
            # 导入配置信息
            template_info = {}
            if config_file and os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    template_info = json.load(f)
            else:
                # 创建默认配置
                template_info = {
                    'type': 'unknown',
                    'description': f"导入的模板：{template_name}",
                    'version': '1.0.0',
                    'author': '系统导入',
                    'tags': ['imported'],
                    'fields': [],
                    'imported': datetime.now().isoformat()
                }
            
            # 更新配置
            templates = self.templates_config.get('templates', {})
            templates[template_name] = template_info
            self.templates_config['templates'] = templates
            self._save_config()
            
            print(f"✅ 模板导入成功：{template_name}")
            return True
            
        except Exception as e:
            print(f"导入模板失败：{e}")
            return False
    
    def create_default_templates(self):
        """创建默认模板"""
        default_templates = [
            {
                'name': 'meeting_minutes_template',
                'type': 'meeting_minutes',
                'description': '标准会议纪要模板',
                'tags': ['会议', '纪要', '标准'],
                'fields': ['title', 'time', 'location', 'host', 'attendees', 'topics']
            },
            {
                'name': 'speech_template',
                'type': 'speech',
                'description': '领导发言稿模板',
                'tags': ['发言', '讲话', '领导'],
                'fields': ['title', 'salutation', 'sections', 'conclusion']
            },
            {
                'name': 'discussion_outline_template',
                'type': 'discussion_outline',
                'description': '讨论提纲模板',
                'tags': ['讨论', '提纲', '会议'],
                'fields': ['title', 'background', 'objectives', 'points']
            },
            {
                'name': 'work_report_template',
                'type': 'work_report',
                'description': '工作汇报模板',
                'tags': ['工作', '汇报', '报告'],
                'fields': ['title', 'recipient', 'progress', 'achievements', 'plans']
            }
        ]
        
        created_count = 0
        for template_info in default_templates:
            # 检查是否已存在
            template_path = self.templates_dir / f"{template_info['name']}.docx"
            if not template_path.exists():
                # 创建空模板文件
                try:
                    from docx import Document
                    doc = Document()
                    doc.add_paragraph(f"{template_info['description']}")
                    doc.save(template_path)
                    
                    # 添加到配置
                    templates = self.templates_config.get('templates', {})
                    templates[template_info['name']] = {
                        'type': template_info['type'],
                        'description': template_info['description'],
                        'version': '1.0.0',
                        'author': '系统',
                        'tags': template_info['tags'],
                        'fields': template_info['fields'],
                        'created': datetime.now().isoformat()
                    }
                    
                    created_count += 1
                    print(f"创建模板：{template_info['name']}")
                    
                except Exception as e:
                    print(f"创建模板失败 {template_info['name']}: {e}")
        
        if created_count > 0:
            self.templates_config['templates'] = templates
            self._save_config()
            print(f"✅ 创建了 {created_count} 个默认模板")
        else:
            print("所有默认模板已存在")


def print_template_list(templates: List[Dict[str, Any]], detailed: bool = False):
    """打印模板列表"""
    if not templates:
        print("📭 没有找到模板")
        return
    
    print(f"\n📋 模板列表（{len(templates)}个）：")
    print("="*80)
    
    for i, template in enumerate(templates, 1):
        print(f"\n{i}. {template['name']}")
        print(f"   类型：{template.get('type', '未知')}")
        print(f"   描述：{template.get('description', '无描述')}")
        print(f"   大小：{template['size']:,} 字节")
        print(f"   修改：{template['modified'][:10]}")
        
        if detailed:
            print(f"   版本：{template.get('version', '1.0.0')}")
            print(f"   作者：{template.get('author', '未知')}")
            tags = template.get('tags', [])
            if tags:
                print(f"   标签：{', '.join(tags)}")
            print(f"   路径：{template['file_path']}")
    
    print("\n" + "="*80)


def print_template_detail(template: Dict[str, Any]):
    """打印模板详细信息"""
    if not template:
        print("❌ 模板不存在")
        return
    
    print(f"\n📄 模板详细信息")
    print("="*80)
    print(f"名称：{template['name']}")
    print(f"类型：{template.get('type', '未知')}")
    print(f"描述：{template.get('description', '无描述')}")
    print(f"版本：{template.get('version', '1.0.0')}")
    print(f"作者：{template.get('author', '未知')}")
    
    tags = template.get('tags', [])
    if tags:
        print(f"标签：{', '.join(tags)}")
    
    fields = template.get('fields', [])
    if fields:
        print(f"字段：{', '.join(fields)}")
    
    print(f"\n📊 文件信息：")
    print(f"   路径：{template['file_path']}")
    print(f"   大小：{template['size']:,} 字节")
    print(f"   创建：{template['created'][:19]}")
    print(f"   修改：{template['modified'][:19]}")
    
    usage = template.get('usage', '')
    if usage:
        print(f"\n📝 使用说明：")
        print(f"   {usage}")
    
    print("\n" + "="*80)


def main():
    parser = argparse.ArgumentParser(description='文档模板管理器')
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # list 命令
    list_parser = subparsers.add_parser('list', help='列出所有模板')
    list_parser.add_argument('--type', help='按类型过滤')
    list_parser.add_argument('--detailed', action='store_true', help='显示详细信息')
    
    # show 命令
    show_parser = subparsers.add_parser('show', help='显示模板详细信息')
    show_parser.add_argument('name', help='模板名称')
    
    # create 命令
    create_parser = subparsers.add_parser('create', help='创建新模板')
    create_parser.add_argument('source', help='源文件路径')
    create_parser.add_argument('name', help='模板名称')
    create_parser.add_argument('type', help='模板类型')
    create_parser.add_argument('--description', help='模板描述')
    create_parser.add_argument('--author', help='作者')
    create_parser.add_argument('--tags', help='标签，用逗号分隔')
    create_parser.add_argument('--fields', help='字段，用逗号分隔')
    
    # update 命令
    update_parser = subparsers.add_parser('update', help='更新模板')
    update_parser.add_argument('name', help='模板名称')
    update_parser.add_argument('--source', help='新的源文件')
    update_parser.add_argument('--description', help='新的描述')
    update_parser.add_argument('--version', help='新的版本')
    update_parser.add_argument('--author', help='新的作者')
    update_parser.add_argument('--tags', help='新的标签，用逗号分隔')
    update_parser.add_argument('--fields', help='新的字段，用逗号分隔')
    
    # delete 命令
    delete_parser = subparsers.add_parser('delete', help='删除模板')
    delete_parser.add_argument('name', help='模板名称')
    
    # export 命令
    export_parser = subparsers.add_parser('export', help='导出模板')
    export_parser.add_argument('name', help='模板名称')
    export_parser.add_argument('output', help='输出路径')
    
    # import 命令
    import_parser = subparsers.add_parser('import', help='导入模板')
    import_parser.add_argument('file', help='模板文件路径')
    import_parser.add_argument('--config', help='配置文件路径')
    
    # init 命令
    init_parser = subparsers.add_parser('init', help='初始化默认模板')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    manager = TemplateManager()
    
    try:
        if args.command == 'list':
            templates = manager.list_templates(args.type)
            print_template_list(templates, args.detailed)
            
        elif args.command == 'show':
            template = manager.get_template(args.name)
            print_template_detail(template)
            
        elif args.command == 'create':
            tags = args.tags.split(',') if args.tags else None
            fields = args.fields.split(',') if args.fields else None
            
            success = manager.create_template(
                source_file=args.source,
                template_name=args.name,
                template_type=args.type,
                description=args.description or '',
                author=args.author or '',
                tags=tags,
                fields=fields
            )
            sys.exit(0 if success else 1)
            
        elif args.command == 'update':
            tags = args.tags.split(',') if args.tags else None
            fields = args.fields.split(',') if args.fields else None
            
            success = manager.update_template(
                template_name=args.name,
                source_file=args.source,
                description=args.description,
                version=args.version,
                author=args.author,
                tags=tags,
                fields=fields
            )
            sys.exit(0 if success else 1)
            
        elif args.command == 'delete':
            success = manager.delete_template(args.name)
            sys.exit(0 if success else 1)
            
        elif args.command == 'export':
            success = manager.export_template(args.name, args.output)
            sys.exit(0 if success else 1)
            
        elif args.command == 'import':
            success = manager.import_template(args.file, args.config)
            sys.exit(0 if success else 1)
            
        elif args.command == 'init':
            manager.create_default_templates()
            
    except Exception as e:
        print(f"错误：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()