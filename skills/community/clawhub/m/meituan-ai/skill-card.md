## Description: <br>
Meituan helps an agent summarize public Meituan merchant, product, and deal information, including prices, ratings, promotions, and comparison highlights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to gather concise summaries and comparisons from public Meituan merchant, product, and promotional pages. It is intended for lightweight insight and reminders, not ordering, interface reverse engineering, or bypassing platform controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public Meituan prices, delivery details, distance, and availability may vary by time and region. <br>
Mitigation: Include the collection time and region in outputs, and treat summaries as time-sensitive guidance rather than durable facts. <br>
Risk: Automated use could drift into account actions, bulk scraping, or platform-control bypass attempts. <br>
Mitigation: Keep use user-directed, analyze only public pages, apply frequency control, and avoid ordering, reverse engineering, or bypassing platform controls. <br>
Risk: Precise location details can be sensitive and may affect result interpretation. <br>
Mitigation: Use only the location context needed for the requested summary and avoid exposing unnecessary precise location details in outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/CodeKungfu/meituan-ai) <br>
- [Publisher Profile](https://clawhub.ai/user/CodeKungfu) <br>
- [Meituan Homepage](https://www.meituan.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summaries, comparison notes, and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results should note collection time and region when price, availability, delivery, or distance information may vary.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
