## Description: <br>
Transforms academic paper text into university-style press releases for general audiences, alumni, and media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Communications staff, researchers, and agents use this skill to turn academic paper content into a structured university press release draft. It produces headlines, lead copy, body text, quotes, boilerplate, and media contact fields for human review before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated quotes and media contact details may be placeholders or otherwise unverified. <br>
Mitigation: Replace quotes and contact information with approved real information before publication. <br>
Risk: Press release summaries may misstate or oversimplify the source paper. <br>
Mitigation: Review the generated draft against the paper and correct scientific claims before release. <br>
Risk: The local script can write output files to a path supplied by the user. <br>
Mitigation: Run the script only with intended inputs and output paths inside the expected workspace. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/lay-press-release-writer) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON press release draft with optional Markdown guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print JSON to stdout or write it to a user-specified output path; generated quotes and media contact details require review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
