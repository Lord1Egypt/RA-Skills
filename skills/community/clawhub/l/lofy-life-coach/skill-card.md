## Description: <br>
Lofy Life Coach helps an agent manage morning briefings, evening reviews, weekly reports, goal tracking, habit monitoring, streak counts, and adaptive nudges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrey401](https://clawhub.ai/user/harrey401) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users of a personal assistant use this skill to track routines, goals, workouts, career progress, and habit streaks through briefings, reviews, weekly resets, and natural-language updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal routine, workout, habit, career-progress, and daily-log data in a local goals file. <br>
Mitigation: Review or delete data/goals.json when needed, and avoid connecting calendar, fitness, or application context you do not want included in briefings. <br>
Risk: Automated nudges may feel intrusive or unhelpful when the user's current context is incomplete. <br>
Mitigation: Keep nudges limited and context-aware; the artifact caps nudges to one per topic per day and instructs the agent not to push harder when the user is having a rough day. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Concise text or Markdown briefings and reviews, with JSON updates to data/goals.json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Morning briefings are capped at 200 words and nudges are capped at 50 words.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
