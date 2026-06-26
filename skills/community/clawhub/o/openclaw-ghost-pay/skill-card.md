## Description: <br>
Discover Ghost payment requirements, execute real x402 calls, report x402 settlements, and run GhostWire quote/prepare/status flows for direct escrow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ghostprotoinfra](https://clawhub.ai/user/ghostprotoinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let OpenClaw agents discover Ghost payment requirements, perform x402 paid requests, report verified settlements, and prepare or inspect GhostWire escrow workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute real x402 paid requests using a live signer. <br>
Mitigation: Use a dedicated low-balance signer, require human approval for live paid calls, set amount caps, and run dry-run mode before first use in a new runtime. <br>
Risk: Signer private keys and payer data may be exposed if passed through prompts, CLI history, logs, screenshots, or settlement metadata. <br>
Mitigation: Store private keys only in protected runtime secret storage, avoid private-key CLI flags, do not place secrets in prompts or frontend output, and keep sensitive payer data out of settlement metadata. <br>
Risk: Unrestricted merchant or Ghost base URLs could route payments or settlement reports to unintended services. <br>
Mitigation: Restrict merchant endpoints, Ghost base URLs, approved Ghost service slugs, and GhostWire roles in the runtime before enabling live calls. <br>
Risk: Manual settlement reporting can be incorrect when used outside verified recovery or unsupported runtime flows. <br>
Mitigation: Prefer SDK auto-reporting for long-lived Node or Python merchant runtimes, and reserve manual reporting for fallback, backfill, or incident recovery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ghostprotoinfra/openclaw-ghost-pay) <br>
- [Publisher profile](https://clawhub.ai/user/ghostprotoinfra) <br>
- [Project homepage](https://github.com/Ghost-Protocol-Infrastructure/GHOST_PROTOCOL/tree/main/integrations/openclaw-ghost-pay) <br>
- [README](README.md) <br>
- [Install guide](INSTALL.md) <br>
- [Quickstart](QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command outputs from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces payment requirement lookups, dry-run request plans, x402 call results, settlement report responses, GhostWire quotes, job creation responses, and job status JSON.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
