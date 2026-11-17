---
name: local-llm-config
description: Set up, manage, and optimize locally-hosted LLMs for agents with automated detection, configuration, and benchmarking capabilities.
version: 1.0.0
author: Z-Hussein
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [llm, local, ollama, lmstudio, llama.cpp, configuration, optimization, benchmarking]
    homepage: https://docs.openclaw.ai/
    related_skills: []
    inputs:
      action:
        type: string
        enum: [detect, list, select, configure, bench, show, reset]
        description: "Action to perform: detect available backends, list models, select/model configuration, benchmark performance, show current config, reset to defaults"
        required: true
      model:
        type: string
        description: "Specific model name to select or configure (required for 'select' action)"
        required: false
      backend:
        type: string
        enum: [ollama, lmstudio, llama.cpp, auto]
        description: "LLM backend to target (default: auto-detect)"
        required: false
        default: auto
      config_file:
        type: string
        description: "Path to configuration file to read/write (default: llm.yaml in skill directory)"
        required: false
      verbose:
        type: boolean
        description: "Enable verbose output with detailed diagnostic information"
        required: false
        default: false
    outputs:
      detection_result:
        type: object
        description: "Result from backend detection action"
        properties:
          backends:
            type: array
            items:
              type: object
              properties:
                name:
                  type: string
                  description: "Backend name (ollama, lmstudio, llama.cpp)"
                available:
                  type: boolean
                  description: "Whether the backend is installed and accessible"
                version:
                  type: string
                  description: "Backend version if available"
                models:
                  type: array
                  items:
                    type: string
                  description: "List of available models"
          recommended:
            type: string
            description: "Suggested optimal model based on available hardware"
          detection_time:
            type: number
            description: "Time taken for detection in seconds"
      model_list:
        type: array
        items:
          type: object
          properties:
            name:
              type: string
              description: "Model identifier"
            size:
              type: string
              description: "Model size (e.g., 7B, 13B, 70B)"
            quantization:
              type: string
              description: "Quantization level (e.g., q4_0, q5_K_M)"
            vram_required:
              type: string
              description: "Estimated VRAM requirement"
            ram_required:
              type: string
              description: "Estimated RAM requirement"
            description:
              type: string
              description: "Model description or capabilities"
        description: "List of available models with specifications"
      config_content:
        type: string
        description: "Generated configuration file content (YAML format)"
      bench_results:
        type: object
        description: "Benchmark results for selected model"
        properties:
          latency_ms:
            type: number
            description: "Average response latency in milliseconds"
          throughput_tps:
            type: number
            description: "Token throughput in tokens per second"
          vramb_used_mb:
            type: number
            description: "Peak VRAM usage during benchmark in MB"
          ram_used_mb:
            type: number
            description: "Peak RAM usage during benchmark in MB"
          timestamp:
            type: string
            description: "ISO timestamp of benchmark completion"
    examples:
      - description: "Detect available LLM backends and models"
        invocation: |
          local-llm-config detect
      - description: "List all available models with specifications"
        invocation: |
          local-llm-config list --verbose
      - description: "Select and configure a specific model"
        invocation: |
          local-llm-config select --model "llama3.2:3b" --backend ollama
      - description: "Benchmark model performance"
        invocation: |
          local-llm-config bench --model "mistral:7b" --timeout 60
      - description: "Show current LLM configuration"
        invocation: |
          local-llm-config show
---

# Local LLM Config Skill

## When to use
Use when you need to configure, switch, tune, or benchmark locally-hosted LLMs (Ollama, LMStudio, llama.cpp, etc.) for any skill-enabled agent.

Essential for:
- Setting up development environments with local LLMs to avoid API costs
- Ensuring privacy by keeping all LLM processing on the local machine
- Optimizing model selection based on available hardware resources
- Switching between different models for various tasks (reasoning vs. speed)
- Troubleshooting LLM connectivity and performance issues
- Creating reproducible LLM configurations for team sharing

## What it does
- 🔍 **Detection**: Automatically detects installed LLM backends via common CLI tools (ollama, lmstudio, llama-cli) or environment variables
- 📋 **Listing**: Lists available models with detailed specifications including size, quantization, and estimated memory requirements
- ⚙️ **Configuration**: Generates model-selection configuration files (YAML format) that agents can consume
- 📊 **Benchmarking**: Measures model performance including latency, token throughput, and resource utilization
- 🔧 **Tuning**: Provides helper snippets to generate prompt templates optimized for selected models
- 💾 **Persistence**: Stores configuration in the agent’s skill directory or profile for consumption by other skills
- 🔄 **Management**: Enables switching between models and backends without disrupting ongoing agent operations

## Typical workflow
1. **Detect**: Run `local-llm-config detect` to see what LLM backends are available and what models they offer
2. **List**: Use `local-llm-config list --verbose` to see detailed model specifications for informed selection
3. **Select**: Choose and configure a model with `local-llm-config select --model <model-name> [--backend <backend>]`
4. **Benchmark** (optional): Verify performance with `local-llm-config bench --model <model-name> [--timeout <seconds>]`
5. **Reference**: Point your agent’s settings or downstream skills to the generated configuration file
6. **Manage**: Switch models later using the select command or view current config with `show`

## Configuration Options
- `$LOCAL_LLM_CONFIG_FILE`: Path to custom configuration file (default: `llm.yaml` in skill directory)
- `$LOCAL_LLM_CACHE_DIR`: Directory for caching model information and benchmark results
- `$LOCAL_LLM_VERBOSE`: Enable verbose logging (equivalent to `--verbose` flag)

## Supported Backends
- **Ollama**: `ollama` command-line interface
- **LMStudio**: Local model serving via LMStudio application  
- **llama.cpp**: Direct execution via `llama-cli` or similar binaries
- **Auto**: Automatic detection of any available backend (default)

## References
- https://ollama.com - Ollama LLM framework
- https://lmstudio.ai - LMStudio local LLM interface
- https://github.com/ggerganov/llama.cpp - llama.cpp efficient LLM inference
- Hugging Face model repositories for compatible model formats
- LiteLLM and LlamaIndex integration patterns for LLM configuration

## Triggers
This skill activates when the user mentions:
- "configure local LLM"
- "set up ollama"
- "choose local model"
- "benchmark LLM performance"
- "switch llm backend"
- "detect available models"
- "local llm configuration"
- "manage llama.cpp"
- "lmstudio setup"
- "optimize model selection"