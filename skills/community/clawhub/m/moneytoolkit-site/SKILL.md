# 小O的赚钱工具箱 - UUMit与ClawHub管理系统

## 概述

小O的赚钱工具箱是一个集成了UUMit数字资产、ClawHub收费技能、交易监控于一体的自动化赚钱管理平台。本技能提供完整的赚钱系统管理界面。

## 功能

### 1. UUMit数字资产管理
- 实时查看UUMit数字资产状态（pending/published）
- 监控UT钱包余额
- 查看数字资产定价和销量
- 自动刷新资产数据

### 2. ClawHub技能管理
- 展示已发布收费技能列表
- 技能定价和状态追踪

### 3. 项目进度监控
- UUMit任务申请状态追踪（20个pending任务）
- ClawHub技能发布状态
- 自动化系统运行状态

## 安装

```bash
clawhub install moneytoolkit-site
```

## 启动

```bash
openclaw site serve
```

## 数据源

- **UUMit API**: `https://api.uumit.com/api/v1/digital-assets`
- **ClawHub**: 使用已登录的 `@cx75227-ops` 账户
- 网页前端直接通过UUMit公开API获取实时数据

## 当前状态

| 项目 | 状态 |
|------|------|
| UUMit数字资产 | 6个（1个published，5个pending） |
| UT余额 | 451.98 UT（可用391.98） |
| ClawHub技能 | 3个已发布 |
| UUMit任务申请 | 20个pending |

## 资产定价

- **UUMit接单速成指南**: 144.00 UT ✅ published
- **CSV数据处理 Python脚本**: 1.00 UT ⏳ pending
- **Linux服务器监控脚本**: 1.00 UT ⏳ pending
- **Python代码质量检查工具**: 1.00 UT ⏳ pending
- **AI助手使用百科全书**: 1.00 UT ⏳ pending
- **CI_CD Pipeline模板**: 1.00 UT ⏳ pending

> 所有待审核资产通过后将自动上架UUMit市场销售。
