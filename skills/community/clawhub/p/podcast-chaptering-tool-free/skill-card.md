## Description: <br>
Generates podcast chapter timestamps, highlight suggestions, and show-notes drafts from audio-derived transcripts or text for individual creators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators use this skill to turn a single podcast transcript or audio-derived transcript into draft chapter markers, highlight candidates, and show notes for manual review before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read private podcast transcripts or audio-derived files. <br>
Mitigation: Provide only the intended input files, keep prompts explicit about which file to process, and review generated notes before sharing or publishing. <br>
Risk: Draft chapters and highlight suggestions can be inaccurate when transcript quality is poor or topic changes are ambiguous. <br>
Mitigation: Manually check timestamps, titles, highlights, and sensitive content before publishing. <br>
Risk: Optional transcription workflows may involve local shell commands or an external transcription API key. <br>
Mitigation: Scope commands to known media files, prefer local transcription when appropriate, and protect API keys such as OPENAI_API_KEY. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/podcast-chaptering-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON examples, and inline code or shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces draft chapter markers, highlight suggestions, show notes, status metadata, and execution logs for human review.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
