## Description:

Fetch Iberian day-ahead electricity prices for Portugal and Spain from OMIE via the OMIEData library, plan cheapest appliance or EV charging windows, compare PT vs ES prices, and trigger smart-home actions from price thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmagnomuller](https://clawhub.ai/user/pmagnomuller)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Portugal and Spain OMIE day-ahead prices, compare markets, and plan low-cost appliance or EV charging windows. It can also propose or execute smart-home control commands from configured price thresholds.

### Deployment Geography for Use:

Portugal and Spain

## Known Risks and Mitigations:

Risk: Control mode can run user-provided shell commands on the local machine when execution is enabled.

Mitigation: Keep control in dry-run mode until thresholds and command strings are reviewed; enable execution only for commands you wrote and verified.

Risk: Local .env handling can affect runtime behavior and may execute shell syntax when sourced by the wrapper.

Mitigation: Keep .env local and controlled, and avoid using configuration files from untrusted sources.

Risk: The release depends on unpinned Python packages for production use.

Mitigation: Install in an isolated environment and pin OMIEData and pandas versions before production deployment.

## Reference(s):

- [OMIE](https://www.omie.es)
- [OMIEData Python package](https://pypi.org/project/OMIEData/)
- [ClawHub skill page](https://clawhub.ai/pmagnomuller/skills/omie-energy)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Control actions are dry-run unless execution is explicitly enabled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
