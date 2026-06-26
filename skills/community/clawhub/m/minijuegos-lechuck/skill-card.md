## Description: <br>
Helps developers integrate the Minijuegos.com and Miniplay LeChuck JavaScript SDK into HTML5 games for player authentication, achievements, stats, leaderboards, and related troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dreadterror](https://clawhub.ai/user/dreadterror) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers use this skill when adding Minijuegos or Miniplay platform integration to an HTML5 game. It provides guidance for SDK setup, player token validation, backend session handling, achievements, stats, leaderboards, and data flush behavior at game over. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Minijuegos write credentials or JWT signing secrets could be exposed if copied into client code, URLs, logs, or source control. <br>
Mitigation: Keep MINIPLAY_API_KEY and JWT_SECRET server-side, use environment variables, return session JWTs through HttpOnly cookies, and review generated code before deployment. <br>
Risk: Stats, achievements, or leaderboard updates may be lost if a game immediately reloads or resets after asynchronous SDK calls. <br>
Mitigation: Use sendBeacon where possible, delay game-over transitions when needed, or implement a server-side session endpoint when data reliability is critical. <br>
Risk: Loading a third-party SDK from the wrong origin or with incompatible cross-origin headers can break platform integration. <br>
Mitigation: Load the LeChuck SDK only from the official Minijuegos domain and use cross-origin headers compatible with the vendor script. <br>


## Reference(s): <br>
- [Backend auth endpoint, DB migration, and credential usage](references/backend.md) <br>
- [Achievements and stats definitions](references/achievements.md) <br>
- [Minijuegos LeChuck SDK release page](https://clawhub.ai/dreadterror/minijuegos-lechuck) <br>
- [Official Minijuegos LeChuck JavaScript SDK](https://ssl.minijuegosgratis.com/lechuck/js/latest.js) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance-only artifact; no executable skill code is bundled.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
