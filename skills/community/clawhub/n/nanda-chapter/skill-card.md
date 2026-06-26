## Description: <br>
Register an OpenClaw agent with a NANDA chapter, submit signed intents, respond to calls, render chapter dashboards, and subscribe to the chapter event bus. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharathvc23](https://clawhub.ai/user/sharathvc23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to join NANDA chapters, maintain a local did:key identity, make signed chapter requests, view chapter dashboards, and follow chapter events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores an unencrypted local signing identity used for chapter requests. <br>
Mitigation: Protect the OpenClaw home directory, use trusted local environments, and use a runtime with stronger key protection if hardware-backed or encrypted-at-rest keys are required. <br>
Risk: Mutating actions can register identities, submit intents, respond to calls, or change subscriptions with a chapter operator. <br>
Mitigation: Review the resolved chapter URL and require explicit user confirmation before mutating actions. <br>
Risk: Submitted intents, calls, and profile details are visible to the chapter operator and may be shared according to that chapter's federation behavior. <br>
Mitigation: Avoid submitting sensitive details unless the user trusts the chapter operator and is comfortable with the chapter's sharing model. <br>


## Reference(s): <br>
- [Project NANDA](https://projectnanda.org) <br>
- [ClawHub release page](https://clawhub.ai/sharathvc23/nanda-chapter) <br>
- [Security policy](SECURITY.md) <br>
- [First introduction example](examples/first-intro.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON helper outputs and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce signed HTTPS chapter requests, rendered dashboard summaries, subscription event summaries, and local identity or audit files through helper behavior.] <br>

## Skill Version(s): <br>
0.5.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
