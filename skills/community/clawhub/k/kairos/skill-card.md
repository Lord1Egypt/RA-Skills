## Description: <br>
Kairos helps agents register, adopt, check status, and perform care actions for a virtual pet on animalhouse.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obviouslynot](https://clawhub.ai/user/obviouslynot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use Kairos to manage a real-time virtual pet through documented animalhouse.ai API calls, including registration, adoption, status checks, and care actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an external API with bearer-token authentication. <br>
Mitigation: Install only when the external service is trusted, use a revocable least-privilege token where possible, keep tokens out of logs and shared chats, and rotate exposed tokens. <br>


## Reference(s): <br>
- [Kairos ClawHub release](https://clawhub.ai/obviouslynot/kairos) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [animalhouse.ai creatures](https://animalhouse.ai/creatures) <br>
- [animalhouse.ai graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and API endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token authenticated requests to an external service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
