---
name: operation-daily-report-claw
description: |
  运营数据日报虾 — 自动化多平台运营数据采集与日报生成。从抖音、小红书、视频号、B站、微博等平台采集数据，清洗标准化后生成结构化日报，并推送到飞书文档/群聊。

  **当以下情况时使用此 Skill**：
  (1) 需要汇总多个内容平台（抖音/小红书/视频号/B站/微博）的运营数据
  (2) 需要生成运营日报、周报、月报
  (3) 需要设置定时自动日报推送到飞书群
  (4) 需要检测异常数据（播放量暴跌、涨粉异常、互动率异常等）并预警
  (5) 用户提到"生成日报"、"运营数据"、"平台数据"、"数据汇总"、"自动日报"、"数据统计"、"播放量"、"涨粉数"、"互动数据"、"定时报表"
---

# 运营数据日报虾

自动化多平台运营数据采集 → 清洗分析 → 日报生成 → 飞书推送。

## 工作流程

### 步骤 1：确认配置
询问用户：
- 需要采集哪些平台（抖音/小红书/视频号/B站/微博）
- 账号 ID 和 API 密钥是否已配置（参考 `references/platform-api-guide.md`）
- 日报类型：日报 / 周报 / 月报
- 推送目标：飞书群 chat_id 或个人

### 步骤 2：数据采集
使用 `scripts/fetch-platform-data.sh` 采集数据：
```bash
# 采集单平台
./scripts/fetch-platform-data.sh fetch douyin <account_id>

# 采集所有平台（并行）
./scripts/fetch-platform-data.sh fetch all
```
数据输出为 JSON 格式，存储在 `data/raw/<platform>_<date>.json`。

### 步骤 3：生成日报
使用 `scripts/generate-report.py` 生成报告：
```bash
# 生成昨日日报
python3 scripts/generate-report.py --date yesterday

# 生成指定日期
python3 scripts/generate-report.py --date 2026-03-31

# 生成周报
python3 scripts/generate-report.py --type weekly --date 2026-03-31
```

### 步骤 4：推送到飞书
1. 用 `feishu_create_doc` 创建飞书云文档（Markdown 格式）
2. 用 `message` 工具将文档链接发送到目标群聊或个人
3. 若有异常数据，额外发送 @全体成员 的预警消息

### 步骤 5：配置定时任务（可选）
若用户需要每天自动执行，提供 cron 配置示例：
```
# 每天早上 8:00 自动生成日报
0 8 * * * cd /path/to/workspace && ./scripts/fetch-platform-data.sh fetch all && python3 scripts/generate-report.py --date yesterday
```

## 数据标准字段

所有平台数据统一标准化为：

| 字段 | 说明 |
|------|------|
| platform | 平台名称 |
| date | 数据日期 |
| views | 播放量/阅读量 |
| likes | 点赞数 |
| comments | 评论数 |
| shares | 转发/分享数 |
| favorites | 收藏数 |
| new_followers | 当日涨粉数 |
| total_followers | 粉丝总数 |
| engagement_rate | 互动率（(likes+comments+shares)/views） |
| completion_rate | 完播率（视频平台） |

## 异常检测

采集完成后自动检查异常，规则详见 `references/anomaly-rules.md`。
发现异常时在日报中标注 ⚠️，并单独发送预警消息。

## 日报模板

日报格式详见 `references/report-templates.md`，支持：
- 简洁版（仅核心指标）
- 详细版（含趋势图）
- 对比版（多平台横向对比）
- 异常版（仅展示异常数据）

## 平台 API 接入

各平台 API 鉴权和调用方式详见 `references/platform-api-guide.md`。

## 注意事项

- 小红书无官方 API，需 Cookie 鉴权，稳定性较低，建议每周检查 Cookie 是否过期
- API 调用有频率限制，建议每天采集 1-2 次
- 确保服务器时区与平台数据时区一致（Asia/Shanghai）
- 历史数据存储在本地 SQLite，长期使用需定期备份
