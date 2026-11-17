## Description:

Design effective excitation signals (step tests) for system identification and parameter estimation in control systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan bounded step-test excitation signals, choose duration and sample rate, and collect response data for control-system identification and parameter estimation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real-equipment step tests can exceed safe operating ranges or affect production and safety-critical systems.

Mitigation: Verify safe operating ranges, use small bounded inputs, confirm supervision and emergency stop capability, and complete a risk assessment before any production or safety-critical use.

Risk: Poorly designed excitation signals can produce incomplete or misleading data for parameter estimation.

Mitigation: Start from steady state, hold the input long enough to observe the response, sample fast enough to capture transients, and avoid input levels that saturate the system.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown guidance with a short Python data-collection example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces control-systems step-test guidance; no tools, credentials, or command execution required.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
