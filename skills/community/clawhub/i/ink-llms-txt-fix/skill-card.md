## Description:

Check a site's published llms.txt with llms.ink, then write a corrected or new llms.txt into the repository's public directory after the user approves. Use when a site or repository owner wants a valid llms.txt; not for sites the user doesn't control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukax](https://clawhub.ai/user/lukax)

### License/Terms of Use:

MIT-0

## Use Case:

Site and repository owners use this skill to check a published llms.txt, review reported issues, and draft or update the file in the repository they maintain. It requires user approval before writing and is not intended for sites the user does not control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner notes context-pack and dependency-discovery capabilities and incomplete inspection of one referenced script, so the available security evidence is limited.

Mitigation: Review the release and decide whether its capabilities fit your use before installing it.

Risk: When configured, LLMS_INK_KEY is sent to llms.ink as a bearer token.

Mitigation: Treat the key as a secret and provide it only in an environment where sending it to llms.ink is appropriate.

Risk: A proposed llms.txt may include inaccurate descriptions or links.

Mitigation: Review the content and verify its public links before approving the repository change.

## Reference(s):

- [llms.ink workflows](https://llms.ink/workflows/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Issue summaries and an llms.txt Markdown file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The file is reviewed with the user and written only after approval.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
