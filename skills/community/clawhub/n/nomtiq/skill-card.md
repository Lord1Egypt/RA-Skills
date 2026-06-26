## Description: <br>
Nomtiq finds restaurants worth going to without rankings or ads, remembers taste and budget, and supports Chinese and English restaurant discovery workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oakcoderx](https://clawhub.ai/user/oakcoderx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Nomtiq to search for restaurants, personalize recommendations from a taste profile, and record dining feedback. The skill supports local China search, overseas search, onboarding, profile analysis, and optional anonymous sharing of liked restaurants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Moltbook sharing can send liked restaurants, areas, prices, and tags to an external service. <br>
Mitigation: Keep Moltbook disabled or leave MOLTBOOK_API_KEY unset unless the user explicitly wants anonymous sharing. <br>
Risk: The package includes promotion research and community-monitoring scripts beyond the core restaurant recommendation workflow. <br>
Mitigation: Remove or ignore promotion and monitor scripts when deploying only a local restaurant recommender. <br>
Risk: Restaurant search can call external services using configured API keys. <br>
Mitigation: Configure only the API keys required for the intended geography and disclose that restaurant queries may be sent to those services. <br>


## Reference(s): <br>
- [ClawHub Nomtiq Release Page](https://clawhub.ai/oakcoderx/nomtiq) <br>
- [AGENT_GUIDE.md](AGENT_GUIDE.md) <br>
- [README.md](README.md) <br>
- [Amap REST API](https://restapi.amap.com) <br>
- [Serper API](https://google.serper.dev) <br>
- [Moltbook API](https://www.moltbook.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Restaurant recommendations may use profile data, external search APIs, and optional Moltbook sharing when configured.] <br>

## Skill Version(s): <br>
0.4.6 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
