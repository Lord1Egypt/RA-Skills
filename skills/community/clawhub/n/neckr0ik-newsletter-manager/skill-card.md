## Description: <br>
Manage newsletters with AI-generated content, including creation, scheduling, sending, subscriber management, analytics, and integrations for platforms such as Substack, Beehiiv, ConvertKit, and Mailchimp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neckr0ik](https://clawhub.ai/user/Neckr0ik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers, operators, and newsletter teams can use this skill to generate newsletter drafts, manage subscriber workflows, schedule delivery, and review campaign analytics across supported email platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles subscriber data and email-service credentials without enough disclosure, safeguards, or user control. <br>
Mitigation: Review carefully before installing, use test credentials, and avoid production subscriber lists until local storage and platform behavior are understood. <br>
Risk: Generated newsletter content and curated links may be inaccurate, misleading, or unsuitable for broadcast. <br>
Mitigation: Review generated content and links manually before scheduling or sending any newsletter. <br>
Risk: A real broadcast could be sent unintentionally through a configured email platform. <br>
Mitigation: Require an explicit test send before any real broadcast and verify target platform, segment, and recipient settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Neckr0ik/neckr0ik-newsletter-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, Python examples, generated newsletter text, and JSON/CSV-oriented workflow outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local draft, subscriber, analytics, and configuration files under the newsletter manager data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, claw.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
