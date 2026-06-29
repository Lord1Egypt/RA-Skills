## Description: <br>
Run Kannaka's memory operations on real quantum hardware for quantum circuits, true quantum random numbers, and resonance recall as amplitude amplification on qBraid's free simulator or deliberately selected real QPUs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickflach](https://clawhub.ai/user/nickflach) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Kannaka Quantum to list quantum devices, run OpenQASM 3 circuits, generate quantum random values, and execute resonance recall on a simulator or an explicitly selected quantum backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real quantum hardware runs can spend qBraid or OpenQuantum credits if a paid backend is selected. <br>
Mitigation: Use the free simulator for routine work and require an explicit hardware device, allow_spend confirmation, low shot count, and max_credits ceiling before a real QPU run. <br>
Risk: The skill may rely on stored qBraid or OpenQuantum credentials when real hardware is used. <br>
Mitigation: Confirm the backend, credential source, shot count, and intended spend before enabling any paid run. <br>
Risk: Installing the external kannaka-quantum package executes third-party code in the user's environment. <br>
Mitigation: Review the package and install it only in an environment appropriate for the user's trust and security requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nickflach/skills/kannaka-quantum) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI subcommands return one JSON object to stdout, including errors, so agents can branch on structured results.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
