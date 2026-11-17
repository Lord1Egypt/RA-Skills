## Description:

Prettifies, minifies, and queries JSON data with dot-path notation for API debugging, nested data cleanup, and log field extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Json Editor to format or compact JSON files and extract specific nested values while debugging APIs, cleaning configuration, or inspecting logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Promotional stdout can corrupt JSON output in pipelines or automation expecting valid JSON.

Mitigation: Review command output before automation; avoid piping it as valid JSON until the promotional line is removed or redirected to stderr.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Plain text, JSON, and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The current script appends a promotional line after command output, so stdout may not remain valid JSON.]

## Skill Version(s):

2.0.0 (source: server release, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
