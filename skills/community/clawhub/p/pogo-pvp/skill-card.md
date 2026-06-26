## Description: <br>
Pokemon GO PvP helper that uses PvPokeTW rankings and PvPoke gamemaster data to answer ranking, moveset, IV comparison, inventory, training-priority, missing-core, and team-building queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pigro0314](https://clawhub.ai/user/pigro0314) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and Pokemon GO PvP players use this skill to query PvP rankings, recommended moves, IV fit, local Pokemon inventory, training order, missing team pieces, and suggested PvP teams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store and update a local Pokemon inventory in data/my_pokemon.json. <br>
Mitigation: Review the local inventory file after commands that add, evaluate, or update Pokemon records. <br>
Risk: The skill refreshes public PvPoke data from GitHub and may use cached data when refreshes fail. <br>
Mitigation: Confirm the cache refresh status before relying on rankings for time-sensitive PvP decisions. <br>
Risk: Missing moves may be auto-filled with recommended moves during evaluation. <br>
Mitigation: Check generated or updated move entries against the user's actual Pokemon before planning resource use. <br>
Risk: The release evidence includes unrelated crypto and purchase capability tags. <br>
Mitigation: Do not grant crypto, purchase, or other unrelated authority to this skill if a platform prompt offers it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pigro0314/pogo-pvp) <br>
- [PvPokeTW](https://pvpoketw.com/) <br>
- [PvPoke Rankings Data](https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/) <br>
- [PvPoke GitHub Repository](https://github.com/pvpoke/pvpoke) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown-style text responses with tables, rankings, recommended moves, IV comparisons, inventory summaries, and team recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update a local data/my_pokemon.json inventory and refresh public PvPoke data caches.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
