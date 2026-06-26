## Description: <br>
HTML-to-PPTX converter that turns HTML slide decks into editable widescreen PPTX files while embedding local CSS and mapping common HTML elements to native PowerPoint shapes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iiustrator](https://clawhub.ai/user/iiustrator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and presentation authors use this skill to convert HTML slide content into editable PPTX decks for later review and editing in presentation tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input HTML can trigger outbound network requests when image elements reference remote URLs. <br>
Mitigation: Review HTML before conversion and run the skill in a network-restricted environment when processing untrusted inputs. <br>
Risk: Dependencies are specified with minimum versions rather than exact pins. <br>
Mitigation: Pin and review Python dependencies before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iiustrator/html2pptx-shape) <br>
- [Publisher profile](https://clawhub.ai/user/iiustrator) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [Runtime requirements](artifact/requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Code, Guidance] <br>
**Output Format:** [PPTX files, command-line output, and Python return data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates 16:9 Office Open XML presentation files; default output name is <input>_converted.pptx unless an output path is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact changelog, released 2026-04-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
