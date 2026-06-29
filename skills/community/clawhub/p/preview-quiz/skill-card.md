## Description: <br>
Create a shareable RooQuiz preview quiz: a right/wrong assessment where correct answers earn points and the taker gets a score, then return a browser-openable preview link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rooquiz](https://clawhub.ai/user/rooquiz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and content creators use this skill to build a graded quiz JSON payload, submit it to RooQuiz's preview endpoint, and share a short-lived preview link for review or testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Quiz titles, questions, answers, descriptions, and links are sent to RooQuiz/Quizster to create a temporary preview. <br>
Mitigation: Do not use the skill with secrets, private business material, student records, health data, or other sensitive content; use a self-hosted deployment or optional secret when access control matters. <br>
Risk: Preview links are temporary and are not a permanent publishing mechanism. <br>
Mitigation: Recreate the quiz or publish it through RooQuiz if a durable form is needed. <br>


## Reference(s): <br>
- [Preview Quiz Skill Page](https://clawhub.ai/rooquiz/skills/preview-quiz) <br>
- [RooQuiz Preview API](https://preview.rooquiz.com/api/preview-forms) <br>
- [Quizster Preview Links](https://quizster.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON examples, HTTP request examples, shell commands, and preview URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces temporary preview links that expire after about one hour; an optional secret can be used when access control matters.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
