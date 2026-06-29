## Description: <br>
Create a shareable RooQuiz preview scorecard, a scored questionnaire where each option adds points toward a total that buckets into levels, and get a link to open in the browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rooquiz](https://clawhub.ai/user/rooquiz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to draft, validate, and create temporary RooQuiz scorecard previews for self-assessments, readiness checks, maturity checks, surveys, and other scored questionnaires. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to send questionnaire content to a public RooQuiz preview endpoint. <br>
Mitigation: Review the generated JSON for sensitive or inappropriate content before approving the request. <br>
Risk: Generated preview links are temporary and may be unsuitable as permanent published forms. <br>
Mitigation: Use preview links only for short-lived review and recreate or publish through RooQuiz when a durable form is needed. <br>
Risk: Generated commands or HTTP requests could target the wrong endpoint when environment overrides are used. <br>
Mitigation: Review the exact endpoint, request body, and command before execution. <br>


## Reference(s): <br>
- [Preview Scorecard on ClawHub](https://clawhub.ai/rooquiz/skills/preview-scorecard) <br>
- [RooQuiz Preview API](https://preview.rooquiz.com/api/preview-forms) <br>
- [RooQuiz Preview Link Base](https://quizster.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON examples, HTTP request details, shell command examples, and preview-link guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a short-lived RooQuiz preview link that expires after about 1 hour.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
