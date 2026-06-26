## Description: <br>
Scores improvement candidates with heuristic rules, evaluator evidence, optional LLM judging, and optional multi-reviewer blind panel review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and improvement-pipeline maintainers use this skill to rank proposed skill changes, inspect scoring rationale, and produce advisory accept, conditional, hold, or reject signals before a separate gate makes final decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes local Python evaluation behavior that can be unsafe for untrusted files. <br>
Mitigation: Run the real-skill evaluator only on trusted Python files or inside a sandboxed environment. <br>
Risk: Non-mock LLM judging may send candidate or skill content through a configured Claude or OpenAI account or proxy. <br>
Mitigation: Use mock LLM judging for sensitive skills, and verify account and proxy settings before non-mock runs. <br>
Risk: accept_for_execution and executor handoff signals are advisory rather than final approvals. <br>
Mitigation: Require a separate gate to approve execution before applying any candidate changes. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/lanyasheng/improvement-discriminator) <br>
- [Publisher profile](https://clawhub.ai/user/lanyasheng) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON scoring reports and markdown-facing guidance with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include per-candidate scores, blockers, recommendations, judge notes, panel reviews, cognitive labels, aggregated scores, and LLM verdicts.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
