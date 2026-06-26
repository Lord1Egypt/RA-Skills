## Description: <br>
Run llama.cpp benchmarks on GGUF models to measure prompt processing and token generation performance across Vulkan, CUDA, ROCm, and CPU backends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexhegit](https://clawhub.ai/user/alexhegit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to benchmark GGUF language models with llama.cpp, compare inference throughput, batch benchmark multiple models, and build or update llama.cpp for a selected backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper runs local shell scripts that search the home directory and /DATA for llama-bench. <br>
Mitigation: Review the scripts before execution and run them from an account and filesystem scope appropriate for local model benchmarking. <br>
Risk: The build helper can clone or update llama.cpp from GitHub and compile local binaries. <br>
Mitigation: Review the target build directory and upstream changes before using update or clean rebuild options. <br>
Risk: Clean rebuild options remove the scoped llama.cpp build directory. <br>
Mitigation: Use a dedicated build directory and confirm it does not contain unrelated work before running clean rebuilds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexhegit/llamacpp-bench) <br>
- [llama.cpp](https://github.com/ggerganov/llama.cpp.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and benchmark result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write timestamped benchmark reports under a local benchmark results directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
