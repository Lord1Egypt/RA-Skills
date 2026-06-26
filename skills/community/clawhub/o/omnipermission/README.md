# OmniPermission Plugin for OpenClaw

**OmniPermission** is a security-first plugin that places a "Human-in-the-Loop" gatekeeper between the AI and high-risk actions. It pauses sensitive plugin actions (like Slack, Telegram, or GitHub) and sends a **Push Notification** to your mobile device via OmniPersona for approval.

---

## 🚀 Installation & Setup

### 1. Install & Enable

Run the following commands to download and activate the plugin within your OpenClaw environment:

```bash
# Install the plugin
openclaw plugins install omnipermission

# Enable the plugin
openclaw plugins enable omnipermission

# Authorize the plugin to use lifecycle hooks (Necessary)
openclaw config set plugins.allow "[\"omnipermission\"]"

```

### 2. Restart the Gateway

**Crucial:** For the hooks and security authorization to take effect, you must restart the OpenClaw gateway:

```bash
openclaw gateway restart

```

### 3. Connect to OmniPersona

The plugin connects to your mobile app using a secret key.

1. **Download the app:**
* [Download on the App Store](https://apps.apple.com/us/app/omnipersona/id6553972082)
* [Get it on Google Play](https://play.google.com/store/apps/details?id=ai.youki.omni.persona&hl=en)


2. **Copy your Key:** Find your unique secret key on the **Home Page** of the OmniPersona mobile app.
3. **Link it:** Run the following command and paste your key when prompted:

```bash
openclaw omnipermission set-key

```

---

## 🛠️ Security Configuration

By default, all tools work without permission. You choose exactly what to control.

### Intercept Tools

Specify which skills/plugins you want to gatekeep. If a skill is on this list, the agent cannot use it without your mobile consent.

```bash
openclaw omnipermission blacklist-tools

```

Example input: `slack, telegram, github, message`

### View Configuration

Check your saved key, your active blacklist, and the current backend environment.

```bash
openclaw omnipermission status

```

### Reset Protection

Wipe the blacklist completely to allow all plugins to run freely.

```bash
openclaw omnipermission clear-blacklist

```

---

## 🧪 Environment Management

If you are a developer testing new features or using a staging environment, you can toggle the backend target. This setting is stored in the plugin's local state.

### Enable Dev Mode

Point the plugin to the development backend (`backend.dev.ecrop.de`):

```bash
openclaw omnipermission enable-dev-mode

```

### Disable Dev Mode (Default)

Switch back to the production backend:

```bash
openclaw omnipermission disable-dev-mode

```

---

## 🛡️ How it Works

1. **Interception**: The plugin monitors the `before_tool_call` hook for any skill in your blacklist.
2. **Mobile Alert**: The agent's **Intent** and **Parameters** are sent to your phone.
3. **Approval**: The agent remains paused until you tap **Approve** in the OmniPersona app.
