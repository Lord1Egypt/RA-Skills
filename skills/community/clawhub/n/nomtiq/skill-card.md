## Description:

Nomtiq 小饭票 helps agents find restaurants using live map search and local dining preferences, returning two reliable recommendations plus one reasoned exploration choice for the user's location, budget, party size, taste, and occasion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oakcoderx](https://clawhub.ai/user/oakcoderx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Nomtiq to choose restaurants for nearby dining, date night, business meals, family gatherings, solo dining, and feedback-driven preference updates. The skill routes mainland-China searches to Amap and other destinations to Google Maps through Serper when the user provides the needed API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release can use an undeclared Baidu Maps credential/provider path.

Mitigation: Before deployment, expose only the intended Amap or Serper key and unset BMAP_KEY unless Baidu Maps use has been explicitly reviewed and approved.

Risk: The documentation includes an unpinned global npx install path.

Mitigation: Prefer the OpenClaw install path for this release and avoid the unpinned npx global command unless the package source and version are independently verified.

Risk: Restaurant preferences, locations, companion notes, scene history, and feedback are stored locally.

Mitigation: Inform users about local storage and use the documented export, reset, companion removal, and history-clear controls when data should be reviewed or deleted.

## Reference(s):

- [ClawHub Nomtiq release page](https://clawhub.ai/oakcoderx/skills/nomtiq)
- [Amap Web Service API endpoint](https://restapi.amap.com)
- [Serper Google Maps API endpoint](https://google.serper.dev)
- [Amap developer key setup](https://console.amap.com/dev/key/app)
- [Serper API key setup](https://serper.dev/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Concise Markdown or plain text recommendations, with setup commands and JSON script output when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.9+, network access, and user-provided Amap or Serper API keys for live search; stores restaurant taste profile and feedback locally.]

## Skill Version(s):

0.5.2 (source: server release, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
