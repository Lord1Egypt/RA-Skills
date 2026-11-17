# PhotoFresco error codes

Every failed PhotoFresco tool call is a tool error whose structured content is
`{ ok: false, code, message, hint }`; the text starts with `Error <code>: <message>` and a
`Next:` line. These are all the codes the MCP server can return, with the same next step it gives
in `hint`. Codes not listed here are an operation's own failure: read the message, check
`doc_get_state` and adjust.

Rules that apply to all of them:

- Requests refused before running changed nothing; you may fix the arguments and call again.
- When the outcome is unclear, read `doc_get_state` (and its `revision`) before repeating an edit.
- Never work around the user: codes about pairing, permissions, Pause or Stop mean the user decides.

## Connection, browser and files

| Code | Next step |
|---|---|
| `invalid_options` | The MCP server configuration is invalid; the person who installed it needs to fix its arguments. |
| `invalid_request` | Fix the arguments as the message says and call again. |
| `not_connected` | Call photofresco_connect, tell the user the connection code, and wait for them to click Allow in the PhotoFresco window. |
| `busy` | The server is shutting down or another connect is running; wait a moment and call photofresco_status. |
| `browser_not_found` | No Chrome, Edge or Chromium was found. Ask the user to install one, or to set PHOTOFRESCO_BROWSER in the MCP server configuration. |
| `browser_unsupported` | The browser is too old (Chromium 120 or newer is needed). Ask the user to update it or point PHOTOFRESCO_BROWSER at a newer one. |
| `browser_launch_failed` | The browser did not start. Ask the user to check that it opens normally, then call photofresco_connect again. |
| `profile_in_use` | Another PhotoFresco MCP server or CLI is using the browser profile. Close it, or ask the user to configure --profile ephemeral. |
| `browser_closed` | The PhotoFresco window was closed and the session ended. Call photofresco_connect to open it again (the user must Allow again). |
| `editor_unavailable` | The editor page did not load. Check the network, then call photofresco_connect again. |
| `editor_unsupported` | The editor and this MCP server speak different protocol versions. Ask the user to update the photofresco package. |
| `page_closed` | The PhotoFresco tab was closed and the session ended. Call photofresco_connect to open it again. |
| `page_reloaded` | The editor reloaded and the session ended. Call photofresco_connect; the user must Allow again. |
| `origin_changed` | The PhotoFresco tab left the editor and the session ended. Call photofresco_connect to reconnect. |
| `channel_rejected` | The editor refused the message. Call photofresco_status; reconnect if the session ended. |
| `pairing_denied` | The user declined the connection. Do not retry unless they ask you to. |
| `pairing_expired` | Nobody answered the connection request in time. Call photofresco_connect again when the user is ready. |
| `pairing_canceled` | The connection request was withdrawn. Call photofresco_connect again when the user is ready. |
| `pairing_in_progress` | A connection request is already waiting for the user. Call photofresco_connect again to keep waiting. |
| `session_active` | This server already has a session. Call photofresco_status. |
| `session_ended` | The session ended (the user pressed Stop, closed the window or reloaded). Call photofresco_connect to start a new one. |
| `path_not_granted` | The path is outside the folders the person granted (see photofresco_status roots). Use a granted folder; only the person can grant more in the MCP server configuration. |
| `path_escape` | The path leaves its granted folder through a symbolic link. Use a real path inside the folder. |
| `path_invalid` | The path is not usable; pass an absolute file path inside a granted folder. |
| `file_exists` | The file exists. Choose another name, or pass overwrite: true if the folder allows overwriting and the user wants it replaced. |
| `not_a_file` | The path is a folder or special file; pass a regular file. |
| `file_too_large` | The file is larger than 32 MiB, the import limit. |
| `read_failed` | The file could not be read; check that it exists and is readable. |
| `write_failed` | The file could not be written; nothing was replaced. Check free space and permissions. |
| `artifact_incomplete` | The export changed or arrived out of order; nothing was written. Export again. |
| `artifact_hash_mismatch` | The exported bytes did not match their checksum; nothing was written. Export again. |
| `artifact_too_large` | The export is too large for this transfer. Use photofresco_export_file to write it to a granted folder, or export a smaller format or layer. |
| `operation_failed` | The editor operation failed; read the message, check doc_get_state and adjust. |

## Editor channel

| Code | Next step |
|---|---|
| `unknown_method` | The editor does not support this request; update the photofresco package. |
| `unauthorized` | The editor no longer recognizes this session. Call photofresco_connect. |

## Sessions and permissions

