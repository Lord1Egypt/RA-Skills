## Description:

Novelty Validator helps users assess whether meeting or brainstorm ideas, methods, or research directions are already covered by prior literature, patents, or related work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-levee](https://clawhub.ai/user/j-levee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research teams use this skill during or after academic meetings to turn a discussed idea into a structured claim, compare it against prior work, and receive a novelty report with evidence and differentiation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive meeting transcripts, unpublished research ideas, and participant-related information.

Mitigation: Use only transcripts and meeting data the user is authorized to access, and avoid confidential or unpublished work unless the organization has approved the data flow.

Risk: Remote embedding or literature-search services can transmit research claims outside the local environment.

Mitigation: Use approved providers and endpoints for confidential work, or fall back to local/offline comparison when external transmission is not approved.

Risk: Participant attribution, contact lookup, or recording controls can create consent and privacy issues.

Mitigation: Confirm every affected participant has authorized the relevant meeting access, recording, attribution, and contact lookup before using those features.

Risk: Default local retention of method-level tags can be inappropriate for sensitive projects.

Mitigation: Disable or clear local retention for sensitive projects and document when retention is active.

## Reference(s):

- [Idea extraction](references/idea-extraction.md)
- [Novelty rubric and multi-agent workflow](references/novelty-rubric.md)
- [Vector Recall Refinement](references/vector_recall.md)
- [Innovation-path engine](references/innovation_path.md)
- [Case Library](references/case_library.md)
- [Vector Recall implementation](references/vector_recall_impl.py)
- [SiliconFlow embeddings API](https://api.siliconflow.cn/v1/embeddings)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with structured evidence tables and inline shell/API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Novelty reports should include confidence, evidence strength, cited prior work, and clear limits on what the search can prove.]

## Skill Version(s):

1.7.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
