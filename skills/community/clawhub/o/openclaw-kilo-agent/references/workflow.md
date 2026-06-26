# Kilo CLI Workflow for OpenClaw

## Core Workflow: The "Brain and Hands" Pattern

### Role of the Brain (OpenClaw)
- **Analyze** the user request.
- **Strategize** the breakdown of tasks.
- **Formulate** the prompt for Kilo.
- **Monitor** Kilo's execution.

### Role of the Hands (Kilo)
- **Execute** the heavy-lifting tasks (code, browser automation, file refactors).
- **Auto-approve** operations using the `--auto` flag.
- **Report** back detailed findings.

## Step-by-Step Task Execution

1. **Initialize the task**: Determine if it's a new or existing session.
   - Use `--continue` to resume the last session.
   - Use `--session <id>` for specific context.
2. **Launch Kilo**: Run the command with the model and auto-approval flags.
   - Example: `kilo run --model <model> --auto "<prompt>"`
3. **Handle completion**: Parse the output from Kilo and provide a summary to the user.

## Example Workflow: Speedtest (Browser Automation)

1. **Goal**: Get upload/download speed from Speedtest.net.
2. **Strategy**:
   - Use Puppeteer MCP server.
   - Navigate to `https://www.speedtest.net/`.
   - Click the 'GO' button.
   - Wait for the results to appear (approx. 30-45 seconds).
   - Extract the speed values using JavaScript evaluation.
3. **Execution**:
   ```bash
   kilo run --model <model> --auto "Use your puppeteer MCP tool to navigate to https://www.speedtest.net/, click the 'GO' button, wait for the test to complete, and then report back the final download and upload speeds."
   ```
4. **Result**: Kilo reports the speeds directly.
