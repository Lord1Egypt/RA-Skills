## Description: <br>
Analyze git repository statistics including contributor rankings, lines of code by language, commit frequency by day/hour, monthly activity trends, and file type breakdowns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnnywang2001](https://clawhub.ai/user/johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect local Git repositories, summarize contributor activity, count tracked files and lines by extension, and generate commit activity trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may expose contributor emails and local repository paths. <br>
Mitigation: Run the skill only on repositories intended for analysis and review reports before sharing them. <br>
Risk: Line-count analysis reads tracked files in the selected repository. <br>
Mitigation: Use the --no-loc option for sensitive or very large repositories, and run the helper only in explicitly chosen local repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnnywang2001/git-stats) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands] <br>
**Output Format:** [Plain text repository report or JSON output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can include contributor names, contributor emails, commit counts, file type counts, LOC totals, repository paths, and activity trend buckets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
