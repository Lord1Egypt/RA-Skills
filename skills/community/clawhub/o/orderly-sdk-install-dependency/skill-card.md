## Description: <br>
Install Orderly SDK packages and related dependencies (hooks, UI, features, wallet connectors) using the preferred package manager. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tarnadas](https://clawhub.ai/user/Tarnadas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers building Orderly Network DEX integrations use this skill to choose and install the SDK, UI, feature, wallet connector, Tailwind, and Vite dependency sets needed for their project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package installation commands could add unintended or unpinned dependencies to a production wallet or DEX project. <br>
Mitigation: Review package names before running commands, consider pinning versions, and audit dependencies before production use. <br>
Risk: Wallet connector setup may require extra dependency and browser polyfill choices that affect runtime behavior. <br>
Mitigation: Install only the wallet connector path required by the project and verify Tailwind and Vite configuration changes in the target application. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Tarnadas/orderly-sdk-install-dependency) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, TypeScript, and CSS code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces package installation guidance and configuration snippets for JavaScript and React projects.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
