#!/usr/bin/env python3
"""HIPAA 美国医疗健康护栏 - 规则包 (terms)。

覆盖美国《健康保险流通与责任法案》(Health Insurance Portability and
Accountability Act, 42 U.S.C. § 1320d et seq.) 及 HHS 隐私规则
(45 C.F.R. Part 160/164)、安全规则语境下，面向美国市场的医疗健康产品
（远程医疗 / 医疗 SaaS / 健康 App / 患者门户）在文案、隐私政策、产品描述中
需警惕的 PHI（受保护健康信息）处理触发点与违规表述。

纯数据定义，无副作用、无网络、无动态执行。

每条术语字段：
    term        触发/违规用语（子串匹配，大小写不敏感）
    category    类别
    severity    风险等级 high / medium / low
    suggestion  整改建议（可选，缺省时使用类别默认建议）

设计原则：
  - 只收录"红线清晰、可编码"的高频触发词与违规表述，降低误报。
  - HIPAA 适用前提是"触及受保护健康信息(PHI)"且属于 covered entity 或
    business associate，因此第一要务是识别"是否处理 PHI"（phi_handling 类）。
  - 一旦触及 PHI，核心义务是签 BAA、落实三层防护、保障个人访问权与泄露通知。
  - 规则可扩展：直接在 TERMS 中追加即可，内核无需改动。
"""

PROFILE = {
    "id": "hipaa",
    "name": "HIPAA 医疗健康护栏规则",
    "version": "1.0.0",
    "basis": "美国《健康保险流通与责任法案》(Health Insurance Portability and Accountability Act, 42 U.S.C. § 1320d et seq.) 及 HHS 隐私规则(45 C.F.R. Part 160/164)、安全规则",
}

# ============ 类别默认建议 ============
CATEGORY_DEFAULT = {
    "phi_handling": "若业务涉及'受保护健康信息'(PHI)的处理，HIPAA 隐私规则与安全规则全面适用：须签 BAA、落实管理/物理/技术三层防护、保障个人访问权与泄露通知。",
    "no_baa": "向业务伙伴(Business Associate)披露 PHI 前须签订商业伙伴协议(BAA)；声称无需 BAA 即共享 PHI 属违规。",
    "no_encryption": "PHI 的存储与传输须加密(安全规则技术防护)；明文存储/传输健康数据属高风险缺口。",
    "third_party_phi": "向第三方披露或出售 PHI 须符合最小必要原则并取得授权；建议审查披露协议与最小化措施。",
    "no_breach_notification": "发生 PHI 泄露须按 breach notification rule 在 60 日内通知受影响个人及 HHS；缺失泄露通知机制属违规。",
    "no_individual_access": "个人有权访问并获取其 PHI 副本；拒绝或限制个人访问权违反隐私规则。",
}

CATEGORY_LABEL = {
    "phi_handling": "处理受保护健康信息(PHI)",
    "no_baa": "缺少商业伙伴协议(BAA)",
    "no_encryption": "PHI 未加密",
    "third_party_phi": "第三方披露 PHI",
    "no_breach_notification": "缺失泄露通知机制",
    "no_individual_access": "限制个人访问权",
}

# ============ 术语表 ============
# (term, category, severity, suggestion?)
TERMS = [
    # —— 处理受保护健康信息(PHI) high（触发 HIPAA 适用）——
    ("protected health information", "phi_handling", "high", None),
    ("PHI", "phi_handling", "high", None),
    ("patient health data", "phi_handling", "high", None),
    ("patient data", "phi_handling", "high", None),
    ("medical records", "phi_handling", "high", None),
    ("health information", "phi_handling", "high", None),
    ("electronic health record", "phi_handling", "high", None),
    ("clinical data", "phi_handling", "high", None),
    ("受保护健康信息", "phi_handling", "high", None),
    ("患者健康数据", "phi_handling", "high", None),
    ("病历信息", "phi_handling", "high", None),
    ("医疗数据", "phi_handling", "high", None),
    ("电子病历", "phi_handling", "high", None),
    ("临床数据", "phi_handling", "high", None),

    # —— 缺少商业伙伴协议(BAA) high ——
    ("share PHI without BAA", "no_baa", "high", None),
    ("no business associate agreement", "no_baa", "high", None),
    ("without BAA", "no_baa", "high", None),
    ("BAA not required", "no_baa", "high", None),
    ("无商业伙伴协议", "no_baa", "high", None),
    ("未签BAA", "no_baa", "high", None),
    ("无需BAA", "no_baa", "high", None),
    ("不签商业伙伴协议", "no_baa", "high", None),

    # —— PHI 未加密 high ——
    ("store PHI unencrypted", "no_encryption", "high", None),
    ("unencrypted patient data", "no_encryption", "high", None),
    ("plaintext health records", "no_encryption", "high", None),
    ("PHI in plaintext", "no_encryption", "high", None),
    ("明文存储病历", "no_encryption", "high", None),
    ("未加密健康数据", "no_encryption", "high", None),
    ("明文保存患者信息", "no_encryption", "high", None),

    # —— 第三方披露 PHI medium ——
    ("sell patient data", "third_party_phi", "medium", None),
    ("share health records with third parties", "third_party_phi", "medium", None),
    ("disclose PHI to third party", "third_party_phi", "medium", None),
    ("出售患者数据", "third_party_phi", "medium", None),
    ("向第三方共享病历", "third_party_phi", "medium", None),
    ("出售健康数据", "third_party_phi", "medium", None),

    # —— 缺失泄露通知机制 medium ——
    ("no breach notification", "no_breach_notification", "medium", None),
    ("breaches not reported", "no_breach_notification", "medium", None),
    ("without breach notice", "no_breach_notification", "medium", None),
    ("未通知数据泄露", "no_breach_notification", "medium", None),
    ("泄露不报告", "no_breach_notification", "medium", None),

    # —— 限制个人访问权 medium ——
    ("deny patient access", "no_individual_access", "medium", None),
    ("no right to access records", "no_individual_access", "medium", None),
    ("restrict patient access", "no_individual_access", "medium", None),
    ("拒绝患者访问", "no_individual_access", "medium", None),
    ("无权查看病历", "no_individual_access", "medium", None),
    ("限制患者访问病历", "no_individual_access", "medium", None),
]
