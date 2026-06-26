## Description: <br>
Batch compress image file sizes (JPG/PNG), keep dimensions, reduce volume. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ginntech](https://clawhub.ai/user/ginntech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to reduce JPG and PNG file sizes in batch while preserving image dimensions, especially for website static assets or other folders of oversized images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The compression script overwrites original image files in place. <br>
Mitigation: Run it on a copied folder or backed-up assets first, and target only the intended directory. <br>
Risk: Use with elevated privileges can modify production or system-owned assets. <br>
Mitigation: Run as a normal user when possible and avoid sudo unless file permissions require it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ginntech/img-compress) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The compression script overwrites image files in place and reports per-file and total size reductions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
