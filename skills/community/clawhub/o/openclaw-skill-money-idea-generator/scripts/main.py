#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
赚钱灵感生成器 - 主入口
集成资产池 + 多数据源
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

from github_monitor import GitHubMonitor
from idea_analyzer import IdeaAnalyzer
from asset_pool import AssetPool
from multi_source_monitor import MultiSourceMonitor
from config import USER_PREFERENCES


class MoneyIdeaGenerator:
    """赚钱灵感生成器（含资产池 + 多数据源）"""
    
    def __init__(self, user_preferences: Dict = None):
        self.monitor = GitHubMonitor()
        self.multi_monitor = MultiSourceMonitor()  # 多数据源
        self.analyzer = IdeaAnalyzer()
        self.pool = AssetPool()
        self.preferences = user_preferences or USER_PREFERENCES
    
    def generate_daily_ideas(self, count: int = 3, save_to_pool: bool = True, use_multi_source: bool = True) -> List[Dict]:
        """
        生成每日赚钱灵感
        
        Args:
            count: 灵感数量
            save_to_pool: 是否保存到资产池
            use_multi_source: 是否使用多数据源
            
        Returns:
            赚钱灵感列表
        """
        ideas = []
        
        # 1. 使用多数据源
        if use_multi_source:
            print("正在获取多平台热点...")
            hot_data = self.multi_monitor.get_all_hot()
            hot_ideas = self.multi_monitor.generate_ideas_from_hot(hot_data)
            
            # 转换格式
            for hot in hot_ideas[:count]:
                ideas.append({
                    'type': 'hot_topic',
                    'name': hot['title'],
                    'description': hot['description'],
                    'target_users': ['创业者', '自媒体运营者', '开发者'],
                    'cost': 100,
                    'expected_income': 3000,
                    'time_needed': 3,
                    'source': hot['source'],
                    'potential': hot['potential'],
                    'project_url': hot['url'],
                })
        
        # 2. GitHub 项目分析
        print("正在搜索 GitHub 热门 AI 项目...")
        projects = self.monitor.search_ai_projects(days=7, min_stars=50)
        
        if projects:
            print("正在分析变现潜力...")
            analyzed = []
            for project in projects[:20]:
                potential, score = self.analyzer.analyze_potential(project)
                project['potential'] = potential
                project['potential_score'] = score
                analyzed.append(project)
            
            analyzed.sort(key=lambda x: x['potential_score'], reverse=True)
            
            for project in analyzed[:count]:
                project_ideas = self.analyzer.generate_ideas(project, self.preferences)
                ideas.extend(project_ideas)
        
        # 3. 如果没有数据，使用备用灵感
        if not ideas:
            ideas = self._get_fallback_ideas()
        
        # 4. 排序并截取
        ranked_ideas = self.analyzer.rank_ideas(ideas, self.preferences)
        final_ideas = ranked_ideas[:count]
        
        # 5. 保存到资产池
        if save_to_pool:
            for idea in final_ideas:
                self.pool.add_idea(idea)
        
        return final_ideas
    
    def analyze_project(self, project_url: str) -> Optional[Dict]:
        """
        分析特定项目的变现潜力
        
        Args:
            project_url: 项目 URL
            
        Returns:
            分析结果
        """
        # 从 URL 提取 owner/repo
        import re
        match = re.search(r'github\.com/([^/]+)/([^/]+)', project_url)
        if not match:
            return None
        
        owner, repo = match.groups()
        
        # 获取项目详情
        project = self.monitor.get_repo_details(owner, repo)
        if not project:
            return None
        
        # 分析潜力
        potential, score = self.analyzer.analyze_potential(project)
        project['potential'] = potential
        project['potential_score'] = score
        
        # 生成灵感
        ideas = self.analyzer.generate_ideas(project, self.preferences)
        
        return {
            'project': project,
            'potential': potential,
            'potential_score': score,
            'ideas': ideas,
        }
    
    def get_hot_opportunities(self) -> List[Dict]:
        """
        获取当前热门变现机会
        
        Returns:
            变现机会列表
        """
        # 获取 GitHub Trending
        print("正在获取 GitHub Trending...")
        trending = self.monitor.get_trending_repos(language='', since='weekly')
        
        # 筛选 AI 相关项目
        ai_keywords = ['ai', 'llm', 'gpt', 'agent', 'chatbot', 'ml', 'machine learning']
        ai_projects = []
        
        for project in trending:
            desc = project.get('description', '').lower()
            if any(k in desc for k in ai_keywords):
                potential, score = self.analyzer.analyze_potential(project)
                project['potential'] = potential
                project['potential_score'] = score
                ai_projects.append(project)
        
        # 排序
        ai_projects.sort(key=lambda x: x['potential_score'], reverse=True)
        
        return ai_projects[:10]
    
    def _get_fallback_ideas(self) -> List[Dict]:
        """获取备用灵感（当无法获取数据时）"""
        return [
            {
                'type': 'deployment_service',
                'name': 'OpenClaw 部署服务',
                'description': '帮助用户部署 OpenClaw AI 智能体，提供技术支持',
                'target_users': ['自媒体运营者', '电商卖家', '小微企业'],
                'cost': 500,
                'expected_income': 5000,
                'time_needed': 2,
                'project': 'OpenClaw',
                'implementation': [
                    '在闲鱼发布服务（¥199-299）',
                    '准备服务器（阿里云/腾讯云最低配）',
                    '标准化部署流程（2小时/客户）',
                    '提供 7 天技术支持',
                ],
            },
            {
                'type': 'training',
                'name': 'AI Agent 使用教程',
                'description': '制作 AI Agent 使用教程，卖给想学习的人',
                'target_users': ['学习者', '开发者', '企业员工'],
                'cost': 0,
                'expected_income': 1000,
                'time_needed': 3,
                'project': 'AI Agent',
                'implementation': [
                    '录制视频教程（B站/抖音）',
                    '制作文字教程（公众号/知乎）',
                    '设置付费订阅（¥99/月）',
                    '定期更新内容',
                ],
            },
            {
                'type': 'consulting',
                'name': 'AI 自动化咨询服务',
                'description': '为企业提供 AI 自动化转型咨询',
                'target_users': ['企业', '创业者', '产品经理'],
                'cost': 100,
                'expected_income': 10000,
                'time_needed': 1,
                'project': 'AI Automation',
                'implementation': [
                    '制作案例展示文档',
                    '在 LinkedIn/知乎 发布内容',
                    '设置咨询价格（¥500-1000/小时）',
                    '提供方案设计服务',
                ],
            },
        ]


