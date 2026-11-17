## Description:

LYGO Deception Radar rebuilds an anonymized Ops Detector radar feed and optional static HTML dashboard from public labeled discourse samples, grouping results into strong, weak calibration, and clear bands with an operational threshold of 0.65.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and security analysts use this skill to rebuild a public, anonymized discourse-signal radar feed and optional static HTML dashboard from labeled samples. It is intended for public analysis, not person-level verdicts, doxing, private mail, or private log ingestion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The build script can load a local lygo-ops-detector module from adjacent paths or LYGO_STACK_ROOT.

Mitigation: Use only a trusted, version-pinned detector installation and avoid pointing LYGO_STACK_ROOT at untrusted directories.

Risk: Generated HTML may be unsafe if built from untrusted sample data.

Mitigation: Process trusted public sample suites only and apply proper HTML escaping before hosting generated dashboards.

Risk: Radar bands and scores can be misread as person-level or legal verdicts.

Mitigation: Use the output only for public discourse-pattern analysis and preserve the documented limits against doxing, private data ingestion, and person verdicts.

## Reference(s):

- [Security Notes](references/SECURITY.md)
- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-deception-radar)
- [Homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-deception-radar)
- [Live Dashboard](https://deepseekoracle.github.io/lygo-protocol-stack/deception-radar/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; generated artifacts are JSON and optional static HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes radar_feed.json and, when requested, an index.html dashboard from public sample data.]

## Skill Version(s):

1.0.0 (source: frontmatter, claw.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
