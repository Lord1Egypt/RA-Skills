## Description:

Integrate Minijuegos.com (Miniplay) LeChuck JS SDK into HTML5 games, including authentication, achievements, stats, leaderboards, backend registration, and game-over data flushing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreadterror](https://clawhub.ai/user/dreadterror)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game engineers use this skill to integrate HTML5 games with the Minijuegos/Miniplay LeChuck SDK, authenticate players, and implement platform stats, achievements, leaderboards, and supporting backend endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sample backend patterns could allow authenticated users to submit stats for another player if copied without hardening.

Mitigation: Derive miniplay_id from the authenticated server-side session, validate and bound all submitted stats, and authorize writes server-side before sending them to Minijuegos.

Risk: Token-bearing Minijuegos authentication URLs and server secrets could be exposed through logs or client code.

Mitigation: Redact token-bearing URLs from logs and keep MINIPLAY_API_KEY and JWT_SECRET exclusively on the server.

Risk: Sample user responses may expose more account data than an application needs.

Mitigation: Return only an explicit allowlist of public user fields from backend endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dreadterror/skills/minijuegos-lechuck)
- [Minijuegos LeChuck SDK](https://ssl.minijuegosgratis.com/lechuck/js/latest.js)
- [Backend - Minijuegos Auth Endpoint](artifact/references/backend.md)
- [Achievements & Stats - Minijuegos.com](artifact/references/achievements.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes JavaScript, Nginx, SQL, environment variable, and Express/Node.js examples.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
