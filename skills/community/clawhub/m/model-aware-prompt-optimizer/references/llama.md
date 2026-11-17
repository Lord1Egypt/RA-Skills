# Meta Llama Instruct profile

- Apply the universal profile to the semantic content: clear system context, explicit user task, constraints, output, evidence, tools, and stopping behavior.
- Preserve proper message roles. Put stable rules and available function definitions in the system message when supported by the target integration.
- For function calling, describe each function and required arguments precisely, and require only the tool-call format expected by the serving stack.
- Use the chat template for the exact Llama model and runtime. Do not manually insert special tokens such as header, turn, or end markers when the tokenizer, SDK, or server already renders them.
- Distinguish base completion models from instruction-tuned chat models. A prompt for one is not automatically valid for the other.
- Llama versions and hosting providers may apply different tool schemas or templates; verify the exact model/runtime before making syntax-specific changes.

## Official sources

- Meta Llama model prompt formats: https://github.com/meta-llama/llama-models/tree/main/models
- Llama 3.3 prompt format: https://github.com/meta-llama/llama-models/blob/main/models/llama3_3/prompt_format.md
- Llama models tools: https://github.com/meta-llama/llama-models

