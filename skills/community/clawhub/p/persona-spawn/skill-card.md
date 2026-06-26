## Description: <br>
Spawn subagents with personas from a local workspace library or the Emblem persona marketplace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[decentraliser](https://clawhub.ai/user/decentraliser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to prepare local persona files, assemble a deterministic persona prompt, and spawn a persona-preserving subagent for bounded tasks that benefit from a different voice, expertise, or operating style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imported persona files can influence spawned subagent behavior. <br>
Mitigation: Review imported persona files before use and prefer known local personas after import. <br>
Risk: Shared context files may disclose workspace documents to spawned subagents. <br>
Mitigation: Keep context_files pointed only at documents intended to be shared with subagents. <br>
Risk: Bootstrapping or bulk importing personas can replace or alter an existing local personas directory. <br>
Mitigation: Back up an existing personas directory before bootstrapping or bulk importing. <br>


## Reference(s): <br>
- [Emblem Persona Marketplace API](references/api-endpoints.md) <br>
- [Writing a Custom SOUL.md](references/soul-guide.md) <br>
- [Persona Spawn on ClawHub](https://clawhub.ai/decentraliser/persona-spawn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces assembled persona prompts and local persona-library setup guidance; spawned subagent output depends on the requested task.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
