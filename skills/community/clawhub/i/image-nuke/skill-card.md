## Description: <br>
Cleans image metadata by stripping EXIF, GPS, camera, color profile, XMP/IPTC, thumbnail, and editing-history data, then re-encodes images with pixel-level noise changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cassh100k](https://clawhub.ai/user/cassh100k) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users working with local image files can use this skill to remove embedded image metadata and produce new JPEG outputs. It is best treated as a lossy local image transformer rather than a simple metadata scrubber. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill promotes anti-forensic image alteration and should not be relied on for claims of forensic untraceability. <br>
Mitigation: Use it only when lossy image transformation is intentional, and do not rely on it for forensic, legal, or evidentiary guarantees. <br>
Risk: The script can automatically install unpinned Python packages when dependencies are missing. <br>
Mitigation: Install and pin dependencies yourself in an isolated environment before running the script. <br>
Risk: The transformation is lossy and always emits JPEG output, which can make the result unsuitable for archival or evidentiary images. <br>
Mitigation: Keep original files and avoid using the transformed output as an archival or evidence-preserving copy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cassh100k/image-nuke) <br>
- [Publisher profile](https://clawhub.ai/user/cassh100k) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated JPEG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are lossy JPEG images; the script states that original files are not modified.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
