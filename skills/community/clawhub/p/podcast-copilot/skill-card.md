## Description: <br>
Podcast copilot workflows with the Podwise CLI for searching podcasts or episodes, checking followed-show updates, asking transcript-grounded questions, processing Podwise, YouTube, Xiaoyuzhou, and local media inputs, and retrieving transcripts, summaries, chapters, Q&A, mind maps, highlights, and keywords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skoowoo](https://clawhub.ai/user/skoowoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate the Podwise CLI for podcast discovery, transcript-grounded analysis, media processing, and retrieval of structured episode artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run the local Podwise CLI with the user's configured account. <br>
Mitigation: Install only when account-level Podwise CLI access is acceptable, and avoid sharing API-key or configuration output. <br>
Risk: Processing URLs or local media can upload selected content to Podwise and may consume quota or credits. <br>
Mitigation: Require explicit user confirmation before process commands and process only intended URLs or files. <br>
Risk: Transcript and summary retrieval depends on Podwise CLI availability, configuration, processing completion, and artifact support. <br>
Mitigation: Check the CLI environment first, wait for processing to finish, and mark unavailable artifacts explicitly. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/skoowoo/podcast-copilot) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/skoowoo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Podwise episode URLs, processing status, transcript-grounded answers, source excerpts when requested, and unavailable artifact notes.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
