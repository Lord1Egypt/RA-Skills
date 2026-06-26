## Description: <br>
Delivers daily revenue cycle management intelligence, learning prompts, and industry updates with SparkChange-focused takeaways. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j3m2b](https://clawhub.ai/user/j3m2b) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations leaders and revenue cycle management learners use this skill to scan healthcare finance news, reinforce CRCR-aligned concepts, and turn daily findings into actionable briefing notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes scheduled external posting or messaging behavior. <br>
Mitigation: Require manual approval before public posts or channel messages are sent. <br>
Risk: The security evidence reports a hardcoded Moltbook API credential. <br>
Mitigation: Remove and rotate the embedded token, then use scoped credentials from an environment variable or secret store. <br>
Risk: Briefings and logs could expose PHI, patient details, or internal strategy if sensitive source material is used. <br>
Mitigation: Avoid putting PHI, patient details, or internal strategy into logs or outbound briefs. <br>


## Reference(s): <br>
- [Rcm Pulse on ClawHub](https://clawhub.ai/j3m2b/jb-rcm-pulse) <br>
- [HFMA CRCR Candidate Key Concepts Guide](https://www.hfma.org/wp-content/uploads/2024/12/crcrconceptguide3_4_24-lonestar.pdf) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown briefings and plain-text outbound messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scheduled weekday pulse that may create archive notes and prepare external posts or channel messages.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
