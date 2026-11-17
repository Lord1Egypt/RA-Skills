# 🛡️ HIPAA 美国医疗健康护栏 (hipaa-guard) v1.0.0

面向**出海美国、处理健康数据**的医疗科技产品（远程医疗 / 医疗 SaaS / 健康 App /
患者门户）的**事前合规护栏**。在文案、隐私政策、产品描述**发布前**，实时检测触发
HIPAA 适用的表述与医疗隐私违规用语，按风险分级输出命中与整改建议。

## 为什么需要

HIPAA（Health Insurance Portability and Accountability Act）由美国 HHS 执法：任何触及
"受保护健康信息"(PHI) 的 covered entity 或其 business associate，必须签 BAA、落实
管理/物理/技术三层安全防护、保障个人访问权，并在 PHI 泄露时履行通知义务。违规可由
HHS OCR 处以高额罚款。本护栏帮你在发布前拦住高频红线。

## 快速开始

```bash
python3 scripts/guard.py --text "We store PHI unencrypted and share health records with third parties"
echo "patient data without BAA" | python3 scripts/guard.py --stdin
python3 scripts/guard.py --text "..." --format json
python3 scripts/guard.py --list-categories
```

## 检测范围（6 类）

| 类别 | 风险 |
|------|------|
| 处理受保护健康信息(PHI) | high |
| 缺少商业伙伴协议(BAA) | high |
| PHI 未加密 | high |
| 第三方披露 PHI | medium |
| 缺失泄露通知 | medium |
| 限制个人访问权 | medium |

## 特性

- 纯本地、零网络、零动态执行（仅 Python 标准库）
- 风险分级 + 逐条整改建议 + 结构化 JSON
- 内核与规则分离，追加词即可扩展

## 法律声明

本工具仅作辅助检测，**不构成法律建议**。重大合规决策请咨询具备美国法执业资格的法律顾问。
详见 `SKILL.md` 的「法律声明」与「Skill 自身合规声明」章节。
