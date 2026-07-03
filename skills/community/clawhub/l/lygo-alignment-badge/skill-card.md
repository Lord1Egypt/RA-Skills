## Description: <br>
Verify LYGO node compliance across P0 golden SHA, stack demo, Phase 1 elasticity, Phase 3-4 federation, optional Grok audit, lattice checks, and emit JSON or Markdown badge results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deepseekoracle](https://clawhub.ai/user/deepseekoracle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check LYGO node alignment status and surface ALIGNED or NEEDS_FIX badge results from the verifier. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Badge results can mislead users if an agent claims ALIGNED without running the verifier. <br>
Mitigation: Run the documented verifier command and surface the actual JSON or Markdown result. <br>
Risk: Third-party repository badge output may be untrusted before review. <br>
Mitigation: Quarantine untrusted repositories and review verifier output before relying on the badge. <br>
Risk: Quick health checks do not cover the full alignment audit. <br>
Mitigation: Run the full badge check before claiming production alignment. <br>


## Reference(s): <br>
- [LYGO Protocol Stack GitHub](https://github.com/DeepSeekOracle/lygo-protocol-stack) <br>
- [LYGO Protocol Stack Documentation](https://deepseekoracle.github.io/lygo-protocol-stack/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with bash commands; verifier output is JSON or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports ALIGNED or NEEDS_FIX badge status from verifier output; full audit requires non-quick mode.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
