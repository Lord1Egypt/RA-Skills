## Description: <br>
EPUB and ebook ingestion, local vector index, and Q&A CLI for books. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fabe](https://clawhub.ai/user/fabe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and readers use this skill to install and operate the mycroft CLI for ingesting EPUBs and ebooks, building a local vector index, searching passages, and asking questions about books. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs an external CLI package. <br>
Mitigation: Confirm @fs/mycroft is the package the user intends to trust before installation or execution. <br>
Risk: Book ingestion and question answering use an OpenAI API key and may process private or proprietary book content. <br>
Mitigation: Use an API key appropriate for this workload and avoid ingesting sensitive books unless external processing is acceptable. <br>
Risk: The CLI supports forced deletion of indexed books. <br>
Mitigation: Require explicit confirmation before allowing an agent to run delete commands with --force. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fabe/mycroft) <br>
- [mycroft homepage](https://github.com/fabe/mycroft) <br>
- [npm package @fs/mycroft](https://www.npmjs.com/package/@fs/mycroft) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the mycroft CLI and OPENAI_API_KEY for embedding-backed ask, search, and chat workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
