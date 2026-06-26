## Description: <br>
AI-agent Skill for PPTX OOXML localization workflows. Use it to unpack PPTX, extract and apply text translations, normalize terminology, enforce language-specific fonts, validate XML integrity, and repack outputs with machine-readable JSON interfaces for automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason2be](https://clawhub.ai/user/jason2be) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external automation agents use this skill to run PPTX OOXML localization workflows: unpacking presentations, extracting text, applying translated TSV content, normalizing terminology and fonts, validating XML, and repacking output PPTX files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and writes user-selected presentation files and directories, so an incorrect input, output, or root path could process the wrong local content. <br>
Mitigation: Run it only on presentations intended for localization and choose input, output, and root directories carefully before execution. <br>
Risk: Generated TSV files and repacked PPTX files may contain translation, terminology, or formatting issues. <br>
Mitigation: Review generated TSV and output PPTX files before production use, and run the XML and font validation steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jason2be/ppt-ooxml-tool) <br>
- [README](artifact/README.md) <br>
- [Release notes v0.1.0](artifact/RELEASE_NOTES_v0.1.0.md) <br>
- [Example job file](artifact/examples/job.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON job specifications, TSV translation files, and PPTX output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports machine-readable JSON responses through the CLI --json mode.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence, target metadata, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
