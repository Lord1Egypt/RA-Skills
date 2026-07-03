## Description: <br>
Helps agents identify hindsight bias in post-outcome judgments, reconstruct what was knowable at the time, and guide users toward decision-process evaluation instead of outcome-driven blame. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and decision reviewers use this skill to analyze post-mortems, investment reviews, legal or operational evaluations, and other situations where outcome knowledge may distort judgments about what was foreseeable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can shape retrospective evaluations of people or decisions, which may affect blame, credit, or institutional learning. <br>
Mitigation: Use the skill's verification steps to pull contemporaneous records, separate decision quality from outcome quality, and document uncertainty before drawing conclusions. <br>
Risk: Security guidance notes that reviewer and admin workflows may send code or command output to configured tools or perform account, moderation, or email actions when explicitly confirmed. <br>
Mitigation: Install and use the skill only in intended authenticated workspaces, review commands before approving writes, and confirm account-impacting actions before execution. <br>


## Reference(s): <br>
- [Primary sources for hindsight-bias](references/sources.md) <br>
- [Baruch Fischhoff's Nixon-China Trip Study, 1972-1975](examples/baruch-fischhoffs-nixon-china-trip-study-1972-1975.md) <br>
- [ClawHub skill page](https://clawhub.ai/deciqai/skills/hindsight-bias) <br>
- [deciqAI publisher profile](https://clawhub.ai/user/deciqai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis template with structured diagnostic fields and coaching prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May pause for user input during coach mode before completing the full analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
