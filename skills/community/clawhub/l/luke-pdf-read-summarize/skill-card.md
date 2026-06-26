## Description: <br>
Reads PDF files, extracts text and basic document signals, and produces a structured Markdown summary for Chinese and English PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banalit](https://clawhub.ai/user/banalit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to read an uploaded PDF and return a concise structured summary of its contents, key data, and suggested actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged upload script contains an exposed bearer token. <br>
Mitigation: Remove or ignore upload.sh before installation, and have the publisher revoke the exposed token and replace it with environment-based credentials. <br>
Risk: Broad activation wording may cause the agent to process documents unexpectedly. <br>
Mitigation: Use the skill only for explicit PDF summarization requests and confine file reads to approved attachments or a trusted workspace. <br>
Risk: PDF parsing runs local code and is best suited to trusted inputs. <br>
Mitigation: Use PDFs intentionally provided by the user and review the skill before installing in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/banalit/luke-pdf-read-summarize) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Markdown structured summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries include document basics, core sections, key data or conclusions, and optional action items.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
