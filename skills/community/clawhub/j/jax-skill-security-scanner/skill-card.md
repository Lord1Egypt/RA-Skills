## Description:

Scans OpenClaw skill directories and supplied text for sensitive operations, trojan or backdoor patterns, prompt poisoning, and hallucination or scam indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonshieh](https://clawhub.ai/user/jasonshieh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to inspect OpenClaw skill directories, review risk reports, and screen text for prompt-poisoning or hallucination-style risk indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat heuristic scan results as a final security decision.

Mitigation: Use the reports as triage input and require manual review before trusting or deploying scanned skills.

Risk: Installing an unverified npm package can introduce supply-chain risk.

Mitigation: Pin the package version and verify the package identity and hashes before installation.

Risk: Scanning overly broad paths can expose unrelated local skill files or produce noisy results.

Mitigation: Choose a narrow scan path that contains only the skills intended for review.

Risk: Runtime JavaScript entry points may behave differently than the documentation suggests.

Mitigation: Review package entry points and runtime files such as bin/ and dist/ before relying on scan output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jasonshieh/skills/jax-skill-security-scanner)
- [npm package](https://www.npmjs.com/package/@jax-npm/skill-security-scanner)
- [Project documentation](https://docs.jax-npm.com/skill-security-scanner)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text, Markdown, JSON, enhanced text, or enhanced Markdown security reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include risk counts, detected issue lists, trojan-pattern summaries, high- and medium-risk summaries, and suggested next steps.]

## Skill Version(s):

1.0.5 (source: server release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
