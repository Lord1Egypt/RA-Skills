<div align="center">
  <h1>📝 Google Keep Skill</h1>
  <h3>Headless Google Keep Automation via Undetected Chrome</h3>
  <br/>
  <p>
    <img src="https://img.shields.io/badge/python-≥3.11-blue" alt="Python">
    <img src="https://img.shields.io/badge/nodriver-Chrome_Automation-orange.svg" alt="nodriver">
    <img src="https://img.shields.io/badge/Google_Keep-Integration-4285F4.svg?logo=google&logoColor=white" alt="Google Keep">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
    <img src="https://img.shields.io/badge/version-1.0.0-blueviolet" alt="Version">
  </p>
</div>

🗒️ **Google Keep Skill** is a **CLI automation tool** that interacts with Google Keep through an undetected headless Chrome browser powered by `nodriver`.

⚡️ Create, read, update, delete, and archive notes — all from the command line with **structured JSON output**.
This acts as a solid primitive for LLM Agents and MCP (Model Context Protocol) Servers, providing bulletproof automation over Google Keep.

🔒 Bot-proof: uses a real Chrome instance with a persistent session, bypassing Google's bot detection entirely.

## 📢 News

- **2026-03-02** 🎉 Released **v1.0.0** — Completely refactored the Basic CRUD (Create, Read, Update, Delete) and Archive functions. The tool now runs with maximum stability using in-memory reads, smart DOM selectors, native CDP/React interactions, and strict JS injection security.

## 🚀 Future Features

The skill is constantly evolving! Upcoming updates will focus on granular operations:
- **Granular List Editing:** Modify, delete, or check a single item in an existing list (currently, the update command replaces the entire list).
- **Partial Update:** Ability to edit only the `title` of a note, preserving the original content in the cloud with 0% risk of formatting loss.
- **Colors and Labels (Tags):** Full support for changing color palettes and adding metadata to existing notes.
- **Pinning:** Command to pin/unpin notes to the top.

## Key Features

🗒️ **Full CRUD Operations**: Create, read, update, delete, and archive notes — text or list type.

📋 **List Support**: Create checklist-style notes with individual items, each properly injected as separate list entries.

🔐 **Persistent Session**: Login once manually; the session is saved and reused across all headless executions.

📄 **Structured JSON Output**: Every command returns clean, parseable JSON. Ideal for LLM Agents to parse and format into beautiful Markdown.

🖥️ **Headless by Default**: Runs without a visible browser window — perfect for server-side automation and CI/CD.

## 🏗️ Architecture

The skill follows a **CLI → Browser Automation → DOM Interaction** pattern, isolating authentication from note operations.

<table align="center" width="100%">
  <tr>
    <th width="30%">Layer</th>
    <th width="30%">Technology</th>
    <th width="40%">Responsibility</th>
  </tr>
  <tr>
    <td><b>🖥️ CLI Interface</b></td>
    <td>argparse / Python</td>
    <td>Parses commands and arguments, dispatches to async handlers.</td>
  </tr>
  <tr>
    <td><b>🌐 Browser Engine</b></td>
    <td>nodriver (undetected Chrome)</td>
    <td>Launches headless Chrome, manages tabs, executes CDP commands.</td>
  </tr>
  <tr>
    <td><b>🔐 Auth Layer</b></td>
    <td>CDP Cookies / Chrome Profile</td>
    <td>Persists Google session securely via OS-level `~/.config/google-keep-skill` directory with strict permissions.</td>
  </tr>
  <tr>
    <td><b>🎯 DOM Interaction</b></td>
    <td>JavaScript / CDP Input</td>
    <td>Finds elements by aria-label and text content, injects values securely avoiding XSS payloads.</td>
  </tr>
  <tr>
    <td><b>📤 Output</b></td>
    <td>JSON (stdout)</td>
    <td>Returns structured success/error responses for automation consumers to render.</td>
  </tr>
</table>

## ✨ Commands

All commands are executed via the CLI. The backend works unconditionally across Google Keep's dynamic interface.

```bash
cd /path/to/google-keep-skill && uv run python scripts/keep.py <command>
```

### ⚙️ Global Flags
* `--visible`: Appended before the command (e.g., `keep.py --visible update ...`). Forces `nodriver` to run the browser in visible mode (headful) instead of secretly executing in the background. Useful for debugging or visually confirming operations.

### 1. System & Session
* `login`: Opens Chrome for manual Google login (one-time setup). The session is bound to the robot's profile and ignored by Git.
* `logout`: Clears the currently saved active session data.
* `check`: Programmatically verifies if the saved session cookie is still valid without heavily interacting with the UI.

