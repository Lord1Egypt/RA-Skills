---
name: invoice-reimbursement
description: AI发票报销助手。上传发票图片自动识别关键信息，智能分类费用类型，查重预警防重复报销，生成可视化HTML报销报告。支持录入/查询/删除/导出全流程。触发词：发票报销、发票识别、整理报销、报销单、发票录入、invoice reimbursement、帮我看看发票、录入发票、报销报告、查发票。
agent_created: true
location: user
allowed-tools: Read, Write, Bash, WebFetch, WebSearch
metadata:
  openclaw:
    requires:
      bins: [python]
---

# 发票报销助手 (Invoice Reimbursement)

AI智能发票报销管理系统 — 拍照识别发票 → 自动分类整理 → 一键生成报销报告。

## 功能概览

| 功能 | 说明 |
|------|------|
| 📷 发票识别 | 上传发票图片/PDF，AI自动提取关键信息 |
| 🏷️ 智能分类 | 自动按费用类型分类（餐饮/交通/住宿/办公/通讯/其他） |
| 🔍 查重预警 | 同一发票号重复录入自动告警 |
| 📊 报销报告 | 生成交互式HTML可视化报销报告 |
| 📋 报销单 | 勾选发票一键生成标准报销单 |
| 📤 数据导出 | 支持CSV/Excel格式导出 |

## 工作流程

```
发票图片 → AI识别提取 → 信息确认 → 入库(查重) → 分类整理 → 生成报告/报销单
```

## 使用方法

### 方式一：直接对话（推荐）

直接发送发票图片或描述，AI会引导完成整个流程：

```
"帮我识别这张发票" + 上传发票图片
```
```
"录入发票：2026年6月15日，餐饮费，金额368元，发票号12345678"
```
```
"生成本月报销报告"
```
```
"生成报销单，选第3、5、7张发票"
```

### 方式二：命令行操作

```bash
# 运行核心脚本
python scripts/invoice_manager.py --help

# 手动添加发票
python scripts/invoice_manager.py add --number 12345678 --date 2026-06-15 \
  --type "增值税普通发票" --category "餐饮" --amount 368 --seller "某某餐厅"

# 查看所有发票
python scripts/invoice_manager.py list

# 检查重复
python scripts/invoice_manager.py check --number 12345678

# 删除发票
python scripts/invoice_manager.py delete --id 3

# 导出CSV
python scripts/invoice_manager.py export --format csv --output invoices.csv

# 生成报销报告
python scripts/report_generator.py --month 2026-06 --output report.html
```

## 数据库结构

本地SQLite存储（`{baseDir}/data/invoices.db`）：

| 字段 | 类型 | 说明 |
|------|------|------|
| invoice_code | TEXT | 发票代码 |
| invoice_number | TEXT | 发票号码（唯一） |
| invoice_date | TEXT | 开票日期 |
| invoice_type | TEXT | 发票类型 |
| category | TEXT | 费用类别 |
| amount | REAL | 金额（不含税） |
| tax_amount | REAL | 税额 |
| total_amount | REAL | 价税合计 |
| seller_name | TEXT | 销售方名称 |
| buyer_name | TEXT | 购买方名称 |
| items | TEXT | 货物/服务明细(JSON) |
| image_path | TEXT | 发票图片路径 |
| notes | TEXT | 备注 |
| status | TEXT | 状态(pending/approved/rejected/reimbursed) |

## 发票类型

支持识别的发票类型：
- 增值税专用发票
- 增值税普通发票
- 增值税电子普通发票
- 增值税电子专用发票
- 通用机打发票
- 出租车发票
- 火车票/机票行程单
- 定额发票
- 其他票据

## 费用类别

自动分类规则：
- **餐饮**：餐饮、食品、外卖、聚餐
- **交通**：打车、火车票、机票、加油、停车、公交
- **住宿**：酒店、宾馆、旅馆、民宿
- **办公**：文具、打印、耗材、快递、办公设备
- **通讯**：话费、网费、邮寄
- **差旅**：机票+酒店组合
- **其他**：无法自动识别的费用

## AI识别策略

1. **优先使用多模态视觉识别**：直接读取发票图片，LLM视觉能力提取关键字段
2. **结构化输出**：提取发票代码、号码、日期、金额、税额、销售方、购买方、明细
3. **智能纠错**：自动修正常见OCR误差（O↔0，l↔1等）
4. **分类推断**：基于销售方名称和明细自动推断费用类别

## 查重规则

- 以 `发票代码 + 发票号码` 为唯一标识
- 同一发票号再次录入时自动拦截并提示
- 支持手动确认强制录入

## 依赖

Python 3.x，无需额外pip安装（使用标准库sqlite3, json, csv, datetime, html）。

报告生成使用纯HTML/CSS/JS，无需外部服务。

## 安全与隐私

- 所有数据存储在本地SQLite，不上传任何云端
- 发票图片仅记录本地路径，不复制文件
- AI识别过程在本地会话中完成
