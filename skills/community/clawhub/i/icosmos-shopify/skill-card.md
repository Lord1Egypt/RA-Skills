## Description: <br>
Shopify 店铺运营/诊断技能：从 Supabase 拉取店铺域名与 token，做装修/产品/结账/指标异常检测，并支持发布引流博文（唯一写操作）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TaceyWong](https://clawhub.ai/user/TaceyWong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store operators, ecommerce teams, and agents use this skill to retrieve Shopify store data, run read-only diagnostics for themes, products, checkout, and metrics, and publish traffic-driving blog posts only after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for business credentials, syncs Shopify tokens, and relies on a separate local CLI for sensitive store actions. <br>
Mitigation: Install only from a trusted publisher, inspect or otherwise trust the CLI, verify credential and token cache handling, and confirm Shopify scopes before use. <br>
Risk: Publishing blog posts is a write action that can affect a live storefront. <br>
Mitigation: Manually review blog content and run publishing only with the documented explicit --confirm flag. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TaceyWong/icosmos-shopify) <br>
- [Shopify GraphQL Admin API reference](https://shopify.dev/docs/api/admin-graphql/latest) <br>
- [Shopify REST Admin API reference](https://shopify.dev/docs/api/admin-rest/latest) <br>
- [Shopify Storefront API reference](https://shopify.dev/docs/api/storefront/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON-oriented output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill recommends unified JSON output for content commands and masks sensitive fields by default.] <br>

## Skill Version(s): <br>
0.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
