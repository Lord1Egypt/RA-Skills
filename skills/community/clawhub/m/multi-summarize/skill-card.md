## Description: <br>
Fast multi-format summarization for URLs, PDFs, videos, audio files, YouTube links, and plain text, powered by Evolink. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvoLinkAI](https://clawhub.ai/user/EvoLinkAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to summarize web pages, local documents, media transcripts, and pasted text into concise TL;DRs, key takeaways, and action items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Summarized URLs, files, transcripts, and prompts are sent to the Evolink API. <br>
Mitigation: Use the skill only for content that can be shared with Evolink, and avoid secrets or highly sensitive documents. <br>
Risk: Local file summarization can expose unintended files if the allowed directory is too broad. <br>
Mitigation: Keep SUMMARIZE_SAFE_DIR narrow and limited to files intended for summarization. <br>
Risk: EVOLINK_API_KEY is required for API access. <br>
Mitigation: Store the key securely, avoid committing it to files, and rotate it if exposure is suspected. <br>
Risk: Audio transcription uses predictable temporary filenames until the publisher changes it to a private mktemp directory. <br>
Mitigation: Avoid processing sensitive audio on shared systems and prefer isolated workspaces for transcription. <br>


## Reference(s): <br>
- [Multi Summarize on ClawHub](https://clawhub.ai/EvoLinkAI/multi-summarize) <br>
- [Evolink Claude Messages API Reference](https://docs.evolink.ai/en/api-manual/language-series/claude/claude-messages-api?utm_source=clawhub&utm_medium=skill&utm_campaign=summarize) <br>
- [Evolink API Key Signup](https://evolink.ai/signup?utm_source=github&utm_medium=skill&utm_campaign=summarize) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-formatted summary text returned by a shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVOLINK_API_KEY; optional EVOLINK_MODEL and SUMMARIZE_SAFE_DIR environment variables control model selection and local file access scope.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
