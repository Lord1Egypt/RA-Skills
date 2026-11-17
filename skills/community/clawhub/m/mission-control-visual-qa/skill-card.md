## Description:

Run Mission Control visual QA over SSH using Puppeteer screenshots and basic DOM checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highlander89](https://clawhub.ai/user/highlander89)

### License/Terms of Use:


## Use Case:

Developers, QA engineers, and operators use this skill to run authorized visual checks for Mission Control pages on a controlled remote host. It captures screenshots and reports basic DOM checks for supplied URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs commands on a remote machine over SSH.

Mitigation: Use a dedicated low-privilege remote account and restrict SSH access to approved Mission Control hosts.

Risk: The runner opens user-supplied URLs.

Mitigation: Run it only against authorized Mission Control pages and avoid attacker-controlled URLs.

Risk: Screenshots and summaries may contain sensitive operational UI data.

Mitigation: Keep OUTPUT_DIR and REMOTE_RUN_DIR fixed to controlled paths and handle generated artifacts as sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/highlander89/skills/mission-control-visual-qa)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance for the agent; runtime output is PNG screenshots and a JSON summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured SSH target plus Puppeteer and Chromium on the remote host.]

## Skill Version(s):

0.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
