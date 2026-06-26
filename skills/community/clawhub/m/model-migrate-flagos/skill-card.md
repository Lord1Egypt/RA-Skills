## Description: <br>
Migrates model code from the latest vLLM upstream repository into vllm-plugin-FL pinned at vLLM 0.13.0, then adapts, registers, validates, benchmarks, serves, and compares the migration against an upstream server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wbavon](https://clawhub.ai/user/wbavon) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to backport newly released vLLM model implementations into vllm-plugin-FL while preserving upstream behavior and verifying correctness with tests, benchmarks, serving checks, and token-level E2E comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad GPU and remote-server control, including commands that can terminate GPU workloads and manage remote vLLM servers. <br>
Mitigation: Install and run it only in a dedicated development or GPU test environment, and gate or remove blanket GPU kill commands before use on shared or production machines. <br>
Risk: Remote E2E workflows can use SSH, default root-oriented settings, and remote process management. <br>
Mitigation: Restrict remote targets to trusted hosts, prefer scoped non-root SSH users and keys, and verify the target host and command before starting or stopping remote services. <br>
Risk: Serving or benchmarking model directories with vLLM and remote-code trust can execute model-supplied code. <br>
Mitigation: Serve and benchmark only trusted model directories after reviewing their source and configuration. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Migration Procedure](references/procedure.md) <br>
- [Compatibility Patches](references/compatibility-patches.md) <br>
- [Operational Rules](references/operational-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code edits, configuration snippets, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify vllm-plugin-FL model and configuration files and may run validation, benchmark, serving, and E2E comparison commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
