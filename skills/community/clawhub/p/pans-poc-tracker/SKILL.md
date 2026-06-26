---
name: pans-poc-tracker
description: |
  AI算力销售POC追踪器。管理POC全生命周期，记录技术卡点，提醒跟进，生成转化报告。
  支持阶段跟踪、团队协作、风险预警。
  触发词：POC跟踪, 测试管理, 技术验证, POC进度, proof of concept, trial tracking
---

# pans-poc-tracker - AI算力销售POC追踪器

## 功能概述

管理AI算力销售POC（概念验证）全生命周期，支持阶段跟踪、技术卡点记录、团队协作和风险预警。

## POC 阶段

1. **申请阶段** - 客户提交POC申请，评估需求
2. **资源准备** - 准备GPU资源、网络配置
3. **环境部署** - 部署测试环境，配置集群
4. **测试执行** - 执行性能测试、稳定性测试
5. **结果评估** - 评估测试结果，分析数据
6. **商务转化** - 推进商务谈判，完成签单

## 数据字段

| 字段 | 说明 |
|------|------|
| poc_id | POC唯一标识 |
| customer | 客户名称 |
| poc_name | POC名称 |
| gpu_config | GPU配置（如 H100x8, A100x4） |
| test_scenario | 测试场景 |
| start_date | 开始日期 |
| end_date | 预计结束日期 |
| tech_owner | 技术负责人 |
| biz_owner | 商务负责人 |
| stage | 当前阶段 |
| progress | 进度百分比 |
| blockers | 技术卡点列表 |
| solutions | 解决方案 |
| feedback | 客户反馈 |
| conversion_prob | 转化概率（0-100） |
| status | 状态（active/closed_success/closed_failed） |
| created_at | 创建时间 |
| updated_at | 更新时间 |
| closed_at | 关闭时间 |
| closed_reason | 关闭原因 |

## CLI 用法

```bash
# 创建新POC（交互式）
python3 poc.py --create

# 列出所有POC
python3 poc.py --list

# 更新POC信息
python3 poc.py --update <poc_id>

# 更新阶段
python3 poc.py --stage <poc_id> <stage_name>

# 记录技术卡点
python3 poc.py --blocker <poc_id> <blocker_description>

# 记录客户反馈
python3 poc.py --feedback <poc_id> <feedback_text>

# 关闭POC
python3 poc.py --close <poc_id> <success|failed> [reason]

# 生成POC报告
python3 poc.py --report [poc_id]

# 显示今日待跟进
python3 poc.py --remind
```

## 数据存储

数据存储在 `~/.qclaw/skills/pans-poc-tracker/data/pocs.json`
