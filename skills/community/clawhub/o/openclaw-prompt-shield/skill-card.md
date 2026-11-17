## Description:

Local input-hardening scanner for OpenClaw agents that uses deterministic, pattern-based checks across 9 LLM input-risk categories and returns a risk score, matched categories, sanitized text, and a safe-to-process verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gopendrasharma89-tech](https://clawhub.ai/user/gopendrasharma89-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to pre-filter user messages, scraped web content, email bodies, RAG snippets, or historical chat logs before downstream agents treat the text as instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pattern-based detection can miss novel prompt-injection or evasion phrasing.

Mitigation: Use the skill as a first-pass signal and keep downstream tool permissions, secret access, and policy controls independently enforced.

Risk: Legitimate security or AI-policy content can trigger false positives.

Mitigation: Tune caution/block thresholds for those domains and use caller-supplied whitelists for known-good quoted material.

Risk: The skill returns advisory verdicts and does not itself block downstream processing.

Mitigation: Wrap the scanner in an agent or platform policy that decides how to handle safe, caution, and block results before using the input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gopendrasharma89-tech/skills/openclaw-prompt-shield)
- [OpenClaw metadata homepage](https://clawhub.ai/gopendrasharma89-tech/openclaw-prompt-shield)
- [Detection categories reference](references/patterns.md)
- [Detection-rule alphabets](references/categories.txt)
- [Suspicious host fragments](references/exfil-hosts.txt)
- [Security review notes](SECURITY.md)

## Skill Output:

**Output Type(s):** [text, JSON, markdown, shell commands, guidance]

**Output Format:** [Plain text or JSON scan reports, sanitized text blocks, batch JSONL outputs, shell exit codes, and Markdown usage guidance with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include a 0-100 risk score, safe/caution/block verdict, matched categories, recommendations, optional redactions, and caller-configurable thresholds and whitelists.]

## Skill Version(s):

0.4.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
