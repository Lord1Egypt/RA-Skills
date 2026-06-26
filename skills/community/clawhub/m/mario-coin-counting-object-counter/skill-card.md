## Description: <br>
Count occurrences of an object in the image using computer vision algorithm. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to count instances of a visual object in an image by running a local OpenCV template-matching script with an example object image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Template matching can produce inaccurate counts when the sample object differs from targets in scale, rotation, lighting, occlusion, or threshold sensitivity. <br>
Mitigation: Use representative object images, tune threshold and dedup_min_dist, and manually review results when counts influence decisions. <br>
Risk: The script reads local image files supplied by path. <br>
Mitigation: Run it only on image files you intend to process, use a virtual environment, and install dependencies from trusted sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lnj22/mario-coin-counting-object-counter) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lnj22) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with bash command examples and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The count depends on the supplied input image, object image, threshold, and deduplication distance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
