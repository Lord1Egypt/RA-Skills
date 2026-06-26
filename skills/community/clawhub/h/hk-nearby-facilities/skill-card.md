## Description: <br>
Find nearby Hong Kong public toilets by place keyword or shared coordinates using FEHD public data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimpang8](https://clawhub.ai/user/jimpang8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer nearby Hong Kong public-toilet requests in Cantonese, Chinese, or English with practical facility names, districts, addresses, distances when coordinates are provided, and map links. <br>

### Deployment Geography for Use: <br>
Hong Kong <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script makes outbound requests to FEHD public data endpoints. <br>
Mitigation: Use the skill only in environments where outbound access to FEHD public endpoints is acceptable. <br>
Risk: Precise live coordinates can reveal sensitive location information. <br>
Mitigation: Share exact latitude and longitude only when distance-ranked nearby results are needed. <br>
Risk: Keyword matches may be approximate and are not turn-by-turn routing directions. <br>
Mitigation: Present broad or low-confidence results as nearby matches and use map links for navigation checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimpang8/hk-nearby-facilities) <br>
- [FEHD map data endpoints](https://www.fehd.gov.hk/english/map) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text facility summaries; optional JSON from the bundled script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Google Maps links, distances, accessibility flags, and approximate-match notes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
