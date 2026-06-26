# GitHub Team Collaboration

GitHub团队协作工具箱 - 管理开发团队工作流、代码审查和项目协调。

## 功能特性

- **Pull Request自动化**: 自动分配审查员、检查PR状态、合并策略
- **Issue管理**: 分类、标记、分配和跟踪问题
- **Sprint规划**: 里程碑管理、燃尽图、速度跟踪
- **团队指标**: PR审查时间、问题解决时间、贡献者统计
- **工作流自动化**: 分支保护、状态检查、发布管理

## 安装依赖

```bash
pip install -r requirements.txt
```

## 设置GitHub认证

将GitHub Token设置为环境变量：

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

## 使用方法

### 管理Pull Request

```python
from scripts.github_team import list_open_prs, assign_reviewers

# 列出开放PR
prs = list_open_prs("myorg", "myrepo")

# 自动分配审查员
assign_reviewers("myorg", "myrepo", 123, ["alice", "bob"])
```

### 跟踪Sprint进度

```python
from scripts.github_team import get_milestone_progress

# 获取sprint进度
progress = get_milestone_progress("myorg", "myrepo", "Sprint-15")
print(f"已完成: {progress['closed_issues']}/{progress['total_issues']}")
```

### 团队指标

```python
from scripts.github_team import get_team_metrics

# 分析团队指标
metrics = get_team_metrics("myorg", "myrepo", days=30)
print(f"平均审查时间: {metrics['avg_review_time']}小时")
```

## 支持的操作

- 仓库管理
- Pull Request生命周期
- Issue跟踪和分类
- 里程碑和项目管理
- 团队成员活动
- 发布管理
- Webhook配置
