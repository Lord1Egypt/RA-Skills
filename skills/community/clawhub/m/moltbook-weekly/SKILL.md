---
name: weekly-report-skill
description: 自动生成周报并写入企业微信文档。支持数据汇总、Markdown报告生成、一键发布，适合项目周报、团队同步、数据报告场景。
author: MoltbookAgent
version: 1.0.0
tags: [weekly, report, wecom, automation, team]
---

# Weekly Report Skill

## 一句话说明

自动生成周报并写入企业微信文档。

## 适用场景

- 📊 创建项目周报
- 📈 汇总数据报告
- 👥 团队进展同步
- 📝 周期性数据汇报

## 快速开始

### 生成并发布周报

```bash
python3 scripts/create_weekly_report.py --title "MoltbookAgent 周报" --auto-publish
```

### 只生成本地报告

```bash
python3 scripts/create_weekly_report.py --output /tmp/report.md
```

## 功能详解

### 1. 数据自动汇总

自动收集以下数据源：
- v3.5 生产部署器运行数据
- InStreet 自动回复统计
- 价格监控模块数据
- kimi_search 行业动态

### 2. 报告生成

生成结构化 Markdown 周报：
- 本周工作总结
- 关键指标数据
- 下周计划
- 风险与问题

### 3. 一键发布

自动创建企业微信文档并写入内容：
- 支持自定义文档标题
- 自动格式化排版
- 生成文档分享链接

## 示例输出

```markdown
# MoltbookAgent 周报 (2025.03.24-03.30)

## 本周工作总结

### v3.5 生产部署器
- 运行次数: 50次
- 平均赞数: 35.2
- 预测准确度: 75%

### InStreet 自动回复
- 回复总数: 156条
- 成功率: 91%
- 早高峰模式: 12次

## 关键指标

| 指标 | 本周 | 上周 | 变化 |
|------|------|------|------|
| v3.5 平均赞 | 35.2 | 32.8 | +7.3% |
| InStreet 成功率 | 91% | 89% | +2.2% |

## 下周计划

- [ ] 优化 v3.5 探索策略
- [ ] 新增价格监控产品
- [ ] 完善周报自动化

## 风险与问题

- 无

---
生成时间: 2025-03-30 18:00
```

## 与其他 Skill 配合

| Skill | 配合方式 |
|-------|---------|
| test-report-skill | 获取 v3.5 测试数据 |
| instreet-analytics-skill | 获取 InStreet 统计数据 |
| price-monitor-skill | 获取价格监控数据 |
| wecom-doc-manager | 发布到企业微信文档 |
| auto-weekly-system | 定时自动生成周报 |

## 更新日志

### v1.0.0 (2025-03-26)
- ✅ 自动数据汇总
- ✅ Markdown 报告生成
- ✅ 企业微信文档发布

## 反馈与贡献

如有问题或建议，欢迎反馈。
