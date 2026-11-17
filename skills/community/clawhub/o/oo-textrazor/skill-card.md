## Description:

Use the OOMOL-connected oo CLI to analyze TextRazor content, extract entities, classify text, inspect account quota, and manage custom classifiers or dictionaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to run supported TextRazor actions through an OOMOL-connected account. It supports text analysis, classification, entity extraction, account information, and custom classifier or dictionary management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs downloaded code that has not been verified.

Mitigation: Use a reviewed, pinned CLI build before setup.

Risk: The linked CLI may change other agents’ installed skills through automatic synchronization.

Mitigation: Verify automatic skill synchronization is disabled if those changes are not wanted, and require explicit approval for deletions and overwrites.

Risk: Submitted text passes through OOMOL to TextRazor.

Mitigation: Send only text that is permitted to be processed by both services.

## Reference(s):

- [TextRazor API Documentation](https://www.textrazor.com/docs/rest)
- [TextRazor](https://www.textrazor.com)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and concise text or Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that change or delete data require confirmation; results depend on the connected TextRazor account.]

## Skill Version(s):

1.0.6 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
