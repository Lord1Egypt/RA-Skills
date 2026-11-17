## Description:

知识拓展笔记术 (Knowledge Expansion Notetaking, KEN) turns a newly shared concept, method, or piece of knowledge into a structured deep-note with source context, concept analysis, applicability boundaries, ambiguity checks, follow-up questions, AI continuation, and synchronized archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binhuatochina](https://clawhub.ai/user/binhuatochina)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal knowledge workers use this skill to convert newly encountered knowledge into reusable notes with definitions, limits, misunderstandings, deeper questions, and concise AI-written expansion. It also prepares archive outputs for Get notes, Feishu Knowledge Base, Feishu Docs, and local fallback storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can archive user-provided note content to Get notes, Feishu Knowledge Base, Feishu Docs, and local storage.

Mitigation: Use it only when that sync is intended, require confirmation before external archive actions, and restrict activation triggers to deliberate user requests.

Risk: Created Feishu documents grant full_access to a fixed user account.

Mitigation: Remove or parameterize the fixed recipient before use and grant only the minimum permission needed for the intended workspace.

Risk: Generated titles, filenames, and XML document content are derived from user-supplied knowledge text.

Mitigation: Sanitize titles and filenames and XML-escape generated content before writing files or executing Feishu update commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binhuatochina/skills/knowledge-expansion-notetaking)
- [Feishu knowledge base configuration](references/feishu-kb-config.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown note content with Feishu XML update guidance, shell command snippets, archive status links, and a short finding summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [AI continuation is capped at 800 Chinese characters; archive behavior targets configured Get and Feishu destinations plus local fallback storage.]

## Skill Version(s):

0.4.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
