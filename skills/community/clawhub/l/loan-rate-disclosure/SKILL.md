---
name: loan-rate-disclosure
description: 借贷利率披露校验器 — 校验借贷报价是否按年化口径披露、是否超基准利率4倍司法保护上限（零依赖） 适用场景：当需要借贷利率披露校验器能力时使用本技能；触发词：loan-rate-disclosure。
slug: loan-rate-disclosure
version: 1.0.1
display_name: 借贷利率披露校验器
display_name_en: Loan Rate Disclosure Check
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux, cli]
platform_compatibility: [windows, macos, linux]
copyright: SynomosAI
description_zh: "借贷利率披露校验器 — 校验借贷报价是否按年化口径披露、是否超基准利率4倍司法保护上限（零依赖）"
description_en: "Validate that loan quotes disclose APR properly and stay within the 4x benchmark-rate judicial protection cap (zero-dependency)."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [loan-rate-disclosure, AI 治理, 借贷利率, 年化披露, 高利贷]
read_when:
  - 信贷业务审核要校验借贷报价是否按年化口径清晰披露
  - 风控系统接收第三方借贷报价要查是否超4倍基准利率司法保护上限
  - 贷款合同合规审查要快速识别高利贷隐患并拦截预警
  - 用户说「这个贷款利率合规吗」「年化报清楚了没」
ai_protocol: true


spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/loan_rate_disclosure.py
  runtime: python3
  call_pattern: args
input_schema:
  rate:
    type: number
    description: "对外报价利率（百分比，如 24 表示 24%）"
    required: false
  base:
    type: number
    description: "参考基准利率LPR（百分比，默认3.85）"
    required: false
  text:
    type: string
    description: "披露文案（校验是否含年化口径）"
    required: false
  json:
    type: bool
    description: "json"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - finance
  - disclosure
  - compliance
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first), added read_when; 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
In credit-business review, to verify that a loan quote is clearly disclosed on a standardized annualized basis and avoid consumer misunderstanding. When a risk system receives third-party loan quotes, use this skill to check whether the rate exceeds the judicial protection cap (4x the benchmark rate). It fits loan-contract compliance review — quickly spotting potential loan-shark risks for blocking or warning. In internal bank / financial-institution audits, it samples whether credit-product pricing meets regulatory disclosure requirements.

### Usage
Invoke the `loan-rate-disclosure` skill from the orchestration platform — no manual code change needed to trigger the check. Accepts JSON contract fragments, CSV quote files or plain text as input. The core parameter `input_data` holds the rate info under check; the output `compliance_status` auto-returns a compliant or violation verdict. The backing script `loan_rate_disclosure.py` runs in the cache directory; no external libraries to install.

### Workflow
1. The caller feeds the raw loan-quote data into the skill input port.
2. The system parses the data and identifies the per-period rate and interest period.
3. Non-annualized rates are auto-converted to a standardized nominal annual rate.
4. Fetch the current benchmark rate and run the internal algorithm to compute the judicial protection cap.
5. Compare the disclosed annual rate against the computed cap and produce the risk verdict.
6. Emit a structured report marking compliant pass or over-cap violation.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
在金融信贷业务审核中，用于校验借贷报价是否按标准年化口径清晰披露，避免消费者误解。当风控系统接收第三方借贷报价时，利用此技能检查利率是否存在超过司法保护上限（4 倍基准利率）的违规风险。适用于贷款合同合规性审查场景，快速识别潜在的高利贷隐患以进行拦截或预警。在银行或金融机构内部审计中，用于抽检信贷产品定价策略是否满足监管披露要求。

### 用法
通过系统技能编排平台调用命令 `loan-rate-disclosure`，无需手动修改代码即可触发校验逻辑。支持直接传入 JSON 格式合同片段、CSV 报价数据文件或文本字符串作为输入参数。指定核心参数 `input_data` 为待校验的利率信息内容，输出参数 `compliance_status` 自动返回合规或违规结论。底层依赖脚本 `loan_rate_disclosure.py` 在缓存目录中执行，无需安装外部库。

### 流程
第一步：调用端传入借贷报价的原始数据至技能输入端口。第二步：系统解析数据并识别出单期利率与计息周期信息。第三步：将非年化利率自动折算为标准化年化名义利率进行计算。第四步：获取当前基准利率，执行内部算法计算司法保护上限值。第五步：比对实际披露年利率与计算上限，生成风险评估结论。第六步：输出结构化报告，标记合规通过或违规超标项。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
