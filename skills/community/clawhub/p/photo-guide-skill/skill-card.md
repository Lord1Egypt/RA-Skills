## Description: <br>
Photo Guide helps agents analyze uploaded photos, infer likely shooting parameters, extract EXIF data when available, and provide beginner-friendly shooting, editing, lighting, props, and learning guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dcison](https://clawhub.ai/user/dcison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and photography beginners use this skill to understand how a reference photo may have been shot, compare EXIF metadata when available, and get practical shooting and post-processing suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Photo metadata may include sensitive camera, date, device, or GPS fields. <br>
Mitigation: Process only user-provided images, disclose that EXIF fields may be read, and avoid sharing location metadata unless the user explicitly approves. <br>
Risk: The skill can install Python dependencies, changing the runtime environment. <br>
Mitigation: Review requirements.txt and install dependencies in a sandbox or virtual environment before use. <br>
Risk: The artifact claims local, read-only processing, but server security evidence says those privacy claims should be tightened. <br>
Mitigation: Verify the EXIF script and agent workflow before deployment, and document the exact local files and metadata fields that may be read. <br>


## Reference(s): <br>
- [Photo Guide ClawHub release](https://clawhub.ai/dcison/photo-guide-skill) <br>
- [Photography parameter reference](references/photography-basics.md) <br>
- [Photography style templates](references/style-templates.md) <br>
- [Post-processing guide](references/post-processing-guide.md) <br>
- [EXIF extraction utility](scripts/extract_exif.py) <br>
- [AgentSkills standard](https://agentskills.io/home) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown analysis report with tables and optional JSON EXIF data from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include inferred camera-setting ranges when EXIF data is absent; follows the user's language.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
