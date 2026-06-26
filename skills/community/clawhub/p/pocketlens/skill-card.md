## Description: <br>
PocketLens helps agents extract expense data from receipts, card statements, and user messages, then record transactions and report spending through PocketLens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edenjw](https://clawhub.ai/user/edenjw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External PocketLens users use this skill to log financial transactions from receipt or card-statement images and natural-language entries. They can also query categories, monthly spending summaries, and card billing information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process sensitive financial images and payment metadata such as merchants, amounts, dates, and card names. <br>
Mitigation: Install only when the user trusts PocketLens and the agent image-processing path with this data. <br>
Risk: The skill can create external expense records before the user reviews extracted transactions. <br>
Mitigation: Have the agent show extracted transactions for approval before creating records in PocketLens. <br>
Risk: A broad or exposed API key can increase the impact of mistaken or unauthorized transaction creation. <br>
Mitigation: Use the least-privilege PocketLens API key available and keep POCKET_LENS_API_URL pointed at a trusted endpoint. <br>


## Reference(s): <br>
- [PocketLens](https://pocketlens.app) <br>
- [PocketLens ClawHub listing](https://clawhub.ai/edenjw/pocketlens) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and JSON arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transaction tables, spending summaries, category lists, card bill summaries, and API error guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
