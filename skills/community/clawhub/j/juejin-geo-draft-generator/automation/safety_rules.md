# Automation Safety Rules

To comply with OpenClaw/ClawHub security standards, the automation script MUST strictly adhere to the following safety boundaries.

## 1. No Auto-Publishing (Human-in-the-loop)
- **Rule:** The script must never click the final publish button.
- **Reason:** Content must be manually reviewed before publication.

## 2. No Credential or Data Harvesting
- **Rule:** The script must NEVER read, export, print, or save `cookie`, `localStorage`, `sessionStorage`, `storage_state`, or any login credentials.
- **Reason:** Extreme protection of user privacy and account security.

## 3. Strict Local Path Boundary
- **Rule:** The script must only read files from the `/input/` and `/output/juejin/` directories within the project. It must not accept arbitrary absolute paths or read outside the project folder.
- **Reason:** Prevents path traversal and unauthorized file access.

## 4. No Dynamic Code Execution
- **Rule:** The script must not use `eval`, `exec`, or dynamically execute external code.
- **Reason:** Prevents injection attacks.

## 5. Yield to Anti-Bot Mechanisms
- **Rule:** If the script encounters a CAPTCHA, security validation, or risk control prompt, it must **STOP** immediately.
- **Reason:** It is a draft filling assistant, not an exploit tool. Bypassing security is strictly forbidden.

## 6. Manual Draft Saving Preferred
- **Rule:** The script defaults to NOT clicking "Save Draft". If the save button is unstable, it must fail gracefully and prompt the user to click it.
- **Reason:** Respects platform UI changes and avoids erroneous clicks.
