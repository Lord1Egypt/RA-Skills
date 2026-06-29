## Description: <br>
Tracks pharmaceutical regulatory sources including NMPA, CDE, FDA, EMA, and ICH, identifies new or updated regulations and guidance, analyzes applicability, tags topics, and generates PDF reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gxpcode-hezhong](https://clawhub.ai/user/gxpcode-hezhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Regulatory affairs, quality, and compliance teams use this skill to monitor selected pharmaceutical regulatory websites and feeds, compare new items against history, fetch details and attachments, and produce applicability-focused tracking reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs Python and browser dependencies before full web tracking functionality is available. <br>
Mitigation: Run setup in a controlled workspace, review the dependency list first, and install only when those dependencies are acceptable. <br>
Risk: The skill contacts external regulatory websites, downloads PDFs, and writes reports, history, and intermediate files. <br>
Mitigation: Use it only in the intended workspace, review generated reports before sharing, and avoid distributing outputs that expose sensitive local attachment paths. <br>
Risk: The skill can modify its configured regulatory source list and includes a local source-management panel. <br>
Mitigation: Run the panel only when needed, stop it afterward, and review source or parser changes before using newly added sources. <br>


## Reference(s): <br>
- [Skill Page](https://clawhub.ai/gxpcode-hezhong/skills/gxpcode-tu-xingsun) <br>
- [Publisher Profile](https://clawhub.ai/user/gxpcode-hezhong) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>
- [Configured Regulatory Sources](artifact/resources/sources.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON intermediate records, PDF reports, configuration updates, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download regulatory attachments and write reports, history, and intermediate data into the active workspace.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
