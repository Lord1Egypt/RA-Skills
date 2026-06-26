## Description: <br>
Phy Proto Break Check compares versions of Protobuf and gRPC .proto files and classifies compatibility changes as critical, breaking, non-breaking, or informational. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill before merging Protobuf or gRPC schema changes to find wire-compatibility, generated-stub, and migration risks. It can compare git revisions, directories, or before-and-after proto files and produce findings suitable for release review or CI gating. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local .proto files and may inspect git history in repositories or directories selected by the user. <br>
Mitigation: Run it only against intended repositories and paths, and avoid pointing it at unrelated sensitive source trees. <br>
Risk: Generated CI fail-gate commands could affect build or release automation if copied without review. <br>
Mitigation: Review the proposed command and scope before adding it to CI or release workflows. <br>
Risk: The artifact uses regex-based proto parsing rather than protoc, so unusual or complex proto syntax may require human review. <br>
Mitigation: Treat findings as compatibility review support and pair them with established proto tooling or manual review for complex schemas. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-proto-break-check) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown findings with migration guidance, inline code or shell commands, and an optional CI fail-gate command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Groups findings by severity and highlights concrete migration steps for breaking changes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
