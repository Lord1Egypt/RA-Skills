## Description: <br>
Structured diagnosis for hard bugs and performance regressions by building a deterministic feedback loop, reproducing the issue, ranking hypotheses, instrumenting, fixing with a regression test, and cleaning up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilmych](https://clawhub.ai/user/ilmych) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose difficult bugs, flaky failures, and performance regressions through a disciplined reproduce-hypothesize-instrument-fix workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may guide an agent to run local commands, create repro tests, or add temporary debug instrumentation. <br>
Mitigation: Review proposed code changes and explicitly approve production instrumentation or access to sensitive environments. <br>
Risk: Temporary debug logs or harnesses can remain after diagnosis if cleanup is skipped. <br>
Mitigation: Use the skill's cleanup checks to remove tagged debug logs and throwaway harnesses before marking the task done. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ilmych/gstack-openclaw-diagnose) <br>
- [Publisher profile](https://clawhub.ai/user/ilmych) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown guidance with structured steps and command or code suggestions when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ranked hypotheses, reproduction loops, instrumentation notes, regression-test guidance, cleanup checks, and completion status.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
