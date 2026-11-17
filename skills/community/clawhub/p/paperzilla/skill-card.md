## Description:

Use the Paperzilla CLI (pz) to browse research projects and feeds, inspect canonical papers and project recommendations, leave feedback, export JSON, and generate Atom feed URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pors](https://clawhub.ai/user/pors)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research operations users use this skill to run the Paperzilla CLI for browsing project feeds, inspecting canonical papers and project recommendations, recording feedback, exporting structured JSON, and generating Atom feed URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Linux install and update steps use a latest release download and system-wide installation path that users should review before execution.

Mitigation: Install only if the Paperzilla release source is trusted; prefer Homebrew or Scoop where appropriate, or use a pinned release with checksum or signature verification and a user-owned bin directory.

## Reference(s):

- [Paperzilla CLI Docs](https://docs.paperzilla.ai/guides/cli)
- [Paperzilla CLI Quickstart](https://docs.paperzilla.ai/guides/cli-getting-started)
- [Paperzilla Skill Page](https://clawhub.ai/pors/skills/paperzilla)
- [Paperzilla CLI Repository](https://github.com/paperzilla-ai/pz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance prefers structured JSON output from pz when an agent needs machine-readable results.]

## Skill Version(s):

0.3.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
