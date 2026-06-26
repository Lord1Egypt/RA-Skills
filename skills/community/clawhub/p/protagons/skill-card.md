## Description: <br>
Browse, search, deploy, and generate Protagon AI character identities, including SOUL.md personality content that an agent can adopt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[protagons-dev](https://clawhub.ai/user/protagons-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use Protagons to browse, search, deploy, and generate portable AI character identities for an agent session. Deployed characters return SOUL.md persona guidance that the caller reviews and decides how to apply. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Returned SOUL.md persona text can conflict with normal safety, tool, or user instructions. <br>
Mitigation: Review any returned SOUL.md before applying it, and do not let character text override normal safety, tool, or user instructions. <br>
Risk: The generation feature sends a Google/Gemini API key to api.usaw.ai for a server-side Gemini call. <br>
Mitigation: Use the generation feature only when comfortable sending the key to that service, and prefer a scoped, limited, or throwaway key. <br>


## Reference(s): <br>
- [Protagons ClawHub listing](https://clawhub.ai/protagons-dev/protagons) <br>
- [Protagons product homepage](https://usaw.ai/voices) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, API Calls] <br>
**Output Format:** [Markdown and JSON-like tool responses with character summaries, categories, SOUL.md persona content, status details, and generation job information.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only browse, search, get, deploy, category, and status tools require no credentials; generation requires a Google/Gemini API key sent to api.usaw.ai for a single server-side call.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
