## Description: <br>
Plan reproducible ML experiment runs with explicit parameters, metrics, and artifacts. Use before model training to standardize tracking-ready experiment definitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x-Professor](https://clawhub.ai/user/0x-Professor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and ML practitioners use this skill before model training to create tracking-ready experiment plans with explicit datasets, parameters, metrics, thresholds, and expected artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script reads a caller-supplied JSON file and writes to a caller-supplied output path, so unintended paths could expose or overwrite project files. <br>
Mitigation: Use only intended input files and choose output paths inside the project or artifact directory; review generated files before relying on them. <br>
Risk: The --dry-run option records dry_run in the generated plan but does not prevent file output. <br>
Mitigation: Do not treat --dry-run as a no-write safety control; point --output at a disposable or intended artifact path. <br>


## Reference(s): <br>
- [Tracking Guide](references/tracking-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance plus generated JSON, Markdown, or CSV run-plan files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script reads an optional JSON payload up to 1 MiB and writes the selected output format to a caller-provided path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
