## Description:

This skill helps agents search DuckDuckGo for web pages, news, images, and videos, then return results as text, Markdown, or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nyetnighy](https://clawhub.ai/user/nyetnighy)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to gather current web, news, image, and video results for research, fact-checking, monitoring, and source discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to an external DuckDuckGo-backed service and may disclose sensitive terms.

Mitigation: Avoid searching for secrets, credentials, private customer data, or confidential internal project names.

Risk: The optional --output path can overwrite files in the workspace.

Mitigation: Use deliberate output paths and review existing files before saving results.

Risk: The DuckDuckGo dependency is not pinned in the skill instructions.

Mitigation: Install the skill in a virtual environment and pin the dependency version for reproducible deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nyetnighy/skills/nyet-web-search)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, shell commands, guidance]

**Output Format:** [Plain text, Markdown, or JSON search results, with optional saved result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports web, news, image, and video search; optional filters include result count, time range, region, safe search, image attributes, and video attributes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
