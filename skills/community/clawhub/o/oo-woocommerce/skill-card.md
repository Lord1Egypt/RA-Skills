## Description: <br>
Use this skill for WooCommerce requests, including reading, creating, and updating store data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect WooCommerce action schemas and run connector actions for products, orders, customers, coupons, categories, tags, attributes, variations, order notes, and WordPress media uploads through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions can change WooCommerce store data, including products, orders, coupons, order notes, variations, order status, and media. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running actions tagged as write or destructive. <br>
Risk: Connector payloads can become invalid if action schemas change. <br>
Mitigation: Inspect the live WooCommerce connector schema before building and running each action payload. <br>
Risk: Use requires the oo CLI, OOMOL sign-in, and a connected WooCommerce account. <br>
Mitigation: Run setup steps only after a command fails with the matching install, authentication, connection, or billing error. <br>


## Reference(s): <br>
- [ClawHub WooCommerce skill](https://clawhub.ai/oomol/oo-woocommerce) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [WooCommerce homepage](https://woocommerce.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are expected as JSON with data and meta.executionId fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
