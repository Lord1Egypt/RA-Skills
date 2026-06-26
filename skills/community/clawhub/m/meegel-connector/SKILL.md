---
name: meegle-connector
description: Connect to Meegle via MCP service, support OAuth authentication, and enable querying and managing work items, views, etc.
version: 1.0.9
homepage: https://www.npmjs.com/package/@lark-project/meego-mcporter
metadata:
  openclaw:
    homepage: https://www.npmjs.com/package/@lark-project/meego-mcporter
    emoji: 📋
    requires:
      bins:
        - node
        - npx
      config:
        - ~/.mcporter/credentials.json
    install:
      - kind: node
        package: "@lark-project/meego-mcporter"
        bins:
          - meego-mcporter
---

# Meegle Skill

Connect to Meegle via MCP service, supporting OAuth authentication.

## Prerequisites

This skill relies on the following environment:

- **Node.js** (>= 18) and `npx`
- **@lark-project/meego-mcporter**: MCP Transfer Tool, sourced from npm (`npm install -g @lark-project/meego-mcporter` or automatically obtained via `npx`)

## Certificate Management Instructions

This skill uses `~/.mcporter/credentials.json` to store OAuth credentials (managed by mcporter).

- **Method 1 (Recommended)**: Browser OAuth - mcporter automatically completes authorization and writes credentials, and the agent does not need to access the credential content.
- **Method 2 (Remote Server)**: When the server does not have a browser, users need to complete OAuth on their local computers and then sync the credentials to the server. In this process, the agent will assist in displaying the OAuth Client configuration (excluding tokens) and writing the authorized credentials provided by the user, and all operations require users to confirm step by step.

Security Constraints:
- The agent shall not initiate credential operations independently, and each step requires explicit confirmation from the user.
- The agent must not record the credential content to logs, historical messages, or any location other than `~/.mcporter/`
- Temporary files generated during the operation must be cleaned up immediately

## Connection Method

### 1. Ask the user which method to use for authentication

Note: Be sure to ask the user and let the user make an active choice. Automatically choosing for the user is prohibited.
This tool supports two authentication methods:

- **Browser OAuth** (Recommended): Suitable for scenarios where OpenClaw is locally installed, automatically re-engaging the browser to complete authorization
- **Remote OAuth Proxy**: Suitable for scenarios where OpenClaw is installed on a remote server (browserless environment)

### 2. Browser OAuth (Recommended)

#### 2.1. Create a Configuration File

Copy `meegle-config.json` from the skill package directory to the working directory.

#### 2.2. Perform OAuth authentication (only once)

```bash
npx @lark-project/meego-mcporter auth meegle --config meegle-config.json
```

This will open a browser for you to authorize your Feishu account. ** After authorization is completed, the credentials will be cached in `~/.mcporter/credentials.json`, and subsequent calls will not require re-authorization. **

### 3. Remote OAuth Proxy

Applicable Scenario: When the remote server does not have a browser, the user needs to complete OAuth on the local computer and then sync the credentials back to the server.

#### 3.1. Create a Configuration File

Copy `meegle-config.json` from the skill package directory to the working directory.

#### 3.2. Generate OAuth Client Configuration

```bash
npx @lark-project/meego-mcporter auth meegle --config meegle-config.json --oauth-timeout 1000
```

This command will generate an OAuth Client configuration (containing only the client parameters, excluding tokens) in `~/.mcporter/credentials.json`.

#### 3.3. Assist users in completing local authorization

This step requires the agent and the user to cooperate to complete credential synchronization. Since the remote server does not have a browser, the user needs to complete OAuth authorization on their local computer.

**Step A - Present the OAuth Client Configuration to the User (Requires User Confirmation):**

Read the contents of `~/.mcporter/credentials.json` (which at this time only contains OAuth client parameters and no tokens), display them to the user, and inform the user:

> The following is the OAuth Client configuration. Please refer to the document https://meegle.com/b/helpcenter/product/5rifl7a7 to complete the authorization on your local computer. After the authorization is completed, please provide me with the generated credential file.

**Step B - Receive authorized credentials provided by the user (user confirmation required):**

After the user completes OAuth locally, they will provide the authorized credential file. After obtaining user confirmation, write it to `~/.mcporter/credentials.json`.

After the write operation is completed, immediately clean up any intermediate temporary files that may have been generated during the operation. The credential content is only stored in `~/.mcporter/credentials.json` and must not be saved to any other location.

#### 3.4. Verify the Authorization Result

Attempted to connect to the MCP server and confirmed successful authorization.

### 4. Subsequent Use

```bash
npx @lark-project/meego-mcporter call meegle <tool_name> --config meegle-config.json
```

## Available Features

- **Query**: To-do, View, Work Item Information
- **Operations**: Create, modify, and transfer work items
