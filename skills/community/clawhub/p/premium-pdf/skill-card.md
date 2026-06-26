## Description: <br>
Generate premium enterprise-style PDFs from markdown content, with automatic de-AI text humanization and a professional Navy + Gold design system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreasozzo](https://clawhub.ai/user/andreasozzo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert markdown or text into polished PDF reports, proposals, and enterprise documents. It can also rewrite common AI-sounding phrases before rendering, so generated documents should be reviewed when exact wording matters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency hygiene issues may arise from unpinned reportlab and Pillow versions. <br>
Mitigation: Install the skill in an isolated Python environment and pin vetted dependency versions before use. <br>
Risk: The de-AI pass intentionally rewrites some wording, which can change exact phrasing in generated PDFs. <br>
Mitigation: Review generated PDFs before sharing them when exact wording or compliance language matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andreasozzo/premium-pdf) <br>
- [Project homepage](https://github.com/andreasozzo/SkillsAI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [PDF file generated from markdown, with command output reporting the generated file path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 on macOS or Linux and Python packages reportlab and Pillow.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
