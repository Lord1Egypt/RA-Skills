## Description:

Install a local OpenClaw skill from a zip file by unzipping, validating, moving it into the active Skills directory, and verifying the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leialexzhang](https://clawhub.ai/user/leialexzhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install a local skill package from a Linux-accessible ZIP into an active Skills directory, validate key files, avoid overwrite conflicts, and report the installed path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ZIP packages may contain unsafe archive entries or links that are not sufficiently validated before installation into an active Skills folder.

Mitigation: Use a hardened installer that validates archive entries before extraction, rejects links and traversal paths, enforces size and file-count limits, and stages packages in quarantine before activation.

Risk: Installing an unreviewed local package can place untrusted instructions into an active agent skills directory.

Mitigation: Review the ZIP contents yourself and require explicit confirmation before moving the extracted skill into the active Skills directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leialexzhang/skills/local-skill-installer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown status summary with command guidance as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports source zip path, extracted folder name, final installed path, validation result, conflict result, and reload or restart recommendation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
