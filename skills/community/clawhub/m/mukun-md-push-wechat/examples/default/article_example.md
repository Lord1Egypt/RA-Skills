---
title: 用 AI Agent 自动化你的周报工作流
digest: 从需求分析到落地部署，一步步构建一个能自动收集信息、生成周报并推送飞书的 AI Agent，实测每周节省2小时。
---

# 用 AI Agent 自动化你的周报工作流

## 为什么要自动化周报

每周五下午写周报大概是程序员最头疼的事之一：翻聊天记录、回忆本周做了什么、整理进展、汇总风险... 我估了一下，每周至少花 **2 小时**在这件事上。一年下来就是 100 多小时。

> 如果说有什么任务最适合交给 AI 来做，周报绝对是其中之一——它的格式固定、信息来源明确、不需要创造性思考。

## 整体思路

自动化周报的核心流程其实很简单：

1. **收集**：从 Git 提交记录、项目管理工具、聊天记录中提取本周工作内容
2. **整理**：用 LLM 对收集到的信息进行归纳、分类、去重
3. **生成**：按固定模板生成结构化的周报文档
4. **推送**：自动发送到飞书/钉钉/企业微信

## 技术选型

我最终选用的技术栈如下：

| 环节 | 方案 | 理由 |
|------|------|------|
| 编排框架 | LangGraph | 支持复杂的状态机和条件分支 |
| LLM | GPT-4o-mini | 性价比高，处理结构化任务足够 |
| Git 信息提取 | GitPython | 成熟稳定的 Git 操作库 |
| 飞书推送 | 飞书开放 API | 官方 SDK，文档完善 |
| 定时触发 | APScheduler | 轻量级定时任务框架 |

## 收集模块的实现

收集模块是整个 Agent 的基础。核心代码如下：

```python
def collect_git_commits(repo_path: str, since: str) -> list[dict]:
    """从 Git 仓库收集指定日期之后的提交记录"""
    repo = git.Repo(repo_path)
    commits = []
    for commit in repo.iter_commits(since=since):
        commits.append({
            "hash": commit.hexsha[:8],
            "message": commit.message.strip(),
            "date": commit.committed_datetime.isoformat(),
            "author": commit.author.name,
        })
    return commits
```

**关键点**：
- 使用 `since` 参数过滤本周的提交，避免处理过多历史数据
- 提取 commit message 的第一行作为摘要，减少 LLM 的输入噪声
- 保留 hash 方便溯源

> 如果你的团队使用 Conventional Commits 规范（如 `feat: xxx`、`fix: xxx`），收集后的信息质量会高很多，建议推广。

## 整理模块：让 LLM 做归纳

收集到的原始信息通常是碎片化的，需要 LLM 来归纳整理。我设计了一个专门的 Prompt：

```
你是一个周报助手。根据以下 Git 提交记录和任务卡片信息，
按「已完成」「进行中」「遇到的风险」三个类别进行归纳。
每条不超过 50 字，用动宾短语开头。

原始信息：
{raw_data}
```

经过测试，GPT-4o-mini 在这个任务上的表现非常稳定，归纳准确率在 **90%** 以上。

## 推送到飞书

生成周报后，通过飞书 Webhook 推送到指定群聊：

```python
def send_to_feishu(webhook_url: str, content: str):
    """通过飞书 Webhook 发送消息"""
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {"title": {"content": "本周工作周报"}},
            "elements": [{"tag": "markdown", "content": content}],
        },
    }
    requests.post(webhook_url, json=payload)
```

## 最终效果

部署上线后，每周五下午 5 点自动执行，2 分钟内完成全部流程：

- 自动拉取本周 Git 提交：约 200 条
- LLM 归纳整理：约 30 秒
- 生成飞书卡片：即时
- 推送到群聊：即时

**每周节省约 2 小时**，周报质量比手写的更好——因为 AI 不会遗漏任何一条提交。

## 下一步优化

- 接入 Jira/Tapd 自动拉取任务状态
- 支持多仓库聚合
- 增加与上周对比差异高亮
- 支持 Agent 主动提问补充信息
