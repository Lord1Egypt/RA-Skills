# God of all Browsers 🚀

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](_meta.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Engine: Puppeteer](https://img.shields.io/badge/Engine-Puppeteer--Core-green.svg)](https://pptr.dev/)

**A 100x smarter browser automation CLI that mimics human behavior using a native stateful Chromium instance.**

Designed specifically for AI-native workflows, `God of all Browsers` solves the gap between vision-less AI and complex, bot-protected websites. It provides a stateful interaction layer that allows AI agents to navigate, interact, and extract data exactly like a human user.

---

## ✨ Key Features

- **🧠 Vision Abstraction (Snapshots):** Instead of navigating raw DOM, it maps every interactable element to a simple `[tag]` ID (e.g. `[1]`, `[15]`). Clicks and types are performed on these tags, eliminating CSS selector brittle-ness.
- **🔄 Stateful & Multi-Tab:** Launches a persistent background Chromium instance. Navigations, clicks opening new tabs, and cookies are preserved across separate CLI calls.
- **🛡️ Bot Evasion:** Built-in techniques to bypass detection:
  - Custom User-Agents and spoofed Canvas signatures.
  - Headless/Non-headless toggles.
  - Automatic `webdriver` footprint removal.
- **💾 Persistent Sessions:** Uses a dedicated `chrome_profile` directory to store login states, sessions, and cookies permanently.
- **🤖 AI-First Commands:** Commands like `google`, `auth-status`, and `log-learning` are tailored for autonomous agents to succeed and self-correct.

---

## 🛠️ Installation & Setup

### Requirements
- **Node.js** (v16+)
- **Google Chrome** or **Chromium** installed on your system.
- **NPM Package Manager**

### Setup (Linux/macOS)
```bash
./setup.sh
```

### Setup (Windows)
```powershell
# Install dependencies
npm install puppeteer-core

# Ensure Chrome is installed at:
# C:\Program Files\Google\Chrome\Application\chrome.exe
```

---

## 🚀 Quick Start (Recommended Workflow)

1.  **Launch the Core**: Start the persistent browser in the background.
    ```bash
    node browser.js start
    ```

2.  **Take a Snapshot**: Navigate to a site and get the visual "tag" map.
    ```bash
    node browser.js snapshot --url "https://news.ycombinator.com"
    ```

3.  **Interact via Tags**: Click the first article link (assuming tag 1).
    ```bash
    node browser.js click --tag "[1]"
    ```

4.  **Extract Data**: Read the content of the article.
    ```bash
    node browser.js read --tag "[5]"
    ```

5.  **Shutdown**: Close the browser when finished.
    ```bash
    node browser.js stop
    ```

---

## 📖 Command Reference

| Command | Purpose | Example |
| :--- | :--- | :--- |
| `start` | Launches the stateful browser instance. | `node browser.js start [--headless]` |
| `snapshot` | Captures DOM/Screenshots & maps tags. | `node browser.js snapshot [--url URL]` |
| `click` | Clicks an element by `[tag]` identifier. | `node browser.js click --tag "[15]"` |
| `type` | Types text into an input field by `[tag]`. | `node browser.js type --tag "[5]" --text="..."` |
| `press` | Simulates a keyboard key press. | `node browser.js press --key "Enter"` |
| `read` | Extracts text from a tag or CSS selector. | `node browser.js read --selector "h1"` |
| `check-tabs`| Lists all currently open browser tabs. | `node browser.js check-tabs` |
| `switch-tab`| Changes focus to a specific tab index. | `node browser.js switch-tab --index 1` |
| `eval` | Executes custom JS inside the browser. | `node browser.js eval --file script.js` |
| `google` | Performs a Google Search + Data Extraction. | `node browser.js google --q "Puppeteer"` |
| `auth-status`| Checks if the current page requires login. | `node browser.js auth-status` |
| `save-session`| Persists current cookies to `session.json`. | `node browser.js save-session` |
| `stop` | Gracefully closes the browser process. | `node browser.js stop` |

---

## 🔬 Advanced Usage: `eval` Power

The `eval` command allows injecting complex, asynchronous logic directly into the browser context.

**Example: Scrape all links from a search results page**
```bash
node browser.js eval --code "return Array.from(document.querySelectorAll('a')).map(a => ({ text: a.innerText, href: a.href }))"
```

You can also run scripts from files:
```bash
node browser.js eval --file "./custom_files/extract_contacts.js"
```

---

## 🧠 Self-Learning Mechanism

Designed for autonomous agents, every failure can be logged to help the AI "learn" and avoid repeating mistakes in future tasks.
```bash
node browser.js log-learning --failed "Popup blocked click" --fixed "Use expand first"
```

---

## 📁 Project Structure

- `browser.js`: Core Puppeteer automation engine.
- `SKILL.md`: Detailed instructions for AI agents (Model-readable).
- `chrome_profile/`: Persistent user data directory (auto-generated).
- `custom_files/`: Directory for your custom script injections.
- `session.json`: Exported cookie/session data.
- `recordings/`: Snapshots and screenshots for manual review.

---

## 🛡️ Security & Ethics

`God of all Browsers` is a powerful tool designed for responsible automation. Users should be aware of the following security considerations:

### 1. **Data Persistence**
*   **Persistent Profiles**: By default, this tool saves all session data, cookies, and local storage in the `./chrome_profile/` directory. This is intentional to allow stateful AI workflows.
*   **Cookie Export**: The `save-session` command exports cookies to `session.json` in plain text. Always treat this file as a sensitive credential.

### 2. **Arbitrary Code Execution (`eval`)**
*   The `eval` command is a high-risk feature that allows executing arbitrary JavaScript inside the browser context. Only use scripts from trusted sources and monitor agent-generated scripts for potential data exfiltration.

### 3. **Bot Evasion & Ethics**
*   Built-in evasion techniques (User-Agent spoofing, canvas signatures) are intended to allow robust automation on bot-protected sites (e.g., public data extraction). They should **not** be used for malicious activities, including bypassing security controls, credential stuffing, or unauthorized access.

### 4. **Best Practices**
*   Run the tool in an isolated or containerized environment if the automation task involves untrusted input or high-risk browsing.
*   Regularly clear the `chrome_profile` and `session.json` if they are no longer needed.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
