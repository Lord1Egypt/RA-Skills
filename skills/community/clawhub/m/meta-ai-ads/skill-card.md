## Description: <br>
Create and manage Meta (Facebook & Instagram) ad campaigns, lead forms, audiences, pixels, and product catalogs via the Plai API, including OAuth account connection for Facebook, Instagram, and Google Ads accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arsalan98m](https://clawhub.ai/user/arsalan98m) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect ad accounts and manage Meta advertising workflows through Plai, including campaign creation, reporting, lead forms, audiences, media, pixels, and catalogs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use sensitive credentials and OAuth-connected advertising accounts. <br>
Mitigation: Install only when the user trusts Plai, keep credentials in environment variables, and revoke connected Meta or Google account access after use when appropriate. <br>
Risk: The skill can create, activate, delete, and change budgets for live advertising campaigns. <br>
Mitigation: Require explicit user approval before campaign activation, deletion, creation, or budget changes. <br>
Risk: Changing PLAI_BASE_URL can route requests to an unintended endpoint. <br>
Mitigation: Keep PLAI_BASE_URL unset unless intentionally using a trusted Plai endpoint. <br>


## Reference(s): <br>
- [Plai](https://plai.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/arsalan98m/meta-ai-ads) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and the PLAI_API_KEY and PLAI_USER_ID environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
