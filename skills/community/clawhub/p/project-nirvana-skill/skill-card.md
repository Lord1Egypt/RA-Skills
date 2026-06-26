## Description: <br>
Nirvana Skill strips SOUL, USER, MEMORY, and chat history before cloud API calls for OpenClaw agents that use a local LLM first. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shivaclaw](https://clawhub.ai/user/shivaclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using OpenClaw agents with a local LLM use this skill to route prompts locally first and strip private context before optional cloud fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud fallback may send sanitized prompts outside the local environment despite the skill's privacy goals. <br>
Mitigation: Disable cloud fallback for highly sensitive work unless it is explicitly needed and approved. <br>
Risk: Audit logs and cached responses may retain sensitive workflow details if storage, deletion, or verbose logging behavior is not reviewed. <br>
Mitigation: Verify where logs and cached responses are stored, how they are deleted, and whether verbose prompt logging can be turned off. <br>
Risk: The security scan flagged mismatched install details and recommends confirming the exact package and publisher before installation. <br>
Mitigation: Confirm the ClawHub package slug and publisher handle before installing or deploying the skill. <br>


## Reference(s): <br>
- [Nirvana Skill ClawHub Page](https://clawhub.ai/shivaclaw/project-nirvana-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/shivaclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an existing local LLM endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
