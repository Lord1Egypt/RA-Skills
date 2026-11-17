## Description:

Uses the Ollama Web Search API to search the web and fetch webpage content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnydou](https://clawhub.ai/user/sunnydou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to run web search queries and retrieve webpage content through Ollama-backed CLI or slash-command workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and fetch URLs are sent to Ollama.

Mitigation: Avoid using the skill for secrets, private internal URLs, regulated data, or confidential research topics.

Risk: The skill requires an Ollama API key and may expose it through local process monitoring while curl is running.

Mitigation: Use a limited, easily revocable API key and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunnydou/skills/ollama-web-search-cli)
- [Ollama Web Search API](https://docs.ollama.com/capabilities/web-search)
- [Ollama API Keys](https://ollama.com/settings/keys)
- [OpenClaw Slash Commands](https://docs.openclaw.ai/tools/slash-commands)
- [OpenClaw Web Tools](https://docs.openclaw.ai/tools/web)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI text with URLs, result summaries, fetched page excerpts, and inline shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are capped by a max_results argument from 1 to 10; fetched page content is summarized as text with a limited link list.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter and script report 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
