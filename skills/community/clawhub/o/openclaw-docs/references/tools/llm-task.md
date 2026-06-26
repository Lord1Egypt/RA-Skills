# LLM Task

Source: https://docs.openclaw.ai/tools/llm-task

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationBuilt-in toolsLLM TaskGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Tools
Built-in tools
LobsterLLM TaskExec ToolWeb Toolsapply_patch ToolElevated ModeThinking LevelsReactions
Browser
Browser (OpenClaw-managed)Browser LoginChrome ExtensionBrowser Troubleshooting
Agent coordination
Agent SendSub-AgentsMulti-Agent Sandbox & Tools
Skills
Slash CommandsSkillsSkills ConfigClawHubPlugins
Extensions
Voice Call PluginZalo Personal Plugin
Automation
HooksCron JobsCron vs HeartbeatAutomation TroubleshootingWebhooksGmail PubSubPollsAuth Monitoring
Media and devices
NodesNode TroubleshootingImage and Media SupportAudio and Voice NotesCamera CaptureTalk ModeVoice WakeLocation Command
On this page
- [LLM Task](#llm-task)
- [Enable the plugin](#enable-the-plugin)
- [Config (optional)](#config-optional)
- [Tool parameters](#tool-parameters)
- [Output](#output)
- [Example: Lobster workflow step](#example-lobster-workflow-step)
- [Safety notes](#safety-notes)

​LLM Task
`llm-task` is an **optional plugin tool** that runs a JSON-only LLM task and
returns structured output (optionally validated against JSON Schema).
This is ideal for workflow engines like Lobster: you can add a single LLM step
without writing custom OpenClaw code for each workflow.
​Enable the plugin

- Enable the plugin:

Copy```
{
  "plugins": {
    "entries": {
      "llm-task": { "enabled": true }
    }
  }
}

```

- Allowlist the tool (it is registered with `optional: true`):

Copy```
{
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": { "allow": ["llm-task"] }
      }
    ]
  }
}

```

​Config (optional)
Copy```
{
  "plugins": {
    "entries": {
      "llm-task": {
        "enabled": true,
        "config": {
          "defaultProvider": "openai-codex",
          "defaultModel": "gpt-5.2",
          "defaultAuthProfileId": "main",
          "allowedModels": ["openai-codex/gpt-5.3-codex"],
          "maxTokens": 800,
          "timeoutMs": 30000
        }
      }
    }
  }
}

```

`allowedModels` is an allowlist of `provider/model` strings. If set, any request
outside the list is rejected.
​Tool parameters

- `prompt` (string, required)

- `input` (any, optional)

- `schema` (object, optional JSON Schema)

- `provider` (string, optional)

- `model` (string, optional)

- `authProfileId` (string, optional)

- `temperature` (number, optional)

- `maxTokens` (number, optional)

- `timeoutMs` (number, optional)

​Output
Returns `details.json` containing the parsed JSON (and validates against
`schema` when provided).
​Example: Lobster workflow step
Copy```
openclaw.invoke --tool llm-task --action json --args-json &#x27;{
  "prompt": "Given the input email, return intent and draft.",
  "input": {
    "subject": "Hello",
    "body": "Can you help?"
  },
  "schema": {
    "type": "object",
    "properties": {
      "intent": { "type": "string" },
      "draft": { "type": "string" }
    },
    "required": ["intent", "draft"],
    "additionalProperties": false
  }
}&#x27;

```

​Safety notes

- The tool is **JSON-only** and instructs the model to output only JSON (no
code fences, no commentary).

- No tools are exposed to the model for this run.

- Treat output as untrusted unless you validate with `schema`.

- Put approvals before any side-effecting step (send, post, exec).

LobsterExec Tool⌘I