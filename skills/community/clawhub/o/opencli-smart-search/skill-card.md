## Description: <br>
Routes search and research requests to suitable opencli sources, using live opencli help to choose sites and commands for web, social, technical, shopping, travel, finance, jobs, and Chinese-language queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liberalchang](https://clawhub.ai/user/liberalchang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to plan and summarize external searches with opencli, selecting an appropriate source before issuing live search commands. It is useful for user-facing research workflows that need targeted source choice, call limits, and a short search summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search requests may be routed to external sites or providers, which can expose sensitive query content outside the local agent session. <br>
Mitigation: For sensitive searches, explicitly name the approved site or ask the agent not to use external search routing. <br>
Risk: Live source availability, command signatures, and search results can change during use. <br>
Mitigation: Run opencli registry and help checks before searching, and report skipped or unavailable sources in the final search summary. <br>


## Reference(s): <br>
- [AI default sources](references/sources-ai.md) <br>
- [Technical and academic sources](references/sources-tech.md) <br>
- [Social media sources](references/sources-social.md) <br>
- [Media and entertainment sources](references/sources-media.md) <br>
- [Information and knowledge sources](references/sources-info.md) <br>
- [Shopping sources](references/sources-shopping.md) <br>
- [Travel sources](references/sources-travel.md) <br>
- [Other vertical sources](references/sources-other.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and a search summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source selection guidance, per-site call counts, skipped-source notes, and coverage gaps when search limits are reached.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
