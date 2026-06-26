## Description: <br>
Conducts a structured manuscript diagnostic interview that checks whether a manuscript's intended reader outcome is supported by concrete structural mechanisms and produces a Signal Report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jadenzbeall](https://clawhub.ai/user/jadenzbeall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and publishing teams use this skill to run a six-prompt manuscript intake that checks whether an intended reader outcome is grounded in concrete manuscript mechanisms and returns a concise Signal Report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manuscript excerpts may contain confidential or unpublished material that is sent to the configured language model provider. <br>
Mitigation: Use only material you are comfortable sharing with that provider, and apply any organizational confidentiality policies before invoking the skill. <br>
Risk: The external continuation link is a separate service with its own privacy and trust considerations. <br>
Mitigation: Review the linked service's terms and privacy posture before submitting manuscript information outside the agent environment. <br>
Risk: The scan identifies surface-level signal inconsistency and may be mistaken for a full editorial or structural evaluation. <br>
Mitigation: Treat the Signal Report as a narrow diagnostic aid and use human editorial review for deeper manuscript decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jadenzbeall/nim-signal-scan) <br>
- [NIM Signal continuation](https://nimlab.netlify.app/signal) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown diagnostic interview and Signal Report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive six-prompt intake; no files or executable code are produced.] <br>

## Skill Version(s): <br>
1.2.1 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
