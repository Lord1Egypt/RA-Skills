#!/usr/bin/env python3
"""
GitSkills - GitHub CLI-like工具，专为OpenClaw设计
"""

import os
import argparse
import logging
import time
from dotenv import load_dotenv
from github import Github, GithubException

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class GitSkills:
    def __init__(self):
        """初始化GitSkills，使用GitHub token"""
        # 从环境变量中获取GitHub token
        self.github_token = os.getenv('GITHUB_TOKEN')
        if not self.github_token:
            logging.error("GitHub token not configured")
            raise EnvironmentError("GitHub token missing. Set GITHUB_TOKEN env var.")
        
        # 验证token格式（初步）
        if not self.github_token.startswith(('ghp_', 'gho_', 'ghu_', 'ghs_', 'ghr_')):
            logging.warning("GitHub token format unusual")
        
        try:
            # 初始化GitHub客户端
            self.g = Github(self.github_token)
            # 获取当前用户
            self.user = self.g.get_user()
            # 验证token有效性
            logging.info(f"Authenticated as {self.user.login}")
        except Exception as e:
            logging.error(f"GitHub authentication failed: {type(e).__name__}")
            raise
        
        # 速率限制处理
        self.max_retries = 3
    
    def _call_with_retry(self, func, *args, **kwargs):
        """带重试的API调用"""
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except GithubException as e:
                if e.status == 403 and 'rate limit' in str(e).lower():
                    if attempt < self.max_retries - 1:
                        wait = 2 ** attempt  # 指数退避
                        logging.warning(f"Rate limit hit, waiting {wait} seconds before retrying...")
                        time.sleep(wait)
                        continue
                raise
            except Exception as e:
                raise
    
    # 仓库管理
    def create_repo(self, name, description="", private=False):
        """创建新仓库"""
        # 输入验证
        if not name or not isinstance(name, str):
            raise ValueError("Repository name must be a non-empty string")
        
        repo = self._call_with_retry(
            self.user.create_repo,
            name=name,
            description=description,
            private=private
        )
        return f"仓库创建成功: {repo.html_url}"
    
    def list_repos(self):
        """列出用户的所有仓库"""
        repos = self._call_with_retry(self.user.get_repos)
        result = "你的仓库列表:\n"
        for repo in repos:
            result += f"- {repo.name}: {repo.html_url}\n"
        return result
    
    def get_repo(self, repo_name):
        """获取仓库详情"""
        # 输入验证
        if not repo_name or not isinstance(repo_name, str):
            raise ValueError("Repository name must be a non-empty string")
        
        try:
            repo = self._call_with_retry(self.user.get_repo, repo_name)
            return f"仓库: {repo.name}\n描述: {repo.description}\nURL: {repo.html_url}\n星标数: {repo.stargazers_count}"
        except Exception as e:
            logging.error(f"Error getting repo {repo_name}: {type(e).__name__}")
            return f"错误: 无法获取仓库信息"
    
    def delete_repo(self, repo_name, confirm=False):
        """删除仓库（需要明确确认）"""
        # 输入验证
        if not repo_name or not isinstance(repo_name, str):
            raise ValueError("Repository name must be a non-empty string")
        
        if not confirm:
            raise ValueError(
                f"Repository '{repo_name}' deletion requires explicit confirmation. "
                "This action is irreversible. Set confirm=True to proceed."
            )
        
        try:
            repo = self._call_with_retry(self.user.get_repo, repo_name)
            self._call_with_retry(repo.delete)
            return f"仓库 {repo_name} 已删除"
        except Exception as e:
            logging.error(f"Error deleting repo {repo_name}: {type(e).__name__}")
            return f"错误: 无法删除仓库"

    
    # 分支管理
    def create_branch(self, repo_name, branch_name):
        """创建新分支"""
        # 输入验证
        if not repo_name or not isinstance(repo_name, str):
            raise ValueError("Repository name must be a non-empty string")
        if not branch_name or not isinstance(branch_name, str):
            raise ValueError("Branch name must be a non-empty string")
        
        try:
            repo = self._call_with_retry(self.user.get_repo, repo_name)
            # 获取默认分支
            default_branch = repo.default_branch
            # 获取默认分支的最新提交
            base_branch = self._call_with_retry(repo.get_branch, default_branch)
            base_sha = base_branch.commit.sha
            # 创建新分支
            self._call_with_retry(
                repo.create_git_ref,
                f"refs/heads/{branch_name}",
                base_sha
            )
            return f"分支 {branch_name} 创建成功"
        except Exception as e:
            logging.error(f"Error creating branch {branch_name} in {repo_name}: {type(e).__name__}")
            return f"错误: 无法创建分支"
    
    def list_branches(self, repo_name):
        """列出仓库的所有分支"""
        # 输入验证
        if not repo_name or not isinstance(repo_name, str):
            raise ValueError("Repository name must be a non-empty string")
        
        try:
            repo = self._call_with_retry(self.user.get_repo, repo_name)
            branches = self._call_with_retry(repo.get_branches)
            result = f"{repo_name} 的分支列表:\n"
            for branch in branches:
                result += f"- {branch.name}\n"
            return result
        except Exception as e:
            logging.error(f"Error listing branches in {repo_name}: {type(e).__name__}")
            return f"错误: 无法列出分支"
    
    # PR管理
    def create_pr(self, repo_name, title, body, head, base):
        """创建PR"""
        # 输入验证
        if not repo_name or not isinstance(repo_name, str):
            raise ValueError("Repository name must be a non-empty string")
        if not title or not isinstance(title, str):
            raise ValueError("PR title must be a non-empty string")
        if not head or not isinstance(head, str):
            raise ValueError("Head branch must be a non-empty string")
        if not base or not isinstance(base, str):
            raise ValueError("Base branch must be a non-empty string")
        
        try:
            repo = self._call_with_retry(self.user.get_repo, repo_name)
            pr = self._call_with_retry(
                repo.create_pull,
                title=title,
                body=body,
                head=head,
                base=base
            )
            return f"PR创建成功: {pr.html_url}"
        except Exception as e:
            logging.error(f"Error creating PR in {repo_name}: {type(e).__name__}")
            return f"错误: 无法创建PR"
    
    def list_prs(self, repo_name):
        """列出仓库的所有PR"""
        # 输入验证
        if not repo_name or not isinstance(repo_name, str):
            raise ValueError("Repository name must be a non-empty string")
        
        try:
            repo = self._call_with_retry(self.user.get_repo, repo_name)
            prs = self._call_with_retry(repo.get_pulls)
            result = f"{repo_name} 的PR列表:\n"
            for pr in prs:
                result += f"- #{pr.number}: {pr.title} ({pr.state})\n"
            return result
        except Exception as e:
            logging.error(f"Error listing PRs in {repo_name}: {type(e).__name__}")
            return f"错误: 无法列出PR"
    
    # Issue管理
    def create_issue(self, repo_name, title, body):
        """创建Issue"""
        # 输入验证
        if not repo_name or not isinstance(repo_name, str):
            raise ValueError("Repository name must be a non-empty string")
        if not title or not isinstance(title, str):
            raise ValueError("Issue title must be a non-empty string")
        
        try:
            repo = self._call_with_retry(self.user.get_repo, repo_name)
            issue = self._call_with_retry(
                repo.create_issue,
                title=title,
                body=body
            )
            return f"Issue创建成功: {issue.html_url}"
        except Exception as e:
            logging.error(f"Error creating issue in {repo_name}: {type(e).__name__}")
            return f"错误: 无法创建Issue"
    
    def list_issues(self, repo_name):
        """列出仓库的所有Issue"""
        # 输入验证
        if not repo_name or not isinstance(repo_name, str):
            raise ValueError("Repository name must be a non-empty string")
        
        try:
            repo = self._call_with_retry(self.user.get_repo, repo_name)
            issues = self._call_with_retry(repo.get_issues, state="open")
            result = f"{repo_name} 的开放Issue列表:\n"
            for issue in issues:
                result += f"- #{issue.number}: {issue.title}\n"
            return result
        except Exception as e:
            logging.error(f"Error listing issues in {repo_name}: {type(e).__name__}")
            return f"错误: 无法列出Issue"


