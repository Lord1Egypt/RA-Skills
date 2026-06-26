# openrank-metrics

## 功能说明
这个 skill 旨在对接开源项目与社区生态指标系统 **OpenDigger**（基于 `oss.open-digger.cn` 数据源），根据用户提供的 GitHub 或 Gitee 仓库地址/开发者名称，快速查询并展示各类开源统计数据。

支持的查询维度包括但不限于：
- **核心指标**：全域 OpenRank、社区 OpenRank、活跃度（Activity）、Stars、关注度（Attention）、技术分叉等。
- **开发者指标**：贡献者数量、新老贡献者比例、参与者、核心贡献者缺席因素（Bus Factor）等。
- **社区运作指标**：Issues 及 PR 的创建与关闭数量、代码行数变更等。

Skill 能够根据查询意图自动提取“最新月份/年份数据及近期趋势”，或输出“指定周期（如2024年度、2023-05等）的全部指标全貌表格”。

## 使用场景
用于衡量开源项目的健康状况、影响力和活跃趋势，支持技术选型背调、开发者社区表现分析等场景。

## 提问示例

**查询最新概览与趋势：**
```text
查询一下 X-lab2017/open-digger 的 OpenRank 数据
```
```text
What is the OpenRank and activity for torvalds/linux?
```

**查询特定周期全貌表格：**
```text
请用表格的形式展示 https://github.com/vuejs/core 在 2024 年度的全部指标数据全貌
```
```text
Show me all metrics for gitee/mindspore/mindspore in 2023-12 as a table.
```