## Description: <br>
LLM hallucination detector with dual strategy (UQLM + rule-based fallback). Scores any AI output's confidence and flags potential hallucination risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[li8476295-bot](https://clawhub.ai/user/li8476295-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI practitioners use this skill to assess LLM-generated text or selected file fields for hallucination risk before critical actions such as code execution, SQL use, or external sends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external uqlm Python package when using its primary scoring path. <br>
Mitigation: Install it in an isolated Python environment, verify the intended PyPI package, and pin versions before relying on it for important workflows. <br>
Risk: Confidence scores and rule-based flags can miss hallucinations or overstate risk. <br>
Mitigation: Use the result as a review aid and keep human review for critical decisions, especially before code execution, SQL use, or external sends. <br>


## Reference(s): <br>
- [Hallucination Check on ClawHub](https://clawhub.ai/li8476295-bot/hallucination-check) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Plain text or JSON with confidence score, risk status, flags, and suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can analyze direct input text or a selected field from a file.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
