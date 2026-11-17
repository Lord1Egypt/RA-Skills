## Description:

Use screenshotbase through an OOMOL-connected account to check quota or capture webpages as hosted screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other screenshotbase users can check account quota and capture webpages as hosted screenshots through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions point to remote CLI installers whose payloads are unverified.

Mitigation: Provision a reviewed CLI version yourself and check its automatic skill-synchronization behavior before use.

Risk: Creating a hosted screenshot can affect hosting, retention, and quota, despite the instructions describing untagged actions as reads.

Mitigation: Before capturing, confirm the target URL and understand the hosting, retention, and quota effects.

## Reference(s):

- [screenshotbase](https://screenshotbase.com)
- [screenshotbase authentication documentation](https://screenshotbase.com/docs/authentication)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Text, Shell commands, Guidance]

**Output Format:** [Action results and text summaries, including hosted screenshot URLs, with shell command examples in the instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshot captures return hosted URLs; results depend on the connected screenshotbase account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
