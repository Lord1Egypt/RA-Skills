## Description: <br>
月老 Matchmaker generates a social-media-based compatibility report for two consenting people, including a match score, chemistry points, friction warnings, and date suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sophie-xin9](https://clawhub.ai/user/sophie-xin9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People considering a relationship, date, or compatibility check use this skill with an agent to collect volunteered social-media data from both participants and produce a structured compatibility report. The report compares interests, values, rhythms, aesthetics, and social habits, then turns those comparisons into practical conversation and date ideas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to collect broad logged-in social-media histories, which can expose private data if participants have not clearly consented. <br>
Mitigation: Use it only when both people agree to the exact platforms and data categories being scanned, and avoid analyzing a public profile without that person's permission. <br>
Risk: Collected profile data and generated reports may contain sensitive or embarrassing inferences. <br>
Mitigation: Collect the smallest useful subset, review the generated data before sharing any report, and delete matchmaker-data after use. <br>
Risk: The skill depends on ManoBrowser browser automation for logged-in account access. <br>
Mitigation: Use a separate browser profile and review or pin the ManoBrowser dependency before running scans. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sophie-xin9/matchmaker) <br>
- [ManoBrowser dependency](https://github.com/ClawCap/ManoBrowser) <br>
- [Example compatibility report](examples/xiaokai_match_report.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance] <br>
**Output Format:** [Markdown compatibility report with scores, tables, warnings, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local analysis guidance based on collected participant data; report quality depends on consented data coverage and accuracy.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
