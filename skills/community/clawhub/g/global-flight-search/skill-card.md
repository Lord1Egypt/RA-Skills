## Description: <br>
零配置即装即用｜全球航班一次搜出结果｜含座位余量和行李额度｜性价比标签智能推荐 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-support agents use this skill to search global flight options, resolve airport or city codes, and check seat availability and baggage allowance before booking elsewhere. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight-search details are sent through the publisher's cloud proxy. <br>
Mitigation: Use the skill only when sharing route, date, cabin class, passenger counts, airport keywords, and routing IDs with that proxy is acceptable. <br>
Risk: Flight prices and availability can change and are presented as reference information. <br>
Mitigation: Confirm final fare, seat availability, and baggage terms on the booking provider before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/global-flight-search) <br>
- [Flight search cloud proxy](https://1439498936-460a7b6oqn.ap-guangzhou.tencentscf.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-formatted text with flight search results, airport codes, seat availability, baggage details, and CLI command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight prices are reference values; seat and baggage lookups require a routing_id from prior search results.] <br>

## Skill Version(s): <br>
1.3.0 (source: release evidence and artifact/version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
