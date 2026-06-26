## Description: <br>
Use this OpenClaw / ClawHub skill when the user wants to turn three ordinary sentences into a verified build-ready prompt bundle for a real app: PC desktop, macOS, Windows, iOS, Android, HarmonyOS, WeChat MiniProgram, self-hosted local web, PWA, or CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peixl](https://clawhub.ai/user/peixl) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and app-building agents use this skill to turn short app ideas into verified Markdown prompt bundles with platform route, template, acceptance, packaging, security, i18n, assumptions, and caveats. It is intended for prompt-bundle generation and verification, not for silently installing SDKs, building apps, or submitting to app stores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generated prompt bundle may instruct a downstream coding agent to install dependencies, run build tools, modify files, use network access, or request deployment credentials. <br>
Mitigation: Review the generated bundle before handing it to another agent, and treat platform SDK use, signing, deployment, and store submission as explicit opt-in implementation work. <br>
Risk: The skill can write prompt-bundle files in the active workspace. <br>
Mitigation: Keep execution workspace-scoped and review the reported output path, assumptions, verification result, and caveats before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/peixl/ifq-app-builder) <br>
- [Homepage](https://github.com/peixl/ifq-app-builder) <br>
- [Quickstart](README.en.md#first-run) <br>
- [Mode Routing](references/modes.md) <br>
- [Platform Matrix](references/platform-matrix.md) <br>
- [Three-Sentence Contract](references/three-sentence-contract.md) <br>
- [Verification](references/verification.md) <br>
- [Security Baseline](references/security-baseline.md) <br>
- [Agent Compatibility](references/agent-compatibility.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown prompt bundle with verification command and evidence summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a workspace-scoped *.prompt.md bundle; verification is typically performed with npm run verify:lite -- <bundle.prompt.md> when shell access is available.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter, package.json, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
