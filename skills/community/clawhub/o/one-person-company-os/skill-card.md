## Description: <br>
Build a visual operating cockpit for an AI-native one-person company across promise, buyer, product, delivery, cash, learning, and assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[living-hi](https://clawhub.ai/user/living-hi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External founders and operators use this skill to turn an AI product idea into a local operating workspace with a cockpit, business-loop state, editable work surfaces, formal deliverables, and visual assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes generated company files and workspace state locally. <br>
Mitigation: Use a dedicated founder-approved workspace directory and keep generated writes inside that directory. <br>
Risk: Generated business, legal, pricing, or customer-facing material could be incomplete or unsuitable for direct use. <br>
Mitigation: Review and approve generated material before publishing it, sending it to customers, changing budgets, or making legal or pricing decisions. <br>
Risk: Tool adapters such as MCP, Dify, or API hosts may expose write-capable actions. <br>
Mitigation: Require explicit user approval before invoking write operations and avoid providing unrelated credentials or secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/living-hi/one-person-company-os) <br>
- [README](artifact/README.md) <br>
- [Security Policy](artifact/SECURITY.md) <br>
- [ClawHub listing draft](artifact/release/clawhub-listing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated local workspace files, including HTML, Markdown, DOCX, SVG, JSON, and optional image prompts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Normal operation uses a founder-approved local workspace and does not require API keys or image generation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and changelog, released 2026-05-06) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
