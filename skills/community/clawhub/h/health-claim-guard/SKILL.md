---
name: health-claim-guard
description: 健康宣称合规扫描 — 保健品/食品宣传文案扫违规疗效宣称（根治/治愈/无副作用等），缺警示语即 FAIL（零依赖） 适用场景：当需要健康宣称合规扫描能力时使用本技能；触发词：health-claim-guard。
slug: health-claim-guard
version: 1.0.1
display_name: 健康宣称合规扫描
display_name_en: Health Claim Guard
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude, codex, cursor, windsurf, workbuddy]
copyright: SynomosAI
description_zh: "健康宣称合规扫描 — 保健品/食品宣传文案扫违规疗效宣称（根治/治愈/无副作用等），缺警示语即 FAIL（零依赖）"
description_en: "Scan health-product marketing copy for illegal therapeutic claims (cure, heal, no side effects) and missing warning labels; violations FAIL (zero-dependency)."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
tags: [health-claim-guard, AI 治理, 健康宣称, 广告合规]
read_when:
  - 保健品/营养品/食品营销文案发布前合规预检
  - 检测文案里有没有"根治""治愈""无副作用"等违规疗效宣称
  - 发布前检查宣传内容是否缺必要健康警示语/风险提示
  - 用户说「这句宣传违不违规」「广告法会不会罚」
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/health_claim_guard.py
  runtime: python3
  call_pattern: args
input_schema:
  args:
    type: string
    description: "命令行参数透传给主脚本，具体取值见各包 --help"
    required: false
output_schema:
  stdout:
    type: string
    description: "标准输出为 JSON 结果，含逐项检查与总体结论"
  exit_code:
    type: integer
    description: "0=PASS/完成；1=FAIL/有警告或待补强；2=用法或参数错误"
capabilities:
  - cli_tool
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first), added read_when; 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
- Pre-release compliance screening of marketing copy for supplements, nutraceuticals and food products.
- Detecting illegal therapeutic claims in text such as "cure" or "heal".
- Checking, before publication, whether the copy is missing required health warnings or risk disclaimers.

### Usage
- **Command**: `python scripts/health_claim_guard.py --input <copy>`
- **Parameters**: `--input` accepts the string or file path to scan; the core logic script runs the analysis directly.
- **Dependency check**: make sure the local environment can find and read the main script.

### Workflow
1. Start the Python runtime and load `health_claim_guard.py`.
2. Feed the copy under review into the scan engine via CLI argument or stdin.
3. The system parses the text automatically, flagging words with illegal features such as "cure" or "no side effects".
4. It checks whether compliant warning-language statements are present; if missing, the text is flagged high-risk.
5. Emit the final verdict: FAIL if violations exist, otherwise PASS.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
- 适用于保健品、营养品等营销文案的合规性预检场景。
- 用于检测文本中是否存在“根治”、“治愈”等违规医疗疗效宣称。
- 在发布前检查宣传内容是否遗漏必要的健康警示语或风险提示。

### 用法
- **执行命令**：`python scripts/health_claim_guard.py --input <文案内容>`
- **参数说明**：`--input` 参数接受待扫描的字符串或文件路径，直接调用主逻辑脚本执行分析。
- **依赖检查**：确保本地环境中主脚本文件可被正常识别与读取。

### 流程
1. 启动 Python 环境并加载 `health_claim_guard.py` 脚本。
2. 将待审核的宣传文案通过命令行参数或标准输入注入到扫描引擎中。
3. 系统自动解析文本，识别包含“根治”、“无副作用”等违规特征的词汇。
4. 检测文案中是否存在合规的警示语声明，若缺失则标记高风险。
5. 输出最终判定结果，存在违规行为时返回 FAIL，否则显示 PASS。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
