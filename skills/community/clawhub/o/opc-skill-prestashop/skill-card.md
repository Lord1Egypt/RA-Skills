## Description: <br>
Transforma o agente OpenClaw em um Assistente de Vendas Virtual consultivo e persuasivo, integrado via REST API / Web Services do PrestaShop com verificacoes de estoque em tempo real e recomendacoes proativas de produtos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jorgeferro](https://clawhub.ai/user/jorgeferro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce teams and developers use this skill to let an OpenClaw agent query a PrestaShop catalog, check stock, and produce customer-facing product recommendations with alternatives when requested items are unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A PrestaShop Web Service key with broader permissions than needed could expose sensitive store capabilities beyond read-only catalog and stock lookup. <br>
Mitigation: Install only with a PrestaShop Web Service key limited to read-only catalog and stock access for the intended shop. <br>
Risk: Customer-facing recommendations can be misleading if the configured shop URL is wrong, unavailable, or returning stale product and stock data. <br>
Mitigation: Review the configured shop URL, require stock checks before presenting products, and handle API failures with a non-technical retry message. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jorgeferro/skills/opc-skill-prestashop) <br>
- [Publisher profile](https://clawhub.ai/user/jorgeferro) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown sales responses with JSON-compatible tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool results can include product names, prices, category IDs, stock quantities, short descriptions, and image URLs when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
