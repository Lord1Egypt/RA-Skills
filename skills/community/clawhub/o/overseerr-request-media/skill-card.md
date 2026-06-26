## Description: <br>
Request movies or TV shows on Overseerr by title and optional season, checking availability before forwarding the request to Sonarr or Radarr. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trialskid](https://clawhub.ai/user/trialskid) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users with an Overseerr instance use this skill to ask an agent to search for movies or TV shows, resolve ambiguous matches, check whether media is already available or requested, and submit new Overseerr requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Overseerr API key to submit media requests. <br>
Mitigation: Store the API key securely and use the least-privileged key available for the intended Overseerr workflow. <br>
Risk: Ambiguous search results could lead to requesting the wrong movie or TV show. <br>
Mitigation: Review ambiguous title matches and have the agent ask the user to choose before submitting a request. <br>
Risk: The skill may create duplicate or unintended requests if availability or request status is unclear. <br>
Mitigation: Check Overseerr availability and request indicators before posting, and treat duplicate-request failures as already requested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/trialskid/overseerr-request-media) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Plain text confirmations or clarification prompts, with shell command examples in the skill guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OVERSEERR_URL and OVERSEERR_API_KEY environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