### 2. Basic Notes CRUD
* `list [--limit N] [--filter "text"]`
  * Passively extracts notes from the DOM grid. Supports case-insensitive text filtering. Returns notes classified as `text` (Normal) or `list` (Task Lists), always retrieving contents as arrays (lines). Automatically ignores Google Keep's "ghost notes".
* `read --title "T"`
  * Actively scans the DOM to extract exclusively the note whose title exactly matches `"T"`, returning all its data and type into memory.
* `create --title "T" --content "C"`
  * Creates a simple **text** note. Uses CDP interactions and async injection. Accepts the `\n` literal in the `content` parameter to elegantly simulate paragraph line breaks.
* `create-list --title "T" --items "A, B, C"`
  * Creates a special **list** type note. The iterative parameter splits commas, typing item by item and simulating organic ENTERs to invoke Google's JavaScript/React chain and build the "checkboxes".
* `update --title "T" [--content "C"]`
  * **The Most Complex Command.** Restructures both Normal and List Notes dynamically:
    * **Normal Text:** Copies original state, actively clears canvas (`Ctrl+A` and `Delete` via organic keyboard events), and re-injects line by line.
    * **Lists:** Simulates `MouseEvent` flows on the exclusion nodes to zero out the list, and then sequentially injects the new `--content` simulating `create-list` logic.
* `delete --title "T"` / `archive --title "T"`
  * Extremely precise. They open the note in modal mode and interact lowly with the floating menu to delete/archive it instantly without relying on unstable screen coordinates grids.

## 🔗 Agent / MCP Usage

When an LLM Agent or MCP server wraps this skill:
1. **Always format the output.** Do not vomit the raw JSON to the user. Extract `data.notes` and format lists as Markdown checklists (`- [ ] Item`) or Markdown unordered lists.
2. **Handle session drops gracefully.** If `success: false` and the message mentions "Session expired", clearly inform the user to run the `login` command in the terminal.
3. **Always read before updating.** If required to append or edit an existing note, the agent MUST call `read` first, rebuild the state in its context, and push the complete rewritten string into `update`.

## 🔧 Usage Examples

```bash
# 1. Text Note Creation
uv run python scripts/keep.py create --title "Meeting Notes" --content "Discuss roadmap\nReview budget\nAssign tasks"

# 2. List Note Creation
uv run python scripts/keep.py create-list --title "Groceries" --items "Milk, Bread, Coffee, Eggs"

# 3. Universal Listing
uv run python scripts/keep.py list

# 4. Listing With Filters (Returns max 5 tickets containing "meeting")
uv run python scripts/keep.py list --filter "meeting" --limit 5

# 5. Specific Local Scan
uv run python scripts/keep.py read --title "Meeting Notes"

# 6. Updating an Entire List (Resetting previous items)
uv run python scripts/keep.py update --title "Groceries" --content "Milk\nAlmond Milk\nSugar"

# 7. Updating the Content of a Text Note
uv run python scripts/keep.py update --title "Meeting Notes" --content "Updated content exclusively"

# 8. Clearing the Board (Delete and Archive)
uv run python scripts/keep.py delete --title "Old Note"
uv run python scripts/keep.py archive --title "Completed Task"
```

## 🔐 Session Persistence

<table align="center" width="100%">
  <tr>
    <th width="25%">Storage</th>
    <th width="40%">Path</th>
    <th width="35%">Purpose</th>
  </tr>
  <tr>
    <td><b>Chrome Profile</b></td>
    <td><code>~/.config/google-keep-skill/chrome-profile/</code></td>
    <td>Full browser state (cookies, cache, localStorage).</td>
  </tr>
  <tr>
    <td><b>Cookie Backup</b></td>
    <td><code>~/.config/google-keep-skill/cookies.json</code></td>
    <td>CDP cookie backup restored on each headless session.</td>
  </tr>
</table>

> [!IMPORTANT]
> These files are stored securely in the user's OS home directory with `0o700`/`0o600` permissions. They are completely decoupled from the skill codebase to prevent data leaks.

## 🧪 Testing

```bash
# Run the End-to-End test suite (requires active session)
uv run python scripts/test_crud.py
```

## ⚠️ Limitations

- CSS selectors may break if Google updates the Keep UI
- Requires one-time manual login (session is persistent afterward)
- Only one Chrome instance can use the profile at a time

## 👤 Author

**Ricardo Reichert**

## 📜 License

This project is released under the [MIT License](LICENSE).
