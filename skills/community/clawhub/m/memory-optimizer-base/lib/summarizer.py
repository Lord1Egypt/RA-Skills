#!/usr/bin/env python3
"""
中期总结生成器 - 从当前会话记忆生成 agent+date 格式的总结
"""

import os
import re
from datetime import datetime, date
from pathlib import Path
import config

class MemorySummarizer:
    def __init__(self, config_obj):
        self.config = config_obj
        base_path = self.config.get('memory.base_path', '~/.openclaw/workspace')
        self.workspace_root = Path(base_path).expanduser()

    def summarize(self, agent_id, target_date=None):
        """
        生成指定Agent在指定日期的中期总结

        Args:
            agent_id: Agent标识
            target_date: 日期对象，默认为今天

        Returns:
            dict: 总结内容和元数据
        """
        if target_date is None:
            target_date = date.today()

        date_str = target_date.strftime('%Y-%m-%d')

        # 1. 收集今日记忆内容
        raw_content = self._collect_daily_memories(target_date)

        if not raw_content:
            return {
                'success': False,
                'message': f'未找到 {date_str} 的记忆内容',
                'content': None
            }

        # 2. 提取关键信息
        extracted = self._extract_key_info(raw_content, agent_id, date_str)

        # 3. 生成结构化总结
        summary = self._render_summary(extracted)

        # 4. 保存到私有中期目录
        saved_path = self._save_summary(agent_id, date_str, summary)

        return {
            'success': True,
            'agent': agent_id,
            'date': date_str,
            'content': summary,
            'path': str(saved_path),
            'stats': {
                'raw_size': len(raw_content),
                'summary_size': len(summary),
                'sessions_count': extracted['sessions_count']
            }
        }

    def _collect_daily_memories(self, target_date):
        """收集指定日期的所有记忆文件内容"""
        date_str = target_date.strftime('%Y-%m-%d')
        contents = []

        # 1. 读取 MEMORY.md 中今日部分（如果存在）
        memory_md = self.workspace_root / 'MEMORY.md'
        if memory_md.exists():
            with open(memory_md, 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取今日日期对应的部分
                today_section = self._extract_date_section(content, date_str)
                if today_section:
                    contents.append(today_section)

        # 2. 读取 memory/YYYY-MM-DD.md 文件
        memory_dir = self.workspace_root / 'memory'
        daily_file = memory_dir / f'{date_str}.md'
        if daily_file.exists():
            with open(daily_file, 'r', encoding='utf-8') as f:
                contents.append(f.read())

        return '\n\n'.join(contents)

    def _extract_date_section(self, content, date_str):
        """从 MARKDOWN 内容中提取指定日期部分"""
        pattern = rf'## {date_str}.*?(?=## \d{{4}}-\d{{2}}-\d{{2}}|$)'
        match = re.search(pattern, content, re.DOTALL)
        return match.group(0).strip() if match else None

    def _extract_key_info(self, raw_content, agent_id, date_str):
        """从原始内容提取关键信息"""
        # 简单规则提取（后续可升级为 NLP）
        lines = raw_content.split('\n')

        activities = []
        learnings = []
        decisions = []
        todos = []
        notes = []

        # 识别关键内容
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # 跳过 markdown 标题行（避免将标题作为内容）
            if line.startswith('#'):
                continue

            # 活动（包含动词的句子）
            if any(kw in line.lower() for kw in ['完成', '进行', '执行', '处理', '会议', '讨论', '发送', '创建']):
                activities.append(line)

            # 学习收获
            if any(kw in line.lower() for kw in ['学习', '学会', '了解', '掌握', '研究', '阅读']):
                learnings.append(line)

            # 决策
            if any(kw in line.lower() for kw in ['决定', '选择', '确定', '计划', '安排']):
                decisions.append(line)

            # 待办
            if any(kw in line.lower() for kw in ['待办', 'TODO', '需要', '应该', '下一步']):
                todos.append(line)

            # 备注（不包含标题行，因为已经跳过）
            if '备注' in line or '注意' in line:
                notes.append(line)

        # 限制数量
        activities = activities[:10]
        learnings = learnings[:8]
        decisions = decisions[:5]
        todos = todos[:10]
        notes = notes[:5]

        # 提取关键词（简易版）
        keywords = self._extract_keywords(raw_content)

        return {
            'agent': agent_id,
            'date': date_str,
            'activities': activities,
            'learnings': learnings,
            'decisions': decisions,
            'todos': todos,
            'notes': notes,
            'keywords': keywords,
            'raw_snippets': lines[:20],  # 保存部分原文
            'sessions_count': len([l for l in lines if 'Session' in l or '会话' in l])
        }

    def _extract_keywords(self, text):
        """简易关键词提取（词频统计）"""
        words = re.findall(r'[\u4e00-\u9fa5]{2,}|[a-zA-Z]{3,}', text.lower())
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1

        # 返回高频词（最多10个）
        sorted_words = sorted(freq.items(), key=lambda x: -x[1])
        return [w for w, _ in sorted_words[:10]]

    def _render_summary(self, extracted):
        """渲染总结文档"""
        template = self.config.get('summarizer.template')
        generated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 清理并格式化列表项
        def format_list(items):
            cleaned = []
            for item in items:
                line = str(item).strip()
                if not line:
                    continue
                # 移除 markdown 标题前缀
                if line.startswith('#'):
                    line = line.lstrip('#').strip()
                # 确保以 "- " 开头
                if not line.startswith('- ') and not line.startswith('* '):
                    line = f'- {line}'
                cleaned.append(line)
            return cleaned if cleaned else ['暂无']

        activities_list = format_list(extracted['activities'])
        learnings_list = format_list(extracted['learnings'])
        decisions_list = format_list(extracted['decisions'])
        todos_list = format_list(extracted['todos'])
        notes_list = format_list(extracted['notes'])

        # 生成内容
        content = template.format(
            agent=extracted['agent'],
            date=extracted['date'],
            generated=generated,
            keywords=', '.join(extracted['keywords']),
            sessions=extracted['sessions_count'],
            activities='\n'.join(activities_list),
            learnings='\n'.join(learnings_list),
            decisions='\n'.join(decisions_list),
            todos='\n'.join(todos_list),
            notes='\n'.join(notes_list)
        )

        return content

    def _save_summary(self, agent_id, date_str, content):
        """保存中期总结到私有目录"""
        private_dir = self.workspace_root / self.config.get('memory.private_root') / agent_id / 'medium-term'
        private_dir.mkdir(parents=True, exist_ok=True)

        file_path = private_dir / f'{date_str}.md'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return file_path
