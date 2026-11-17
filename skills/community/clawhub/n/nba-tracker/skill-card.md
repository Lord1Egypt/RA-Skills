## Description:

NBA Tracker helps agents query NBA schedules, standings, player statistics, injury status, live scores, and close-game alerts using the nba_api library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luoruikun0531](https://clawhub.ai/user/luoruikun0531)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and NBA viewers use this skill to generate code, commands, and guidance for checking team records, daily schedules, player information, live scores, and close-game alerts. It is intended for game-viewing assistance rather than betting, prediction-market, or other low-latency decision workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Apple Calendar example can create local calendar events through unsafe AppleScript without clear consent or input escaping.

Mitigation: Do not run calendar automation unless the user explicitly asks for calendar changes; rewrite the integration to pass values as data or validate and escape event fields before any osascript use.

Risk: Live scores and stats may be delayed, throttled, or unavailable, and the artifact warns against betting or prediction-market use.

Mitigation: Use this skill for viewing assistance only; use professional low-latency data providers for betting, trading, or other time-sensitive financial decisions, and cache or rate-limit NBA API calls.

## Reference(s):

- [NBA API Reference](artifact/API_REFERENCE.md)
- [nba_api GitHub](https://github.com/swar/nba_api)
- [nba_api Documentation](https://github.com/swar/nba_api/tree/master/docs)
- [nba_api Examples](https://github.com/swar/nba_api/tree/master/docs/examples)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Python and shell command examples plus console-style text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on external NBA API availability, throttling behavior, and local environment configuration.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
