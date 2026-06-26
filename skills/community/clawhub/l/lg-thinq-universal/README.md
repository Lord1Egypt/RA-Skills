# LG ThinQ Universal Skill

**Connect and manage your LG ThinQ devices seamlessly with OpenClaw.**

This skill acts as a **Universal Manager** that automates the entire integration process. It starts by discovering all LG appliances (ACs, Refrigerators, Washers, etc.) linked to your account. Then, it simplifies management by generating specialized, lightweight OpenClaw skills for each individual device. This approach ensures a secure, private connection that allows for natural language control without ever exposing your sensitive credentials in the device-specific skills.

## 🚀 Quick Start

### 1. Installation
Install the universal skill using `clawhub`:

```bash
clawhub install lg-thinq-universal
```

### 2. Get Your Credentials
You can obtain your **Personal Access Token (PAT)** by following these steps:

1.  Visit the official portal: [https://connect-pat.lgthinq.com](https://connect-pat.lgthinq.com)
2.  Log in with your **ThinQ account**.
3.  Select the **"ADD NEW TOKEN"** button.
4.  Enter a **Token name** (e.g., "OpenClaw-Skill").
5.  Select the features you want to control.
6.  Select the **"CREATE TOKEN"** button.
7.  **Copy** the newly generated token immediately.

### 3. Setup Environment
We recommend setting your credentials in your shell environment for better security.

**Option A: Shell Environment (Preferred)**
```bash
export LG_PAT="your_newly_generated_token"
export LG_COUNTRY="IN"  # Your 2-letter ISO country code (US, GB, IN, etc.)
```

**Option B: .env File (Root Only)**
Create a `.env` file **only** in the `lg-thinq-universal` directory:
```bash
cd ~/.openclaw/workspace/skills/lg-thinq-universal
echo "LG_PAT=your_token_here" > .env
echo "LG_COUNTRY=your_country_code" >> .env
```
> ⚠️ **SECURITY WARNING**: NEVER copy this `.env` file or your `LG_PAT` into the individual device skill folders created later. Those folders must remain isolated for your safety.

---

## 🤖 Step 4: OpenClaw Integration

**Now that your credentials are set, it's time to let OpenClaw handle the rest.**

Paste this simple prompt into your OpenClaw chat to begin the automated setup of your devices:

```text
I have installed the lg-thinq-universal skill and added the tokens. Please follow the SKILL.md to run the discovery setup and help me assemble the workspace for my LG devices.
```

---

## 🛠️ How to Utilize This Skill

### The Universal Manager (`lg-thinq-universal`)
Once the agent is ready, you can manually run management scripts from `~/.openclaw/workspace/skills/lg-thinq-universal/`:
*   `python scripts/lg_api_tool.py list-devices`: See all your connected LG appliances.
*   `python scripts/lg_api_tool.py check-config`: Verify your token and country are set correctly.

### The Device Skills (Generated)
After the setup is complete, you will have specific skills like `lg-ac-livingroom`. You can then talk to OpenClaw naturally:
*   *"OpenClaw, turn on the living room AC."*
*   *"OpenClaw, set the kitchen fridge to 3 degrees."*
*   *"OpenClaw, check if the washer is finished."*

---

## ❓ FAQ & Troubleshooting

### Q: My device is not appearing in the list.
**A:** There are two common reasons:
1.  **Not in App:** Ensure you have added the device to your LG account using the official **LG ThinQ app** on your phone. If it's not in the app, it won't show up here.
2.  **Offline:** Check that the device is "Online" and connected to Wi-Fi in the LG ThinQ app.

### Q: I get a `401 Unauthorized` error.
**A:** Your `LG_PAT` might be expired or incorrect. Double-check your environment variables and regenerate the token if necessary.

### Q: `setup.sh` fails with permission errors.
**A:** Navigate to the directory and run: `chmod +x setup.sh`.

### Q: How do I update the device list?
**A:** Simply run `./setup.sh` again from the `lg-thinq-universal` directory to refresh all profiles.

---

## 🔒 Security Mandates
*   **Zero-Leak**: We never store your `LG_PAT` in generated device skills. They only use a `LG_DEVICE_ID`.
*   **Shell Credentials for Device Skills**: Generated device skills expect `LG_PAT` and `LG_COUNTRY` to be available in the shell when they run.
*   **Local-First**: All API communication happens directly from your machine to LG's servers.
*   **Validation**: Every command uses optimistic locking (`x-conditional-control`) to ensure your device state is always what you expect.

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements, new features, or additional device profiles, feel free to open an issue or submit a pull request.

---
*Made with ❤️ by Utkarsh Tiwari | Welcome contributions!*
