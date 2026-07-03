## Description: <br>
Classifies product feature lists into Kano categories and produces a pruned, evidence-labeled backlog focused on must-be reliability, performance tradeoffs, attractive MDP picks, and low-value cuts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[monikazapisekstudio](https://clawhub.ai/user/monikazapisekstudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, founders, design/product engineers, and agents use this skill to triage feature backlogs, distinguish must-have, performance, and delight work, cut indifferent or reverse features, and frame MDP-over-MVP tradeoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: May apply an opinionated pruning lens to general backlog or stakeholder-scope discussions where neutral project management advice is expected. <br>
Mitigation: Invoke intentionally for Kano-style feature pruning and review recommendations against user research, product strategy, and stakeholder constraints before acting. <br>
Risk: May over-prune or under-prioritize features when the input lacks concrete feature names, target segment, product stage, constraints, or user evidence. <br>
Mitigation: Provide concrete features and context, mark low-evidence classifications as assumptions, and validate questionable decisions with user research before committing. <br>
Risk: Market-access prerequisites such as compliance requirements can be misread as feature backlog items if the request is ambiguous. <br>
Mitigation: Separate compliance and go-to-market prerequisites from Kano feature triage and document them as required constraints rather than optional backlog candidates. <br>


## Reference(s): <br>
- [Kano Classification](references/kano-classification.md) <br>
- [Kano vs. MDP/MVP](references/kano-vs-mdpmvp.md) <br>
- [Experience Rot Checklist](references/experience-rot-checklist.md) <br>
- [CEO Pushback Scripts](references/ceo-pushback-scripts.md) <br>
- [Evaluation Evidence](EVIDENCE.md) <br>
- [Skill Listing](https://clawhub.ai/monikazapisekstudio/skills/kano-model-strategist) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown table plus concise prose recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits tables to 15 rows and asks for concrete feature list, target user segment, product stage, and constraints when inputs are missing.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
