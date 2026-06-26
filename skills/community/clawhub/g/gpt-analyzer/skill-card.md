## Description: <br>
GPT-specific pattern detection with model fingerprinting and version identification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raghulpasupathi](https://clawhub.ai/user/raghulpasupathi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to analyze text for GPT-like writing patterns and receive a heuristic model label, confidence score, indicators, and recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GPT detection output is a rough heuristic and should not be treated as proof of GPT authorship or a specific model version. <br>
Mitigation: Use the result only as an advisory signal and require independent evidence for moderation, academic, employment, or other consequential decisions. <br>
Risk: The detectVersion and checkWatermarks options may imply analysis behavior that is not supported in this version. <br>
Mitigation: Do not rely on those options as adding separate detection behavior unless the implementation is independently verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raghulpasupathi/gpt-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, guidance] <br>
**Output Format:** [JSON-like JavaScript object with confidence scores, model label, indicators, and recommendation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Configurable minimum confidence threshold; detectVersion and checkWatermarks options should not be assumed to add real analysis behavior in this version.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
