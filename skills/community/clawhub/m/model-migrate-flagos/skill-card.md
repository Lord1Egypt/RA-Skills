## Description:

Migrates model code from the latest vLLM upstream repository into the vllm-plugin-FL project pinned at vLLM v0.13.0, including compatibility adaptation, registration, and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wbavon](https://clawhub.ai/user/wbavon)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to backport newly released upstream vLLM model implementations into vllm-plugin-FL. It guides code copying, compatibility patches, model registration, tests, benchmarking, serve/request smoke tests, and token-level E2E comparison against an upstream server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can forcibly terminate GPU processes during benchmark or serve setup.

Mitigation: Run only in an isolated development environment and require user confirmation before terminating processes.

Risk: The skill can launch local or remote vLLM services that may be broadly reachable or unauthenticated.

Mitigation: Bind services to localhost or a protected network and restrict access before serving models.

Risk: The workflow uses trust-remote-code for model serving and benchmarking.

Mitigation: Review exact model code before enabling trust-remote-code, or disable it when not required.

Risk: Remote E2E verification can use SSH with disabled host-key checking and root-style defaults.

Mitigation: Validate remote configuration values, use non-root SSH, and enable host-key checking before remote execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wbavon/skills/model-migrate-flagos)
- [README](artifact/README.md)
- [Migration Procedure](artifact/references/procedure.md)
- [vLLM 0.13.0 Compatibility Patches](artifact/references/compatibility-patches.md)
- [Operational Rules](artifact/references/operational-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown progress updates with inline shell commands, code edits, configuration guidance, and verification reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify vllm-plugin-FL model and config files, run local or remote vLLM verification commands, and write benchmark or E2E result files during migration.]

## Skill Version(s):

1.1.0 (source: server release evidence; artifact frontmatter metadata version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
