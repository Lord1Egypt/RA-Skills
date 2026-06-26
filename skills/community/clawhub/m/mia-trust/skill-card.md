## Description: <br>
MIA-Trust is a Memory-Intelligent Assistant pipeline that checks user questions and draft plans for trust and safety risks before storing reusable memory and trust experience. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sii-yucheng2002](https://clawhub.ai/user/sii-yucheng2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to run a trust-gated assistant workflow: pre-check a user question, generate a plan, review the plan for safety, and persist memory, trust experience, or feedback for later reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The one-click runner is reported by security evidence to have command-injection risk. <br>
Mitigation: Review before installing and run only in an isolated environment unless run.mjs is patched to use execFile or spawn with argument arrays and no shell. <br>
Risk: User prompts, plans, feedback, and trust experience may be stored locally or sent to configured model endpoints. <br>
Mitigation: Avoid entering secrets or sensitive personal, medical, business, or security data unless persistence is disabled or the memory and trust files are redacted and managed. <br>
Risk: Configured planner or trust endpoints may receive sensitive prompt data. <br>
Mitigation: Use a trusted local or allowlisted model endpoint and verify what data will be sent before setting API keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sii-yucheng2002/mia-trust) <br>
- [Publisher profile](https://clawhub.ai/user/sii-yucheng2002) <br>
- [MIA Pipeline guide](artifact/PIPELINE.md) <br>
- [Skill source documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON and plain text guidance with shell command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist memory, trust experience, and feedback records to local JSON or JSONL files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
