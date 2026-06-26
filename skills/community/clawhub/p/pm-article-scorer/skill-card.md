## Description: <br>
Scores public-account articles on a 0-100 heuristic rubric to decide whether they are relevant and useful for AI product managers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agasding](https://clawhub.ai/user/agasding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, content operations teams, and agent workflows use this skill to triage RSS or public-account articles for AI product-management relevance, ranking, and daily selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Heuristic scores can be imperfect or misleading for final article selection. <br>
Mitigation: Use the score as a triage signal and keep human review for publishing or reading decisions. <br>
Risk: A future implementation of heuristic_score could introduce unnecessary exposure of article content. <br>
Mitigation: Confirm any implementation keeps article content local and avoids logging, network upload, credentials, or broad file access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agasding/pm-article-scorer) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Python dictionary / JSON-like structured scoring result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns article relevance, interest level, score, recommendation, dimension scores, content type, tags, reasons, and summary.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
