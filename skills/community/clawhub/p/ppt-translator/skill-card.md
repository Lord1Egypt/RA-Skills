## Description: <br>
Translate PPTX presentations to another language while preserving slide layout through a render-and-verify workflow that can check for text overflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nimo1987](https://clawhub.ai/user/Nimo1987) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, employees, and developers use this skill to translate editable PPTX presentations while retaining the original slide layout. It supports agent workflows that extract slide text, supply translations, rewrite the presentation, and verify rendered slides before returning the final file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation text and rendered slide images may be processed through the user's configured translation or Vision workflow. <br>
Mitigation: Use approved model and data-handling settings for sensitive decks, and avoid sending confidential content to services that are not cleared for that data. <br>
Risk: Layout preservation depends on the calling agent performing verification and retries, not on the script alone. <br>
Mitigation: Review rendered slides before relying on the final PPTX, and rerun or adjust scaling when overflow or formatting issues remain. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Code, Guidance] <br>
**Output Format:** [PPTX file with optional PNG render, JSON/log text, and agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python-pptx and LibreOffice; supports PPTX input and output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
