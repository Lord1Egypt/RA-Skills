---
name: hongkong-immigration
description: "Answer and plan Hong Kong visa, entry-permit, residency, and immigration questions. Use when the user asks about 港澳通行证/签注、单程证、访港签证、高才通、优才、专才、IANG、受养人、香港身份或永居以及赴港旅游、工作、留学或定居."
---

# hongkong-immigration

## Purpose

帮助用户判断赴港所需证件/签证类型，给出申请路径、材料清单和官方办理渠道。覆盖三类人群：内地居民（通行证+签注）、外国护照持有人（访港签证/免签）、赴港工作·升学·定居人士（人才计划）。

## When to use

- 用户问"去香港需要什么证件/签证"、办证流程、续签、逾期等问题。
- 用户比较高才通/优才/专才/IANG 等身份路径，或问永居/转永居条件。
- 不适用：澳门单独事务、香港以外目的地、法律纠纷代理（提示咨询持牌顾问或律师）。

## Workflow

1. 识别用户身份与目的，三选一并读取对应参考文件：
   - 中国内地居民短期赴港（旅游/探亲/商务）→ [references/mainland-permits.md](references/mainland-permits.md)
   - 外国护照持有人访港/过境 → [references/visit-visas.md](references/visit-visas.md)
   - 任何国籍，赴港工作、升学、创业、定居 → [references/talent-schemes.md](references/talent-schemes.md)
   - 涉及法律依据、居留权认定、逾期/非法工作后果 → 另读 [references/legal-basis.md](references/legal-basis.md)
   - 续签、拒签、永居、换雇主、双重身份等高频争议 → 另读 [references/faq-playbook.md](references/faq-playbook.md)
2. 信息不足时先问清：国籍/户籍、目的、停留时长、学历与工作背景（人才类）。
3. 给出结论：所需证件类型、申请条件、材料清单、办理渠道、大致时间线。
4. 核实时效性：配额、薪资门槛、收费、免签名单等数字经常调整。凡引用具体数字，
   必须先用网络搜索核对官方来源（入境处 immd.gov.hk、国家移民管理局 nia.gov.cn），
   并注明信息截至日期；无法核实时明确说明"以官方最新公布为准"。
5. 结尾提醒：本回答为一般信息，不构成法律或移民建议；个案以受理机关认定为准。

## Output format

专业、引经据典是硬要求。具体规范：

- 先一句话给结论（需要什么证件/走哪条路径），再分步骤展开；比较用表格。
- 每个关键论断标注依据，分三个层级并明确区分：
  1. 法律依据：引用条例章节条文（如《入境条例》Cap.115 第 41 条），取自 legal-basis.md；
  2. 政策口径：引用入境处/移民局官方页面并给链接；
  3. 实务经验：来自社区案例（faq-playbook.md）的注明"实务经验，非官方口径"。
- 给方案时输出完整行动清单：条件自查 → 材料清单 → 办理渠道 → 时间线 → 风险点。
- 末尾集中列出全部引用来源链接。

## References

- [references/mainland-permits.md](references/mainland-permits.md) — 港澳通行证与签注种类、办理与续签
- [references/visit-visas.md](references/visit-visas.md) — 外籍访客免签安排与访港签证
- [references/talent-schemes.md](references/talent-schemes.md) — 高才通/优才/专才/IANG/留学路径与永居
- [references/legal-basis.md](references/legal-basis.md) — 基本法、入境条例(Cap.115)等法律依据与关键判例
- [references/faq-playbook.md](references/faq-playbook.md) — 续签/拒签/永居/双重身份等高频问题实战手册
