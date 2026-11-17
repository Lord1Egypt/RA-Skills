# 🔍 Privacy Check

**隐私敏感信息扫描器** — 检测文件中的敏感个人信息（PII），支持 15+ 种模式、多种输出格式和高级过滤功能。

纯 Python 标准库，无外部依赖，全本地运行。

---

## 功能特性

| 功能 | 说明 |
|------|------|
| 15+ PII 模式 | 身份证、手机号、邮箱、银行卡、信用卡(含Luhn校验)、SSN、护照、驾驶证、微信号、支付宝号等 |
| 智能脱敏 | 根据不同类型自动脱敏，保留格式但隐藏原文 |
| 多格式输出 | JSON（默认）、CSV、HTML 报告 |
| 白名单忽略 | `--ignore` 参数使用正则排除不相关行 |
| 文件类型过滤 | `--ext .txt,.csv` 只扫描指定扩展名 |
| ASCII 条形图 | 终端输出含类型分布条形图 |
| 递归目录扫描 | 自动遍历子目录所有文件 |
| Luhn 校验 | 银行卡号、信用卡号自动 Luhn 算法验证 |

## 检测模式

| 模式ID | 检测内容 | 严重级别 |
|--------|---------|---------|
| china_id | 中国大陆18位身份证号 | 高 |
| china_phone | 中国大陆手机号 | 高 |
| email | 电子邮件地址 | 中 |
| bank_card | 银行卡号（Luhn校验） | 高 |
| credit_card | 信用卡号（Luhn校验） | 高 |
| ssn | 美国社会安全号 | 高 |
| china_passport | 中国护照号 | 高 |
| hk_passport | 港澳护照号 | 高 |
| tw_passport | 台湾护照号 | 中 |
| driver_license | 中国大陆驾驶证号 | 高 |
| wechat_id | 微信号 | 中 |
| alipay_id | 支付宝账号（邮箱/手机） | 中 |
| ip_address | IP地址 | 低 |
| china_postal | 邮政编码 | 低 |
| api_key | API密钥 | 高 |

## 快速开始

```bash
# 扫描单个文件
python3 scripts/scanner.py --file data.csv

# 扫描目录下所有文件
python3 scripts/scanner.py --dir ./data/

# 导出 JSON 报告
python3 scripts/scanner.py --file users.json --output report.json

# 导出 HTML 报告（可视化）
python3 scripts/scanner.py --dir ./data/ --format html --output report.html

# 导出 CSV 报告
python3 scripts/scanner.py --file logs.txt --format csv --output report.csv

# 忽略注释行和日志前缀
python3 scripts/scanner.py --dir ./src/ --ignore "^#" --ignore "^//" --ignore "^--"

# 只扫描 CSV 和 JSON 文件
python3 scripts/scanner.py --dir ./uploads/ --ext .csv,.json
```

## 输出格式

### JSON（默认）
```json
{
  "scan_time": "2026-07-19T12:00:00",
  "total_findings": 42,
  "errors": 0,
  "by_type": {"china_id": 5, "china_phone": 10, "email": 20, ...},
  "by_severity": {"高": 30, "中": 10, "低": 2},
  "details": [
    {"file": "data.csv", "line": 128, "type": "china_id",
     "description": "中国大陆身份证号", "severity": "高",
     "match": "1101**********1234", "context": [...]}
  ]
}
```

### CSV
```
file,line,type,description,severity,match
data.csv,128,china_id,中国大陆身份证号,高,1101**********1234
```

### HTML
生成带样式和图表（ASCII条）的可视化报告，包含摘要卡片、类型分布和详情表格。

## 法律声明

本工具的设计目的是辅助识别文件中的潜在敏感个人信息，供数据治理和安全审查参考。它**不能替代专业合规审计**。

- 检测结果可能存在漏报（模式未覆盖的PII类型）或误报（非PII内容被匹配）
- 使用者应自行核实检测结果
- 脱敏处理仅用于显示，不保证完全消除再识别风险
- 建议结合业务数据和隐私法规要求进行人工复核

## 安全说明

- ✅ 纯本地运行，无网络请求
- ✅ 仅读取用户指定的文件路径
- ✅ 检测结果脱敏显示
- ❌ 无任意代码执行（exec/eval）
- ❌ 无系统命令执行（subprocess/shell）
- ❌ 无数据上传或遥测

## 许可证

MIT License — 详见 LICENSE 文件（如适用）。
