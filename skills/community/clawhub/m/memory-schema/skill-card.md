## Description: <br>
Schema lifecycle management for Basic Memory: discover unschemaed notes, infer schemas, create and edit schema definitions, validate notes, and detect drift. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phernandez](https://clawhub.ai/user/phernandez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base maintainers use this skill to manage structured note types in Basic Memory, including discovering repeated note structures, creating Picoschema definitions, validating notes, and detecting schema drift. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proposed schema writes, schema edits, or note fixes can change how Basic Memory notes are organized and validated. <br>
Mitigation: Review proposed write_note, edit_note, schema_validate, and schema_diff-driven changes before approval; start new schemas with warning-mode validation when strict enforcement is not yet needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phernandez/memory-schema) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with Picoschema YAML and Basic Memory tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose schema note writes, schema edits, validation checks, and drift reports for user review.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
