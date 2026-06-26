## Description: <br>
Submits proofs to the OpenMath platform using a two-stage commit-reveal flow. Use when the user wants to commit a proof hash or reveal a Lean/Rocq proof on the Shentu network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bennyzhe](https://clawhub.ai/user/bennyzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and theorem provers use this skill to prepare and submit OpenMath proof commitments and proof reveals through Shentu, then check transaction and theorem status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Blockchain submissions may spend fees or deposits and publish proof details. <br>
Mitigation: Before broadcasting, verify the theorem ID, proof file, prover and agent addresses, feegrant limits, RPC endpoint, and exact shentud binary. <br>
Risk: Local key or configuration setup can expose sensitive wallet material if handled carelessly. <br>
Mitigation: Keep key creation or recovery and openmath-env.json writes as explicit user-approved manual steps, and use the local OS keyring for signing. <br>
Risk: Using an unexpected shentud binary or RPC endpoint can lead to unintended transaction behavior. <br>
Mitigation: Confirm the shentud path and version before submission, prefer trusted official releases, and review any SHENTU_NODE_URL override. <br>


## Reference(s): <br>
- [Init Setup](references/init-setup.md) <br>
- [OpenMath Environment Example](references/openmath-env.example.json) <br>
- [Shentu Proof Submission Guidelines](references/submission_guidelines.md) <br>
- [OpenMath Authz Setup](references/authz_setup.md) <br>
- [Shentu Releases](https://github.com/shentufoundation/shentu/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and generated transaction files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate proofhash.json or proofdetail.json locally before the user broadcasts with shentud.] <br>

## Skill Version(s): <br>
v1.0.7 (source: frontmatter; release evidence version 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
