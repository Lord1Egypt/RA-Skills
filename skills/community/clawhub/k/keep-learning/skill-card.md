## Description: <br>
Learn and memorize knowledge from local directories, including Markdown and code files, by extracting key insights, building a knowledge index, and storing results in agent memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nileader](https://clawhub.ai/user/nileader) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and agent users use this skill to ingest a local knowledge base into agent memory, keep an index of supported source files, and produce a learning report for later retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and remember contents from the selected local knowledge folder. <br>
Mitigation: Use a narrow, purpose-specific directory that excludes secrets, personal files, unrelated proprietary code, and other information that should not be stored in agent memory. <br>
Risk: For git repositories, the skill may run git pull before indexing and change the local checkout. <br>
Mitigation: Confirm the target path before learning, review repository status when needed, and use a separate working copy if local changes must be isolated. <br>
Risk: Unsupported or very large files may be skipped or summarized, so memory may not contain the complete source context. <br>
Mitigation: Check the generated learning report and use the knowledge index to reopen source files for deeper review when exact details matter. <br>


## Reference(s): <br>
- [Source repository](https://github.com/nileader/keep-learning) <br>
- [ClawHub skill page](https://clawhub.ai/nileader/keep-learning) <br>
- [Memory Strategy Reference](artifact/references/MEMORY-STRATEGY.md) <br>
- [Supported File Formats](artifact/references/SUPPORTED-FORMATS.md) <br>
- [Knowledge Index Template](artifact/assets/knowledge-index-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown learning report with memory-entry summaries, knowledge-index summaries, notes, and occasional shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores selected configuration and learning state under ~/.keep-learning/ and writes learned summaries to the agent memory system when available.] <br>

## Skill Version(s): <br>
0.0.2 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
