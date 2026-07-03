# 政府采购智能分析 Skill (gov-procurement-analyst)

## 简介

面向投标人（供应商）、招标代理、采购单位的**政府采购全流程智能分析助手**，覆盖商机发现、投标决策、文件编制、合规审计、供应商背调五大核心场景。

## 文件结构

```
gov-procurement-analyst/
├── SKILL.md                           # 核心技能文件（入口）
├── README.md                          # 本文件
├── references/                        # 参考文档
│   ├── procurement-platforms.md       # 数据源平台清单与合规指南
│   ├── anti-scraping-best-practices.md # 反爬策略与最佳实践
│   └── enterprise-profiling.md        # 企业画像构建与匹配算法
└── scripts/                           # 辅助脚本
    ├── collected_data.py              # 数据采集（合规版）
    ├── enterprise_matcher.py          # 企业画像匹配与商机评分
    ├── bid_decision_analyzer.py       # 投标决策分析器
    └── compliance_checker.py          # 合规审计辅助工具
```

## 核心能力

| 模块 | 功能 | 触发词 |
|------|------|--------|
| 商机发现 | 多平台采集 + 智能匹配 + 日报推送 | "政府采购"、"采购公告"、"帮我找项目" |
| 投标决策 | 资质检查 + 竞对分析 + 报价策略 + SWOT | "这个标能不能投"、"报价多少"、"中标概率" |
| 文件编制 | 招标文件解析 + 评分自检 + 内容生成 | "编制投标文件"、"生成技术方案" |
| 供应商背调 | 企业画像 + 诉讼/处罚/经营异常查询 | "查一下XX公司"、"企业背调" |
| 合规审计 | 围标串标检测 + 时间节点合规 + 评分异常 | "围标串标"、"采购合规检查" |

## 数据采集合规性

本 Skill 仅采集公开信息，严格遵守以下原则：

- ✅ 遵守各平台 robots.txt
- ✅ 请求间隔 ≥3 秒
- ✅ 明确的 User-Agent 标识
- ✅ 不破解验证码、不绕过付费墙
- ✅ 24 小时缓存，不重复请求
- ❌ 不使用代理池、不伪造身份
- ❌ 不采集非公开信息
- ❌ 不转售原始数据

详见 [references/anti-scraping-best-practices.md](references/anti-scraping-best-practices.md)

## 使用方式

### 在 WorkBuddy 中直接使用

安装后，在对话中使用触发词即可：

```
用户：帮我找北京的IT设备政府采购项目
Skill：[自动触发，执行商机发现流程]
```

### 脚本独立运行

```bash
# 1. 数据采集
python scripts/collected_data.py --url "http://search.ccgp.gov.cn/..." --output data.json

# 2. 企业匹配
python scripts/enterprise_matcher.py --projects data.json --enterprise my_company.json --output results.json

# 3. 投标决策
python scripts/bid_decision_analyzer.py --project project.json --enterprise company.json --output decision.json

# 4. 合规审计
python scripts/compliance_checker.py --projects projects.json --output audit.json
```

## 依赖

**必需**：
- Python 3.10+
- requests, beautifulsoup4

**推荐**：
- pdfplumber（PDF 解析）
- python-docx（Word 生成）
- pandas（数据处理）

## 版本历史

- v1.0.0 (2026-07-03)：初版发布

## 许可证

MIT License

## 免责声明

本 Skill 提供的所有分析、建议均基于公开信息和统计模型，仅供参考，不构成法律、财务或投资建议。