def main():
    """主函数"""
    # 创建命令行解析器
    parser = argparse.ArgumentParser(description='GitSkills - GitHub CLI-like工具，专为OpenClaw设计')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 仓库命令
    repo_parser = subparsers.add_parser('repo', help='仓库管理命令')
    repo_subparsers = repo_parser.add_subparsers(dest='repo_command')
    
    # 创建仓库
    create_repo_parser = repo_subparsers.add_parser('create', help='创建新仓库')
    create_repo_parser.add_argument('--name', required=True, help='仓库名称')
    create_repo_parser.add_argument('--description', default='', help='仓库描述')
    create_repo_parser.add_argument('--private', action='store_true', help='设置仓库为私有')
    
    # 列出仓库
    repo_subparsers.add_parser('list', help='列出仓库')
    
    # 获取仓库详情
    get_repo_parser = repo_subparsers.add_parser('get', help='获取仓库详情')
    get_repo_parser.add_argument('--name', required=True, help='仓库名称')
    
    # 删除仓库
    delete_repo_parser = repo_subparsers.add_parser('delete', help='删除仓库')
    delete_repo_parser.add_argument('--name', required=True, help='仓库名称')
    
    # 分支命令
    branch_parser = subparsers.add_parser('branch', help='分支管理命令')
    branch_subparsers = branch_parser.add_subparsers(dest='branch_command')
    
    # 创建分支
    create_branch_parser = branch_subparsers.add_parser('create', help='创建新分支')
    create_branch_parser.add_argument('--repo', required=True, help='仓库名称')
    create_branch_parser.add_argument('--name', required=True, help='分支名称')
    
    # 列出分支
    list_branches_parser = branch_subparsers.add_parser('list', help='列出分支')
    list_branches_parser.add_argument('--repo', required=True, help='仓库名称')
    
    # PR命令
    pr_parser = subparsers.add_parser('pr', help='PR管理命令')
    pr_subparsers = pr_parser.add_subparsers(dest='pr_command')
    
    # 创建PR
    create_pr_parser = pr_subparsers.add_parser('create', help='创建PR')
    create_pr_parser.add_argument('--repo', required=True, help='仓库名称')
    create_pr_parser.add_argument('--title', required=True, help='PR标题')
    create_pr_parser.add_argument('--body', default='', help='PR内容')
    create_pr_parser.add_argument('--head', required=True, help='源分支')
    create_pr_parser.add_argument('--base', required=True, help='目标分支')
    
    # 列出PR
    list_prs_parser = pr_subparsers.add_parser('list', help='列出PR')
    list_prs_parser.add_argument('--repo', required=True, help='仓库名称')
    
    # Issue命令
    issue_parser = subparsers.add_parser('issue', help='Issue管理命令')
    issue_subparsers = issue_parser.add_subparsers(dest='issue_command')
    
    # 创建Issue
    create_issue_parser = issue_subparsers.add_parser('create', help='创建Issue')
    create_issue_parser.add_argument('--repo', required=True, help='仓库名称')
    create_issue_parser.add_argument('--title', required=True, help='Issue标题')
    create_issue_parser.add_argument('--body', default='', help='Issue内容')
    
    # 列出Issue
    list_issues_parser = issue_subparsers.add_parser('list', help='列出Issue')
    list_issues_parser.add_argument('--repo', required=True, help='仓库名称')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    try:
        # 初始化GitSkills
        skills = GitSkills()
        
        # 处理仓库命令
        if args.command == 'repo':
            if args.repo_command == 'create':
                print(skills.create_repo(args.name, args.description, args.private))
            elif args.repo_command == 'list':
                print(skills.list_repos())
            elif args.repo_command == 'get':
                print(skills.get_repo(args.name))
            elif args.repo_command == 'delete':
                # 二次确认
                print(f"⚠️  警告：即将永久删除仓库 '{args.name}'")
                print("  此操作不可恢复！")
                confirm = input("  输入 'yes' 确认删除: ").strip()
                if confirm != 'yes':
                    print("  取消删除")
                else:
                    print(skills.delete_repo(args.name, confirm=True))
        
        # 处理分支命令
        elif args.command == 'branch':
            if args.branch_command == 'create':
                print(skills.create_branch(args.repo, args.name))
            elif args.branch_command == 'list':
                print(skills.list_branches(args.repo))
        
        # 处理PR命令
        elif args.command == 'pr':
            if args.pr_command == 'create':
                print(skills.create_pr(args.repo, args.title, args.body, args.head, args.base))
            elif args.pr_command == 'list':
                print(skills.list_prs(args.repo))
        
        # 处理Issue命令
        elif args.command == 'issue':
            if args.issue_command == 'create':
                print(skills.create_issue(args.repo, args.title, args.body))
            elif args.issue_command == 'list':
                print(skills.list_issues(args.repo))
        
    except ValueError as e:
        print(f"错误: {str(e)}")
    except EnvironmentError as e:
        print(f"环境错误: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {type(e).__name__}: {str(e)}")
        print("错误: 发生未知错误，请检查日志获取详细信息")

if __name__ == '__main__':
    main()

