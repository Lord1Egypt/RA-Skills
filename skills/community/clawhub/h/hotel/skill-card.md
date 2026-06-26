## Description: <br>
Local-first hotel decision engine for trip stays, hotel comparison, shortlist creation, booking readiness, and accommodation planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIstack](https://clawhub.ai/user/AGIstack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel planners and agent users use this skill to capture trip context, compare hotel candidates, shortlist best-fit stays, and check whether a selected option has enough information for booking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel plans, travel dates, budgets, notes, and preferences are retained in local JSON files. <br>
Mitigation: Avoid storing secrets or highly sensitive personal details in hotel notes, and delete the local JSON files when the data is no longer needed. <br>


## Reference(s): <br>
- [Hotel Philosophy](references/philosophy.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/AGIstack/hotel) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores trip, hotel, and preference data in local JSON files under ~/.openclaw/workspace/memory/hotel.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
