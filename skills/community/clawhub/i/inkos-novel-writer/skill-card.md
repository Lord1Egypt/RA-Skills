## Description: <br>
Autonomous novel writing CLI agent with a local web workbench for creative fiction writing, chapter continuation, import, style analysis, EPUB export, AIGC detection, fan fiction, multi-agent drafting, auditing, revision, analytics, and configurable LLM provider routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adchina2025](https://clawhub.ai/user/adchina2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, writers, and developers use this skill to drive InkOS for long-form fiction projects, including creating books, generating and revising chapters, importing existing drafts, managing story state, and exporting manuscripts. It is most useful when an agent needs command guidance for a project-local novel writing workflow that uses configured LLM provider credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires LLM provider credentials such as OPENAI_API_KEY, and configured providers may incur cost or expose prompts to the selected provider. <br>
Mitigation: Use a dedicated API key with spending limits and configure only trusted LLM provider endpoints. <br>
Risk: Custom OpenAI-compatible base URLs can receive the configured API key and manuscript content. <br>
Mitigation: Avoid untrusted custom base URLs; use only provider endpoints or proxies that the user controls or has audited. <br>
Risk: Bulk rewrite, rename, delete, daemon, and multi-chapter generation workflows can make large project-local manuscript changes. <br>
Mitigation: Keep projects under version control or export backups before running large automated edits or generation batches. <br>
Risk: Private manuscripts, truth files, logs, and configuration may contain sensitive creative work or credentials. <br>
Mitigation: Store projects in protected folders and keep configuration files containing keys out of shared repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adchina2025/inkos-novel-writer) <br>
- [Publisher profile](https://clawhub.ai/user/adchina2025) <br>
- [InkOS homepage](https://github.com/Narcooo/inkos) <br>
- [npm package](https://www.npmjs.com/package/@actalk/inkos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured JSON command examples where supported by InkOS.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide commands that create or edit project-local manuscript files, configuration files, logs, exports, and local web workbench sessions.] <br>

## Skill Version(s): <br>
2.3.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
