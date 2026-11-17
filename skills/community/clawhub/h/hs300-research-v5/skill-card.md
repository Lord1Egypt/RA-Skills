## Description:

Research HS300 index constituents for stock analysis and portfolio construction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run HS300/CSI 300 stock research, multi-factor scoring, technical and fundamental analysis, and portfolio-construction research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext financial-data service credentials are present in the artifact.

Mitigation: Remove and rotate embedded credentials before use; require user-supplied environment secrets for provider authentication.

Risk: Authenticated provider access behavior conflicts with documentation that says JQData is disabled or user-configured.

Mitigation: Align documentation and configuration, disable default authentication, and require explicit user setup before enabling provider access.

Risk: Pickle-based caches may be unsafe in shared or sensitive environments.

Mitigation: Replace pickle caches with a safer serialization format and avoid loading cache files from untrusted locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/hs300-research-v5)
- [Tushare Pro](https://tushare.pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; generated research reports may be Markdown or Excel files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to financial data providers and user-supplied provider credentials; outputs are research references and not investment advice.]

## Skill Version(s):

5.2.2 (source: server release metadata; artifact frontmatter 5.2.0, package.json 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
