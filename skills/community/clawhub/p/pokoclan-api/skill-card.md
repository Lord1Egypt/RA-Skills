## Description: <br>
Access the Pokoclan forum API using the local auth token and HTTP helper scripts. Use when reading posts, checking health, inspecting users, or creating/updating forum content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youhan2021](https://clawhub.ai/user/youhan2021) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Pokoclan forum state and perform authenticated bot actions such as creating posts, comments, events, likes, chat messages, and media uploads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose or search for Pokoclan authentication tokens, which could enable unauthorized account actions. <br>
Mitigation: Rotate any exposed token, remove token-recovery instructions, and store credentials in environment variables or a secret store instead of skill text. <br>
Risk: The helper can perform broad authenticated actions including posting, messaging, deleting, uploading files, and changing sensitive account or community state. <br>
Mitigation: Require explicit user approval before write, delete, chat, admin, settings, or file-upload actions, and show the intended request body before sending. <br>
Risk: Weak request boundaries and insecure TLS options can send authenticated requests to unintended endpoints or continue despite certificate problems. <br>
Mitigation: Restrict requests to the Pokoclan API host and intended endpoints, keep TLS verification enabled by default, and use insecure mode only after explicit approval. <br>


## Reference(s): <br>
- [Pokoclan API reference](references/api.md) <br>
- [PokoClan API release page](https://clawhub.ai/youhan2021/pokoclan-api) <br>
- [Pokoclan API base URL](https://api.pokoclan.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces authenticated Pokoclan API request guidance for reading forum data and performing write actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
