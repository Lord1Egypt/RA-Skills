## Description: <br>
JEP Primitive Skills provides atomic reference implementations of Judge, Delegate, Terminate, and Verify for agent collaboration grammar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[schchit](https://clawhub.ai/user/schchit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent-system engineers use this skill to generate JEP-04 event JSON for judge, delegate, terminate, and verify operations in multi-agent collaboration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public API deployment could allow unauthenticated event generation if exposed directly. <br>
Mitigation: Run the API behind authentication, TLS, and rate limits before exposing it outside a trusted environment. <br>
Risk: Open dependency ranges can change runtime behavior across installations. <br>
Mitigation: Pin or audit dependency versions for the target deployment. <br>
Risk: The optional signature field is metadata unless the surrounding system verifies it. <br>
Mitigation: Integrate real signature verification before relying on signature values for trust decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/schchit/jep-primitive-skills) <br>
- [README](artifact/jep-primitive-skills/README.md) <br>
- [Skill definition](artifact/jep-primitive-skills/SKILL.md) <br>
- [Changelog](artifact/jep-primitive-skills/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON events, API responses, Python objects] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include JEP verb, actor, timestamp, nonce, hash, references, optional task linkage, and canonical JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, artifact frontmatter, manifest, and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
