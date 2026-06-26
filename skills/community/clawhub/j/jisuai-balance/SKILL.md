---
name:极速AI余额查询
description: 查询极速AI账户余额和剩余次数。当用户说"查询极速AI余额"、"查询极速AI余额次数"、"极速AI还剩多少次"、"极速AI余额"时触发此技能。调用API获取用户的total(余额)和num(剩余次数)信息。
---

# 极速AI余额查询

## 触发词
- "查询极速AI余额"
- "查询极速AI余额次数"
- "极速AI还剩多少次"
- "极速AI余额"

## 自动读取配置

技能会自动从 `~/.openclaw/openclaw.json` 读取极速AI的 API Key：
- 查找 `models.providers` 中 baseUrl 为 `https://v2.aicodee.com` 的配置
- 读取对应的 apiKey

**客户无需额外配置**（如果已配置过极速AI的 API Key）

## API 调用

- 余额查询地址：`http://v2api.aicodee.com/chaxun/balance?key={api_key}`
- API Key 从 OpenClaw 配置中自动读取

返回 JSON 格式：
```json
{
  "success": true,
  "total": 100.00,
  "num": 1000
}
```

- `total`: 账户余额（美元）
- `num`: 剩余次数

## 执行方式

运行 `scripts/check_balance.py`

## 返回格式

根据用户询问的内容返回：

- 问余额 → `您的账户余额为：${total}`
- 问次数 → `您剩余次数：{num}次`
- 都问 → `您的账户余额为：${total}，剩余次数：{num}次`

## 错误处理

- `success: false` → 显示 `message` 错误信息
- API 调用失败 → `查询余额失败，请稍后重试`
- 未配置 → `未配置极速AI API Key，请在 OpenClaw 配置中添加`