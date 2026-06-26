## Description: <br>
Comprehensive command-line tools for modifying and manipulating images, such as resize, blur, crop, flip, and many more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and command-line users use this skill to get ImageMagick command guidance for local image edits such as resizing, cropping, blurring, orientation fixes, color adjustments, and format conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wildcard image operations may process many local files or modify more images than intended. <br>
Mitigation: Review generated ImageMagick commands before running them and test broad patterns on a small copy of the target files. <br>
Risk: Installing ImageMagick from an untrusted source can introduce supply-chain risk. <br>
Mitigation: Install ImageMagick only from a trusted package source for the target operating system. <br>
Risk: License terms are unclear because the skill frontmatter references a LICENSE.txt that is not present in the artifact. <br>
Mitigation: Confirm the applicable license with the publisher before relying on the skill in contexts where license terms matter. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lnj22/mario-coin-counting-image-editing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local ImageMagick command examples and dependency installation guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
