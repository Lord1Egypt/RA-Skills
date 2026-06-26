## Description: <br>
Repair Evolver restart storms caused by singleton lock/PID false positives and service restart policy mismatch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xyezir](https://clawhub.ai/user/xyezir) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations engineers use this skill to diagnose and repair Evolver service restart loops caused by stale singleton locks, PID reuse, or restart policy mismatch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Service patching, lock cleanup, or restart may briefly interrupt availability or remove a lock that still belongs to an active process. <br>
Mitigation: Confirm the target service and process identity, capture current service state and configuration, avoid deleting active locks, and keep a rollback path ready before applying changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xyezir/oc-evolver-restart-loop-fix) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with root cause analysis, patch summary, shell commands, and stability proof] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on minimal reversible service changes and post-fix restart-counter stability.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
