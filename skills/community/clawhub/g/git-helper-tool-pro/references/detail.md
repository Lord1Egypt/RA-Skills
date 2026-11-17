# 详细参考 - git-helper-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
import re
import subprocess
import json
from datetime import datetime

class ConflictAnalyzer:
    """智能冲突分析器"""

    CONFLICT_PATTERN = re.compile(
        r'<<<<<<< (\S+)\n(.*?)=======\n(.*?)>>>>>>> (\S+)',
        re.DOTALL
    )

    @staticmethod
    def analyze_conflicts(cwd=None):
        """分析所有冲突文件"""
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=U"],
            capture_output=True, text=True, cwd=cwd
        )
        conflict_files = result.stdout.strip().split('\n') if result.stdout.strip() else []

        analysis = {
            "analysis_time": datetime.now().isoformat(),
            "total_conflict_files": len(conflict_files),
            "files": []
        }

        for filepath in conflict_files:
            file_analysis = ConflictAnalyzer._analyze_file(filepath, cwd)
            analysis["files"].append(file_analysis)

        analysis["summary"] = ConflictAnalyzer._generate_summary(analysis["files"])
        return analysis

    @staticmethod
    def _analyze_file(filepath, cwd=None):
        """分析单个冲突文件"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            conflicts = list(ConflictAnalyzer.CONFLICT_PATTERN.finditer(content))

            file_info = {
                "file": filepath,
                "conflict_count": len(conflicts),
                "conflicts": [],
                "complexity": "low"
            }

            for i, match in enumerate(conflicts, 1):
                our_branch = match.group(1)
                our_code = match.group(2).strip()
                their_code = match.group(4)
                their_code_content = match.group(3).strip()

                conflict = {
                    "index": i,
                    "our_branch": our_branch,
                    "their_branch": their_code,
                    "our_lines": len(our_code.split('\n')),
                    "their_lines": len(their_code_content.split('\n')),
                    "our_code": our_code[:500],
                    "their_code": their_code_content[:500],
                    "analysis": ConflictAnalyzer._analyze_conflict_content(
                        our_code, their_code_content
                    )
                }
                file_info["conflicts"].append(conflict)

            total_lines = sum(c["our_lines"] + c["their_lines"] for c in file_info["conflicts"])
            if total_lines > 50:
                file_info["complexity"] = "high"
            elif total_lines > 20:
                file_info["complexity"] = "medium"

            return file_info

        except Exception as e:
            return {"file": filepath, "error": str(e)}

    @staticmethod
    def _analyze_conflict_content(our_code, their_code):
        """分析冲突内容类型"""
        analysis = {
            "type": "unknown",
            "recommendation": "手动检查并选择正确版本",
            "auto_resolvable": False
        }

        if our_code.strip() == their_code.strip():
            analysis["type"] = "whitespace"
            analysis["recommendation"] = "仅空白差异,任选其一即可"
            analysis["auto_resolvable"] = True

        elif our_code.strip().startswith("import") and their_code.strip().startswith("import"):
            analysis["type"] = "import"
            analysis["recommendation"] = "合并双方导入语句"
            analysis["auto_resolvable"] = True

        elif not our_code.strip() or not their_code.strip():
            analysis["type"] = "addition"
            analysis["recommendation"] = "保留有内容的一方"
            analysis["auto_resolvable"] = True

        elif re.search(r'["\']?\w+["\']?\s*[:=]\s*', our_code) and \
             re.search(r'["\']?\w+["\']?\s*[:=]\s*', their_code):
            analysis["type"] = "config"
            analysis["recommendation"] = "检查配置值,选择正确的配置"

        elif re.search(r'def\s+\w+|function\s+\w+', our_code) and \
             re.search(r'def\s+\w+|function\s+\w+', their_code):
            analysis["type"] = "function_signature"
            analysis["recommendation"] = "检查函数签名,合并参数"

        return analysis

    @staticmethod
    def _generate_summary(files):
        """生成摘要"""
        total_conflicts = sum(f.get("conflict_count", 0) for f in files)
        auto_resolvable = sum(
            1 for f in files for c in f.get("conflicts", [])
            if c.get("analysis", {}).get("auto_resolvable")
        )
        high_complexity = sum(1 for f in files if f.get("complexity") == "high")

        return {
            "total_conflicts": total_conflicts,
            "auto_resolvable": auto_resolvable,
            "manual_required": total_conflicts - auto_resolvable,
            "high_complexity_files": high_complexity,
            "recommendation": "优先处理自动可解决的冲突" if auto_resolvable > 0 else "所有冲突需手动解决"
        }

analyzer = ConflictAnalyzer()
analysis = analyzer.analyze_conflicts()
print(json.dumps(analysis, indent=2, ensure_ascii=False))
```

## 代码示例 (python)

```python
class GitRecoveryAssistant:
    """Git故障自动恢复助手"""

    RECOVERY_SCENARIOS = {
        "accidental_commit": {
            "description": "误提交了不需要的代码",
            "steps": [
                "git reset --soft HEAD~1   # 撤销提交,保留变更",
                "git restore --staged .     # 取消暂存",
                "git restore .              # 丢弃变更(如需要)"
            ],
            "safe": True
        },
        "accidental_push": {
            "description": "误推送了提交到远程",
            "steps": [
                "git revert <commit-sha>    # 创建反向提交(安全)",
                "git push origin <branch>   # 推送撤销"
            ],
            "safe": True
        },
        "accidental_delete_branch": {
            "description": "误删除了本地分支",
            "steps": [
                "git reflog                 # 查找分支最后位置",
                "git checkout -b <branch> <sha>  # 从SHA恢复分支"
            ],
            "safe": True
        },
        "accidental_reset": {
            "description": "误执行了git reset --hard",
            "steps": [
                "git reflog                 # 查找reset前的提交",
                "git reset --hard <sha>     # 恢复到该提交"
            ],
            "safe": True
        },
        "merge_conflict_stuck": {
            "description": "合并冲突中无法继续",
            "steps": [
                "git merge --abort          # 取消合并",
                "git reset --hard HEAD       # 重置到合并前状态"
            ],
            "safe": True
        },
        "rebase_stuck": {
            "description": "变基过程中卡住",
            "steps": [
                "git rebase --abort         # 取消变基",
                "# 解决冲突后重新变基"
            ],
            "safe": True
        },
        "detached_head": {
            "description": "处于分离HEAD状态",
            "steps": [
                "git branch temp-branch     # 创建临时分支保存",
                "git switch main            # 切回主分支",
                "git merge temp-branch      # 合并临时分支"
            ],
            "safe": True
        }
    }

    @staticmethod
    def detect_issue(cwd=None):
        """自动检测当前问题"""
        issues = []

        merge_head = subprocess.run(
            ["git", "rev-parse", "--verify", "MERGE_HEAD"],
            capture_output=True, text=True, cwd=cwd
        )
        if merge_head.returncode == 0:
            issues.append({
                "scenario": "merge_conflict_stuck",
                "message": "检测到正在合并中"
            })

        rebase_dir = subprocess.run(
            ["test", "-d", ".git/rebase-merge"],
            capture_output=True, cwd=cwd
        )
        if rebase_dir.returncode == 0:
            issues.append({
                "scenario": "rebase_stuck",
                "message": "检测到正在变基中"
            })

        symbolic = subprocess.run(
            ["git", "symbolic-ref", "-q", "HEAD"],
            capture_output=True, text=True, cwd=cwd
        )
        if symbolic.returncode != 0:
            issues.append({
                "scenario": "detached_head",
                "message": "检测到分离HEAD状态"
            })

        return issues

    @staticmethod
    def get_recovery_plan(scenario):
        """获取恢复方案"""
        plan = GitRecoveryAssistant.RECOVERY_SCENARIOS.get(scenario)
        if plan:
            return {
                "scenario": scenario,
                "description": plan["description"],
                "steps": plan["steps"],
                "safe": plan["safe"]
            }
        return None

    @staticmethod
    def auto_recover(scenario, cwd=None):
        """自动执行恢复"""
        plan = GitRecoveryAssistant.get_recovery_plan(scenario)
        if not plan or not plan["safe"]:
            return {"success": False, "message": "无法自动恢复,需手动处理"}

        results = []
        for step in plan["steps"]:
            if step.startswith("#"):
                results.append({"step": step, "status": "skip"})
                continue

            cmd = step.split()
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
            results.append({
                "step": step,
                "status": "success" if result.returncode == 0 else "failed",
                "output": result.stdout + result.stderr
            })

            if result.returncode != 0:
                return {"success": False, "results": results}

        return {"success": True, "results": results}
```

## 代码示例 (python)

```python
class BatchRepositoryDiagnostics:
    """批量仓库诊断工具"""

    def __init__(self, repo_paths):
        self.repos = repo_paths

    def diagnose_all(self):
        """诊断所有仓库"""
        results = {}
        for repo in self.repos:
            results[repo] = self._diagnose_repo(repo)
        return self._generate_summary(results)

    def _diagnose_repo(self, repo_path):
        """诊断单个仓库"""
        diag = {"path": repo_path, "issues": [], "status": "healthy"}

        try:
            status = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, cwd=repo_path
            )
            if status.stdout.strip():
                diag["issues"].append({
                    "level": "warning",
                    "issue": "有未提交的变更",
                    "count": len(status.stdout.strip().split('\n'))
                })

            ahead = subprocess.run(
                ["git", "rev-list", "--count", "@{upstream}..HEAD"],
                capture_output=True, text=True, cwd=repo_path
            )
            if ahead.stdout.strip().isdigit() and int(ahead.stdout) > 0:
                diag["issues"].append({
                    "level": "warning",
                    "issue": f"有{ahead.stdout.strip()}个未推送提交"
                })

            behind = subprocess.run(
                ["git", "rev-list", "--count", "HEAD..@{upstream}"],
                capture_output=True, text=True, cwd=repo_path
            )
            if behind.stdout.strip().isdigit() and int(behind.stdout) > 0:
                diag["issues"].append({
                    "level": "info",
                    "issue": f"落后远程{behind.stdout.strip()}个提交"
                })

            stash = subprocess.run(
                ["git", "stash", "list"],
                capture_output=True, text=True, cwd=repo_path
            )
            if stash.stdout.strip():
                count = len(stash.stdout.strip().split('\n'))
                if count > 5:
                    diag["issues"].append({
                        "level": "info",
                        "issue": f"有{count}个stash"
                    })

            size = subprocess.run(
                ["du", "-sh", ".git"],
                capture_output=True, text=True, cwd=repo_path
            )
            if size.stdout:
                size_str = size.stdout.split('\t')[0]
                if 'G' in size_str:
                    diag["issues"].append({
                        "level": "warning",
                        "issue": f"仓库较大({size_str}),建议优化"
                    })

            merged = subprocess.run(
                ["git", "branch", "--merged"],
                capture_output=True, text=True, cwd=repo_path
            )
            merged_branches = [
                b.strip().lstrip('* ') for b in merged.stdout.split('\n')
                if b.strip() and b.strip() not in ['main', 'master']
            ]
            if merged_branches:
                diag["issues"].append({
                    "level": "info",
                    "issue": f"有{len(merged_branches)}个可清理的分支"
                })

            if diag["issues"]:
                diag["status"] = "needs_attention"

        except Exception as e:
            diag["status"] = "error"
            diag["issues"].append({"level": "error", "issue": str(e)})

        return diag

    def _generate_summary(self, results):
        """生成诊断摘要"""
        total = len(results)
        healthy = sum(1 for r in results.values() if r["status"] == "healthy")
        needs_attention = sum(1 for r in results.values() if r["status"] == "needs_attention")
        errors = sum(1 for r in results.values() if r["status"] == "error")

        return {
            "diagnosis_time": datetime.now().isoformat(),
            "total_repos": total,
            "healthy": healthy,
            "needs_attention": needs_attention,
            "errors": errors,
            "details": results
        }
```

## 代码示例 (python)

```python
class GitKnowledgeBase:
    """Git团队知识库"""

    FAQ = {
        "如何撤销最近的提交": {
            "answer": "使用 git reset --soft HEAD~1 撤销提交但保留变更",
            "command": "git reset --soft HEAD~1",
            "category": "撤销操作"
        },
        "如何修改最近的提交信息": {
            "answer": "使用 git commit --amend -m '新信息' 修改",
            "command": "git commit --amend -m 'new message'",
            "category": "提交管理"
        },
        "如何解决合并冲突": {
            "answer": "1.查看冲突文件 2.编辑解决 3.git add 4.git commit",
            "command": "git diff --name-only --diff-filter=U",
            "category": "冲突解决"
        },
        "如何创建标签": {
            "answer": "使用 git tag -a v1.0 -m '版本说明' 创建附注标签",
            "command": "git tag -a v1.0 -m 'message'",
            "category": "版本管理"
        },
        "如何查看文件历史": {
            "answer": "使用 git log --oneline -- file.txt 查看文件提交历史",
            "command": "git log --oneline -- file.txt",
            "category": "历史查看"
        }
    }

    TROUBLESHOOTING = {
        "push被拒绝(non-fast-forward)": {
            "cause": "远程有你本地没有的提交",
            "solution": "先 git pull --rebase 再 push",
            "commands": [
                "git pull --rebase origin main",
                "git push origin main"
            ]
        },
        "merge conflict无法解决": {
            "cause": "合并冲突未完全解决",
            "solution": "检查冲突标记,确保全部解决",
            "commands": [
                "grep -r '<<<\\|>>>\\|===' .",
                "git add .",
                "git commit"
            ]
        },
        "fatal: not a git repository": {
            "cause": "不在Git仓库目录中",
            "solution": "切换到仓库目录或初始化仓库",
            "commands": [
                "cd /path/to/repo",
                "# 或 git init"
            ]
        },
        "permission denied (publickey)": {
            "cause": "SSH密钥未配置或未添加",
            "solution": "生成SSH密钥并添加到Git平台",
            "commands": [
                "ssh-keygen -t ed25519 -C 'email'",
                "cat ~/.ssh/id_ed25519.pub",
                "# 添加到Git平台"
            ]
        }
    }

    @staticmethod
    def search(query):
        """搜索知识库"""
        results = {"faq": [], "troubleshooting": []}

        for question, info in GitKnowledgeBase.FAQ.items():
            if query.lower() in question.lower():
                results["faq"].append({
                    "question": question,
                    "answer": info["answer"],
                    "command": info["command"],
                    "category": info["category"]
                })

        for problem, info in GitKnowledgeBase.TROUBLESHOOTING.items():
            if query.lower() in problem.lower():
                results["troubleshooting"].append({
                    "problem": problem,
                    "cause": info["cause"],
                    "solution": info["solution"],
                    "commands": info["commands"]
                })

        return results

    @staticmethod
    def get_all_categories():
        """获取所有分类"""
        categories = set()
        for info in GitKnowledgeBase.FAQ.values():
            categories.add(info["category"])
        return sorted(categories)
```

