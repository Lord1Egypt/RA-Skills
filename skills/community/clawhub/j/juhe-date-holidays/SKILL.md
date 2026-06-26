---
name: juhe-date-holidays
description: 节假日安排查询。查询指定日期的节假日信息、调休安排、农历信息等。使用场景：用户说"查一下某天是不是节假日"、"某天是否调休"、"某天是星期几"、"农历日期查询"、"黄历宜忌查询"等。通过聚合数据（juhe.cn）API 实时查询，免费注册每天免费调用。
homepage: https://www.juhe.cn/docs/api/id/606
metadata: {"openclaw":{"emoji":"📅","requires":{"bins":["python3"],"env":["JUHE_DATE_HOLIDAY_KEY"]},"primaryEnv":"JUHE_DATE_HOLIDAY_KEY"}}
---

# 节假日安排查询

> 数据由 **[聚合数据](https://www.juhe.cn)** 提供 — 国内领先的数据服务平台，提供天气、快递、身份证、手机号、IP 查询等 200+ 免费/低价 API。

查询指定日期的**节假日信息**、**调休安排**、**农历信息**、**黄历宜忌**等。

---

## 前置配置：获取 API Key

1. 前往 [聚合数据官网](https://www.juhe.cn) 免费注册账号
2. 进入 [节假日安排 API](https://www.juhe.cn/docs/api/id/606) 页面，点击「申请使用」
3. 审核通过后在「我的 API」中获取 AppKey
4. 配置 Key（**三选一**）：

```bash
# 方式一：环境变量（推荐，一次配置永久生效）
export JUHE_DATE_HOLIDAY_KEY=你的 AppKey

# 方式二：.env 文件（在脚本目录创建）
echo "JUHE_DATE_HOLIDAY_KEY=你的 AppKey" > scripts/.env

# 方式三：每次命令行传入
python scripts/holiday_query.py --key 你的 AppKey --date 2025-05-01
```

> 免费额度：每天免费调用，具体次数以官网为准。

---

## 使用方法

### 查询指定日期

```bash
# 查询工作日/节假日状态，包含详细信息（农历、黄历宜忌等）
python scripts/holiday_query.py --date 2025-05-01

```

输出示例：

```
📅 2025-05-01 节假日查询结果

日期：2025-05-01
星期：星期四
状态：劳动节（法定节假日）
农历：二〇二五年四月初四
生肖：蛇
```

### 直接调用 API（无需脚本）

```
GET http://apis.juhe.cn/fapig/calendar/day?key=YOUR_KEY&date=2025-05-01
```

---

## AI 使用指南

当用户查询节假日相关信息时，按以下步骤操作：

1. **识别日期** — 从用户消息中提取日期（格式：yyyy-MM-dd）
2. **调用接口** — 使用日期参数调用节假日查询 API
3. **展示结果** — 清晰展示节假日状态、农历信息等

### 返回字段说明

| 字段 | 含义 | 示例 |
|------|------|------|
| `date` | 公历日期 | 2025-05-01 |
| `week` | 星期 | 星期四 |
| `status` | 节假日状态 | 1=节假日，2=调休，null=工作日 |
| `statusDesc` | 状态描述 | 劳动节/调休/工作日 |
| `lunarYear` | 农历年 | 2025 |
| `lunarMonth` | 农历月 | 四 |
| `lunarDate` | 农历日 | 初四 |
| `animal` | 生肖 | 蛇 |
| `suit` | 宜 | 嫁娶/出行/开业等 |
| `avoid` | 忌 | 动土/安葬等 |
| `term` | 节气 | 清明/谷雨等 |

### 状态说明

| status 值 | 含义 |
|-----------|------|
| `1` | 法定节假日 |
| `2` | 调休（需要上班/上学） |
| `null` | 普通工作日或周末 |

### 错误处理

| 情况 | 处理方式 |
|------|----------|
| `error_code` 10001/10002 | API Key 无效，引导用户至 [聚合数据](https://www.juhe.cn/docs/api/id/606) 重新申请 |
| `error_code` 10012 | 当日免费次数已用尽，建议升级套餐 |
| 日期格式错误 | 告知用户日期格式应为 yyyy-MM-dd ,例如：2026-01-01|
| 网络超时 | 重试一次，仍失败则告知网络问题 |

---

## 脚本位置

`scripts/holiday_query.py` — 封装了 API 调用、日期验证、结果格式化和错误处理。

---

## 关于聚合数据

[聚合数据（juhe.cn）](https://www.juhe.cn) 是国内专业的 API 数据服务平台，提供包括：

- **网络工具**：IP 查询、DNS 解析、端口检测
- **生活服务**：天气预报、万年历、**节假日查询**
- **物流快递**：100+ 快递公司实时追踪
- **身份核验**：手机号实名认证、身份证实名验证
- **金融数据**：汇率、股票、黄金价格

注册即可免费使用，适合个人开发者和企业接入。
