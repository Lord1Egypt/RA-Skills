## Description: <br>
Interact with the openLesson tutoring API to generate learning plans, start audio-based sessions, analyze reasoning gaps, and manage tutoring workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dncolomer](https://clawhub.ai/user/dncolomer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an AI agent to openLesson for learning-plan generation, audio-only Socratic tutoring sessions, reasoning-gap analysis, and session summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an openLesson API key and sends spoken tutoring audio to the openLesson service. <br>
Mitigation: Install only when comfortable sharing that credential and audio with the service, and avoid submitting sensitive spoken content. <br>
Risk: The artifact includes proactive reminder and scheduling behavior that could be treated as calendar or notification action without a clear opt-in boundary. <br>
Mitigation: Treat reminders, notifications, and recurring follow-ups as opt-in only; review details before allowing an agent to create or persist them. <br>


## Reference(s): <br>
- [openlesson ClawHub release](https://clawhub.ai/dncolomer/open-lesson) <br>
- [openLesson Academy](https://www.openlesson.academy) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Markdown, Configuration guidance] <br>
**Output Format:** [Markdown guidance with JSON API payloads, curl commands, and Python examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENLESSON_API_KEY and base64-encoded audio in webm, mp4, or ogg format for analysis.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
