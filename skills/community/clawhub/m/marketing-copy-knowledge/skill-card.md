## Description: <br>
Marketing Copy Knowledge helps agents generate Meta Ads, Google Ads, and social post copy using a FABE x SPIN marketing knowledge base by 邱煜庭（小黑老師）, with freemium and paid API-key usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[backtrue](https://clawhub.ai/user/backtrue) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to request marketing-copy generation or query a curated FABE x SPIN knowledge base for Meta Ads, Google Ads, and social posts. It is intended for non-sensitive marketing prompts and product descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketing prompts, product descriptions, or user-provided context may be sent to a third-party service. <br>
Mitigation: Use only non-sensitive marketing content; do not send secrets, credentials, private customer data, raw payment details, or other confidential material. <br>
Risk: The paid flow can purchase credits and use an API key. <br>
Mitigation: Require explicit operator authorization before purchase, keep payment details out of prompts, and protect any issued X-Api-Key as a credential. <br>
Risk: Generated marketing copy or knowledge chunks may be inaccurate, misleading, or unsuitable for a regulated campaign. <br>
Mitigation: Review generated copy before publication and use returned attribution fields when citing the knowledge source. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/backtrue/marketing-copy-knowledge) <br>
- [Publisher Profile](https://clawhub.ai/user/backtrue) <br>
- [Think with Black Homepage](https://thinkwithblack.com) <br>
- [FABE x SPIN Book Page](https://fabe.thinkwithblack.com/) <br>
- [Service OpenAPI Specification](https://toldyou-lobstermind.backtrue.workers.dev/openapi.json) <br>
- [Service llms.txt](https://toldyou-lobstermind.backtrue.workers.dev/llms.txt) <br>
- [MCP Server Card](https://toldyou-lobstermind.backtrue.workers.dev/.well-known/mcp/server-card.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with REST examples; service responses return marketing copy or attributed knowledge chunks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a third-party service; paid generation can require an X-Api-Key.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
