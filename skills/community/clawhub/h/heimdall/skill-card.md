## Description:

Author and run evidence-backed browser and API test plans with honest blocked and non-run semantics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use Heimdall to author, validate, and run repeatable browser and API test plans that produce inspectable evidence instead of unsupported claims. It is suited for checking live applications through Playwright/CDP, an isolated Docker browser lane, or an explicit handoff for logged-in browser work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Test plans can trigger high-impact browser actions and HTTP requests against real systems.

Mitigation: Review every plan before execution and avoid production, paid, or destructive targets unless the target, request volume, credentials, and rollback path are clear.

Risk: Risk labels and allow-risk controls are coordination mechanisms rather than a sandbox.

Mitigation: Use read-only cases by default, require explicit review before allowing destructive, paid, or production cases, and prefer the container driver for untrusted targets.

Risk: Authentication state files and run evidence can contain sensitive information.

Mitigation: Keep storageState files outside version control, pass secrets through environment tokens, and treat heimdall-runs output as sensitive.

Risk: Mutable source install commands can change what is installed over time.

Mitigation: Prefer pinned commits or reviewed ClawHub releases when installing for repeatable use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/antreasantoniou/skills/heimdall)
- [README](README.md)
- [Skill Instructions](SKILL.md)
- [Plan JSON Schema](heimdall.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to produce Heimdall JSON plans, CLI commands, and honest run summaries with blocked or skipped cases called out.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
