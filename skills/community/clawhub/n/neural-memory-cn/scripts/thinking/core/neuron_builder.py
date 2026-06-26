# Neuron Builder - 神经元构建器
# 从现有记忆文件初始化神经元系统
import os
import re
from typing import List, Dict, Optional
from ..storage.manager import StorageManager
from .models import Neuron

class NeuronBuilder:
    """神经元构建器 - 从现有数据源创建神经元"""

    def __init__(self, storage: StorageManager):
        self.storage = storage

    def build_from_memory_files(self):
        """从现有的记忆文件构建初始神经元"""
        base_path = self.storage.base_path
        long_term_path = os.path.join(base_path, "memory_long_term")

        created_count = 0

        # 1. 从 UserProfile 创建用户属性神经元（保护类型）
        user_profile_path = os.path.join(long_term_path, "UserProfile.md")
        if os.path.exists(user_profile_path):
            created_count += self._create_from_user_profile(user_profile_path)

        # 2. 从 Preferences 创建偏好神经元（保护类型）
        preferences_path = os.path.join(long_term_path, "Preferences.md")
        if os.path.exists(preferences_path):
            created_count += self._create_from_preferences(preferences_path)

        # 3. 从 LearningProjects 创建项目神经元
        projects_path = os.path.join(long_term_path, "LearningProjects.md")
        if os.path.exists(projects_path):
            created_count += self._create_from_learning_projects(projects_path)

        # 4. 从 KeyInsights 创建洞察神经元
        insights_path = os.path.join(long_term_path, "KeyInsights.md")
        if os.path.exists(insights_path):
            created_count += self._create_from_key_insights(insights_path)

        # 5. 从 KnowledgeConnections 创建连接神经元（这些作为concept类型）
        connections_path = os.path.join(long_term_path, "KnowledgeConnections.md")
        if os.path.exists(connections_path):
            created_count += self._create_from_knowledge_connections(connections_path)

        print(f"总共创建了 {created_count} 个神经元")
        return created_count

    def _create_from_user_profile(self, filepath: str) -> int:
        """从 USER.md 创建用户属性神经元"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        count = 0

        # 提取身份信息
        identity_match = re.search(r'## Identity\n(.*?)(?=##|\Z)', content, re.DOTALL)
        if identity_match:
            identity_block = identity_match.group(1).strip()
            neuron = Neuron.create(
                type='user_profile',
                name='User Identity',
                content=identity_block,
                tags=['user', 'identity', 'protected'],
                metadata={'source': 'USER.md', 'section': 'Identity'}
            )
            if self.storage.add_neuron(neuron):
                count += 1

        # 提取学习兴趣
        interests_match = re.search(r'## Autonomous Learning Interests\n(.*?)(?=##|\Z)', content, re.DOTALL)
        if interests_match:
            interests_block = interests_match.group(1).strip()
            neuron = Neuron.create(
                type='user_preference',
                name='Learning Interests',
                content=interests_block,
                tags=['user', 'interests', 'protected'],
                metadata={'source': 'USER.md', 'section': 'Interests'}
            )
            if self.storage.add_neuron(neuron):
                count += 1

        # 提取偏好
        prefs_match = re.search(r'## Preferences\n(.*?)(?=##|\Z)', content, re.DOTALL)
        if prefs_match:
            prefs_block = prefs_match.group(1).strip()
            neuron = Neuron.create(
                type='user_preference',
                name='User Preferences',
                content=prefs_block,
                tags=['user', 'preferences', 'protected'],
                metadata={'source': 'USER.md', 'section': 'Preferences'}
            )
            if self.storage.add_neuron(neuron):
                count += 1

        return count

    def _create_from_preferences(self, filepath: str) -> int:
        """从 Preferences.md 创建偏好神经元"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        neuron = Neuron.create(
            type='preference',
            name='Personal Preferences',
            content=content,
            tags=['preferences', 'learning_style', 'protected'],
            metadata={'source': 'Preferences.md'}
        )

        if self.storage.add_neuron(neuron):
            return 1
        return 0

    def _create_from_learning_projects(self, filepath: str) -> int:
        """从 LearningProjects.md 创建项目神经元"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取各个学习项目
        projects = re.split(r'### ', content)[1:]  # 跳过开头，每个项目以 ### 开头
        count = 0

        for project_text in projects:
            if not project_text.strip():
                continue

            # 提取项目名称（如果没有明确名称，使用前几个词）
            name_match = re.match(r'\[([^\]]+)\]', project_text)
            if name_match:
                name = name_match.group(1).strip()
            else:
                name = project_text[:50].strip().replace('\n', ' ')

            neuron = Neuron.create(
                type='topic',
                name=name,
                content=project_text[:500],  # 截取前500字符作为摘要
                tags=['learning_project', 'topic'],
                metadata={'source': 'LearningProjects.md'}
            )
            if self.storage.add_neuron(neuron):
                count += 1

        return count

    def _create_from_key_insights(self, filepath: str) -> int:
        """从 KeyInsights.md 创建洞察神经元"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取各个洞察
        insights = re.split(r'### ', content)[1:]  # 每个洞察以 ### 开头
        count = 0

        for insight_text in insights:
            if not insight_text.strip():
                continue

            # 提取洞察标题
            title_match = re.match(r'\[([^\]]+)\]', insight_text)
            if title_match:
                title = title_match.group(1).strip()
            else:
                title = insight_text[:50].strip().replace('\n', ' ')

            neuron = Neuron.create(
                type='insight',
                name=title,
                content=insight_text[:500],
                tags=['insight', 'key_insight'],
                metadata={'source': 'KeyInsights.md'}
            )
            if self.storage.add_neuron(neuron):
                count += 1

        return count

    def _create_from_knowledge_connections(self, filepath: str) -> int:
        """从 KnowledgeConnections.md 提取所有领域名称作为概念神经元"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取所有参与连接的领域名称
        # 格式: **领域A + 领域B**
        pattern = r'\*\*([^*\n]+) \+ ([^*\n]+)\*\*'
        matches = re.findall(pattern, content)

        fields = set()
        for from_field, to_field in matches:
            fields.add(from_field.strip())
            fields.add(to_field.strip())

        count = 0
        for field in fields:
            neuron = Neuron.create(
                type='concept',
                name=field,
                content=f"领域概念: {field}",
                tags=['concept', 'field'],
                metadata={'source': 'KnowledgeConnections.md'}
            )
            if self.storage.add_neuron(neuron):
                count += 1

        return count

    def create_neuron_from_text(self, name: str, content: str, neuron_type: str = 'concept',
                                tags: List[str] = None, metadata: Dict = None) -> Optional[Neuron]:
        """从文本创建单个神经元"""
        neuron = Neuron.create(
            type=neuron_type,
            name=name,
            content=content,
            tags=tags or [],
            metadata=metadata or {}
        )

        if self.storage.add_neuron(neuron):
            return neuron
        return None
