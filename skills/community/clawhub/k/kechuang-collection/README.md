# 🔬 kechuang-collection

**科创线索采集 Skill for Claude Code**

7×24自动监控全网科创公开信息，基于公司KPI智能筛选有效线索，替代人工筛取的低效工作。

## 安装

```bash
# 通过 npm 安装
npm install -g kechuang-collection
```

然后在 Claude Code 中使用 `/kechuang-collection` 命令。

## 使用方式

| 命令 | 功能 |
|------|------|
| `/kechuang-collection scan <关键词>` | 实时扫描科创线索 |
| `/kechuang-collection monitor` | 启动定时监控 |
| `/kechuang-collection report` | 生成汇总报告 |
| `/kechuang-collection list-sources` | 查看监控渠道 |
| `/kechuang-collection add-source <url>` | 添加监控源 |

## 采集范围

- 科技厅、工信厅、发改委、高新区等政府平台
- 科技项目申报、奖项评选、补贴公告、科研课题立项
- 行业科创动态、重点企业合作、技术攻关项目

## License

MIT