## Description: <br>
Inference-based intrusion detection for AI agents using pattern matching, optional LLM analysis, quarantine records, and review commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emberDesire](https://clawhub.ai/user/emberDesire) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and operators use this OpenClaw plugin to scan AI-agent messages for jailbreaks, prompt injection, credential theft, social engineering, and related threats. It can warn, block, quarantine metadata-only records, and expose commands for scanning and quarantine review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can inspect agent messages and may use optional LLM, classifier, or Telegram alerting integrations. <br>
Mitigation: Disable useLlmTask, classifierAgent, llmEndpoint, and Telegram alerts when prompts or incident metadata must stay local. <br>
Risk: Quarantine behavior writes security metadata to local storage. <br>
Mitigation: Set an appropriate quarantineDir and cleanup policy before deployment. <br>
Risk: Trusted-owner bypass can skip scanning for configured owner messages. <br>
Mitigation: Set trustOwners to false for higher-risk deployments. <br>
Risk: Blocking thresholds can interrupt legitimate messages or allow risky traffic if tuned poorly. <br>
Mitigation: Review strictMode and per-agent riskThreshold settings, then monitor quarantine review outcomes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/emberDesire/hopeids) <br>
- [Publisher profile](https://clawhub.ai/user/emberDesire) <br>
- [hopeIDS documentation](https://exohaven.online/products/hopeids) <br>
- [hopeid npm package](https://www.npmjs.com/package/hopeid) <br>
- [GitHub link listed by artifact](https://github.com/E-x-O-Entertainment-Studios-Inc/hopeIDS) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown command responses, JSON tool and RPC results, configuration snippets, and setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return allow, warn, or block decisions with risk scores, intent labels, notifications, quarantine IDs, and metadata-only quarantine records.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
