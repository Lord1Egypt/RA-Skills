## Description: <br>
Post updates to LinkedIn, track analytics, and optimize content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yadavabhijeet4](https://clawhub.ai/user/yadavabhijeet4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to draft, preview, publish, and review LinkedIn posts, with optional Gemini-based feedback before publishing and analytics from local post history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LinkedIn access tokens can authorize publishing posts and may be exposed by token helper output. <br>
Mitigation: Use only with an account and app where the requested posting scope is acceptable; store tokens in local environment variables and avoid running token helpers in logged terminals or CI. <br>
Risk: Draft content or research notes can be sent to Google Gemini during draft generation or feedback. <br>
Mitigation: Use --no-feedback for sensitive drafts and keep secrets or confidential material out of research_notes.md. <br>
Risk: The skill can publish public LinkedIn posts when run with the confirmation flag. <br>
Mitigation: Review preview output before publishing and reserve --confirm for posts approved for public release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yadavabhijeet4/linkedin-ai-optimizer) <br>
- [Publisher profile](https://clawhub.ai/user/yadavabhijeet4) <br>
- [LinkedIn Developers apps](https://www.linkedin.com/developers/apps) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, files] <br>
**Output Format:** [Plain text and Markdown terminal output, plus JSONL history entries for published posts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preview mode is the default for posting; publishing requires an explicit confirmation flag.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
