## Description:

Kuvera portfolio & market data CLI for querying mutual fund data, gold prices, USD/INR rates, fund category returns, and read-only Kuvera portfolio information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ankitsul](https://clawhub.ai/user/ankitsul)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to retrieve Kuvera market data, mutual fund details, and read-only portfolio, transaction, and SIP information after login when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logging in gives the skill access to sensitive Kuvera profile and investment data.

Mitigation: Use authenticated commands only on trusted systems and review outputs before sharing them.

Risk: Passing a real password as a command-line argument can expose it through shell history, process listings, or logs on shared systems.

Mitigation: Avoid login on shared or monitored machines and clear shell history or other command logs if credentials were entered.

Risk: The saved bearer token may remain readable according to local filesystem permissions until removed or expired.

Mitigation: Restrict local credential-file permissions and remove the stored token when access is no longer needed.

## Reference(s):

- [Kuvera CLI API Guide](references/api-guide.md)
- [Kuvera](https://kuvera.in)
- [OpenClaw](https://openclaw.org)
- [ClawHub Skill Page](https://clawhub.ai/ankitsul/skills/kuvera)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI output and Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands require Kuvera login and may display sensitive profile, portfolio, transaction, or SIP data.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
