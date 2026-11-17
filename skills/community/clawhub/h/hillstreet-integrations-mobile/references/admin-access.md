# Open-Connect admin access

1. Call `open_connect_status` through the original installed connector. Read its actual scopes.
   Keep ChatGPT action approval settings, Open-Connect account roles, client scopes, project grants
   and provider consent separate. **Allow all actions** changes only the host approval preference.
2. For `configure_connection`, `execute_plan`, `decide_control_approval`, `create_capability_draft`,
   `record_run_outcome` and `install_capability`, require both an Admin/legacy Owner account and
   `control:write`. Other policy and provider checks still apply; a scope does not install an executor.
3. If `control:write` is absent, use the signed-in owner key-management UI at
   `https://open-connect.site/api-keys` to update the exact active owned connection key, or reconnect
   with explicit OAuth consent requesting the scope after deployed discovery advertises it.
   Preserve the key's organization, workspace, project, expiry and value. Do not update grants by
   direct SQL, impersonate a user session, or add the scope silently to default consent.
4. Verify the original connector after its authentication cache refreshes (up to 30 seconds).
   Inspect actual scopes again. Do not test access by changing a production connection or sending
   a message. If the host cannot present authorization, report the exact owner action required.
5. Create or edit credential values in the authenticated **Secrets** UI at
   `https://open-connect.site/secrets`. `list_credential_metadata` and `match_browser_credentials`
   return metadata only. `configure_connection` accepts an opaque `credential://` reference.
   Never put raw secrets in tool arguments, plugins, skills, logs or source files.
6. Treat `secure_injection_available: false` as a missing browser integration. An account match
   does not sign in. Use only the browser host's supported authentication flow; do not extract
   cookies or fill through another transport after a native credential protection blocks access.
7. Update remote MCP behavior in its owning repository and deployment. Preserve plugin/App IDs,
   endpoint, OAuth bindings and audience. Refresh tools through the host's supported app settings
   after deployment; a package version bump alone does not refresh cached tool schemas or grants.
8. Report source validation, deployment, plugin release, live client grants and successful operations
   separately. Do not call unsupported operations enabled or a standby worker actively monitoring.


## Resource management (discover before use)

Call `get_admin_access` to distinguish the actual account role from token grants.
Discover the live schema before assuming a deployment or connector refresh is complete.
For personal Admin keys with both `resources:write` and `control:write`:

1. Search existing personal resources to avoid duplicates. Read `get_owned_resource` before editing.
2. Create a private draft with `create_resource`; use type `toolkit`, `tool`, `skill`, or the matching resource type.
3. Upload plain Markdown, JSON or text with `upload_resource_content` (maximum 256 KiB). Use authenticated Studio for ZIP packages. Never upload private keys or credential exports.
4. Pass the exact returned `updated_at` as `expected_updated_at` to every upload/edit/publication request. A conflict requires rereading the record.
5. Metadata edits and uploads reset verification and unpublish the resource. Complete the separate security review before `set_resource_publication` with `confirm=true` and explicit user authorization to publish.
6. Read back the resource. Creation/upload is not publication, installation, or execution. Project/workspace/organization keys cannot manage the personal library.

Use `get_credential_management` for the authenticated Secrets screen. It provides a destination only, not a completed credential action. Credential creation, value retrieval, editing and deletion occur in that authenticated UI. `list_credential_metadata` remains metadata-only; do not claim raw-value access or secure injection through MCP. Keep credentials out of resource packages and tool arguments.

## Tool discovery and synchronization

Treat server deployment, Composio toolkit discovery and ChatGPT tool discovery as separate stages. If `control:write` is already present but the new resource tools are missing, refresh the existing custom MCP toolkit/app through its supported host settings. Do not rotate keys, recreate accounts, or silently widen OAuth consent to repair a schema cache. Rerun status and `get_admin_access` after rediscovery; only claim a write capability verified after its exact tool schema and account role are proven.

Preview account sync before applying it. If every matched account already exists and candidates is empty, sync is reconciled; do not duplicate imports or assign unrelated project access. Keep secret values in the authenticated Secrets UI and opaque references in connector configuration.
