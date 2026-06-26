## Description: <br>
Clean privacy-sensitive metadata (C2PA, EXIF, XMP, IPTC, GPS) from user-owned images by writing sanitized copies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiwork4me](https://clawhub.ai/user/aiwork4me) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and publishing teams use this skill to create sanitized image copies before sharing, publishing, or archiving files that may contain privacy-sensitive file metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be misused on images the user does not own or is not authorized to process. <br>
Mitigation: Confirm the user owns or is authorized to process the images before running cleanup. <br>
Risk: Batch runs or explicit output paths can produce unexpected output locations or replace existing cleaned outputs when overwrite is used. <br>
Mitigation: Run a dry-run before folder batches, review planned output locations, and use overwrite only after explicit confirmation. <br>
Risk: The verification scan is a quality check rather than proof that every possible provenance signal or marker was removed. <br>
Mitigation: Review verification results and avoid representing the output as free of all possible hidden or external provenance signals. <br>
Risk: The cleanup only affects file-level metadata and does not remove pixel-level watermarks, invisible signals, or external platform records. <br>
Mitigation: Use it for file metadata hygiene only and disclose that pixel-level and server-side provenance remain outside scope. <br>


## Reference(s): <br>
- [Technical Reference](references/technical-details.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aiwork4me/image-metadata-cleaner) <br>
- [GitHub Repository](https://github.com/AIwork4me/image-metadata-cleaner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON manifest output from the cleanup script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces sanitized image copies, human-readable summaries, and optional JSON manifests; input images are not overwritten unless an explicit overwrite option is used for outputs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
