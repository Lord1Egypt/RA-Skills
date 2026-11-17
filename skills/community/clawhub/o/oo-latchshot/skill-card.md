## Description:

Operate Latchshot through an OOMOL-connected account, including capturing public web pages and checking usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to capture public web pages with Latchshot and check account usage through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified code and introduce broader skill changes without clear user consent.

Mitigation: Review and independently verify the CLI before allowing automatic setup; consider disabling broader skill synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: Page capture sends the selected URL through Latchshot and uploads the resulting artifact to transit storage using the connected account.

Mitigation: Confirm the capture URL and its effects before running, and use the connected account only if you trust OOMOL with the submitted data.

## Reference(s):

- [Latchshot homepage](https://latchshot.fly.dev)
- [Latchshot API documentation](https://latchshot.fly.dev/docs.md)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-latchshot)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Text]

**Output Format:** [PNG, JPEG, or PDF page captures; structured action results and usage information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Page capture uploads an artifact to transit storage.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