def format_idea_output(ideas: List[Dict]) -> str:
    """格式化输出灵感"""
    output = []
    output.append("=" * 60)
    output.append("💰 今日赚钱灵感")
    output.append("=" * 60)
    output.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    output.append("")
    
    for i, idea in enumerate(ideas, 1):
        output.append(f"【灵感 #{i}】{idea['name']}")
        output.append(f"  描述：{idea['description']}")
        output.append(f"  目标用户：{', '.join(idea['target_users'])}")
        output.append(f"  启动成本：¥{idea['cost']}")
        output.append(f"  预期收入：¥{idea['expected_income']}/月")
        output.append(f"  所需时间：{idea['time_needed']} 天")
        
        if 'implementation' in idea:
            output.append("  实现路径：")
            for step in idea['implementation']:
                output.append(f"    - {step}")
        
        if 'project_url' in idea:
            output.append(f"  🔗 {idea['project_url']}")
        
        output.append("")
    
    return "\n".join(output)


# 主入口
if __name__ == '__main__':
    generator = MoneyIdeaGenerator()
    
    print("\n=== 测试：生成每日赚钱灵感 ===\n")
    ideas = generator.generate_daily_ideas(count=3)
    print(format_idea_output(ideas))
    
    print("\n=== 测试：分析特定项目 ===\n")
    result = generator.analyze_project('https://github.com/langchain-ai/langchain')
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))