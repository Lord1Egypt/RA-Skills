## Description: <br>
科学计算工具 handles arithmetic, trigonometric, logarithmic, square-root, exponentiation, and factorial requests by routing them to an external calculator API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alinklab](https://clawhub.ai/user/alinklab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, researchers, and other users can ask for common scientific calculations and receive a summarized result. Use requires an API key and sends calculation inputs to an external service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an API key, stores it locally in .env, and sends calculation inputs to an external service. <br>
Mitigation: Install only when comfortable with local API-key storage and external processing; prefer a local-only calculator for ordinary scientific calculations. <br>
Risk: The scanner found the remote API dependency and credential handling unexpected for a scientific calculator. <br>
Mitigation: Review the publisher's service, data handling, and credential retention expectations before using the skill with sensitive inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alinklab/skills/math-genie-calc) <br>
- [XiaoBenYang API key page](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown or plain text summaries of JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY_APIKEY value and sends calculation inputs to an external API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
