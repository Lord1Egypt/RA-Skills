## Description: <br>
Track and synthesize podcasts with subscriptions, briefings, progress tracking, and smart alerts for new episodes and guests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to manage podcast subscriptions, prioritize listening queues, generate episode briefings, and track guests or topics across audio and YouTube podcasts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local podcast records may retain subscriptions, listening progress, guest watchlists, summaries, and inferred interests. <br>
Mitigation: Use explicit podcast commands and review or delete ~/podcasts/ when local listening history or summaries should not be retained. <br>
Risk: Processing episodes may involve media-download or transcription tools when the user asks for summaries or briefings. <br>
Mitigation: Run those tools only for explicit user requests and review the generated transcript or summary before relying on it. <br>
Risk: Transcript-derived summaries and quotes can be wrong when based on auto-generated captions or imperfect transcription. <br>
Mitigation: Disclose transcript source quality and verify important quotes, timestamps, and claims against the original episode. <br>


## Reference(s): <br>
- [Briefings & Summaries](briefings.md) <br>
- [Discovery & Recommendations](discovery.md) <br>
- [Learning Mode](learning.md) <br>
- [YouTube Video Podcasts](youtube.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown summaries, tables, checklists, and concise recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain local Markdown records under ~/podcasts/ for subscriptions, queues, briefings, knowledge, and guest tracking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
