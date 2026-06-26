# Passive-Income-Tracker Skill

被动收入追踪仪表板 - 多平台收入整合与财务预测分析工具。

## 功能

- **多平台整合**: 自动同步各大被动收入平台数据
- **收入分类**: 自动 categorize 不同收入来源
- **趋势分析**: 可视化收入增长趋势
- **财务预测**: AI 预测未来收入
- **税务准备**: 自动生成税务报告
- **目标追踪**: 设定和追踪财务目标

## 触发词

当用户提到以下关键词时使用此技能：
- "被动收入"
- "passive income"
- "收入追踪"
- "财务仪表板"
- "收入分析"
- "理财追踪"
- "multiple income streams"
- "收入报告"
- "财务预测"

## 使用方法

### 查看收入概览

```bash
clawhub run passive-income-tracker overview --period month
```

### 同步平台数据

```bash
clawhub run passive-income-tracker sync --platforms all
```

### 生成报告

```bash
clawhub run passive-income-tracker report --format pdf --period quarter
```

### 财务预测

```bash
clawhub run passive-income-tracker forecast --months 12
```

## 配置

在 `TOOLS.md` 中添加以下配置：

```markdown
### Passive Income Tracker

支持的平台和 API Keys:
- Gumroad: (API Key)
- Patreon: (API Key)
- YouTube: (API Key)
- Amazon Associates: (API Key)
- Teachable: (API Key)
- Stripe: (API Key)
- PayPal: (API Key)
- 其他：(手动导入 CSV)

财务目标:
- 月度目标：$XXXX
- 年度目标：$XXXXX
```

## 输出格式

生成结构化的收入报告，包含：
- 总收入和分类收入
- 环比/同比增长
- 各平台贡献比例
- 预测收入
- 税务估算

## 注意事项

- 敏感财务数据本地加密存储
- 支持手动导入数据
- 定期备份数据
