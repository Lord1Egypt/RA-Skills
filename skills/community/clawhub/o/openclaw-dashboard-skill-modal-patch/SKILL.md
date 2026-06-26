---
name: openclaw-dashboard-skill-modal-patch
description: Repair the OpenClaw Control UI Skills modal when clicking a skill row does nothing and DevTools shows a showModal InvalidStateError because the dialog is not yet in the document.
---

# OpenClaw Dashboard Skill Modal Patch

Use this skill when the OpenClaw dashboard Skills page becomes non-responsive and clicking a skill row fails to open the detail modal.

## Trigger symptom

DevTools shows:

```text
InvalidStateError: Failed to execute 'showModal' on 'HTMLDialogElement': The element is not in a Document.
```

## Fix procedure

1. Open the live bundle:
   ```sh
   nano /opt/homebrew/lib/node_modules/openclaw/dist/control-ui/assets/skills-m2TVOQPH.js
   ```

2. Search for:
   ```text
   showModal()
   ```

3. Replace:
   ```js
   ${r(e=>{!(e instanceof HTMLDialogElement)||e.open||e.showModal()})}
   ```
   with:
   ```js
   ${r(e=>{if(!(e instanceof HTMLDialogElement)||e.open)return;let t=()=>{if(e.open)return;try{e.showModal()}catch{setTimeout(()=>{try{e.showModal()}catch{}},0)}};e.isConnected?t():setTimeout(t,0)})}
   ```

4. Save the file and exit.

5. Hard reload the dashboard:
   - `Cmd+Shift+R`

6. Click a skill row and confirm the modal opens.

## Notes

- This is a UI timing bug, not a skills backend failure.
- If the asset filename changes in a future OpenClaw build, apply the same patch to the current `skills-*.js` bundle referenced by DevTools.
