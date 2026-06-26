## Description: <br>
Tutor Buddy Pro provides step-by-step interactive homework help using the Socratic method, with study plans, adaptive quizzes, progress tracking, and learning-style adaptation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Students, parents, and learners use this skill for guided homework support, exam preparation, quiz practice, and progress summaries across common academic subjects. It is designed to coach the learner through concepts rather than simply provide final answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive learner profiles, quiz results, session logs, and study plans, which may involve children or classroom use. <br>
Mitigation: Install only where local storage of learner data is acceptable, keep generated data files protected, and avoid collecting personal details beyond what is needed for tutoring. <br>
Risk: Dashboard sync plans conflict with the local-only privacy claims if they are enabled or implemented without clear consent and controls. <br>
Mitigation: Do not enable or build dashboard sync until the destination, authentication, consent, retention, and deletion controls are explicit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nollio/normieclaw-tutor-buddy-pro) <br>
- [Publisher profile](https://clawhub.ai/user/nollio) <br>
- [README](artifact/README.md) <br>
- [Security and Data Handling](artifact/SECURITY.md) <br>
- [Dashboard Specification](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>
- [Tutor Configuration](artifact/config/tutor-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local learner profiles, quiz history, session logs, study plans, progress reports, and dashboard configuration when the hosting agent executes the documented setup or reporting flows.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
