## Description: <br>
Provides techniques for writing effective fuzzing harnesses across languages when creating new fuzz targets or improving existing harness code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reikys](https://clawhub.ai/user/reikys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to choose fuzzing entry points, write minimal harnesses, structure inputs, and iterate on coverage and reproducibility for C, C++, Rust, Go, libFuzzer, AFL++, cargo-fuzz, and related fuzzing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or adapted fuzzing harness code may execute local project code with malformed inputs and sanitizer instrumentation. <br>
Mitigation: Review harness code before compiling or running it, isolate fuzzing runs as appropriate, and expect the fuzzer to exercise crash-prone inputs by design. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/reikys/harness-writing) <br>
- [FuzzedDataProvider Header](https://github.com/llvm/llvm-project/blob/main/compiler-rt/include/fuzzer/FuzzedDataProvider.h) <br>
- [libFuzzer Documentation](https://llvm.org/docs/LibFuzzer.html) <br>
- [cargo-fuzz Book](https://rust-fuzz.github.io/book/cargo-fuzz.html) <br>
- [Rust arbitrary Crate](https://github.com/rust-fuzz/arbitrary) <br>
- [Split Inputs in libFuzzer](https://github.com/google/fuzzing/blob/master/docs/split-inputs.md) <br>
- [Structure-Aware Fuzzing](https://github.com/google/fuzzing/blob/master/docs/structure-aware-fuzzing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No runtime hooks or persistent privileges; outputs are reference guidance and example harness patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
