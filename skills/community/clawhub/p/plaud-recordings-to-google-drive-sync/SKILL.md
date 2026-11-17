---
name: plaud-recordings-to-google-drive-sync
description: "Plaud Recordings to Google Drive Sync: Automatically backs up your Plaud recordings to Google Drive and keeps a tracking spreadsheet in Google Sheets. Each time you run this workflow, it downloads any new recordings from your Plaud account to a \"Plaud Recordings\" folder in Drive, creates a transcript for each recording (using Plaud's built-in transcripts when available, or automatic speech-to-text otherwise), saves the transcript alongside the audio file, identifies what each recording is about."
version: 1.0.1
homepage: https://www.agentpmt.com/agent-workflow-skills/plaud-recordings-to-google-drive-sync
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/agent-workflow-skills/plaud-recordings-to-google-drive-sync"}}
---
# Plaud Recordings to Google Drive Sync

## Freshness
Last updated: `2026-08-07`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Workflow Does
Automatically backs up your Plaud recordings to Google Drive and keeps a tracking spreadsheet in Google Sheets. Each time you run this workflow, it downloads any new recordings from your Plaud account to a "Plaud Recordings" folder in Drive, creates a transcript for each recording (using Plaud's built-in transcripts when available, or automatic speech-to-text otherwise), saves the transcript alongside the audio file, identifies what each recording is about (meeting, interview, note, etc.), and logs everything in a spreadsheet with links to the audio and transcript files. You can run this as often as you like - it only processes new recordings and won't duplicate anything. Just connect your Plaud, Google Drive, and Google Sheets accounts and run it whenever you want to sync your latest recordings.

## Required Setup
- AgentPMT overview: `../what-is-agentpmt`.
- Account MCP/REST setup: `../agentpmt-account-mcp-rest-api-setup`.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

## Workflow Session Management
Call `AgentPMT-Workflow-Skills` with `start_workflow` before the first step and `end_workflow` after the final step.

```json
{"action":"start_workflow","skill_id":"plaud-recordings-to-google-drive-sync"}
```

```json
{"action":"end_workflow","skill_id":"plaud-recordings-to-google-drive-sync","rating":5,"comment":"completed"}
```

## Workflow Process
1. Find or Create Sheet
   - Tool product: Google Sheets.
   - Tool skill: `../google-sheets`.
   - ClawHub page: https://clawhub.ai/agentpmt/google-sheets.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill google-sheets`.
   - Marketplace: https://www.agentpmt.com/marketplace/google-sheets-api.
   - Tool instructions: Locate the tracking spreadsheet. First run action 'search' with query 'Plaud Recordings'. If a spreadsheet named exactly 'Plaud Recordings' exists, use its spreadsheet_id; if none exists, run action 'create' with title 'Plaud Recordings' and initial_headers ['Recording ID','Recording Link','Status','Recording Type','Transcript Link','Recorded At'] on the first tab. Then run action 'get_headers' and, for EACH of 'Recording Type', 'Transcript Link', and 'Recorded At' that an existing sheet is missing, add it with action 'append_column' (one call per missing column, in that order). Do not assume the tab is called 'Sheet1' — read the real tab name from get_headers. Output the spreadsheet_id AND the tab name (sheet_name) for all downstream Sheets steps.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
2. Ensure Drive Folder
   - Tool product: Google Drive.
   - Tool skill: `../google-drive`.
   - ClawHub page: https://clawhub.ai/agentpmt/google-drive.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill google-drive`.
   - Marketplace: https://www.agentpmt.com/marketplace/google-drive.
   - Tool instructions: Run action 'ensure_folder_path' with ensure_path 'Plaud Recordings' to create the folder at My Drive root if it does not already exist. Output the resulting folder_id for the upload steps.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
3. Read Logged IDs
   - Tool product: Google Sheets.
   - Tool skill: `../google-sheets`.
   - ClawHub page: https://clawhub.ai/agentpmt/google-sheets.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill google-sheets`.
   - Marketplace: https://www.agentpmt.com/marketplace/google-sheets-api.
   - Tool instructions: Using the spreadsheet_id and sheet_name from the Find or Create Sheet step, run action 'read' with range 'A2:A' to get every value in the 'Recording ID' column below the header. Output the set of Recording IDs already logged. If only the header exists, output an empty set. IMPORTANT: treat this as a fast prefilter only. It is re-checked authoritatively inside the loop at claim time, because another run of this workflow can log recordings after this read happens.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
4. List Plaud Recordings
   - Tool product: Plaud.
   - Tool skill: `../plaud`.
   - ClawHub page: https://clawhub.ai/agentpmt/plaud.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill plaud`.
   - Marketplace: https://www.agentpmt.com/marketplace/plaud.
   - Tool instructions: List ALL of the user's Plaud recordings with action 'list_files' and page_size 100 (the tool's default page_size is only 20, so always pass it explicitly), paginating with 'page' until a page returns fewer results than page_size. For each recording collect its durable 'id', 'name' (reference only), 'start_at' (when the recording began — a naive ISO timestamp in UTC), and 'duration' in milliseconds. Output the complete list of recordings.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
