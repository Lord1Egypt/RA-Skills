## Description:

Scan markdown files and verify that hyperlinks to local files and remote URLs resolve correctly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use this skill to check README, documentation, wiki, and static-site Markdown for broken local or remote hyperlinks before publishing or release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanning untrusted Markdown can cause the checker to request internal or private network URLs.

Mitigation: Run it only on trusted documents or in a network-restricted environment unless URL target controls are added.

Risk: Local link checks can reveal whether arbitrary paths exist outside the intended documentation set.

Mitigation: Constrain scans to the intended project root and review documents before checking links from untrusted sources.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and diagnostic text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports broken links with file paths, line numbers, URLs, and failure reasons; exits nonzero when broken links are found.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
