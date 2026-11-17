## Description:

Supports steel supply-demand spot information queries and bidding data retrieval for finding buyers, suppliers, tender information, and project opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyb92](https://clawhub.ai/user/wyb92)

### License/Terms of Use:

MIT-0

## Use Case:

External steel-market users and agents use this skill to classify bidding or supply-demand intent, extract query parameters, and retrieve Mysteel steel-market information for buying, selling, tender discovery, and project-opportunity workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a Mysteel API key in a plaintext project file and documents passing the key on the command line.

Mitigation: Avoid using the documented --save_api_key command with a real key unless shell history and workspace access are protected; keep references/api_key.md out of source control and shared archives, restrict file permissions, and rotate the key if exposure is possible.

Risk: Steel-market queries are sent to Mysteel APIs.

Mitigation: Use the skill only when sharing the query content with Mysteel is acceptable, and avoid submitting sensitive or unnecessary business information.

## Reference(s):

- [Intent Recognition and Parameter Extraction Guide](references/intent-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with shell command examples and summarized lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Mysteel API key; bidding lookups are limited to the most recent three calendar years.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
