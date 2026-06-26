## Description: <br>
Self-reflection engine for AI agents. Extracts patterns from session transcripts into a weighted graph with Hebbian learning and time decay. Compiles a token-budgeted lens of active self-knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[madebydia](https://clawhub.ai/user/madebydia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to extract recurring patterns from session transcripts, maintain persistent self-reflection memory, and compile a compact metacognition lens for future agent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent self-memory can store sensitive or incorrect behavioral guidance. <br>
Mitigation: Review generated memory and lens files before using them in agent workflows, and clear memory/metacognition.json when the retained guidance is no longer appropriate. <br>
Risk: Memory text may be sent to a configurable embeddings endpoint. <br>
Mitigation: Install only when EMBEDDINGS_URL is unset or points to a trusted local service, and verify endpoint behavior before processing sensitive transcripts. <br>
Risk: The security scan reports a mismatch between the stated localhost-only posture and implementation behavior. <br>
Mitigation: Treat the release as needing review before deployment and prefer an updated release that removes curl/subprocess and enforces localhost-only endpoints. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/madebydia/metacognition) <br>
- [Project Homepage](https://github.com/madebydia/metacognition) <br>
- [OpenClaw](https://openclaw.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and command-line output from Python CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persistent memory to memory/metacognition.json and compiles a token-budgeted lens to scripts/metacognition-lens.md.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
