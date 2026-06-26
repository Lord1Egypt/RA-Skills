## Description: <br>
A toolkit for fuzzy string matching and data reconciliation, useful for matching entity names across datasets where spelling variations, typos, or formatting differences exist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and data engineers use this skill to compare non-identical string keys and reconcile entity names across datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional rapidfuzz installation could introduce dependency risk if installed from an untrusted package source. <br>
Mitigation: Install rapidfuzz only from trusted Python package sources and review dependency provenance before use. <br>
Risk: Entity matching on sensitive datasets can expose confidential data if run in an untrusted environment. <br>
Mitigation: Run matching workflows only in trusted environments with appropriate access controls for the source datasets. <br>
Risk: Fuzzy matching can create false positives or miss true matches when thresholds and normalization rules are poorly tuned. <br>
Mitigation: Validate matching thresholds against representative data and review uncertain matches before relying on the results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/invoice-fraud-detection-fuzzy-match) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands] <br>
**Output Format:** [Markdown with Python code blocks and inline shell package hints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python examples with difflib and optional rapidfuzz.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
