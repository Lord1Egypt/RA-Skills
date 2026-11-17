## Description:

JF Open Pro AI Smart Search helps agents search JF Tech cloud-stored alarm videos by semantic queries such as people, vehicles, animals, and behaviors, then retrieve matching clips or playback URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators with authorized JF Tech account and device access use this skill to locate cloud alarm video segments with semantic search terms and retrieve playback links for review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signed JF Tech requests and sensitive video access details may be sent beyond the declared API scope if endpoint configuration is changed.

Mitigation: Use only approved JF Tech API hosts, avoid overriding JF_ENDPOINT unless it is explicitly allowlisted, and review network configuration before deployment.

Risk: Playback URLs and video search results can expose sensitive camera footage details in logs or agent transcripts.

Mitigation: Treat playback URLs as temporary secrets, limit transcript and log retention, and redact URLs or identifiers before sharing outputs.

Risk: The artifact reports version 1.0.1 while the server release metadata and target metadata report 1.0.0.

Mitigation: Confirm the intended public release version during validation before rendering the public Skill Card.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-ai-smart-search)
- [JF Open API reference](references/jftech-api.md)
- [AI search examples](references/search-examples.md)
- [JF Tech open platform](https://open.jftech.com/)
- [JF Tech API documentation](https://docs.jftech.com/)
- [JF Tech AI smart search documentation](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=d2c0d9105d9c4b78bc0d2ee3851d2557)
- [JF Tech cloud playback API documentation](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=2e08468f46564602d01ae8a244661672)
- [JF Tech open platform SDK](https://github.com/jftech/open-platform-sdk)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and script output that may include JSON API responses or playback URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JF Tech credentials and device identifiers supplied through environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
