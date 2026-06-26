## Description: <br>
Renames academic PDF papers to standardized "[Year] [Venue] Title.pdf" filenames through an Extract, Verify, Rename workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[67available](https://clawhub.ai/user/67available) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to organize academic PDF folders by extracting candidate metadata, verifying it manually or with web search, and safely previewing or executing standardized renames. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatically extracted PDF metadata can be incorrect or incomplete. <br>
Mitigation: Review the generated manifest and add verified title, year, and venue values before marking files ready for rename. <br>
Risk: Batch rename execution changes local filenames. <br>
Mitigation: Run preview mode first and rely on the script-created timestamped backup before using execute mode. <br>


## Reference(s): <br>
- [Manifest Schema](references/manifest_spec.md) <br>
- [Standard Venue Abbreviations](references/venue_abbrev.md) <br>
- [Common Mistakes and Anti-patterns](references/anti_patterns.md) <br>
- [ClawHub Release Page](https://clawhub.ai/67available/pdf-rename) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands, Python configuration edits, JSON manifests, and rename previews] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or updates manifest files and local PDF filenames when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
