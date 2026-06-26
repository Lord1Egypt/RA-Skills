## Description: <br>
Production orchestration for pptx page task extraction and batch image delivery by reusing main-image-editor + psd-automator. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dhrxy](https://clawhub.ai/user/dhrxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and production operators use this skill to turn PPTX task decks into structured batch image-editing work, execute the edits against PSD workflows, and package the generated image deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads PPTX and request files and may process local image assets through OCR and related automation. <br>
Mitigation: Review PPTX and request inputs before execution, avoid untrusted inputs, and run dry-run first. <br>
Risk: The skill can edit PSD workflows and write delivery directories and ZIP archives. <br>
Mitigation: Keep backups or version control for important PSDs, set an explicit delivery.outputDir and simple zipName, and verify outputs after the run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dhrxy/ppt-task-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Files] <br>
**Output Format:** [JSON execution summaries with generated image directories and ZIP archives] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run mode reports planned work without copying output files; successful runs can produce a delivery directory and all-images.zip.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
