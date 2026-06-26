## Description: <br>
Prepare input files for molecular docking software, automatically determine Grid Box center and size, and generate AutoDock Vina or AutoDock4 configuration files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and computational biology developers use this skill to prepare receptor and ligand inputs, calculate grid box dimensions, and generate docking configuration files before running AutoDock Vina or AutoDock4. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local file reads and writes can overwrite existing docking configuration files when paths are reused. <br>
Mitigation: Run the tool in a project workspace, provide explicit input and output paths, and avoid pointing output at files that should be preserved. <br>
Risk: Docking setup quality depends on prepared structure files and correct active-site, ligand, or manual grid inputs. <br>
Mitigation: Review receptor preparation, ligand references, residue selections, and grid dimensions before relying on generated docking configurations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/protein-docking-configurator) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with shell and Python examples; generated docking configuration files are plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local receptor and ligand structure files and writes AutoDock Vina config.txt or AutoDock4 .gpf outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
