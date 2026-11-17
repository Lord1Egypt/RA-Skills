## Description:

LYGO Public Witness helps agents fetch and label allowlisted public reference feeds and LYGO lattice JSON without inventing missing sources or writing to live charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and operators use this skill to distinguish public OSINT-style reference overlays from LYGO canon data, inspect public witness feeds, and produce doctrine text, source summaries, overlay JSON, dry-run proposals, or optional local Ollama summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound public-data access may contact external HTTPS sources during canon, reference, or overlay commands.

Mitigation: Installers should expect outbound HTTPS GETs to the listed public sources and run the skill in an environment where that network posture is acceptable.

Risk: Report-writing flags can create local files.

Mitigation: Use report-writing flags only with paths intended for newly created reports.

Risk: The optional Ollama command sends a fixed witness prompt to a local service.

Mitigation: Run the Ollama command only if a local Ollama service at 127.0.0.1:11434 should receive and summarize the prompt.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/deepseekoracle/skills/lygo-public-witness)
- [LYGO Public Witness homepage](https://chatagent.ca/witness/)
- [SkillHub FULL LYGO reference](https://chatagent.ca/lygoskillhub.html#full-lygo)
- [Security notes](references/SECURITY.md)
- [SkillSpector audit response](references/SKILLSPECTOR_AUDIT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally write JSON reports only when report-writing flags are supplied.]

## Skill Version(s):

1.0.0 (source: frontmatter, claw.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
