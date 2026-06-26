---
name: oo-postman
description: "Postman (postman.com). Use this skill for ANY Postman request — reading, creating, updating, and deleting data. Whenever a task involves Postman, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Postman"
  author: "OOMOL"
  version: "1.0.1"
  services: ["postman"]
  icon: "https://static.oomol.com/logo/third-party/Postman.webp"
---

# Postman

Operate **Postman** through your OOMOL-connected account. This skill calls the `postman` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Postman. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "postman" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "postman" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_a_collection` — Tool to create a new Postman collection in a specific workspace or the default workspace. Use when you need to create a collection with workspace specification. For complete collection format details, refer to the Postman Collection Format documentation. [write]
- `create_a_collection_comment` — Tool to create a comment on an API's collection. Use when you need to add a comment to a specific collection within an API. To create a reply on an existing comment, include the thread_id in the request. [write]
- `create_a_collection_from_a_schema` — Tool to create a collection from a schema and link it to an API with specified relations. Note: This endpoint is deprecated in Postman v10 and higher. Use when you need to generate a collection from an API schema and establish relations like contract tests or documentation. [write]
- `create_a_folder` — Tool to create a folder in a Postman collection. Use when you need to organize requests by creating a new folder within a collection. For complete details, see the Postman Collection Format documentation. [write]
- `create_a_folder_comment` — Tool to create a comment on a folder. Use when you need to add a comment to a specific folder in a collection. [write]
- `create_a_fork2` — Tool to create a fork from an existing environment into a workspace. Use when you need to fork an environment to a specified workspace. [write]
- `create_a_mock_server` — Tool to create a new mock server in a Postman collection. Use when you need to create a mock server to simulate API endpoints for testing or development. Returns the created mock server's details including the mockUrl which can be used to make requests. [write]
- `create_a_monitor` — Tool to create a new monitor in a specific workspace to run a collection on a schedule. Use when you need to set up automated collection runs at specified intervals using cron expressions within a workspace. [write]
- `create_a_pull_request` — Tool to create a pull request for a forked collection into its parent collection. Use when you need to propose changes from a forked collection to be merged into the parent collection. The forked collection must exist before creating a pull request. [write]
- `create_a_request` — Tool to create a new request in a Postman collection. Use when you need to add a request to an existing collection with specified method, URL, headers, and body. [write]
- `create_a_request_comment` — Tool to create a comment on a request. Use when you need to add a comment to a specific request within a collection or reply to an existing comment thread. [write]
- `create_a_response` — Tool to create a request response in a Postman collection. Use when you need to add a saved response example to a specific request in a collection. [write]
- `create_a_response_comment` — Tool to create a comment on a response. Use when you need to add a comment to a specific response within a collection or reply to an existing comment thread. [write]
- `create_a_schema` — Tool to create a schema for an API in Postman. Use when you need to add a schema definition (such as OpenAPI, GraphQL, or Protocol Buffers) to an existing API. The schema can consist of single or multiple files. Returns the created schema's ID and metadata upon successful creation. [write]
- `create_a_server_response` — Tool to create a server response on a Postman mock server. Use when you need to simulate 5xx server-level responses (500, 503, etc.) for testing error conditions. [write]
- `create_a_spec` — Tool to create an API specification in Postman's Spec Hub. Use when you need to create single or multi-file specifications in a workspace. Supports various spec types including OpenAPI 3.0, OpenAPI 3.1, and AsyncAPI 2.0. [write]
- `create_a_spec_file` — Tool to create a new file in an API specification. Use when you need to add a new file (such as schema definitions, path configurations, or components) to an existing spec. [write]
- `create_a_webhook` — Tool to create a webhook that triggers a collection with a custom payload. Use when you need to set up a webhook endpoint that can trigger a Postman collection run. The webhook URL is available in the webhookUrl property of the response. [write]
- `create_a_workspace` — Tool to create a new workspace in Postman. Use when you need to create a workspace with a specified name, type (personal, team, private, or public), and optional description. Returns the created workspace's ID, name, and type upon successful creation. [write]
- `create_an_api` — Tool to create a new API in Postman. Use when you need to create an API with a name, summary, and description in your Postman workspace. [write]
- `create_an_environment` — Tool to create a new environment in a Postman workspace. Use when you need to create a new environment with variables for different settings (development, production, testing, etc.). Returns the created environment's ID, name, and UID upon successful creation. [write]
- `create_or_update_a_schema_file` — Tool to create or update an API schema file in Postman. Use when you need to add a new schema file or modify an existing one within an API schema. Requires API ID, schema ID, file path, and stringified JSON content. [write]
- `create_relations` — Tool to create new relations for an API version. Use when you need to link collections or mock servers to an API version as contract tests, test suites, documentation, or mocks. [write]
- `delete_a_collection` — Tool to permanently delete a collection from Postman. Use when you need to remove a collection that is no longer needed. [destructive]
- `delete_a_collections_comment` — Tool to delete a comment from an API's collection. Use when you need to remove a specific comment from a collection. On success, returns HTTP 204 No Content. [destructive]
- `delete_a_folder` — Tool to delete a folder in a Postman collection. Use when you need to remove a folder and all its contents from a collection. The folder ID should not contain spaces to avoid 404 errors. [destructive]
- `delete_a_folders_comment` — Tool to delete a comment from a folder. Use when you need to remove a specific comment from a folder. Returns HTTP 204 No Content on successful deletion. [destructive]
- `delete_a_requests_comment` — Tool to delete a comment from a request. Use when you need to remove a specific comment from a request. On success, this returns an HTTP 204 No Content response. [destructive]
- `delete_a_response` — Tool to delete a response in a Postman collection. Use when you need to remove a saved response from a collection. [destructive]
- `delete_a_responses_comment` — Tool to delete a comment from a response. Use when you need to remove a specific comment from a collection response. On successful deletion, this returns HTTP 204 No Content. [destructive]
- `delete_a_schema_file` — Tool to delete a file in an API schema. Use when you need to remove a specific file from a schema. On success, returns HTTP 204 No Content response. [destructive]
- `delete_a_server_response` — Tool to delete a mock server's server response. Use when you need to remove a specific response from a Postman mock server. [destructive]
- `delete_a_spec` — Tool to delete an API specification from Postman. Use when you need to permanently remove a specification. On success, returns HTTP 204 No Content response. [destructive]
- `delete_a_spec_file` — Tool to delete a file from an API specification. Use when you need to remove a specific file from a multi-file specification. [destructive]
- `delete_a_workspace` — Tool to delete a Postman workspace permanently. Use when you need to remove a workspace and all its contents. Deletion is permanent and cannot be undone. [destructive]
- `delete_an_api` — Tool to delete an API from Postman. Use when you need to permanently remove an API. On success, returns HTTP 204 No Content response. [destructive]
- `delete_an_apis_comment` — Tool to delete a comment from an API. Use when you need to remove a comment from a specific API. On success, this returns an HTTP 204 No Content response indicating the comment was successfully deleted. [destructive]
- `delete_an_environment` — Tool to delete an environment permanently in Postman. Use when you need to remove an environment that is no longer needed. [destructive]
- `delete_monitor` — Tool to delete a monitor by its ID. Use when you need to permanently remove a monitor from Postman. The monitor ID must be provided to identify which monitor to delete. [destructive]
- `duplicate_a_collection` — Tool to create a duplicate of a collection in another workspace. Use when you need to copy an existing collection to a different workspace. Returns an asynchronous task that can be tracked using the duplication task status endpoint. [write]
- `fork_collection` — Tool to create a fork of a collection in a specified workspace. Use when you need to fork an existing collection to a workspace.
- `generate_a_collection_from_spec` — Tool to generate a Postman collection from an OpenAPI 2.0, 3.0, or 3.1 specification. Use when you need to create a collection from an existing API spec. The operation is asynchronous and returns a task ID and polling URL to check the generation status.
- `generate_spec_from_collection` — Tool to generate an API specification from a Postman collection. Use when you need to create an OpenAPI 3.0 specification from an existing collection. The operation is asynchronous and returns a task ID and polling URL to check the generation status.
- `get_a_collections_comments` — Tool to retrieve all comments left by users in an API's collection. Use when you need to fetch all comments associated with a specific collection within an API.
- `get_a_collections_forks` — Tool to get all forks of a specific collection. Use when you need to retrieve information about who has forked a collection, including fork IDs, users, and creation dates.
- `get_a_collections_pull_requests` — Tool to get information about a collection's pull requests including source and destination IDs, status, and URLs. Use when you need to retrieve pull request details for a specific collection.
- `get_a_collections_roles` — Tool to get information about all roles in a collection. Use when you need to retrieve the IDs of all users, teams, and groups with access to view or edit a collection.
- `get_a_folder` — Tool to retrieve information about a folder in a Postman collection. Use when you need to fetch details about a specific folder including its name, description, owner, and timestamps.
- `get_a_folders_comments` — Tool to retrieve all comments left by users in a folder. Use when you need to fetch all comments associated with a specific folder within a collection.
- `get_a_monitor` — Tool to retrieve information about a specific monitor in Postman. Use when you need to fetch monitor details including schedule, collection, environment, and run status.
- `get_a_request` — Tool to retrieve information about a specific request in a Postman collection. Use when you need to fetch details about a request including its method, URL, headers, body, authentication, and associated scripts.
- `get_a_requests_comments` — Tool to retrieve all comments left by users in a request. Use when you need to fetch all comments associated with a specific request within a collection.
- `get_a_response` — Tool to retrieve information about a saved response in a Postman collection. Use when you need to fetch details about a specific response including status, headers, body, and metadata.
- `get_a_responses_comments` — Tool to retrieve all comments left by users in a response. Use when you need to fetch all comments associated with a specific response within a collection.
- `get_a_schema` — Tool to retrieve information about an API schema from Postman. Use when you need to fetch schema details for a specific API. Optionally specify a version ID to get a schema published in a specific API version.
- `get_a_spec` — Tool to retrieve information about an API specification in Postman. Use when you need to fetch spec details including name, type, and timestamps.
- `get_a_spec_file` — Tool to get the contents of an API specification's file. Use when you need to retrieve the actual content and metadata of a specific file within a spec.
- `get_a_specs_definition` — Tool to get the complete contents of an API specification's definition. Use when you need to retrieve the full OpenAPI/Swagger specification content for a spec. Returns the raw definition content as a string.
- `get_a_specs_files` — Tool to retrieve all files in an API specification from Postman. Use when you need to list or view specification files for a specific spec ID. Returns file metadata including IDs, names, paths, types, and timestamps.
- `get_a_specs_generated_collections` — Tool to retrieve all collections generated from an API specification in Postman. Use when you need to fetch collections that have been auto-generated from a spec. Returns metadata and an array of generated collections.
- `get_a_team_user` — Tool to get information about a user on the Postman team. Use when you need to retrieve details about a specific team member including their ID, name, email, roles, and join date.
- `get_a_workspace` — Tool to get detailed information about a specific workspace by its ID. Use when you need to retrieve the complete structure of a workspace including all collections, environments, APIs, mocks, and monitors.
- `get_a_workspaces_activity_feed` — Tool to get a workspace's activity feed showing who added or removed collections, environments, or elements, and users joining or leaving. Use when you need to track workspace changes and user activity.
- `get_a_workspaces_roles` — Tool to get the roles of users, user groups, and partners in a workspace. Use when you need to retrieve role assignments and understand who has what level of access to a specific workspace.
- `get_accounts` — Tool to retrieve Postman billing account details for the authenticated team. Use when you need to access account information such as account ID, team ID, account state, billing slots, sales channel, or billing email.
- `get_all_api_releases` — Tool to get all releases for a specific API version in Postman. Use when you need to list releases for an API version. Note: This endpoint is deprecated in Postman v10 and higher.
- `get_all_apis` — Tool to get all APIs accessible to the authenticated user with optional workspace filtering. Use when you need to list or retrieve APIs from Postman. Returns an array of API objects with their IDs, names, summaries, and other metadata.
- `get_all_collections2` — Tool to get all collections accessible to the authenticated user. Use when you need to retrieve all your collections including subscribed collections. Returns detailed information for each collection including owner, creation/update timestamps, and visibility.
- `get_all_environments` — Tool to get all environments accessible to the authenticated user with optional workspace filtering. Use when you need to list or retrieve environments from Postman. Returns an array of environment objects with their IDs, names, and UIDs.
- `get_all_forked_collections` — Tool to retrieve all forked collections for the authenticated user. Use when you need to list or access all collections that the user has forked.
- `get_all_groups` — Tool to get all user groups in a Postman team. Use when you need to list all groups and their details including member counts and timestamps. Returns an array of group objects with their IDs, names, team IDs, user counts, and creation/update timestamps.
- `get_all_linked_relations` — Tool to retrieve all linked relations for a specific API version in Postman. Use when you need to discover what collections, documentation, mocks, or monitors are linked to an API version.
- `get_all_mock_servers` — Tool to get all active mock servers accessible to the authenticated user. Use when you need to list or retrieve mock servers from Postman. By default, returns only mock servers you created across all workspaces. Can be filtered by workspace ID to get mock servers specific to a workspace.
- `get_all_monitors` — Tool to get all monitors accessible to the authenticated user with optional workspace filtering. Use when you need to list or retrieve monitors from Postman. Returns an array of monitor objects with their IDs, names, and UIDs.
- `get_all_specs` — Tool to get all API specifications in a workspace. Use when you need to list or retrieve API specs from a specific Postman workspace. Returns an array of spec objects with their IDs, names, types, and timestamps, along with pagination metadata.
- `get_all_team_users` — Tool to get information about all users on the Postman team. Use when you need to list all team members and their details including roles and join dates. Returns an array of user objects with their IDs, names, usernames, emails, roles, and join timestamps.
- `get_all_test_relations` — Tool to retrieve all test relations for a specific API version. Use when you need to get test relations associated with an API version. Note: This endpoint is deprecated in Postman v10 and higher.
- `get_all_versions` — Tool to get all published versions of a specific API in Postman. Use when you need to list or retrieve version information for an API. Returns an array of version objects with their IDs and names.
- `get_all_workspaces` — Tool to get all workspaces accessible to the authenticated user with optional type filtering. Use when you need to list or retrieve workspaces from Postman. Returns an array of workspace objects with their IDs, names, and types.
- `get_an_api` — Tool to retrieve information about a specific API in Postman. Use when you need to fetch API details including name, description, versions, and schemas.
- `get_an_api_version` — Tool to get information about a specific API version in Postman. Use when you need to retrieve details about a particular version of an API. Returns version details including ID, name, creation date, and associated schemas.
- `get_an_apis_comments` — Tool to retrieve all comments left by users in an API. Use when you need to fetch all comments associated with a specific API.
- `get_an_environment` — Tool to retrieve detailed information about a specific environment in Postman. Use when you need to fetch environment details including name, ID, owner, and all environment variables.
- `get_an_environments_forks` — Tool to retrieve all forked environments for a specific environment. Use when you need to list all environments that have been forked from a particular environment.
- `get_async_collection_update_status` — Tool to get the status of an asynchronous collection update task. Use when you need to check whether a previously initiated async collection update is still processing, has completed successfully, or has failed. The task ID is obtained from PUT /collections/{collectionId} endpoint when using the Prefer: respond-async header. [write]
- `get_authenticated_user` — Tool to get information about the authenticated user. Use when you need to retrieve details about the current authenticated user, including their user ID, username, and email address.
- `get_collection_access_keys` — Tool to retrieve all personal and team collection access keys for the authenticated user. Use when you need to list or manage collection access keys. Returns an array of access key objects with their IDs, tokens, status, and associated collection information.
- `get_contract_test_relations` — Tool to retrieve contract test relations for a specific API version. Use when you need to check contract test associations. Note: This endpoint is deprecated and may return limited or no data.
- `get_documentation_relations` — Tool to get documentation relations for a specific API version. This endpoint is deprecated in Postman v10 and higher.
- `get_duplication_task_status` — Tool to get the status of a collection duplication task. Use when you need to check whether a previously initiated collection duplication is still processing or has completed. The task ID must first be obtained from the POST /collections/{collectionId}/duplicates endpoint.
- `get_environment_relations` — Tool to get environment relations for a specific API version. This endpoint is deprecated in Postman v10 and higher.
- `get_generated_spec` — Tool to retrieve the API specification generated for a Postman collection. Use when you need to fetch OpenAPI/Swagger specs that have been auto-generated from a collection. Returns metadata and an array of generated specifications.
- `get_global_variables` — Tool to get a workspace's global variables. Use when you need to retrieve global variables that are available throughout a workspace for access between collections, requests, scripts, and environments. Note that this endpoint only works with personal or team workspaces, not public workspaces.
- `get_integration_test_relations` — Tool to get integration test relations for a specific API version. This endpoint is deprecated and may not return active data.
- `get_resource_types` — Tool to get all resource types supported by Postman's SCIM API. Use when you need to discover what resource types (e.g., User, Group) are available in the SCIM API and their corresponding endpoints and schemas.
- `get_schema_file_contents` — Tool to get the contents of an API schema file at a specified path. Use when you need to retrieve the actual content of a schema file. Optionally specify a version ID to get file contents from a specific API version.
- `get_schema_files` — Tool to retrieve files in an API schema from Postman. Use when you need to list or view schema files for a specific API and schema ID. Optionally filter by version ID to get files from a particular API version.
- `get_service_provider_configuration` — Tool to get Postman's SCIM API service provider configuration information. Use when you need to discover supported SCIM operations, capabilities, and authentication schemes. This endpoint returns configuration details including support for PATCH, bulk operations, filtering, sorting, and ETag handling.
- `get_source_collections_status` — Tool to check whether there is a change between a forked collection and its parent (source) collection. Use when you need to determine if the source collection has updates that are not yet in the forked collection. This endpoint only works with forked collections; attempting to use it with regular collections will result in an error.
- `get_test_suite_relations` — Tool to get test suite relations for a specific API version. Use when you need to retrieve the test suites associated with an API version. Note: This endpoint is deprecated and only works with legacy v9 APIs. For v10+ APIs, this returns an empty array.
- `get_unclassified_relations` — Tool to get unclassified relations for an API version in Postman. Use when you need to retrieve unclassified relations for a specific API version. This endpoint is for Postman v10 and higher.
- `import_openapi` — Tool to import an OpenAPI specification into Postman as a new collection. Use when you need to convert an OpenAPI 3.0+ specification into a Postman collection within a specific workspace. The imported specification will be automatically converted to a Postman collection with all endpoints, request parameters, and documentation. [write]
- `list_account_invoices` — Tool to get all invoices for a Postman billing account filtered by status. Use when you need to retrieve invoice history for an account. The account ID must first be obtained from the GET /accounts endpoint.
- `merge_a_fork` — Tool to merge a forked collection back into its parent collection. This endpoint is deprecated. Use when you need to merge changes from a forked collection into the parent collection. [write]
- `merge_a_fork2` — Tool to merge a forked environment back into its parent environment. Use when you need to merge changes from a forked environment into the parent. [write]
- `publish_a_mock_server` — Tool to publish a mock server in Postman. Use when you need to make a mock server publicly accessible. Publishing sets the mock server's Access Control configuration to public. [write]
- `pull_source_changes2` — Tool to pull changes from a parent (source) collection into a forked collection. Use when you need to sync a forked collection with its parent.
- `replace_an_environments_data` — Tool to completely replace an environment's data with new variables and values. Use when you need to update an entire environment by replacing all its contents. This operation replaces ALL existing variables with the ones provided in the request. [write]
- `replace_collections_data_asynchronously` — Tool to replace the entire contents of a collection asynchronously. Use when you need to completely replace a collection with new data. IMPORTANT: Include the collection's ID values in item, variable, and other nested objects to preserve them. If you do not include IDs, existing items will be removed and new items will be created. [write]
- `resolve_a_comment_thread` — Tool to resolve a comment thread and any associated replies. Use when you need to mark a comment thread as resolved. On success, this returns an HTTP 204 No Content response. [write]
- `review_a_pull_request` — Tool to update the review status of a pull request by approving, declining, or unapproving it. Use when you need to perform a review action on a Postman pull request.
- `run_a_monitor` — Tool to trigger an immediate run of a monitor and retrieve its execution results. Use when you need to manually execute a monitor outside of its scheduled runs.
- `sync_collection_with_schema` — Tool to sync a collection attached to an API with the API schema. This is an asynchronous endpoint that returns HTTP 202 Accepted. Use when you need to synchronize a collection with changes made to the API schema. The collection must already be attached to the API. Returns a task ID that can be used to check the status of the sync operation. [write]
- `sync_collection_with_spec` — Tool to sync a collection generated from an API specification. This is an asynchronous operation that returns HTTP 202 Accepted. Use when you need to update a collection to match the latest version of its source API specification. The collection must have been generated from a spec. [write]
- `sync_spec_with_collection` — Tool to sync an API specification with a linked collection. This is an asynchronous operation that returns HTTP 202 Accepted with task tracking information. Use when you need to synchronize changes from a generated collection back to its source specification. Prerequisites: the collection must be generated from the spec, and the spec must be single-file. [write]
- `transfer_folders` — Tool to copy or move folders into a collection or folder. Use when you need to reorganize collections by transferring folders between collections or into other folders. [write]
- `transform_collection_to_openapi` — Tool to transform an existing Postman Collection into a stringified OpenAPI 3.0.3 definition. Use when you need to convert a collection to OpenAPI format for API documentation or interoperability with other tools.
- `update_a_folder` — Tool to update a folder in a Postman collection. Use when you need to modify the name or description of an existing folder. For complete properties and information, see the Postman Collection Format documentation. [write]
- `update_a_folders_comment` — Tool to update a comment on a folder. Use when you need to modify the text content of an existing comment on a specific folder in a collection. [write]
- `update_a_mock_server` — Tool to update an existing mock server. Use when you need to change a mock server's name, collection, environment, or privacy settings. The collection UID is required for all updates. [write]
- `update_a_monitor` — Tool to update an existing monitor in Postman. Use when you need to modify monitor properties like name, active status, collection, environment, options, notifications, or distribution settings. [write]
- `update_a_pull_request` — Tool to update an open pull request in Postman. Use when you need to modify the title, description, source, destination, or reviewers of an existing pull request. All fields must be provided in the request. [write]
- `update_a_request` — Tool to update a request in a Postman collection. Use when you need to modify an existing request's name, method, URL, headers, or body following the Postman Collection Format. [write]
- `update_a_requests_comment` — Tool to update a comment on a request. Use when you need to modify the text content of an existing comment on a specific request within a collection. [write]
- `update_a_response` — Tool to update a response in a Postman collection. Use when you need to modify properties of an existing saved response example such as name, status, code, headers, cookies, or body. [write]
- `update_a_responses_comment` — Tool to update a comment on a response. Use when you need to modify the text content of an existing comment on a specific response within a collection. [write]
- `update_a_server_response` — Tool to update a mock server's server response. Use when you need to modify properties of an existing server response such as name, status code, language, body, or headers. At least one property must be included in the update request. [write]
- `update_a_spec_file` — Tool to update an API specification file's content. Use when you need to modify the contents of a specific file within a spec. [write]
- `update_a_specs_properties` — Tool to update an API specification's properties such as its name. Use when you need to modify metadata of an existing spec. [write]
- `update_a_workspace` — Tool to update an existing workspace in Postman. Use when you need to modify the name, type, or description of a workspace. The 'type' field is required for all updates. [write]
- `update_an_api` — Tool to update an existing API in Postman. Use when you need to modify the name, summary, or description of an API. [write]
- `update_an_apis_comment` — Tool to update a comment on an API. Use when you need to modify the text content of an existing comment on a specific API. [write]
- `update_an_environment` — Tool to update specific environment properties using JSON Patch operations (RFC 6902). Use when you need to modify environment name or variables without replacing the entire environment. [write]
- `update_global_variables` — Tool to update and replace a workspace's global variables. Use when you need to set or replace all global variables in a workspace. Note: This endpoint replaces all existing global variables with the provided list. [write]
- `update_part_of_a_collection` — Tool to update specific collection properties like name, description, authentication, variables, or events. Use when you need to partially update a collection without replacing the entire collection structure. Returns the updated collection information after the changes are applied. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Postman state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Postman is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=postman
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Postman homepage: https://www.postman.com
