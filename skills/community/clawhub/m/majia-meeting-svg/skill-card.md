## Description: <br>
Converts meeting transcripts into phone-friendly SVG meeting-summary cards and automatically exports PNG images for sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maojiebc](https://clawhub.ai/user/maojiebc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, operators, and project teams use this skill to turn meeting transcripts or speech-to-text notes into structured visual minutes that summarize decisions, unresolved items, action owners, and milestones. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting transcripts may contain sensitive or confidential information. <br>
Mitigation: Use only with transcript content approved for local processing and sharing, and review generated SVG/PNG files before forwarding them. <br>
Risk: The converter can create files and may modify the host Python environment through a runtime pip install fallback. <br>
Mitigation: Run conversion in an isolated environment or remove the runtime install fallback; confirm output paths before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/maojiebc/majia-meeting-svg) <br>
- [Project homepage](https://github.com/maojiebc/majia-meeting-svg) <br>
- [Examples directory](https://github.com/maojiebc/majia-meeting-svg/tree/main/references/examples) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands] <br>
**Output Format:** [SVG XML, PNG image output, and a short Markdown or text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces phone-first meeting-summary cards from transcript input and may invoke a local SVG-to-PNG converter.] <br>

## Skill Version(s): <br>
1.1.11 (source: ClawHub release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
