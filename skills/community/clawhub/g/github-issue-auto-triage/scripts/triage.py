#!/usr/bin/env python3
"""
GitHub Issue Auto Triage Skill
自动分类 GitHub Issue，AI 打标签、分配负责人、检测重复、回复 FAQ

作者：于金泽
版本：1.0.0
日期：2026-03-16
"""

import os
import sys
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
import hashlib

# 配置
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
GITHUB_OWNER = os.getenv('GITHUB_OWNER', '')
GITHUB_REPO = os.getenv('GITHUB_REPO', '')
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY', 'sk-xxx')

# 默认配置
DEFAULT_CONFIG = {
    'triage': {
        'enabled': True,
        'interval_minutes': 30,
        'auto_label': True,
        'auto_assign': True,
        'detect_duplicates': True,
        'auto_reply_faq': True
    },
    'labels': {
        'bug': {
            'keywords': ['bug', 'error', 'crash', 'fail', 'broken', 'issue', 'problem'],
            'priority': 'high'
        },
        'enhancement': {
            'keywords': ['feature', 'enhancement', 'improve', 'add', 'request'],
            'priority': 'medium'
        },
        'question': {
            'keywords': ['question', 'help', 'how to', 'confused', 'understand'],
            'priority': 'low'
        },
        'documentation': {
            'keywords': ['doc', 'documentation', 'readme', 'guide'],
            'priority': 'low'
        }
    },
    'faq': [
        {
            'keywords': ['install', 'installation', 'setup', 'get started'],
            'answer': '👋 Thanks for your interest! Please see our installation guide: https://docs.example.com/install\n\nIf you encounter any issues, feel free to ask!'
        },
        {
            'keywords': ['license', 'licensing', 'commercial use'],
            'answer': '📄 We use the MIT License. You can freely use this project for personal and commercial purposes. See LICENSE file for details.'
        },
        {
            'keywords': ['contribute', 'contributing', 'pull request'],
            'answer': '🎉 We welcome contributions! Please check our CONTRIBUTING.md guide first: https://github.com/CONTRIBUTING.md'
        }
    ]
}


