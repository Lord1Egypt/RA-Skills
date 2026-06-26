## Description: <br>
PDF Toolkit Pro provides local commands for merging, splitting, compressing, and batch-processing PDF files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gdp6539](https://clawhub.ai/user/gdp6539) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Office users, document managers, students, teachers, legal and accounting staff, designers, and automation users use this skill to prepare local PDF processing workflows for merge, split, compression, and batch operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation may fetch npm dependencies at install time, and the artifact does not include a lockfile. <br>
Mitigation: Pin dependencies, add and review a lockfile, and update glob to a patched version before using the skill with sensitive PDFs or in production. <br>
Risk: The PDF-to-image workflow currently writes per-page PDF files rather than actual PNG or JPG images. <br>
Mitigation: Verify generated outputs before relying on them and use a confirmed image conversion tool when image files are required. <br>


## Reference(s): <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/gdp6539/pdf-toolkit-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate on local PDF files and write outputs to user-selected paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
