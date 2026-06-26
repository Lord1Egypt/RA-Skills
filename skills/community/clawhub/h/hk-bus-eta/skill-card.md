## Description: <br>
Fast, reliable Hong Kong bus ETA lookup for KMB, Citybus, and LWB with fuzzy stop matching, bilingual output, and multi-route parallel queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomfong](https://clawhub.ai/user/tomfong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and compatible AI agents use this skill to answer Hong Kong public bus arrival queries from route and stop names. It is suited for quick next-bus lookups, bilingual responses, and comparing ETAs across multiple routes. <br>

### Deployment Geography for Use: <br>
Hong Kong <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python scripts and may create or refresh cache files inside its scripts directory. <br>
Mitigation: Installers should expect writes only to the documented skill-local cache paths and should review those paths during deployment. <br>
Risk: The skill contacts public Hong Kong transit and open-data services to retrieve ETA and stop data. <br>
Mitigation: Allow network access only to the documented transit data domains and avoid sending secrets or private data in route and stop queries. <br>
Risk: Live ETA data can be missing, delayed, or outside service hours. <br>
Mitigation: Use the documented fixed fallback messages when no ETA is returned and avoid fabricating arrival times. <br>
Risk: Route and stop names are passed as command arguments. <br>
Mitigation: Use normal argument passing and careful quoting for user-provided route and stop names. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomfong/hk-bus-eta) <br>
- [Publisher profile](https://clawhub.ai/user/tomfong) <br>
- [KMB/LWB ETA data service](https://data.etabus.gov.hk/) <br>
- [Citybus ETA data service](https://rt.data.gov.hk/) <br>
- [Hong Kong open data portal](https://data.gov.hk/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Concise Markdown or plain text containing route labels, stop names, destinations, Google Maps links, ETA times, operator labels, and fixed fallback messages when no ETA is available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Traditional Chinese and English output; route and stop query parameters; multi-route responses may be grouped by route.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
