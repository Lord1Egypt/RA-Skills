## Description: <br>
Openclaw Prompt Shield is a local Python input-hardening scanner that scores untrusted text for prompt-injection, jailbreak, role-override, data-exfiltration, and related LLM input risks before an agent processes it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gopendrasharma89-tech](https://clawhub.ai/user/gopendrasharma89-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to pre-filter user messages, scraped web content, email bodies, RAG snippets, or chat logs before those inputs are treated as agent instructions. It returns risk scores, category matches, verdicts, and sanitized text or JSON reports so the caller can decide whether to continue, review, or block downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner can read input files and write reports or sanitized files at paths supplied by the caller. <br>
Mitigation: Provide only intended input and output paths, and review generated reports or sanitized files before relying on them downstream. <br>
Risk: Pattern-based verdicts are a first-pass signal and may miss novel attacks or flag legitimate security discussion. <br>
Mitigation: Combine the verdict with policy-level controls, human review for high-impact workflows, and deliberate threshold or whitelist settings for trusted research content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gopendrasharma89-tech/openclaw-prompt-shield) <br>
- [Security review notes](SECURITY.md) <br>
- [Detection pattern reference](references/patterns.md) <br>
- [Detection category alphabets](references/categories.txt) <br>
- [Exfiltration host fragments](references/exfil-hosts.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Guidance] <br>
**Output Format:** [Plain text or JSON scan reports, with optional sanitized UTF-8 text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deterministic local scoring with safe, caution, and block verdicts; no API keys or remote calls are required.] <br>

## Skill Version(s): <br>
0.4.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
