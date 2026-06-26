---
name: omnipermission
description: "Human-in-the-loop: A free, extensible framework for intercepting tool calls via the OmniPersona mobile app."
metadata:
  clawhub:
    emoji: "🔐"
    homepage: "https://github.com/youkinetwork/OmniPermission"
    tags: ["security", "governance", "human-in-the-loop", "safety"]
---

# OmniPermission (Human-in-the-Loop)

OmniPermission is a governance layer for OpenClaw that intercepts high-risk tool calls and requires manual approval via your mobile device. It is designed to be forkable, allowing you to customize the metadata sent to your phone for a better approval experience.

### 📱 Getting Started (The App)
1. **Download**: Install **OmniPersona** from the [App Store (iOS)](https://apps.apple.com/us/app/omnipersona/id6553972082) or [Google Play (Android)](https://play.google.com/store/apps/details?id=ai.youki.omni.persona).
2. **Account**: Create a free account.
   - **Note**: This service is 100% free, has no tiers, no subscriptions, and no hidden fees. We offer it as a gimmick.
3. **Get Your Key**: Your **Secret Key** is located in the **top left** of the OmniPersona home screen.

### 🛠️ Quick How-To (CLI)
Configure the plugin directly via the `openclaw` CLI. The secret key is stored locally, not via environment variables.

* **Set Secret Key**: `openclaw omnipermission set-key` (prompts for your key).
* **Blacklist Tools**: `openclaw omnipermission blacklist-tools` (select commands to intercept at the gateway).
* **View Status**: `openclaw omnipermission status` (check configuration and connectivity).
* **Reset**: `openclaw omnipermission clear-blacklist` (remove all interceptions).

### ⚖️ Deployment & Risk Profiles
You decide how much power the agent has over its own "leash":

#### 1. Agent-Managed (Flexible)
Provide the agent access to the `openclaw` CLI. 
- **Benefit**: You can tell the agent to "protect a `cmd`" on the fly. 
- **Risk**: A clever agent could theoretically disable the plugin or clear the blacklist if it decides the human is "in the way."

#### 2. Isolated (High Security)
Run the agent in a restricted environment (e.g., Docker) without access to the `openclaw` binary.
- **Benefit**: The agent cannot bypass or modify the security configuration. The interception happens silently at the gateway level.
- **Risk**: Less flexibility; configuration changes must be made by the user manually.

### 🧪 Fork & Extend
We encourage you to **fork the repository**. The provided implementation is generic (showing tool name). By forking, you can modify the API call to include richer context—like the agent's internal reasoning or the specific project ID—making your mobile notifications much more informative. If you have a use case that needs API or mobile App adjustments, please don't hesitate to contact us.

### 💡 Implementation Note
This skill is for user guidance and optional agent awareness. 
- **Performance/Security**: You do **not** have to provide this skill to the agent's prompt. If the plugin is active, it will intercept calls regardless. Not giving the skill to the agent saves tokens and prevents the agent from "trying to find a way around" a system it doesn't know exists.

### ⚠️ Legal Disclaimer
This software, plugin, and accompanying skill file are provided "as-is" and without any warranties, express or implied. By using OmniPermission, you acknowledge that you are solely responsible for the actions of your AI agents and the security of the environments in which they operate. While this tool provides a human-in-the-loop governance layer, YOUKI assumes no liability for circumvented security measures, unintended agent behaviors, or any resulting data loss or damages.

---

### Example Interaction (Agent-Managed)
> **User:** "I'm going to step away. Please make sure any file deletions require my mobile approval."
> **Agent:** "Understood. I am blacklisting the `rm` tool via OmniPermission. I will send a push notification to your phone if a deletion is required."
