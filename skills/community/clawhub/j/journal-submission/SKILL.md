---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4a677bd9d680e9793dee310c93c3656_2ffda460617411f1832e5254006c9bbf
    ReservedCode1: wMgawdxbWiQ/0XR2GSMPVbF07TzpyghdS/p5Mif2FTZ7foLL6VVg7cxw+hw3BZtj4FrSpBbQVLwVQUhmjTYXCmBRbpKMK9772/mEjrsZnWVoF2ZXqPgTo70fdZzgAuDHhUHdbnEbZhdUEM4h0OFwTmNUVgil0iYvakzFgq1WJmtwpK/v1cA6AXZGUig=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4a677bd9d680e9793dee310c93c3656_2ffda460617411f1832e5254006c9bbf
    ReservedCode2: wMgawdxbWiQ/0XR2GSMPVbF07TzpyghdS/p5Mif2FTZ7foLL6VVg7cxw+hw3BZtj4FrSpBbQVLwVQUhmjTYXCmBRbpKMK9772/mEjrsZnWVoF2ZXqPgTo70fdZzgAuDHhUHdbnEbZhdUEM4h0OFwTmNUVgil0iYvakzFgq1WJmtwpK/v1cA6AXZGUig=
---

# AI 学术论文润色 (Academic Polish)

## 概述

Academic Polish 是一款 AI 驱动的学术论文润色技能，基于全球顶级期刊规范库 + 多学科术语词典 + 学术英语语法规则引擎，自动对论文段落进行语言润色、格式规范化、引用合规检查和学术风格优化，输出逐句对照的修改报告。

## 适用场景

- 投稿前论文语言润色与格式排版
- 论文初稿的学术英语语法校对
- 引用格式自动转换与合规检查
- 多学科交叉论文的术语统一
- 非英语母语研究者的学术写作提升

## 润色维度

| 维度 | 说明 |
|------|------|
| 语法与拼写 | 时态、主谓一致、冠词、拼写错误修正 |
| 学术风格 | 被动语态/主动语态优化、冗余表达精简、正式度提升 |
| 逻辑连贯 | 段落衔接、过渡词、逻辑递进关系优化 |
| 术语规范 | 学科术语统一、缩写首次定义、符号标准化 |
| 引用格式 | 参考文献格式转换、引文插入、交叉引用校验 |
| 合规性 | 字数限制、摘要结构、关键词格式、图表编号 |
| 期刊适配 | 针对目标期刊的格式模板、模板匹配检查 |

## 支持的期刊与格式规范

| 期刊 / 出版社 | 覆盖规范 |
|------|---------|
| Nature | Article / Letter / Review 格式，200 字摘要，Methods 独立节 |
| Science | Research Article / Report，125 词摘要，SM 要求 |
| Elsevier | 旗下 2,500+ 期刊模板，LaTeX / Word 双格式 |
| IEEE | IEEEtran 模板，双栏格式，6-8 页限制 |
| ACM | ACM Primary Article Template，CCS Concepts |
| Springer | Lecture Notes / 期刊模板，Word / LaTeX |
| PLOS | PLOS ONE / Biology / Medicine，开放获取规范 |
| 中文核心期刊 | GB7714 引用，CNKI 格式，中文摘要 200-300 字 |

## 支持的引用格式

| 格式 | 适用领域 | 示例 |
|------|---------|------|
| APA 7th | 心理学、教育学、社会科学 | (Smith, 2023, p. 42) |
| MLA 9th | 文学、语言学、人文科学 | (Smith 42) |
| Chicago (Notes-Bibliography) | 历史、艺术、人文学科 | ^1 Smith, *Title*, 42. |
| Harvard | 商科、经济学 | (Smith 2023, p.42) |
| IEEE | 工程、计算机科学 | [1] |
| Vancouver | 医学、生物医学 | [1] |
| GB/T 7714-2015 | 中文学术期刊 | [1] 张三. … |
| ACS | 化学 | 1. Smith, J. … |

## 支付协议（AI收）

本技能采用支付宝 AI 收 HTTP 402 协议，按次计费。

