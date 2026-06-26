# Investment Daily Report — 每日投研日报生成器

## 简介

一键生成覆盖 A 股、港股、美股的专业级每日投研日报。基于 NeoData 金融数据 API 实时采集行情、资金流向、板块轮动等数据，输出结构化 Markdown 日报。

## 快速开始

```bash
# 生成今日完整日报
node scripts/generate_report.cjs

# 快速模式
node scripts/generate_report.cjs --quick

# 仅 A 股
node scripts/generate_report.cjs --market cn
```

## 系统要求

- Node.js >= 18
- 网络连接
- 零外部依赖

## 输出示例

生成文件默认命名：`investment-report-YYYY-MM-DD.md`

## 版本

- v1.0.0 — 初始版本

## 许可

MIT
