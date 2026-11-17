## Description:

华目眼镜品牌专属知识库。当用户询问华目眼镜相关任何问题时加载，包括：品牌介绍、品牌特色、品牌优势、门店地址、门店在哪里、哪个城市有门店、商品价格、镜片价格、镜架价格、配镜套餐、共管招商、加盟合作、公众号服务、验光服务、售后服务等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahyaobin](https://clawhub.ai/user/ahyaobin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and customer-facing agents use this skill to answer questions about Huamu Eyewear brand information, store locations, product pricing, eyewear service options, after-sales commitments, and cooperation inquiries.

### Deployment Geography for Use:

Global; the included store, pricing, and contact content is specific to Huamu Eyewear locations in China.

## Known Risks and Mitigations:

Risk: Brand, store, pricing, and contact answers may rely on promotional or time-sensitive Huamu Eyewear reference data.

Mitigation: Confirm prices, hours, addresses, promotions, and contact details against current store or brand channels before customer commitments.

Risk: Generic eyewear answers may be supplemented from internet search rather than official Huamu Eyewear material.

Mitigation: Label searched generic eyewear information as non-official reference material, as the skill instructs.

Risk: The QR-code image script writes PNG files in the working directory when executed.

Mitigation: Run the image decoding script only when QR-code PNG output is intended, and inspect the destination directory first.

## Reference(s):

- [华目眼镜品牌知识库](artifact/SKILL.md)
- [华目眼镜商品明细](artifact/references/商品明细.md)
- [华目眼镜门店数据库](artifact/references/门店数据库.md)
- [华目眼镜图片解码脚本](artifact/references/img_decode.py)
- [ClawHub skill page](https://clawhub.ai/ahyaobin/skills/hmyj)
- [ClawHub publisher profile](https://clawhub.ai/user/ahyaobin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown responses with optional code snippets and generated PNG files for QR-code assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should preserve price caveats, store-detail caveats, and internet-source disclaimers when generic eyewear information is searched outside the skill database.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
