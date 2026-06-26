## Description: <br>
Automated lead generation pipeline that finds local businesses with weak/no websites, AI-generates custom demo sites, deploys to Vercel, and runs a 5-email cold outreach drip sequence via AgentMail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RazzleDazzleI](https://clawhub.ai/user/RazzleDazzleI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales operators, agencies, and developers use this skill to find local business prospects, prepare custom website demos, deploy previews, and coordinate outreach from an approval workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use sensitive third-party accounts to deploy websites and send recurring cold emails. <br>
Mitigation: Use test accounts first, least-privilege API keys, strict sending and deployment limits, and manual approval before enabling automated polling or scheduled outreach. <br>
Risk: Generated demo websites and outreach may be inaccurate, unwanted, or non-compliant for some recipients or jurisdictions. <br>
Mitigation: Review every generated website and email before sending, add unsubscribe and suppression handling, and confirm cold-email compliance for the locations being contacted. <br>
Risk: The release references an external project and dependencies that may change outside this skill card. <br>
Mitigation: Review the external repository and dependency tree before installation or production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/RazzleDazzleI/lead-gen-website-pipeline) <br>
- [Drip Sequence Reference](references/drip-sequence.md) <br>
- [Environment Variables Reference](references/env-example.md) <br>
- [Google Sheet Setup](references/google-sheet-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and generated website/outreach artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses external API credentials and can coordinate deployments, lead tracking, and recurring outreach when configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
