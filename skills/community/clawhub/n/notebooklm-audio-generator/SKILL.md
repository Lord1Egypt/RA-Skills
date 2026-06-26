---
name: notebooklm-audio-generator
description: Automates uploading multiple sources (files, URLs, YouTube, Drive, text) to a NotebookLM notebook, generating a deep dive audio overview in a preferred language, and downloading the result. It guides the user through notebook management, source addition, audio generation, and downloading using the notebooklm-mcp-cli.
---

# NotebookLM Audio Generator Skill

This skill automates the process of using Google's NotebookLM to generate a deep-dive audio overview from various sources and download it to a specified directory.

## Prerequisites

This skill relies on the `notebooklm-mcp-cli` package and the `epub2txt` utility for `.epub` support. Before proceeding, ensure the user has them installed and authenticated.

### Installation & Setup

If the user has not set up the CLI or the conversion tool, instruct them to do so first:

1. **Install the NotebookLM CLI:**
   ```bash
   uv tool install notebooklm-mcp-cli
   # OR
   pip install notebooklm-mcp-cli
   ```
2. **Authenticate:**
   ```bash
   nlm login
   ```
3. **Install epub2txt (for .epub support):**
   The skill expects `epub2txt` to be installed in your programs directory. Clone and initialize it using the following commands:
   ```bash
   mkdir -p ~/Programs
   cd ~/Programs
   git clone https://github.com/SPACESODA/epub2txt.git
   cd epub2txt
   chmod +x run.sh
   ./run.sh  # This initializes the virtual environment
   ```

## Workflow

When activated, follow these steps **strictly** in order. Do not skip steps.

### Step 1: Gather Information

Ask the user for the following information one by one to prepare for the generation:
1. Ask for a desired name for the new notebook. If not provided, use the default name "Audio Overview Notebook".
2. **Source Selection:** Ask the user to select their sources from the following options:
   - **Local Files:** `.pdf`, `.txt`, and `.epub` (which will be automatically converted). Use GUI pickers:
     - **macOS:** `osascript -e "set theFiles to choose file with prompt \"Select your source file(s):\" multiple selections allowed true" ...`
     - **Linux:** `zenity --file-selection --multiple ...`
     - **Windows:** PowerShell `OpenFileDialog`.
   - **Web/Video URLs:** Ask the user to provide any website or YouTube URLs.
   - **Google Drive:** Ask for Google Drive Document IDs.
3. **Preferred Language:** Ask the user for the preferred output language (BCP-47 code).
   - **Options:** Provide common choices: `en` (English - default), `zh` (Chinese), `ja` (Japanese), `es` (Spanish), `fr` (French), `de` (German).
4. **Download Destination:** Use a GUI directory picker to select where the audio file should be saved.

**Crucial:** Ask the user interactively to confirm they have provided/selected all the sources they wish to include before proceeding.

### Step 2: Create a New Notebook

Use the `notebook_create` tool to create a new notebook with the provided name. Keep track of the `notebook_id`.

### Step 3: Upload Sources

- Loop through all gathered sources:
  - **EPUB Files:** Convert to `.txt` first: `cd ~/Programs/epub2txt && ./run.sh "<path>"`. Use the new `.txt` path.
  - **Other Files:** Use `source_add(source_type="file", file_path="...")`.
  - **URLs/YouTube:** Use `source_add(source_type="url", url="...")`.
  - **Drive:** Use `source_add(source_type="drive", document_id="...")`.
- Always set `wait=true` to ensure sources are processed.

### Step 4: Generate Audio Overview

- Use the `studio_create` tool to start the audio generation.
  - Set `notebook_id` to the ID.
  - Set `artifact_type` to `audio`.
  - Set `audio_format` to `deep_dive`.
  - Set `audio_length` to `long`.
  - **Language:** Use the user's selected BCP-47 code (e.g., `zh`).
  - **Custom Prompt:** If the selected language is NOT English (`en`), you MUST provide the following `focus_prompt` to encourage a longer, more detailed output:
    > "Please provide an extremely detailed deep dive. Analyze each source file thoroughly without omitting any details. The conversation should be as long as possible, aiming for over 40 minutes."
  - Set `confirm` to `true`.

### Step 5: Monitor Generation Status

- **Inform the user:** Explicitly tell the user that generating a long, deep-dive audio overview can take 5 to 15 minutes.
- Use the `studio_status` tool with `action: status` in a polling loop (using `run_shell_command` with `sleep 300` between checks) until the `status` becomes `completed`.
- Note the `audio_url` and `artifact_id` when finished. **Crucial:** If there are multiple audio artifacts returned in the status, always identify and note the **latest one** (the one with the most recent `created_at` timestamp).

### Step 6: Download the Audio

- Using the `artifact_id` of the latest audio, try using the `download_artifact` tool first to save the audio to the destination path with an `.mp3` extension.

### Step 7: Final Verification

- Verify the downloaded file using `file <output_path>`.
- Inform the user that the process is complete.