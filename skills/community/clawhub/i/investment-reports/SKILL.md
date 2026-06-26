---
name: investage
description: 價值投資每日追蹤系統 - 整合估值、技術分析、情緒分析，輸出綜合評分報告並發送 Email。適用於個人投資組合追蹤。
---

# Investage - 價值投資每日追蹤系統

> ⚠️ **注意**：此為公開模板版本。個人持股資料請見 `config.example.yaml`

## 功能

- **持股追蹤** - 追蹤你的投資組合每日變化
- **技術分析** - MA(30/100/200)、RSI、成交量、K線型態、乖離率
- **估值分析** - Yahoo Finance 分析師目標價
- **情緒分析** - Reddit 社區討論情緒
- **綜合評分** - 加權評分系統 (BUY/HOLD/WATCH/SELL)
- **每日報告** - HTML Email 自動發送

## 資料庫設定

```bash
# 建立 PostgreSQL 資料庫
createdb investage

# 連線
psql -d investage -U your_user
```

## 安裝

```bash
# 複製到你的 skills 目錄
cp -r investage ~/.openclaw/workspace/skills/

# 設定資料庫連線
export PGHOST=localhost
export PGDATABASE=investage
export PGUSER=your_user
```

## 資料表結構

```sql
-- 股票主檔
CREATE TABLE stocks (
    ticker VARCHAR(10) PRIMARY KEY,
    company_name VARCHAR(100),
    sector VARCHAR(50),
    currency VARCHAR(10) DEFAULT 'USD'
);

-- 持股記錄
CREATE TABLE holdings (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) REFERENCES stocks(ticker),
    shares DECIMAL(15,4),
    avg_cost DECIMAL(10,4),
    purchase_date DATE DEFAULT CURRENT_DATE
);

-- 觀察清單
CREATE TABLE watchlist (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) UNIQUE NOT NULL,
    added_date DATE DEFAULT CURRENT_DATE,
    reason TEXT,
    status VARCHAR(20) DEFAULT 'WATCHING'
);
```

## 使用方式

```bash
# 發送每日報告
python3 scripts/email_reporter.py

# 技術分析測試
python3 scripts/technical_analyzer.py NVDA

# 估值分析測試  
python3 scripts/valuation_analyzer.py NVDA
```

## 評分權重

| 維度 | 權重 |
|------|------|
| 估值 | 30% |
| 趨勢 | 25% |
| 宏觀/情緒 | 20% |
| 技術信號 | 15% |
| 風險 | 10% |

## 評分等級

| 分數 | 建議 |
|------|------|
| ≥65 | 🟢 BUY (買入) |
| 50-64 | 🔵 HOLD (持有) |
| 40-49 | 🟡 WATCH (觀望) |
| <40 | 🔴 SELL (賣出) |

## Email 設定

使用 gog 發送：

```bash
# 確認 gog 已設定
gog auth list

# 發送報告
gog gmail send --to your@email.com --subject "Daily Report" --body-html report.html
```

## Cron Job 設定

```bash
# 每日早上 07:30 發送報告 (台灣時間)
30 7 * * 1-5 python3 /path/to/scripts/email_reporter.py
```

## 自訂欄位

在 `config.yaml` 設定你的：
- Email 收件者列表
- 追蹤標的
- 持股資料

## 技術棧

- Python 3
- yfinance (股價數據)
- psycopg2 (PostgreSQL)
- gog (Email 發送)

## 授權

MIT License

---

*此為開源模板，個人持股資料請自行設定於 config.yaml*
