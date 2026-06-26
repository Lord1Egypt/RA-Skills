## Description: <br>
Review Responder monitors configured Google Business Profile reviews, drafts industry-aware replies, routes drafts for operator approval, and posts approved responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris-openclaw](https://clawhub.ai/user/chris-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agencies, consultants, and operators use this skill to manage Google Business Profile review replies across configured client accounts. It drafts responses with rating and industry constraints, then requires operator approval before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Google OAuth client secrets and refresh tokens locally, which can provide ongoing access to client Google Business Profile data if exposed. <br>
Mitigation: Store client JSON files outside source control with restrictive filesystem permissions or an encrypted secrets store, and maintain a token revocation and rotation plan. <br>
Risk: The included scripts can post public Google Business Profile replies and do not provide a separate technical approval check. <br>
Mitigation: Require a fresh operator approval before any reply command is run, and review the exact final reply text before publication. <br>
Risk: Regulated-industry replies can create compliance risk if drafts reference protected health information, case details, or other sensitive client information. <br>
Mitigation: Apply the medical, legal, and other industry profiles on every draft, keep regulated replies general, and have operators review drafts against their own compliance policies. <br>


## Reference(s): <br>
- [ClawHub Listing](https://clawhub.ai/chris-openclaw/google-review-responder) <br>
- [Publisher Profile](https://clawhub.ai/user/chris-openclaw) <br>
- [README](artifact/README.md) <br>
- [Setup Guide](artifact/SETUP.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>
- [Google OAuth Token Endpoint](https://oauth2.googleapis.com/token) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces draft review replies, approval prompts, pending-review summaries, and posting confirmations; public replies require operator approval before publication.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata, SKILL.md frontmatter, and CHANGELOG.md released 2026-06-08) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
