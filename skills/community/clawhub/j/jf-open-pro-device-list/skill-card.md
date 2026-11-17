## Description:

Queries JFTech developer-account device lists with pagination and optional device serial-number filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to list devices bound to a JFTech open-platform account, either page by page or by supplying specific device serial numbers.

### Deployment Geography for Use:

Global, with documented JFTech API endpoints for China Mainland, Asia, Europe, and North America.

## Known Risks and Mitigations:

Risk: Routine runs may expose device login tokens or full device credential fields in logs or transcripts.

Mitigation: Run only in trusted agent sessions, avoid sharing transcripts that contain device output, and prefer a version or wrapper that redacts password and loginToken fields by default.

Risk: The skill can send signed account requests to an arbitrary host when JF_ENDPOINT is changed.

Mitigation: Use only trusted JFTech endpoints and restrict or review JF_ENDPOINT before execution.

## Reference(s):

- [JFTech Open Platform Documentation](https://docs.jftech.com)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text, table, or JSON device-list output with Markdown usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JFTech account credentials and can include device identifiers, usernames, passwords, or login tokens in command output.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter metadata says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
