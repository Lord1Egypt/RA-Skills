## Description: <br>
Drive hostile or full-screen terminal UIs through the `ht` CLI from montanaflynn/headless-terminal when an agent needs reliable PTY-backed interaction, screen snapshots, or deterministic wait/synchronization for tools like `vim`, `top`, `htop`, `git add -p`, SSH-driven TUIs, installers, auth prompts, or REPLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inertia186](https://clawhub.ai/user/inertia186) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to decide when to control a real terminal UI through `ht`, send small keystroke sequences, wait for deterministic screen conditions, capture terminal state, and clean up sessions safely. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing an unrelated or untrusted package named `ht` or `headless-terminal` could give the agent the wrong tool or introduce supply-chain risk. <br>
Mitigation: Install from the named Montana Flynn headless-terminal project or another explicitly trusted source, and verify the installed CLI supports the expected `ht run`, `ht send`, and `ht view` commands. <br>
Risk: PTY control over remote, authentication, or destructive terminal flows can quickly affect real systems or expose sensitive data. <br>
Mitigation: Require deliberate approval for privacy-sensitive, remote, authentication, or destructive flows, send only small keystroke sequences, and inspect fresh terminal snapshots before continuing. <br>
Risk: Screenshots, terminal recordings, and snapshots can capture secrets or private terminal contents. <br>
Mitigation: Protect, redact, or delete captured terminal artifacts according to the sensitivity of the session. <br>


## Reference(s): <br>
- [Headless Terminal project](https://github.com/montanaflynn/headless-terminal) <br>
- [Headless Terminal releases](https://github.com/montanaflynn/headless-terminal/releases) <br>
- [Examples](references/examples.md) <br>
- [Key notation](references/keys.md) <br>
- [Wait strategies](references/waits.md) <br>
- [Recipes](references/recipes.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Asciicast v2 documentation](https://docs.asciinema.org/manual/asciicast/v2/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend text or PNG terminal snapshots and asciicast recordings when appropriate.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
