# IMRC 运营报告生成工具

装备所月度/年度运营情况汇总工具，从 IMRC 系统提取数据，结合美信消息，生成结构化运营报告。

## 快速开始

### 1. 提取 IMRC 数据

```bash
python scripts/extractor.py --month 2026-07
```

### 2. 收集美信消息

```bash
python scripts/meixin_collector.py --days 30
```

### 3. 生成报告

```bash
python scripts/report_generator.py --month 2026-07 --output report.md
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `config/pages.json` | IMRC 10个页面配置 |
| `config/report_template.md` | 报告模板 |
| `scripts/extractor.py` | IMRC 页面数据提取 |
| `scripts/meixin_collector.py` | 美信消息收集 |
| `scripts/report_generator.py` | 报告生成 |
| `templates/` | 各分项报告模板 |

## 报告结构

- **第一页**：整体介绍（10分钟汇报用）
- **分项报告**：项目运营/预算/合同/投资/风险等

## 测试

```bash
python scripts/test_imrc_report.py
```
