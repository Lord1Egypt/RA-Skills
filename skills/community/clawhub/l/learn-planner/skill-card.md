## Description: <br>
Generates seven-day learning plans, topic quizzes, and local study progress summaries for common technical learning topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners, instructors, and developer enablement teams use this skill to create short study plans, generate basic quizzes, and track completion milestones locally without requiring an account or network access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the skill executes local Bash and Python code and writes progress data under the user's home directory. <br>
Mitigation: Review the script before use and run it only where creating ~/.local/share/education-skill/progress.json is acceptable. <br>
Risk: Generated learning plans and quizzes are built-in guidance and may be incomplete for specialized or current topics. <br>
Mitigation: Use the generated material as a starting point and verify important learning resources against authoritative documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/learn-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal-formatted text with structured plan, quiz, and progress sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Progress is stored locally under ~/.local/share/education-skill/progress.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
