---
name: traecli
description: TRAE CLI installation, configuration and usage guide. TRAE CLI is an AI-powered CLI programming assistant supporting natural language driven development.
read_when:
  - Installing TRAE CLI
  - Configuring TRAE
  - Using TRAE commands
  - Troubleshooting TRAE issues
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["sh","curl"]}}}
allowed-tools: Bash(*), Read(*), Write(*), Edit(*)
---

# TRAE CLI Skill

## What is TRAE CLI?

TRAE CLI is your dedicated Code Agent. You can send natural language instructions to TRAE CLI to complete a series of complex development tasks from code writing, testing to Git operations, allowing you to focus on higher-value creative work.

### Core Features

- **Code Writing & Modification**: Add new features, fix bugs, or refactor existing code based on requirements
- **Code Understanding & Q&A**: Quickly answer code questions about project architecture, business logic, function implementation, etc.
- **Feature Testing & Debugging**: Run lint tools and unit tests, fix failed test cases, and help troubleshoot and fix potential issues
- **Git Operation Automation**: Simplify Git workflows, such as automatically creating commit messages, resolving merge conflicts, querying commit history, etc.
- **Third-party Capability Integration**: Flexibly integrate third-party tools and services through the Model Context Protocol (MCP)
- **Large Language Models**: Built-in multiple large language models, supporting configuration and use of models provided by OpenAI and Claude

### Product Advantages

- **Ready to Use**: Simple configuration, can be used in projects immediately after installation without complex environment setup
- **Highly Extensible**: Easily integrate custom tools and large language models through configuration files to meet team-specific needs
- **Task Automation**: Automate tedious and repetitive development tasks so you can focus on more creative work

### Important Notes

- **Usage Limitation**: Only TRAE Enterprise Edition can use TRAE CLI
- **Usage Warning**: TRAE CLI uses Max mode by default, please monitor your usage consumption

## Installation

### macOS & Linux

Execute the following script in your local terminal to install TRAE CLI:

```bash
sh -c "$(curl -L https://lf-cdn.trae.com.cn/obj/trae-com-cn/trae-cli/install.sh)" && export PATH=~/.local/bin:$PATH
```

### Windows (PowerShell)

Execute the following script in PowerShell to install TRAE CLI:

```powershell
irm https://lf-cdn.trae.com.cn/obj/trae-com-cn/trae-cli/install.ps1 | iex
```

**Note**: If the built-in Ripgrep in TRAE CLI is unavailable, you also need to install Visual C++ Redistributable (VC runtime library).

## Quick Start

### Starting TRAE CLI

1. Execute `cd` command to enter your target project
2. Execute the following command to start TRAE CLI:

```bash
traecli
```

3. After startup, you will enter the TRAE CLI interface
4. Enter an instruction or question in the dialog box and send it to TRAE CLI. For example: "Explain the architecture of this project"
5. TRAE CLI will prompt you to log in to your enterprise account
6. Log in to your enterprise account and complete authorization, then return to TRAE CLI
7. TRAE CLI will start analyzing the question and generating a response

### Upgrading TRAECLI

TRAE CLI supports both automatic and manual upgrades:

- **Automatic Upgrade**: When you start TRAE CLI, if the current version is not the latest, TRAE CLI will start automatic upgrade and prompt the status in the lower right corner
- **Manual Upgrade**: Use `traecli update` command to manually upgrade

## Usage Scenarios

### Understanding Unfamiliar Codebases

When working with a new project, use TRAE CLI to quickly establish an overall understanding of the codebase.

**Examples:**

- **Understand project architecture**: "What is the overall architecture of this project? Please explain with a directory tree and text."
- **Track core business flows**: "What is the payment flow in our system? What key services and function calls are involved?"
- **Locate specific functionality**: "Where is the user permission validation logic implemented?"
- **Analyze complex module design**: "Tell me about the design of the cache module, including caching strategies and invalidation mechanisms."

### Writing and Modifying Code

TRAE CLI can help you develop new features, fix bugs, write documentation, etc.

**Examples:**

- **Update documentation**: "Update the README.md file to add a description of 'support multi-model switching' in the feature introduction section."
- **Add business logic**: "Add an input parameter validation to the order creation interface to ensure that the user ID cannot be empty."
- **Fix complex issues**: "There is a race condition in the background worker queue implementation. Please help me locate and fix it."

### Testing and Debugging

TRAE CLI can help you run unit tests, locate problems, and provide fix suggestions.

**Examples:**

