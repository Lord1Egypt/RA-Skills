# Microsoft Teams access policy

An access policy limits which endpoints Microsoft Teams connections may call through Maton. Microsoft Teams doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/microsoft-teams#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Microsoft Teams: its 139 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create microsoft-teams --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1.0/teams"},
    {"method": "GET", "path": "v1.0/teams/{id}"},
    {"method": "GET", "path": "v1.0/me/joinedTeams"},
    {"method": "GET", "path": "v1.0/me/joinedTeams/**"},
    {"method": "GET", "path": "v1.0/me/teamwork/**"},
    {"method": "GET", "path": "v1.0/users/{id}/joinedTeams"},
    {"method": "GET", "path": "v1.0/users/{id}/joinedTeams/**"},
    {"method": "GET", "path": "v1.0/users/{id}/teamwork/**"},
    {"method": "GET", "path": "v1.0/groups/{id}/team/**"},
    {"method": "GET", "path": "v1.0/teams/{id}/group/**"},
    {"method": "GET", "path": "v1.0/teams/{id}/schedule/**"},
    {"method": "GET", "path": "v1.0/teams/{id}/template"},
    {"method": "GET", "path": "v1.0/teams/{id}/photo/**"},
    {"method": "GET", "path": "v1.0/teams/{id}/operations/**"},
    {"method": "GET", "path": "v1.0/teams/{id}/permissionGrants/**"},
    {"method": "GET", "path": "v1.0/teams/{id}/installedApps/**"},
    {"method": "GET", "path": "v1.0/teams/{id}/installedApps"},
    {"method": "GET", "path": "v1.0/teams/{id}/installedApps/{id}"},
    {"method": "GET", "path": "v1.0/chats/{id}/installedApps"},
    {"method": "GET", "path": "v1.0/chats/{id}/installedApps/{id}"},
    {"method": "GET", "path": "v1.0/appCatalogs/teamsApps/**"},
    {"method": "GET", "path": "v1.0/teams/{id}/members/**"},
    {"method": "GET", "path": "v1.0/teams/{id}/members"},
    {"method": "GET", "path": "v1.0/teams/{id}/members/{id}"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/**"},
    {"method": "GET", "path": "v1.0/teams/{id}/allChannels/**"},
    {"method": "GET", "path": "v1.0/teams/{id}/incomingChannels/**"},
    {"method": "GET", "path": "v1.0/teams/{id}/primaryChannel/**"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/filesFolder"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/sharedWithTeams"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/sharedWithTeams/{id}"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/sharedWithTeams/{id}/allowedMembers"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/messages"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/messages/delta"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/messages/{id}"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/messages/{id}/hostedContents"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/messages/{id}/hostedContents/{id}"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/messages/{id}/hostedContents/{id}/$value"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/messages/{id}/replies"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/messages/{id}/replies/delta"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/messages/{id}/replies/{id}"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/messages/{id}/replies/{id}/hostedContents"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/messages/{id}/replies/{id}/hostedContents/{id}/$value"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/members"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/members/{id}"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/allMembers"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/tabs"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/tabs/{id}"},
    {"method": "GET", "path": "v1.0/teams/{id}/channels/{id}/tabs/{id}/teamsApp"},
    {"method": "GET", "path": "v1.0/chats/{id}/tabs"},
    {"method": "GET", "path": "v1.0/chats/{id}/tabs/{id}"},
    {"method": "GET", "path": "v1.0/teams/{id}/tags/**"},
    {"method": "GET", "path": "v1.0/teams/{id}/tags"},
    {"method": "GET", "path": "v1.0/teams/{id}/tags/{id}"},
    {"method": "GET", "path": "v1.0/teams/{id}/tags/{id}/members"},
    {"method": "GET", "path": "v1.0/teams/{id}/tags/{id}/members/{id}"},
    {"method": "GET", "path": "v1.0/chats"},
    {"method": "GET", "path": "v1.0/chats/{id}/**"},
    {"method": "GET", "path": "v1.0/chats/{id}"},
    {"method": "GET", "path": "v1.0/chats/{id}/pinnedMessages"},
    {"method": "GET", "path": "v1.0/chats/{id}/permissionGrants"},
    {"method": "GET", "path": "v1.0/me/chats"},
    {"method": "GET", "path": "v1.0/me/chats/{id}/**"},
    {"method": "GET", "path": "v1.0/users/{id}/chats"},
    {"method": "GET", "path": "v1.0/users/{id}/chats/{id}/**"},
    {"method": "GET", "path": "v1.0/chats/{id}/messages"},
    {"method": "GET", "path": "v1.0/chats/{id}/messages/delta"},
    {"method": "GET", "path": "v1.0/chats/{id}/messages/{id}"},
    {"method": "GET", "path": "v1.0/chats/{id}/messages/{id}/hostedContents"},
    {"method": "GET", "path": "v1.0/chats/{id}/messages/{id}/hostedContents/{id}"},
    {"method": "GET", "path": "v1.0/chats/{id}/messages/{id}/hostedContents/{id}/$value"},
    {"method": "GET", "path": "v1.0/chats/{id}/members"},
    {"method": "GET", "path": "v1.0/chats/{id}/members/{id}"},
    {"method": "GET", "path": "v1.0/me/onlineMeetings"},
    {"method": "GET", "path": "v1.0/me/onlineMeetings/{id}/**"},
    {"method": "GET", "path": "v1.0/me/onlineMeetings/{id}"},
    {"method": "GET", "path": "v1.0/me/onlineMeetings/{id}/recordings"},
    {"method": "GET", "path": "v1.0/me/onlineMeetings/{id}/recordings/{id}"},
    {"method": "GET", "path": "v1.0/me/onlineMeetings/{id}/recordings/{id}/content"},
    {"method": "GET", "path": "v1.0/me/onlineMeetings/{id}/transcripts"},
    {"method": "GET", "path": "v1.0/me/onlineMeetings/{id}/transcripts/{id}"},
    {"method": "GET", "path": "v1.0/me/onlineMeetings/{id}/transcripts/{id}/content"},
    {"method": "GET", "path": "v1.0/me/onlineMeetings/{id}/transcripts/{id}/metadataContent"},
    {"method": "GET", "path": "v1.0/me/onlineMeetings/{id}/attendanceReports"},
    {"method": "GET", "path": "v1.0/me/onlineMeetings/{id}/attendanceReports/{id}"},
    {"method": "GET", "path": "v1.0/me/onlineMeetings/{id}/attendanceReports/{id}/attendanceRecords"},
    {"method": "GET", "path": "v1.0/me/onlineMeetings/{id}/attendeeReport"},
    {"method": "GET", "path": "v1.0/users/{id}/onlineMeetings"},
    {"method": "GET", "path": "v1.0/users/{id}/onlineMeetings/{id}/**"},
    {"method": "GET", "path": "v1.0/users/{id}/onlineMeetings/{id}"},
    {"method": "GET", "path": "v1.0/users/{id}/onlineMeetings/{id}/recordings"},
    {"method": "GET", "path": "v1.0/users/{id}/onlineMeetings/{id}/recordings/{id}"},
    {"method": "GET", "path": "v1.0/users/{id}/onlineMeetings/{id}/recordings/{id}/content"},
    {"method": "GET", "path": "v1.0/users/{id}/onlineMeetings/{id}/transcripts"},
    {"method": "GET", "path": "v1.0/users/{id}/onlineMeetings/{id}/transcripts/{id}"},
    {"method": "GET", "path": "v1.0/users/{id}/onlineMeetings/{id}/transcripts/{id}/content"},
    {"method": "GET", "path": "v1.0/users/{id}/onlineMeetings/{id}/transcripts/{id}/metadataContent"},
    {"method": "GET", "path": "v1.0/users/{id}/onlineMeetings/{id}/attendanceReports"},
    {"method": "GET", "path": "v1.0/users/{id}/onlineMeetings/{id}/attendanceReports/{id}"},
    {"method": "GET", "path": "v1.0/users/{id}/onlineMeetings/{id}/attendanceReports/{id}/attendanceRecords"},
    {"method": "GET", "path": "v1.0/users/{id}/onlineMeetings/{id}/attendeeReport"},
    {"method": "GET", "path": "v1.0/communications/onlineMeetings/**"},
    {"method": "GET", "path": "v1.0/me/calendar/events"},
    {"method": "GET", "path": "v1.0/me/events"},
    {"method": "GET", "path": "v1.0/me/events/{id}"},
    {"method": "GET", "path": "v1.0/me/calendarView"},
    {"method": "GET", "path": "v1.0/me/calendar/calendarView"},
    {"method": "GET", "path": "v1.0/users/{id}/calendar/events"},
    {"method": "GET", "path": "v1.0/users/{id}/events"},
    {"method": "GET", "path": "v1.0/users/{id}/events/{id}"},
    {"method": "GET", "path": "v1.0/users/{id}/calendarView"},
    {"method": "GET", "path": "v1.0/users/{id}/calendar/calendarView"},
    {"method": "GET", "path": "v1.0/me/presence"},
    {"method": "GET", "path": "v1.0/users/{id}/presence"},
    {"method": "GET", "path": "v1.0/communications/presences"},
    {"method": "GET", "path": "v1.0/communications/presences/{id}"},
    {"method": "POST", "path": "v1.0/communications/getPresencesByUserId"},
    {"method": "GET", "path": "v1.0/me"},
    {"method": "GET", "path": "v1.0/users"},
    {"method": "GET", "path": "v1.0/users/{id}"},
    {"method": "GET", "path": "v1.0/groups"},
    {"method": "GET", "path": "v1.0/groups/{id}"},
    {"method": "GET", "path": "v1.0/groups/{id}/members"},
    {"method": "GET", "path": "v1.0/groups/{id}/owners"},
    {"method": "POST", "path": "v1.0/me/getMemberGroups"},
    {"method": "POST", "path": "v1.0/me/checkMemberGroups"},
    {"method": "POST", "path": "v1.0/users/{id}/getMemberGroups"},
    {"method": "POST", "path": "v1.0/users/{id}/checkMemberGroups"},
    {"method": "POST", "path": "v1.0/groups/{id}/getMemberGroups"},
    {"method": "POST", "path": "v1.0/groups/{id}/checkMemberGroups"},
    {"method": "GET", "path": "v1.0/teamwork"},
    {"method": "GET", "path": "v1.0/teamwork/deletedTeams"},
    {"method": "GET", "path": "v1.0/teamwork/deletedChats/{id}"},
    {"method": "GET", "path": "v1.0/teamsTemplates/**"},
    {"method": "POST", "path": "v1.0/search/query"},
    {"method": "GET", "path": "v1.0/subscriptions"},
    {"method": "GET", "path": "v1.0/subscriptions/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Microsoft Teams endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v1.0/teams | read | teams | List teams in the organization. |
| GET | v1.0/teams/{id} | read | teams | Get a team. |
| GET | v1.0/me/joinedTeams | read | teams | List the teams the signed-in user is a member of. |
| GET | `v1.0/me/joinedTeams/**` | read | teams | Read a joined team of the signed-in user and anything under it (same tree as teams/{id}). |
| GET | `v1.0/me/teamwork/**` | read | teams | Read the Teams data of the signed-in user: associated teams and personally installed apps. |
| GET | v1.0/users/{id}/joinedTeams | read | teams | List the teams a specified user is a member of. |
| GET | `v1.0/users/{id}/joinedTeams/**` | read | teams | Read a joined team of a specified user and anything under it (same tree as teams/{id}). |
| GET | `v1.0/users/{id}/teamwork/**` | read | teams | Read the Teams data of a specified user: associated teams and personally installed apps. |
| GET | `v1.0/groups/{id}/team/**` | read | teams | Read the team of a Microsoft 365 group and anything under it (channels, messages, members, apps). |
| GET | `v1.0/teams/{id}/group/**` | read | teams | Get the Microsoft 365 group behind a team. |
| GET | `v1.0/teams/{id}/schedule/**` | read | teams | Read the Shifts schedule of a team (shifts, time off, requests); schedule writes are not catalogued. |
| GET | v1.0/teams/{id}/template | read | teams | Get the template a team was created from. |
| GET | `v1.0/teams/{id}/photo/**` | read | teams | Read the photo of a team (metadata and $value content). |
| GET | `v1.0/teams/{id}/operations/**` | read | teams | List or get long-running operations of a team. |
| GET | `v1.0/teams/{id}/permissionGrants/**` | read | teams | List resource-specific permission grants of a team. |
| POST | v1.0/teams | write | teams | Create a team. |
| PUT | v1.0/groups/{id}/team | write | teams | Create a team from an existing Microsoft 365 group. |
| PATCH | v1.0/teams/{id} | write | teams | Update the settings of a team. |
| DELETE | v1.0/teams/{id} | write | teams | Delete a team. |
| DELETE | v1.0/groups/{id} | write | teams | Delete the Microsoft 365 group behind a team, which deletes the team. |
| POST | v1.0/teams/{id}/archive | write | teams | Archive a team. |
| POST | v1.0/teams/{id}/unarchive | write | teams | Restore an archived team. |
| POST | v1.0/teams/{id}/clone | write | teams | Clone a team. |
| POST | v1.0/teams/{id}/completeMigration | write | teams | Complete the migration of a team. |
| POST | v1.0/teams/{id}/sendActivityNotification | write | teams | Send an activity feed notification in the scope of a team. |
| PUT | v1.0/teams/{id}/photo/$value | write | teams | Replace the photo of a team. |
| POST | v1.0/me/teamwork/sendActivityNotification | write | teams | Send an activity feed notification to the signed-in user. |
| POST | v1.0/users/{id}/teamwork/sendActivityNotification | write | teams | Send an activity feed notification to a specified user. |
| POST | v1.0/teamwork/sendActivityNotificationToRecipients | write | teams | Send activity feed notifications to multiple users. |
| POST | v1.0/me/teamwork/installedApps | write | apps | Install an app in the personal scope of the signed-in user. |
| DELETE | v1.0/me/teamwork/installedApps/{id} | write | apps | Uninstall an app from the personal scope of the signed-in user. |
| POST | v1.0/me/teamwork/installedApps/{id}/upgrade | write | apps | Upgrade an app installed in the personal scope of the signed-in user. |
| POST | v1.0/users/{id}/teamwork/installedApps | write | apps | Install an app in the personal scope of a specified user. |
| DELETE | v1.0/users/{id}/teamwork/installedApps/{id} | write | apps | Uninstall an app from the personal scope of a specified user. |
| POST | v1.0/users/{id}/teamwork/installedApps/{id}/upgrade | write | apps | Upgrade an app installed in the personal scope of a specified user. |
| GET | `v1.0/teams/{id}/installedApps/**` | read | apps | Read anything under the apps installed in a team. |
| GET | v1.0/teams/{id}/installedApps | read | apps | List apps of a team. |
| GET | v1.0/teams/{id}/installedApps/{id} | read | apps | Get an installed app of a team. |
| POST | v1.0/teams/{id}/installedApps | write | apps | Add an installed app to a team. |
| DELETE | v1.0/teams/{id}/installedApps/{id} | write | apps | Remove an installed app from a team. |
| POST | v1.0/teams/{id}/installedApps/{id}/upgrade | write | apps | Upgrade an app installed in a team. |
| GET | v1.0/chats/{id}/installedApps | read | apps | List apps of a chat. |
| GET | v1.0/chats/{id}/installedApps/{id} | read | apps | Get an installed app of a chat. |
| POST | v1.0/chats/{id}/installedApps | write | apps | Add an installed app to a chat. |
| DELETE | v1.0/chats/{id}/installedApps/{id} | write | apps | Remove an installed app from a chat. |
| POST | v1.0/chats/{id}/installedApps/{id}/upgrade | write | apps | Upgrade an app installed in a chat. |
| GET | `v1.0/appCatalogs/teamsApps/**` | read | apps | Read the organization's Teams app catalog: apps, app definitions and bots. |
| POST | v1.0/appCatalogs/teamsApps | write | apps | Publish an app to the organization's Teams app catalog. |
| POST | v1.0/appCatalogs/teamsApps/{id}/appDefinitions | write | apps | Publish a new version of an app in the Teams app catalog. |
| PATCH | v1.0/appCatalogs/teamsApps/{id}/appDefinitions/{id} | write | apps | Update or approve an app definition in the Teams app catalog. |
| DELETE | v1.0/appCatalogs/teamsApps/{id} | write | apps | Remove an app from the organization's Teams app catalog. |
| GET | `v1.0/teams/{id}/members/**` | read | team members | Read anything under the members of a team. |
| GET | v1.0/teams/{id}/members | read | team members | List members of a team. |
| GET | v1.0/teams/{id}/members/{id} | read | team members | Get a member of a team. |
| POST | v1.0/teams/{id}/members | write | team members | Add a member to a team. |
| PATCH | v1.0/teams/{id}/members/{id} | write | team members | Update a member's role in a team. |
| DELETE | v1.0/teams/{id}/members/{id} | write | team members | Remove a member from a team. |
| POST | v1.0/teams/{id}/members/add | write | team members | Add several members to a team in one request. |
| POST | v1.0/teams/{id}/members/remove | write | team members | Remove several members from a team in one request. |
| GET | `v1.0/teams/{id}/channels/**` | read | channels | Read anything under the channels of a team: channels, messages, replies, members, tabs, files folder, shared teams. |
| GET | `v1.0/teams/{id}/allChannels/**` | read | channels | List or get all channels of a team, including shared channels hosted elsewhere. |
| GET | `v1.0/teams/{id}/incomingChannels/**` | read | channels | List or get channels shared with a team from other teams. |
| GET | `v1.0/teams/{id}/primaryChannel/**` | read | channels | Read the General channel of a team and anything under it (messages, members, tabs, files folder). |
| GET | v1.0/teams/{id}/channels | read | channels | List channels of a team. |
| GET | v1.0/teams/{id}/channels/{id} | read | channels | Get a channel. |
| GET | v1.0/teams/{id}/channels/{id}/filesFolder | read | channels | Get the SharePoint folder that stores the files of a channel. |
| GET | v1.0/teams/{id}/channels/{id}/sharedWithTeams | read | channels | List teams a shared channel is shared with. |
| GET | v1.0/teams/{id}/channels/{id}/sharedWithTeams/{id} | read | channels | Get a team a shared channel is shared with. |
| GET | v1.0/teams/{id}/channels/{id}/sharedWithTeams/{id}/allowedMembers | read | channels | List members of a team who can access a shared channel. |
| POST | v1.0/teams/{id}/channels | write | channels | Create a channel in a team. |
| PATCH | v1.0/teams/{id}/channels/{id} | write | channels | Update a channel. |
| DELETE | v1.0/teams/{id}/channels/{id} | write | channels | Delete a channel. |
| POST | v1.0/teams/{id}/channels/{id}/archive | write | channels | Archive a channel. |
| POST | v1.0/teams/{id}/channels/{id}/unarchive | write | channels | Restore an archived channel. |
| POST | v1.0/teams/{id}/channels/{id}/provisionEmail | write | channels | Provision an email address for a channel. |
| POST | v1.0/teams/{id}/channels/{id}/removeEmail | write | channels | Remove the email address of a channel. |
| POST | v1.0/teams/{id}/channels/{id}/completeMigration | write | channels | Complete the migration of a channel. |
| POST | v1.0/teams/{id}/channels/{id}/startMigration | write | channels | Start migrating messages into a channel. |
| DELETE | v1.0/teams/{id}/channels/{id}/sharedWithTeams/{id} | write | channels | Stop sharing a channel with a team. |
| PATCH | v1.0/teams/{id}/primaryChannel | write | channels | Update the General channel of a team. |
| GET | v1.0/teams/{id}/channels/{id}/messages | read | channel messages | List messages in a channel. |
| GET | v1.0/teams/{id}/channels/{id}/messages/delta | read | channel messages | Track message changes in a channel (delta query). |
| GET | v1.0/teams/{id}/channels/{id}/messages/{id} | read | channel messages | Get a message in a channel. |
| GET | v1.0/teams/{id}/channels/{id}/messages/{id}/hostedContents | read | channel messages | List hosted contents (inline images, code snippets) of a message in a channel. |
| GET | v1.0/teams/{id}/channels/{id}/messages/{id}/hostedContents/{id} | read | channel messages | Get a hosted content of a message in a channel. |
| GET | v1.0/teams/{id}/channels/{id}/messages/{id}/hostedContents/{id}/$value | read | channel messages | Download the bytes of a hosted content of a message in a channel. |
| POST | v1.0/teams/{id}/channels/{id}/messages | write | channel messages | Send a message in a channel. |
| PATCH | v1.0/teams/{id}/channels/{id}/messages/{id} | write | channel messages | Edit a message in a channel. |
| DELETE | v1.0/teams/{id}/channels/{id}/messages/{id} | write | channel messages | Delete a message in a channel. |
| POST | v1.0/teams/{id}/channels/{id}/messages/{id}/softDelete | write | channel messages | Soft-delete a message in a channel. |
| POST | v1.0/teams/{id}/channels/{id}/messages/{id}/undoSoftDelete | write | channel messages | Restore a soft-deleted a message in a channel. |
| POST | v1.0/teams/{id}/channels/{id}/messages/{id}/setReaction | write | channel messages | Add a reaction to a message in a channel. |
| POST | v1.0/teams/{id}/channels/{id}/messages/{id}/unsetReaction | write | channel messages | Remove a reaction from a message in a channel. |
| POST | v1.0/teams/{id}/channels/{id}/messages/replyWithQuote | write | channel messages | Send a message that quotes other messages in a channel. |
| POST | v1.0/teams/{id}/primaryChannel/messages | write | channel messages | Send a message in the General channel of a team. |
| GET | v1.0/teams/{id}/channels/{id}/messages/{id}/replies | read | channel message replies | List replies to a message in a channel. |
| GET | v1.0/teams/{id}/channels/{id}/messages/{id}/replies/delta | read | channel message replies | Track reply changes for a message in a channel (delta query). |
| GET | v1.0/teams/{id}/channels/{id}/messages/{id}/replies/{id} | read | channel message replies | Get a reply to a message in a channel. |
| GET | v1.0/teams/{id}/channels/{id}/messages/{id}/replies/{id}/hostedContents | read | channel message replies | List hosted contents of a reply in a channel. |
| GET | v1.0/teams/{id}/channels/{id}/messages/{id}/replies/{id}/hostedContents/{id}/$value | read | channel message replies | Download the bytes of a hosted content of a reply in a channel. |
| POST | v1.0/teams/{id}/channels/{id}/messages/{id}/replies | write | channel message replies | Reply to a message in a channel. |
| PATCH | v1.0/teams/{id}/channels/{id}/messages/{id}/replies/{id} | write | channel message replies | Edit a reply in a channel. |
| DELETE | v1.0/teams/{id}/channels/{id}/messages/{id}/replies/{id} | write | channel message replies | Delete a reply in a channel. |
| POST | v1.0/teams/{id}/channels/{id}/messages/{id}/replies/{id}/softDelete | write | channel message replies | Soft-delete a reply in a channel. |
| POST | v1.0/teams/{id}/channels/{id}/messages/{id}/replies/{id}/undoSoftDelete | write | channel message replies | Restore a soft-deleted a reply in a channel. |
| POST | v1.0/teams/{id}/channels/{id}/messages/{id}/replies/{id}/setReaction | write | channel message replies | Add a reaction to a reply in a channel. |
| POST | v1.0/teams/{id}/channels/{id}/messages/{id}/replies/{id}/unsetReaction | write | channel message replies | Remove a reaction from a reply in a channel. |
| POST | v1.0/teams/{id}/channels/{id}/messages/{id}/replies/replyWithQuote | write | channel message replies | Reply with quoted messages in a channel. |
| POST | v1.0/teams/{id}/primaryChannel/messages/{id}/replies | write | channel message replies | Reply to a message in the General channel of a team. |
| GET | v1.0/teams/{id}/channels/{id}/members | read | channel members | List members of a channel. |
| GET | v1.0/teams/{id}/channels/{id}/members/{id} | read | channel members | Get a member of a channel. |
| POST | v1.0/teams/{id}/channels/{id}/members | write | channel members | Add a member to a channel. |
| PATCH | v1.0/teams/{id}/channels/{id}/members/{id} | write | channel members | Update a member's role in a channel. |
| DELETE | v1.0/teams/{id}/channels/{id}/members/{id} | write | channel members | Remove a member from a channel. |
| POST | v1.0/teams/{id}/channels/{id}/members/add | write | channel members | Add several members to a channel in one request. |
| POST | v1.0/teams/{id}/channels/{id}/members/remove | write | channel members | Remove several members from a channel in one request. |
| GET | v1.0/teams/{id}/channels/{id}/allMembers | read | channel members | List all members of a channel, including members from shared teams. |
| GET | v1.0/teams/{id}/channels/{id}/tabs | read | tabs | List tabs of a channel. |
| GET | v1.0/teams/{id}/channels/{id}/tabs/{id} | read | tabs | Get a tab of a channel. |
| POST | v1.0/teams/{id}/channels/{id}/tabs | write | tabs | Add a tab to a channel. |
| PATCH | v1.0/teams/{id}/channels/{id}/tabs/{id} | write | tabs | Update a tab of a channel. |
| DELETE | v1.0/teams/{id}/channels/{id}/tabs/{id} | write | tabs | Remove a tab from a channel. |
| GET | v1.0/teams/{id}/channels/{id}/tabs/{id}/teamsApp | read | tabs | Get the app behind a channel tab. |
| GET | v1.0/chats/{id}/tabs | read | tabs | List tabs of a chat. |
| GET | v1.0/chats/{id}/tabs/{id} | read | tabs | Get a tab of a chat. |
| POST | v1.0/chats/{id}/tabs | write | tabs | Add a tab to a chat. |
| PATCH | v1.0/chats/{id}/tabs/{id} | write | tabs | Update a tab of a chat. |
| DELETE | v1.0/chats/{id}/tabs/{id} | write | tabs | Remove a tab from a chat. |
| GET | `v1.0/teams/{id}/tags/**` | read | tags | Read anything under the tags of a team: tags and tag members. |
| GET | v1.0/teams/{id}/tags | read | tags | List tags of a team. |
| GET | v1.0/teams/{id}/tags/{id} | read | tags | Get a tag of a team. |
| POST | v1.0/teams/{id}/tags | write | tags | Add a tag to a team. |
| PATCH | v1.0/teams/{id}/tags/{id} | write | tags | Update a tag of a team. |
| DELETE | v1.0/teams/{id}/tags/{id} | write | tags | Remove a tag from a team. |
| GET | v1.0/teams/{id}/tags/{id}/members | read | tags | List tags of a team tag. |
| GET | v1.0/teams/{id}/tags/{id}/members/{id} | read | tags | Get a tag member of a team tag. |
| POST | v1.0/teams/{id}/tags/{id}/members | write | tags | Add a tag member to a team tag. |
| DELETE | v1.0/teams/{id}/tags/{id}/members/{id} | write | tags | Remove a tag member from a team tag. |
| GET | v1.0/chats | read | chats | List chats. |
| GET | `v1.0/chats/{id}/**` | read | chats | Read a chat and anything under it: messages, members, tabs, installed apps, pinned messages. |
| GET | v1.0/chats/{id} | read | chats | Get a chat. |
| GET | v1.0/chats/{id}/pinnedMessages | read | chats | List pinned messages of a chat. |
| GET | v1.0/chats/{id}/permissionGrants | read | chats | List resource-specific permission grants of a chat. |
| GET | v1.0/me/chats | read | chats | List the chats of the signed-in user. |
| GET | `v1.0/me/chats/{id}/**` | read | chats | Read a chat of the signed-in user and anything under it (messages, members, tabs, apps). |
| GET | v1.0/users/{id}/chats | read | chats | List the chats of a specified user. |
| GET | `v1.0/users/{id}/chats/{id}/**` | read | chats | Read a chat of a specified user and anything under it (messages, members, tabs, apps). |
| POST | v1.0/chats | write | chats | Create a one-on-one or group chat. |
| PATCH | v1.0/chats/{id} | write | chats | Update a chat, such as its topic. |
| DELETE | v1.0/chats/{id} | write | chats | Delete a chat. |
| POST | v1.0/chats/{id}/hideForUser | write | chats | Hide a chat for a user. |
| POST | v1.0/chats/{id}/unhideForUser | write | chats | Unhide a chat for a user. |
| POST | v1.0/chats/{id}/markChatReadForUser | write | chats | Mark a chat as read for a user. |
| POST | v1.0/chats/{id}/markChatUnreadForUser | write | chats | Mark a chat as unread for a user. |
| POST | v1.0/chats/{id}/sendActivityNotification | write | chats | Send an activity feed notification in the scope of a chat. |
| POST | v1.0/chats/{id}/removeAllAccessForUser | write | chats | Remove a user's access to a chat. |
| POST | v1.0/chats/{id}/completeMigration | write | chats | Complete the migration of a chat. |
| POST | v1.0/chats/{id}/startMigration | write | chats | Start migrating messages into a chat. |
| POST | v1.0/chats/{id}/pinnedMessages | write | chats | Pin a message in a chat. |
| DELETE | v1.0/chats/{id}/pinnedMessages/{id} | write | chats | Unpin a message from a chat. |
| GET | v1.0/chats/{id}/messages | read | chat messages | List messages in a chat. |
| GET | v1.0/chats/{id}/messages/delta | read | chat messages | Track message changes in a chat (delta query). |
| GET | v1.0/chats/{id}/messages/{id} | read | chat messages | Get a message in a chat. |
| GET | v1.0/chats/{id}/messages/{id}/hostedContents | read | chat messages | List hosted contents (inline images, code snippets) of a message in a chat. |
| GET | v1.0/chats/{id}/messages/{id}/hostedContents/{id} | read | chat messages | Get a hosted content of a message in a chat. |
| GET | v1.0/chats/{id}/messages/{id}/hostedContents/{id}/$value | read | chat messages | Download the bytes of a hosted content of a message in a chat. |
| POST | v1.0/chats/{id}/messages | write | chat messages | Send a message in a chat. |
| PATCH | v1.0/chats/{id}/messages/{id} | write | chat messages | Edit a message in a chat. |
| DELETE | v1.0/chats/{id}/messages/{id} | write | chat messages | Delete a message in a chat. |
| POST | v1.0/chats/{id}/messages/{id}/softDelete | write | chat messages | Soft-delete a message in a chat. |
| POST | v1.0/chats/{id}/messages/{id}/undoSoftDelete | write | chat messages | Restore a soft-deleted a message in a chat. |
| POST | v1.0/chats/{id}/messages/{id}/setReaction | write | chat messages | Add a reaction to a message in a chat. |
| POST | v1.0/chats/{id}/messages/{id}/unsetReaction | write | chat messages | Remove a reaction from a message in a chat. |
| POST | v1.0/chats/{id}/messages/replyWithQuote | write | chat messages | Send a message that quotes other messages in a chat. |
| POST | v1.0/me/chats/{id}/messages | write | chat messages | Send a message in a chat of the signed-in user. |
| PATCH | v1.0/me/chats/{id}/messages/{id} | write | chat messages | Edit a message in a chat of the signed-in user. |
| POST | v1.0/me/chats/{id}/messages/{id}/softDelete | write | chat messages | Soft-delete a message in a chat of the signed-in user. |
| POST | v1.0/me/chats/{id}/messages/{id}/undoSoftDelete | write | chat messages | Restore a soft-deleted a message in a chat of the signed-in user. |
| POST | v1.0/me/chats/{id}/messages/{id}/setReaction | write | chat messages | Add a reaction to a message in a chat of the signed-in user. |
| POST | v1.0/me/chats/{id}/messages/{id}/unsetReaction | write | chat messages | Remove a reaction from a message in a chat of the signed-in user. |
| POST | v1.0/users/{id}/chats/{id}/messages | write | chat messages | Send a message in a chat of a specified user. |
| PATCH | v1.0/users/{id}/chats/{id}/messages/{id} | write | chat messages | Edit a message in a chat of a specified user. |
| POST | v1.0/users/{id}/chats/{id}/messages/{id}/softDelete | write | chat messages | Soft-delete a message in a chat of a specified user. |
| POST | v1.0/users/{id}/chats/{id}/messages/{id}/undoSoftDelete | write | chat messages | Restore a soft-deleted a message in a chat of a specified user. |
| POST | v1.0/users/{id}/chats/{id}/messages/{id}/setReaction | write | chat messages | Add a reaction to a message in a chat of a specified user. |
| POST | v1.0/users/{id}/chats/{id}/messages/{id}/unsetReaction | write | chat messages | Remove a reaction from a message in a chat of a specified user. |
| GET | v1.0/chats/{id}/members | read | chat members | List members of a chat. |
| GET | v1.0/chats/{id}/members/{id} | read | chat members | Get a member of a chat. |
| POST | v1.0/chats/{id}/members | write | chat members | Add a member to a chat. |
| PATCH | v1.0/chats/{id}/members/{id} | write | chat members | Update a member's role in a chat. |
| DELETE | v1.0/chats/{id}/members/{id} | write | chat members | Remove a member from a chat. |
| POST | v1.0/chats/{id}/members/add | write | chat members | Add several members to a chat in one request. |
| POST | v1.0/chats/{id}/members/remove | write | chat members | Remove several members from a chat in one request. |
| GET | v1.0/me/onlineMeetings | read | online meetings | Find an online meeting of the signed-in user by JoinWebUrl or videoTeleconferenceId filter. |
| GET | `v1.0/me/onlineMeetings/{id}/**` | read | online meetings | Read an online meeting of the signed-in user and anything under it: recordings, transcripts, attendance reports, content. |
| GET | v1.0/me/onlineMeetings/{id} | read | online meetings | Get an online meeting of the signed-in user; also serves getAllRecordings(...) and getAllTranscripts(...). |
| GET | v1.0/me/onlineMeetings/{id}/recordings | read | online meetings | List recordings of an online meeting of the signed-in user. |
| GET | v1.0/me/onlineMeetings/{id}/recordings/{id} | read | online meetings | Get a recording of an online meeting of the signed-in user. |
| GET | v1.0/me/onlineMeetings/{id}/recordings/{id}/content | read | online meetings | Download a recording of an online meeting of the signed-in user. |
| GET | v1.0/me/onlineMeetings/{id}/transcripts | read | online meetings | List transcripts of an online meeting of the signed-in user. |
| GET | v1.0/me/onlineMeetings/{id}/transcripts/{id} | read | online meetings | Get a transcript of an online meeting of the signed-in user. |
| GET | v1.0/me/onlineMeetings/{id}/transcripts/{id}/content | read | online meetings | Download a transcript of an online meeting of the signed-in user. |
| GET | v1.0/me/onlineMeetings/{id}/transcripts/{id}/metadataContent | read | online meetings | Download the time-aligned metadata of a transcript of an online meeting of the signed-in user. |
| GET | v1.0/me/onlineMeetings/{id}/attendanceReports | read | online meetings | List attendance reports of an online meeting of the signed-in user. |
| GET | v1.0/me/onlineMeetings/{id}/attendanceReports/{id} | read | online meetings | Get an attendance report of an online meeting of the signed-in user. |
| GET | v1.0/me/onlineMeetings/{id}/attendanceReports/{id}/attendanceRecords | read | online meetings | List attendance records of an attendance report of the signed-in user. |
| GET | v1.0/me/onlineMeetings/{id}/attendeeReport | read | online meetings | Download the attendee report of a live event of the signed-in user. |
| POST | v1.0/me/onlineMeetings | write | online meetings | Create an online meeting for the signed-in user. |
| POST | v1.0/me/onlineMeetings/createOrGet | write | online meetings | Create an online meeting with an external id for the signed-in user, or return the existing one. |
| PATCH | v1.0/me/onlineMeetings/{id} | write | online meetings | Update an online meeting of the signed-in user. |
| DELETE | v1.0/me/onlineMeetings/{id} | write | online meetings | Delete an online meeting of the signed-in user. |
| POST | v1.0/me/onlineMeetings/{id}/sendVirtualAppointmentSms | write | online meetings | Send an SMS notification about a virtual appointment of the signed-in user. |
| POST | v1.0/me/onlineMeetings/{id}/sendVirtualAppointmentReminderSms | write | online meetings | Send an SMS reminder about a virtual appointment of the signed-in user. |
| GET | v1.0/users/{id}/onlineMeetings | read | online meetings | Find an online meeting of a specified user by JoinWebUrl or videoTeleconferenceId filter. |
| GET | `v1.0/users/{id}/onlineMeetings/{id}/**` | read | online meetings | Read an online meeting of a specified user and anything under it: recordings, transcripts, attendance reports, content. |
| GET | v1.0/users/{id}/onlineMeetings/{id} | read | online meetings | Get an online meeting of a specified user; also serves getAllRecordings(...) and getAllTranscripts(...). |
| GET | v1.0/users/{id}/onlineMeetings/{id}/recordings | read | online meetings | List recordings of an online meeting of a specified user. |
| GET | v1.0/users/{id}/onlineMeetings/{id}/recordings/{id} | read | online meetings | Get a recording of an online meeting of a specified user. |
| GET | v1.0/users/{id}/onlineMeetings/{id}/recordings/{id}/content | read | online meetings | Download a recording of an online meeting of a specified user. |
| GET | v1.0/users/{id}/onlineMeetings/{id}/transcripts | read | online meetings | List transcripts of an online meeting of a specified user. |
| GET | v1.0/users/{id}/onlineMeetings/{id}/transcripts/{id} | read | online meetings | Get a transcript of an online meeting of a specified user. |
| GET | v1.0/users/{id}/onlineMeetings/{id}/transcripts/{id}/content | read | online meetings | Download a transcript of an online meeting of a specified user. |
| GET | v1.0/users/{id}/onlineMeetings/{id}/transcripts/{id}/metadataContent | read | online meetings | Download the time-aligned metadata of a transcript of an online meeting of a specified user. |
| GET | v1.0/users/{id}/onlineMeetings/{id}/attendanceReports | read | online meetings | List attendance reports of an online meeting of a specified user. |
| GET | v1.0/users/{id}/onlineMeetings/{id}/attendanceReports/{id} | read | online meetings | Get an attendance report of an online meeting of a specified user. |
| GET | v1.0/users/{id}/onlineMeetings/{id}/attendanceReports/{id}/attendanceRecords | read | online meetings | List attendance records of an attendance report of a specified user. |
| GET | v1.0/users/{id}/onlineMeetings/{id}/attendeeReport | read | online meetings | Download the attendee report of a live event of a specified user. |
| POST | v1.0/users/{id}/onlineMeetings | write | online meetings | Create an online meeting for a specified user. |
| POST | v1.0/users/{id}/onlineMeetings/createOrGet | write | online meetings | Create an online meeting with an external id for a specified user, or return the existing one. |
| PATCH | v1.0/users/{id}/onlineMeetings/{id} | write | online meetings | Update an online meeting of a specified user. |
| DELETE | v1.0/users/{id}/onlineMeetings/{id} | write | online meetings | Delete an online meeting of a specified user. |
| POST | v1.0/users/{id}/onlineMeetings/{id}/sendVirtualAppointmentSms | write | online meetings | Send an SMS notification about a virtual appointment of a specified user. |
| POST | v1.0/users/{id}/onlineMeetings/{id}/sendVirtualAppointmentReminderSms | write | online meetings | Send an SMS reminder about a virtual appointment of a specified user. |
| GET | `v1.0/communications/onlineMeetings/**` | read | online meetings | Read online meetings through the communications path (application-style access by filter or id). |
| POST | v1.0/communications/onlineMeetings | write | online meetings | Create an online meeting through the communications path. |
| GET | v1.0/me/calendar/events | read | calendar | List events in the default calendar of the signed-in user (Teams meetings appear as events). |
| GET | v1.0/me/events | read | calendar | List calendar events of the signed-in user. |
| GET | v1.0/me/events/{id} | read | calendar | Get a calendar event of the signed-in user. |
| GET | v1.0/me/calendarView | read | calendar | List calendar events of the signed-in user within a time range. |
| GET | v1.0/me/calendar/calendarView | read | calendar | List events in the default calendar of the signed-in user within a time range. |
| POST | v1.0/me/events | write | calendar | Create a calendar event (optionally a Teams meeting) for the signed-in user; invitations are sent to attendees. |
| POST | v1.0/me/calendar/events | write | calendar | Create an event (optionally a Teams meeting) in the default calendar of the signed-in user. |
| PATCH | v1.0/me/events/{id} | write | calendar | Update a calendar event of the signed-in user. |
| DELETE | v1.0/me/events/{id} | write | calendar | Delete a calendar event of the signed-in user. |
| GET | v1.0/users/{id}/calendar/events | read | calendar | List events in the default calendar of a specified user (Teams meetings appear as events). |
| GET | v1.0/users/{id}/events | read | calendar | List calendar events of a specified user. |
| GET | v1.0/users/{id}/events/{id} | read | calendar | Get a calendar event of a specified user. |
| GET | v1.0/users/{id}/calendarView | read | calendar | List calendar events of a specified user within a time range. |
| GET | v1.0/users/{id}/calendar/calendarView | read | calendar | List events in the default calendar of a specified user within a time range. |
| POST | v1.0/users/{id}/events | write | calendar | Create a calendar event (optionally a Teams meeting) for a specified user; invitations are sent to attendees. |
| POST | v1.0/users/{id}/calendar/events | write | calendar | Create an event (optionally a Teams meeting) in the default calendar of a specified user. |
| PATCH | v1.0/users/{id}/events/{id} | write | calendar | Update a calendar event of a specified user. |
| DELETE | v1.0/users/{id}/events/{id} | write | calendar | Delete a calendar event of a specified user. |
| GET | v1.0/me/presence | read | presence | Get the presence (availability and activity) of the signed-in user. |
| POST | v1.0/me/presence/setPresence | write | presence | Set the presence session of the signed-in user. |
| POST | v1.0/me/presence/clearPresence | write | presence | Clear the presence session of the signed-in user. |
| POST | v1.0/me/presence/setUserPreferredPresence | write | presence | Set the preferred presence of the signed-in user. |
| POST | v1.0/me/presence/clearUserPreferredPresence | write | presence | Clear the preferred presence of the signed-in user. |
| POST | v1.0/me/presence/setStatusMessage | write | presence | Set the status message of the signed-in user. |
| POST | v1.0/me/presence/setAutomaticLocation | write | presence | Set the automatic work location of the signed-in user. |
| POST | v1.0/me/presence/setManualLocation | write | presence | Set the manual work location of the signed-in user. |
| POST | v1.0/me/presence/clearAutomaticLocation | write | presence | Clear the automatic work location of the signed-in user. |
| POST | v1.0/me/presence/clearLocation | write | presence | Clear the work location of the signed-in user. |
| GET | v1.0/users/{id}/presence | read | presence | Get the presence (availability and activity) of a specified user. |
| POST | v1.0/users/{id}/presence/setPresence | write | presence | Set the presence session of a specified user. |
| POST | v1.0/users/{id}/presence/clearPresence | write | presence | Clear the presence session of a specified user. |
| POST | v1.0/users/{id}/presence/setUserPreferredPresence | write | presence | Set the preferred presence of a specified user. |
| POST | v1.0/users/{id}/presence/clearUserPreferredPresence | write | presence | Clear the preferred presence of a specified user. |
| POST | v1.0/users/{id}/presence/setStatusMessage | write | presence | Set the status message of a specified user. |
| POST | v1.0/users/{id}/presence/setAutomaticLocation | write | presence | Set the automatic work location of a specified user. |
| POST | v1.0/users/{id}/presence/setManualLocation | write | presence | Set the manual work location of a specified user. |
| POST | v1.0/users/{id}/presence/clearAutomaticLocation | write | presence | Clear the automatic work location of a specified user. |
| POST | v1.0/users/{id}/presence/clearLocation | write | presence | Clear the work location of a specified user. |
| GET | v1.0/communications/presences | read | presence | List presence objects. |
| GET | v1.0/communications/presences/{id} | read | presence | Get the presence of a user by id. |
| POST | v1.0/communications/getPresencesByUserId | read | presence | Get the presence of several users by id; POST only carries the id list. |
| POST | v1.0/communications/presences/{id}/setPresence | write | presence | Change a user's presence (setPresence). |
| POST | v1.0/communications/presences/{id}/clearPresence | write | presence | Change a user's presence (clearPresence). |
| POST | v1.0/communications/presences/{id}/setUserPreferredPresence | write | presence | Change a user's presence (setUserPreferredPresence). |
| POST | v1.0/communications/presences/{id}/clearUserPreferredPresence | write | presence | Change a user's presence (clearUserPreferredPresence). |
| POST | v1.0/communications/presences/{id}/setStatusMessage | write | presence | Change a user's presence (setStatusMessage). |
| GET | v1.0/me | read | directory | Get the profile of the signed-in user. |
| GET | v1.0/users | read | directory | List or search users in the organization. |
| GET | v1.0/users/{id} | read | directory | Get a user by id or userPrincipalName. |
| GET | v1.0/groups | read | directory | List or filter groups, for example the groups that have a team. |
| GET | v1.0/groups/{id} | read | directory | Get a group. |
| GET | v1.0/groups/{id}/members | read | directory | List members of a group. |
| GET | v1.0/groups/{id}/owners | read | directory | List owners of a group. |
| POST | v1.0/me/getMemberGroups | read | directory | Return the ids of all groups the signed-in user is a member of; POST only carries options. |
| POST | v1.0/me/checkMemberGroups | read | directory | Check which of the given groups the signed-in user is a member of; POST only carries the id list. |
| POST | v1.0/users/{id}/getMemberGroups | read | directory | Return the ids of all groups a specified user is a member of; POST only carries options. |
| POST | v1.0/users/{id}/checkMemberGroups | read | directory | Check which of the given groups a specified user is a member of; POST only carries the id list. |
| POST | v1.0/groups/{id}/getMemberGroups | read | directory | Return the ids of all groups a group is a member of; POST only carries options. |
| POST | v1.0/groups/{id}/checkMemberGroups | read | directory | Check which of the given groups a group is a member of; POST only carries the id list. |
| POST | v1.0/groups | write | directory | Create a group. |
| PATCH | v1.0/groups/{id} | write | directory | Update a group. |
| POST | v1.0/groups/{id}/members/$ref | write | directory | Add a member to a group. |
| DELETE | v1.0/groups/{id}/members/{id}/$ref | write | directory | Remove a member from a group. |
| POST | v1.0/groups/{id}/owners/$ref | write | directory | Add an owner to a group. |
| DELETE | v1.0/groups/{id}/owners/{id}/$ref | write | directory | Remove an owner from a group. |
| GET | v1.0/teamwork | read | teamwork | Get tenant-wide Teams settings. |
| GET | v1.0/teamwork/deletedTeams | read | teamwork | List deleted teams. |
| GET | v1.0/teamwork/deletedChats/{id} | read | teamwork | Get a deleted chat. |
| POST | v1.0/teamwork/deletedChats/{id}/undoDelete | write | teamwork | Restore a deleted chat. |
| GET | `v1.0/teamsTemplates/**` | read | teamwork | List or get available team templates. |
| POST | v1.0/search/query | read | search | Run a Microsoft Search query (chat messages and other entity types); POST only carries the query. |
| POST | v1.0/$batch | write | batch | JSON batch of up to 20 Graph requests; can carry writes, so it is not part of read access. |
| GET | v1.0/subscriptions | read | subscriptions | List change-notification (webhook) subscriptions; clientState is not returned. |
| GET | v1.0/subscriptions/{id} | read | subscriptions | Get a change-notification subscription. |
| POST | v1.0/subscriptions | write | subscriptions | Create a webhook subscription that pushes team, channel, chat, message or presence changes to an external URL. |
| PATCH | v1.0/subscriptions/{id} | write | subscriptions | Renew or update a webhook subscription. |
| DELETE | v1.0/subscriptions/{id} | write | subscriptions | Delete a webhook subscription. |
| POST | v1.0/subscriptions/{id}/reauthorize | write | subscriptions | Reauthorize a webhook subscription after a lifecycle notification. |
