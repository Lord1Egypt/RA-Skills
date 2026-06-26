## Description: <br>
Pull daily Gumroad product/sales analytics safely (no raw PII persistence by default). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vladchatware](https://clawhub.ai/user/vladchatware) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and creators use this skill to let an agent collect Gumroad sales and product metrics, produce daily revenue and count summaries, and optionally preserve redacted raw API responses for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a Gumroad access token and uses it to fetch sales and product data. <br>
Mitigation: Keep the credentials file private, restrict file permissions, and prefer a dedicated or revocable token. <br>
Risk: Using --store-raw can retain detailed Gumroad API responses locally. <br>
Mitigation: Use the default summary-only mode unless raw local records are required; review stored files before sharing or syncing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vladchatware/gumroad-analytics) <br>
- [Gumroad API endpoint](https://api.gumroad.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON metric files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily summary JSON by default; raw Gumroad API files are written only when explicitly requested, with sales fields redacted.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
