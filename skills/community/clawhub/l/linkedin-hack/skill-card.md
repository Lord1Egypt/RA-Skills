## Description:

Tinker LinkedIn lets an agent crawl LinkedIn profiles, search results, connections, inbox, and feed through a user-shared signed-in LinkedIn browser tab while keeping cookies in the browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent inspect LinkedIn account and third-party profile data through a shared browser session for profile research, inbox review, feed inspection, and drafting outreach. Message sending requires exact per-action consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates a LinkedIn tab signed in as the user and can read account and third-party profile data.

Mitigation: Install and run it only when the user is comfortable letting an agent operate the shared signed-in LinkedIn tab.

Risk: The skill can send a LinkedIn message when the exact per-message consent flag is provided.

Mitigation: Require the exact conversation URN in the consent flag and review drafts before allowing message-send.

Risk: LinkedIn automation may violate LinkedIn rules or create account-restriction risk.

Mitigation: Use conservative limits, keep the user present, and avoid unsupported bulk outreach or rate-limit bypass behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/globalcaos/skills/linkedin-hack)
- [TinkerClaw repository](https://github.com/globalcaos/tinkerclaw)
- [LinkedIn session settings](https://www.linkedin.com/psettings/sessions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance and terminal text from LinkedIn crawl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a shared linkedin.com tab, loopback browser relay, daily request ceilings, and exact per-action consent for message-send.]

## Skill Version(s):

1.2.2 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