- **Run unit tests and fix issues**: "Run all unit tests and try to fix those failed test cases."
- **Investigate security vulnerabilities**: "Scan the code for possible SQL injection vulnerabilities and provide fix suggestions."
- **Analyze failure causes**: "The build on CI failed. Help me analyze the logs and find out the cause of the failure."

### Automating Git Operations

Let TRAE CLI handle Git commands for you.

**Examples:**

- **Quick commit**: "Help me commit the staged files with the commit message 'feat: add user profile page'."
- **Query commit history**: "Find out which commit modified the login page UI style."
- **Handle complex branch operations**: "Rebase my current branch to the main branch and automatically resolve conflicts during the process."

### Using TRAE CLI in Automation Scripts

TRAE CLI supports running in non-interactive mode. You can conveniently integrate TRAE CLI into CI/CD pipelines or other automation scripts to achieve development process automation.

**Examples:**

- **Update README automatically in CI script based on recent Git commits**:
  ```bash
  traecli --allowed-tool Bash,Edit,MultiEdit,Write -p "update README with latest changes"
  ```

- **Automatically run a pre-written Prompt template in CI script**:
  ```bash
  traecli -p /command arg1 arg2
  ```

## Command Line Arguments

You can use the following command line arguments to pass additional information:

| Argument | Description |
|----------|-------------|
| `--allowed-tool` | Specify automatically allowed tools, such as "Bash", "Edit", "Replace", etc. Multiple tools are separated by commas. Can be specified multiple times. |
| `--bash-tool-timeout` | Set the maximum running time for commands executed through the Bash tool. After timeout, execution will be automatically terminated, e.g., 30s, 5m, 1h. |
| `-c / --config` | Override settings in "k=v" format. |
| `--disallowed-tools` | Specify automatically disabled tools. Multiple tools are separated by commas. Can be specified multiple times. |
| `-h / --help` | Get usage help for TRAE CLI. |
| `--json` | Output complete information in JSON format, including System Prompt, tool calls, execution process, and final results. Only used with `--print`. |
| `-p / --print` | Print response content and exit immediately, suitable for pipe scenarios. |
| `--query-timeout` | Set the maximum execution duration for a single query. Timeout will terminate the query, e.g., 30s, 5m, 1h. |
| `-v / --version` | View the current version of TRAE CLI. |

## Slash Commands

In a session, use slash commands to execute quick operations, manage session state, and customize common workflows.

### Built-in Slash Commands

| Command | Purpose |
|---------|---------|
| `/agent-new` | Create a new custom agent. |
| `/clear` or `/reset` | Clear conversation history and release context. |
| `/feedback` | Submit feedback or report issues. |
| `/init` | Initialize a new AGENTS.md file for the current directory. |
| `/login` | Log in to TRAE CLI. |
| `/logout` | Log out of TRAE CLI. |
| `/mcp` | Manage MCP Server and tools. |
| `/model` | Switch the AI model being used. |
| `/plugin` or `/plugins` | Manage plugins. |
| `/status` | Display TRAE CLI status information. |
| `/terminal-setup` | Install the Shift+Enter shortcut for line breaks. |

### Custom Slash Commands

You can define commonly used prompts as Markdown files, and TRAE CLI will execute them as custom slash commands.

#### Syntax

```
/<command-name> [arguments]
```

**Parameter Description:**

- `<command-name>`: Name derived from the Markdown file name (without the `.md` extension)
- `[arguments]`: Optional arguments passed to the command

#### Creating Custom Slash Commands

1. Use `mkdir -p .traecli/commands` to create the `.traecli/commands` directory in the project root
2. Use `cd .traecli/commands` to enter the `.traecli/commands` directory
3. Create a Markdown format custom slash command configuration file in the `.traecli/commands` directory
4. Configure the custom slash command and save

**Frontmatter Field Description:**

| Frontmatter | Description | Example |
|-------------|-------------|---------|
| `description` | Brief description of this custom slash command. | `Review code changes with context` |
| `argument-hint` | Arguments required by the slash command (/). This hint will be displayed to the user when performing slash command auto-completion. | `argument-hint: add [tagId] \| remove [tagId] \| list` |
| `tools` | Specify available tools. Multiple tools are separated by commas. | `Read,Write,mcp__{$mcp_server_name}__{$tool_name}` |
| `model` | Specify the model to use. | `kimi-k2` |

**Example:**

