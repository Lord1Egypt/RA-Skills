## Description:

Search the web using the Perplexity Agent API to provide real-time information, news, and grounded answers with citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidsteelerose](https://clawhub.ai/user/davidsteelerose)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route current-events, web research, and real-time information requests through Perplexity and return grounded answers with citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and prompts are sent to Perplexity when the skill is used.

Mitigation: Avoid private or sensitive queries unless sharing them with the Perplexity provider fits the user's data-sharing expectations.

Risk: The skill requires a Perplexity API key in the runtime environment.

Mitigation: Store the API key in an environment variable and avoid exposing it in prompts, logs, source files, or shared transcripts.

## Reference(s):

- [Perplexity Agent API endpoint](https://api.perplexity.ai/v1/agent)
- [ClawHub skill page](https://clawhub.ai/davidsteelerose/skills/perplexity-agent)
- [Publisher profile](https://clawhub.ai/user/davidsteelerose)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [JSON response containing success status, answer text, and model metadata, usually summarized to the user as Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PERPLEXITY_API_KEY and sends the user's search query to Perplexity.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
