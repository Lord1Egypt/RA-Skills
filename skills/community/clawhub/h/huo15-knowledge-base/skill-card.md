## Description:

Huo15 Knowledge Base helps agents maintain an isolated Markdown knowledge base by ingesting documents, compiling raw material into wiki entries with an LLM, and searching or checking the resulting wiki.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jobzhao15](https://clawhub.ai/user/jobzhao15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create per-agent knowledge-base directories, ingest source material, compile it into human-readable Markdown wiki entries, and search or maintain the resulting knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LLM-generated filenames may allow compiled output to be written outside the intended wiki folder.

Mitigation: Validate and normalize generated filenames before writing files; reject absolute paths, parent-directory segments, and names that do not end in a safe Markdown filename.

Risk: Raw document prompts can be sent to the configured LLM endpoint.

Mitigation: Use only non-sensitive documents unless the configured local or provider endpoint is trusted for that data.

Risk: Compile and lint workflows process ingested content and can propagate unsafe or misleading content into the wiki.

Mitigation: Avoid running compile or lint on untrusted ingested content, and review generated wiki changes before relying on them.

Risk: Bulk activation creates persistent knowledge-base directories for every detected agent.

Mitigation: Run all-agent activation only when that persistent per-agent storage is intended.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, shell command output, JSON configuration, and agent-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates per-agent raw, wiki, and cache directories; LLM-backed compilation depends on the user's configured provider.]

## Skill Version(s):

0.7.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
