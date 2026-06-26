## Description: <br>
Automatically collect and publish security guidelines and guides from KISA and Boho to Notion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rebugui](https://clawhub.ai/user/rebugui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to collect Korean security guideline posts from KISA and Boho, download related PDFs, and publish the collected material into a configured Notion database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a sibling security-news-feed module that is not part of this release artifact. <br>
Mitigation: Review and trust the referenced sibling module before installing or running this skill. <br>
Risk: The skill reads workspace environment secrets for Notion and related publishing configuration. <br>
Mitigation: Use a least-privilege Notion integration scoped only to the intended database and avoid sharing logs or screenshots that expose .env values. <br>
Risk: The artifact describes automatic LaunchAgent or cron execution. <br>
Mitigation: Run the collection and publishing flow manually first, then enable scheduling only after verifying behavior and outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rebugui/kisa-guideline-hub) <br>
- [Notion database schema for guidelines](references/schema.md) <br>
- [Example guideline publications](references/examples.md) <br>
- [KISA guideline source](https://xn--3e0b707e.xn--3e0b31i8re36g/2060207) <br>
- [Boho guideline source](https://www.boho.or.kr) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Publishes collected guideline records and PDF attachments to Notion when run with valid local dependencies and credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
