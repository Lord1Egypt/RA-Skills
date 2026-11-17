## Description:

Hamibot guides agents working with the Hamibot CLI, an open-source Node.js command-line tool for authorized remote Android automation on a user's authenticated and paired devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hamibot](https://clawhub.ai/user/hamibot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to install, authenticate, and operate the Hamibot CLI for authorized Android device automation. It supports tasks such as executing scripts, managing files, simulating touch input, capturing screenshots, launching apps, and querying paired device information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable remote code for a CLI that can control paired Android devices.

Mitigation: Review the upstream Hamibot CLI before installing, prefer a pinned trusted release or commit, avoid elevated privileges, and use tokens or device-control commands only for devices the user owns or is explicitly authorized to manage.

## Reference(s):

- [Hamibot official site](https://hamibot.com)
- [Hamibot CLI repository](https://github.com/hamibot/cli)
- [Hamibot account tokens](https://hamibot.com/account/tokens)
- [ClawHub skill page](https://clawhub.ai/hamibot/skills/hamibot)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI command examples, authentication steps, device-selection guidance, and JSON-output usage notes.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
