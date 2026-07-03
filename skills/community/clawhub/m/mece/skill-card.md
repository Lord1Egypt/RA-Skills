## Description: <br>
Guides an agent to decompose broad or overlapping problems into mutually exclusive, collectively exhaustive issue trees, test for gaps and overlap, and identify the load-bearing branch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to structure complex business, strategy, or analytical questions into a MECE decomposition. It helps turn broad or messy problem spaces into testable branches, identify missing or overlapping categories, and produce a concise issue-tree-style markdown artifact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate for broad problem-solving or presentation-prep requests when the user prefers less structured brainstorming. <br>
Mitigation: Invoke it explicitly for structured decomposition, or ask the agent to stay exploratory when early structure would constrain ideation. <br>
Risk: A decomposition can look rigorous while still using overlapping categories, missing residual cases, or choosing the wrong top-level dimension. <br>
Mitigation: Review the overlap check, gap check, sum-to-whole test, and alternative decompositions before relying on the output. <br>


## Reference(s): <br>
- [Sources - mece](references/sources.md) <br>
- [Lou Gerstner's IBM Turnaround Decomposition (1993)](examples/lou-gerstner-ibm-turnaround-decomposition-1993.md) <br>
- [IBM Investor Relations](https://www.ibm.com/investor/) <br>
- [ClawHub listing](https://clawhub.ai/deciqai/skills/mece) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, Markdown] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a structured MECE decomposition with the whole problem, top-level split, ME and CE tests, optional sub-decomposition, load-bearing branch, implied action, and alternatives considered.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
