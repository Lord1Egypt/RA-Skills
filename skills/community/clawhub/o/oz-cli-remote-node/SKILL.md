# oz

## Description
This skill implements the `/oz` slash command and acts as a proxy to the `oz-cli` on a remote node.
Use this skill ONLY when the user activates Oz mode with `/oz` or explicitly asks to use Oz/Warp.

## Onboarding & Setup (First-Time Use)
When a user first installs or attempts to use this skill, guide them through the setup process:
1. **Explain the Purpose**: Let the user know this skill allows them to run the `oz` CLI on a *remote* node via the Gateway, acting as a proxy.
2. **Determine the Remote Node**: Ask the user for the exact name of the remote node where `oz-cli` is installed (e.g., "Build Node"). Save this node name into your workspace's `TOOLS.md` or a local memory file so you remember it for all future uses.
3. **Verify Tool Permissions**: Verify that you (the agent) have the `nodes` tool enabled. If not, instruct the user to grant it (e.g., `openclaw config set agents.list[<your-index>].tools.allow '["nodes"]'`) and restart the gateway.
4. **Sandbox Detection**: Check if you are currently running in a Docker sandbox (e.g., by checking if `/.dockerenv` exists or using `cat /proc/1/cgroup`). If you are in a sandbox, inform the user that local `oz` execution is impossible without a custom developer image.
5. **Select Agent Profile**: Once the remote node is known, execute `oz agent profile list --output-format json` on that node using the `nodes` tool. 
   - Note: Ignore standard error warnings (like `libEGL warning`) and parse the JSON array (e.g., `[{"id":"Unsynced","name":"Default"},{"id":"...","name":"Claude"}]`).
   - Show the user the list of profile *names* and ask which one they want to use.
   - Save the selected profile's `id` (not the name) to your memory alongside the node name.

## State Memory (Oz Mode)
- If the user types `/oz`, you MUST reply with a clear confirmation: "✅ Oz mode is now ACTIVE. All messages will be sent to the Oz CLI on the remote node. Type `/oz off` to exit, or use `! <command>` to run a direct bash command."
- If the user types `/oz off`, you MUST reply: "❌ Oz mode is now OFF. Returning to normal assistant behavior."
- While in Oz mode, treat EVERY subsequent message from the user as a prompt for the `oz` CLI on the remote node, UNLESS the message starts with `!`.

## Execution on Remote Node
You must use the `nodes` tool with `action="run"` and `node="<Saved_Node_Name>"` for all execution here. Do NOT use local `exec`.

1. **Direct Bash Commands (`!`)**:
   - If the user message starts with `!` (e.g. `! ls -la` or `! mkdir test`):
   - Strip the `!` and run it as a direct shell command on the remote node using the `nodes` tool.
   - Command array format: `["bash", "-c", "<command>"]`
   - Use `cwd`: `~/git` (or the last known working directory if changed).
   - Report the output directly.

2. **Oz CLI Prompts & Run Tracking**:
   - **CRITICAL**: ALWAYS use `oz agent run`. NEVER use `oz agent run-cloud`.
   - Run the `oz` CLI on the remote node using the `nodes` tool.
   - Command array format MUST include the saved profile id: 
     `["oz", "agent", "run", "--cwd", "~/git", "--profile", "<Saved_Profile_ID>", "--prompt", "<user_prompt>"]`
   - **Run Tracking**: When you start an `oz agent run`, you MUST keep track of it:
     1. Monitor the initial output to capture the unique Run ID and the "Open in Oz URL".
     2. Create a tracking file in your workspace named `oz_run.<id>.md`.
     3. Include in this file: Date, Time, Run ID, the Original Prompt, the Open in Oz URL, and any other relevant metadata.
     4. Keep track of the `oz` commands that are currently running.
   - **Completion**: Once the `oz agent run` command is done, update the tracking file and send a response back to the user formatted EXACTLY like this:
     ```
     oz agent for run ID: <id> done.
     
     <the response from the oz agent>
     ```

### Supported `oz agent run` Flags
You can append these flags to the `oz agent run` command if explicitly requested by the user:
- `--cwd <PATH>` (`-C`): run from a different directory.
- `--name <NAME>` (`-n`): label the run for grouping and traceability.
- `--share`: share the session with teammates.
- `--profile <ID>`: use a specific agent profile (defaults to the saved ID if not specified).
- `--model <MODEL_ID>`: override the default model.
- `--skill <SPEC>`: use a skill as the base prompt.
- `--mcp <SPEC>`: start one or more MCP servers (UUID, JSON path, or inline JSON). Can be repeated.
- `--environment <ID>` (`-e`): run in a specific cloud environment.
- `--file <PATH>` (`-f`): load run configuration from a YAML or JSON file.