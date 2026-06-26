## Description: <br>
Read and trade on Manifold Markets by searching markets, fetching probabilities, inspecting users and bets, and preparing bets, share sales, or comments only after explicit user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Crotalus](https://clawhub.ai/user/Crotalus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent search Manifold Markets, inspect market and user data, and prepare account actions such as bets, share sales, and comments. Actions that spend funds or post content require the user's explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent use a Manifold account for actions that spend funds or post content. <br>
Mitigation: Install only when account access is intended, keep MANIFOLD_API_KEY private, prefer a revocable key when available, and approve every proposed bet, sale, or comment before execution. <br>
Risk: A trade or sale could target the wrong market, side, amount, or limit if details are ambiguous. <br>
Mitigation: Fetch the market first, restate the market question, identifier, action, side, amount or shares, and any limits, then stop and ask when required details are missing. <br>
Risk: Comments submitted through the API may post user-visible content and can incur a fee. <br>
Mitigation: Confirm the exact comment text and target market before submitting the API request. <br>


## Reference(s): <br>
- [Manifold Markets](https://manifold.markets) <br>
- [Manifold API Documentation](https://docs.manifold.markets/api) <br>
- [Manifold Markets Skill on ClawHub](https://clawhub.ai/Crotalus/manifold) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for command examples and MANIFOLD_API_KEY for write actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
