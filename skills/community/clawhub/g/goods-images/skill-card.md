## Description: <br>
Use when the user wants to generate product detail images or carousel/main images for e-commerce platforms like Taobao. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[briefness](https://clawhub.ai/user/briefness) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, sellers, and e-commerce operators use this skill to turn product photos and descriptions into product detail images and carousel images for storefront listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may save uploaded product images and generated outputs to local temporary storage. <br>
Mitigation: Avoid highly confidential unreleased product photos unless local temporary storage is acceptable, and delete /tmp/product-details/ after use when files should not remain. <br>
Risk: Generated marketing images may alter product appearance or create misleading e-commerce assets if outputs are not checked. <br>
Mitigation: Review generated images against the original product photo before publishing, especially product colors, logos, text, and promotional claims. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/briefness/goods-images) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, images, guidance] <br>
**Output Format:** [Markdown response with generated image files and optional Python/PIL or shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves generated product images and temporary working files under /tmp/product-details/ during normal operation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
