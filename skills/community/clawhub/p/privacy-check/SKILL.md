---
name: privacy-check
description: |
  隐私敏感信息扫描器 (Privacy Check) v1.0.1。
  检测15+种敏感个人信息：身份证号、手机号、邮箱、银行卡、信用卡、
  SSN、护照、驾驶证、微信号、支付宝号、API密钥等。
  支持 JSON/CSV/HTML 报告输出、白名单忽略、文件类型过滤。

  Use when: 需要在数据文件中发现敏感信息、
  数据发布前做隐私审查、合规检查准备、数据脱敏预处理。

  🎉 v1.0.1 安全增强更新：
  - 6 种新增PII模式（信用卡、SSN、港澳台护照、驾驶证、微信号、支付宝）
  - CSV / HTML 报告格式
  - 白名单忽略模式
  - 文件扩展名过滤
  - 🔒 上下文行自动脱敏，避免敏感数据聚合泄露
  - 🔒 上下文默认关闭（--context 开启），减少敏感数据聚合风险
  - 🔒 报告头部增加安全警告
  - ASCII 条形图摘要

  v1.0.0 核心功能：
  - 🔍 10+ 种敏感信息模式检测
  - 🎭 自动脱敏显示
  - 📊 JSON 报告输出
  - 🚀 纯本地运行，无外部依赖

  触发关键词：隐私检查、PII扫描、敏感信息检测、
  数据合规、脱敏、隐私审计、个人信息保护
  适用范围：任意文本文件（TXT/CSV/JSON/日志等）
  运行模式：纯本地，无网络请求 ❎
  外部依赖：Python标准库（无需额外安装）
---

# 🔍 Privacy Check v1.0.1

## Overview
扫描文件中的敏感个人信息。支持单个文件或整个目录递归扫描，输出结构化的 JSON/CSV/HTML 报告，并通过 ASCII 条形图展示类型分布。

## Usage
```bash
# 扫描单个文件
python3 scripts/scanner.py --file data.csv

# 扫描目录
python3 scripts/scanner.py --dir ./data/

# HTML 报告
python3 scripts/scanner.py --dir ./data/ --format html --output report.html

# 忽略注释行 + 只扫描 txt/csv
python3 scripts/scanner.py --dir ./data/ --ignore "^#" --ext .txt,.csv
```

## Supported Patterns (15+)

| 类型 | 示例(脱敏后) | 严重级别 |
|------|-------------|---------|
| 中国大陆身份证号 | 1101**********1234 | 高 |
| 中国大陆手机号 | 138****1234 | 高 |
| 电子邮件地址 | usa****@example.com | 中 |
| 银行卡号(Luhn) | 6222**********1234 | 高 |
| 信用卡号(Luhn) | 4111**********1111 | 高 |
| 美国社会安全号(SSN) | ***-**-1234 | 高 |
| 中国护照号 | E1****34 | 高 |
| 港澳护照号 | AB****78 | 高 |
| 台湾护照号 | 12****89 | 中 |
| 中国大陆驾驶证号 | 1101************99 | 高 |
| 微信号 | zh****en | 中 |
| 支付宝账号 | usa****@... | 中 |
| IP地址 | 192.***.*.* | 低 |
| 邮政编码 | 100*** | 低 |
| API密钥 | sk-...****abcd | 高 |

## Output Formats

**JSON (默认)** — 结构化数据供程序处理：
```json
{"scan_time": "...", "total_findings": 42, "by_type": {"china_id": 5, ...}}
```

**CSV** (`--format csv`) — 扁平表格，每行一条发现：
```csv
file,line,type,description,severity,match
data.csv,128,china_id,中国大陆身份证号,高,1101**********1234
```

**HTML** (`--format html`) — 带样式、摘要卡片和条形图的可视化页面。

## ASCII 条形图摘要
v1.0.1 终端输出包含类型分布图：
```
████████████████████ 中国大陆身份证号: 15
████████████ 邮箱: 8
██████ 手机号: 4
```

## Legal
本工具仅辅助检测，不能替代专业合规审计。检测结果可能存在漏报或误报，使用者应自行核实。

## Security
- ✅ 纯本地运行，无网络请求
- ✅ 仅读取用户指定的文件
- ✅ 检测结果脱敏显示，不泄露原始数据
- ❌ 无任意代码执行（无 exec/eval）
- ❌ 无系统命令执行（无 subprocess/shell）
