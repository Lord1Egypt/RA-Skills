---
name: jira-issue-analyzer
description: Jira 问题分析编排器。负责获取 issue 与附件、委托日志分析 subagent，并产出最终 Markdown 报告到本地目录。适用于用户要求生成 Jira 问题分析文档的场景。
---

# Jira Issue Analyzer

## 前置检查

1. Jira 脚本目录（已迁移到 Skill 内，不在项目目录）：
   - `~/.cursor/skills/jira-issue-analyzer/jira`
2. 初始化虚拟环境（必须）：
   - `cd ~/.cursor/skills/jira-issue-analyzer/jira`
   - `python3 -m venv .venv`
   - `.venv/bin/python -m pip install -r requirements.txt`
3. 配置：
   - `cp .env.example .env`
   - 填写 `JIRA_BASE_URL`、`JIRA_TOKEN`
4. 连接测试（必须使用 venv python）：
   - `.venv/bin/python main.py --test`

## 标准工作流

### 1) 获取 issue 信息

```bash
cd ~/.cursor/skills/jira-issue-analyzer/jira
.venv/bin/python main.py get <ISSUE_KEY_OR_URL> -f json
```

### 2) 下载附件

```bash
cd ~/.cursor/skills/jira-issue-analyzer/jira
.venv/bin/python main.py download <ISSUE_KEY_OR_URL> -d /tmp/jira_<ISSUE_KEY>
```

### 3) 解压压缩包并递归处理

需要时解压压缩包，作为后续分析输入。

### 4) 委托日志分析 subagent

日志分析与问题归因请直接委托个人 subagent：
- `jira-log-analyst`（定义文件：`~/.cursor/agents/jira-log-analyst.md`）

### 5) 输出标准报告

按 [report-template.md](report-template.md) 结构输出。

### 6) 报告落地到本地文件

将报告以 Markdown 文件保存到项目目录：
- 目录：`<project>/.cursor/work/jira/`
- 文件名建议：`<ISSUE_KEY>_analysis.md`

示例路径：
- `/Users/zhangyu/FlutterProject/flutter_hiigge_app/.cursor/work/jira/PI2506-150_analysis.md`

### 7) 清理下载附件

报告生成并保存后，删除临时附件目录，避免磁盘堆积：
- 例如删除 `/tmp/jira_<ISSUE_KEY>`
- 必须在报告落盘完成后再执行

## 快速命令参考

```bash
# 获取 issue 详情
cd ~/.cursor/skills/jira-issue-analyzer/jira
.venv/bin/python main.py get HA-2560 -f json

# 下载附件
.venv/bin/python main.py download HA-2560 -d /tmp/jira_HA-2560
```

