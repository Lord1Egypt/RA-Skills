## Description:

Retrieves relevant legal provisions and similar case examples for user-described disputes, then formats legal basis, case summaries, and optional practical analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rose-develop](https://clawhub.ai/user/rose-develop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve legal provisions and similar case examples for common dispute descriptions, such as fraud, unpaid debts, contract breaches, personal injury, torts, and litigation prospects. The skill can also summarize legal risk factors and practical next steps when the user asks for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User dispute descriptions may contain personal, financial, or legal-strategy details that are sent to Wendaoyun's external API.

Mitigation: Use minimized and redacted queries; avoid names, IDs, addresses, account details, exact private facts, and legal strategy before calling the API.

Risk: Legal retrieval results and similar-case summaries may be incomplete, jurisdiction-sensitive, or unsuitable as final legal advice.

Mitigation: Treat the output as retrieval assistance, verify legal conclusions with authoritative sources, and consult qualified legal counsel for consequential decisions.

Risk: The skill depends on a user-provided WENDAOYUN_API_KEY for authenticated external API calls.

Mitigation: Store the API key only in the environment, do not paste it into prompts or logs, and revoke it promptly if exposure is suspected.

## Reference(s):

- [Wendaoyun Open Platform](https://open.wendaoyun.com/home)
- [Wendaoyun get-laws API endpoint](https://h5.wintaocloud.com/prod-api/api/invoke/get-laws)
- [ClawHub skill page](https://clawhub.ai/rose-develop/skills/pre-judgment-of-similar-cases-wdy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with formatted legal provisions, case summaries, optional analysis, and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses WENDAOYUN_API_KEY for authenticated API requests; top_k defaults to 3 and is capped at 5.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
