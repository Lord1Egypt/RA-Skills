## Description: <br>
Harden OpenClaw browser extension relay behavior by eliminating blank-target tab churn, fixing download behavior forwarding, and standardizing download paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielsinewe](https://clawhub.ai/user/danielsinewe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when hardening or debugging OpenClaw extension-relay browser sessions, especially flaky target creation, missing download behavior, and inconsistent download locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Relay-mode downloads are standardized to ~/Downloads/OpenClaw, which may be unsuitable when sessions handle sensitive downloaded files. <br>
Mitigation: Confirm that path is acceptable for the workflow and manage or clear downloaded files according to the user's data-handling requirements. <br>
Risk: Reusing blank browser targets can interact with existing browser session state during extension-relay testing. <br>
Mitigation: Use isolated browser profiles or test sessions when sensitive tabs may be open, then verify that blank target reuse behaves as expected before broader use. <br>


## Reference(s): <br>
- [OpenClaw Browser Relay Reliability release](https://clawhub.ai/danielsinewe/openclaw-browser-relay-reliability) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands] <br>
**Output Format:** [Markdown guidance with file paths, implementation direction, and verification steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires rg for repository search. Guidance is instruction-only and produces no executable payload by itself.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
