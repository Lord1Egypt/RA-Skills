## Description:

Manage CloudRobo assets across repositories, catalogs, versions, tags, Actions, permissions, marketplace search, lineage, and local-to-OBS import and export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud developers and engineers use this skill to query and manage CloudRobo repositories, catalogs, assets, versions, tags, Actions, permissions, and lineage, and to import or export asset files through OBS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled test script's preview operations may delete real cloud assets.

Mitigation: Use disposable resources and narrowly scoped credentials; avoid production credentials and existing asset IDs, and confirm deletion targets before running lifecycle operations.

Risk: The setup instructions document insecure connection settings.

Mitigation: Set CLOUDROBO_VERIFY_SSL=true before connecting.

Risk: The external SDK's runtime behavior was not tested.

Mitigation: Review the SDK behavior and rehearse operations with disposable resources before using it against production assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cloudrobo-asset)
- [API Paths](references/api-paths.md)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [IAM Policies](references/iam-policies.md)
- [Validation Rules](references/validation-rules.md)
- [Edge Cases](references/edge-cases.md)
- [Verification Method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance, shell commands, CloudRobo operation results, and exported asset files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operation results depend on CloudRobo permissions and available repositories, catalogs, and assets.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
