## Description: <br>
PocketLens helps OpenClaw users scan receipts and card payment screenshots, record transactions, list categories, and view spending or card billing summaries through PocketLens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edenjw](https://clawhub.ai/user/edenjw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to connect OpenClaw with PocketLens for personal expense tracking, receipt or card statement extraction, transaction entry, category lookup, spending summaries, and card bill checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send sensitive receipt, card statement, and spending data to PocketLens and create account records. <br>
Mitigation: Use a revocable PocketLens API key with the narrowest permission available, redact unnecessary card or account details from images, and review extracted transactions before creation. <br>
Risk: A custom POCKET_LENS_API_URL can direct PocketLens API requests away from the default service. <br>
Mitigation: Keep POCKET_LENS_API_URL unset or pointed at the official PocketLens service unless deliberately using a trusted endpoint. <br>


## Reference(s): <br>
- [PocketLens Skill README](README.md) <br>
- [PocketLens](https://pocketlens.app) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with shell commands and JSON helper-script results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responds in Korean or English to match the user; requires POCKET_LENS_API_KEY and can use an optional POCKET_LENS_API_URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
