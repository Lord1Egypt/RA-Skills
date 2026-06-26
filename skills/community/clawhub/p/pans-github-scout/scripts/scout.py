#!/usr/bin/env python3
"""
pans-github-scout: 扫描 GitHub 寻找潜在 AI 公司客户

功能：
- 搜索维度：AI/ML repos、大模型项目、训练代码
- 筛选：star数、活跃度、公司规模
- CLI：--search, --filter, --export
"""

import argparse
import csv
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


class GitHubScout:
    """GitHub AI 公司客户扫描器"""
    
    BASE_URL = "https://api.github.com"
    
    # AI/ML 相关搜索关键词
    AI_KEYWORDS = [
        "machine learning",
        "deep learning",
        "neural network",
        "transformer",
        "llm",
        "large language model",
        "pytorch",
        "tensorflow",
        "huggingface",
        "openai",
        "fine-tuning",
        "training",
        "inference",
        "gpu",
        "cuda"
    ]
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "pans-github-scout/1.0"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
    
    def _api_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict:
        """发送 GitHub API 请求"""
        url = f"{self.BASE_URL}{endpoint}"
        if params:
            query = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
            url = f"{url}?{query}"
        
        req = urllib.request.Request(url, headers=self.headers)
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print("错误: GitHub API 速率限制。请设置 GITHUB_TOKEN 环境变量。", file=sys.stderr)
            elif e.code == 404:
                print(f"错误: 资源未找到 {url}", file=sys.stderr)
            else:
                print(f"HTTP 错误 {e.code}: {e.reason}", file=sys.stderr)
            return {}
        except Exception as e:
            print(f"请求错误: {e}", file=sys.stderr)
            return {}
    
    def search_repos(self, query: str, sort: str = "stars", order: str = "desc", 
                     per_page: int = 30, page: int = 1) -> List[Dict]:
        """搜索仓库"""
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": min(per_page, 100),
            "page": page
        }
        result = self._api_request("/search/repositories", params)
        return result.get("items", [])
    
    def search_ai_repos(self, keyword: Optional[str] = None, min_stars: int = 0,
                        language: Optional[str] = None, updated_within: Optional[int] = None) -> List[Dict]:
        """搜索 AI/ML 相关仓库"""
        search_terms = []
        
        if keyword:
            search_terms.append(keyword)
        else:
            search_terms.append(" OR ".join(self.AI_KEYWORDS[:5]))
        
        query_parts = [search_terms[0]]
        
        if min_stars > 0:
            query_parts.append(f"stars:>={min_stars}")
        
        if language:
            query_parts.append(f"language:{language}")
        
        if updated_within:
            date = (datetime.now() - timedelta(days=updated_within)).strftime("%Y-%m-%d")
            query_parts.append(f"pushed:>={date}")
        
        query = " ".join(query_parts)
        return self.search_repos(query)
    
    def get_repo_details(self, owner: str, repo: str) -> Dict:
        """获取仓库详情"""
        return self._api_request(f"/repos/{owner}/{repo}")
    
    def get_user_orgs(self, username: str) -> List[Dict]:
        """获取用户所属组织"""
        return self._api_request(f"/users/{username}/orgs")
    
    def get_org_details(self, org: str) -> Dict:
        """获取组织详情"""
        return self._api_request(f"/orgs/{org}")
    
    def filter_leads(self, repos: List[Dict], min_stars: int = 100, 
                     max_stars: Optional[int] = None,
                     updated_within: Optional[int] = None,
                     has_company: bool = False) -> List[Dict]:
        """筛选潜在客户"""
        filtered = []
        
        for repo in repos:
            # 基础筛选
            stars = repo.get("stargazers_count", 0)
            if stars < min_stars:
                continue
            if max_stars and stars > max_stars:
                continue
            
            # 活跃度筛选
            if updated_within:
                pushed_at = repo.get("pushed_at", "")
                if pushed_at:
                    try:
                        last_push = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
                        if (datetime.now().replace(tzinfo=last_push.tzinfo) - last_push).days > updated_within:
                            continue
                    except:
                        pass
            
            # 公司信息筛选
            owner = repo.get("owner", {})
            owner_type = owner.get("type", "")
            
            lead = {
                "name": repo.get("name", ""),
                "full_name": repo.get("full_name", ""),
                "description": repo.get("description", ""),
                "url": repo.get("html_url", ""),
                "stars": stars,
                "forks": repo.get("forks_count", 0),
                "language": repo.get("language", ""),
                "created_at": repo.get("created_at", ""),
                "updated_at": repo.get("updated_at", ""),
                "pushed_at": repo.get("pushed_at", ""),
                "owner_login": owner.get("login", ""),
                "owner_type": owner_type,
                "owner_url": owner.get("html_url", ""),
                "topics": ",".join(repo.get("topics", [])),
            }
            
            filtered.append(lead)
        
        return filtered
    
    def enrich_leads(self, leads: List[Dict]) -> List[Dict]:
        """丰富线索信息（获取组织详情）"""
        enriched = []
        
        for lead in leads:
            if lead["owner_type"] == "Organization":
                org_details = self.get_org_details(lead["owner_login"])
                if org_details:
                    lead["company"] = org_details.get("company", "")
                    lead["blog"] = org_details.get("blog", "")
                    lead["location"] = org_details.get("location", "")
                    lead["email"] = org_details.get("email", "")
                    lead["public_repos"] = org_details.get("public_repos", 0)
                    lead["followers"] = org_details.get("followers", 0)
            
            enriched.append(lead)
        
        return enriched


