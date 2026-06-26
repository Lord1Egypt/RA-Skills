## Description: <br>
Converts a user-provided PPTX presentation into a structured Markdown speech script by extracting slide text, speaker notes, and slide thumbnails for the agent to rewrite into a coherent talk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qigaiai](https://clawhub.ai/user/qigaiai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers can use this skill to turn a PPTX file into a polished Markdown speech draft with slide-thumbnail references. It is suited for presentation preparation, internal talks, training material, and converting slide content into a more natural spoken narrative. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically download large LibreOffice and Poppler dependencies during normal use. <br>
Mitigation: Install LibreOffice and poppler-utils manually before running the skill when download provenance, network access, or reproducibility matters. <br>
Risk: On Linux, missing Poppler dependencies may trigger package-manager installation that can require sudo. <br>
Mitigation: Run the agent without passwordless sudo and preinstall required packages in a controlled environment. <br>
Risk: The final Markdown speech draft may overwrite an intermediate Markdown file generated from the PPTX. <br>
Mitigation: Keep backups of generated Markdown outputs and review the output path before allowing the agent to write final content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qigaiai/ppt-to-speech) <br>
- [Example speech output](examples/sample_speech.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, files, shell commands, guidance] <br>
**Output Format:** [Markdown speech draft with relative image references and companion PNG thumbnail files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May overwrite the intermediate Markdown output; the extraction script also creates a thumbnail directory next to the input file.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata; artifact frontmatter lists 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
