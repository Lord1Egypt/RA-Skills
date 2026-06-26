---
name: policy-to-checklist
description: 把征稿启事、通知、比赛规则、制度文件、招标要求等转成可执行检查清单与时间线。
metadata: {"openclaw":{"emoji":"✅","requires":{"bins":["node","pbpaste"]}}}
---

# Policy To Checklist

这是一个把复杂要求文档转成执行清单的 skill。

## 主要用途

适合处理：
- 征稿通知
- 投稿要求
- 比赛规则
- 申报书要求
- 制度文件
- 招标要求
- 申请表填写说明
- 项目申报通知

## 调用方式

当用户说：
- 读取剪贴板并整理成清单
- 把这段通知变成执行 checklist
- 帮我提取要求和截止信息
- 把投稿要求拆成步骤

你应运行：

```bash
node {baseDir}/scripts/read_clipboard.mjs