## Description: <br>
Fetches real-time Hugging Face trending data via the public HF-Mirror API and generates structured Markdown reports in English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ddongcui](https://clawhub.ai/user/ddongcui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and conversational AI users use this skill to fetch current HF-Mirror trending models, datasets, and Spaces and turn them into an English Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes an outbound request to hf-mirror.com to fetch public trending data. <br>
Mitigation: Run it only when that network access is expected and permitted. <br>
Risk: The script can write a Markdown report to the current working directory or a caller-provided path. <br>
Mitigation: Provide an explicit output path when the destination matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ddongcui/hfmirror-trending-en) <br>
- [HF-Mirror trending API](https://hf-mirror.com/api/trending) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with tables for trending models, datasets, and Spaces] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local Markdown file such as trending_summary.md when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
