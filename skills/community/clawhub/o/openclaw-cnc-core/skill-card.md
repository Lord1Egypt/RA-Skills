## Description: <br>
OpenClaw CNC Core helps agents work with CNC machining quote workflows, including STEP/STL parsing, material and time estimation, quote calculation, historical-case retrieval, and risk review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timo2026](https://clawhub.ai/user/timo2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CNC workflow engineers use this skill to add quoting, material configuration, drawing parsing, case retrieval, and manual-review logic to machining quote systems. It is also useful for evaluating whether a submitted part quote should be calculated automatically or escalated for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive CAD files, order details, or customer snippets may leave the local machine through the public HTTP demo, cloud LLM providers, or a Feishu webhook. <br>
Mitigation: Review data flows before use, avoid uploading proprietary CAD files to the public demo unless authorized, prefer local/Ollama mode for sensitive work, and configure Feishu only when sending those snippets is approved. <br>
Risk: The quote engine imports executable code from a local ~/.openclaw/workspace/data path. <br>
Mitigation: Review, restrict, or remove the data_layer import behavior before production deployment, and ensure the local workspace path is controlled by trusted operators. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/timo2026/openclaw-cnc-core) <br>
- [OpenClaw CNC Website](https://openclaw.ai/cnc) <br>
- [Provider Configuration Guide](docs/PROVIDERS.md) <br>
- [Release Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and bash examples, JSON configuration examples, and structured quote or risk-review data when used from code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference cloud LLM providers, local Ollama mode, SQLite-backed case data, STEP/STL inputs, and CNC quote records.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata; artifact CHANGELOG top entry is 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