```markdown
---
description: Review code changes with context
argument-hint: <file-pattern>
model: kimi-k2
tools: Read
---

## Code Review Request

Files to review: $1

Current git diff: !`git diff HEAD -- $1`

File structure: !`find . -name "$1" -type f | head -10`

## Your task

Please perform a thorough code review of specified files focusing on:

1. **Code Quality**: Check for best practices, readability, and maintainability
2. **Security**: Look for potential security vulnerabilities
3. **Performance**: Identify potential performance issues
4. **Testing**: Suggest areas that need test coverage
5. **Documentation**: Check if code is properly documented

Provide specific suggestions for improvement with line numbers where applicable.
```

#### Other Features

TRAE CLI provides a series of special syntaxes for dynamically referencing parameters, setting default values, and inserting system command execution results in command definitions, greatly enhancing the flexibility and reusability of custom commands.

**`$ARGUMENTS`**

The `$ARGUMENTS` placeholder captures all arguments passed to the command, separated by spaces between multiple arguments.

Example:

```bash
# Command definition
echo 'Deploying service: $ARGUMENTS to staging environment' > .traecli/commands/deploy-service.md

# Usage
> /deploy-service auth-api v2.3.1
# $ARGUMENTS becomes: "auth-api v2.3.1"
```

**`$N`**

You can access specific parameters individually by positional parameters `$N`, just like in shell scripts.

Example:

```bash
# Command definition
echo 'Deploy service $1 to environment $2 with version $3' > .traecli/commands/deploy-service.md

# Usage
> /deploy-service auth staging v1.4.2
# $1 becomes "auth", $2 becomes "staging", $3 becomes "v1.4.2"
```

**!`command`**

!`command` is used to execute the specified command and insert its standard output result directly into the current position as text content.

For example, in the following command definition, `!`cat VERSION`` will be executed when TRAE CLI processes the file. TRAE CLI will run `cat VERSION`, then get its standard output (e.g., 1.4.0), and finally replace the `!`cat VERSION`` segment with the output content.

```bash
# Command definition
echo "Project version: !`cat VERSION`" > traecli/commands/show-version.md

# After replacement
Project version: 1.4.0
```

**`${N:-DefaultValue}`**

`${N:-DefaultValue}` is used to provide default values for variables.

- If variable N is not defined or is empty, use DefaultValue as a substitute
- If variable N is defined and has a non-empty value, use the variable's own value

Example:

```bash
# Command definition
echo 'Deploying to environment: ${1:-staging}' > .traecli/commands/deploy.md

# Usage
# Case 1: User provided parameter and defined $1="production"
> /deploy production
# ${1:-staging} becomes "production"

# Case 2: User did not provide parameter, $1 is undefined
> /deploy
# ${1:-staging} becomes "staging"
```

## Troubleshooting

### Installation Issues

**Problem**: Installation script fails to execute

**Solution**:
- Ensure you have network access to `lf-cdn.trae.com.cn`
- Check if `curl` is installed on your system
- For Windows, ensure PowerShell execution policy allows running scripts

**Problem**: TRAE CLI command not found after installation

**Solution**:
- Make sure you added `~/.local/bin` to your PATH
- On macOS & Linux: `export PATH=~/.local/bin:$PATH`
- On Windows: Restart PowerShell after installation

### Runtime Issues

**Problem**: Ripgrep not working

**Solution**:
- On Windows, install Visual C++ Redistributable (VC runtime library)
- Download from Microsoft's official website

**Problem**: Login issues

**Solution**:
- Ensure you have a TRAE Enterprise Edition account
- Check your network connection
- Use `/login` command to re-authenticate

**Problem**: Command timeout

**Solution**:
- Use `--bash-tool-timeout` to increase timeout for long-running commands
- Use `--query-timeout` to increase query timeout
- Example: `traecli --bash-tool-timeout 10m --query-timeout 5m`

### Performance Issues

**Problem**: High usage consumption

**Solution**:
- TRAE CLI uses Max mode by default, which may consume more resources
- Consider using a lighter model with `/model` command
- Monitor your usage regularly

## Best Practices

1. **Start Simple**: Begin with simple questions to understand your codebase before complex tasks
2. **Use Custom Commands**: Create custom slash commands for repetitive tasks to improve efficiency
3. **Git Integration**: Let TRAE CLI handle Git operations to ensure consistent commit messages
4. **CI/CD Integration**: Use non-interactive mode for automation scripts
5. **Monitor Usage**: Keep track of your usage consumption, especially when using Max mode
6. **Review Changes**: Always review code changes suggested by TRAE CLI before applying them

## Additional Resources

- Official Documentation: https://docs.trae.cn/cli
- TRAE CLI Open Source License: https://docs.trae.cn/cli/open-source-software-notice-for-trae-cli
- MCP Documentation: https://docs.trae.cn/cli/model-context-protocol
