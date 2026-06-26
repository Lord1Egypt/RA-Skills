## Description: <br>
Build, maintain, query, and lint a persistent Markdown knowledge wiki that sits between raw sources and final answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teki-ai](https://clawhub.ai/user/teki-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to maintain a persistent Markdown wiki for ingesting source material, answering from compiled notes, and linting wiki structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads source material and persists summaries into wiki pages, which can accidentally capture sensitive information. <br>
Mitigation: Keep the wiki in version control or review diffs, and avoid pointing the skill at folders containing secrets or sensitive source material. <br>
Risk: Wiki updates can preserve incorrect, stale, or contradictory claims if generated edits are accepted without review. <br>
Mitigation: Review changed pages, surface contradictions explicitly, and use lint checks for stale claims, weak links, duplicate pages, and schema drift. <br>


## Reference(s): <br>
- [Getting Started with an LLM Wiki](references/getting-started.md) <br>
- [Wiki Patterns Reference](references/wiki-patterns.md) <br>
- [Ingest Patterns](references/ingest-patterns.md) <br>
- [Query Patterns](references/query-patterns.md) <br>
- [Wiki Lint Checklist](references/lint-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Analysis, Guidance] <br>
**Output Format:** [Markdown pages, wiki updates, prioritized issue lists, and concise answers with citations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update wiki pages, index files, logs, source summaries, and lint reports when requested.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
