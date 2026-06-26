## Description: <br>
Finds young AI-coding and entrepreneurial product-builder candidates on Jike. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robinc913](https://clawhub.ai/user/robinc913) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Talent scouts and recruiting operators use this skill to browse Jike, identify candidates who show AI-assisted coding, entrepreneurship, or independent product-building signals, and maintain a deduplicated local candidate pool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a logged-in Jike browser session during candidate discovery. <br>
Mitigation: Use a dedicated browser profile or account where possible, confirm login steps manually, and set clear search and time boundaries before execution. <br>
Risk: The workflow stores candidate IDs, profile links, post links, match notes, and discovery dates in a local talent-pool file. <br>
Mitigation: Periodically review the local talent-pool JSON file and delete candidate records that are no longer needed. <br>


## Reference(s): <br>
- [Jike web app](https://web.okjike.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown report with candidate counts and links, plus JSON entries in a local talent-pool file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes new candidate IDs, post links, profile links, match reasons, and discovery dates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
