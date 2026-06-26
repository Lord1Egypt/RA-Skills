## Description: <br>
Avoid common Linux kernel mistakes - atomic context violations, allocation failures, and locking traps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and kernel engineers use this skill as a quick reference for avoiding common Linux kernel mistakes around atomic context, allocation, user pointers, memory ordering, module cleanup, and locking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Kernel guidance can be incomplete for a specific kernel version, subsystem, or driver context. <br>
Mitigation: Review suggested practices against the target kernel tree and subsystem documentation before applying them to real kernel code. <br>
Risk: Applying low-level kernel advice without validation can contribute to crashes, deadlocks, allocation failures, or information leaks. <br>
Mitigation: Use code review, isolated development kernels, and kernel debugging options before promoting related changes to privileged or production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/kernel) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ivangdavila) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown reference guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Content-only Linux kernel guidance with no disclosed execution, persistence, credential, or data-transfer behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
