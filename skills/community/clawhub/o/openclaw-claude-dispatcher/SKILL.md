---
name: openclaw-claude-dispatcher
description: |
  Dispatch long-running coding tasks to Claude Code CLI with automatic callback notifications to Feishu/WeCom when complete.

  Use this skill whenever the user wants to:
  - Create a new project or application from scratch
  - Modify/upgrade an existing project with new features
  - Refactor or improve existing code
  - Run any coding task that might take a long time
  - Get notified in Feishu or WeCom when the task completes

  TRIGGER on phrases like: "create a new project", "build an app", "add feature to project", "upgrade project", "refactor code", "improve the codebase", or any request that involves substantial code generation or modification where the user wants to be notified when it's done.
---

# OpenClaw Claude Code Dispatcher

This skill helps you dispatch coding tasks to Claude Code CLI and receive automatic notifications when they complete.

## When to use this skill

Use this skill when the user wants to:
- **Create new projects** - "Write a vocabulary learning app", "Build a REST API for user management"
- **Modify existing projects** - "Add login to my web app", "Upgrade the database layer"
- **Long-running tasks** - Any substantial coding work that will take time and the user wants to be notified when done

The task runs in the background via Claude Code CLI, and when it completes, a notification is sent to the configured channel (Feishu group, WeCom group, or WeCom private message).

## System Overview

```
User request → dispatch-claude-code.sh → Claude Code CLI executes task
                                              ↓
                                      Task completes → Hook triggers
                                              ↓
                                   notify-agi.sh sends notification
                                              ↓
                                   Feishu/WeCom receives message
```

## Step 1: Understand the task

Extract these details from the user's request:

1. **Task description** - What should Claude Code do?
2. **Working directory** - Where is the project? (required for existing projects)
   - For new projects: use a sensible default like `~/projects/<project-name>`
   - For existing projects: the user should specify the path
3. **Notification channel** - Where to send completion notice?
   - Default: Feishu (most reliable)
   - Options: Feishu group, WeCom group, WeCom user

Ask clarifying questions if needed, but default to Feishu if the user doesn't specify.

## Step 2: Prepare the dispatch

### Key paths and IDs

**Notification targets:**
- Feishu group: `oc_934e5b3011709a0ea5d713789e61dc4e`
- WeCom group: `group:wrCQYUEQAAHpLlnGfGnpwcxxverWPs7A`
- WeCom user: `user:xclipse` (or other userid)

**Dispatch script:**
```bash
~/openclaw/scripts/dispatch-claude-code.sh
```

### Common parameters

```bash
-p, --prompt TEXT        # Task description (required)
-n, --name NAME          # Task name for tracking
-c, --channel CHANNEL    # feishu or wecom (default: feishu)
-g, --group ID           # Target group/user ID
-w, --workdir DIR        # Working directory (default: /home/ecs-user/openclaw)
--permission-mode MODE   # bypassPermissions, dontAsk, acceptEdits
--agent-teams            # Enable multi-agent collaboration
```

### Default configuration

Use these defaults unless the user specifies otherwise:
- Channel: `feishu`
- Group: `oc_934e5b3011709a0ea5d713789e61dc4e`
- Permission mode: `bypassPermissions` (for non-interactive execution)
- Working directory: For existing projects use the path they specify; for new projects create under `~/projects/`

## Step 3: Execute the dispatch

### Basic dispatch pattern

```bash
~/openclaw/scripts/dispatch-claude-code.sh \
  -p "Your detailed task description here" \
  -n "descriptive-task-name" \
  -c feishu \
  -g "oc_934e5b3011709a0ea5d713789e61dc4e" \
  -w "/path/to/project" \
  --permission-mode bypassPermissions
```

### For new projects

When creating a new project:
1. Choose a project directory: `~/projects/<project-name>`
2. Create the directory first: `mkdir -p ~/projects/<project-name>`
3. Dispatch with that directory as workdir

Example:
```bash
mkdir -p ~/projects/vocab-app
~/openclaw/scripts/dispatch-claude-code.sh \
  -p "Create a vocabulary learning application with spaced repetition..." \
  -n "vocab-app-creation" \
  -g "oc_934e5b3011709a0ea5d713789e61dc4e" \
  -w "/home/ecs-user/projects/vocab-app" \
  --permission-mode bypassPermissions
```

### For existing projects

When modifying an existing project, the user should tell you where it is:

```bash
~/openclaw/scripts/dispatch-claude-code.sh \
  -p "Add user login functionality with JWT authentication..." \
  -n "dgt-web-add-login" \
  -g "oc_934e5b3011709a0ea5d713789e61dc4e" \
  -w "/home/ecs-user/projects/dgt-web" \
  --permission-mode bypassPermissions
```

### For complex tasks (Agent Teams)

If the task is complex or involves multiple components, add `--agent-teams`:

