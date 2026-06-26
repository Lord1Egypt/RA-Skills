## Description: <br>
Meituan helps agents summarize public Meituan merchant, product, offer, rating, price, and review information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to collect concise summaries and comparisons from public Meituan merchant, product, and offer pages for internal analysis and alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill could be used outside its public-page scope for ordering, account actions, authenticated pages, or interface reverse engineering. <br>
Mitigation: Keep use limited to public Meituan pages and do not perform ordering, account-changing actions, authenticated access, interface calls, or attempts to bypass platform protections. <br>
Risk: Bulk collection or high-frequency access could violate platform boundaries. <br>
Mitigation: Use lightweight, human-triggered analysis, apply frequency control, and avoid bulk scraping. <br>
Risk: Prices, delivery information, promotions, distance, and availability can vary by time and region. <br>
Mitigation: Include the collection time and region with summaries and treat time-sensitive values as snapshots. <br>
Risk: Location details may expose sensitive user context. <br>
Mitigation: Share only the location detail needed for the specific analysis and avoid unnecessary precise location disclosure. <br>


## Reference(s): <br>
- [Meituan homepage](https://www.meituan.com/) <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/meituan-hot-trend) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or structured text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries should include collection time and region when prices, delivery details, promotions, distance, or availability are discussed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
