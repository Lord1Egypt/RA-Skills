## Description: <br>
Tracks garden pests and diseases, logs treatments, monitors effectiveness, and provides treatment recommendations for home gardeners and small farmers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johstracke](https://clawhub.ai/user/johstracke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users such as home gardeners and small farmers use this skill to record pest and disease observations, track treatment history, monitor treatment effectiveness, and get garden problem recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Treatment recommendations may be incomplete, outdated, or unsuitable for a specific crop, product, region, or edible-crop restriction. <br>
Mitigation: Verify the current product label, crop and pest compatibility, local rules, required protective equipment, child and pet precautions, and pre-harvest restrictions before acting. <br>
Risk: The skill stores garden problem notes, affected plants, severity, treatments, and effectiveness history locally. <br>
Mitigation: Use it only for information you are comfortable keeping in ~/.openclaw/workspace/pest_tracker_db.json and handle exported Markdown files accordingly. <br>
Risk: Exported reports can persist in safe local directories and may contain treatment history or garden notes. <br>
Mitigation: Export only to intended locations and review exported Markdown before sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johstracke/pest-disease-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [CLI text output, Markdown exports, and local JSON data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores pest, disease, treatment, and effectiveness records locally under ~/.openclaw/workspace/pest_tracker_db.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
