## Description: <br>
Persistent wiki manager based on Karpathy's LLM-Wiki pattern that builds and maintains a structured, interlinked markdown wiki from user-provided sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[john-ver](https://clawhub.ai/user/john-ver) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to initialize, ingest into, query, lint, and maintain a durable local markdown wiki from their own source material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally creates and updates persistent local wiki files, so sensitive source material or questions could be retained in the wiki. <br>
Mitigation: Choose the wiki root carefully and avoid placing secrets or highly sensitive material in sources or prompts. <br>
Risk: Durable wiki edits can overwrite, preserve, or amplify incorrect or stale information over time. <br>
Mitigation: Review generated changes, use the lint workflow for contradictions and stale claims, and keep version control or backups for the wiki. <br>


## Reference(s): <br>
- [Karpathy LLM-Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown files and concise text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local wiki files under the configured wiki root.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
