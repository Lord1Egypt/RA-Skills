---
name: pans-crm-sync
description: |
  AI算力销售 CRM 同步工具。对接 Salesforce 和 HubSpot 双平台，
  自动同步客户状态、更新 Pipeline、生成 CRM 报表，支持双向/增量同步
  和冲突检测与解决。
  触发词：CRM同步, 客户同步, Salesforce, HubSpot, pipeline同步,
  客户状态更新, CRM报表, crm sync
---

# pans-crm-sync

AI算力销售CRM同步工具。对接Salesforce/HubSpot，自动同步客户状态、更新Pipeline、生成CRM报表。

## 功能

- 支持 Salesforce 和 HubSpot 双平台
- 客户数据同步（双向/增量）
- Pipeline 状态更新
- CRM 报表生成
- 冲突检测与解决

## 安装

```bash
# 安装依赖
pip install simple-salesforce hubspot-api-client

# 配置环境变量
export SALESFORCE_USERNAME="your_username"
export SALESFORCE_PASSWORD="your_password"
export SALESFORCE_SECURITY_TOKEN="your_token"
export HUBSPOT_API_KEY="your_api_key"
```

## 使用

```bash
# 同步客户数据
python scripts/crm.py --sync --platform salesforce

# 更新Pipeline状态
python scripts/crm.py --update --platform hubspot --status "Closed Won"

# 查询客户信息
python scripts/crm.py --query --platform salesforce --email "customer@example.com"
```

## CLI 参数

| 参数 | 说明 |
|------|------|
| `--sync` | 执行同步操作 |
| `--update` | 更新记录 |
| `--query` | 查询记录 |
| `--platform` | 平台选择: `salesforce` 或 `hubspot` |
| `--status` | 状态值（用于 --update） |
| `--email` | 邮箱（用于 --query） |
| `--limit` | 查询结果限制 |

## 触发词

CRM同步, 客户同步, Salesforce, HubSpot, pipeline同步, 客户状态更新, CRM报表, crm sync
