# 🔑 API Key 配置指南

使用前请配置以下 API Key 和推送设置！

---

## 1️⃣ CommodityPriceAPI（价格数据）

### 获取方式

1. 访问官网：https://commoditypriceapi.com
2. 注册账号
3. 获取 API Key
4. 选择订阅计划（有免费套餐）

### 配置方法

编辑文件：
```bash
vim ~/.openclaw/skills/market-open-analysis/commodity_price.py
```

修改：
```python
API_KEY = "YOUR_COMMODITY_PRICE_API_KEY_HERE"  # ← 改为你的 Key
```

### 测试

```bash
curl -H "X-API-Key: YOUR_KEY" \
  "https://api.commoditypriceapi.com/v2/rates/latest?base=USD&symbols=XAU,WTIOIL-FUT"
```

---

## 2️⃣ 东方财富妙想 API（新闻资讯）

### 获取方式

联系东方财富妙想官方申请 API 访问权限。

### 配置方法

编辑文件：
```bash
vim ~/.openclaw/skills/market-open-analysis/config.py
```

修改：
```python
MX_API_KEY = "YOUR_MX_API_KEY_HERE"  # ← 改为你的 Key
```

---

## 3️⃣ 推送配置

### 配置推送用户

编辑文件：
```bash
vim ~/.openclaw/skills/market-open-analysis/config.py
```

```python
# 推送用户 ID（必填）
# 飞书格式：ou_xxxxxxxxxxxx
# Telegram: username 或 user_id
# Discord: user_id 或 channel_id
DEFAULT_TARGET = "your_user_id"
```

### 配置推送渠道（可选）

```python
# 推送渠道（可选，留空使用 OpenClaw 默认渠道）
# 支持：feishu, telegram, discord, slack, whatsapp 等
DEFAULT_CHANNEL = ""  # 留空使用默认
```

**支持的平台：**
- `feishu` - 飞书
- `telegram` - Telegram
- `discord` - Discord
- `slack` - Slack
- `whatsapp` - WhatsApp
- 留空 - 使用 OpenClaw 默认渠道

---

## ✅ 验证配置

配置完成后，测试运行：

```bash
# 测试价格查询
python3 ~/.openclaw/skills/market-open-analysis/main.py --stage collect

# 测试完整流程
python3 ~/.openclaw/skills/market-open-analysis/main.py --stage analyze
```

如果看到价格数据和推送成功，说明配置正确！

---

## ⚠️ 注意事项

- API Key 请妥善保管，不要上传到公开仓库
- 不同 API 的调用频率限制不同，请注意查看官方文档
- 免费套餐通常有调用次数限制
