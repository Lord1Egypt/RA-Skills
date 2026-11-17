---
name: lgd-badge-issuer
description: >-
  Issue an lgd-certified badge certificate once a system passes all three law checks, attaching a SHA-256 fingerprint and a dated issuance record.

  lgd-badge-issuer — 三律全过才签发 lgd-certified 徽章证书（SHA-256 指纹 + 签发台账），未过拒绝并留痕。
slug: lgd-badge-issuer
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
display_name: LGD 徽章签发器
display_name_en: LGD Badge Issuer
agent_created: true
author: XLGD · 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux]
copyright: XLGD · SynomosAI
description_zh: "lgd-badge-issuer — 三律全过才签发 lgd-certified 徽章证书（SHA-256 指纹 + 签发台账），未过拒绝并留痕。"
description_en: "Issue an lgd-certified badge certificate once a system passes all three law checks, attaching a SHA-256 fingerprint and a dated issuance record. Use it when an automated review flow needs to confirm qualification and hand back an auditable credential, or to reject failing applications with a logged reason."
classification:
  internal: ["LGD theory system"]
  skillhub: ["ai-governance"]
  clawhub: ["search", "development"]
  iso_25010: ["Security", "Maintainability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [lgd-badge-issuer, AI 治理, LGD徽章, 证书签发]
read_when:
  - 用户完成三律考核并申请 lgd-certified 徽章证书时
  - 自动化审核流程要核验资格合规性并生成电子证书前
  - 审计要求输出含 SHA-256 指纹及签发记录的合规凭证时
  - 用户说「通过三律考核了，发个徽章」
ai_protocol: true

---
> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
- When a user has passed the "three laws" assessment and applies for an `lgd-certified` badge certificate.
- In an automated review flow, before verifying qualification compliance and generating an e-certificate.
- When an audit requires a compliance credential carrying a SHA-256 fingerprint and issuance record.

### Usage
- Run the Python script `badge_issuer.py` from the current environment.
- Core parameters: `--user_id` (user identifier) and `--three_laws_status` (pass status, e.g. `"all_pass"`).
- Example: `python badge_issuer.py --user_id "U001" --three_laws_status "all_pass"`.
- The skill handles dependencies and returns the certificate object or an error code.

### Workflow
1. The system receives the application data and the corresponding "three laws" verification status.
2. Internally call `badge_issuer.py` for pre-qualification and compliance check.
3. If the three laws do not all pass, trigger the refusal and log the failure to the ledger.
4. If all pass, generate the certificate content and compute its SHA-256 fingerprint.
5. Write the `lgd-certified` badge certificate to the designated output path and return it.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
- 用户完成“三律”考核并申请 `lgd-certified` 徽章证书时。
- 自动化审核流程中需要核验资格合规性并生成电子证书前。
- 审计需求要求输出包含 SHA-256 指纹及签发记录的合规凭证时。

### 用法
- 调用技能需执行 Python 脚本 `badge_issuer.py`，路径位于当前环境。
- 核心参数包含：`--user_id`（用户标识）、`--three_laws_status`（三律通过状态），示例为 `"all_pass"`。
- 命令执行格式参考：`python badge_issuer.py --user_id "U001" --three_laws_status "all_pass"`。
- 技能会自动处理依赖并返回证书对象或错误码。

### 流程
1. 系统接收用户申请数据及对应的“三律”验证状态。
2. 内部调用 `badge_issuer.py` 进行资格预审与合规校验。
3. 若“三律”未全过，触发拒绝机制并在台账记录失败日志。
4. 若“三律”全过，生成证书内容并计算 SHA-256 哈希指纹。
5. 将 `lgd-certified` 徽章证书写入指定输出路径并完成返回。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

## Triggers / 触发词

这些是用户真实会说的话（中 / 英对照），命中任一即应加载本技能：

- 「三律检查都过了，帮我出证书」 / "all three checks passed, issue the certificate"
- 「要给通过审核的系统发徽章」 / "issue a badge for an approved system"
- 「这个证书得带指纹和签发记录」 / "certificate must carry a fingerprint and issuance record"
- 「自动审核流程里怎么发凭证」 / "how to issue credentials inside an automated review"
- 「没过审的申请要拒绝并留痕」 / "reject a failed application and log why"
- 「给合规审计出一张可验证凭证」 / "give the auditor a verifiable compliance credential"

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
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/lgd-badge-issuer
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/lgd-badge-issuer/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

---

## Data handling / 数据处理边界

- 默认不向任何外部地址发送数据：扫描结果、报告、命中明细一律只写本地或只打印到当前会话。
- 如需外发（告警、工单、邮件、IM），必须由人先明确指定接收方，并在每次发送前逐次确认；本技能不预设、也不硬编码任何接收端。
- 只处理调用者明确指定的目标路径，不遍历无关目录，不跟随符号链接，不读取目标之外的凭据文件。
- 命中内容在输出时按需脱敏，避免把敏感原值写进日志或对话记录。
