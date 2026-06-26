## Description: <br>
Automated academic writing assistant based on a three-layer architecture: Framework Layer, Summary Layer, and Body Layer. Organizes all files in a structured project directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MRchenkuan](https://clawhub.ai/user/MRchenkuan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Students, researchers, and academic-writing teams use this skill to organize long-form papers, process references, generate document frameworks, write section drafts, and keep framework, summary, and body layers synchronized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and overwrite local thesis project files, including draft body files and synchronization data. <br>
Mitigation: Use a dedicated project directory with backups or version control, and review changes before allowing body generation or synchronization. <br>
Risk: Synchronization can replace existing draft content when framework, summary, or body layers change. <br>
Mitigation: Inspect proposed edits and keep recoverable checkpoints before synchronizing modified sections. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown, JSON project files, and concise status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update files under the selected academic-writing project directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
