## Description:

Help users build a personal knowledge base by organizing whatever they send into structured notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

People who capture personal notes, links, questions, quotes, and ideas use this skill to turn loose input into a portable Markdown knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores user-provided material in a persistent local Markdown folder.

Mitigation: Confirm the target folder before first use and keep backups for important notes.

Risk: Fetching links can expose the requested URL to external sites and may capture inaccurate page summaries.

Mitigation: Ask for confirmation before fetching links and keep the original source URL with each saved summary.

Risk: Processed inbox items may be removed after conversion into notes.

Mitigation: Review converted notes before deleting inbox entries.

## Reference(s):

- [Personal Knowledge Base on ClawHub](https://clawhub.ai/ivangdavila/skills/pkm)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown notes and concise guidance, with filenames, links, tags, and occasional shell commands when useful.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Markdown files under ~/kb/ when the agent has filesystem access and user approval.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
