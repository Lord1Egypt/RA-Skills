## Description: <br>
Intent inference and alignment for persistent AI agents. Classifies gaps between tasks and intentions, checks for misalignment before executing, and prevents wasted work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MouseRider](https://clawhub.ai/user/MouseRider) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to help persistent AI agents infer user intent, classify ambiguity, check for misalignment, and push back when a requested task may not serve the user's goal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Intent inference can be wrong if user profile, memory, or project context is stale or incomplete. <br>
Mitigation: Keep user profile and memory context accurate, and ask for clarification before expensive, irreversible, or high-stakes actions. <br>
Risk: The agent may over-apply pushback or intent inference when the user wants literal execution. <br>
Mitigation: Be explicit when literal execution is preferred, and use the skill's own guidance to avoid questioning every task. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/MouseRider/intention-engine) <br>
- [Nate Skelton's Intent Engineering](https://natesnewsletter.substack.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Markdown guidance and inline decision protocols] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no executable code, tool calls, credential handling, or hidden install behavior found in security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
