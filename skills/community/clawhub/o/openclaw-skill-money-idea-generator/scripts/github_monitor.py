#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub 热门项目监控
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from config import GITHUB_TOKEN, CATEGORIES, EXCLUDE_KEYWORDS, MIN_STARS


class GitHubMonitor:
    """GitHub 热门项目监控"""
    
    def __init__(self, token: str = GITHUB_TOKEN):
        self.token = token
        self.headers = {'Authorization': f'token {token}'} if token else {}
        self.base_url = 'https://api.github.com'
    
    def search_ai_projects(self, days: int = 7, min_stars: int = MIN_STARS) -> List[Dict]:
        """
        搜索最近热门的 AI 项目
        
        Args:
            days: 最近几天创建的
            min_stars: 最小星标数
            
        Returns:
            项目列表
        """
        results = []
        
        # 计算日期
        since = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        for category in CATEGORIES:
            query = f'{category} created:>{since} stars:>{min_stars}'
            url = f'{self.base_url}/search/repositories'
            params = {
                'q': query,
                'sort': 'stars',
                'order': 'desc',
                'per_page': 20,
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    for item in data.get('items', []):
                        # 排除不需要的项目
                        if self._should_exclude(item['full_name'], item.get('description', '')):
                            continue
                        
                        results.append({
                            'name': item['full_name'],
                            'stars': item['stargazers_count'],
                            'language': item.get('language', ''),
                            'description': item.get('description', ''),
                            'url': item['html_url'],
                            'created_at': item['created_at'],
                            'pushed_at': item['pushed_at'],
                            'category': category,
                        })
            except Exception as e:
                print(f"搜索失败 ({category}): {e}")
        
        # 去重并排序
        seen = set()
        unique_results = []
        for item in sorted(results, key=lambda x: x['stars'], reverse=True):
            if item['name'] not in seen:
                seen.add(item['name'])
                unique_results.append(item)
        
        return unique_results[:20]
    
    def get_trending_repos(self, language: str = '', since: str = 'weekly') -> List[Dict]:
        """
        获取 GitHub Trending 项目
        
        Args:
            language: 编程语言
            since: 时间范围 (daily, weekly, monthly)
            
        Returns:
            项目列表
        """
        # 使用非官方 API
        url = f'https://api.gitterapp.com/repositories'
        params = {
            'language': language,
            'since': since,
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data[:20]:
                    if self._should_exclude(item.get('full_name', ''), item.get('description', '')):
                        continue
                    
                    results.append({
                        'name': item.get('full_name', ''),
                        'stars': item.get('stargazers_count', 0),
                        'language': item.get('language', ''),
                        'description': item.get('description', ''),
                        'url': item.get('html_url', ''),
                        'trending_stars': item.get('trending_stars', 0),
                    })
                return results
        except Exception as e:
            print(f"获取 Trending 失败: {e}")
        
        # 降级：使用搜索 API
        return self.search_ai_projects(days=7)
    
    def _should_exclude(self, name: str, description: str) -> bool:
        """判断是否应该排除"""
        text = f"{name} {description or ''}".lower()
        for keyword in EXCLUDE_KEYWORDS:
            if keyword.lower() in text:
                return True
        return False
    
    def get_repo_details(self, owner: str, repo: str) -> Optional[Dict]:
        """
        获取仓库详情
        
        Args:
            owner: 仓库所有者
            repo: 仓库名
            
        Returns:
            仓库详情
        """
        url = f'{self.base_url}/repos/{owner}/{repo}'
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'name': data['full_name'],
                    'stars': data['stargazers_count'],
                    'forks': data['forks_count'],
                    'language': data.get('language', ''),
                    'description': data.get('description', ''),
                    'topics': data.get('topics', []),
                    'license': data.get('license', {}).get('spdx_id', ''),
                    'open_issues': data['open_issues_count'],
                    'watchers': data['watchers_count'],
                    'url': data['html_url'],
                    'created_at': data['created_at'],
                    'pushed_at': data['pushed_at'],
                }
        except Exception as e:
            print(f"获取仓库详情失败: {e}")
        
        return None


# 测试
if __name__ == '__main__':
    monitor = GitHubMonitor()
    
    print('=== 最近热门 AI 项目 ===')
    projects = monitor.search_ai_projects(days=7)
    for i, p in enumerate(projects[:10], 1):
        print(f"{i}. {p['name']} ⭐{p['stars']}")
        print(f"   {p['description'][:50]}...")
        print(f"   🔗 {p['url']}")
        print()