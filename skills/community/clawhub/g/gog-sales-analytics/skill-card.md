## Description:

Automated weekly workflow that scrapes GOG store discounts, analyzes the full discounted-game dataset with Gemini, generates a markdown insights report, and syncs it to Feishu Drive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to run a recurring workflow that collects discounted GOG game data, produces Gemini-assisted deal insights, and distributes the generated report through Feishu Drive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow publishes the whole working directory after handling API keys and generated reports, creating a credible credential and data exposure risk.

Mitigation: Remove automatic publication from the recurring workflow or replace it with a separate explicit release action that uses a staged allowlist excluding .env, generated data, logs, caches, and other private files.

Risk: GOG sales data and generated reports are sent to Gemini and Feishu.

Mitigation: Use the skill only when that data sharing is acceptable for the deployment context and configured accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/gog-sales-analytics)
- [GOG discounted games listing](https://www.gog.com/en/games?priceDiscounted=true)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu Drive upload_all API](https://open.feishu.cn/open-apis/drive/v1/files/upload_all)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration]

**Output Format:** [Markdown report, JSON sales data, and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes the full discounted-game dataset and can upload the generated report to Feishu Drive when configured.]

## Skill Version(s):

1.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
