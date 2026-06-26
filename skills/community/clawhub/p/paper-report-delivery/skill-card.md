## Description: <br>
Build, automate, or maintain a daily paper-report delivery pipeline that collects papers, selects A/B groups, generates Chinese summaries and detailed innovation analysis, produces readable HTML with embedded images, prepares Telegram message chunks, archives outputs, and delivers reports to Telegram with retry and HTML-then-fallback behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FanWu-fan](https://clawhub.ai/user/FanWu-fan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement or maintain daily paper and news digest workflows that generate readable HTML, Telegram-ready text chunks, local archives, and resilient Telegram delivery with fallback behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image metadata can cause local files to be embedded into generated HTML and sent through Telegram. <br>
Mitigation: Run only on trusted report metadata, restrict image_path values to known asset directories with real image MIME types, and inspect generated HTML before sending. <br>
Risk: Telegram delivery can send report artifacts to an unintended destination if the target is not configured deliberately. <br>
Mitigation: Set an explicit Telegram target, keep delivery settings configurable, and avoid hard-coded chat ids or group names. <br>
Risk: Running the workflow in a directory with sensitive files increases the impact of unintended file embedding. <br>
Mitigation: Run in a scoped workspace that contains only expected report inputs and generated artifacts until file-embedding behavior is constrained. <br>


## Reference(s): <br>
- [Paper Report Delivery Workflow](references/workflow.md) <br>
- [ClawHub skill page](https://clawhub.ai/FanWu-fan/paper-report-delivery) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with code, shell commands, configuration notes, and generated report artifacts such as HTML, JSON, text, Markdown, and PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local report artifacts and Telegram delivery payloads; supports HTML-first delivery with text fallback.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
