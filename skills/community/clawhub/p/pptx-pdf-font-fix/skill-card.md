## Description: <br>
Fixes PowerPoint PDF font embedding issues by patching fully opaque PPTX text runs with minimal transparency so desktop PowerPoint exports use the intended fonts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chernojagne](https://clawhub.ai/user/chernojagne) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and presentation authors use this skill to repair PPTX files whose exported PDFs substitute default fonts despite embedded custom fonts. The skill runs a local patching script and returns a patched PPTX for review and desktop PowerPoint PDF export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally modifies slide XML formatting in a user-provided PPTX. <br>
Mitigation: Keep the original PPTX and review the patched presentation before relying on the exported PDF. <br>
Risk: The workaround depends on desktop PowerPoint PDF export and may not apply to server-side converters. <br>
Mitigation: Use PowerPoint desktop for the final PDF export and verify that the expected fonts are embedded. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chernojagne/pptx-pdf-font-fix) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and a patched PPTX file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local PPTX copy; PDF export remains a desktop PowerPoint step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
