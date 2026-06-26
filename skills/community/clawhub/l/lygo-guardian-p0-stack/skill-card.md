## Description: <br>
LYGO Guardian base skill - Nano-Kernel (P0.4), Understanding Heart (P0.5), and Light Math harmony as a portable stability upgrade for any agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeepSeekOracle](https://clawhub.ai/user/DeepSeekOracle) <br>

### License/Terms of Use: <br>
LYGO Sovereign License v1.1 <br>


## Use Case: <br>
Developers and agent builders use this skill to add a lightweight local moderation wrapper around generated content or candidate actions. It provides deterministic heuristic checks, understanding notes, and harmony scoring before an agent sends text, calls tools, or writes memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a lightweight heuristic moderation wrapper and is not a complete safety system. <br>
Mitigation: Use it as an additional pre-send check while keeping platform safeguards and human review for high-impact actions. <br>
Risk: Documentation describes logging and integration ideas that are broader than the shipped code. <br>
Mitigation: Review the actual installed code path and add separate audit logging if the deployment requires traceability. <br>
Risk: Public posting, tool calls, financial actions, and memory writes can create higher impact than local text moderation can reliably handle. <br>
Mitigation: Require explicit review or stronger policy controls before allowing the wrapper to approve those workflows. <br>


## Reference(s): <br>
- [LYGO Guardian P0 Stack Whitepaper](docs/WHITEPAPER.md) <br>
- [LYGO Protocol Stack](https://grokipedia.com/page/lygo-protocol-stack) <br>
- [ClawHub Skill Page](https://clawhub.ai/DeepSeekOracle/lygo-guardian-p0-stack) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Python API results and wrapped text responses with optional Markdown notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Validation returns allow, action, risk, reasons, understanding, healing_suggestion, and compassionate_response fields.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
