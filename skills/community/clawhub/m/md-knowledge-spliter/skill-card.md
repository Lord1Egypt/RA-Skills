## Description:

Helps agents split large Markdown knowledge documents into topic-based chunks with an index so relevant sections can be found without loading the whole file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephyb97](https://clawhub.ai/user/josephyb97)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to organize large Markdown knowledge bases into indexed, topic-focused chunks for targeted lookup and incremental maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may restructure Markdown files in broad target locations.

Mitigation: Review target paths before allowing writes and prefer documentation folders over private or sensitive directories.

Risk: Broad triggers such as loading or splitting large files could apply outside the intended knowledge-base workflow.

Mitigation: Confirm the task is documentation organization before invoking the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josephyb97/skills/md-knowledge-spliter)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown guidance and indexed Markdown file structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an INDEX.md convention and topic-based chunk files for Markdown knowledge directories.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
