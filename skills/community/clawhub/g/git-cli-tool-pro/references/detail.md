# 详细参考 - git-cli-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
class GitDiagnostics:
    """Git仓库深度诊断"""

    @staticmethod
    def full_diagnosis(cwd=None):
        """完整诊断"""
        return {
            "diagnosis_time": datetime.now().isoformat(),
            "repository": GitDiagnostics._repo_info(cwd),
            "health": GitDiagnostics._health_check(cwd),
            "performance": GitDiagnostics._performance_check(cwd),
            "security": GitDiagnostics._security_check(cwd),
            "recommendations": GitDiagnostics._recommendations(cwd)
        }

    @staticmethod
    def _repo_info(cwd=None):
        """仓库基本信息"""
        return {
            "branch": GitAutomation.run_git("branch", "--show-current", cwd=cwd),
            "remote": GitAutomation.run_git("remote", "-v", cwd=cwd),
            "total_commits": GitAutomation.run_git("rev-list", "--count", "HEAD", cwd=cwd),
            "total_branches": len(GitAutomation.run_git("branch", "-a", cwd=cwd).split('\n')),
            "repo_size": GitDiagnostics._get_repo_size(cwd)
        }

    @staticmethod
    def _get_repo_size(cwd=None):
        """获取仓库大小"""
        cmd = ["du", "-sh", ".git"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
        return result.stdout.strip().split('\t')[0] if result.stdout else "unknown"

    @staticmethod
    def _health_check(cwd=None):
        """健康检查"""
        issues = []

        status = GitAutomation.get_repo_status(cwd)

        if not status["is_clean"]:
            issues.append({
                "level": "warning",
                "issue": "有未提交的变更",
                "details": f"暂存:{len(status['staged'])}, 修改:{len(status['modified'])}, 未跟踪:{len(status['untracked'])}"
            })

        if status["ahead"] > 0:
            issues.append({
                "level": "warning",
                "issue": f"有{status['ahead']}个未推送的提交"
            })

        if status["stash_count"] > 5:
            issues.append({
                "level": "info",
                "issue": f"有{status['stash_count']}个stash,建议清理"
            })

        large_files = GitDiagnostics._check_large_files(cwd)
        if large_files:
            issues.append({
                "level": "warning",
                "issue": "发现大文件",
                "details": large_files
            })

        return {
            "status": "healthy" if not issues else "needs_attention",
            "issues": issues
        }

    @staticmethod
    def _check_large_files(cwd=None, threshold=10*1024*1024):
        """检查大文件"""
        result = subprocess.run(
            ["git", "rev-list", "--objects", "--all"],
            capture_output=True, text=True, cwd=cwd
        )
        large_files = []
        for line in result.stdout.split('\n'):
            parts = line.split(' ', 1)
            if len(parts) == 2:
                sha, path = parts
                size_result = subprocess.run(
                    ["git", "cat-file", "-s", sha],
                    capture_output=True, text=True, cwd=cwd
                )
                if size_result.stdout.strip().isdigit():
                    size = int(size_result.stdout.strip())
                    if size > threshold:
                        large_files.append({
                            "file": path,
                            "size_mb": round(size / 1024 / 1024, 2)
                        })
        return large_files[:10]

    @staticmethod
    def _performance_check(cwd=None):
        """性能检查"""
        issues = []

        size = GitDiagnostics._get_repo_size(cwd)
        if "G" in size:
            issues.append({
                "level": "warning",
                "issue": f"仓库较大({size}),建议使用git gc优化"
            })

        result = subprocess.run(
            ["git", "count-objects", "-v"],
            capture_output=True, text=True, cwd=cwd
        )
        for line in result.stdout.split('\n'):
            if line.startswith("count:") and int(line.split()[1]) > 10000:
                issues.append({
                    "level": "info",
                    "issue": "松散对象较多,建议运行git gc"
                })

        return {"status": "ok" if not issues else "optimize", "issues": issues}

    @staticmethod
    def _security_check(cwd=None):
        """安全检查"""
        issues = []

        result = subprocess.run(
            ["git", "log", "--all", "--diff-filter=A", "--name-only", "--format="],
            capture_output=True, text=True, cwd=cwd
        )
        sensitive_patterns = ['.env', '.pem', '.key', '.secret', 'credentials']
        for line in result.stdout.split('\n'):
            for pattern in sensitive_patterns:
                if pattern in line.lower():
                    issues.append({
                        "level": "critical",
                        "issue": f"可能包含敏感文件: {line}"
                    })

        return {"status": "secure" if not issues else "at_risk", "issues": issues}

    @staticmethod
    def _recommendations(cwd=None):
        """生成建议"""
        recs = []
        health = GitDiagnostics._health_check(cwd)

        for issue in health["issues"]:
            if "未提交" in issue["issue"]:
                recs.append("提交或暂存当前变更")
            if "未推送" in issue["issue"]:
                recs.append("推送未推送的提交到远程")
            if "stash" in issue["issue"]:
                recs.append("清理不需要的stash")
            if "大文件" in issue["issue"]:
                recs.append("考虑使用Git LFS管理大文件")

        return recs
```

## 代码示例 (python)

```python
import subprocess
import json
import os
from datetime import datetime

class GitAutomation:
    """Git自动化操作库"""

    @staticmethod
    def run_git(*args, cwd=None):
        """执行Git命令"""
        cmd = ["git"] + list(args)
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=cwd
        )
        if result.returncode != 0:
            raise RuntimeError(f"Git命令失败: {' '.join(cmd)}\n{result.stderr}")
        return result.stdout.strip()

    @staticmethod
    def get_repo_status(cwd=None):
        """获取仓库完整状态"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "branch": GitAutomation.run_git("branch", "--show-current", cwd=cwd),
            "is_clean": False,
            "staged": [],
            "modified": [],
            "untracked": [],
            "ahead": 0,
            "behind": 0,
            "stash_count": 0,
            "last_commit": None
        }

        output = GitAutomation.run_git("status", "--porcelain=v2", "--branch", cwd=cwd)
        for line in output.split('\n'):
            if line.startswith('# branch.head'):
                status["branch"] = line.split()[-1]
            elif line.startswith('# branch.ab'):
                parts = line.split()
                status["ahead"] = int(parts[2].lstrip('+'))
                status["behind"] = int(parts[3].lstrip('-'))
            elif line.startswith('1 '):
                parts = line.split()
                file_path = parts[-1]
                xy = parts[1]
                if xy[0] != '.':
                    status["staged"].append(file_path)
                if xy[1] != '.':
                    status["modified"].append(file_path)
            elif line.startswith('? '):
                status["untracked"].append(line[2:])

        status["is_clean"] = not (status["staged"] or status["modified"] or status["untracked"])

        stash_output = GitAutomation.run_git("stash", "list", cwd=cwd)
        status["stash_count"] = len(stash_output.split('\n')) if stash_output else 0

        last_commit = GitAutomation.run_git(
            "log", "-1", "--format=%H|%an|%ar|%s", cwd=cwd
        )
        if last_commit:
            parts = last_commit.split('|', 3)
            status["last_commit"] = {
                "hash": parts[0],
                "author": parts[1],
                "time": parts[2],
                "message": parts[3]
            }

        return status

    @staticmethod
    def smart_commit(message, cwd=None):
        """智能提交"""
        status = GitAutomation.get_repo_status(cwd)

        if status["is_clean"]:
            return {"success": False, "message": "没有变更需要提交"}

        if status["modified"] or status["untracked"]:
            GitAutomation.run_git("add", "-A", cwd=cwd)

        GitAutomation.run_git("commit", "-m", message, cwd=cwd)

        return {
            "success": True,
            "message": message,
            "files_committed": len(status["staged"] + status["modified"] + status["untracked"])
        }

    @staticmethod
    def sync_branch(cwd=None):
        """智能同步分支"""
        results = {"fetched": False, "pulled": False, "pushed": False}

        GitAutomation.run_git("fetch", "--all", "--prune", cwd=cwd)
        results["fetched"] = True

        status = GitAutomation.get_repo_status(cwd)
        if status["behind"] > 0:
            GitAutomation.run_git("pull", "--rebase", cwd=cwd)
            results["pulled"] = True

        if status["ahead"] > 0:
            GitAutomation.run_git("push", cwd=cwd)
            results["pushed"] = True

        return results

    @staticmethod
    def create_feature_branch(name, base="main", cwd=None):
        """创建功能分支"""
        GitAutomation.run_git("fetch", "origin", base, cwd=cwd)
        GitAutomation.run_git("switch", base, cwd=cwd)
        GitAutomation.run_git("pull", "--rebase", cwd=cwd)

        branch_name = f"feature/{name}" if not name.startswith("feature/") else name
        GitAutomation.run_git("switch", "-c", branch_name, cwd=cwd)

        GitAutomation.run_git("push", "-u", "origin", branch_name, cwd=cwd)

        return {"branch": branch_name, "base": base}

    @staticmethod
    def finish_feature_branch(branch_name=None, cwd=None):
        """完成功能分支(合并并清理)"""
        if not branch_name:
            branch_name = GitAutomation.run_git("branch", "--show-current", cwd=cwd)

        status = GitAutomation.get_repo_status(cwd)
        if not status["is_clean"]:
            return {"success": False, "message": "工作区不干净,请先提交或暂存"}

        GitAutomation.run_git("switch", "main", cwd=cwd)
        GitAutomation.run_git("pull", "--rebase", cwd=cwd)

        GitAutomation.run_git("merge", "--no-ff", branch_name, cwd=cwd)

        GitAutomation.run_git("push", cwd=cwd)

        GitAutomation.run_git("branch", "-d", branch_name, cwd=cwd)
        GitAutomation.run_git("push", "origin", "--delete", branch_name, cwd=cwd)

        return {"success": True, "merged": branch_name, "deleted": True}

automation = GitAutomation()

status = automation.get_repo_status()
print(json.dumps(status, indent=2, ensure_ascii=False))

```

## 代码示例 (bash)

```bash
#!/bin/bash
workflow_feature() {
    local name="$1"
    echo "=== 功能开发工作流: $name ==="

    git fetch --all --prune
    git switch main
    git pull --rebase
    git switch -c "feature/$name"
    git push -u origin "feature/$name"

    echo "功能分支已创建: feature/$name"
    echo "开发完成后运行: workflow_finish_feature $name"
}

workflow_finish_feature() {
    local name="$1"
    echo "=== 完成功能: $name ==="

    if [ -n "$(git status --porcelain)" ]; then
        echo "[!] 工作区不干净,请先提交"
        return 1
    fi

    git switch main
    git pull --rebase

    git merge --no-ff "feature/$name"
    git push

    git branch -d "feature/$name"
    git push origin --delete "feature/$name"

    echo "功能已合并并清理: feature/$name"
}

workflow_hotfix() {
    local issue="$1"
    echo "=== 热修复工作流: $issue ==="

    git switch main
    git pull --rebase
    git switch -c "hotfix/$issue"
    echo "热修复分支已创建: hotfix/$issue"
    echo "修复后运行: workflow_finish_hotfix $issue"
}

workflow_finish_hotfix() {
    local issue="$1"
    echo "=== 完成热修复: $issue ==="

    git switch main
    git merge --no-ff "hotfix/$issue"
    git push

    git tag -a "hotfix-$issue-$(date +%Y%m%d)" -m "热修复: $issue"
    git push --tags

    git branch -d "hotfix/$issue"
    git push origin --delete "hotfix/$issue"

    echo "热修复已完成并打标签"
}

workflow_release() {
    local version="$1"
    echo "=== 发布工作流: v$version ==="

    git switch main
    git pull --rebase

    git switch -c "release/v$version"

    echo "发布分支已创建: release/v$version"
    echo "测试通过后运行: workflow_finish_release $version"
}

workflow_finish_release() {
    local version="$1"
    echo "=== 完成发布: v$version ==="

    git switch main
    git merge --no-ff "release/v$version"

    git tag -a "v$version" -m "发布版本 v$version"
    git push
    git push --tags

    git branch -d "release/v$version"
    git push origin --delete "release/v$version"

    echo "版本 v$version 已发布"
}
```

## 代码示例 (python)

```python
class MultiRepoManager:
    """多仓库统一管理"""

    def __init__(self, repos_file):
        self.repos = self._load_repos(repos_file)

    def _load_repos(self, repos_file):
        """加载仓库列表"""
        repos = []
        with open(repos_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    repos.append(line)
        return repos

    def batch_status(self):
        """批量获取状态"""
        results = {}
        for repo in self.repos:
            if os.path.exists(repo):
                try:
                    results[repo] = GitAutomation.get_repo_status(cwd=repo)
                except Exception as e:
                    results[repo] = {"error": str(e)}
            else:
                results[repo] = {"error": "仓库目录不存在"}
        return results

    def batch_sync(self):
        """批量同步所有仓库"""
        results = {}
        for repo in self.repos:
            if os.path.exists(repo):
                try:
                    results[repo] = GitAutomation.sync_branch(cwd=repo)
                except Exception as e:
                    results[repo] = {"error": str(e)}
        return results

    def batch_cleanup(self):
        """批量清理所有仓库"""
        results = {}
        for repo in self.repos:
            if os.path.exists(repo):
                try:
                    output = subprocess.run(
                        ["git", "branch", "--merged", "main"],
                        capture_output=True, text=True, cwd=repo
                    )
                    branches = [
                        b.strip().lstrip('* ') for b in output.stdout.split('\n')
                        if b.strip() and b.strip() != 'main' and b.strip() != 'master'
                    ]
                    for branch in branches:
                        subprocess.run(["git", "branch", "-d", branch], cwd=repo)
                    results[repo] = {"cleaned": branches}
                except Exception as e:
                    results[repo] = {"error": str(e)}
        return results
```

