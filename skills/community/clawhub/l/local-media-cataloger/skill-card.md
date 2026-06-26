## Description: <br>
Index local photos, videos, and creative assets into a searchable manifest with tags, dates, shoot info, and reuse ideas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, media managers, and developers use this skill to inventory user-selected local media folders, generate media manifests, identify duplicate candidates, and plan archive or delivery structures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script enumerates files under the folder path selected by the user, which can expose local media filenames and metadata in the generated manifest. <br>
Mitigation: Run the skill only on a specific project or media directory, avoid broad personal or cloud-sync roots, and review the CSV or JSON manifest before sharing it. <br>
Risk: Folder plans or duplicate candidates could lead to unwanted renames, moves, merges, or deletion if applied without review. <br>
Mitigation: Treat organization and duplicate handling as a preview first, then make changes only after the user explicitly confirms the intended scope and action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/local-media-cataloger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional CSV or JSON manifest artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should use explicit assumptions and preview file organization or duplicate handling before suggesting changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
