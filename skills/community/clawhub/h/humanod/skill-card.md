## Description: <br>
Give your AI agent hands in the real world. Hire verified humans for physical tasks, data collection, and physical verification via the Humanod network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Armandobrazil](https://clawhub.ai/user/Armandobrazil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use Humanod to create, monitor, assign, cancel, and validate paid real-world tasks performed by humans. Typical tasks include local photo collection, physical location checks, and submitted-proof review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend money by creating paid tasks and can release or reject payment for human work. <br>
Mitigation: Require the agent to summarize the task, worker choice, budget, location, and payment or rejection effect, then obtain explicit user confirmation before every modifying action. <br>
Risk: The API key is handled through an exposed query-parameter pattern. <br>
Mitigation: Use a dedicated, revocable Humanod API key with the least permissions available, rotate it if exposed, and verify the Humanod service and API endpoint before funding the account. <br>
Risk: Real-world task requests and proof review may expose private addresses, sensitive locations, personal data, or confidential business details. <br>
Mitigation: Avoid including sensitive details unless necessary, provide precise validation criteria, and review submitted proof before approving payment. <br>


## Reference(s): <br>
- [Humanod ClawHub release](https://clawhub.ai/Armandobrazil/humanod) <br>
- [Humanod documentation](https://docs.humanod.app) <br>
- [Humanod application](https://www.humanod.app) <br>
- [Humanod API endpoint](https://humanod-api.onrender.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Guidance] <br>
**Output Format:** [API requests and responses with concise natural-language task summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a HUMANOD_API_KEY and user confirmation before actions that create, assign, cancel, or validate paid tasks.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
