## Description: <br>
Provides guidance and commands for discovering and querying Pilot Protocol news and current-events service agents across sources such as Hacker News, dev.to, GDELT, Reddit, Stack Exchange, and USGS hazards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover Pilot Protocol news service agents, inspect each agent's filter contract, and fetch structured feed data or natural-language summaries for current-events workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on Pilot Protocol, the pilotctl binary, a running daemon, and joining network 9. <br>
Mitigation: Install and run it only in environments where Pilot Protocol, pilotctl, and the joined network are trusted. <br>
Risk: Returned links, public feed data, and Gemini-generated summaries may contain external or misleading content. <br>
Mitigation: Treat outputs as external content, verify important claims against primary sources, and avoid sending sensitive or private queries through public feed agents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-service-agents-news) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot skills index](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON response examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent responses may include JSON envelopes with items, counts, pagination, truncation status, and upstream URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
