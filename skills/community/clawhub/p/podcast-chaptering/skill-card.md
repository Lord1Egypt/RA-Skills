## Description: <br>
Podcast Chaptering helps agents generate podcast chapters, highlights, show notes, social captions, and Markdown, JSON, SRT, VTT, or ID3 outputs from transcripts, with optional batch processing and API deployment guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, production teams, and developers use this skill to turn podcast transcripts into chapter markers, highlights, show notes, social copy, and platform-ready output formats. Developers can also use it as guidance for batch workflows or a FastAPI-style chaptering service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Podcast transcripts may be sent to an external AI provider during AI chaptering. <br>
Mitigation: Confirm provider privacy settings and avoid confidential or unpublished material unless the account and provider terms meet the user's privacy requirements. <br>
Risk: Batch processing can read and write many transcript and output files. <br>
Mitigation: Use a scoped input and output directory, review generated files before publication, and avoid running the workflow on unrelated folders. <br>
Risk: API deployment can expose chapter generation endpoints to unauthorized callers. <br>
Mitigation: Protect FastAPI deployments with authentication and restrict access before accepting remote uploads or batch jobs. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, Python code snippets, shell commands, and chaptering outputs such as Markdown, JSON, SRT, VTT, and ID3 metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include batch-processing summaries, social media captions, API deployment guidance, and human-review recommendations for chapter boundaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
