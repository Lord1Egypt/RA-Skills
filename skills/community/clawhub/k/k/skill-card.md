## Description:

Manage and organize local notes with categories and tags, search note content, and export knowledge in JSON or Markdown formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgta23](https://clawhub.ai/user/hgta23)

### License/Terms of Use:

MIT-0

## Use Case:

Students, professionals, creatives, researchers, and general users can use this skill through an agent to create, update, organize, search, and export personal or work notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notes are saved to a local file and may contain sensitive information.

Mitigation: Use the skill only where local note persistence is acceptable, and harden the storage path and file permissions before storing sensitive notes.

Risk: Running the skill from a shared or attacker-writable directory can expose or alter saved notes.

Mitigation: Run it from a trusted working directory and avoid shared writable locations.

## Reference(s):

- [KnowledgeKeeper Skill on ClawHub](https://clawhub.ai/hgta23/skills/k)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Plain text responses, structured note data, JSON exports, or Markdown exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists notes locally to knowledge.json in the working directory.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
