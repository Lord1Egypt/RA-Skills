## Description: <br>
Translates ArXiv papers into close-reading Chinese Markdown, preserves full paragraph-level detail, adds explicit translator notes, validates formatting, and prepares IMA Knowledge Base and Tencent Docs variants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fandywang87](https://clawhub.ai/user/fandywang87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create complete Chinese translations of ArXiv papers with structured Markdown, formulas, figures, references, and platform-specific preparation for IMA Knowledge Base and Tencent Docs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can upload generated Markdown and images to IMA Knowledge Base and Tencent Docs. <br>
Mitigation: Confirm upload destinations and authorization steps with the user before executing upload or token configuration commands. <br>
Risk: Private manuscripts or restricted notes could be exposed if processed through the same upload workflow. <br>
Mitigation: Use the workflow for public ArXiv papers unless the user explicitly approves handling and uploading restricted content. <br>
Risk: Translation or formatting errors can misrepresent paper details, formulas, figures, references, or acronym expansions. <br>
Mitigation: Run the included validation script and manually check first acronym expansions, figure placement, references, and LaTeX macro compatibility before publishing. <br>


## Reference(s): <br>
- [Platform Compatibility and Lessons Learned](references/platform-compat.md) <br>
- [Translation Iteration History](references/iteration-history.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/fandywang87/paper-translation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Chinese Markdown translations with inline shell command snippets and platform-specific Markdown variants] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces IMA and Tencent Docs Markdown variants; requires confirmation before upload or token configuration steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