| 项目 | 值 |
|------|-----|
| 单价 | ¥0.50 / 次 |
| 支付协议 | `alipay_` 短链协议 |
| 网关地址 | `http://8.145.54.67:3000` |
| 技能路径 | `/skill/academic-polish` |
| 支付确认路径 | `/pay-confirm` |

### 支付流程

```
1. 客户端发起润色请求  POST /skill/academic-polish
2. 服务端返回 402 Payment Required
   Header: X-Payment-Needed: true
   Header: X-Short-Link: alipay_XXXXXXXXXXXXXXXX
3. 用户完成支付宝支付
4. 客户端携带支付凭证回传  POST /pay-confirm
   Header: X-Payment-Credential: <支付凭证>
5. 服务端验证通过 → 执行论文润色 → 返回结果
```

### HTTP 请求头规范

| 头名称 | 说明 |
|--------|------|
| `X-Payment-Needed` | 服务端返回：`true` 表示需要支付 |
| `X-Short-Link` | 服务端返回：支付宝短链 URL 供用户支付 |
| `X-Payment-Credential` | 客户端回传：支付完成后的凭证字符串 |
| `X-Service-Tier` | 可选，`basic`（基础润色）或 `premium`（深度润色） |

## 润色服务档位

### 基础档（basic = ¥0.50）
- 单段论文文本润色（最多 2,000 词）
- 语法/拼写/标点修正
- 学术风格基础优化
- 修改对照（原文 vs 润色后）
- 输出 JSON 格式润色报告

### 深度档（premium = ¥1.00 - 预留）
- 全部基础功能
- 逐句详细分析（语法/逻辑/术语）
- 目标期刊格式自动适配
- 引用格式自动转换
- 查重预检建议
- 输出 PDF 完整润色报告

## 数据底座

所有期刊规范、引用格式规则、学术英语错误模式、学科术语词典存储于 `references/academic-polish.json`，结构如下：

```json
{
  "journal_specs": { ... },        // Nature/Science/Elsevier/IEEE/ACM 期刊规范
  "citation_rules": { ... },       // APA/MLA/Chicago/Harvard/IEEE/GB7714 引用规则
  "academic_errors": [ ... ],      // 学术英语常见错误模式
  "discipline_lexicon": { ... },   // 各学科术语词典
  "style_guidelines": [ ... ]      // 学术写作风格指南
}
```

## 使用示例

### 请求

```bash
curl -X POST http://8.145.54.67:3000/skill/academic-polish \
  -H "Content-Type: application/json" \
  -H "X-Service-Tier: basic" \
  -d '{"text": "The result shows that the method is very good and can be used in many applications.", "discipline": "computer_science", "target_journal": "IEEE"}'
```

### 响应（支付后）

```json
{
  "service": "AI 学术论文润色",
  "tier": "basic",
  "discipline": "computer_science",
  "target_journal": "IEEE",
  "polish_stats": {
    "grammar_fixes": 2,
    "style_improvements": 3,
    "terminology_suggestions": 1
  },
  "original": "The result shows that the method is very good and can be used in many applications.",
  "polished": "The experimental results demonstrate that the proposed method achieves superior performance and exhibits broad applicability across diverse domains.",
  "diff": [
    {
      "type": "style",
      "original": "The result shows that",
      "revised": "The experimental results demonstrate that",
      "reason": "学术写作中应使用更精确的表述，'result' 应具体化为 'experimental results'，'shows' 应升级为 'demonstrates'"
    },
    {
      "type": "word_choice",
      "original": "very good",
      "revised": "superior performance",
      "reason": "避免使用主观形容词 'very good'，改为可量化的学术表述"
    },
    {
      "type": "word_choice",
      "original": "can be used in many applications",
      "revised": "exhibits broad applicability across diverse domains",
      "reason": "替换过于口语化的表达，提升学术正式度"
    }
  ],
  "citation_suggestions": [
    "如本文涉及方法对比，建议引用 IEEE 格式的相关文献：[1] Author, 'Title,' Journal, vol., no., pp., Year."
  ]
}
```

## 许可

MIT License — 详见 LICENSE 文件
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
