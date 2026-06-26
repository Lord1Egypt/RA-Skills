# 📦 每日开盘分析 Skill - 安装指南

## ✅ 已完成安装

Skill 已创建在：`~/.openclaw/skills/market-open-analysis/`

**包含内容：**
- ✅ `main.py` - 主程序
- ✅ `commodity_price.py` - 价格查询 API 客户端
- ✅ `config.py` - 配置文件
- ✅ `install_cron.py` - 定时任务安装脚本
- ✅ `requirements.txt` - Python 依赖
- ✅ 完整文档（SKILL.md, README.md, INSTALL.md）

---

## 🚀 使用步骤

### 1️⃣ 安装 Python 依赖

```bash
pip3 install -r ~/.openclaw/skills/market-open-analysis/requirements.txt
```

### 2️⃣ 配置 API Key（必填！）

#### 配置商品价格 API

1. 访问 https://commoditypriceapi.com 获取 API Key
2. 编辑文件：
```bash
vim ~/.openclaw/skills/market-open-analysis/commodity_price.py
```
3. 修改：
```python
API_KEY = "YOUR_COMMODITY_PRICE_API_KEY_HERE"  # ← 改为你的 Key
```

#### 配置新闻资讯 API

1. 联系东方财富妙想官方获取 API Key
2. 编辑文件：
```bash
vim ~/.openclaw/skills/market-open-analysis/config.py
```
3. 修改：
```python
MX_API_KEY = "YOUR_MX_API_KEY_HERE"  # ← 改为你的 Key
```

### 3️⃣ 配置推送用户（可选）

编辑 `config.py`：
```bash
vim ~/.openclaw/skills/market-open-analysis/config.py
```

修改：
```python
DEFAULT_TARGET = "ou_xxxxxxxxxxxx"  # 您的飞书 open_id
```

### 4️⃣ 安装定时任务

```bash
python3 ~/.openclaw/skills/market-open-analysis/install_cron.py install
```

输入 `y` 确认安装。

### 4️⃣ 验证安装

```bash
# 查看定时任务
crontab -l

# 手动测试收集
python3 ~/.openclaw/skills/market-open-analysis/main.py --stage collect

# 手动测试推送
python3 ~/.openclaw/skills/market-open-analysis/main.py --stage analyze
```

---

## 📋 定时任务说明

| 时间 | 任务 | 说明 |
|------|------|------|
| **5:00** | `--stage collect` | 获取实时价格并保存 |
| **5:30** | `--stage analyze` | 读取 5 点数据 + 信息面分析 → 推送 |

**执行日期：** 周一至周五（交易日）

---

## 🔧 管理命令

```bash
# 查看定时任务状态
python3 ~/.openclaw/skills/market-open-analysis/install_cron.py status

# 卸载定时任务
python3 ~/.openclaw/skills/market-open-analysis/install_cron.py uninstall

# 手动收集数据
python3 ~/.openclaw/skills/market-open-analysis/main.py --stage collect

# 手动分析推送
python3 ~/.openclaw/skills/market-open-analysis/main.py --stage analyze

# 指定日期测试
python3 ~/.openclaw/skills/market-open-analysis/main.py --stage analyze --date 2026-03-17

# 指定推送用户
python3 ~/.openclaw/skills/market-open-analysis/main.py --stage analyze --target ou_xxxxxxxxxxxx
```

---

## 📁 文件位置

| 类型 | 路径 |
|------|------|
| **Skill 目录** | `~/.openclaw/skills/market-open-analysis/` |
| **价格数据** | `~/openclaw/workspace/data/market_price_*.json` |
| **分析报告** | `~/openclaw/workspace/reports/market_open_*.md` |
| **执行日志** | `~/openclaw/workspace/logs/market_open.log` |

---

## 📊 推送格式

```
# 🌅 交易日早间行情播报
_生成时间：2026-03-17 05:30:00_

---

| 品种 | 收盘价 | 开盘预测 | 置信度 |
|------|--------|----------|--------|
| ⛽ 美油 | `94.92` | 🔴 高开 | 🟡 中 |
| 🥇 黄金 | `5002.59` | ⚪ 平开 | ⚪ 低 |

---

## 💡 预测原因

**⛽ 美油**：高开
  - 利好消息占优 (+3 条)
  - 信号强烈，置信度高
  - 隔夜消息：25 条（利好 3/利空 0）

**🥇 黄金**：平开
  - 消息面中性
  - 隔夜消息：16 条（利好 0/利空 0）

---
> ⚠️ _市场有风险，投资需谨慎_
```

---

## ❓ 常见问题

### Q: 如何修改推送时间？
编辑 crontab：
```bash
crontab -e
# 修改时间（例如改为 6:00 和 6:30）
0 6 * * 1-5 ...
30 6 * * 1-5 ...
```

### Q: 如何临时禁用推送？
```bash
# 注释掉 crontab 中的任务
crontab -e
# 在行首添加 #
# 30 5 * * 1-5 ...
```

### Q: 如何查看历史报告？
```bash
ls -la ~/openclaw/workspace/reports/
cat ~/openclaw/workspace/reports/market_open_20260317_*.md
```

### Q: 推送失败怎么办？
1. 检查 OpenClaw 是否正常运行
2. 检查飞书授权是否有效
3. 查看日志：`tail ~/openclaw/workspace/logs/market_open.log`

---

## 📞 技术支持

- Skill 文档：`~/.openclaw/skills/market-open-analysis/SKILL.md`
- 日志文件：`~/openclaw/workspace/logs/market_open.log`

---

**安装完成！从下一个交易日开始，您将在 5:30 收到开盘分析推送。** 🎉
