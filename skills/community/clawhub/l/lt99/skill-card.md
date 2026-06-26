## Description: <br>
Lt99 helps a player use a site-issued API key to call the $LT99 practice-game HTTP API for watching rounds, checking state, entering, betting, and viewing history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luyao-inc](https://clawhub.ai/user/luyao-inc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate the LT99 practice-game API with a user-provided Bearer API key, including round observation, account state checks, entry, betting, and history review. It is intended for agents that can make real HTTP requests and run curl-style API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent access to a sensitive LT99 API key and betting authority. <br>
Mitigation: Use only a limited LT99 practice account with a revocable key, and require confirmation of the digit, amount, and request destination before each bet. <br>
Risk: The API base URL can be overridden by environment variables. <br>
Mitigation: Confirm the request destination is the intended earninghub.ai LT99 API before sending authenticated requests, and avoid overrides unless the user controls them. <br>
Risk: The agent could report round state, balance, or streak values that were not returned by the API. <br>
Mitigation: Require successful HTTP JSON responses before making user-facing claims, and do not infer fields that are absent from responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luyao-inc/lt99) <br>
- [Publisher profile](https://clawhub.ai/user/luyao-inc) <br>
- [Project homepage](https://github.com/luyao-inc/LT99) <br>
- [LT99 game page](https://www.earninghub.ai/game/lt99/) <br>
- [LT99 API base](https://www.earninghub.ai/lt99-api) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline HTTP and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a user-provided Bearer API key and may require curl or another tool capable of POST requests.] <br>

## Skill Version(s): <br>
1.4.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
