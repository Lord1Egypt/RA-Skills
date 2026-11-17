## Description:

HumanTyping types target text into a browser with human-like timing, adjacent-key mistakes, immediate and deferred corrections, French accent handling, pauses, and variable speed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luke2day](https://clawhub.ai/user/luke2day)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use HumanTyping to generate, preview, save, or replay realistic browser keystroke sequences into selected fields during OpenClaw-driven browser workflows. It supports deterministic seeds for repeatable tests or recordings and dry-run previews before typing into a page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can type text into the currently available browser page.

Mitigation: Open and inspect the intended page first, pass a specific selector, and verify the target field before running.

Risk: It can enter text into sensitive or production forms if directed there.

Mitigation: Use --dry-run when uncertain and avoid sensitive or production forms unless the typed text is explicitly intended for that page.

Risk: Browser typing depends on the intended OpenClaw/Chromium session being available.

Mitigation: Start the OpenClaw browser, navigate to the target page, and inspect the page before playback.

## Reference(s):

- [HumanTyping on ClawHub](https://clawhub.ai/luke2day/skills/human-typing-simulator)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON keystroke event scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can dry-run to preview events, save scripts for replay, inspect script statistics, or type into a selected browser field.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact files declare 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
