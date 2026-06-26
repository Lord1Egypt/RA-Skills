## Description: <br>
AI meeting assistant via ghostmeet. Start sessions, get live transcripts, and generate AI summaries from any browser meeting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Higangssh](https://clawhub.ai/user/Higangssh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and external users use this skill to work with a self-hosted Ghostmeet backend: checking health, listing meeting sessions, retrieving transcripts, and generating action-oriented meeting summaries when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting transcripts can contain sensitive information. <br>
Mitigation: Keep transcript content within the current user workflow and avoid using the skill for confidential meetings unless the local backend and extension are acceptable for that setting. <br>
Risk: Summary generation sends transcript text to Anthropic when GHOSTMEET_ANTHROPIC_KEY is configured. <br>
Mitigation: Leave GHOSTMEET_ANTHROPIC_KEY unset or skip summary generation when transcript text should not be sent to Anthropic. <br>
Risk: The skill depends on an external Ghostmeet Docker backend and a manually loaded Chrome extension. <br>
Mitigation: Review the Ghostmeet backend and extension permissions/source before use, and run the backend only in environments where that local service is expected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Higangssh/ghostmeet) <br>
- [Ghostmeet Project Repository](https://github.com/Higangssh/ghostmeet) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and local API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include meeting transcripts, summaries, action items, and troubleshooting guidance from a local Ghostmeet backend.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
