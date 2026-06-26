## Description: <br>
Interact with KitchenOwl APIs through a reusable CLI script for login, token handling, REST and GraphQL calls, and shopping-list read or update tasks on self-hosted or cloud KitchenOwl instances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pietro395](https://clawhub.ai/user/Pietro395) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to call KitchenOwl APIs from an agent workflow when they need to inspect or update shopping-list data without using the KitchenOwl web UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable KitchenOwl credentials locally and can access authenticated account data. <br>
Mitigation: Use HTTPS and a trusted KitchenOwl instance, prefer limited or revocable tokens, and restrict permissions on ~/.config/kitchenowl-api/session.json. <br>
Risk: Authenticated REST, POST, DELETE, or GraphQL mutation calls can change KitchenOwl data. <br>
Mitigation: Review and explicitly approve write operations before execution, especially requests that modify shopping-list items or account data. <br>
Risk: Passing passwords directly on the command line can expose credentials through shell history or process inspection. <br>
Mitigation: Avoid command-line passwords when possible and use token-based access or another credential handling method with lower exposure. <br>


## Reference(s): <br>
- [KitchenOwl API skill on ClawHub](https://clawhub.ai/Pietro395/kitchenowl-api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write local KitchenOwl session tokens and perform authenticated REST or GraphQL requests against the configured KitchenOwl instance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
