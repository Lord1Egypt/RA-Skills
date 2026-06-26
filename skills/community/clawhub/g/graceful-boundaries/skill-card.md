## Description: <br>
Assess API or website conformance with the Graceful Boundaries specification and provide concrete guidance or implementation changes for clearer rate-limit and error communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snapsynapse](https://clawhub.ai/user/snapsynapse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent operators use this skill to audit HTTP services for Graceful Boundaries conformance, identify gaps in structured refusals and proactive limit discovery, and implement response patterns that help agents avoid blind retries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auditing a service can send HTTP requests to the target and may be inappropriate for systems the user does not own or have permission to test. <br>
Mitigation: Run audits only against owned or authorized services, and avoid internal or sensitive network targets unless that is the intended scope. <br>
Risk: Builder-mode guidance can modify application error handling, rate-limit disclosure, and response headers. <br>
Mitigation: Review generated code changes before committing or deploying, and verify behavior against the service's actual security and operational requirements. <br>


## Reference(s): <br>
- [Graceful Boundaries ClawHub release](https://clawhub.ai/snapsynapse/graceful-boundaries) <br>
- [Graceful Boundaries specification site](https://gracefulboundaries.dev) <br>
- [Specification](artifact/spec.md) <br>
- [Implementation guide](artifact/docs/implementation-guide.md) <br>
- [curl examples](artifact/docs/curl-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include conformance findings, gap analysis, implementation snippets, and verification commands.] <br>

## Skill Version(s): <br>
1.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
