## Description:

Drive hostile or full-screen terminal UIs through the `ht` CLI from montanaflynn/headless-terminal when an agent needs reliable PTY-backed interaction, screen snapshots, or wait/synchronization for tools like `vim`, `top`, `htop`, `git add -p`, SSH-driven TUIs, installers, auth prompts, or REPLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inertia186](https://clawhub.ai/user/inertia186)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to decide when to drive redraw-heavy terminal programs through the `ht` CLI and how to synchronize, inspect, and clean up those sessions safely. It helps agents work with full-screen TUIs, REPLs, installers, SSH-driven terminal flows, and interactive commands that are unreliable under plain stdin/stdout control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Terminal screenshots, recordings, or session views can expose passwords, MFA prompts, tokens, production incidents, or confidential data.

Mitigation: Get approval before using `ht` for privacy-sensitive flows, avoid capturing secrets, and store or redact any screenshots or recordings safely.

Risk: Installing an unrelated package named `ht` or `headless-terminal` can put a different tool on PATH than the skill expects.

Mitigation: Install only the named Montana Flynn headless-terminal CLI from the Homebrew tap or official release artifacts, and verify support for commands such as `ht run`, `ht send`, and `ht view`.

Risk: Automating a real PTY can quickly perform destructive actions in remote systems, installers, or interactive prompts.

Mitigation: Use the smallest meaningful keystrokes, wait for deterministic screen conditions, inspect fresh views after state changes, and ask before destructive or remote TUI operations.

## Reference(s):

- [Headless Terminal Skill](SKILL.md)
- [Examples](references/examples.md)
- [Key Notation](references/keys.md)
- [Recipes](references/recipes.md)
- [Troubleshooting](references/troubleshooting.md)
- [Wait Strategies](references/waits.md)
- [montanaflynn/headless-terminal](https://github.com/montanaflynn/headless-terminal)
- [headless-terminal releases](https://github.com/montanaflynn/headless-terminal/releases)
- [asciicast v2 documentation](https://docs.asciinema.org/manual/asciicast/v2/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include terminal session commands, wait strategies, cleanup steps, and troubleshooting advice.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
