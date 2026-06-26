---
name: jd-lawsuit
description: >-
  Judicial Dispute（消费纠纷维权助手）。通过浏览器自动化采集电商平台订单数据、
  商品快照、物流记录，生成退款申请、12315投诉函、民事起诉状等维权文书。
  Use when user mentions "维权", "退款", "投诉", "消费纠纷", "订单纠纷",
  "12315", "消费者权益", "lawsuit", "dispute", or needs help with
  e-commerce order disputes and consumer rights protection.
---

# JD Lawsuit — Judicial Dispute 消费纠纷维权

通过浏览器采集电商订单证据，生成维权文书，引导投诉和诉讼流程。

## 前置条件

- 浏览器已登录目标电商平台（本 skill 不处理登录，由用户自行完成）
- 需要 browser-use MCP（CDP 连接）

## 核心流程

```
确认平台与登录 → 定位订单 → 采集证据 → 生成文书 → 投诉/起诉
```

### Step 1: 确认平台与登录状态

向用户确认纠纷发生的**电商平台**，导航到该平台用户中心检查登录状态。

各平台的入口 URL、订单页路径、选择器策略见 [references/platform-guide.md](references/platform-guide.md)。

### Step 2: 定位目标订单

向用户确认**订单号**或**商品关键词**，导航到订单列表页采集数据。

### Step 3: 证据固定

对关键页面截图、提取结构化数据，保存至 `~/Downloads/dispute-evidence/{订单号}/`，
自动生成证据清单索引。

详细采集流程、截图规范、文件命名见 [references/evidence-collection.md](references/evidence-collection.md)。

### Step 4: 生成维权文书

根据纠纷类型生成对应文书：

| 类型 | 典型情况 | 生成文书 |
|------|----------|----------|
| 退款/退货 | 商品质量问题、描述不符、未收到货 | 退款申请函 |
| 价格欺诈 | 先涨后降、虚假满减、保价不兑现 | 12315 投诉函 + 赔偿计算 |
| 虚假宣传 | 商品描述与实物严重不符 | 12315 投诉函 |
| 售后不作为 | 客服推诿、超时未处理 | 12315 投诉函 + 起诉状 |
| 食品安全 | 过期/变质/违禁添加 | 12315 投诉函 + 退一赔十计算 |

文书模板见 [references/legal-templates.md](references/legal-templates.md)。

### Step 5: 投诉提交（可选）

引导用户通过合适渠道提交投诉。

各渠道操作步骤见 [references/complaint-channels.md](references/complaint-channels.md)。

## 详细参考

| 主题 | 文档 |
|------|------|
| 电商平台适配指南 | [references/platform-guide.md](references/platform-guide.md) |
| 证据采集与截图规范 | [references/evidence-collection.md](references/evidence-collection.md) |
| 维权文书模板 | [references/legal-templates.md](references/legal-templates.md) |
| 法律依据速查 | [references/legal-basis.md](references/legal-basis.md) |
| 投诉渠道操作指南 | [references/complaint-channels.md](references/complaint-channels.md) |

## 注意事项

- 不自动输入账号密码，登录始终由用户手动完成
- 截图前等待页面完全加载（`browser_wait` 2-3 秒 + snapshot 确认）
- 生成的文书为参考模板，提示用户根据实际情况修改后使用
- 若金额较大或情况复杂，建议用户咨询专业律师
