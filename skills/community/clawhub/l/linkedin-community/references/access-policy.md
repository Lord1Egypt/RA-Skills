# LinkedIn Community Management access policy

An access policy limits which endpoints LinkedIn Community Management connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/linkedin-community-management#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for LinkedIn Community Management: its 45 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create linkedin-community-management --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "rest/assets/{id}"},
    {"method": "GET", "path": "rest/documents"},
    {"method": "GET", "path": "rest/documents/{id}"},
    {"method": "GET", "path": "rest/images"},
    {"method": "GET", "path": "rest/images/{id}"},
    {"method": "GET", "path": "rest/eventSubscriptions"},
    {"method": "GET", "path": "rest/eventSubscriptions/{id}"},
    {"method": "GET", "path": "rest/organizationalEntityNotifications"},
    {"method": "GET", "path": "rest/organizationAcls"},
    {"method": "GET", "path": "rest/organizationAuthorizations"},
    {"method": "GET", "path": "rest/organizationAuthorizations/{id}"},
    {"method": "GET", "path": "rest/networkSizes/{id}"},
    {"method": "GET", "path": "rest/organizations"},
    {"method": "GET", "path": "rest/organizations/{id}"},
    {"method": "GET", "path": "rest/organizationsLookup"},
    {"method": "GET", "path": "rest/posts"},
    {"method": "GET", "path": "rest/posts/{id}"},
    {"method": "GET", "path": "rest/me"},
    {"method": "GET", "path": "rest/people"},
    {"method": "GET", "path": "rest/people/{id}"},
    {"method": "GET", "path": "v2/me"},
    {"method": "GET", "path": "v2/people"},
    {"method": "GET", "path": "v2/people/{id}"},
    {"method": "GET", "path": "rest/reactions"},
    {"method": "GET", "path": "rest/reactions/{id}"},
    {"method": "GET", "path": "rest/socialActions"},
    {"method": "GET", "path": "rest/socialActions/{id}"},
    {"method": "GET", "path": "rest/socialActions/{id}/comments"},
    {"method": "GET", "path": "rest/socialActions/{id}/comments/{id}"},
    {"method": "GET", "path": "rest/socialActions/{id}/likes"},
    {"method": "GET", "path": "rest/socialMetadata"},
    {"method": "GET", "path": "rest/socialMetadata/{id}"},
    {"method": "GET", "path": "rest/brandPageStatistics"},
    {"method": "GET", "path": "rest/memberCreatorPostAnalytics"},
    {"method": "GET", "path": "rest/memberCreatorVideoAnalytics"},
    {"method": "GET", "path": "rest/memberFollowersCount"},
    {"method": "GET", "path": "rest/organizationPageStatistics"},
    {"method": "GET", "path": "rest/organizationalEntityFollowerStatistics"},
    {"method": "GET", "path": "rest/organizationalEntityShareStatistics"},
    {"method": "GET", "path": "rest/videoAnalytics"},
    {"method": "GET", "path": "rest/geoTypeahead"},
    {"method": "GET", "path": "rest/peopleTypeahead"},
    {"method": "GET", "path": "rest/vanityUrl"},
    {"method": "GET", "path": "rest/videos"},
    {"method": "GET", "path": "rest/videos/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The LinkedIn Community Management endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| POST | rest/assets | write | assets | Register an asset upload. |
| GET | rest/assets/{id} | read | assets | Get an asset. |
| GET | rest/documents | read | documents | Batch get documents. |
| POST | rest/documents | write | documents | Initialize a document upload. |
| GET | rest/documents/{id} | read | documents | Get a document. |
| GET | rest/images | read | images | Batch get images. |
| POST | rest/images | write | images | Initialize an image upload. |
| GET | rest/images/{id} | read | images | Get an image. |
| POST | rest/images/{id} | write | images | Update an image. |
| GET | rest/eventSubscriptions | read | notifications | List event subscriptions. |
| GET | rest/eventSubscriptions/{id} | read | notifications | Get an event subscription. |
| PUT | rest/eventSubscriptions/{id} | write | notifications | Create or update an event subscription. |
| DELETE | rest/eventSubscriptions/{id} | write | notifications | Delete an event subscription. |
| GET | rest/organizationalEntityNotifications | read | notifications | List social action notifications for an organization. |
| GET | rest/organizationAcls | read | organization access | List organization role assignments. |
| PUT | rest/organizationAcls/{id} | write | organization access | Assign or update an organization role. |
| GET | rest/organizationAuthorizations | read | organization access | List organization authorizations. |
| GET | rest/organizationAuthorizations/{id} | read | organization access | Get an organization authorization. |
| GET | rest/networkSizes/{id} | read | organizations | Get the follower count of an organization. |
| GET | rest/organizations | read | organizations | List organizations, or look one up by vanity name or parent. |
| GET | rest/organizations/{id} | read | organizations | Get an organization. |
| GET | rest/organizationsLookup | read | organizations | Batch look up organizations. |
| GET | rest/posts | read | posts | List posts by author, or batch get posts by URN. |
| POST | rest/posts | write | posts | Create a post, or reshare a post. |
| GET | rest/posts/{id} | read | posts | Get a post. |
| POST | rest/posts/{id} | write | posts | Partially update a post. |
| DELETE | rest/posts/{id} | write | posts | Delete a post. |
| GET | rest/me | read | profile | Get the current member. |
| GET | rest/people | read | profile | Batch get member profiles. |
| GET | rest/people/{id} | read | profile | Get a member profile. |
| GET | v2/me | read | profile | Get the current member (v2). |
| GET | v2/people | read | profile | Batch get member profiles (v2). |
| GET | v2/people/{id} | read | profile | Get a member profile (v2). |
| GET | rest/reactions | read | reactions | List reactions on a post or comment. |
| POST | rest/reactions | write | reactions | Create a reaction. |
| GET | rest/reactions/{id} | read | reactions | Get a reaction. |
| DELETE | rest/reactions/{id} | write | reactions | Delete a reaction. |
| GET | rest/socialActions | read | social actions | Batch get social action summaries. |
| GET | rest/socialActions/{id} | read | social actions | Get the social action summary of a post or comment. |
| GET | rest/socialActions/{id}/comments | read | social actions | List comments on a post or comment. |
| POST | rest/socialActions/{id}/comments | write | social actions | Create a comment or reply. |
| GET | rest/socialActions/{id}/comments/{id} | read | social actions | Get a comment. |
| POST | rest/socialActions/{id}/comments/{id} | write | social actions | Edit a comment. |
| DELETE | rest/socialActions/{id}/comments/{id} | write | social actions | Delete a comment. |
| GET | rest/socialActions/{id}/likes | read | social actions | List likes on a post or comment. |
| POST | rest/socialActions/{id}/likes | write | social actions | Like a post or comment. |
| DELETE | rest/socialActions/{id}/likes/{id} | write | social actions | Remove a like. |
| GET | rest/socialMetadata | read | social metadata | Batch get social metadata. |
| GET | rest/socialMetadata/{id} | read | social metadata | Get social metadata of a post or comment. |
| POST | rest/socialMetadata/{id} | write | social metadata | Update social metadata, such as disabling comments. |
| GET | rest/brandPageStatistics | read | statistics | Get page statistics for a brand page. |
| GET | rest/memberCreatorPostAnalytics | read | statistics | Get post analytics for a member. |
| GET | rest/memberCreatorVideoAnalytics | read | statistics | Get video analytics for a member. |
| GET | rest/memberFollowersCount | read | statistics | Get the follower count of a member. |
| GET | rest/organizationPageStatistics | read | statistics | Get page statistics for an organization. |
| GET | rest/organizationalEntityFollowerStatistics | read | statistics | Get follower statistics for an organization. |
| GET | rest/organizationalEntityShareStatistics | read | statistics | Get share statistics for an organization or its posts. |
| GET | rest/videoAnalytics | read | statistics | Get video analytics. |
| GET | rest/geoTypeahead | read | typeahead | Search geo locations for post targeting. |
| GET | rest/peopleTypeahead | read | typeahead | Search members to mention. |
| GET | rest/vanityUrl | read | typeahead | Resolve a vanity URL to a member or organization. |
| GET | rest/videos | read | videos | Batch get videos. |
| POST | rest/videos | write | videos | Initialize or finalize a video upload. |
| GET | rest/videos/{id} | read | videos | Get a video. |
| POST | rest/videos/{id} | write | videos | Update a video. |
