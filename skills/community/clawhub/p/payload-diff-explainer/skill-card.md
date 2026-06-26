## Description: <br>
Compare two JSON payloads or API responses and explain the meaningful differences in plain English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cheeseqi](https://clawhub.ai/user/cheeseqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to compare user-provided JSON payloads, API responses, config objects, or diffs and understand meaningful structural, value, type, and impact differences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payloads may contain secrets, tokens, session cookies, personal data, or sensitive internal identifiers. <br>
Mitigation: Redact sensitive values before sharing payloads with any chat-based tool. <br>
Risk: The skill may infer likely business, UI, or backend impact from payload structure without access to the full system context. <br>
Mitigation: Treat impact statements as analysis guidance and verify them against application behavior, logs, tests, or domain knowledge before taking action. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown sections covering summary, important differences, structural differences, likely noise, and likely impact.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only analysis of user-provided content; users should redact secrets, tokens, session cookies, personal data, and sensitive internal identifiers before sharing payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
