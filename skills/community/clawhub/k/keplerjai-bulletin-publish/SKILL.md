---
name: keplerjai-bulletin-publish
description: 采集 AI 新闻，校验 stage1 JSON，发布 KeplerJAI 简讯，并以可迁移、面向 agent workspace 的方式生成最终摘要。
---

# KeplerJAI Bulletin Skill

当目标是完成一套从 AI 新闻采集到简讯发布汇总的 KeplerJAI 工作流时，应使用这份 skill。

## 设计意图

这份 skill 围绕一套可迁移结构设计：

1. skill 目录提供提示词、脚本和工作流规则。
2. 目标 agent workspace 存放运行产物。
3. 面向用户的最终结果应是整理好的摘要文本，而不是中间执行报告。

这份 skill 应当能够在另一台机器上被 OpenClaw 学习并直接使用，正常情况下不应要求用户手工重写本地路径。

## 职责划分

OpenClaw 应负责：

1. 读取 `stage1-task-prompt.txt`
2. 采集合格的 AI 新闻条目
3. 将 stage1 输出写入目标运行目录

随后由 Python 脚本负责：

1. 校验 stage1 JSON
2. 发布简讯
3. 生成最终摘要
4. 向 `pipeline.log` 追加进度日志

## 执行边界

这份 skill 旨在作为单层工作流运行。

OpenClaw 应在当前运行中自行完成 stage1 采集。

以下方式都不应被当作默认的学习后执行路线：

1. `scripts/run_saved_pipeline.py`
2. 嵌套的 `openclaw agent ...` 命令
3. 为了做 stage1 采集而再额外启动一个完整 agent 的后台流程

这些路线仅是人工调试辅助方式，绝不能成为从这份 skill 中学习出的标准定时任务方案。

## 运行输出模式

运行产物应写入：

`<agent_workspace>/keplerjai-bulletin-publish`

预期输出包括：

- `stage1-output.txt`
- `stage1-output.normalized.json`
- `publish-result.json`
- `final-message.txt`
- `pipeline.log`

## 认证

优先认证变量：

```text
KEPLERAI_API_KEY
```

兼容认证变量：

```text
KEPLERJAI_BEARER_TOKEN
```

## 定时任务规则

如果基于这份 skill 创建定时任务，则应遵循：

1. 任务 owner 必须与目标 workspace 对齐。
2. 路径必须从本地已安装的 skill 目录和目标 workspace 自动推导。
3. 工作流必须保持可追踪。
4. 进度必须写入 `pipeline.log`。
5. 成功时只返回 `final-message.txt` 的内容。
6. stage1 采集必须在当前工作流中直接完成。
7. 绝不能把 `scripts/run_saved_pipeline.py` 作为学习后的定时任务执行路径。
8. 绝不能在定时任务内部再启动另一个 `openclaw agent` 进程。

只有在自动推导路径确实做不到时，才允许手工改写路径作为兜底。

## 参考文件

- `README.md`
- `CRON_SETUP.md`
- `stage1-task-prompt.txt`
