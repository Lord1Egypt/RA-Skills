## Description:

Guides an agent through authorized Mallary CLI discovery, account setup, and social publishing workflows while protecting sensitive account data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sammydigits](https://clawhub.ai/user/sammydigits)

### License/Terms of Use:

MIT-0

## Use Case:

People using Mallary with an agent can inspect connected profiles, drafts, posts, and analytics, set up access, or request specific publishing and account actions through the CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth setup grants broad access to connected social accounts, and unintended actions can publish content or change account state.

Mitigation: Use Mallary only for explicit user requests; verify the target profile, destination, content, media, and timing before acting, then check the result without retrying an uncertain write.

Risk: Credentials and account data can leak through command output or agent transcripts.

Mitigation: Keep API keys in a secret manager, never expose tokens, and redact sensitive profile, post, and account details from responses.

Risk: An unreviewed CLI installation can execute code with access to connected accounts.

Mitigation: Install only with user approval and prefer a pinned or reviewed CLI version over an unpinned one-off invocation.

## Reference(s):

- [Mallary skill on ClawHub](https://clawhub.ai/sammydigits/skills/mallary)
- [Mallary website](https://mallary.ai/)
- [Mallary documentation](https://docs.mallary.ai)
- [Mallary CLI package](https://www.npmjs.com/package/@mallary/cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline CLI commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Minimized results with sensitive account details redacted.]

## Skill Version(s):

1.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
