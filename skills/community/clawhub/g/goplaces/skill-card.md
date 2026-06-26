## Description: <br>
Query Google Places API (New) via the goplaces CLI for text search, place details, resolve, and reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to look up places, retrieve details and reviews, resolve location names, and request human-readable or JSON output from the goplaces CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Google Places API key and may send location queries over the network. <br>
Mitigation: Use a restricted Google Places API key with quota or billing limits, and avoid sharing the key in prompts or logs. <br>
Risk: GOOGLE_PLACES_BASE_URL can redirect requests away from the default Google Places endpoint when set. <br>
Mitigation: Leave GOOGLE_PLACES_BASE_URL unset unless intentionally using a trusted proxy or test endpoint. <br>
Risk: Installation depends on a third-party Homebrew tap and the goplaces CLI project. <br>
Mitigation: Install only after reviewing and trusting the Homebrew tap and goplaces project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steipete/goplaces) <br>
- [goplaces GitHub repository](https://github.com/steipete/goplaces) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the goplaces binary and GOOGLE_PLACES_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
