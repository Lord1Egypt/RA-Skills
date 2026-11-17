---
name: lgd-badge-verify
description: >-
  Verify a badge certificate by recomputing its fingerprint to catch tampering, checking that evidence hashes match the expected format, and confirming the serial exists in the ledger and was not revoked.

  lgd-badge-verify — 验徽章证书：指纹重算防篡改 + 证据哈希格式校验 + 台账对账（serial 存在且未吊销）。
slug: lgd-badge-verify
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
display_name: LGD 徽章验真器
display_name_en: LGD Badge Verifier
agent_created: true
author: XLGD · 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux]
copyright: XLGD · SynomosAI
description_zh: "lgd-badge-verify — 验徽章证书：指纹重算防篡改 + 证据哈希格式校验 + 台账对账（serial 存在且未吊销）。"
description_en: "Verify a badge certificate by recomputing its fingerprint to catch tampering, checking that evidence hashes match the expected format, and confirming the serial exists in the ledger and was not revoked. Use it when receiving certified files or devices, running supply-chain checks or auditing a certificate inventory."
classification:
  internal: ["LGD theory system"]
  skillhub: ["ai-governance"]
  clawhub: ["search", "development"]
  iso_25010: ["Security", "Maintainability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [lgd-badge-verify, AI 治理, LGD徽章, 证书验真]
read_when:
  - 供应链安全场景，接收带徽章证书的文件/设备时做身份核验
  - 合规审计要验证证书指纹防篡改能力与证据哈希格式
  - 库存管理要确认徽章序列号在台账中存在且未吊销
  - 用户说「这个徽章是真的吗」「证书被改过没有」
ai_protocol: true

---
> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
For supply-chain security — identity verification when receiving electronic files or devices bearing a badge certificate. For compliance audits — verifying the certificate's anti-tamper fingerprint and whether evidence-hash formats meet the standard. For inventory management — confirming the badge serial exists in the ledger and is not currently revoked.

### Usage
Run the script `badge_verify.py`; the `--serial` parameter (string) does a fast check by certificate serial. Call the `verify_integrity()` action to read a file and recompute the fingerprint and compare hash formats. For ledger reconciliation, use `reconcile_ledger(serial)` with the database connection info.

### Workflow
1. Load the dependency script `badge_verify.py` into the runtime sandbox.
2. Parse the input for the certificate serial or file path.
3. Run the fingerprint-recompute algorithm against the raw data to detect tampering.
4. Validate that evidence-hash formats meet the required cryptographic standard.
5. Query the internal ledger to confirm the serial exists and is not marked revoked.
6. Aggregate all checks and output the final pass/fail verdict.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
适用于供应链安全场景，当接收带有徽章证书的电子文件或设备时进行身份核验。适用于合规审计场景，需要验证证书指纹防篡改能力及证据哈希格式是否符合标准。适用于库存管理场景，需确认徽章序列号在台账中存在且当前未被吊销的状态。

### 用法
执行脚本 `badge_verify.py`，支持参数 `--serial`（字符串型，输入证书序列号）进行快速校验。可调用动作 `verify_integrity()` 读取文件并执行指纹重算与哈希格式比对。若需台账对账功能，使用动作 `reconcile_ledger(serial)` 并传入数据库连接信息。

### 流程
1. 加载技能依赖脚本 `badge_verify.py` 至运行沙箱环境。
2. 解析输入参数获取证书序列号或文件路径数据。
3. 执行指纹重算算法比对原始数据，防止篡改修改。
4. 校验证据哈希格式是否符合系统规定的加密标准。
5. 查询内部台账确认该序列号存在且状态未标记为吊销。
6. 汇总所有校验结果并输出最终验证通过或不通过判定。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

## Triggers / 触发词

这些是用户真实会说的话（中 / 英对照），命中任一即应加载本技能：

- 「这个证书是不是被人改过」 / "has this certificate been tampered with"
- 「收到的文件带徽章怎么验真」 / "the file came with a badge, how do I verify it"
- 「编号在台账里查不到」 / "this serial is missing from our ledger"
- 「证书是不是已经吊销了」 / "check whether the certificate was revoked"
- 「供应链来料资质要核一遍」 / "we need to verify supplier credentials"
- 「证据哈希格式对不对怎么判断」 / "is this evidence hash in the right format"

Trigger when the user says any of the above, in Chinese or English.

---

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/lgd-badge-verify
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/lgd-badge-verify/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

---

## Data handling / 数据处理边界

- 默认不向任何外部地址发送数据：扫描结果、报告、命中明细一律只写本地或只打印到当前会话。
- 如需外发（告警、工单、邮件、IM），必须由人先明确指定接收方，并在每次发送前逐次确认；本技能不预设、也不硬编码任何接收端。
- 只处理调用者明确指定的目标路径，不遍历无关目录，不跟随符号链接，不读取目标之外的凭据文件。
- 命中内容在输出时按需脱敏，避免把敏感原值写进日志或对话记录。
