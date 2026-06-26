## Description: <br>
Fetch and analyze peer reviews from OpenReview for any academic paper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vectorsss](https://clawhub.ai/user/vectorsss) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External researchers, authors, and developers use this skill to fetch public OpenReview reviews for a paper and synthesize reviewer scores, consensus points, disagreements, author responses, meta-reviews, and decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts OpenReview and public web sources for review data. <br>
Mitigation: Use it only where this external access is acceptable and prefer OpenReview API results over search-derived fallback content. <br>
Risk: Fetched paper and review content is saved locally under /tmp. <br>
Mitigation: Delete the generated JSON file after use if local retention is not desired. <br>


## Reference(s): <br>
- [OpenReview Forum Pages](https://openreview.net/forum?id=<forum_id>) <br>
- [OpenReview API v2](https://api2.openreview.net) <br>
- [OpenReview API v1](https://api.openreview.net) <br>
- [Paper Review Synthesis Report Template](references/report-template.md) <br>
- [ClawHub Release Page](https://clawhub.ai/vectorsss/openreview-review-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown synthesis report with supporting JSON fetched to /tmp by the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Matches the user's language when producing the review synthesis.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
