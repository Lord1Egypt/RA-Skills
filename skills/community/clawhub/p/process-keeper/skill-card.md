## Description:

Backfill project timelines, capture key decisions and fixes, and extract reusable process notes from development work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiyan521](https://clawhub.ai/user/shiyan521)

### License/Terms of Use:

MIT

## Use Case:

Developers and repo-aware agent users use this skill to reconstruct project history, record key decisions and fixes, and produce compact process notes or retrospective material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated process notes may expose private project names, private paths, or internal-only details if reused publicly.

Mitigation: Review notes before sharing and keep public output free of private project names, private paths, and internal-only notes.

Risk: Implicit invocation may update process documentation when the user did not intend automatic process-log maintenance.

Mitigation: Prefer explicit invocation on sensitive projects and review generated notes before committing or publishing them.

## Reference(s):

- [Process Guide](PROCESS_GUIDE.md)
- [Example Prompts](references/examples.md)
- [Process Entry Template](references/process-template.md)
- [ClawHub Skill Page](https://clawhub.ai/shiyan521/skills/process-keeper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown process entries, timelines, summaries, outlines, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update compact process notes such as docs/process/HISTORY.md when the user asks to save them.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