def export_to_csv(leads: List[Dict], filepath: str):
    """导出线索到 CSV"""
    if not leads:
        print("没有数据可导出")
        return
    
    fieldnames = [
        "name", "full_name", "owner_login", "owner_type",
        "stars", "forks", "language", "topics",
        "company", "blog", "location", "email",
        "url", "owner_url", "description",
        "created_at", "updated_at", "pushed_at"
    ]
    
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(leads)
    
    print(f"已导出 {len(leads)} 条线索到 {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="扫描 GitHub 寻找潜在 AI 公司客户",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --search "transformer" --min-stars 500
  %(prog)s --search-ai --min-stars 1000 --updated-within 30
  %(prog)s --export leads.csv
        """
    )
    
    # 搜索参数
    parser.add_argument("--search", "-s", help="搜索关键词")
    parser.add_argument("--search-ai", action="store_true", help="使用 AI/ML 关键词搜索")
    parser.add_argument("--language", "-l", help="编程语言筛选 (如: python, javascript)")
    
    # 筛选参数
    parser.add_argument("--min-stars", type=int, default=0, help="最小 star 数")
    parser.add_argument("--max-stars", type=int, help="最大 star 数")
    parser.add_argument("--updated-within", type=int, help="最近 N 天内更新过")
    
    # 导出参数
    parser.add_argument("--export", "-o", help="导出到 CSV 文件路径")
    parser.add_argument("--enrich", action="store_true", help="丰富线索信息（需要更多 API 调用）")
    parser.add_argument("--limit", type=int, default=30, help="结果数量限制")
    
    # 其他
    parser.add_argument("--token", help="GitHub API Token (或设置 GITHUB_TOKEN 环境变量)")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    
    args = parser.parse_args()
    
    # 初始化扫描器
    scout = GitHubScout(token=args.token)
    
    # 执行搜索
    repos = []
    
    if args.search:
        print(f"搜索: {args.search}")
        query_parts = [args.search]
        if args.language:
            query_parts.append(f"language:{args.language}")
        repos = scout.search_repos(" ".join(query_parts), per_page=args.limit)
    elif args.search_ai:
        print("使用 AI/ML 关键词搜索...")
        repos = scout.search_ai_repos(
            min_stars=args.min_stars,
            language=args.language,
            updated_within=args.updated_within
        )
    else:
        parser.print_help()
        return
    
    if not repos:
        print("未找到匹配的仓库")
        return
    
    print(f"找到 {len(repos)} 个仓库")
    
    # 筛选
    leads = scout.filter_leads(
        repos,
        min_stars=args.min_stars,
        max_stars=args.max_stars,
        updated_within=args.updated_within
    )
    
    print(f"筛选后: {len(leads)} 个潜在客户")
    
    # 丰富信息
    if args.enrich:
        print("正在丰富线索信息...")
        leads = scout.enrich_leads(leads)
    
    # 导出或显示
    if args.export:
        export_to_csv(leads, args.export)
    elif args.json:
        print(json.dumps(leads, indent=2, ensure_ascii=False))
    else:
        # 表格输出
        print("\n" + "="*100)
        print(f"{'Name':<30} {'Stars':<8} {'Language':<12} {'Owner':<20} {'Type':<12}")
        print("="*100)
        
        for lead in leads[:20]:  # 最多显示20条
            name = lead["name"][:28] if len(lead["name"]) > 28 else lead["name"]
            owner = lead["owner_login"][:18] if len(lead["owner_login"]) > 18 else lead["owner_login"]
            lang = lead["language"] or "N/A"
            lang = lang[:10] if len(lang) > 10 else lang
            print(f"{name:<30} {lead['stars']:<8} {lang:<12} {owner:<20} {lead['owner_type']:<12}")
        
        if len(leads) > 20:
            print(f"\n... 还有 {len(leads) - 20} 条结果")
        
        print("="*100)
        print(f"\n使用 --export <file.csv> 导出完整结果")
        print(f"使用 --json 查看完整 JSON 数据")


if __name__ == "__main__":
    main()
