## Description:

Newspaper/magazine PDF download skill that lets an agent query collected publication updates, locate specific issues, and return PDF download links when an Import Token is configured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1787812757](https://clawhub.ai/user/1787812757)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users on supported agent platforms use this skill to check recent newspaper and magazine updates, resolve named issues by date, and retrieve PDF download links from pick-read.vip when an Import Token is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured Import Tokens can appear in returned download links, logs, and saved result files.

Mitigation: Treat generated download URLs as secrets, avoid sharing outputs, use --no-save where possible, and rotate any token that may have been exposed.

Risk: The runtime uses insecure TLS behavior for outbound requests.

Mitigation: Use only in trusted environments and prefer a version that redacts tokens and uses normal verified HTTPS before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1787812757/skills/newspaper-download-skill)
- [Publisher profile](https://clawhub.ai/user/1787812757)
- [pick-read.vip](https://pick-read.vip)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, download links]

**Output Format:** [Markdown or plain text with CLI JSON results and PDF download URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save JSON result files unless --no-save is used; generated download URLs can include Import Tokens.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