class GitHubIssueTriage:
    """GitHub Issue 自动分类器"""
    
    def __init__(self, config: Dict = None):
        self.config = config or DEFAULT_CONFIG
        self.github_headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = f'https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}'
    
    def get_uncategorized_issues(self, limit: int = 10) -> List[Dict]:
        """获取未分类的 Issue"""
        url = f'{self.base_url}/issues'
        params = {
            'state': 'open',
            'per_page': limit,
            'sort': 'created',
            'direction': 'asc'
        }
        
        response = requests.get(url, headers=self.github_headers, params=params)
        response.raise_for_status()
        
        issues = response.json()
        # 过滤出没有标签或没有分配负责人的 Issue
        uncategorized = [
            issue for issue in issues 
            if len(issue.get('labels', [])) == 0 or not issue.get('assignee')
        ]
        
        return uncategorized
    
    def classify_issue(self, issue: Dict) -> Dict:
        """使用 AI 分类 Issue"""
        title = issue.get('title', '')
        body = issue.get('body', '')
        content = f"{title}\n\n{body}"
        
        # 关键词匹配
        classifications = []
        for label_type, config in self.config['labels'].items():
            score = sum(1 for kw in config['keywords'] if kw.lower() in content.lower())
            if score > 0:
                classifications.append({
                    'label': label_type,
                    'score': score,
                    'priority': config['priority']
                })
        
        # 按分数排序
        classifications.sort(key=lambda x: x['score'], reverse=True)
        
        # 使用 LLM 进行更准确的分类
        llm_classification = self._llm_classify(title, body)
        
        # 合并结果
        if llm_classification and llm_classification not in [c['label'] for c in classifications]:
            classifications.insert(0, {
                'label': llm_classification,
                'score': 10,
                'priority': self.config['labels'].get(llm_classification, {}).get('priority', 'medium')
            })
        
        return {
            'classifications': classifications,
            'suggested_label': classifications[0]['label'] if classifications else 'question',
            'priority': classifications[0]['priority'] if classifications else 'medium'
        }
    
    def _llm_classify(self, title: str, body: str) -> Optional[str]:
        """使用 LLM 分类 Issue"""
        prompt = f"""
请分析这个 GitHub Issue 并分类为以下类型之一：bug, enhancement, question, documentation

标题：{title}
描述：{body[:500]}

只返回类型名称（bug/enhancement/question/documentation），不要其他内容。
"""
        
        try:
            # 调用 DashScope API
            url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'
            headers = {
                'Authorization': f'Bearer {DASHSCOPE_API_KEY}',
                'Content-Type': 'application/json'
            }
            data = {
                'model': 'qwen-plus',
                'input': {
                    'messages': [
                        {'role': 'user', 'content': prompt}
                    ]
                }
            }
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            
            llm_result = result.get('output', {}).get('text', '').strip().lower()
            
            # 验证结果
            valid_labels = ['bug', 'enhancement', 'question', 'documentation']
            for label in valid_labels:
                if label in llm_result:
                    return label
            
            return None
        except Exception as e:
            print(f"LLM 分类失败：{e}")
            return None
    
    def detect_duplicates(self, issue: Dict) -> List[Dict]:
        """检测重复 Issue"""
        title = issue.get('title', '')
        
        # 获取所有已关闭的 Issue
        url = f'{self.base_url}/issues'
        params = {
            'state': 'all',
            'per_page': 100
        }
        
        response = requests.get(url, headers=self.github_headers, params=params)
        response.raise_for_status()
        
        all_issues = response.json()
        
        # 简单相似度检测
        duplicates = []
        for existing in all_issues:
            if existing['number'] == issue['number']:
                continue
            
            existing_title = existing.get('title', '').lower()
            similarity = self._calculate_similarity(title.lower(), existing_title)
            
            if similarity > 0.7:  # 相似度阈值
                duplicates.append({
                    'number': existing['number'],
                    'title': existing['title'],
                    'similarity': similarity,
                    'state': existing['state']
                })
        
        # 按相似度排序
        duplicates.sort(key=lambda x: x['similarity'], reverse=True)
        
        return duplicates[:3]  # 返回最相似的 3 个
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度（简单版本）"""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union) if union else 0.0
    
    def check_faq(self, issue: Dict) -> Optional[str]:
        """检查是否为 FAQ 问题"""
        title = issue.get('title', '').lower()
        body = issue.get('body', '').lower()
        content = f"{title} {body}"
        
        for faq in self.config['faq']:
            if any(kw in content for kw in faq['keywords']):
                return faq['answer']
        
        return None
    
    def add_labels(self, issue_number: int, labels: List[str]) -> bool:
        """添加标签到 Issue"""
        url = f'{self.base_url}/issues/{issue_number}/labels'
        data = {'labels': labels}
        
        response = requests.post(url, headers=self.github_headers, json=data)
        return response.status_code == 200
    
    def assign_issue(self, issue_number: int, assignee: str) -> bool:
        """分配 Issue 给负责人"""
        url = f'{self.base_url}/issues/{issue_number}/assignees'
        data = {'assignees': [assignee]}
        
        response = requests.post(url, headers=self.github_headers, json=data)
        return response.status_code == 200
    
    def add_comment(self, issue_number: int, comment: str) -> bool:
        """添加评论到 Issue"""
        url = f'{self.base_url}/issues/{issue_number}/comments'
        data = {'body': comment}
        
        response = requests.post(url, headers=self.github_headers, json=data)
        return response.status_code == 201
    
    def triage_issue(self, issue: Dict, dry_run: bool = False) -> Dict:
        """处理单个 Issue"""
        issue_number = issue['number']
        title = issue['title']
        
        print(f"\n{'='*60}")
        print(f"📋 处理 Issue #{issue_number}: {title}")
        print(f"{'='*60}")
        
        result = {
            'issue_number': issue_number,
            'actions': [],
            'success': True
        }
        
        # 1. 分类
        print("\n🔍 正在分类...")
        classification = self.classify_issue(issue)
        suggested_label = classification['suggested_label']
        print(f"✅ 分类结果：{suggested_label} (优先级：{classification['priority']})")
        result['classification'] = classification
        
        # 2. 检测重复
        print("\n🔍 检测重复 Issue...")
        duplicates = self.detect_duplicates(issue)
        if duplicates:
            print(f"⚠️  发现 {len(duplicates)} 个相似 Issue:")
            for dup in duplicates:
                print(f"   - #{dup['number']}: {dup['title']} (相似度：{dup['similarity']:.2f})")
            result['duplicates'] = duplicates
        else:
            print("✅ 未发现重复 Issue")
        
        # 3. 检查 FAQ
        print("\n🔍 检查 FAQ...")
        faq_answer = self.check_faq(issue)
        if faq_answer:
            print(f"✅ 匹配到 FAQ 答案")
            result['faq_answer'] = faq_answer
        
        if not dry_run:
            # 添加标签
            if classification['suggested_label']:
                print(f"\n🏷️  添加标签：{classification['suggested_label']}")
                if self.add_labels(issue_number, [classification['suggested_label']]):
                    result['actions'].append(f'Added label: {classification["suggested_label"]}')
                    print("✅ 标签添加成功")
                else:
                    print("❌ 标签添加失败")
            
            # 添加 FAQ 评论
            if faq_answer:
                print(f"\n💬 添加 FAQ 回复...")
                if self.add_comment(issue_number, faq_answer):
                    result['actions'].append('Added FAQ comment')
                    print("✅ 评论添加成功")
                else:
                    print("❌ 评论添加失败")
        
        print(f"\n✅ Issue #{issue_number} 处理完成")
        return result
    
    def run(self, dry_run: bool = False, issue_number: Optional[int] = None) -> Dict:
        """运行分类任务"""
        print("🚀 开始 GitHub Issue 自动分类")
        print(f"📅 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 仓库：{GITHUB_OWNER}/{GITHUB_REPO}")
        print(f"🔧 模式：{'Dry Run' if dry_run else '正式运行'}")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'repository': f'{GITHUB_OWNER}/{GITHUB_REPO}',
            'dry_run': dry_run,
            'issues_processed': 0,
            'results': []
        }
        
        try:
            if issue_number:
                # 处理特定 Issue
                url = f'{self.base_url}/issues/{issue_number}'
                response = requests.get(url, headers=self.github_headers)
                response.raise_for_status()
                issue = response.json()
                
                result = self.triage_issue(issue, dry_run)
                results['results'].append(result)
                results['issues_processed'] += 1
            else:
                # 处理所有未分类 Issue
                issues = self.get_uncategorized_issues()
                
                if not issues:
                    print("\n✅ 没有需要处理的 Issue")
                    return results
                
                print(f"\n📊 发现 {len(issues)} 个未分类 Issue")
                
                for issue in issues:
                    try:
                        result = self.triage_issue(issue, dry_run)
                        results['results'].append(result)
                        results['issues_processed'] += 1
                    except Exception as e:
                        print(f"❌ 处理 Issue #{issue['number']} 失败：{e}")
                        results['results'].append({
                            'issue_number': issue['number'],
                            'error': str(e),
                            'success': False
                        })
        
        except Exception as e:
            print(f"\n❌ 运行失败：{e}")
            results['error'] = str(e)
        
        # 打印总结
        print(f"\n{'='*60}")
        print("📊 处理总结")
        print(f"{'='*60}")
        print(f"处理 Issue 数：{results['issues_processed']}")
        print(f"成功：{sum(1 for r in results['results'] if r.get('success'))}")
        print(f"失败：{sum(1 for r in results['results'] if not r.get('success'))}")
        
        return results


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='GitHub Issue Auto Triage')
    parser.add_argument('--dry-run', action='store_true', help='Dry run mode')
    parser.add_argument('--issue', type=int, help='Process specific issue number')
    parser.add_argument('--config', type=str, help='Config file path')
    
    args = parser.parse_args()
    
    # 加载配置
    config = DEFAULT_CONFIG
    if args.config and os.path.exists(args.config):
        with open(args.config, 'r') as f:
            config = json.load(f)
    
    # 检查必要的环境变量
    if not GITHUB_TOKEN:
        print("❌ 错误：请设置 GITHUB_TOKEN 环境变量")
        sys.exit(1)
    
    if not GITHUB_OWNER or not GITHUB_REPO:
        print("❌ 错误：请设置 GITHUB_OWNER 和 GITHUB_REPO 环境变量")
        sys.exit(1)
    
    # 创建分类器并运行
    triage = GitHubIssueTriage(config)
    results = triage.run(dry_run=args.dry_run, issue_number=args.issue)
    
    # 保存结果
    output_file = f'triage_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 结果已保存到：{output_file}")


if __name__ == '__main__':
    main()
