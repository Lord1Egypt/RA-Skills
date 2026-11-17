## Description:

PDF Processor extracts text from academic PDFs, detects language, translates English content into Chinese, generates concise Chinese summaries, and organizes outputs using a local Ollama model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reaperchen](https://clawhub.ai/user/reaperchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and students use this skill to process academic papers and research reports locally: extract PDF text, translate English papers into Chinese, generate concise Chinese summaries, and create a searchable paper index.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local PDF contents are sent to an Ollama service on localhost during translation and summary generation.

Mitigation: Use a dedicated local environment, avoid sensitive PDFs on shared machines, and confirm the Ollama service endpoint is local before processing.

Risk: Temporary extraction and progress files can contain document text while processing is in progress.

Mitigation: Run the skill in a controlled processing directory with appropriate file permissions and remove residual temporary files after interrupted runs.

Risk: The original PDF is moved into the completed/original folder as part of normal processing.

Mitigation: Process copies when the original file location must be preserved, or use the documented directory layout so movement is expected.

Risk: The skill can attempt to start the local Ollama service if the required model is unavailable.

Mitigation: Start and monitor Ollama manually in production-like use, and stop the service if it starts unexpectedly.

## Reference(s):

- [PDF Processing Workflow](references/workflow.md)
- [PDF Directory Structure](references/directory-structure.md)
- [Ollama](https://ollama.ai)
- [ClawHub Skill Page](https://clawhub.ai/reaperchen/skills/pdf-processor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; generated artifacts include text translations, text summaries, temporary JSON progress files, and a JSON paper index.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local PDF files and a local Ollama qwen2.5:7b service; English PDFs are translated in segments with resumable progress.]

## Skill Version(s):

2.0.0 (source: evidence release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
