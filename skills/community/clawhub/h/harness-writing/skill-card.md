## Description:

Guides developers through writing effective fuzzing harnesses across languages for new fuzz targets or improvements to existing harness code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reikys](https://clawhub.ai/user/reikys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to identify fuzzing entry points and write or improve C, C++, Rust, AFL++, cargo-fuzz, go-fuzz, and structure-aware harnesses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some C++ examples use raw typed-pointer casts and vector-backed input access patterns that may be unsafe if copied directly into production fuzz targets.

Mitigation: Before production use, replace raw typed-pointer casts with memcpy or explicit decoding, and prefer vector::data() with clear zero-length handling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/reikys/skills/harness-writing)
- [FuzzedDataProvider Header](https://github.com/llvm/llvm-project/blob/main/compiler-rt/include/fuzzer/FuzzedDataProvider.h)
- [libFuzzer Documentation](https://llvm.org/docs/LibFuzzer.html)
- [cargo-fuzz Book](https://rust-fuzz.github.io/book/cargo-fuzz.html)
- [arbitrary Crate](https://github.com/rust-fuzz/arbitrary)
- [Split Inputs in libFuzzer](https://github.com/google/fuzzing/blob/master/docs/split-inputs.md)
- [Structure-Aware Fuzzing with Protocol Buffers](https://github.com/google/fuzzing/blob/master/docs/structure-aware-fuzzing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no tools, credentials, or runtime actions are invoked by the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
