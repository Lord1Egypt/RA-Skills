## Description: <br>
Orthogonal API Platform helps agents search, discover, integrate, and call paid APIs through the Orthogonal SDK, Run API, or x402 direct payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChristianPickettCode](https://clawhub.ai/user/ChristianPickettCode) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to find paid APIs, inspect endpoint details and pricing, generate integration snippets, and run selected API calls through Orthogonal credits or x402 payment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate paid API calls through /v1/run or x402 payment flows. <br>
Mitigation: Require explicit approval before every paid request, including review of the target API, request body, destination, and price. <br>
Risk: API keys or payment credentials could expose spend authority if used too broadly. <br>
Mitigation: Use a restricted Orthogonal API key and avoid main wallet private keys; prefer a dedicated low-balance wallet or safer secret storage for payment flows. <br>
Risk: Search and list results may surface endpoints that are broader than the user's intended task. <br>
Mitigation: Prefer targeted search over bulk listing, inspect endpoint details and pricing, and confirm the selected API before integration or execution. <br>


## Reference(s): <br>
- [Orthogonal Homepage](https://orthogonal.com) <br>
- [Orthogonal Dashboard Documentation](https://orthogonal.com/dashboard/docs) <br>
- [Orthogonal API Discovery](https://orthogonal.com/discover) <br>
- [Orthogonal API Base URL](https://api.orth.sh/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with JSON responses, cURL commands, and JavaScript or Python code snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paid API call requests and x402 payment examples; review target API, request body, destination, and price before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
