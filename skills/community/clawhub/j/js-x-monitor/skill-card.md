## Description:

X.com account monitoring automation that periodically checks configured accounts for new tweets and sends notifications to selected messaging channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imjszhang](https://clawhub.ai/user/imjszhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor selected X.com accounts for new posts, deduplicate previously seen content, and route updates to configured notification channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notification providers can receive monitored account identifiers and tweet content.

Mitigation: Use only non-sensitive monitored accounts and notification channels that are acceptable for receiving this content.

Risk: Scheduled job management and shell handling were flagged as unsafe in the security review.

Mitigation: Review start and stop behavior before deployment, and avoid unusual account names or manual config entries until job matching and shell interpolation are narrowed.

Risk: The skill writes local configuration and state files for monitored accounts.

Mitigation: Check local file permissions and avoid storing sensitive monitoring configurations on shared machines.

## Reference(s):

- [JS X Monitor on ClawHub](https://clawhub.ai/imjszhang/skills/js-x-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local configuration and state files under the user's OpenClaw x-monitor directory when its commands are run.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
