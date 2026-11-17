## Description:

MuMu AI Novel helps an agent create or bind a novel project, generate chapter batches, audit plot consistency with RAG, and review or rewrite chapters for Chinese fiction workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crypto-2042](https://clawhub.ai/user/crypto-2042)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and writing agents use this skill to manage a MuMu novel project lifecycle: initialize or bind a project, create outlines and chapter slots, trigger generation, inspect drafts, analyze chapters for lore consistency, and publish approved rewrites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overwrite or publish chapters through approve and rewrite commands.

Mitigation: Review target chapter IDs and rewritten content before running approve or rewrite actions.

Risk: API authentication and session handling are under-protected for shared or untrusted environments.

Mitigation: Use a trusted MuMu API endpoint, prefer HTTPS for non-local endpoints, configure explicit credentials, and avoid shared session files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crypto-2042/skills/mumuai-novel-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and script-generated text or JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MuMu API endpoint credentials and explicit project_id and optional style_id values for project-bound operations.]

## Skill Version(s):

1.0.6 (source: release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
