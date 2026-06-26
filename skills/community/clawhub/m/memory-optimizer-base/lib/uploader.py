#!/usr/bin/env python3
"""
上传器 - 将中期总结上传到公共长期记忆空间
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
import config

class MemoryUploader:
    def __init__(self, config_obj):
        self.config = config_obj
        base_path = self.config.get('memory.base_path', '~/.openclaw/workspace')
        self.workspace_root = Path(base_path).expanduser()

    def upload(self, agent_id, target_date=None, title=None, confirm_callback=None):
        """
        上传中期总结到公共空间

        Args:
            agent_id: Agent标识
            target_date: 日期（默认今天）
            title: 事件标题（可选）
            confirm_callback: 确认回调函数，用于用户交互

        Returns:
            dict: 上传结果
        """
        if target_date is None:
            target_date = datetime.now().date()

        date_str = target_date.strftime('%Y-%m-%d')

        # 1. 读取中期总结
        medium_file = self._get_medium_summary(agent_id, date_str)
        if not medium_file:
            return {
                'success': False,
                'message': f'未找到 {agent_id} 在 {date_str} 的中期总结'
            }

        with open(medium_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 2. 解析元数据
        metadata = self._parse_summary_metadata(content)

        # 3. 确定标题
        if not title:
            title = self._generate_title(metadata, agent_id, date_str)

        # 4. 格式化公共空间文档
        public_content = self._format_public_content(content, metadata, title)

        # 5. 用户确认
        if self.config.get('upload.require_upload_confirm', True):
            if confirm_callback:
                approved = confirm_callback(public_content, metadata)
            else:
                # 默认自动确认（生产环境应该要求交互）
                print(f"⚠️  即将上传到公共空间：{title}")
                print(f"📄 内容预览（前500字）：")
                print(public_content[:500] + ('...' if len(public_content) > 500 else ''))
                response = input("确认上传？(y/N): ").strip().lower()
                approved = response == 'y'
        else:
            approved = True

        if not approved:
            return {
                'success': False,
                'message': '用户取消上传',
                'cancelled': True
            }

        # 6. 保存到公共空间
        public_path = self._save_to_public(agent_id, date_str, title, public_content)
        metadata['public_path'] = str(public_path)

        # 7. 可选：备份到私有长期
        if self.config.get('upload.backup_private', True):
            self._backup_to_private(agent_id, date_str, title, public_content, metadata)

        # 8. 可选：删除中期总结（已上传）
        # medium_file.unlink(missing_ok=True)

        return {
            'success': True,
            'agent': agent_id,
            'date': date_str,
            'title': title,
            'public_path': str(public_path),
            'metadata': metadata,
            'message': f'✅ 已上传到公共空间：{public_path}'
        }

    def _get_medium_summary(self, agent_id, date_str):
        """获取指定日期的中期总结文件"""
        private_dir = self.workspace_root / self.config.get('memory.private_root') / agent_id / 'medium-term'
        file_path = private_dir / f'{date_str}.md'
        return file_path if file_path.exists() else None

    def _parse_summary_metadata(self, content):
        """解析总结文件的元数据（YAML front matter）"""
        metadata = {}

        # 提取 front matter
        if content.startswith('---'):
            end = content.find('---', 3)
            if end != -1:
                front_matter = content[3:end].strip()
                for line in front_matter.split('\n'):
                    if ':' in line:
                        key, val = line.split(':', 1)
                        metadata[key.strip()] = val.strip()

        return metadata

    def _generate_title(self, metadata, agent_id, date_str):
        """生成上传标题"""
        # 优先级：1. 从元数据提取 2. 从关键词生成 3. 默认格式
        if 'title' in metadata:
            return metadata['title']

        keywords = metadata.get('keywords', '')
        if keywords:
            # 取前2个关键词
            kw_list = keywords.split(', ')[:2]
            return f"{agent_id}的{'+'.join(kw_list)}经验"

        return f"{agent_id} - {date_str} 工作总结"

    def _format_public_content(self, original_content, metadata, title):
        """格式化为公共空间文档"""
        # 添加新的 front matter
        new_metadata = f"""---
agent: {metadata.get('agent', 'unknown')}
date: {metadata.get('date', datetime.now().strftime('%Y-%m-%d'))}
title: {title}
uploaded: {datetime.now().isoformat()}
source: private-medium-term
keywords: {metadata.get('keywords', '')}
sessions: {metadata.get('sessions', '0')}
---

"""

        # 添加来源标记
        header = f"""# {title}

> 来源：{metadata.get('agent')} 的私有记忆总结  
> 日期：{metadata.get('date')}  
> 上传时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

---

"""

        return new_metadata + header + original_content

    def _save_to_public(self, agent_id, date_str, title, content):
        """保存到公共空间"""
        public_dir = self.workspace_root / self.config.get('memory.public_root') / agent_id / date_str
        public_dir.mkdir(parents=True, exist_ok=True)

        # 生成文件名
        filename = self.config.get('upload.filename_template', '{agent}-{date}-{title}.md')
        filename = filename.format(agent=agent_id, date=date_str, title=title.replace(' ', '_'))

        file_path = public_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return file_path

    def _backup_to_private(self, agent_id, date_str, title, content, metadata):
        """备份到私有长期目录"""
        private_long_dir = self.workspace_root / self.config.get('memory.private_root') / agent_id / 'long-term' / date_str
        private_long_dir.mkdir(parents=True, exist_ok=True)

        filename = title.replace(' ', '_') + '.md'
        file_path = private_long_dir / filename

        backup_content = f"""---
original_medium: memory/private/{agent_id}/medium-term/{date_str}.md
uploaded_to_public: {metadata.get('public_path', 'unknown')}
---

""" + content

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(backup_content)

        return file_path