| Code | Next step |
|---|---|
| `consent_required` | External agents are turned off in the editor's Data & privacy settings; only the user can turn them on. |
| `invalid_params` | The arguments do not match the input schema; fix them as the message says. |
| `unknown_operation` | The editor does not know this operation. Check the tool list (photofresco_list_tool_groups). |
| `reserved_operation` | Only the user can do this in the editor; ask them. |
| `capability_denied` | The user has not granted the permission this needs. Call photofresco_request_access with it and explain why; the user decides in the PhotoFresco window. |
| `capability_revoked` | The user revoked a permission while this ran; partial edits stay in History. Ask again with photofresco_request_access if still needed. |
| `budget_exhausted` | The credit budget the user granted is used up or expired. Ask for a new budget with photofresco_request_access. |
| `spending_unavailable` | Paid AI is unavailable (the user is signed out or the service is unreachable). Ask the user to sign in to PhotoFresco. |
| `unknown_session` | The session no longer exists. Call photofresco_connect. |
| `session_stopped` | The user stopped the session. Call photofresco_connect only if they want to continue. |
| `stale_connection` | This connection was replaced. Call photofresco_connect. |
| `session_disconnected` | The session is disconnected. Call photofresco_connect. |
| `too_many_sessions` | The editor has too many agent sessions. Ask the user to stop one. |
| `too_many_requests` | Too many requests are running; wait for them to finish, then call again. |
| `no_target_document` | The session has no target document. Open one with photofresco_import_file or doc_new, or target one with photofresco_attach. |
| `unknown_document` | That document is closed or unknown. Call photofresco_documents. |
| `document_closed` | The target document was closed. Open or target another document. |
| `document_not_active` | The target document is not the active tab. Ask the user to switch to it, or target the active one with photofresco_attach. |
| `target_changed` | The target document changed while this ran. Check doc_get_state, then call again. |
| `lease_held` | Another agent is editing this document. Wait, or ask the user to stop it. |
| `lease_paused` | The user edited the document, so agent edits are paused. Ask them to press Resume in the editor, then check doc_get_state. |
| `lease_lost` | This session lost its edit lease. Check doc_get_state, then call again. |
| `human_busy` | The user is in the middle of a transform or text edit. Wait until they finish, then call again. |
| `stale_revision` | The document changed (revision differs). Re-read doc_get_state and plan from the current state. |
| `request_conflict` | The request ID was reused with different arguments. Call again (a new ID is generated). |
| `outcome_unknown` | The outcome is unknown. Check doc_get_state and the revision before retrying; do not blindly repeat. |
| `unknown_pairing` | The connection request is gone. Call photofresco_connect. |
| `too_many_pairings` | Too many connection requests are waiting in the editor. Ask the user to answer or dismiss them. |

## Previews and exports

| Code | Next step |
|---|---|
| `invalid_region` | The region is invalid; use whole pixels with positive width and height. |
| `region_out_of_bounds` | The region lies outside the canvas; check the document size with doc_get_state. |
| `preview_too_large` | The preview would be too large; use a smaller scale or max_size (the message names the largest usable scale). |
| `unknown_layer` | No layer has that ID; read the layer IDs from doc_get_state. |
| `unsupported_layer_kind` | This layer kind is not supported here; choose another layer. |
| `mask_unavailable` | That layer has no raster mask, or there is no selection. |
| `export_failed` | The export failed; read the message and try another format. |
| `export_timeout` | The export took longer than 120 s; try PNG or a smaller document. |
| `artifact_limit` | Too many exports are held in the editor; release old ones (artifact_release) or wait 10 minutes. |
| `artifact_unknown` | No export with that ID belongs to this session. Export again. |
| `artifact_expired` | The export expired (exports live 10 minutes). Export again. |
| `artifact_evicted` | The export was evicted by newer exports. Export again. |
| `artifact_released` | The export was released. Export again. |
| `artifact_document_mismatch` | The export belongs to a document that is not the active target. Switch back to it or export again. |
| `invalid_range` | The offset is outside the artifact. |

## Workflows

| Code | Next step |
|---|---|
| `workflow_invalid` | The workflow is invalid; fix it as the message says and validate it again before running. |
| `version_mismatch` | An operation in the workflow changed since it was saved; update those steps to the current schema and validate again. |
| `workflow_refused` | The workflow cannot run as given (the message says why); change it and validate again. |
| `workflow_step_failed` | A workflow step failed and the run stopped; steps before it stay applied. Read the message and doc_get_state, then roll back or continue. |
| `document_changed` | The document changed while the workflow ran, so it stopped. Check doc_get_state before continuing. |
| `workflow_busy` | Another workflow is running; wait for it to finish or cancel it. |
| `unknown_run` | No retained workflow run has that ID; list the recent runs. |
| `rollback_conflict` | The run was not rolled back because the document changed after it; nothing was undone. Undo step by step with history_undo if needed. |
| `rollback_unavailable` | This run cannot be rolled back (the message says why); nothing was undone. |

## This server

| Code | Next step |
|---|---|
| `unknown_tool_group` | Use a group ID from photofresco_list_tool_groups. |
| `internal_error` | The MCP server hit an unexpected error; call photofresco_status and try again. |
