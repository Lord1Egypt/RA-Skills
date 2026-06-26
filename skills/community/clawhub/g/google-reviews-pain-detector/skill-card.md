## Description: <br>
Scrapes Google reviews for businesses to identify pain words related to missed calls and poor phone coverage, scoring lead quality for AI receptionist sales. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JayJJimenez](https://clawhub.ai/user/JayJJimenez) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales operators and agent users use this skill to scan business review pages and lead lists for signs of missed calls, unreachable staff, and other phone coverage issues. It returns scored lead signals and snippets that help prioritize AI receptionist outreach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs automated review-site scraping and imports a local Scrapling dependency. <br>
Mitigation: Install only if this behavior is acceptable for the intended environment and run without the save flag first to inspect results. <br>
Risk: Using the save flag can modify the local Master Lead List by appending HOT leads. <br>
Mitigation: Back up the Master Lead List and review scored leads before running with the save flag. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JayJJimenez/google-reviews-pain-detector) <br>
- [Publisher profile](https://clawhub.ai/user/JayJJimenez) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Console text or JSON with pain scores, matched terms, review snippets, and lead summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append HOT leads to a local master lead list only when the user passes the explicit save flag.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
