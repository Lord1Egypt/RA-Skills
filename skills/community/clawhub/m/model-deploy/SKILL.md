---
name: model-deploy
description: Use this skill when users request to deploy LLMs (Qwen, DeepSeek, etc.) on specified GPU servers and start the model service. This skill can Download models using ModelScope; Start the vLLM inference service.
---

# Model Deploy
Deploy large language models on GPU servers using vLLM. **NOTE: only ModelScope plateform and vLLM inference engine is supported currently.**

Please ensure that the server where your OpenClaw is located has passwordless login access to the GPU servers. You can achieve this using `ssh-copy-id` command on your OpenClaw server.

This skill assumes that Miniconda is already installed on your server and is used to manage Python environments. You can use the following command to create the vllm environment with Miniconda:

```bash
conda create -n vllm python=3.10 -y
conda activate vllm
pip install vllm
```

## Quick Start
On the ModelScope platform, models are uniquely identified by `<MODEL_ORG>/<MODEL_NAME>`. For example, for `Qwen/Qwen3.5-0.8B`, `MODEL_ORG` is Qwen and `MODEL_NAME` is Qwen3.5-0.8B.

### Deploying Qwen Family Models
To deploy Qwen-Family models, use the deployment script `scripts/deploy.sh`. The usage of the script is as follows:

```bash
Usage: [ENV_VARS] deploy.sh <model_name>

Example:
  PORT=8001 \
  GPU_COUNT=4 \
  ./deploy.sh Qwen3.5-0.8B

Environment Variables:
  ENV_NAME        conda environment name (default: vllm)
  PORT            service port (default: 8000)
  GPU_COUNT       number of GPUs for tensor parallelism (default: 1)
  PROXY           proxy address (default: http://{proxyaddress}:{port})
  MODEL_BASE_PATH local path to store models (default: /home/work/models)
```

| Variable | Description | Default |
|----------|-------------|---------|
| MODEL_ORG | model organization | Qwen |
| MODEL_NAME | model name | Qwen3.5-0.8B |
| ENV_NAME | conda environment | vllm |
| PORT | model service port | 8000 |
| GPU_COUNT | number of GPUs for tensor parallelism | 1 |
| PROXY | proxy address | http://{proxyaddress}:{port} |
| MODEL_BASE_PATH | local storage path for models | /home/work/models |

## Deployment Steps
- Extract required information from the user request: model name (MODEL_NAME), model organization (MODEL_ORG), target server address (TARGET_HOST), deployment user (TARGET_USER), and other necessary parameters.

- Copy `./skills/model-deploy/scripts/deploy.sh` to the specified path on the target server, e.g., `$HOME/wangwei1237`.
- Grant execute permission to the deployment script on the target server.
- Run the deployment script on the target server **using the following format**:
```bash
ssh ${TARGET_USER}@${TARGET_HOST} "cd $HOME/wangwei1237 && PORT=8001 && ./deploy.sh Qwen3.5-0.8B"
```
- After deployment, test whether the model service has started successfully on the target server by running:
```bash
curl -X POST http://127.0.0.1:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
      "messages": [{"role": "user", "content": "你好"}],
      "max_tokens": 512
  }'
```

## Constraints
- Commands on the target server **must** be executed in this format:
  `ssh ${TARGET_USER}@${TARGET_HOST} "${CMD}"`

## Troubleshooting
- **Port occupied**: Check with `netstat -tlnp | grep <port>`
- **Version issues**: Run `pip install vllm --upgrade`
- **Network issues**: Set proxy with `export https_proxy="http://{proxyaddress}:{port}"`
- **Insufficient GPU memory**: Check GPU usage with `nvidia-smi`, find a suitable GPU index `GPU_FAN`, set `export CUDA_VISIBLE_DEVICES=$GPU_FAN` to specify the GPU, then rerun the deployment script.