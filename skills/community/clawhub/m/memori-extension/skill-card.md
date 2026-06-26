## Description: <br>
Memory augmentation and LLM call interception using the Memori Python library with optional Zhipu API integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ian-at](https://clawhub.ai/user/ian-at) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agents use this skill to search local Memori-backed memories, augment prompts with retrieved context, and optionally intercept LLM calls for memory-aware responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can retain sensitive conversation content or secrets in the SQLite database. <br>
Mitigation: Avoid storing secrets, keep the memory database in a controlled path, and apply local filesystem permissions appropriate to the deployment. <br>
Risk: Setting ZHIPUAI_API_KEY can send conversation content to Zhipu AI for augmentation. <br>
Mitigation: Start without ZHIPUAI_API_KEY for local-only operation and enable it only after confirming that external data sharing is acceptable. <br>
Risk: A configurable technical-terms file can influence when LLM interception happens. <br>
Mitigation: Keep MEMORI_TECH_TERMS_FILE in a trusted location and review updates before using persistent term changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ian-at/memori-extension) <br>
- [Memori library repository](https://github.com/MemoriLabs/Memori) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Python return values and Markdown documentation with inline shell and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return retrieved memory objects, augmented prompt text, or modified message lists depending on the helper function used.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
