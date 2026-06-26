## Description: <br>
Generates Chinese Junqi dark-piece layouts with an LLM, validates them against fixed rules, and renders approved layouts as image cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imcaptor](https://clawhub.ai/user/imcaptor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players or agents use this skill to draft style-specific Junqi dark-piece layouts, validate them against placement and piece-count rules, and render approved layouts as shareable cards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generated Junqi layout can violate the skill's placement rules if it is returned before validation. <br>
Mitigation: Validate every generated layout with the bundled validator and regenerate or correct the layout before returning or rendering it. <br>
Risk: The renderer creates parent folders and writes an image to the requested output path. <br>
Mitigation: Use trusted JSON layout inputs and choose an output path in an intended workspace location. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imcaptor/junqi-dark-layout) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance, files] <br>
**Output Format:** [Markdown or JSON layout data, with optional shell commands and rendered image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Layouts use a 30-cell array with 25 playable positions and 5 fixed forbidden positions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
