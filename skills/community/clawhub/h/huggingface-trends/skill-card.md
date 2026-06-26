## Description: <br>
Monitor and fetch trending models from Hugging Face with support for filtering by task, library, and popularity metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianxingleo](https://clawhub.ai/user/tianxingleo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and AI practitioners use this skill to discover, compare, and monitor popular Hugging Face models by task, library, likes, downloads, or creation date. It supports command-line use, formatted summaries, and optional JSON export for follow-on analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Hugging Face for public model metadata and may use an HTTP proxy. <br>
Mitigation: Use a trusted proxy or omit the proxy when direct network access works. <br>
Risk: Optional JSON export writes to a user-selected path and may overwrite an existing file. <br>
Mitigation: Choose output paths deliberately and review them before running exports. <br>
Risk: The cron example creates recurring background network requests and log files. <br>
Mitigation: Install scheduled jobs only when daily monitoring is intended and logs are acceptable. <br>


## Reference(s): <br>
- [Hugging Face model metadata documentation](https://huggingface.co/docs/huggingface_hub/guides/models) <br>
- [Hugging Face models API](https://huggingface.co/api) <br>
- [ClawHub skill page](https://clawhub.ai/tianxingleo/huggingface-trends) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, JSON] <br>
**Output Format:** [Formatted terminal text with optional JSON files and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include model identifiers, likes, downloads, task, library, and date metadata when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
