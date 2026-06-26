## Description: <br>
Fetch and display the top trending Google searches in the last 24 hours for any country. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brunovu20](https://clawhub.ai/user/brunovu20) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve current Google Trends daily RSS topics for a chosen country, then present ranks, estimated search volume, publication time, related news headlines, and Trends links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Google Trends over the network and may display external news links from the public RSS feed. <br>
Mitigation: Review network use before installation, treat feed content and linked news as external public content, and verify important claims with primary sources. <br>
Risk: The release metadata includes a sensitive-credentials capability tag even though the security evidence reports no API key or credential access. <br>
Mitigation: Confirm the metadata before publication and correct the tag if credential access is not required. <br>
Risk: Google Trends topics and approximate traffic values can change as the public RSS feed updates. <br>
Mitigation: Present results with the fetch time, selected country code, and source attribution, and avoid fabricating missing traffic numbers or topics. <br>


## Reference(s): <br>
- [Google Trends daily RSS feed](https://trends.google.com/trending/rss?geo={GEO}) <br>
- [ClawHub skill page](https://clawhub.ai/brunovu20/google-trending) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown summary of Google Trends RSS results, with optional shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on the public Google Trends RSS feed, selected ISO country code, and requested count.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
