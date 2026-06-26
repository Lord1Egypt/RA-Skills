## Description: <br>
Build and deploy safety-profiled gogcli binaries with compile-time command removal for restricted AI-agent use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrennerSpear](https://clawhub.ai/user/BrennerSpear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and administrators use this skill to choose L1, L2, or L3 gog safety profiles, build a restricted gog binary, deploy it to approved hosts, and verify that blocked commands are unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is admin-oriented and its safety profiles may still allow sensitive credential, sharing, script, and deployment actions. <br>
Mitigation: Audit the selected profile before building and remove token export/import, keyring, and service-account controls from restricted tiers unless explicitly required. <br>
Risk: The build and deploy flow fetches upstream code and can replace /usr/local/bin/gog on remote hosts. <br>
Mitigation: Pin or verify the upstream source before building, deploy only to approved hosts, keep the backup binary, and run deployment verification. <br>
Risk: Profile edge cases such as Drive sharing and filter forwarding can expose data or create unexpected forwarding behavior. <br>
Mitigation: Review the YAML profile for the target environment and disable sharing or forwarding-related commands when those actions are not needed. <br>


## Reference(s): <br>
- [Safety Level Reference](references/levels.md) <br>
- [L1 Draft Profile](references/l1-draft.yaml) <br>
- [L2 Collaborate Profile](references/l2-collaborate.yaml) <br>
- [L3 Standard Profile](references/l3-standard.yaml) <br>
- [gogcli safety profiles PR](https://github.com/steipete/gogcli/pull/366) <br>
- [gogcli-safe build source](https://github.com/drewburchfield/gogcli-safe.git) <br>
- [L1 profile gist](https://gist.github.com/BrennerSpear/757e23d62af920c6e86630f2eab57dc9) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and YAML profile references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces build, deployment, verification, and rollback guidance for selected gog safety levels.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
