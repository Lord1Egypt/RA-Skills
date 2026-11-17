## Description:

Security-first wrapper for installing agent skills. Scans for malware, prompt injection, and suspicious patterns before installation. Use instead of `clawhub install` for safer skill management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panzacoder](https://clawhub.ai/user/panzacoder)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use Pincer to scan ClawHub skills before installation, audit installed skills, and manage trusted or blocked publishers. It is intended as a command-line safety layer for agent skill management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner dependency is invoked without a pinned mcp-scan version.

Mitigation: Pin mcp-scan to a reviewed version and update it through an explicit review process.

Risk: Scanner errors may weaken the security gate.

Mitigation: Fail closed when scanner execution or parsing fails, and block or prompt before installation.

Risk: Fetched filenames could escape the intended temporary scan directory.

Mitigation: Normalize and validate fetched paths so downloaded files remain confined to the temporary scan directory.

Risk: The install fallback can fetch or install untrusted skill code before the intended checks complete.

Mitigation: Remove the install fallback or make it a non-executing fetch path that preserves pre-install scanning.

Risk: Auto-approval may not require an explicit trusted-publisher check.

Mitigation: Disable auto-approval by default or require a confirmed trusted publisher before clean scans proceed automatically.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/panzacoder/skills/pincer)
- [Pincer Repository](https://github.com/panzacoder/pincer)
- [mcp-scan](https://github.com/invariantlabs-ai/mcp-scan)
- [1Password Security Research](https://1password.com/blog/from-magic-to-malware-how-openclaws-agent-skills-become-an-attack-surface)
- [Snyk ToxicSkills Report](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text and optional JSON summaries, with shell commands and configuration guidance in Markdown documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires clawhub, jq, uvx, and the pincer command-line wrapper installed on PATH.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
