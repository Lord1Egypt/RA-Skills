## Description: <br>
Helps an agent design and build supervised self-running automation loops with triggers, state files, objective gates, stop conditions, command guardrails, and rollout guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hansraj316](https://clawhub.ai/user/hansraj316) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn recurring chores such as CI triage, PR checking, digests, dependency bumps, lint/build loops, and documentation refreshes into supervised agent loops with objective pass/fail gates and explicit stopping conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended loops can keep running after the user stops prompting and may make account-visible changes if triggers, permissions, and stop conditions are too broad. <br>
Mitigation: Before enabling a generated loop, verify the trigger, command allowlist, hard-stop gate, state file, maximum iterations, and whether it can push commits, open PRs, comment, label, or perform other visible actions. <br>
Risk: A poorly proven loop can repeat incorrect work or incur unexpected cost. <br>
Mitigation: Run the loop manually first, validate the objective gate on known-good and known-bad cases, measure token and wall-clock cost per iteration, and start at a low autonomy level. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with file templates, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce procedure skill files, state-file formats, command allowlists, trigger setup guidance, proof-run summaries, cost estimates, and autonomy-level guidance.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
