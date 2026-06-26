## Description: <br>
Uploads IELTS reading review JSON files to a hosted dashboard so users can review records and progress trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dengjiawei1226](https://clawhub.ai/user/dengjiawei1226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External IELTS learners use this skill to upload existing reading review JSON data and open a personal dashboard that shows historical reviews and progress trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The upload workflow sends the selected review file, a persistent machine-derived ID, and the local username to tuyaya.online. <br>
Mitigation: Install and use only if that data sharing is acceptable; override the generated user ID or username through environment variables when appropriate. <br>
Risk: Generated dashboard URLs include an API key. <br>
Mitigation: Do not share generated dashboard URLs and rotate or replace credentials if a URL is exposed. <br>
Risk: The skill includes a fallback command that downloads a script from GitHub. <br>
Mitigation: Avoid the fallback download path unless the fetched script has been reviewed and trusted. <br>
Risk: Optional HTML inputs can add unrelated local content to the upload payload. <br>
Mitigation: Upload only intended review artifacts and avoid attaching unrelated HTML files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dengjiawei1226/ielts-review-upload) <br>
- [Publisher profile](https://clawhub.ai/user/dengjiawei1226) <br>
- [IELTS reading dashboard](https://tuyaya.online/ielts/reading.html) <br>
- [IELTS API endpoint](https://tuyaya.online/ielts-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and dashboard URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a user-specific dashboard URL containing an API key.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
