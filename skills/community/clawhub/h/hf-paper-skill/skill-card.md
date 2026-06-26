## Description: <br>
Fetches popular Hugging Face Papers listings, optionally translates abstracts into Chinese, and generates bilingual Markdown reports with trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[isongxw](https://clawhub.ai/user/isongxw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and AI agents use this skill to collect daily, weekly, or monthly Hugging Face Papers highlights and produce bilingual summaries for review or note-taking workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: When translation is enabled, public paper abstracts are sent to the configured DeepLX or OpenAI-compatible translation provider. <br>
Mitigation: Use a dedicated low-privilege API key, verify DEEPLX_URL and OPENAI_BASE_URL before running, or use --no-translate to avoid third-party translation calls. <br>


## Reference(s): <br>
- [Hugging Face Papers](https://huggingface.co/papers) <br>
- [Date Override Reference](references/date-override.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown report with bilingual paper summaries and local file path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local .md report under a reports/ directory when an output path is supplied.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
