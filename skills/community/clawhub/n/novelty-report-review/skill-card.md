## Description: <br>
Reviews scientific and technological novelty search reports against GB/T scientific and technological novelty search practices, checking novelty-point interpretation, Chinese and English search terms, search strategy, literature selection, and conclusions while reporting only issues and actionable improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charliegates309-oss](https://clawhub.ai/user/charliegates309-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and reviewers use this skill to audit Word-format scientific and technological novelty search reports for problems in novelty-point framing, search terms and translations, query construction, representative literature selection, and novelty conclusions. The skill returns only detected issues, priority fixes, and concrete revision suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-provided novelty report contents and may expose confidential project topics, keywords, or technical details to the agent session. <br>
Mitigation: Use it only with reports the user is comfortable sharing with the agent, and avoid live search workflows when the project topic or technical details are confidential. <br>
Risk: Fallback shell-based extraction of Word documents can process the wrong file if the path is ambiguous. <br>
Mitigation: Confirm the exact document path before allowing shell-based extraction. <br>
Risk: The skill may reference current Baidu Scholar search results, which may not reproduce a full systematic database search. <br>
Mitigation: Treat search-supported findings as review guidance and validate final novelty conclusions against the required databases and institutional review process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charliegates309-oss/novelty-report-review) <br>
- [Publisher profile](https://clawhub.ai/user/charliegates309-oss) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown audit report with prioritized findings and revision suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include shell-based document extraction commands only as an intermediate recovery method when direct Word document reading fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
