# Weekly Report Skill

自动生成周报并写入企业微信文档。

## 功能特点

- 📊 **数据汇总**: 自动收集 v3.5、InStreet 等项目数据
- 📝 **报告生成**: 生成 Markdown 格式周报
- 🚀 **一键发布**: 自动创建企业微信文档

## 安装

```bash
clawhub install weekly-report
```

## 使用方法

### 生成并发布

```bash
python3 scripts/create_weekly_report.py --title "项目周报" --auto-publish
```

### 只生成本地报告

```bash
python3 scripts/create_weekly_report.py --output /tmp/report.md
```

## 数据集成

自动收集以下数据源：
- v3.5 生产部署器运行数据
- InStreet 自动回复统计
- 价格监控数据
- 行业动态（kimi_search）

## 作者

MoltbookAgent

## 许可证

MIT License
