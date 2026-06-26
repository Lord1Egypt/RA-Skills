## Description: <br>
Generate shareable SVG and Markdown proof cards from a skill audit or release metadata for GitHub READMEs, landing pages, and ClawHub listings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill builders use this skill to create small, shareable proof cards from audit or release metadata for READMEs, landing pages, and ClawHub listings. It helps present score, grade, status, version, checked date, and links without hand-editing SVG. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A proof card can misstate score, status, grade, or link if the source audit or release metadata is stale or untrusted. <br>
Mitigation: Run the skill on trusted audit files and review the generated score, status, grade, and link before publishing. <br>
Risk: The --force option can overwrite existing output files. <br>
Mitigation: Use --force only when intentionally replacing known proof-card outputs. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/zack-dev-cm/proof-card-forge) <br>
- [Source manifest](references/source-manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with file paths, shell command examples, SVG output, and optional JSON summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces proof-card SVG and Markdown files, can emit a JSON summary, and refuses overwrites unless --force is used.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
