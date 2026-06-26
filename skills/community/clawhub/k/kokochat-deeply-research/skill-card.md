## Description: <br>
KokoChat Deeply Research guides an OpenClaw agent through the research phase for KokoChat Deeply course generation by using KokoChat search and page fetching to produce sourced Chinese notes for a later outline pass. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[komako-workshop](https://clawhub.ai/user/komako-workshop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw and KokoChat users use this skill when a Chinese deep-research course request needs real web sources, a concise synthesis, and a structured handoff to KokoChat's outline-generation phase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics, search queries, and fetched page content may be sent to KokoChat's hosted search service or web fetch infrastructure. <br>
Mitigation: Avoid using sensitive or confidential topics unless that data sharing is acceptable for the deployment. <br>
Risk: The broader KokoChat setup enables exec and web_fetch for the deeply agent. <br>
Mitigation: Review the companion kokochat-search skill and install script before deployment, and keep tool allowlists scoped to the intended agent. <br>
Risk: Hosted search may be unavailable or return no results, which can affect source coverage. <br>
Mitigation: Follow the artifact guidance to report search failure honestly and avoid inventing URLs or citations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/komako-workshop/kokochat-deeply-research) <br>
- [KokoChat hosted search endpoint](https://deeply.plus/deeply/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Chinese Markdown prose followed by one fenced koko.deeply.research.notes JSON block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The notes block contains topic, synthesis, and a flat sources list using URLs returned by hosted search or page fetch.] <br>

## Skill Version(s): <br>
0.5.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
