# Playwright Draft Flow

This document outlines the step-by-step automation flow for the draft assistant.

## Flow Steps

1. **Launch Visible Browser:**
   - Playwright launches a Chromium browser in `headless=False` mode.
   - **Crucial:** No `storage_state` or cookies are injected or read. The user logs in completely manually.

2. **Navigate to Juejin Creator Center:**
   - Go to `https://juejin.cn/creator/content/article/draft`.
   - Wait for the user to solve any login or security prompts manually.

3. **Open Markdown Editor:**
   - Wait for the editor input field to appear.

4. **Fill Content (Assistant Mode):**
   - Safely read from the restricted local `/output/juejin/` directory.
   - Fill the title and markdown content.

5. **Stop and Wait for Human:**
   - The script explicitly stops and defaults to NOT saving the draft automatically.
   - The user must review the checklist, fill tags, upload covers, save the draft, and ultimately click "Publish".
