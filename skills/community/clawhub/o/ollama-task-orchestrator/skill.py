#!/usr/bin/env python3
"""
Ollama Task Orchestrator — OpenClaw skill
Manages Ollama queue and task execution on a remote worker Mac via SSH.

Configuration (environment variables or defaults):
  OLLAMA_WORKER_HOST   SSH host alias for the worker Mac (default: worker-mac)
  OLLAMA_RUNNER_PATH   Path to the runner directory on the worker Mac
                       (default: ~/worker/runner)
"""

import os
import subprocess
import threading
import shlex

WORKER_HOST = os.environ.get("OLLAMA_WORKER_HOST", "worker-mac")
RUNNER_PATH = os.environ.get("OLLAMA_RUNNER_PATH", "~/worker/runner")


class OllamaTaskOrchestrator:
    def __init__(self, worker_host: str = WORKER_HOST, runner_path: str = RUNNER_PATH):
        self.worker_host = worker_host
        self.runner_path = runner_path
        self.lock = threading.Lock()

    def _ssh(self, command):
        """Run a command on the worker Mac via SSH."""
        if isinstance(command, str):
            remote_command = command
        else:
            remote_command = shlex.join(command)
        result = subprocess.run(
            ["ssh", self.worker_host, remote_command],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode

    def queue_status(self, args: str = "") -> str:
        """Check queue status and Ollama server health."""
        cmd = [f"{self.runner_path}/queue_status.sh"]
        if args:
            cmd.extend(shlex.split(args))
        stdout, stderr, code = self._ssh(cmd)
        if code != 0:
            return f"Error checking queue status: {stderr}"
        return stdout

    def run_task(self, task_command: str) -> str:
        """Run a task on the worker Mac with exclusivity locking."""
        with self.lock:
            cmd = [f"{self.runner_path}/run_task.sh", *shlex.split(task_command)]
            stdout, stderr, code = self._ssh(cmd)
            if code != 0:
                return f"Error running task: {stderr}"
            return stdout

    def handle(self, command_line: str) -> str:
        """Parse and dispatch CLI/chat commands."""
        parts = command_line.strip().split(maxsplit=2)
        if not parts:
            return "No command provided."

        cmd = parts[0].lower()
        if cmd != "ollama":
            return "Unknown command. Use: ollama status | ollama run <task>"

        if len(parts) < 2:
            return "Usage: ollama <status|run> [args]"

        subcmd = parts[1].lower()

        if subcmd == "status":
            extra = parts[2] if len(parts) > 2 else ""
            return self.queue_status(extra)

        elif subcmd == "run":
            if len(parts) < 3:
                return "Usage: ollama run <task_command>"
            return self.run_task(parts[2])

        else:
            return f"Unknown subcommand: {subcmd}. Use: status | run"


if __name__ == "__main__":
    import sys

    orchestrator = OllamaTaskOrchestrator()
    if len(sys.argv) < 2:
        print("Usage: python skill.py <status|run> [args]")
        sys.exit(1)
    output = orchestrator.handle("ollama " + " ".join(sys.argv[1:]))
    print(output)
