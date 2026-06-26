# Hermes Agent Bridge

This skill allows OpenClaw to delegate tasks or ask questions directly to a standalone Hermes Agent installed on the same system via its CLI interface.

## Description
Use this skill when you need to leverage Hermes Agent's fast response times, its specific configured personas, or its local terminal tools. This acts as a bridge where OpenClaw asks Hermes to process a prompt and return the result.

## Usage
Run the following bash command using the `exec` tool, passing the prompt as a string. Note that we rely on `hermes` being in the PATH (e.g., `~/.local/bin/hermes`).

```bash
~/.local/bin/hermes chat -q "your prompt here"
```

## Examples
If the user asks you to "ask Hermes to write a quick script" or "see what Hermes thinks about this":

1. Call the `exec` tool:
   - `command`: `~/.local/bin/hermes chat -q "Write a quick Python script to monitor system load"`

2. Read the stdout of the `exec` result, which contains Hermes's answer, and relay it back to the user.