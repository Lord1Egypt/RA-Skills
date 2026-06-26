## Description: <br>
Power system network data formats and topology. Use when parsing bus, generator, and branch data for power flow analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to interpret MATPOWER-style power-grid network data, including bus, generator, branch, reserve, and load fields for power flow analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unreviewed network JSON files may contain unexpected or malformed data that could lead to incorrect analysis. <br>
Mitigation: Review network JSON files before analysis and parse them with structured JSON tooling before deriving power-system summaries. <br>
Risk: Installing scientific Python packages from untrusted sources can introduce supply-chain risk. <br>
Mitigation: Install NumPy and related packages only from trusted package indexes or approved internal mirrors. <br>
Risk: Very large network files can waste time and context if inspected line by line. <br>
Mitigation: Use Python's JSON parser for summaries and only run line-count or file-size checks when needed. <br>


## Reference(s): <br>
- [PGLib-OPF benchmark library](https://github.com/power-grid-lib/pglib-opf) <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/grid-dispatch-operator-power-flow-data) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/wu-uk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers MATPOWER-style network JSON data, including topology, bus types, per-unit values, reserve fields, bus-number mapping, branch interpretation, and load summaries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
