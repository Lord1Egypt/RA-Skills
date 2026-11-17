## Description:

Personal Insight Engine (PIE) is a strategic analysis tool that scans local session logs from memory/*.md and extracts three strategic insights using LLMs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Founders, operators, and developers use this skill to summarize recent OpenClaw memory logs into a weekly strategic review focused on product, market, business, and operational patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local session logs are sent to external LLM providers after best-effort redaction, and security evidence warns that privacy protections are overstated.

Mitigation: Use only on workspaces where sending recent memory logs to Gemini or Zhipu is acceptable; avoid secrets, customer data, private notes, and regulated information unless file-scope and redaction issues are fixed.

Risk: The security summary identifies weak file-scope controls around memory-log collection.

Mitigation: Review the files selected for analysis before running the skill and restrict the workspace contents to logs intended for external analysis.

Risk: Dependencies are declared without version pins.

Mitigation: Pin and review dependencies before operational use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/franklu0819-lang/skills/personal-insight-engine)
- [Gemini Generate Content API Endpoint](https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent)
- [Zhipu Chat Completions API Endpoint](https://open.bigmodel.cn/api/paas/v4/chat/completions)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report printed to standard output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and either GEMINI_API_KEY or ZHIPU_API_KEY; scans recent OpenClaw memory Markdown files before calling the selected external LLM provider.]

## Skill Version(s):

1.0.4 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
