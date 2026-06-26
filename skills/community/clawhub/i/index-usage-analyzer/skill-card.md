## Description: <br>
Analyzes database indexes and suggests redundant ones to remove for schema optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ink5725](https://clawhub.ai/user/ink5725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database maintainers use this skill to inspect SQLite index metadata, identify indexes whose names match redundant patterns, and produce advisory cleanup recommendations for schema optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads SQLite schema metadata and writes a recommendation file under /root/.schema. <br>
Mitigation: Install and run it only where access to that schema metadata and output path is acceptable. <br>
Risk: Generated indexes_to_drop recommendations may be incomplete or incorrect for a target schema. <br>
Mitigation: Treat the recommendations as advisory and review them manually before allowing any other tool to drop indexes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Guidance] <br>
**Output Format:** [JSON report and recommendation JSON file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes advisory recommendations to /root/.schema/recommendation.json and does not modify the database.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
