# OneDrive access policy

An access policy limits which endpoints OneDrive connections may call through Maton. OneDrive doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/one-drive#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for OneDrive: its 105 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create one-drive --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1.0/me"},
    {"method": "GET", "path": "v1.0/me/drives"},
    {"method": "GET", "path": "v1.0/drives/{id}"},
    {"method": "GET", "path": "v1.0/users/{id}/drive"},
    {"method": "GET", "path": "v1.0/users/{id}/drives"},
    {"method": "GET", "path": "v1.0/groups/{id}/drive"},
    {"method": "GET", "path": "v1.0/groups/{id}/drives"},
    {"method": "GET", "path": "v1.0/sites/{id}/drive"},
    {"method": "GET", "path": "v1.0/sites/{id}/drives"},
    {"method": "GET", "path": "v1.0/me/drive"},
    {"method": "GET", "path": "v1.0/me/drive/root"},
    {"method": "GET", "path": "v1.0/me/drive/root/children"},
    {"method": "GET", "path": "v1.0/me/drive/root:/**"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/children"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/listItem"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/retentionLabel"},
    {"method": "GET", "path": "v1.0/me/drive/recent"},
    {"method": "GET", "path": "v1.0/me/drive/sharedWithMe"},
    {"method": "GET", "path": "v1.0/me/drive/following"},
    {"method": "GET", "path": "v1.0/me/drive/bundles"},
    {"method": "GET", "path": "v1.0/me/drive/bundles/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/special"},
    {"method": "GET", "path": "v1.0/me/drive/special/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/special/{id}/children"},
    {"method": "GET", "path": "v1.0/me/drive/list"},
    {"method": "GET", "path": "v1.0/drives/{id}/root"},
    {"method": "GET", "path": "v1.0/drives/{id}/root/children"},
    {"method": "GET", "path": "v1.0/drives/{id}/root:/**"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/children"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/listItem"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/retentionLabel"},
    {"method": "GET", "path": "v1.0/drives/{id}/recent"},
    {"method": "GET", "path": "v1.0/drives/{id}/sharedWithMe"},
    {"method": "GET", "path": "v1.0/drives/{id}/following"},
    {"method": "GET", "path": "v1.0/drives/{id}/bundles"},
    {"method": "GET", "path": "v1.0/drives/{id}/bundles/{id}"},
    {"method": "GET", "path": "v1.0/drives/{id}/special"},
    {"method": "GET", "path": "v1.0/drives/{id}/special/{id}"},
    {"method": "GET", "path": "v1.0/drives/{id}/special/{id}/children"},
    {"method": "GET", "path": "v1.0/drives/{id}/list"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/content"},
    {"method": "POST", "path": "v1.0/me/drive/items/{id}/preview"},
    {"method": "POST", "path": "v1.0/me/drive/root:/{id}/preview"},
    {"method": "POST", "path": "v1.0/me/drive/root:/{id}/{id}/preview"},
    {"method": "POST", "path": "v1.0/me/drive/root:/{id}/{id}/{id}/preview"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/content"},
    {"method": "POST", "path": "v1.0/drives/{id}/items/{id}/preview"},
    {"method": "POST", "path": "v1.0/drives/{id}/root:/{id}/preview"},
    {"method": "POST", "path": "v1.0/drives/{id}/root:/{id}/{id}/preview"},
    {"method": "POST", "path": "v1.0/drives/{id}/root:/{id}/{id}/{id}/preview"},
    {"method": "POST", "path": "v1.0/me/drive/items/{id}/{id}/preview"},
    {"method": "POST", "path": "v1.0/drives/{id}/items/{id}/{id}/preview"},
    {"method": "POST", "path": "v1.0/me/drives/{id}/items/{id}/preview"},
    {"method": "POST", "path": "v1.0/users/{id}/drive/items/{id}/preview"},
    {"method": "POST", "path": "v1.0/users/{id}/drives/{id}/items/{id}/preview"},
    {"method": "POST", "path": "v1.0/groups/{id}/drive/items/{id}/preview"},
    {"method": "POST", "path": "v1.0/groups/{id}/drives/{id}/items/{id}/preview"},
    {"method": "POST", "path": "v1.0/sites/{id}/drive/items/{id}/preview"},
    {"method": "POST", "path": "v1.0/sites/{id}/drives/{id}/items/{id}/preview"},
    {"method": "GET", "path": "v1.0/me/drive/root/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/root/delta"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/delta"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/{id}"},
    {"method": "GET", "path": "v1.0/drives/{id}/root/{id}"},
    {"method": "GET", "path": "v1.0/drives/{id}/root/delta"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/delta"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/{id}"},
    {"method": "POST", "path": "v1.0/search/query"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/thumbnails"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/thumbnails/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/thumbnails/{id}/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/thumbnails/{id}/{id}/content"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/thumbnails"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/thumbnails/{id}"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/thumbnails/{id}/{id}"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/thumbnails/{id}/{id}/content"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/versions"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/versions/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/versions/{id}/content"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/versions"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/versions/{id}"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/versions/{id}/content"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/permissions"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/permissions/{id}"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/permissions"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/permissions/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/analytics"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/analytics/allTime"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/analytics/lastSevenDays"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/analytics"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/analytics/allTime"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/analytics/lastSevenDays"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/subscriptions"},
    {"method": "GET", "path": "v1.0/drives/{id}/items/{id}/subscriptions"},
    {"method": "GET", "path": "v1.0/me/drive/**"},
    {"method": "GET", "path": "v1.0/me/drives/**"},
    {"method": "GET", "path": "v1.0/drives/**"},
    {"method": "GET", "path": "v1.0/users/{id}/drive/**"},
    {"method": "GET", "path": "v1.0/users/{id}/drives/**"},
    {"method": "GET", "path": "v1.0/groups/{id}/drive/**"},
    {"method": "GET", "path": "v1.0/groups/{id}/drives/**"},
    {"method": "GET", "path": "v1.0/sites/{id}/drive/**"},
    {"method": "GET", "path": "v1.0/sites/{id}/drives/**"}
  ],
  "deny": []
}
```

## Endpoints

The OneDrive endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v1.0/me | read | user | Get the signed-in user's profile. |
| GET | v1.0/me/drives | read | drives | List the drives available to the signed-in user. |
| GET | v1.0/drives/{id} | read | drives | Get a drive by ID. |
| GET | v1.0/users/{id}/drive | read | drives | Get a user's OneDrive. |
| GET | v1.0/users/{id}/drives | read | drives | List a user's drives. |
| GET | v1.0/groups/{id}/drive | read | drives | Get a group's document library. |
| GET | v1.0/groups/{id}/drives | read | drives | List a group's document libraries. |
| GET | v1.0/sites/{id}/drive | read | drives | Get a site's default document library. |
| GET | v1.0/sites/{id}/drives | read | drives | List a site's document libraries. |
| GET | v1.0/me/drive | read | drives | Get the signed-in user's drive. |
| GET | v1.0/me/drive/root | read | items | Get the root folder of the signed-in user's drive. |
| GET | v1.0/me/drive/root/children | read | items | List the items in the root folder of the signed-in user's drive. |
| GET | `v1.0/me/drive/root:/**` | read | items | Path-addressed reads in the signed-in user's drive: root:/path, root:/path:/children, :/content, :/versions, :/workbook/... (any GET). |
| GET | v1.0/me/drive/items/{id} | read | items | Get a drive item by ID. |
| GET | v1.0/me/drive/items/{id}/children | read | items | List the children of a folder. |
| GET | v1.0/me/drive/items/{id}/listItem | read | items | Get the SharePoint list item behind a drive item. |
| GET | v1.0/me/drive/items/{id}/retentionLabel | read | items | Get the retention label on a drive item. |
| GET | v1.0/me/drive/recent | read | items | List recently used files. |
| GET | v1.0/me/drive/sharedWithMe | read | items | List files shared with the user. |
| GET | v1.0/me/drive/following | read | items | List followed drive items. |
| GET | v1.0/me/drive/bundles | read | items | List bundles (albums) in the drive. |
| GET | v1.0/me/drive/bundles/{id} | read | items | Get a bundle. |
| GET | v1.0/me/drive/special | read | items | List special folders. |
| GET | v1.0/me/drive/special/{id} | read | items | Get a special folder (documents, photos, music, approot, ...). |
| GET | v1.0/me/drive/special/{id}/children | read | items | List the items in a special folder. |
| GET | v1.0/me/drive/list | read | items | Get the SharePoint list that backs the drive. |
| POST | v1.0/me/drive/root/children | write | items | Create a folder or item in the root folder. |
| POST | v1.0/me/drive/items/{id}/children | write | items | Create a folder or item inside a folder. |
| PATCH | v1.0/me/drive/items/{id} | write | items | Update a drive item: rename, move, change metadata. |
| DELETE | v1.0/me/drive/items/{id} | write | items | Delete a drive item (moves it to the recycle bin). |
| POST | v1.0/me/drive/items/{id}/copy | write | items | Copy a drive item to another location. |
| POST | v1.0/me/drive/items/{id}/restore | write | items | Restore a deleted drive item. |
| POST | v1.0/me/drive/items/{id}/permanentDelete | write | items | Permanently delete a drive item. |
| POST | v1.0/me/drive/items/{id}/follow | write | items | Follow a drive item. |
| POST | v1.0/me/drive/items/{id}/unfollow | write | items | Stop following a drive item. |
| POST | v1.0/me/drive/items/{id}/checkout | write | items | Check out a file so others cannot edit it. |
| POST | v1.0/me/drive/items/{id}/checkin | write | items | Check in a checked-out file. |
| POST | v1.0/me/drive/items/{id}/discardCheckout | write | items | Discard the checkout of a file. |
| POST | v1.0/me/drive/items/{id}/assignSensitivityLabel | write | items | Assign a sensitivity label to a file (metered API). |
| POST | v1.0/me/drive/items/{id}/extractSensitivityLabels | write | items | Extract sensitivity labels and update the item's label metadata. |
| PATCH | v1.0/me/drive/items/{id}/retentionLabel | write | items | Set or lock the retention label on a drive item. |
| DELETE | v1.0/me/drive/items/{id}/retentionLabel | write | items | Remove the retention label from a drive item. |
| POST | v1.0/me/drive/bundles | write | items | Create a bundle (album). |
| GET | v1.0/drives/{id}/root | read | items | Get the root folder of a drive addressed by ID. |
| GET | v1.0/drives/{id}/root/children | read | items | List the items in the root folder of a drive addressed by ID. |
| GET | `v1.0/drives/{id}/root:/**` | read | items | Path-addressed reads in a drive addressed by ID: root:/path, root:/path:/children, :/content, :/versions, :/workbook/... (any GET). |
| GET | v1.0/drives/{id}/items/{id} | read | items | Get a drive item by ID. |
| GET | v1.0/drives/{id}/items/{id}/children | read | items | List the children of a folder. |
| GET | v1.0/drives/{id}/items/{id}/listItem | read | items | Get the SharePoint list item behind a drive item. |
| GET | v1.0/drives/{id}/items/{id}/retentionLabel | read | items | Get the retention label on a drive item. |
| GET | v1.0/drives/{id}/recent | read | items | List recently used files. |
| GET | v1.0/drives/{id}/sharedWithMe | read | items | List files shared with the user. |
| GET | v1.0/drives/{id}/following | read | items | List followed drive items. |
| GET | v1.0/drives/{id}/bundles | read | items | List bundles (albums) in the drive. |
| GET | v1.0/drives/{id}/bundles/{id} | read | items | Get a bundle. |
| GET | v1.0/drives/{id}/special | read | items | List special folders. |
| GET | v1.0/drives/{id}/special/{id} | read | items | Get a special folder (documents, photos, music, approot, ...). |
| GET | v1.0/drives/{id}/special/{id}/children | read | items | List the items in a special folder. |
| GET | v1.0/drives/{id}/list | read | items | Get the SharePoint list that backs the drive. |
| POST | v1.0/drives/{id}/root/children | write | items | Create a folder or item in the root folder. |
| POST | v1.0/drives/{id}/items/{id}/children | write | items | Create a folder or item inside a folder. |
| PATCH | v1.0/drives/{id}/items/{id} | write | items | Update a drive item: rename, move, change metadata. |
| DELETE | v1.0/drives/{id}/items/{id} | write | items | Delete a drive item (moves it to the recycle bin). |
| POST | v1.0/drives/{id}/items/{id}/copy | write | items | Copy a drive item to another location. |
| POST | v1.0/drives/{id}/items/{id}/restore | write | items | Restore a deleted drive item. |
| POST | v1.0/drives/{id}/items/{id}/permanentDelete | write | items | Permanently delete a drive item. |
| POST | v1.0/drives/{id}/items/{id}/follow | write | items | Follow a drive item. |
| POST | v1.0/drives/{id}/items/{id}/unfollow | write | items | Stop following a drive item. |
| POST | v1.0/drives/{id}/items/{id}/checkout | write | items | Check out a file so others cannot edit it. |
| POST | v1.0/drives/{id}/items/{id}/checkin | write | items | Check in a checked-out file. |
| POST | v1.0/drives/{id}/items/{id}/discardCheckout | write | items | Discard the checkout of a file. |
| POST | v1.0/drives/{id}/items/{id}/assignSensitivityLabel | write | items | Assign a sensitivity label to a file (metered API). |
| POST | v1.0/drives/{id}/items/{id}/extractSensitivityLabels | write | items | Extract sensitivity labels and update the item's label metadata. |
| PATCH | v1.0/drives/{id}/items/{id}/retentionLabel | write | items | Set or lock the retention label on a drive item. |
| DELETE | v1.0/drives/{id}/items/{id}/retentionLabel | write | items | Remove the retention label from a drive item. |
| POST | v1.0/drives/{id}/bundles | write | items | Create a bundle (album). |
| GET | v1.0/me/drive/items/{id}/content | read | content | Download the contents of a file (also ?format=pdf conversion). |
| POST | v1.0/me/drive/items/{id}/preview | read | content | Get a short-lived embeddable preview URL for a file; nothing is stored or shared. |
| POST | v1.0/me/drive/root:/{id}/preview | read | content | Preview a file addressed by path in the root folder (root:/file:/preview). |
| POST | v1.0/me/drive/root:/{id}/{id}/preview | read | content | Preview a file addressed by path one folder deep. |
| POST | v1.0/me/drive/root:/{id}/{id}/{id}/preview | read | content | Preview a file addressed by path two folders deep. |
| PUT | v1.0/me/drive/items/{id}/content | write | content | Replace the contents of an existing file (simple upload). |
| PUT | v1.0/me/drive/items/{id}/{id}/content | write | content | Upload a new file by parent ID and name (items/{parent-id}:/{filename}:/content). |
| PUT | `v1.0/me/drive/root:/**` | write | content | Upload or replace a file addressed by path (root:/path:/content). |
| POST | v1.0/me/drive/items/{id}/createUploadSession | write | content | Create a resumable upload session for an existing file. |
| POST | v1.0/me/drive/items/{id}/{id}/createUploadSession | write | content | Create a resumable upload session for a new file by parent ID and name. |
| GET | v1.0/drives/{id}/items/{id}/content | read | content | Download the contents of a file (also ?format=pdf conversion). |
| POST | v1.0/drives/{id}/items/{id}/preview | read | content | Get a short-lived embeddable preview URL for a file; nothing is stored or shared. |
| POST | v1.0/drives/{id}/root:/{id}/preview | read | content | Preview a file addressed by path in the root folder (root:/file:/preview). |
| POST | v1.0/drives/{id}/root:/{id}/{id}/preview | read | content | Preview a file addressed by path one folder deep. |
| POST | v1.0/drives/{id}/root:/{id}/{id}/{id}/preview | read | content | Preview a file addressed by path two folders deep. |
| PUT | v1.0/drives/{id}/items/{id}/content | write | content | Replace the contents of an existing file (simple upload). |
| PUT | v1.0/drives/{id}/items/{id}/{id}/content | write | content | Upload a new file by parent ID and name (items/{parent-id}:/{filename}:/content). |
| PUT | `v1.0/drives/{id}/root:/**` | write | content | Upload or replace a file addressed by path (root:/path:/content). |
| POST | v1.0/drives/{id}/items/{id}/createUploadSession | write | content | Create a resumable upload session for an existing file. |
| POST | v1.0/drives/{id}/items/{id}/{id}/createUploadSession | write | content | Create a resumable upload session for a new file by parent ID and name. |
| POST | v1.0/me/drive/items/{id}/{id}/preview | read | content | Preview a file addressed by parent ID and name (items/{parent-id}:/{filename}:/preview). |
| POST | v1.0/drives/{id}/items/{id}/{id}/preview | read | content | Preview a file addressed by parent ID and name (items/{parent-id}:/{filename}:/preview). |
| POST | v1.0/me/drives/{id}/items/{id}/preview | read | content | Get a short-lived preview URL for a file under me/drives/{id}. |
| POST | v1.0/users/{id}/drive/items/{id}/preview | read | content | Get a short-lived preview URL for a file under users/{id}/drive. |
| POST | v1.0/users/{id}/drives/{id}/items/{id}/preview | read | content | Get a short-lived preview URL for a file under users/{id}/drives/{id}. |
| POST | v1.0/groups/{id}/drive/items/{id}/preview | read | content | Get a short-lived preview URL for a file under groups/{id}/drive. |
| POST | v1.0/groups/{id}/drives/{id}/items/{id}/preview | read | content | Get a short-lived preview URL for a file under groups/{id}/drives/{id}. |
| POST | v1.0/sites/{id}/drive/items/{id}/preview | read | content | Get a short-lived preview URL for a file under sites/{id}/drive. |
| POST | v1.0/sites/{id}/drives/{id}/items/{id}/preview | read | content | Get a short-lived preview URL for a file under sites/{id}/drives/{id}. |
| GET | v1.0/me/drive/root/{id} | read | search | Search the drive or track changes with a function segment: root/search(q='text'), root/delta(token='...'). |
| GET | v1.0/me/drive/root/delta | read | search | Track changes in the drive (delta). |
| GET | v1.0/me/drive/items/{id}/delta | read | search | Track changes under a folder (delta). |
| GET | v1.0/me/drive/items/{id}/{id} | read | search | Function segment on an item: search(q='text'), delta(token='...'), getActivitiesByInterval(...). |
| GET | v1.0/drives/{id}/root/{id} | read | search | Search the drive or track changes with a function segment: root/search(q='text'), root/delta(token='...'). |
| GET | v1.0/drives/{id}/root/delta | read | search | Track changes in the drive (delta). |
| GET | v1.0/drives/{id}/items/{id}/delta | read | search | Track changes under a folder (delta). |
| GET | v1.0/drives/{id}/items/{id}/{id} | read | search | Function segment on an item: search(q='text'), delta(token='...'), getActivitiesByInterval(...). |
| POST | v1.0/search/query | read | search | Microsoft Search query across files, sites, lists and list items (POST only carries the query). |
| GET | v1.0/me/drive/items/{id}/thumbnails | read | thumbnails | List the thumbnail sets of a drive item. |
| GET | v1.0/me/drive/items/{id}/thumbnails/{id} | read | thumbnails | Get a thumbnail set. |
| GET | v1.0/me/drive/items/{id}/thumbnails/{id}/{id} | read | thumbnails | Get one thumbnail size (small, medium, large). |
| GET | v1.0/me/drive/items/{id}/thumbnails/{id}/{id}/content | read | thumbnails | Download a thumbnail image. |
| GET | v1.0/drives/{id}/items/{id}/thumbnails | read | thumbnails | List the thumbnail sets of a drive item. |
| GET | v1.0/drives/{id}/items/{id}/thumbnails/{id} | read | thumbnails | Get a thumbnail set. |
| GET | v1.0/drives/{id}/items/{id}/thumbnails/{id}/{id} | read | thumbnails | Get one thumbnail size (small, medium, large). |
| GET | v1.0/drives/{id}/items/{id}/thumbnails/{id}/{id}/content | read | thumbnails | Download a thumbnail image. |
| GET | v1.0/me/drive/items/{id}/versions | read | versions | List the versions of a file. |
| GET | v1.0/me/drive/items/{id}/versions/{id} | read | versions | Get one version of a file. |
| GET | v1.0/me/drive/items/{id}/versions/{id}/content | read | versions | Download the contents of an earlier version. |
| POST | v1.0/me/drive/items/{id}/versions/{id}/restoreVersion | write | versions | Restore an earlier version as the current one. |
| DELETE | v1.0/me/drive/items/{id}/versions/{id} | write | versions | Delete a version of a file. |
| GET | v1.0/drives/{id}/items/{id}/versions | read | versions | List the versions of a file. |
| GET | v1.0/drives/{id}/items/{id}/versions/{id} | read | versions | Get one version of a file. |
| GET | v1.0/drives/{id}/items/{id}/versions/{id}/content | read | versions | Download the contents of an earlier version. |
| POST | v1.0/drives/{id}/items/{id}/versions/{id}/restoreVersion | write | versions | Restore an earlier version as the current one. |
| DELETE | v1.0/drives/{id}/items/{id}/versions/{id} | write | versions | Delete a version of a file. |
| GET | v1.0/me/drive/items/{id}/permissions | read | permissions | List who a drive item is shared with, including existing sharing links. |
| GET | v1.0/me/drive/items/{id}/permissions/{id} | read | permissions | Get one sharing permission. |
| POST | v1.0/me/drive/items/{id}/createLink | write | permissions | Create a sharing link for a drive item. |
| POST | v1.0/me/drive/items/{id}/invite | write | permissions | Share a drive item with people and optionally email them. |
| POST | v1.0/me/drive/items/{id}/permissions | write | permissions | Add a permission to a drive item. |
| PATCH | v1.0/me/drive/items/{id}/permissions/{id} | write | permissions | Change the roles of a sharing permission. |
| DELETE | v1.0/me/drive/items/{id}/permissions/{id} | write | permissions | Remove a sharing permission. |
| POST | v1.0/me/drive/items/{id}/permissions/{id}/grant | write | permissions | Grant users access to an existing sharing link. |
| POST | v1.0/me/drive/items/{id}/permissions/{id}/revokeGrants | write | permissions | Revoke users' access to a sharing link. |
| POST | v1.0/me/drive/items/{id}/validatePermission | write | permissions | Validate a password-protected sharing permission (unverified side effects). |
| GET | v1.0/drives/{id}/items/{id}/permissions | read | permissions | List who a drive item is shared with, including existing sharing links. |
| GET | v1.0/drives/{id}/items/{id}/permissions/{id} | read | permissions | Get one sharing permission. |
| POST | v1.0/drives/{id}/items/{id}/createLink | write | permissions | Create a sharing link for a drive item. |
| POST | v1.0/drives/{id}/items/{id}/invite | write | permissions | Share a drive item with people and optionally email them. |
| POST | v1.0/drives/{id}/items/{id}/permissions | write | permissions | Add a permission to a drive item. |
| PATCH | v1.0/drives/{id}/items/{id}/permissions/{id} | write | permissions | Change the roles of a sharing permission. |
| DELETE | v1.0/drives/{id}/items/{id}/permissions/{id} | write | permissions | Remove a sharing permission. |
| POST | v1.0/drives/{id}/items/{id}/permissions/{id}/grant | write | permissions | Grant users access to an existing sharing link. |
| POST | v1.0/drives/{id}/items/{id}/permissions/{id}/revokeGrants | write | permissions | Revoke users' access to a sharing link. |
| POST | v1.0/drives/{id}/items/{id}/validatePermission | write | permissions | Validate a password-protected sharing permission (unverified side effects). |
| GET | v1.0/me/drive/items/{id}/analytics | read | analytics | Get view/activity analytics for a drive item. |
| GET | v1.0/me/drive/items/{id}/analytics/allTime | read | analytics | Get all-time activity statistics for a drive item. |
| GET | v1.0/me/drive/items/{id}/analytics/lastSevenDays | read | analytics | Get the last seven days of activity statistics. |
| GET | v1.0/drives/{id}/items/{id}/analytics | read | analytics | Get view/activity analytics for a drive item. |
| GET | v1.0/drives/{id}/items/{id}/analytics/allTime | read | analytics | Get all-time activity statistics for a drive item. |
| GET | v1.0/drives/{id}/items/{id}/analytics/lastSevenDays | read | analytics | Get the last seven days of activity statistics. |
| GET | v1.0/me/drive/items/{id}/subscriptions | read | subscriptions | List webhook subscriptions on a drive item. |
| POST | v1.0/me/drive/items/{id}/subscriptions | write | subscriptions | Create a webhook subscription on a drive item. |
| GET | v1.0/drives/{id}/items/{id}/subscriptions | read | subscriptions | List webhook subscriptions on a drive item. |
| POST | v1.0/drives/{id}/items/{id}/subscriptions | write | subscriptions | Create a webhook subscription on a drive item. |
| POST | v1.0/subscriptions | write | subscriptions | Create a change-notification webhook subscription. |
| PATCH | v1.0/subscriptions/{id} | write | subscriptions | Renew or update a webhook subscription. |
| DELETE | v1.0/subscriptions/{id} | write | subscriptions | Delete a webhook subscription. |
| POST | v1.0/subscriptions/{id}/reauthorize | write | subscriptions | Reauthorize a webhook subscription. |
| GET | `v1.0/me/drive/**` | read | drive trees | Any GET under the signed-in user's drive, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/me/drive/**` | write | drive trees | Any other POST under the signed-in user's drive, including root:/path: addressed forms. |
| PUT | `v1.0/me/drive/**` | write | drive trees | Any other PUT under the signed-in user's drive, including root:/path: addressed forms. |
| PATCH | `v1.0/me/drive/**` | write | drive trees | Any other PATCH under the signed-in user's drive, including root:/path: addressed forms. |
| DELETE | `v1.0/me/drive/**` | write | drive trees | Any other DELETE under the signed-in user's drive, including root:/path: addressed forms. |
| GET | `v1.0/me/drives/**` | read | drive trees | Any GET under the signed-in user's drives, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/me/drives/**` | write | drive trees | Any other POST under the signed-in user's drives, including root:/path: addressed forms. |
| PUT | `v1.0/me/drives/**` | write | drive trees | Any other PUT under the signed-in user's drives, including root:/path: addressed forms. |
| PATCH | `v1.0/me/drives/**` | write | drive trees | Any other PATCH under the signed-in user's drives, including root:/path: addressed forms. |
| DELETE | `v1.0/me/drives/**` | write | drive trees | Any other DELETE under the signed-in user's drives, including root:/path: addressed forms. |
| GET | `v1.0/drives/**` | read | drive trees | Any GET under drives addressed by ID, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/drives/**` | write | drive trees | Any other POST under drives addressed by ID, including root:/path: addressed forms. |
| PUT | `v1.0/drives/**` | write | drive trees | Any other PUT under drives addressed by ID, including root:/path: addressed forms. |
| PATCH | `v1.0/drives/**` | write | drive trees | Any other PATCH under drives addressed by ID, including root:/path: addressed forms. |
| DELETE | `v1.0/drives/**` | write | drive trees | Any other DELETE under drives addressed by ID, including root:/path: addressed forms. |
| GET | `v1.0/users/{id}/drive/**` | read | drive trees | Any GET under a user's drive, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/users/{id}/drive/**` | write | drive trees | Any other POST under a user's drive, including root:/path: addressed forms. |
| PUT | `v1.0/users/{id}/drive/**` | write | drive trees | Any other PUT under a user's drive, including root:/path: addressed forms. |
| PATCH | `v1.0/users/{id}/drive/**` | write | drive trees | Any other PATCH under a user's drive, including root:/path: addressed forms. |
| DELETE | `v1.0/users/{id}/drive/**` | write | drive trees | Any other DELETE under a user's drive, including root:/path: addressed forms. |
| GET | `v1.0/users/{id}/drives/**` | read | drive trees | Any GET under a user's drives, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/users/{id}/drives/**` | write | drive trees | Any other POST under a user's drives, including root:/path: addressed forms. |
| PUT | `v1.0/users/{id}/drives/**` | write | drive trees | Any other PUT under a user's drives, including root:/path: addressed forms. |
| PATCH | `v1.0/users/{id}/drives/**` | write | drive trees | Any other PATCH under a user's drives, including root:/path: addressed forms. |
| DELETE | `v1.0/users/{id}/drives/**` | write | drive trees | Any other DELETE under a user's drives, including root:/path: addressed forms. |
| GET | `v1.0/groups/{id}/drive/**` | read | drive trees | Any GET under a group's drive, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/groups/{id}/drive/**` | write | drive trees | Any other POST under a group's drive, including root:/path: addressed forms. |
| PUT | `v1.0/groups/{id}/drive/**` | write | drive trees | Any other PUT under a group's drive, including root:/path: addressed forms. |
| PATCH | `v1.0/groups/{id}/drive/**` | write | drive trees | Any other PATCH under a group's drive, including root:/path: addressed forms. |
| DELETE | `v1.0/groups/{id}/drive/**` | write | drive trees | Any other DELETE under a group's drive, including root:/path: addressed forms. |
| GET | `v1.0/groups/{id}/drives/**` | read | drive trees | Any GET under a group's drives, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/groups/{id}/drives/**` | write | drive trees | Any other POST under a group's drives, including root:/path: addressed forms. |
| PUT | `v1.0/groups/{id}/drives/**` | write | drive trees | Any other PUT under a group's drives, including root:/path: addressed forms. |
| PATCH | `v1.0/groups/{id}/drives/**` | write | drive trees | Any other PATCH under a group's drives, including root:/path: addressed forms. |
| DELETE | `v1.0/groups/{id}/drives/**` | write | drive trees | Any other DELETE under a group's drives, including root:/path: addressed forms. |
| GET | `v1.0/sites/{id}/drive/**` | read | drive trees | Any GET under a site's default document library, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/sites/{id}/drive/**` | write | drive trees | Any other POST under a site's default document library, including root:/path: addressed forms. |
| PUT | `v1.0/sites/{id}/drive/**` | write | drive trees | Any other PUT under a site's default document library, including root:/path: addressed forms. |
| PATCH | `v1.0/sites/{id}/drive/**` | write | drive trees | Any other PATCH under a site's default document library, including root:/path: addressed forms. |
| DELETE | `v1.0/sites/{id}/drive/**` | write | drive trees | Any other DELETE under a site's default document library, including root:/path: addressed forms. |
| GET | `v1.0/sites/{id}/drives/**` | read | drive trees | Any GET under a site's document libraries, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/sites/{id}/drives/**` | write | drive trees | Any other POST under a site's document libraries, including root:/path: addressed forms. |
| PUT | `v1.0/sites/{id}/drives/**` | write | drive trees | Any other PUT under a site's document libraries, including root:/path: addressed forms. |
| PATCH | `v1.0/sites/{id}/drives/**` | write | drive trees | Any other PATCH under a site's document libraries, including root:/path: addressed forms. |
| DELETE | `v1.0/sites/{id}/drives/**` | write | drive trees | Any other DELETE under a site's document libraries, including root:/path: addressed forms. |
| GET | `v1.0/shares/**` | write | shares | Open a sharing link or share ID. Kept out of read: a Prefer: redeemSharingLink header makes this GET grant the caller durable access. |
| POST | v1.0/shares/{id}/permission/grant | write | shares | Grant users access to a sharing link. |
| DELETE | v1.0/shares/{id}/permission | write | shares | Delete the permission behind a sharing link. |
| POST | `v1.0/shares/**` | write | shares | Any other POST under a share. |
| PUT | `v1.0/shares/**` | write | shares | Any PUT under a share, e.g. uploading into a shared folder. |
| PATCH | `v1.0/shares/**` | write | shares | Any PATCH under a share. |
| DELETE | `v1.0/shares/**` | write | shares | Any other DELETE under a share. |
| POST | v1.0/$batch | write | batch | JSON batch of up to 20 Graph requests; can carry writes. |
