## Description: <br>
Polish a technical blog draft into an 1000-1200 word, 4-5 section en-US article, preserve technical terms/code, and generate consistent hero + per-section image prompts when the user asks to polish and translate a blog with images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j3ffyang](https://clawhub.ai/user/j3ffyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and external users can use this skill to polish a local technical blog draft into an en-US article package and prepare coordinated hero and section image prompts. Review is needed before publishing because the security evidence reports that the workflow may produce placeholder or incomplete blog content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports that the workflow may write canned placeholder content instead of reliably polishing the supplied draft. <br>
Mitigation: Review generated Markdown against the original draft before publishing, and treat the output as a draft until a human confirms accuracy and completeness. <br>
Risk: The skill reads from a local draft path and writes generated files to a local output directory. <br>
Mitigation: Keep draftPath and outputDir pointed at non-sensitive locations and inspect outputs before sharing them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, structured JSON fields, image prompt text, and shell workflow output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes polished markdown and intended image filenames to a local output directory; image files are only produced when an image-generation tool is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
