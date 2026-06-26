# DingTalk DEAP Agent Integration

> [中文版](DEAP_AGENT_GUIDE.md)

Connect DingTalk [DEAP](https://deap.dingtalk.com) Agent with [OpenClaw](https://openclaw.ai) Gateway to enable natural language-driven local device operations.

## Key Features

- ✅ **Natural Language Interaction** - Users type natural language commands in the DingTalk chat (e.g., "Find PDF files on my desktop"), and the Agent automatically parses and executes the corresponding operations
- ✅ **NAT Traversal** - Designed for local devices without public IPs, establishing a stable communication tunnel between local and cloud environments via the Connector client
- ✅ **Cross-Platform Support** - Provides native binaries for Windows, macOS, and Linux, ensuring smooth operation across all platforms

## System Architecture

This solution uses a layered architecture with three core components:

1. **OpenClaw Gateway** - Deployed on the local device, provides a standardized HTTP interface for receiving and processing operation commands from the cloud, leveraging the OpenClaw engine to execute tasks
2. **DingTalk OpenClaw Connector** - Runs locally, building a communication tunnel between local and cloud environments to solve the problem of local devices without public IPs
3. **DingTalk DEAP MCP** - An extension module for the DEAP Agent, responsible for forwarding user natural language requests to the OpenClaw Gateway via the cloud tunnel

```mermaid
graph LR
    subgraph "DingTalk App"
        A["User chats with Agent"] --> B["DEAP Agent"]
    end

    subgraph "Local Environment"
        D["DingTalk OpenClaw Connector"] --> C["OpenClaw Gateway"]
        C --> E["PC Operation Execution"]
    end

    B -.-> D
```

## Implementation Guide

### Step 1: Set Up the Local Environment

Ensure the OpenClaw Gateway is installed and running on your local device. The default address is `127.0.0.1:18789`:

```bash
openclaw gateway start
```

#### Configure Gateway Parameters

1. Visit the [Configuration Page](http://127.0.0.1:18789/config)
2. In the **Overview**, set the Gateway Token and save it securely:
   ![alt text](images/image-5.png)
3. Switch to **Infrastructure** and enable the `OpenAI Chat Completions Endpoint`:
   ![alt text](images/image-6.png)

4. Click the `Save` button in the top-right corner to save your configuration

### Step 2: Obtain Required Parameters

#### Get corpId

Log in to the [DingTalk Developer Platform](https://open-dev.dingtalk.com) to find your enterprise CorpId:

<img width="864" height="450" alt="Get corpId from DingTalk Developer Platform" src="https://github.com/user-attachments/assets/18ec9830-2d43-489a-a73f-530972685225" />

#### Get apiKey

Log in to the [DingTalk DEAP Platform](https://deap.dingtalk.com), navigate to **Security & Permissions** → **API-Key Management** to create a new API Key:

<img width="1222" height="545" alt="DingTalk DEAP Platform API-Key Management" src="https://github.com/user-attachments/assets/dfe29984-4432-49c1-8226-0f9b60fbb5bc" />

### Step 3: Start the Connector Client

1. Download the installer for your operating system from the [Releases](https://github.com/hoskii/dingtalk-openclaw-connector/releases/tag/v0.0.1) page
2. Extract and run the Connector in the corresponding directory (macOS example):

   ```bash
   unzip connector-mac.zip
   ./connector-darwin -deapCorpId YOUR_CORP_ID -deapApiKey YOUR_API_KEY
   ```
   ![alt text](images/image-7.png)

### Step 4: Configure the DEAP Agent

1. Log in to the [DingTalk DEAP Platform](https://deap.dingtalk.com) and create a new agent:

   <img width="2444" height="1486" alt="Create New Agent" src="https://github.com/user-attachments/assets/0b7f0855-f991-4aeb-b6e6-7576346b4477" />

2. In the skill management page, search for and integrate the OpenClaw skill:

   <img width="3430" height="1732" alt="Add OpenClaw Skill" src="https://github.com/user-attachments/assets/d44f0038-f863-4c1f-afa7-b774d875e4ba" />

3. Configure skill parameters:

   | Parameter    | Source     | Description                                                                            |
   | ------------ | ---------- | -------------------------------------------------------------------------------------- |
   | apikey       | From Step 2 | DEAP Platform API Key                                                                  |
   | apihost      | Default     | Typically `127.0.0.1:18789`. On Windows, you may need to use `localhost:18789` instead |
   | gatewayToken | From Step 1 | Gateway authentication token                                                           |

   <img width="3426" height="1752" alt="Configure OpenClaw Skill Parameters" src="https://github.com/user-attachments/assets/bc725789-382f-41b5-bbdb-ba8f29923d5c" />

Note that OpenClaw is an MCP, so you also need to configure its trigger rules. The MCP will only be invoked when the rules are satisfied:
<img width="1088" height="526" alt="image" src="https://github.com/user-attachments/assets/8b0b6f6d-70ff-4edc-b674-7a24126aadfa" />

4. Publish the Agent:

   <img width="3416" height="1762" alt="Publish Agent" src="https://github.com/user-attachments/assets/3f8c3fdb-5f2b-4a4b-8896-35202e713bf3" />

### Step 5: Start Using

1. Search for and find your Agent in the DingTalk App:

   <img width="1260" height="436" alt="Search for Agent" src="https://github.com/user-attachments/assets/30feff80-1b28-4274-830b-7045aed14980" />

2. Start your natural language conversation:

   <img width="1896" height="1240" alt="Chat with Agent" src="https://github.com/user-attachments/assets/2a80aab8-3fbf-4d18-beea-770577cb1a40" />
