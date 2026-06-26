## Description: <br>
Prompt Injection Firewall for AI agents. 113 detection patterns, 14 threat categories, zero dependencies. Protects against fake authority, command injection, memory poisoning, skill malware, crypto spam, and more. Hash-chain tamper-proof whitelist with mandatory peer review. Claude Code hook integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stlas](https://clawhub.ai/user/stlas) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to scan user prompts, files, stdin, or batches for prompt injection, spam, command injection, phishing, and related manipulation patterns before an agent processes the content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional hook can inspect and block future prompts, and false positives can interrupt normal work. <br>
Mitigation: Enable the hook only after reviewing its behavior, keep warning and block thresholds aligned with local tolerance, and provide a bypass or review path for legitimate blocked prompts. <br>
Risk: Whitelist changes alter filtering behavior and can reduce detection coverage if misused. <br>
Mitigation: Use the provided whitelist commands, require peer review for entries, verify the hash chain, and review exemption scope and expiration before deployment. <br>
Risk: The skill depends on PyYAML for pattern and whitelist parsing. <br>
Mitigation: Install PyYAML from a trusted package source and include it in normal dependency review. <br>
Risk: Peer-review labels are local process labels rather than strong identity proof. <br>
Mitigation: Map approver labels to an auditable local approval process when using the whitelist in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stlas/prompt-shield) <br>
- [Project URL listed in skill documentation](https://github.com/stlas/PromptShield) <br>
- [SCORING.md](artifact/SCORING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, JSON scan results, shell exit codes, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scan results classify input as CLEAN, WARNING, or BLOCK with scores capped at 100.] <br>

## Skill Version(s): <br>
3.0.6 (source: ClawHub release metadata and artifact/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
