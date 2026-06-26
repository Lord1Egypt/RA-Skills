---
name: rtm-skill
description: Remember The Milk skill for OpenClaw
---

# Remember The Milk (RTM) Skill for OpenClaw

This skill integrates [Remember The Milk](https://www.rememberthemilk.com/) with OpenClaw, allowing you to manage your daily tasks directly from the command line.

## Installation (CLI Usage)

This skill can automatically be loaded by OpenClaw. However, if you would like to use the `rtm` command directly in your Mac's terminal (or allow LLM agents to use it as a shell command), you can install it globally via npm:

```bash
npm link
```

## Obtaining API Credentials

Before using this skill, you need to obtain an API Key and a Shared Secret from Remember The Milk:

1. Go to the [Remember The Milk API Keys](https://www.rememberthemilk.com/services/api/keys.rtm) page.
2. Log in with your Remember The Milk account if prompted.
3. Apply for a new API Key by registering your application.
4. Once created, you will receive an **API Key** and a **Shared Secret**.
5. Once you have your credentials, you must save them securely so the bot doesn't lose them. Choose one of the following methods:

### Method A: Using the `config` command (Recommended)

Run this command in your terminal:

```bash
rtm config <your-api-key> <your-shared-secret>
```

This saves the credentials safely to `~/.rtm-credentials.json` ensuring they persist across terminal restarts.

### Method B: Using a `.env` file

Create a file named `.env` in this skill's folder (you can use `.env.example` as a template) and add your keys:

```env
RTM_API_KEY="your-api-key"
RTM_SHARED_SECRET="your-shared-secret"
```

> **IMPORTANT**
> Do NOT edit `index.js` to embed your API key/secret directly into the source files. 
> Using one of the methods above ensures your credentials remain secure and recognizable by the bot.

## Setup and Authorization

Before you can use the commands to manage your tasks, you need to authorize the skill with your Remember The Milk account.

> **NOTE**
> When you authorize this application, an authentication token will be saved locally to `~/.rtm-token.json` in plaintext. 
> Keep this file secure on trusted devices, and delete it if you uninstall the skill.

1. **Start Authorization:**

   ```bash
   rtm auth
   ```
   
   This command will provide you with an authorization URL. Open this URL in your web browser and authorize the application.

2. **Save Token:**

   After authorizing in the browser, run the following command with the `frob` provided.
   
   ```bash
   rtm token <frob>
   ```
   
   This will save your authentication token locally (`~/.rtm-token.json`) so you only need to do this once.

## Available Commands

Once authorized, you can use the following commands to interact with your tasks.

### List Tasks

List your tasks. By default, this only fetches **incomplete** tasks to keep the response fast and clean:

```bash
rtm list
```

You can explicitly ask for completed tasks (up to 100 recent ones), or all tasks:

```bash
rtm list completed  # Fetches up to 100 recently completed tasks
rtm list all        # Fetches absolutely all tasks
```

This will fetch and display the specified tasks along with their properties:
- Completion status (✅ or ⬜️)
- Persistent Task IDs (`task_id`)
- Lists (categories)
- Priorities and due dates
- Tags and notes

*The Task ID (e.g., `8573921`) is a permanent identifier used for completing or modifying tasks.*

### Add a Task

Create a new task:

```bash
rtm add <task name>
```

Example: `rtm add Buy groceries`

### Add a Note

Add a note to an existing task using its `task_id`:

```bash
rtm note <task_id> <note text>
```

Example: `rtm note 8573921 Make sure to check the expiry dates`

### Complete a Task

Mark a specific task as completed using its `task_id` (obtainable via `rtm list`):

```bash
rtm complete <task_id>
```

Example: `rtm complete 8573921`

### Modify Task Properties

You can modify task properties using the following commands (all require the `task_id` from `rtm list`):

- **Due Date:** `rtm due <task_id> <date string>` (Leave date empty to delete the due date)
  - Example: `rtm due 8573921 tomorrow`
  - Delete due: `rtm due 8573921`
- **Start Date:** `rtm start <task_id> <date string>`
  - Example: `rtm start 8573921 next week`
- **Priority:** `rtm priority <task_id> <1|2|3|N>` (N is for none)
  - Example: `rtm priority 8573921 2`
- **Postpone:** `rtm postpone <task_id>` (Postpones the task's due date by 1 day)
  - Example: `rtm postpone 8573921`

### Delete a Task

Delete a specific task using its `task_id`:

```bash
rtm delete <task_id>
```

Example: `rtm delete 8573921`
