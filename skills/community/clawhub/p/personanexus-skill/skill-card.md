## Description: <br>
Build structured AI agent personalities using OCEAN, DISC, and Jungian frameworks. Define traits, communication styles, guardrails, and compile to system prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcrowan3](https://clawhub.ai/user/jcrowan3) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to define, validate, scaffold, and compile structured AI agent identities into prompts and platform-specific personality files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Identity YAML and generated prompts can encode broad behavior, permissions, memory, database, voice provider, or runtime-evolution settings that may affect deployed agents. <br>
Mitigation: Review identity YAML and compiled prompts before deployment, with extra attention to fields that grant capabilities or change runtime behavior. <br>
Risk: Unpinned Python dependencies can change behavior across installations. <br>
Mitigation: Install from a trusted Python package source and pin dependency versions for production use. <br>


## Reference(s): <br>
- [PersonaNexus ClawHub Skill](https://clawhub.ai/jcrowan3/personanexus-skill) <br>
- [PersonaNexus Repository](https://github.com/PersonaNexus/personanexus) <br>
- [PersonaNexus ClawHub Skill Repository](https://github.com/PersonaNexus/personanexus-clawhub-skill.git) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [System prompts, JSON, Markdown, YAML templates, and CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are produced locally from user-provided identity YAML and selected compile targets.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
