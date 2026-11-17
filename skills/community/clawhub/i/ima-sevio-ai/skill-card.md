## Description:

Generates videos with IMA Sevio 1.0 and IMA Sevio 1.0-Fast from text prompts and optional image inputs, returning video and cover URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allenfancy-gan](https://clawhub.ai/user/allenfancy-gan)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to produce Sevio model videos from text prompts, source images, first/last frames, or reference images in agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, task data, API keys, and local media may be sent to IMA services during generation and upload workflows.

Mitigation: Install only when the publisher and IMA service endpoints are trusted, use a limited-scope IMA API key when available, and avoid submitting sensitive prompts or media.

Risk: Configurable network endpoints can redirect task or upload traffic if command arguments or environment variables are untrusted.

Mitigation: Do not set --base-url or IMA_IM_BASE_URL outside trusted IMA endpoints, and avoid running the skill with untrusted command arguments or environment variables.

Risk: Preference and operational log files are written under ~/.openclaw and may remain visible on shared machines.

Mitigation: Review or remove local preferences and logs after use, especially on shared systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allenfancy-gan/skills/ima-sevio-ai)
- [ClawHub publisher profile](https://clawhub.ai/user/allenfancy-gan)
- [IMA Studio](https://imastudio.com/)
- [IMA API key management](https://www.imaclaw.ai/imaclaw/apikey)
- [IMA subscription and credits](https://www.imaclaw.ai/imaclaw/subscription)
- [IMA video creation records](https://www.imastudio.com/ai-creation/text-to-video)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [CLI status text and optional JSON containing task_id, url, cover_url, model_id, model_name, and credit.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns remote media URLs for generated videos; local preference and operational log files may be written under ~/.openclaw.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
