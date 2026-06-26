## Description: <br>
Summarize URLs, local files such as PDFs, images, and audio, and YouTube links using the summarize CLI with customizable length and model options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users use this skill to generate concise or extended summaries from web pages, local documents, media files, and YouTube links through the summarize CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted files, URLs, page contents, and transcript data may be processed by SkillBoss and possibly downstream providers. <br>
Mitigation: Avoid sensitive or regulated content unless provider data handling has been reviewed, and keep remote fallbacks disabled when privacy matters. <br>
Risk: The skill requires a SKILLBOSS_API_KEY for remote model and fallback services. <br>
Mitigation: Store the key as an environment variable, limit access to trusted environments, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/kirk-summarize) <br>
- [summarize homepage](https://summarize.sh) <br>
- [Complete setup guide](https://skillboss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide use of JSON output, extraction-only mode, summary length options, model selection, and optional fallback handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
