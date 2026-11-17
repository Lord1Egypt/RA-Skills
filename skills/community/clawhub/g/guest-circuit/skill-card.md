## Description:

Podcast-appearance research for guest booking: sweeps Podcast Index, web search, and the guest's own channels, then delivers a circuit report with an appearance timeline, repeated topics, unclaimed angles, receptiveness signal, and a specific pitch angle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conorbronsdon](https://clawhub.ai/user/conorbronsdon)

### License/Terms of Use:

MIT-0

## Use Case:

Podcast booking teams, marketers, founders, and developer relations practitioners use this skill before guest outreach to map a prospective guest's public podcast circuit, avoid repeated topics, and shape a targeted pitch around an unclaimed angle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on public web search, Podcast Index, and the guest's own public channels, so missing or ambiguous public records can lead to incomplete outreach conclusions.

Mitigation: Provide a concrete anchor fact for the guest, require fetched-page verification for every appearance, and place ambiguous leads in a could-not-verify section.

Risk: The skill creates a local report file that may contain outreach planning details.

Mitigation: Use it for public podcast-appearance research and avoid sensitive or private outreach plans unless local report persistence is acceptable.

Risk: Podcast Index access is optional and may be unavailable in some agent environments.

Mitigation: When Podcast Index is not configured, state that limitation in the report sources, fall back to web and own-channel research, and do not fill gaps from model memory.

## Reference(s):

- [Guest Circuit README](README.md)
- [Sweep Subagent Prompts](patterns/subagent-prompts.md)
- [Simon Willison Circuit Example](examples/simon-willison-circuit.md)
- [podcastindex-mcp](https://github.com/conorbronsdon/podcastindex-mcp)
- [ClawHub Skill Page](https://clawhub.ai/conorbronsdon/skills/guest-circuit)

## Skill Output:

**Output Type(s):** [analysis, markdown, files, guidance]

**Output Format:** [Markdown report with tables, source links, and a concise pitch recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local circuit report file by default and shows the appearance timeline and suggested pitch angle inline for review.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
