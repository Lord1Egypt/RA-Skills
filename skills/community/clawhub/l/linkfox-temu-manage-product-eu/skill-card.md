## Description: <br>
Helps agents use LinkFox gateway scripts and references for Temu Partner EU product management APIs, including product queries, SKU queries, edits, deletion, stock and sale status changes, compliance edits, category checks, attributes, external codes, and video cover image workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operators, and developers use this skill to manage live Temu EU product catalog data through LinkFox-mediated Partner EU APIs. It supports operational workflows such as finding products, reading details, updating listings, changing stock or sale status, deleting goods, and editing compliance information. <br>

### Deployment Geography for Use: <br>
Europe <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate on live Temu EU product data and perform destructive or business-impacting actions such as deletion, full product updates, stock changes, sale status changes, and compliance edits. <br>
Mitigation: Require explicit human confirmation before executing those actions, and review the target goods IDs, request payloads, and intended site before running commands. <br>
Risk: The skill handles sensitive LinkFox and Temu credentials, and locally saved tokens may be weakly protected. <br>
Mitigation: Prefer short-lived tokens supplied only when needed, avoid local token storage on shared or unprotected machines, and rotate credentials after operational use. <br>
Risk: Generic proxy and file-download helpers can be used beyond the narrow Manage Product workflow. <br>
Mitigation: Use the specific EU product-management scripts where possible and avoid running proxy or file-download helpers for unrelated API types. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-temu-manage-product-eu) <br>
- [API reference](artifact/references/api.md) <br>
- [Access token guide](artifact/references/access-token.md) <br>
- [Partner EU catalog](artifact/references/partner-eu-catalog.md) <br>
- [Manage Product API index](artifact/references/apis/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that call live LinkFox and Temu endpoints when the user supplies credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
