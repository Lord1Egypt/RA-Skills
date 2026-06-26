## Description: <br>
Retrieves and summarizes public Mafengwo travel notes and attraction pages, including ratings, reviews, tickets, opening times, and itinerary cues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and travel operations teams use this skill to produce lightweight summaries of public Mafengwo destination, attraction, and travelogue pages for internal analytics, reminders, and itinerary drafting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated collection or high-frequency access could violate Mafengwo platform rules. <br>
Mitigation: Use the skill only for lightweight summaries of public pages, avoid bulk collection, and follow Mafengwo platform rules. <br>
Risk: Travel details such as prices, tickets, and opening hours may change seasonally or without notice. <br>
Mitigation: Verify time-sensitive details before use and include the collection time when reporting them. <br>
Risk: Dynamic page rendering may cause incomplete or stale extraction if content has not loaded. <br>
Mitigation: Wait for visible page content before summarizing and treat missing fields as unavailable rather than inferred. <br>


## Reference(s): <br>
- [ClawHub Mafengwo package page](https://clawhub.ai/CodeKungfu/mafengwo) <br>
- [Mafengwo homepage](https://www.mafengwo.cn/) <br>
- [Mafengwo travel notes](https://www.mafengwo.cn/gonglve/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown or structured text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries should include collection time for time-sensitive prices or opening hours when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
