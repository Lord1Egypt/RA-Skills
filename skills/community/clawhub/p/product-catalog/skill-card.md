## Description:

使用场景: 用户需要维护SKU产品库、显式绑定图片、确认中英文内容并生成和更新可核对PDF目录时。

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

供需要维护私有产品目录的用户使用：按 SKU 管理产品资料与图片，核对价格和中英文内容，并生成、比较及导出可复核的目录交付物。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private product details and images are stored by the platform, and its privacy and encryption claims are not independently verified.

Mitigation: Obtain authorization before uploading customer material and review the provider's privacy terms and retention behavior.

Risk: Exposure of a shared platform key could allow unauthorized account or product-catalog access.

Mitigation: Keep the key in the configured environment, and never paste it into chat, logs, or public files.

Risk: Incorrect product facts, image associations, translations, or fees could affect a catalog or incur charges.

Mitigation: Have the user verify each product's content and image, review current prices, and separately approve translations and paid generation before execution.

Risk: Deleting a library does not delete frozen project copies.

Mitigation: Delete the corresponding frozen projects separately when their data should be removed.

## Reference(s):

- [AI Skills 平台](https://ai-skills.open-idea.net)
- [产品目录操作与数据结构](https://ai-skills.open-idea.net/skill-docs/product-catalog/OPERATIONS.md)
- [HTTP 请求、上传与轮询](https://ai-skills.open-idea.net/skill-docs/product-catalog/HTTP-REQUESTS.md)
- [API 密钥与计费](https://ai-skills.open-idea.net/skill-docs/product-catalog/API-KEY.md)
- [授权、隐私与质量边界](https://ai-skills.open-idea.net/skill-docs/product-catalog/BEHAVIOR-RULES.md)
- [ClawHub 技能页面](https://clawhub.ai/youteacher/skills/product-catalog)

## Skill Output:

**Output Type(s):** [PDF catalogs, PNG page previews, JSON and CSV data, ZIP delivery packages, User-facing guidance]

**Output Format:** [PDF, PNG, JSON, CSV, ZIP, and concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires human review of product facts, image mapping, translations, prices, and applicable fees; generated projects and delivery files are retained for 30 days.]

## Skill Version(s):

1.1.0 (source: metadata.packageVersion)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
