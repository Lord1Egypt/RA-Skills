---
name: logistics-care
description: >-
  电商物流延迟检测与客户安抚短信发送技能。导入订单CSV或手动输入运单号，
  自动查询物流轨迹、检测延迟风险（发货超时/运输停滞/派送异常/预计超时），
  AI生成安抚话术，通过阿里云/腾讯云短信发送给客户。支持dry-run预览模式。
  Triggers: 物流延迟, 快递延迟, 发货超时, 物流异常, 安抚短信, 催发货,
  物流检测, 订单物流查询, 批量查快递, 物流提醒, logistics delay,
  shipping delay, delivery notification, 电商物流, 发货提醒.
version: "1.0.0"
agent_created: true
metadata:
  openclaw:
    requires:
      bins:
        - python.exe
        - requests
    emoji: "📦"
    homepage: https://github.com/bettermen/logistics-care
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
  - WebSearch
---

# 电商物流延迟检测 + 安抚短信技能

## 概述

为电商卖家提供「物流监控→延迟检测→安抚话术→短信发送」一站式服务。
检测到异常后，自动生成专业安抚短信并发送给客户，降低差评率和客诉。

## 核心能力

1. **物流轨迹查询** — 支持60+快递公司，自动识别快递公司
2. **延迟风险检测** — 4条规则引擎：发货超时、运输停滞、派送异常、预计超时
3. **AI安抚话术** — 根据延迟原因个性化生成短信内容
4. **短信发送** — 阿里云/腾讯云短信，支持dry-run预览

## 工作模式

| 模式 | 说明 |
|------|------|
| `dry-run` | 仅检测物流状态，预览安抚短信，不真实发送（默认） |
| `send` | 检测 → 预览 → 确认 → 批量发送短信 |

## 快速开始

### 模式 1：CSV批量导入

准备CSV文件（UTF-8编码），包含以下列：

```csv
order_id,customer_name,customer_phone,tracking_number,carrier_code,order_date,product_name
20260615001,张三,13800138000,SF1234567890,SF,2026-06-10,新款T恤
20260615002,李四,13900139000,YT9876543210,,2026-06-11,运动鞋
20260615003,王五,13700137000,JD000111222333,,2026-06-08,手机壳
```

必填列：`order_id`, `customer_phone`, `tracking_number`
可选列：`customer_name`, `carrier_code`（不填则自动识别）, `order_date`, `product_name`

### 模式 2：手动单号查询

直接提供运单号，逐一手动输入客户信息。

## 使用流程

### Step 1: 获取订单数据

```python
# WorkBuddy 将执行：
python scripts/order_processor.py --input orders.csv --validate
```

### Step 2: 查询物流状态并检测延迟

```python
python scripts/logistics_checker.py --input orders.csv --output results.json
```

### Step 3: 生成安抚短信预览

```python
python scripts/sms_sender.py --input results.json --mode dry-run --output preview.html
```

### Step 4: 确认并发送短信（可选）

```python
python scripts/sms_sender.py --input results.json --mode send --provider aliyun
```

## 延迟检测规则

| 规则 | 条件 | 严重程度 |
|------|------|----------|
| 发货超时 | 下单>48h，物流状态仍为「待揽件」 | 🔴 高 |
| 运输停滞 | 最近更新>24h，状态为「运输中」 | 🟡 中 |
| 派送异常 | 状态为「异常」「退回」「丢失」 | 🔴 高 |
| 预计超时 | 当前时间>预计送达时间，未签收 | 🟡 中 |

## API 配置

### 物流查询 — UAPI

- 接口地址：`https://uapis.cn/api/v1/misc/tracking/query`
- 认证方式：API Key（免费注册即送积分）
- 费用：40积分/次（访客积分有限，建议注册）

配置方式：在 `~/.workbuddy/skills/logistics-care/references/api_config.md` 中填写 API Key

### 短信发送 — 阿里云短信

- SDK：`dysmsapi20170525`
- 需要：AccessKey + 短信签名 + 模板CODE

### 短信发送 — 腾讯云短信（备用）

- SDK：`tencentcloud-sdk-python`
- 需要：SecretId + SecretKey + SDK AppID + 模板ID

## 安抚短信模板策略

根据延迟原因选择话术风格：

- **发货超时**：致歉 + 解释原因 + 新发货时间 + 补偿
- **运输停滞**：告知已催促快递 + 预计到达时间 + 致谢耐心
- **派送异常**：紧急通知 + 已联系快递处理 + 替代方案
- **预计超时**：温和提醒 + 更新预计时间 + 随时联系

每条短信控制在70字以内（1条短信），减少成本。

## 输出

1. **HTML报告** — 可视化展示所有订单物流状态、延迟摘要、短信发送结果
2. **JSON结果** — 结构化数据，可二次处理
3. **短信预览** — 每条短信内容 + 发送状态

## 技能维护

- 物流API如有变动，更新 `references/api_config.md`
- 延迟规则阈值可在 `scripts/logistics_checker.py` 的 `DELAY_RULES` 字典中调整
- 安抚话术模板在 `scripts/sms_sender.py` 的 `MESSAGE_TEMPLATES` 中维护