```bash
~/openclaw/scripts/dispatch-claude-code.sh \
  -p "Refactor the entire test suite, add integration tests..." \
  -n "test-refactor" \
  -g "oc_934e5b3011709a0ea5d713789e61dc4e" \
  -w "/home/ecs-user/projects/myapp" \
  --agent-teams \
  --permission-mode bypassPermissions
```

## Step 4: Confirm dispatch

After running the dispatch command, tell the user:

1. **What task was dispatched** - Brief summary
2. **Where it's running** - The working directory
3. **Where they'll get notified** - Channel and group/user
4. **What happens next** - "The task is now running in Claude Code. When it completes, you'll receive a notification in [Feishu/WeCom] with a summary of the results."

Example response:
```
✅ Task dispatched successfully!

📋 Task: Create vocabulary learning app
📁 Location: ~/projects/vocab-app
💬 Notification: Feishu group

The task is running in Claude Code. You'll receive a notification in Feishu when it completes (usually 5-15 minutes for a new project, depending on complexity).
```

## Handling channel preferences

### If user wants WeCom instead of Feishu

```bash
# WeCom group
-c wecom -g "group:wrCQYUEQAAHpLlnGfGnpwcxxverWPs7A"

# WeCom private message
-c wecom -g "user:xclipse"
```

**Important:** For WeCom (企业微信), the WebSocket session must be active. Remind the user: "Make sure you've interacted with the bot in WeCom recently so the session is active."

### If user wants both channels

You can dispatch once and the notification goes to the specified channel. If they want multiple notifications, you'd need to run the hook manually after completion (advanced, usually not needed).

## Common scenarios

### Scenario 1: New standalone project

User: "Create a new project, write a todo list app with React"

```bash
mkdir -p ~/projects/todo-app
~/openclaw/scripts/dispatch-claude-code.sh \
  -p "Create a React-based todo list application with local storage, add/delete/complete functionality, and a clean modern UI" \
  -n "todo-app-creation" \
  -g "oc_934e5b3011709a0ea5d713789e61dc4e" \
  -w "/home/ecs-user/projects/todo-app" \
  --permission-mode bypassPermissions
```

### Scenario 2: Upgrade existing project

User: "Upgrade project 'projects/dgt-web' add user login"

```bash
~/openclaw/scripts/dispatch-claude-code.sh \
  -p "Add complete user authentication system: login page, JWT token handling, protected routes, and session management" \
  -n "dgt-web-add-auth" \
  -g "oc_934e5b3011709a0ea5d713789e61dc4e" \
  -w "/home/ecs-user/projects/dgt-web" \
  --permission-mode bypassPermissions
```

### Scenario 3: Complex refactoring

User: "Refactor the test suite in ~/myapp, make it more maintainable"

```bash
~/openclaw/scripts/dispatch-claude-code.sh \
  -p "Refactor the test suite: improve organization, add helper utilities, increase coverage, use consistent patterns" \
  -n "myapp-test-refactor" \
  -g "oc_934e5b3011709a0ea5d713789e61dc4e" \
  -w "/home/ecs-user/myapp" \
  --agent-teams \
  --permission-mode bypassPermissions
```

## Troubleshooting

### If dispatch fails

Common issues:
1. **Working directory doesn't exist** - Create it first with `mkdir -p`
2. **Nested Claude Code session** - Can't run Claude Code inside Claude Code. User should run from a regular terminal.
3. **Permission denied** - Check if dispatch script is executable: `ls -l ~/openclaw/scripts/dispatch-claude-code.sh`

### Checking system status

If needed, verify the system is ready:

```bash
# Check if hook is installed
ls -la ~/.claude/hooks/notify-agi.sh

# Check if dispatch script exists
ls -la ~/openclaw/scripts/dispatch-claude-code.sh

# Verify OpenClaw is running
openclaw status
```

But avoid doing this proactively - only if there's an actual problem.

## What NOT to do

❌ **Don't monitor logs in real-time** - This consumes tokens and the user will get notified when done

❌ **Don't read task outputs** - Wait for the notification, the summary will be in the message

❌ **Don't check status repeatedly** - The hook will fire when complete

❌ **Don't try to run Claude Code yourself** - Always use the dispatch script, which handles the hook setup

## Permission modes

Choose based on the task:

- `bypassPermissions` - No prompts, fully automated (recommended default)
- `dontAsk` - Run without asking, but still show what's happening
- `acceptEdits` - Safer for critical codebases, but requires some interaction

Default to `bypassPermissions` unless the user expresses concern about automated changes.

## Summary checklist

Before dispatching, make sure you have:
- [ ] Clear task description
- [ ] Working directory determined (create if new project)
- [ ] Notification channel chosen (default: Feishu)
- [ ] Appropriate permission mode (default: bypassPermissions)
- [ ] Task name for tracking

Then run the dispatch command and confirm with the user what you did.
