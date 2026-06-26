# 🚀 快速安装指南

## 方式一：交互式安装（推荐）

运行安装向导，自动引导配置：

```bash
python3 ~/.openclaw/skills/market-open-analysis/install_cron.py install
```

**向导将帮助您完成：**

1. ✅ 配置 CommodityPriceAPI Key
   - 访问 https://commoditypriceapi.com 获取
   - 免费套餐：每月 100 次调用

2. ✅ 配置东方财富妙想 API Key
   - 联系官方申请
   - 或暂时跳过，后续配置

3. ✅ 配置推送用户 ID
   - 飞书：`ou_xxxxxxxxxxxx`
   - Telegram: `username`
   - Discord: `user_id`

4. ✅ 配置推送渠道
   - 支持：feishu, telegram, discord, slack, whatsapp
   - 留空使用默认渠道

5. ✅ 安装定时任务
   - 交易日 5:00 收集数据
   - 交易日 5:30 推送报告

---

## 方式二：手动配置

### 1. 配置 API Key

**商品价格 API：**
```bash
vim ~/.openclaw/skills/market-open-analysis/commodity_price.py
```
```python
API_KEY = "YOUR_KEY_HERE"  # ← 改为你的 Key
```

**新闻资讯 API：**
```bash
vim ~/.openclaw/skills/market-open-analysis/config.py
```
```python
MX_API_KEY = "YOUR_KEY_HERE"  # ← 改为你的 Key
```

### 2. 配置推送

```bash
vim ~/.openclaw/skills/market-open-analysis/config.py
```
```python
# 推送用户 ID
DEFAULT_TARGET = "ou_xxxxxxxxxxxx"  # 飞书示例

# 推送渠道（可选）
DEFAULT_CHANNEL = "feishu"  # 或 telegram/discord/slack
```

### 3. 安装定时任务

```bash
python3 ~/.openclaw/skills/market-open-analysis/install_cron.py install
```

---

## 验证安装

```bash
# 查看定时任务
crontab -l

# 手动测试
python3 ~/.openclaw/skills/market-open-analysis/main.py --stage analyze

# 查看日志
tail ~/openclaw/workspace/logs/market_open.log
```

---

## 其他命令

```bash
# 仅配置 API（不安装定时任务）
python3 ~/.openclaw/skills/market-open-analysis/install_cron.py config

# 查看状态
python3 ~/.openclaw/skills/market-open-analysis/install_cron.py status

# 卸载定时任务
python3 ~/.openclaw/skills/market-open-analysis/install_cron.py uninstall
```

---

## 📞 需要帮助？

查看详细文档：
- `SKILL.md` - 完整技能文档
- `API_KEY.example.md` - API Key 获取指南
- `INSTALL.md` - 详细安装步骤
