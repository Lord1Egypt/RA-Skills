## Description: <br>
Identifies plant species from images or videos and returns structured species, taxonomy, growth habit, maintenance, recommendation, and report-link information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ClawHub users use this skill to analyze plant photos, videos, or URLs through the LifeEmergence cloud service for gardening, ecological survey, and natural education workflows. It can also query cloud-hosted historical plant recognition reports tied to the automatically managed user identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plant images or videos are sent to the LifeEmergence cloud service and may contain sensitive visual information. <br>
Mitigation: Avoid uploading sensitive media and confirm that the publisher's retention, deletion, and data-handling controls are acceptable before use. <br>
Risk: The skill silently creates or reuses an identity, stores tokens locally, and ties cloud reports to that identity. <br>
Mitigation: Review token-storage and account-deletion controls, and run the skill in an isolated environment when identity linkage is not acceptable. <br>
Risk: The skill can retrieve historical cloud reports associated with the automatically managed identity. <br>
Mitigation: Limit access to the runtime environment and verify that report-history queries are appropriate for the current user and context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/new-smyx-plant-species-recognition-analysis) <br>
- [API interface document](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files] <br>
**Output Format:** [Markdown text with structured JSON report content, progress messages, report links, and optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local file input, public URL input, cloud history listing, detail-level selection, and optional output-file writing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
