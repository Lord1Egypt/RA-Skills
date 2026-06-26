# Lemonade Server Manager for OpenClaw NullClaw, and the "Claw" family

This skill enables your OpenClaw or NullClaw AI agent to securely orchestrate, manage, and interact with local and remote Lemonade Server instances. It acts as a comprehensive declarative bridge for model lifecycle management, hardware monitoring, and multimodal inference.

## Core Features

- **Multi-Server Orchestration**: Dynamically route requests to different local or remote Lemonade Servers using the agent's built in tools.
- **Zero Command Injection**: All HTTP logic is abstracted into purely declarative markdown documentation in `SKILL.md`, instructing the agent to utilize standard native tools (`curl`) rather than executing malicious prompt injections.
- **Hardware Awareness**: Allows the agent to query system info, monitor NPU/GPU constraints, and intelligently load/unload models to free up VRAM.
- **Multimodal Ready**: Full support for text completion, chat workflows, and stable-diffusion image generation.

## Installation

You can install this skill globally via ClawHub or manually clone it into your workspace.

### Option 1: ClawHub (Recommended)
```bash
clawhub install lemonade-server-manager
```

### Option 2: Manual Git Setup
Navigate to your workspace and clone the repository:
```bash
cd ~/.openclaw/workspace/skills/
git clone https://github.com/james-martinez/lemonade-server-manager.git
cd lemonade-server-manager
```

## Authentication Configuration

This skill supports environment-based authentication for interacting with Lemonade Servers.

### API Key (Environment Variable)
To interact with a local or remote server securely, provide your API key via the following environment variable on your host OS:
```bash
export LEMONADE_API_KEY="your-api-key-here"
```

## Available API Endpoints

The agent has access to the following categorized endpoints, executing them natively via standard tools (e.g., `curl`):

| Endpoint Name | Description | Lemonade Endpoint |
| :--- | :--- | :--- |
| `System Info` | Retrieves hardware and device enumeration. | `/api/v1/system-info` |
| `Health Check` | Checks server status and loaded models. | `/api/v1/health` |
| `List Models` | Lists downloaded and available models. | `/api/v1/models` |
| `Pull Model` | Downloads a specified model to the server. | `/api/v1/pull` |
| `Load Model` | Loads a model into GPU/NPU memory. | `/api/v1/load` |
| `Unload Model` | Unloads a model to free up system VRAM. | `/api/v1/unload` |
| `Chat Completion` | Executes standard LLM chat tasks. | `/api/v1/chat/completions` |
| `Generate Image` | Creates images using stable-diffusion. | `/api/v1/images/generations` |

## Usage Examples

Once installed, ask your OpenClaw or NullClaw agent to perform server tasks:
- *"What models are currently loaded on my local Lemonade server?"*
- *"Check the system health on http://192.168.1.50:8000. If there's enough VRAM, download and load the Llama 3 model."*
- *"Unload the active LLM to free up the NPU."*
