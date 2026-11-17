## Description:

Analyze physician academic influence and collaboration networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Agents can help medical-affairs, pharmaceutical, and research analysts run a local profiler for named physicians, summarize publication metrics, and inspect collaboration signals from supplied publication data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation describes therapeutic-area, geography, metrics, output, and format parameters, while the script accepts a named author, optional JSON data, and a demo mode.

Mitigation: Review the CLI behavior before operational use and run the script with the documented implementation arguments until the documentation and code are aligned.

Risk: Publication datasets supplied to the local script may contain sensitive or proprietary information.

Mitigation: Use only non-sensitive publication data files that are intended for local analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/kol-profiler)
- [Publisher profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [text, code, shell commands]

**Output Format:** [Plain text CLI profile printed to stdout, with JSON publication data accepted as input.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally without external network access; use only non-sensitive publication data files intended for analysis.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
