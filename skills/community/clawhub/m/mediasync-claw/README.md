<div align="center">

# MediaSync-Claw: Remote P2P Media Server & Streaming Skill for OpenClaw

**[ 🌐 Visit Official Website & Full Documentation ](https://poly-ai.chat/mediasync-claw)**

[English](README.md) | [简体中文](README_ZH.md) | [日本語](README_JA.md) | [Deutsch](README_DE.md) | [Español](README_ES.md)

</div>

---

## 📖 Overview & Core Value

**MediaSync-Claw** is a dedicated **OpenClaw Skill** and **Remote P2P Media Server** developed by [Poly AI](https://poly-ai.chat). 

Its core value is enabling users to access, index, and stream their local home PC media library **anytime, anywhere via WhatsApp** using the OpenClaw AI agent. The generated media list supports seamless playback with the **AIpollo Player** via high-speed P2P tunneling. 

For advanced configurations, enterprise support, and the latest updates, please visit our **[Official Product Page](https://poly-ai.chat/mediasync-claw)**.

---

## ⚙️ Prerequisites

* **OpenClaw**: Ensure OpenClaw is deployed and running in your local environment.
* **Firewall / Antivirus Whitelist**: Add an exception (trust rule) for `frpc.exe` in your Windows Defender or antivirus software. *We ensure that `frpc.exe` is completely safe and unaltered.*

---

## 🚀 Step-by-Step Installation & Usage

1. **Download & Install**: Clone or download this repository into your OpenClaw skills directory.
2. **Setup Media Library**: Create a `videos` directory inside the skill folder and place the MP4 video files you wish to access remotely into it.
3. **Configure WhatsApp**: Connect and configure your WhatsApp channel within OpenClaw.
4. **Launch Skill**: Run the MediaSync-Claw skill in OpenClaw.
5. **Remote Command via WhatsApp**: In your WhatsApp chat, send natural language requests (e.g., when you want to view, list, search, or play local videos/playlists from your video library) to trigger this skill and generate the media list.
6. **One-Click Playback**: Click the generated link from the media list to start streaming on AIpollo Player.

---

## 🔒 Security Disclosures & Risk Management

### Risk 1: Public Network Routing via FRP Reverse Proxy
To provide convenient remote media streaming across restricted local networks, this skill establishes an outbound tunnel using the FRP (Fast Reverse Proxy) client (`frpc`) to connect with an `frps` relay server. This enables public routing for your local media service via the `*.yunfrp.net` domain.

### Risk 2: Plaintext HTTP Transmission & P2P Stream Architecture
The actual video streaming of this skill relies on **P2P direct connections**. HTTP is strictly used for transmitting lightweight control instructions and never carries sensitive personal user data.

### Risk 3: Automated `frpc.exe` Binary Retrieval
To support cross-network NAT traversal and reverse proxying, the required `frpc.exe` binary is fetched directly from official GitHub releases to ensure maximum supply-chain integrity and security.

---

## 🛡️ Best Practice Recommendations

* **Dedicated Server / Virtual Machine**: For optimal security, we strongly recommend running this media server skill on a standalone secondary device or within an isolated Virtual Machine (VM) rather than on your primary workstation.
* **Routine Maintenance**: Keep your host operating system, OpenClaw environment, and security patches updated regularly.

---

## 💻 Platform Compatibility

* **Current Support**: Windows (x64)
* **Roadmap**: Linux / macOS support is under active development.

*If you need support for other platforms or encounter network traversal issues, please open a GitHub Issue or reach out to us. Thank you for your support and trust!*