5. Find New Recordings
   - Prompt: Determine which Plaud recordings are not yet logged in the spreadsheet.
6. For Each New Recording
   - Iterate over the configured collection, then continue through the connected workflow path.
7. Summarize Run
   - Prompt: Report the results of the sync run.
8. Get Plaud File
   - Tool product: Plaud.
   - Tool skill: `../plaud`.
   - ClawHub page: https://clawhub.ai/agentpmt/plaud.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill plaud`.
   - Marketplace: https://www.agentpmt.com/marketplace/plaud.
   - Tool instructions: For the current recording, call action 'get_file' with file_id copied EXACTLY from the current recording's 'id' in the List Plaud Recordings output.

ERRORS: a '500 Internal Server Error' almost always means the file_id is wrong or the recording no longer exists — it does NOT mean Plaud is down. Re-check the id and retry once; if it still fails, output {fetch_failed: true}, skip the remaining steps for this recording, and do NOT log a row for it (leaving it unlogged makes the next run retry it). Separately, 'OAuth credential expired or revoked', 'Credential for requirement Plaud OAuth is outdated / connection schema has changed', and a 422 missing_credentials response all mean the SAME thing: the Plaud credential must be re-authorised. Do not spend retries on them — call AgentPMT-Send-Human-Request with request_type enable_tool and stop the run.

AUDIO URL: read 'presigned_url'. When it comes back null, that is USUALLY A TRANSIENT signing failure, not a permanent state — the tool says so in its own response. Wait about 60 seconds and call get_file again, up to 3 attempts total. Only if it is still null after those retries, record presigned_url as unavailable and continue, because a transcript can still be produced from Plaud's own copy.

PLAUD'S OWN TRANSCRIPT: do NOT try to read transcripts out of get_file's 'source_list' — on current accounts that array is routinely empty even for recordings Plaud has processed. Instead call action 'get_transcript' with file_id and block 'transaction' (the raw transcript, with speaker names and timestamps). It returns one page of utterances at a time: whenever the response carries a 'next_cursor', call get_transcript again passing it as 'cursor' until no cursor remains, collecting every utterance. Block 'transaction_polish' returns Plaud's AI-cleaned transcript in the same per-utterance shape if you prefer it. Set has_plaud_transcript true ONLY when this yields at least one non-empty utterance; an empty result or an error here is normal and simply means Plaud has no transcript, so fall through to Speech-to-Text.

Output: presigned_url (or unavailable), recording id, start_at (naive ISO, UTC), duration (ms), has_plaud_transcript, and the collected utterances array when present.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
9. Claim Row in Sheet
   - Tool product: Google Sheets.
   - Tool skill: `../google-sheets`.
   - ClawHub page: https://clawhub.ai/agentpmt/google-sheets.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill google-sheets`.
   - Marketplace: https://www.agentpmt.com/marketplace/google-sheets-api.
   - Tool instructions: Claim this recording in the sheet BEFORE doing any expensive upload or transcription work, so a second run executing at the same time cannot process it as well. This step is the workflow's duplicate guard.

