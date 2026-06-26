# Contributing

Contributions are welcome! Here's how to get started:

## Reporting issues

Open a GitHub issue describing:
- What you were trying to do
- What happened vs what you expected
- Your OS, Ollama version, and OpenClaw version

## Submitting changes

1. Fork the repo and create a branch: `git checkout -b my-fix`
2. Make your changes
3. Test manually by running `runner/queue_status.sh` and `runner/run_task.sh ping` on your worker machine
4. Submit a pull request with a clear description of what changed and why

## Ideas for contributions

- Support for Windows worker machines (PowerShell runner)
- Multiple worker nodes with round-robin dispatch
- Persistent task queue with retry logic
- Output streaming instead of waiting for full response
- Web UI for queue monitoring
