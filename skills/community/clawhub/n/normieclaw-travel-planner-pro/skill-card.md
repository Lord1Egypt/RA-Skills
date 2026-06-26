## Description: <br>
Travel Planner Pro helps an agent build day-by-day travel itineraries with budget estimates, weather-aware activity planning, packing lists, document checklists, local tips, and shareable trip summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and their agents use this skill to plan personal travel, maintain travel preferences, compare destinations, prepare packing and document checklists, generate trip reminders, and produce readable itinerary summaries for companions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel profiles, itineraries, budgets, companion details, and document checklists can reveal sensitive personal travel patterns. <br>
Mitigation: Store only necessary trip details, avoid raw passport numbers, loyalty member numbers, confirmation codes, and unnecessary companion data, and review local files before sharing them. <br>
Risk: Destination research, weather lookups, shared itineraries, and optional dashboard sync can expose trip metadata to third parties. <br>
Mitigation: Assume external lookups and sync features disclose destination, date, or location metadata; redact sensitive fields and require explicit user confirmation before sending or syncing itineraries. <br>
Risk: Setup and reminder workflows can write files or run shell scripts in the user's workspace. <br>
Mitigation: Ask for confirmation before file writes or script execution, keep generated files under the intended travel/config/scripts paths, and review script behavior before installation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nollio/normieclaw-travel-planner-pro) <br>
- [README](README.md) <br>
- [Security guidance](SECURITY.md) <br>
- [First-run setup guide](SETUP-PROMPT.md) <br>
- [Travel configuration](config/travel-config.json) <br>
- [Trip reminder script](scripts/trip-reminder.sh) <br>
- [Dashboard specification](dashboard-kit/DASHBOARD-SPEC.md) <br>
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON snippets, shell commands, and plain-text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local travel profile, itinerary, budget, packing, reminder, and shareable Markdown files when the user confirms writes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
