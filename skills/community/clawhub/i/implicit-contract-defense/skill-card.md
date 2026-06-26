## Description: <br>
Provides a Rust, SeaORM, and frontend development workflow that concentrates API contracts, constants, and database entities into explicit boundaries to prevent implicit contract drift. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiamu-ssr](https://clawhub.ai/user/xiamu-ssr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when working on Rust backends with SeaORM, any frontend, and a database to establish explicit API, constants, and entity contracts and to run local checks that catch drift. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts inspect source files and gen_types.sh runs the local Rust test flow. <br>
Mitigation: Run the scripts only in the intended Rust/SeaORM workspace and review the script configuration paths before execution. <br>
Risk: gen_types.sh rewrites the selected frontend types file. <br>
Mitigation: Point it at a generated file path and review the resulting diff before relying on the output. <br>
Risk: The artifact examples contain a Cancelled-status documentation mismatch. <br>
Mitigation: Treat the examples as patterns and align the status enum with documented transitions before adopting them as canonical. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiamu-ssr/implicit-contract-defense) <br>
- [check_contracts.sh](references/check_contracts.sh) <br>
- [gen_types.sh](references/gen_types.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include project-specific file layout guidance and paths for generated frontend type output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
