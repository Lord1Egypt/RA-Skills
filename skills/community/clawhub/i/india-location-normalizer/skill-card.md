## Description: <br>
Normalizes Indian real-estate location text into canonical Mumbai and Pune city and locality fields with confidence scores and unresolved flags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vishalgojha](https://clawhub.ai/user/vishalgojha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External teams and developers use this skill after lead extraction to standardize Indian real-estate location hints before scoring, routing, analytics, or storage. It is intended for Mumbai and Pune locality normalization and flags ambiguous or low-confidence cases instead of forcing a match. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ambiguous aliases can create incorrect city or locality assignments for downstream routing, scoring, analytics, or storage. <br>
Mitigation: Review ambiguous aliases and make downstream steps respect confidence scores and unresolved_flag before automation. <br>
Risk: Coverage is limited to the supplied Mumbai and Pune alias map, so unsupported locations may remain unresolved. <br>
Mitigation: Treat unresolved outputs as requiring human or upstream review rather than canonical locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vishalgojha/india-location-normalizer) <br>
- [India location alias map](references/india-location-aliases-v1.json) <br>
- [Location normalizer input schema](references/location-normalizer-input.schema.json) <br>
- [Location normalizer output schema](references/location-normalizer-output.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, guidance] <br>
**Output Format:** [JSON matching references/location-normalizer-output.schema.json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [One normalized location record per input lead, including city, canonical locality, micro-market, matched alias, confidence, resolution method, and unresolved flag.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
