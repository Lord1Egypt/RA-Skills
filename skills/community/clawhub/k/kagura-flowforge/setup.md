# FlowForge Setup Guide

This guide walks through installing and configuring FlowForge in your workspace.

## Step 1: Install FlowForge CLI

FlowForge has two parts:
- **This skill** (what you just installed from ClawHub) — teaches your agent when and how to use FlowForge
- **The FlowForge CLI** (a separate Node.js tool) — the workflow engine that tracks state, enforces step order, and persists progress in a local SQLite database

The skill talks to the CLI. You need both.

Check if the CLI is already installed:

```bash
flowforge --version
```

If not installed:

```bash
npm install -g @kagura-agent/flowforge
```

Verify installation:

```bash
flowforge --version
```

## Step 2: Create Workflows Directory

FlowForge auto-discovers workflows from a `workflows/` directory. Create it in your workspace:

```bash
mkdir -p workflows
```

## Step 3: Add Example Workflow

Create a starter workflow to test the setup:

```bash
cat > workflows/example.yaml << 'EOF'
name: example
description: Example workflow to test FlowForge
start: start

nodes:
  start:
    task: |
      This is the first step.
      Task: Print "Hello from FlowForge"
    next: finish

  finish:
    task: |
      Final step.
      Task: Print "Workflow complete"
    terminal: true
EOF
```

## Step 4: Register the Workflow

```bash
flowforge define workflows/example.yaml
```

Verify it's registered:

```bash
flowforge list
```

You should see `example` in the list.

## Step 5: Test Execution

Start the example workflow:

```bash
flowforge start example
```

View current status:

```bash
flowforge status
```

Complete the first node:

```bash
flowforge next
```

Finish the workflow:

```bash
flowforge next
```

View execution history:

```bash
flowforge log
```

## Step 6: Configure Agent Steering (Optional)

If using with AI agents (like OpenClaw), add steering to your workspace's `AGENTS.md` or `CLAUDE.md`:

```markdown
## FlowForge Workflows

For multi-step structured tasks, use FlowForge workflows. Check `flowforge list` to see available workflows and use the flowforge skill to execute them.

Common workflows:
- Code contribution: `flowforge start code-contribution`
- Research/learning: `flowforge start research`
- Code review: `flowforge start review`
```

## Step 7: Add Your Own Workflows

Create workflow YAML files in the `workflows/` directory. FlowForge will auto-discover them.

Example: `workflows/code-contribution.yaml`

```yaml
name: code-contribution
description: Contribute code to open source project
start: study

nodes:
  study:
    task: Read project structure and identify work to do
    next: implement

  implement:
    task: Write code changes following project patterns
    next: test

  test:
    task: Run tests and verify implementation
    branches:
      - condition: tests pass
        next: submit
      - condition: tests fail
        next: implement

  submit:
    task: Create pull request
    next: verify

  verify:
    task: Address review feedback
    terminal: true
```

Register it:

```bash
flowforge define workflows/code-contribution.yaml
```

See [references/yaml-format.md](references/yaml-format.md) for complete YAML format documentation.

See [references/examples/](references/examples/) for more workflow templates.

## Step 8: Build Your Mapping Table

As you use FlowForge, you'll notice patterns — certain phrases from the user always map to the same workflow. When this happens, add the mapping to the **My Workflows** table in SKILL.md:

```markdown
| Intent | Workflow |
|--------|----------|
| deploy to production | deploy |
| review this PR | code-review |
| research a topic | research |
```

This table is yours to maintain. It makes FlowForge faster to trigger — instead of running `flowforge list` every time, you'll know exactly which workflow to start.

## Troubleshooting

### Command not found: flowforge

FlowForge CLI is not installed or not in PATH. Run:

```bash
npm install -g @kagura-agent/flowforge
```

### Permission denied

You may need to use `sudo` (not recommended) or configure npm to install global packages without sudo:

```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

Then retry:

```bash
npm install -g @kagura-agent/flowforge
```

### Workflow not found after define

Make sure you used the correct YAML path:

```bash
flowforge define workflows/your-workflow.yaml
```

Check registered workflows:

```bash
flowforge list
```

### Database location

FlowForge stores state in `~/.flowforge/flowforge.db`. To reset everything:

```bash
rm -rf ~/.flowforge
```

## Next Steps

- Read [SKILL.md](SKILL.md) to understand how agents use FlowForge
- Read [references/yaml-format.md](references/yaml-format.md) for YAML format details
- Browse [references/examples/](references/examples/) for workflow templates
- Create your own workflows in `workflows/` directory
