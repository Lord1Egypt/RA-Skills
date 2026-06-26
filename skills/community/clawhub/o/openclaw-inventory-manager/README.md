# Where are you from (OpenClaw Skill Inventory Manager) 📦🦀

An enterprise-grade asset manager for OpenClaw that automates the auditing, tracking, and synchronization of installed skills to your personal GitHub repository.

## 🚀 Overview

Managing numerous AI skills from different sources (**ClawHub**, **GitHub**, **NPM**, **Manual**) can lead to path confusion, "ghost" skills, and security risks. 

**Where are you from** was created to solve these problems by providing a unified audit trail for your AI workstation. No matter where you downloaded a skill from, this tool knows its origins and history.

## 🛠️ Prerequisites

*   **OpenClaw**: Installed and configured.
*   **Node.js**: **Version 14 or higher is required.** The manager script runs on Node.js.
*   **Git**: Required for the synchronization feature.

## 📁 Project Structure

```text
.agents/skills/openclaw-inventory-manager/
├── SKILL.md                 # English instructions & metadata
├── PUBLISH.md               # Publishing-ready summary & motivation
├── inventory.js              # Main CLI entry point
├── utils/                   # Modular utility libraries
│   ├── scanner.js           # Directory scanning & depth control
│   ├── securityScrubber.js  # Regex-based masking (10+ patterns)
│   ├── gitManager.js        # Git CLI automation
│   ├── sourceDetector.js    # Origin & method detection
│   ├── manifestGenerator.js # JSON/Markdown report creation
│   └── logger.js            # Unified logging utility
└── templates/
    └── manifest-template.md # Customizable report template
```

## 📖 Getting Started

1.  **Bootstrap (Recommended)**: For first-time users, run the guided setup wizard:
    ```bash
    node inventory.js bootstrap
    ```
2.  **Scan**: Run `node inventory.js status` to see what's installed and where it came from.
3.  **Sync**: Run `node inventory.js sync --push` to update your manifests and push to GitHub.

For a step-by-step walkthrough, see [TUTORIAL.md](./TUTORIAL.md).  
For full technical documentation, see [SKILL.md](./SKILL.md).

---
*Where are you from? Know your origins. Stay secure.*
