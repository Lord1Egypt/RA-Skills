## Description:

Pokémon GO PvP 培养查询技能 v1.1。基于 PvPokeTW 真实排行数据 + gamemaster 基础种族值，提供排名查询、最佳 IV、用户 IV 对比等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pigro0314](https://clawhub.ai/user/pigro0314)

### License/Terms of Use:

MIT-0

## Use Case:

External Pokémon GO PvP players use this skill to query PvPokeTW-based rankings, recommended moves, IV comparisons, team suggestions, and local roster priorities from Chinese-language commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local roster commands store Pokémon inventory data in data/my_pokemon.json, and /pvp 评估我的 can update missing recommended moves in that file.

Mitigation: Review and back up data/my_pokemon.json before use; in managed deployments, require explicit user confirmation before evaluation writes recommended moves.

Risk: Ranking, moveset, and gamemaster answers depend on external PvPoke/PvPokeTW data and local caches that may be stale or unavailable.

Mitigation: Refresh ranking and gamemaster caches on a defined schedule, surface cache timestamps, and return an unavailable-data message when authoritative data cannot be loaded.

Risk: The security evidence marks the release suspicious because the public description under-discloses local inventory writes.

Mitigation: Disclose file-write behavior in user-facing docs and review source behavior before installing or distributing the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pigro0314/skills/pogo-pvp)
- [PvPokeTW](https://pvpoketw.com/)
- [PvPoke GitHub repository](https://github.com/pvpoke/pvpoke)
- [PvPoke rankings data](https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/)
- [PvPoke gamemaster data](https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/gamemaster.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration, files]

**Output Format:** [Chinese-language Markdown/plain text command responses, with local JSON roster updates when inventory commands are used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on PvPoke/PvPokeTW ranking and gamemaster data caches; roster operations read or update data/my_pokemon.json.]

## Skill Version(s):

1.0.0 (source: server release metadata; skill text describes v1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
