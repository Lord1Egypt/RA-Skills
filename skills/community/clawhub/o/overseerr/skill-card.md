## Description: <br>
Request movies/TV and monitor request status via the Overseerr API (stable Overseerr, not the beta Seerr rewrite). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j1philli](https://clawhub.ai/user/j1philli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to search a configured Overseerr instance, create movie or TV requests, inspect request status, and monitor request updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user-supplied Overseerr API key and can perform actions allowed by that key. <br>
Mitigation: Use an API key with permissions appropriate for the intended requester and only configure trusted Overseerr instances. <br>
Risk: Ambiguous title searches can lead to requesting the first matching movie or TV result. <br>
Mitigation: Search first for ambiguous titles and confirm the intended media before creating a request. <br>
Risk: The monitor command polls continuously and can print request metadata to stdout. <br>
Mitigation: Stop the monitor when finished and avoid piping monitor output into shared logs when request metadata may be sensitive. <br>


## Reference(s): <br>
- [Overseerr homepage](https://overseerr.dev/) <br>
- [ClawHub skill page](https://clawhub.ai/j1philli/overseerr) <br>
- [Publisher profile](https://clawhub.ai/user/j1philli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts return JSON or newline-delimited JSON events.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node plus OVERSEERR_URL and OVERSEERR_API_KEY environment variables.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
