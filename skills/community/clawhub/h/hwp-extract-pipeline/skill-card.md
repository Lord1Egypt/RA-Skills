## Description: <br>
Extracts text from Korean HWP/HWPX and PDF or scan attachments through a local fallback pipeline using hwp-reader, pyhwp, HWPX parsing, and strings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heoboong](https://clawhub.ai/user/heoboong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract text from locally stored Korean HWP/HWPX and PDF-like document attachments and return structured JSON for downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted document text is written to local JSON files using a user-provided ID. <br>
Mitigation: Use simple IDs containing only letters, numbers, dashes, or underscores; run the skill from an intended output directory; delete generated JSON files when no longer needed. <br>
Risk: The extraction pipeline may invoke local hwp-reader, pyhwp, virtualenv, and strings binaries. <br>
Mitigation: Use only trusted local binaries and virtual environments, and validate the toolchain before processing sensitive documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heoboong/hwp-extract-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files] <br>
**Output Format:** [JSON emitted to stdout and written to a local *_extracted.json file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local input file path and record ID; may use local hwp-reader, pyhwp, virtualenv, and strings binaries when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
