## Description: <br>
Generic multi-agent content pipeline - sequential and parallel agent stages with status tracking, error recovery, and progress callbacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design multi-stage agent workflows that generate, validate, transform, and deliver content while tracking status and handling stage failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is presented as a generic no-network pipeline, while the bundled code includes a specialized voice and story API that can send audio and text to external providers and store user content. <br>
Mitigation: Review the bundled code, provider terms, API key handling, database/cache behavior, and privacy implications before enabling the skill. <br>
Risk: The included voice and story flow can process audio and child-related content. <br>
Mitigation: Use it only in environments with appropriate consent, retention, and privacy controls for the data being processed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/multi-agent-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown guidance with Python code examples and source files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Status callbacks, retry behavior, caching guidance, and optional API-backed pipeline stages depend on the stage functions a user provides.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
