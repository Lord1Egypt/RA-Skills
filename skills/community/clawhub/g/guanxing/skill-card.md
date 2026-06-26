## Description: <br>
Chinese metaphysics AI for BaZi, daily fortune, crypto fortune, Feng Shui, Tarot, I-Ching divination, dream interpretation, name scoring, compatibility matching, and zodiac analysis powered by the GuanXing API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doggychip](https://clawhub.ai/user/doggychip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to call the GuanXing API for Chinese metaphysics readings, including birth-chart analysis, daily fortune, crypto fortune, Feng Shui, Tarot, I-Ching divination, dream interpretation, name scoring, compatibility, and zodiac readings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send sensitive personal details, including names, birth dates, birth hours, dreams, relationship details, and personal questions, to heartai.zeabur.app. <br>
Mitigation: Confirm with the user before sending sensitive details and avoid submitting information the user does not want shared with the GuanXing service. <br>
Risk: The skill depends on the GUANXING_API_KEY credential for API access. <br>
Mitigation: Store GUANXING_API_KEY as a private environment variable and do not paste or log the key in chat transcripts, command output, or shared configuration. <br>


## Reference(s): <br>
- [GuanXing Web App and API](https://heartai.zeabur.app) <br>
- [ClawHub Skill Page](https://clawhub.ai/doggychip/guanxing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses GUANXING_API_KEY and sends user-provided request details to the GuanXing API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