STEP 1 — RE-READ, DO NOT TRUST THE EARLIER SET: call action 'read' on the Plaud Recordings spreadsheet (spreadsheet_id and sheet_name from the Find or Create Sheet step) with range 'A2:A' RIGHT NOW. The logged-ID set gathered at the start of the run is stale by this point — a concurrent run may have logged this very recording in the meantime. Use this fresh read.

STEP 2: if the current recording id already appears in that fresh column A, another run owns it. Output {already_claimed: true}, append NOTHING, and skip every remaining step for this recording — no audio upload, no transcription, no transcript upload, no row update.

STEP 3: otherwise immediately append one row with action 'append_rows' and value_input_option 'USER_ENTERED', as an object keyed by headers: {'Recording ID': the current recording id, 'Recording Link': '', 'Status': 'claimed', 'Recording Type': '', 'Transcript Link': '', 'Recorded At': the recording's start_at exactly as Plaud returned it (naive ISO timestamp, UTC)}. Output {already_claimed: false}.

The blank Recording Link and the placeholder 'claimed' status are filled in by the Update Status & Type step at the end. A row still reading 'claimed' after a run means that run died partway and the recording needs attention.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
10. Upload Audio to Drive
   - Tool product: Google Drive.
   - Tool skill: `../google-drive`.
   - ClawHub page: https://clawhub.ai/agentpmt/google-drive.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill google-drive`.
   - Marketplace: https://www.agentpmt.com/marketplace/google-drive.
   - Tool instructions: If already_claimed is true, do nothing and output an empty Drive audio link. If presigned_url was still unavailable after the retries in the Get Plaud File step, skip the upload and output an empty Drive audio link — that is not a failure. Otherwise upload the recording audio into the Plaud Recordings folder with action 'upload_file_from_storage': source_file_url = the presigned_url, parent_folder_id = the folder_id from the Ensure Drive Folder step, filename '<recording id>.mp3', content_type 'audio/mpeg', max_upload_bytes 262144000. Read uploaded_file.web_view_link from the response and output it as the Drive audio link. Never upload the same recording id twice in one run — Drive happily stores two files with identical names, so a repeated upload silently creates a duplicate.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
11. Get Transcript (Plaud or STT)
   - Tool product: Speech to Text With Speakers.
   - Tool skill: `../speech-to-text-with-speakers`.
   - ClawHub page: https://clawhub.ai/agentpmt/speech-to-text-with-speakers.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill speech-to-text-with-speakers`.
   - Marketplace: https://www.agentpmt.com/marketplace/speech-to-text-with-speakers.
   - Tool instructions: Obtain a transcript for the current recording, preferring Plaud's own.

IF already_claimed is true: do nothing, output {skipped: true, reason: 'claimed by another run'}.
IF has_plaud_transcript is true: do NOT call this tool at all — output {used_plaud_transcript: true} and reuse the utterances collected by get_transcript in the Get Plaud File step.
IF presigned_url is unavailable AND has_plaud_transcript is false: there is nothing to transcribe — output {skipped: true, reason: 'no audio url'}.

OTHERWISE call Speech-to-Text: choose the action by recording duration (up to 15 min 'transcribe_quick', up to 30 min 'transcribe_standard', up to 60 min 'transcribe_extended'; over 60 minutes DO NOT transcribe — output {skipped: true, reason: 'exceeds 60 minute limit'}). Pass public_url set to the presigned_url, output_format 'json', and enable_diarization true ONLY when the recording duration is 20 minutes or less (diarization is provider-limited to 20 minutes — for longer recordings set enable_diarization false). The submit response is a task envelope: if its status is already 'completed', use outputs[0] directly; if 'processing', poll action 'get_task' with the returned task_id every 15 seconds until status is 'completed' or 'failed'. Short clips can still take a couple of minutes, so keep polling rather than giving up.

A task can complete SUCCESSFULLY with an empty result (transcript '', words [], speakers []) when the audio contains no speech. That is a success, not a failure — pass it through so the transcript file is still saved and the row is still finished.

On genuine failure, check error_details.recommended_actions and retry once with the recommended larger tier if one is suggested; otherwise treat as skipped with the error as the reason. Output {used_plaud_transcript: false} plus outputs[0]'s json_data (transcript, words, speakers), result_file_id, and result_signed_url.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
12. Save Transcript to Drive
   - Tool product: Google Drive.
   - Tool skill: `../google-drive`.
   - ClawHub page: https://clawhub.ai/agentpmt/google-drive.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill google-drive`.
   - Marketplace: https://www.agentpmt.com/marketplace/google-drive.
   - Tool instructions: If transcription was skipped for any reason (including already_claimed), do nothing and output {skipped: true}. Otherwise save the transcript JSON into the Plaud Recordings folder (parent_folder_id from the Ensure Drive Folder step) with action 'upload_file_from_storage', filename '<recording id> - transcription.json', content_type 'application/json'.

WHEN used_plaud_transcript is true: base64-encode the utterances array collected via get_transcript in the Get Plaud File step and pass it as source_content_base64 together with that filename. This works regardless of how long the recording is.

WHEN the transcript came from Speech-to-Text: pass the completed task's result_signed_url as source_file_url, or result_file_id as source_file_id if the signed URL is unavailable.

Read uploaded_file.web_view_link from the response and output the transcript file's Drive link.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
13. Distill Recording Type
   - Prompt: Determine the recording's purpose/type from what the speaker says at the very beginning.
14. Update Status & Type
   - Tool product: Google Sheets.
   - Tool skill: `../google-sheets`.
   - ClawHub page: https://clawhub.ai/agentpmt/google-sheets.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill google-sheets`.
   - Marketplace: https://www.agentpmt.com/marketplace/google-sheets-api.
   - Tool instructions: If already_claimed is true, do nothing — the row belongs to another run and must not be touched.

Otherwise finalise this recording's row in the Plaud Recordings spreadsheet (spreadsheet_id and sheet_name from the Find or Create Sheet step) using action 'update_row' with key_column 'Recording ID' and key_value set to the current recording id. ALWAYS set 'Recording Link' to the Drive audio link from the Upload Audio to Drive step (or '' when the audio was unavailable) — the claim row was written with it blank. Then set the rest according to the outcome:
- transcript saved (from Plaud or Speech-to-Text): {'Status': 'transcribed', 'Recording Type': the recording_type from the Distill Recording Type step, 'Transcript Link': the transcript file's Drive link from the Save Transcript to Drive step}
- skipped because the recording exceeded 60 minutes: {'Status': 'download only', 'Recording Type': 'too long to transcribe'}
- skipped for any other reason: {'Status': 'download only', 'Recording Type': 'not transcribed'}

This step is what clears the placeholder 'claimed' status, so it must run for every recording this run actually claimed.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.

## Tool Skill Links
- Google Sheets: `../google-sheets`; ClawHub https://clawhub.ai/agentpmt/google-sheets; skills.sh `npx skills add AgentPMT/agent-skills --skill google-sheets`; marketplace https://www.agentpmt.com/marketplace/google-sheets-api
- Google Drive: `../google-drive`; ClawHub https://clawhub.ai/agentpmt/google-drive; skills.sh `npx skills add AgentPMT/agent-skills --skill google-drive`; marketplace https://www.agentpmt.com/marketplace/google-drive
- Plaud: `../plaud`; ClawHub https://clawhub.ai/agentpmt/plaud; skills.sh `npx skills add AgentPMT/agent-skills --skill plaud`; marketplace https://www.agentpmt.com/marketplace/plaud
- Speech to Text With Speakers: `../speech-to-text-with-speakers`; ClawHub https://clawhub.ai/agentpmt/speech-to-text-with-speakers; skills.sh `npx skills add AgentPMT/agent-skills --skill speech-to-text-with-speakers`; marketplace https://www.agentpmt.com/marketplace/speech-to-text-with-speakers

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Workflow page: https://www.agentpmt.com/agent-workflow-skills/plaud-recordings-to-google-drive-sync
- AgentPMT workflows: https://www.agentpmt.com/agent-workflow-skills
