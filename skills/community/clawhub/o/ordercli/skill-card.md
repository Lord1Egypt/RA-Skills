## Description: <br>
Foodora-only CLI for checking past orders and active order status (Deliveroo WIP). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate the ordercli command-line tool for Foodora order history, active order tracking, and guarded reorder workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chrome cookie and browser session import can delegate access to the user's Foodora account. <br>
Mitigation: Install only from a trusted ordercli package, prefer password-stdin or a dedicated browser profile, and confirm where imported sessions are stored and how to delete them. <br>
Risk: Reorder commands can change the user's cart when confirmed. <br>
Mitigation: Use preview mode first and require explicit user confirmation before running any reorder or cart-changing command. <br>


## Reference(s): <br>
- [Ordercli homepage](https://ordercli.sh) <br>
- [Ordercli ClawHub page](https://clawhub.ai/steipete/ordercli) <br>
- [Foodora Austria](https://www.foodora.at/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with ordercli shell commands, configuration examples, and optional JSON command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local ordercli binary; supports Foodora workflows now and documents Deliveroo as work in progress.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
