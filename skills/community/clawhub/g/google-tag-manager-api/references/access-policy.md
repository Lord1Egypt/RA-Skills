# Google Tag Manager access policy

An access policy limits which endpoints Google Tag Manager connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-tag-manager#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Google Tag Manager: its 38 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create google-tag-manager --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "tagmanager/v2/accounts"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}"},
    {"method": "GET", "path": "tagmanager/v2/accounts/containers:lookup"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/destinations"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/destinations/{id}"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/environments"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/environments/{id}"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/version_headers"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/version_headers:latest"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/versions/{id}"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/versions:live"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/built_in_variables"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/clients"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/clients/{id}"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/folders"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/folders/{id}"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/gtag_config"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/gtag_config/{id}"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/status"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/tags"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/tags/{id}"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/templates"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/templates/{id}"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/transformations"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/transformations/{id}"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/triggers"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/triggers/{id}"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/variables"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/variables/{id}"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/zones"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/zones/{id}"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/containers/{id}:snippet"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/user_permissions"},
    {"method": "GET", "path": "tagmanager/v2/accounts/{id}/user_permissions/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Google Tag Manager endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | tagmanager/v2/accounts | read | accounts | Lists all GTM Accounts that a user has access to. |
| GET | tagmanager/v2/accounts/{id} | read | accounts | Gets a GTM Account. |
| PUT | tagmanager/v2/accounts/{id} | write | accounts | Updates a GTM Account. |
| GET | tagmanager/v2/accounts/containers:lookup | read | containers | Looks up a Container by destination ID or tag ID. |
| GET | tagmanager/v2/accounts/{id}/containers | read | containers | Lists all Containers that belongs to a GTM Account. |
| POST | tagmanager/v2/accounts/{id}/containers | write | containers | Creates a Container. |
| GET | tagmanager/v2/accounts/{id}/containers/{id} | read | containers | Gets a Container. |
| PUT | tagmanager/v2/accounts/{id}/containers/{id} | write | containers | Updates a Container. |
| DELETE | tagmanager/v2/accounts/{id}/containers/{id} | write | containers | Deletes a Container. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/destinations | read | containers | Lists all Destinations linked to a GTM Container. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/destinations/{id} | read | containers | Gets a Destination. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/destinations:link | write | containers | Adds a Destination to this Container and removes it from the Container to which it is currently linked. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/environments | read | containers | Lists all GTM Environments of a GTM Container. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/environments | write | containers | Creates a GTM Environment. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/environments/{id} | read | containers | Gets a GTM Environment. |
| PUT | tagmanager/v2/accounts/{id}/containers/{id}/environments/{id} | write | containers | Updates a GTM Environment. |
| DELETE | tagmanager/v2/accounts/{id}/containers/{id}/environments/{id} | write | containers | Deletes a GTM Environment. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/environments/{id}:reauthorize | write | containers | Re-generates the authorization code for a GTM Environment. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/version_headers | read | containers | Lists all Container Versions of a GTM Container. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/version_headers:latest | read | containers | Gets the latest container version header |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/versions/{id} | read | containers | Gets a Container Version. |
| PUT | tagmanager/v2/accounts/{id}/containers/{id}/versions/{id} | write | containers | Updates a Container Version. |
| DELETE | tagmanager/v2/accounts/{id}/containers/{id}/versions/{id} | write | containers | Deletes a Container Version. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/versions/{id}:publish | write | containers | Publishes a Container Version. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/versions/{id}:set_latest | write | containers | Sets the latest version used for synchronization of workspaces when detecting conflicts and errors. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/versions/{id}:undelete | write | containers | Undeletes a Container Version. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/versions:live | read | containers | Gets the live (i.e. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces | read | containers | Lists all Workspaces that belong to a GTM Container. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces | write | containers | Creates a Workspace. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id} | read | containers | Gets a Workspace. |
| PUT | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id} | write | containers | Updates a Workspace. |
| DELETE | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id} | write | containers | Deletes a Workspace. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/built_in_variables | read | containers | Lists all the enabled Built-In Variables of a GTM Container. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/built_in_variables | write | containers | Creates one or more GTM Built-In Variables. |
| DELETE | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/built_in_variables | write | containers | Deletes one or more GTM Built-In Variables. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/built_in_variables:revert | write | containers | Reverts changes to a GTM Built-In Variables in a GTM Workspace. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/bulk_update | write | containers | Applies multiple entity changes to a workspace in one call. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/clients | read | containers | Lists all GTM Clients of a GTM container workspace. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/clients | write | containers | Creates a GTM Client. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/clients/{id} | read | containers | Gets a GTM Client. |
| PUT | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/clients/{id} | write | containers | Updates a GTM Client. |
| DELETE | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/clients/{id} | write | containers | Deletes a GTM Client. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/clients/{id}:revert | write | containers | Reverts changes to a GTM Client in a GTM Workspace. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/folders | read | containers | Lists all GTM Folders of a Container. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/folders | write | containers | Creates a GTM Folder. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/folders/{id} | read | containers | Gets a GTM Folder. |
| PUT | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/folders/{id} | write | containers | Updates a GTM Folder. |
| DELETE | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/folders/{id} | write | containers | Deletes a GTM Folder. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/folders/{id}:entities | write | containers | List all entities in a GTM Folder. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/folders/{id}:move_entities_to_folder | write | containers | Moves entities to a GTM Folder. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/folders/{id}:revert | write | containers | Reverts changes to a GTM Folder in a GTM Workspace. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/gtag_config | read | containers | Lists all Google tag configs in a Container. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/gtag_config | write | containers | Creates a Google tag config. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/gtag_config/{id} | read | containers | Gets a Google tag config. |
| PUT | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/gtag_config/{id} | write | containers | Updates a Google tag config. |
| DELETE | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/gtag_config/{id} | write | containers | Deletes a Google tag config. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/status | read | containers | Finds conflicting and modified entities in the workspace. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/tags | read | containers | Lists all GTM Tags of a Container. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/tags | write | containers | Creates a GTM Tag. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/tags/{id} | read | containers | Gets a GTM Tag. |
| PUT | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/tags/{id} | write | containers | Updates a GTM Tag. |
| DELETE | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/tags/{id} | write | containers | Deletes a GTM Tag. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/tags/{id}:revert | write | containers | Reverts changes to a GTM Tag in a GTM Workspace. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/templates | read | containers | Lists all GTM Templates of a GTM container workspace. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/templates | write | containers | Creates a GTM Custom Template. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/templates/{id} | read | containers | Gets a GTM Template. |
| PUT | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/templates/{id} | write | containers | Updates a GTM Template. |
| DELETE | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/templates/{id} | write | containers | Deletes a GTM Template. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/templates/{id}:revert | write | containers | Reverts changes to a GTM Template in a GTM Workspace. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/templates:import_from_gallery | write | containers | Imports a GTM Custom Template from Gallery. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/transformations | read | containers | Lists all GTM Transformations of a GTM container workspace. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/transformations | write | containers | Creates a GTM Transformation. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/transformations/{id} | read | containers | Gets a GTM Transformation. |
| PUT | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/transformations/{id} | write | containers | Updates a GTM Transformation. |
| DELETE | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/transformations/{id} | write | containers | Deletes a GTM Transformation. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/transformations/{id}:revert | write | containers | Reverts changes to a GTM Transformation in a GTM Workspace. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/triggers | read | containers | Lists all GTM Triggers of a Container. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/triggers | write | containers | Creates a GTM Trigger. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/triggers/{id} | read | containers | Gets a GTM Trigger. |
| PUT | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/triggers/{id} | write | containers | Updates a GTM Trigger. |
| DELETE | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/triggers/{id} | write | containers | Deletes a GTM Trigger. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/triggers/{id}:revert | write | containers | Reverts changes to a GTM Trigger in a GTM Workspace. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/variables | read | containers | Lists all GTM Variables of a Container. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/variables | write | containers | Creates a GTM Variable. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/variables/{id} | read | containers | Gets a GTM Variable. |
| PUT | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/variables/{id} | write | containers | Updates a GTM Variable. |
| DELETE | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/variables/{id} | write | containers | Deletes a GTM Variable. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/variables/{id}:revert | write | containers | Reverts changes to a GTM Variable in a GTM Workspace. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/zones | read | containers | Lists all GTM Zones of a GTM container workspace. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/zones | write | containers | Creates a GTM Zone. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/zones/{id} | read | containers | Gets a GTM Zone. |
| PUT | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/zones/{id} | write | containers | Updates a GTM Zone. |
| DELETE | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/zones/{id} | write | containers | Deletes a GTM Zone. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}/zones/{id}:revert | write | containers | Reverts changes to a GTM Zone in a GTM Workspace. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}:create_version | write | containers | Creates a Container Version from the entities present in the workspace, deletes the workspace, and sets the base container version to the newly created version. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}:quick_preview | write | containers | Quick previews a workspace by creating a fake container version from all entities in the provided workspace. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}:resolve_conflict | write | containers | Resolves a merge conflict for a workspace entity by updating it to the resolved entity passed in the request. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}/workspaces/{id}:sync | write | containers | Syncs a workspace to the latest container version by updating all unmodified workspace entities and displaying conflicts for modified entities. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}:combine | write | containers | Combines Containers. |
| POST | tagmanager/v2/accounts/{id}/containers/{id}:move_tag_id | write | containers | Move Tag ID out of a Container. |
| GET | tagmanager/v2/accounts/{id}/containers/{id}:snippet | read | containers | Gets the tagging snippet for a Container. |
| GET | tagmanager/v2/accounts/{id}/user_permissions | read | user_permissions | List all users that have access to the account along with Account and Container user access granted to each of them. |
| POST | tagmanager/v2/accounts/{id}/user_permissions | write | user_permissions | Creates a user's Account & Container access. |
| GET | tagmanager/v2/accounts/{id}/user_permissions/{id} | read | user_permissions | Gets a user's Account & Container access. |
| PUT | tagmanager/v2/accounts/{id}/user_permissions/{id} | write | user_permissions | Updates a user's Account & Container access. |
| DELETE | tagmanager/v2/accounts/{id}/user_permissions/{id} | write | user_permissions | Removes a user from the account, revoking access to it and all of its containers. |
