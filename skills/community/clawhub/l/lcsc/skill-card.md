## Description:

通过 camoufox-cli 浏览器自动化操作立创商城，完成元器件搜索、查看详情、加入购物车、BOM 配单、PCB/SMT 下单等操作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinky-yan](https://clawhub.ai/user/sinky-yan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate LCSC/JLC storefront workflows, including component search, product-detail review, cart operations, BOM matching, PCB/SMT ordering, and order lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables purchases, order access, and design-file uploads without clear confirmation safeguards.

Mitigation: Require fresh explicit confirmation that includes destination site, files, quantities, price, shipping, and manufacturing parameters before cart changes, uploads, order access, or order placement.

Risk: Cookie import/export and JavaScript evaluation can expose sessions or perform unintended browser actions.

Mitigation: Use cookie handling or JavaScript evaluation only when the user explicitly asks for those actions and the requested scope is clear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sinky-yan/skills/lcsc)
- [Publisher profile](https://clawhub.ai/user/sinky-yan)
- [LCSC storefront](https://www.szlcsc.com/)
- [LCSC BOM page](https://bom.szlcsc.com/bom.html)
- [JLC PCB order page](https://www.jlc.com/newOrder/#/pcb/pcbPlaceOrder)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume camoufox-cli is available at /opt/homebrew/bin/camoufox-cli.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
