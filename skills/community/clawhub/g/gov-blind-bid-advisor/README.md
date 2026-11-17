# 政府采购盲投参谋（gov-blind-bid-advisor）

## 简介

投标人（供应商）侧的**盲投参谋**：不靠人脉关系，只用公开数据，专注两件事——

1. **商机发现**：采集政府采购公开公告，按你的企业画像做匹配度评分与排序，输出"适合我投"的高匹配项目雷达。
2. **投标决策**：对某一个具体项目，做资格符合性 / 能力适配 / 利润测算 / 风险雷区的 go/no-go 结构化判断，输出"强烈建议投 / 建议投 / 谨慎 / 不建议"结论与关键动作。

并内置**投标人防御视角**的风险自查：时间节点合规、废标雷区、排他性/萝卜坑条款扫描（帮你识别"被量身定制"的标）。

纯本地 + 公开数据采集，零 API Key。

## 文件结构

```
gov-blind-bid-advisor/
├── SKILL.md                           # 核心技能（系统提示 / 入口）
├── README.md                          # 本文件
├── _meta.json                         # 技能元数据
├── references/                        # 参考文档
│   ├── category-codes.md              # 公告类别码 + 品目分类（解析/匹配用）
│   ├── enterprise-profiling.md        # 企业画像数据模型与匹配算法
│   ├── bid-decision-rubric.md         # 投标决策评分框架、阈值、法条
│   ├── compliance-guardrails.md       # 合规红线、废标雷区、萝卜坑识别
│   ├── procurement-platforms.md       # 数据源说明（唯一数据源：ccgp.gov.cn 中央站）
│   ├── anti-scraping-best-practices.md# 采集合规最佳实践
│   └── ima-knowledge-bases.md         # IMA 知识库挂载清单与检索增强用法
└── scripts/                           # 辅助脚本（Python，可独立运行）
    ├── collected_data.py              # 合规采集器（唯一数据源：中国政府采购网中央站）
    ├── enterprise_matcher.py          # 企业画像匹配与商机评分
    ├── bid_decision_analyzer.py       # 投标决策分析器
    └── compliance_checker.py          # 招标文件风险自查（投标人防御视角）
```

## 核心能力

| 功能 | 做什么 | 触发词示例 |
|------|--------|-----------|
| 🔍 商机发现 | 采集公告 + 画像匹配 + 排序雷达 | "找广东的 AI 大模型项目""扫描适合我投的标" |
| 📊 投标决策 | 资格/能力/利润/风险 go-no-go | "这个标能不能投""分析一下这个公告" |
| 🛡️ 风险自查 | 时间合规 + 废标雷区 + 萝卜坑扫描 | "这个标有没有排他条款""时间节点合规吗" |

## 合规红线（不可逾越）

- ❌ 围标 / 串标 / 价格联盟；不提供任何协同报价或规避审查的方法。
- ❌ 资质 / 业绩造假、虚假中小企业声明；缺失资质只给*合法*补强路径。
- ❌ 规避否决条款、破解验证码、绕过登录、轮换 IP、采集非公开信息。
- ✅ 仅用公开数据；robots + 同域 ≥3 秒限速 + 透明 UA；决策仅供参考，最终由投标人拍板。

## 使用方式

### 在对话中直接使用
```
用户：找广东省近期的 AI 大模型采购项目
用户：分析这个标能不能投 http://www.ccgp.gov.cn/cggg/zygg/...
用户：这个招标文件有没有排他性条款（粘贴文本）
```

### 脚本独立运行
```bash
# 1. 采集中央站公开招标公告（默认 2 页；--pages 控制翻页）
python scripts/collected_data.py --pages 3 --output ccgp.json

# 2. 商机匹配（需企业画像 JSON）
python scripts/enterprise_matcher.py --projects ccgp.json --enterprise my_company.json --output match.json

# 3. 投标决策（需项目 JSON + 企业画像）
python scripts/bid_decision_analyzer.py --project project.json --enterprise my_company.json --output decision.json

# 4. 招标文件风险自查
python scripts/compliance_checker.py --project project.json --output risk.json
```

> 📌 **数据源说明**：本技能**仅以中国政府采购网中央站（www.ccgp.gov.cn）为唯一数据源**。
> 各省政府采购网的招标数据会汇总/同步到中央站，且省级站反爬普遍较强；
> 因此只采中央站即可覆盖全国（含省级）公开公告，无需逐省采集，也更稳健合规。

## IMA 知识库挂载（检索增强）

本技能可挂载用户发布的招投标 / 政府采购权威 IMA 知识库（需宿主已连接 IMA MCP），用于检索真实招标文件、
法规全文、否决 / 投诉案例，使结论有据可循。共挂载 7 个库：6 个主挂载（招标文件汇集、政府采购实务与合规、
招投标实务与合规、评标否决AI、异议投诉处理、政府采购投诉AI）+ 1 个次挂载（国有企业采购，话题触发）。
已实测均可检索；订阅库「法律-法律案例」因检索返回空已排除。完整清单与用法见
`references/ima-knowledge-bases.md`。

## 依赖

**必需**：Python 3.10+  
**采集/匹配/决策**：`requests` + `beautifulsoup4`（中央站采集实测可用）  
无 OCR / 无外部 API Key。网络或依赖缺失时自动降级（见 SKILL.md 鲁棒性章节）。

## 许可证

MIT License

## 反馈与联系

使用问题、误报反馈、实务建议，欢迎通过 **项目仓库提交 Issue** 反馈（GitHub Issues）。
本技能仅通过项目仓库接收反馈，不附加任何第三方联系方式或推广信息。

## 免责声明

本技能所有分析、建议均基于公开信息与统计模型，仅供参考，不构成法律、财务或投资建议；
投标与否及质疑/投诉等法律行为的最终决策与责任由投标人自行承担。

---

署名：一线评标专家&ChesaraM
