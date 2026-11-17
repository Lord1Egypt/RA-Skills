## Description:

Scan and remove sensitive data before publishing skills. Detect API keys, tokens, secrets, and personal info.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalomeve](https://clawhub.ai/user/dalomeve)

### License/Terms of Use:


## Use Case:

Developers and skill publishers use this skill before publishing or pushing skill files to scan for secrets, personal information, and internal URLs, then apply targeted redactions and complete a pre-publish privacy checklist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scrubber can recursively overwrite many files in place.

Mitigation: Review the target path before execution and run only on a narrowed project directory.

Risk: The artifact claims original files are backed up, but server security evidence says that backup behavior is not implemented.

Mitigation: Create an independent backup before running any redaction workflow on a real project.

Risk: The scanner may miss some sensitive data categories.

Mitigation: Review scan results manually and supplement with additional secret scanning before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dalomeve/skills/prepublish-privacy-scrub)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Markdown]

**Output Format:** [Markdown with PowerShell code blocks and checklist content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file scanning and in-place redaction guidance; no external logging is described.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
