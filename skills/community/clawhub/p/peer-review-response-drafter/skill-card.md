## Description: <br>
Assist in drafting professional peer review response letters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Researchers, authors, and academic teams use this skill to turn reviewer comments and revision notes into a professional point-by-point response letter for journal or conference resubmission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: File input and output paths may reach outside the intended workspace. <br>
Mitigation: Check every input and output path before running; avoid absolute paths and ../ traversal until workspace-only path validation is added. <br>
Risk: Reviewer comments and manuscript details may contain confidential or unpublished information. <br>
Mitigation: Keep inputs and generated response letters out of shared or version-controlled folders unless they are approved for disclosure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/peer-review-response-drafter) <br>
- [Response Templates](references/response_templates.md) <br>
- [Tone Guide](references/tone_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style, plain-text, or LaTeX response letter] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read reviewer comments from stdin or a file and optionally write the drafted response letter to a selected output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
