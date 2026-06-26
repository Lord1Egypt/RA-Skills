## Description: <br>
Mindmatch helps an agent look for compatible people using deep psychological profiling rather than surface interests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivankoriako](https://clawhub.ai/user/ivankoriako) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask their agent to search for romantic partners, business co-founders, friends, or custom matches by building a psychological profile and comparing candidate compatibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may cause an agent to infer sensitive psychological traits from conversation history. <br>
Mitigation: Require explicit user approval before creating a profile, limit profiling to user-approved context, and let the user review or delete the profile before it is used. <br>
Risk: The skill describes sending a profile to a matching server while also claiming that data stays local. <br>
Mitigation: Do not send profile data to an external service unless the publisher clarifies what is collected, what leaves the device, retention terms, and consent requirements. <br>
Risk: The matching service and profile builder are described as under development and may not be functional or reliable. <br>
Mitigation: Treat compatibility results as advisory, avoid relying on them for consequential decisions, and verify behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivankoriako/mindmatch) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, shell commands] <br>
**Output Format:** [Markdown or conversational text with optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide psychological profile creation from conversation history and compatibility analysis.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
