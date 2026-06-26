## Description: <br>
News Sum Lite generates a lightweight Chinese daily news briefing from current news searches, saves it as Markdown, and can email it as an HTML report with the Markdown attached. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liliangjie91](https://clawhub.ai/user/liliangjie91) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or employees can use this skill to have an agent assemble a Chinese daily news digest across international affairs, economy/finance, and technology/AI. The workflow emphasizes sourced items, short Chinese summaries, daily takeaways, and an optional emailed report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create a local news archive and send the generated report through a local Gmail command without clear recipient or approval controls. <br>
Mitigation: Before any email is sent, require the agent to show the recipient, subject, body, and attachment path and obtain explicit user confirmation. <br>
Risk: The generated Markdown file may be attached and sent before the user has reviewed the report content. <br>
Mitigation: Review the saved report path and generated content before allowing the email command to run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liliangjie91/news-sum-lite) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown daily news briefing with source links, plus an HTML email body generated from the Markdown attachment.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese summaries are about 300 characters per news item; default topics are international affairs, economy/finance, and technology/AI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
