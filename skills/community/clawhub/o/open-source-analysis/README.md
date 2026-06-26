# open-source-analysis

## 功能说明
这个 skill 旨在根据用户提供的 GitHub 项目地址或名称，自动分析项目并生成一份结构化的开源项目分析报告。报告支持中英文双语输出（会根据用户的提问语言自动适配），内容涵盖：
- 项目一句话简介
- 主要技术栈与编程语言
- 实时项目数据（Stars, Forks 等）
- 使用的开源协议（License）
- 多维度的综合评分与评价依据（活跃度、文档完善度、社区活跃度、上手难度及综合评分）。

## 使用场景
当你遇到一个未知的开源项目，或者需要快速对某个项目进行背调、技术选型参考时，只需提供其 GitHub 地址。

## 提问示例

**中文模式：**
```text
请帮我分析一下这个项目：https://github.com/vuejs/core
```
```text
https://github.com/actionbook/actionbook
```

**英文模式：**
```text
Analyze the repository https://github.com/torvalds/linux
```