## Description: <br>
Musallat Bot is a Gemini 1.5 Flash-powered persona chatbot that answers prompts in a blunt, passive-aggressive senior-developer style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Musallat-Dev](https://clawhub.ai/user/Musallat-Dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers can use this skill to route a text prompt to a Gemini-backed persona bot for terse, intentionally abrasive technical replies. It is best suited to environments where that tone is acceptable and third-party AI processing is permitted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact text exposes an apparent Gemini API key, and the security review says it should not be relied on. <br>
Mitigation: Do not use the embedded key; revoke or rotate it if you own it, remove it from the skill, and provide your own restricted GEMINI_API_KEY. <br>
Risk: Prompts are sent to Google/Gemini for generation. <br>
Mitigation: Use only with prompts you are comfortable sending to that third-party service and follow your organization's data-handling rules. <br>
Risk: The bot is designed to produce intentionally rude, passive-aggressive responses. <br>
Mitigation: Limit use to contexts where that tone is acceptable, and review generated text before sharing it externally. <br>


## Reference(s): <br>
- [Musallat Bot ClawHub page](https://clawhub.ai/Musallat-Dev/musallat-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text chatbot response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses are generated from the user's prompt and may include intentionally rude persona language.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
