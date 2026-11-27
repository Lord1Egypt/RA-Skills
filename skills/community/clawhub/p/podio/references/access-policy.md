# Podio access policy

An access policy limits which endpoints Podio connections may call through Maton. Podio doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/podio#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Podio: its 226 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create podio --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "action/{id}"},
    {"method": "GET", "path": "app_store/category"},
    {"method": "GET", "path": "app_store/org"},
    {"method": "GET", "path": "app_store/{id}/author/{id}"},
    {"method": "GET", "path": "app_store/{id}/category/{id}"},
    {"method": "GET", "path": "app_store/{id}/own"},
    {"method": "GET", "path": "app_store/{id}/recommended/{id}"},
    {"method": "GET", "path": "app_store/{id}/top"},
    {"method": "GET", "path": "app_store/{id}/v2"},
    {"method": "GET", "path": "app_store/{id}/{id}"},
    {"method": "GET", "path": "app"},
    {"method": "GET", "path": "app/features"},
    {"method": "GET", "path": "app/icon/search"},
    {"method": "GET", "path": "app/org/{id}/top"},
    {"method": "GET", "path": "app/space/{id}"},
    {"method": "GET", "path": "app/top"},
    {"method": "GET", "path": "app/{id}/dependencies"},
    {"method": "GET", "path": "app/{id}/field/{id}"},
    {"method": "GET", "path": "app/{id}/inverse_dependencies"},
    {"method": "GET", "path": "space/{id}/dependencies"},
    {"method": "GET", "path": "batch"},
    {"method": "GET", "path": "batch/{id}"},
    {"method": "GET", "path": "batch/{id}/{id}/{id}/running"},
    {"method": "GET", "path": "calendar"},
    {"method": "GET", "path": "calendar/app/{id}"},
    {"method": "POST", "path": "calendar/app/{id}/filter"},
    {"method": "GET", "path": "calendar/app/{id}/ics/{id}/{id}"},
    {"method": "GET", "path": "calendar/export"},
    {"method": "GET", "path": "calendar/export/linked_account/{id}"},
    {"method": "GET", "path": "calendar/export/linked_account/{id}/{id}/{id}"},
    {"method": "GET", "path": "calendar/export/{id}/{id}"},
    {"method": "GET", "path": "calendar/ics/{id}/{id}"},
    {"method": "GET", "path": "calendar/item/{id}/field/{id}/ics"},
    {"method": "GET", "path": "calendar/linked_account/{id}"},
    {"method": "GET", "path": "calendar/personal/summary"},
    {"method": "GET", "path": "calendar/space/{id}"},
    {"method": "GET", "path": "calendar/space/{id}/ics/{id}/{id}"},
    {"method": "GET", "path": "calendar/space/{id}/summary"},
    {"method": "GET", "path": "calendar/summary"},
    {"method": "GET", "path": "calendar/task/{id}/ics"},
    {"method": "GET", "path": "comment/{id}"},
    {"method": "GET", "path": "comment/{id}/revision"},
    {"method": "GET", "path": "comment/{id}/{id}"},
    {"method": "GET", "path": "contact"},
    {"method": "GET", "path": "contact/app/{id}"},
    {"method": "GET", "path": "contact/linked_account/{id}"},
    {"method": "GET", "path": "contact/org/{id}"},
    {"method": "GET", "path": "contact/skill"},
    {"method": "GET", "path": "contact/space/{id}"},
    {"method": "GET", "path": "contact/space/{id}/totals/space"},
    {"method": "GET", "path": "contact/totals"},
    {"method": "GET", "path": "contact/totals/v3"},
    {"method": "GET", "path": "contact/user/{id}"},
    {"method": "GET", "path": "contact/user/{id}/{id}"},
    {"method": "GET", "path": "contact/{id}/v2"},
    {"method": "GET", "path": "contact/{id}/vcard"},
    {"method": "GET", "path": "conversation"},
    {"method": "GET", "path": "conversation/direct/{id}"},
    {"method": "GET", "path": "conversation/event/{id}"},
    {"method": "GET", "path": "conversation/search"},
    {"method": "GET", "path": "conversation/{id}"},
    {"method": "GET", "path": "conversation/{id}/count"},
    {"method": "GET", "path": "conversation/{id}/event"},
    {"method": "GET", "path": "conversation/{id}/{id}"},
    {"method": "GET", "path": "email/app/{id}"},
    {"method": "GET", "path": "email/group"},
    {"method": "GET", "path": "file"},
    {"method": "GET", "path": "file/app/{id}"},
    {"method": "GET", "path": "file/linked_account/{id}"},
    {"method": "GET", "path": "file/space/{id}"},
    {"method": "GET", "path": "file/space/{id}/latest"},
    {"method": "GET", "path": "file/{id}"},
    {"method": "GET", "path": "flow/{id}"},
    {"method": "GET", "path": "flow/{id}/context"},
    {"method": "GET", "path": "flow/{id}/{id}"},
    {"method": "POST", "path": "flow/{id}/{id}/attributes"},
    {"method": "POST", "path": "flow/{id}/{id}/effect/attributes"},
    {"method": "GET", "path": "form/app/{id}"},
    {"method": "GET", "path": "form/{id}"},
    {"method": "GET", "path": "grant/org/{id}/own"},
    {"method": "GET", "path": "grant/space/{id}/user/{id}"},
    {"method": "GET", "path": "grant/{id}/{id}"},
    {"method": "GET", "path": "grant/{id}/{id}/count"},
    {"method": "GET", "path": "grant/{id}/{id}/own"},
    {"method": "GET", "path": "hook/{id}/{id}"},
    {"method": "GET", "path": "importer/{id}/info"},
    {"method": "POST", "path": "importer/{id}/preview/{id}"},
    {"method": "GET", "path": "integration/{id}/field"},
    {"method": "GET", "path": "app/{id}/item/{id}"},
    {"method": "POST", "path": "item/app/{id}/calculate"},
    {"method": "GET", "path": "item/app/{id}/count"},
    {"method": "GET", "path": "item/app/{id}/external_id/{id}"},
    {"method": "POST", "path": "item/app/{id}/filter"},
    {"method": "POST", "path": "item/app/{id}/filter/{id}"},
    {"method": "GET", "path": "item/app/{id}/values"},
    {"method": "GET", "path": "item/app/{id}/xlsx"},
    {"method": "GET", "path": "item/field/{id}/find"},
    {"method": "GET", "path": "item/field/{id}/range"},
    {"method": "GET", "path": "item/field/{id}/top"},
    {"method": "GET", "path": "item/{id}"},
    {"method": "GET", "path": "item/{id}/clone"},
    {"method": "GET", "path": "item/{id}/field/{id}/recalc/status"},
    {"method": "GET", "path": "item/{id}/reference"},
    {"method": "GET", "path": "item/{id}/reference/field/{id}"},
    {"method": "GET", "path": "item/{id}/reference/{id}/preview"},
    {"method": "GET", "path": "item/{id}/revision"},
    {"method": "GET", "path": "item/{id}/revision/{id}"},
    {"method": "GET", "path": "item/{id}/revision/{id}/{id}"},
    {"method": "GET", "path": "item/{id}/value"},
    {"method": "GET", "path": "item/{id}/value/v2"},
    {"method": "GET", "path": "item/{id}/value/{id}"},
    {"method": "GET", "path": "item/{id}/value/{id}/v2"},
    {"method": "GET", "path": "item/{id}/badge/{id}"},
    {"method": "GET", "path": "layout/{id}/{id}"},
    {"method": "GET", "path": "layout/{id}/{id}/default"},
    {"method": "GET", "path": "linked_account"},
    {"method": "GET", "path": "notification"},
    {"method": "GET", "path": "notification/inbox/new/count"},
    {"method": "GET", "path": "notification/settings"},
    {"method": "GET", "path": "notification/{id}"},
    {"method": "GET", "path": "oauth/scope"},
    {"method": "GET", "path": "org"},
    {"method": "GET", "path": "org/admin-orgs/{id}"},
    {"method": "GET", "path": "org/shared/{id}"},
    {"method": "GET", "path": "org/url"},
    {"method": "GET", "path": "org/{id}"},
    {"method": "GET", "path": "org/{id}/admin"},
    {"method": "GET", "path": "org/{id}/all_spaces"},
    {"method": "GET", "path": "org/{id}/appstore"},
    {"method": "GET", "path": "org/{id}/member"},
    {"method": "GET", "path": "org/{id}/member/search"},
    {"method": "GET", "path": "org/{id}/member/{id}"},
    {"method": "GET", "path": "org/{id}/member/{id}/space_member"},
    {"method": "GET", "path": "org/{id}/report/login"},
    {"method": "GET", "path": "org/{id}/space"},
    {"method": "GET", "path": "org/{id}/space/url/{id}"},
    {"method": "GET", "path": "question/{id}"},
    {"method": "GET", "path": "rating/{id}/{id}"},
    {"method": "GET", "path": "rating/{id}/{id}/like_count"},
    {"method": "GET", "path": "rating/{id}/{id}/liked_by"},
    {"method": "GET", "path": "rating/{id}/{id}/{id}"},
    {"method": "GET", "path": "rating/{id}/{id}/{id}/self"},
    {"method": "GET", "path": "rating/{id}/{id}/{id}/{id}"},
    {"method": "GET", "path": "recurrence/{id}/{id}"},
    {"method": "GET", "path": "reference/resolve"},
    {"method": "POST", "path": "reference/search"},
    {"method": "GET", "path": "reference/{id}/{id}"},
    {"method": "GET", "path": "reference/{id}/{id}/accessible_by"},
    {"method": "GET", "path": "reference/{id}/{id}/accessible_by/count"},
    {"method": "GET", "path": "reminder/{id}/{id}"},
    {"method": "POST", "path": "search"},
    {"method": "POST", "path": "search/app/{id}"},
    {"method": "GET", "path": "search/app/{id}/space/{id}"},
    {"method": "GET", "path": "search/app/{id}/v2"},
    {"method": "POST", "path": "search/org/{id}"},
    {"method": "GET", "path": "search/org/{id}/v2"},
    {"method": "POST", "path": "search/space/{id}"},
    {"method": "GET", "path": "search/space/{id}/v2"},
    {"method": "GET", "path": "search/v2"},
    {"method": "GET", "path": "space/{id}/member"},
    {"method": "GET", "path": "space/{id}/member/total"},
    {"method": "GET", "path": "space/{id}/member/v2"},
    {"method": "GET", "path": "space/{id}/member/{id}"},
    {"method": "GET", "path": "space/{id}/member/{id}/v2"},
    {"method": "GET", "path": "space/org/{id}"},
    {"method": "GET", "path": "space/org/{id}/available"},
    {"method": "GET", "path": "space/org/{id}/url/{id}"},
    {"method": "GET", "path": "space/top"},
    {"method": "GET", "path": "space/url"},
    {"method": "GET", "path": "space/{id}"},
    {"method": "GET", "path": "space/{id}/available"},
    {"method": "GET", "path": "status/{id}"},
    {"method": "GET", "path": "stream"},
    {"method": "GET", "path": "stream/app/{id}"},
    {"method": "POST", "path": "stream/app/{id}/filter"},
    {"method": "GET", "path": "stream/app/{id}/v3"},
    {"method": "GET", "path": "stream/org/{id}"},
    {"method": "GET", "path": "stream/org/{id}/v3"},
    {"method": "GET", "path": "stream/space/{id}"},
    {"method": "GET", "path": "stream/space/{id}/v3"},
    {"method": "GET", "path": "stream/user/{id}"},
    {"method": "GET", "path": "stream/user/{id}/v3"},
    {"method": "GET", "path": "stream/v3"},
    {"method": "GET", "path": "stream/{id}/{id}"},
    {"method": "GET", "path": "stream/{id}/{id}/activity_group"},
    {"method": "GET", "path": "stream/{id}/{id}/activity_group/{id}/{id}"},
    {"method": "GET", "path": "stream/{id}/{id}/group/{id}"},
    {"method": "GET", "path": "stream/{id}/{id}/v3"},
    {"method": "GET", "path": "subscription/inactive"},
    {"method": "GET", "path": "subscription/{id}"},
    {"method": "GET", "path": "subscription/{id}/{id}"},
    {"method": "GET", "path": "tag/app/{id}"},
    {"method": "GET", "path": "tag/app/{id}/search"},
    {"method": "GET", "path": "tag/app/{id}/search/full"},
    {"method": "GET", "path": "tag/app/{id}/top"},
    {"method": "GET", "path": "tag/org/{id}"},
    {"method": "GET", "path": "tag/org/{id}/search"},
    {"method": "GET", "path": "tag/space/{id}"},
    {"method": "GET", "path": "tag/space/{id}/search"},
    {"method": "GET", "path": "task"},
    {"method": "GET", "path": "task/label"},
    {"method": "GET", "path": "task/org/{id}/summary"},
    {"method": "GET", "path": "task/personal/summary"},
    {"method": "GET", "path": "task/space/{id}/summary"},
    {"method": "GET", "path": "task/summary"},
    {"method": "GET", "path": "task/total"},
    {"method": "GET", "path": "task/total/{id}"},
    {"method": "GET", "path": "task/{id}"},
    {"method": "GET", "path": "task/{id}/{id}"},
    {"method": "GET", "path": "task/{id}/{id}/count"},
    {"method": "GET", "path": "task/{id}/{id}/summary"},
    {"method": "GET", "path": "user"},
    {"method": "GET", "path": "user/profile"},
    {"method": "GET", "path": "user/profile/{id}"},
    {"method": "GET", "path": "user/property/{id}"},
    {"method": "GET", "path": "user/setting/{id}"},
    {"method": "GET", "path": "user/setting/{id}/{id}"},
    {"method": "GET", "path": "view/app/{id}"},
    {"method": "GET", "path": "view/app/{id}/{id}"},
    {"method": "GET", "path": "voting/app/{id}/voting"},
    {"method": "GET", "path": "voting/item/{id}/result"},
    {"method": "GET", "path": "voting/item/{id}/voting/{id}/result"},
    {"method": "GET", "path": "voting/item/{id}/voting/{id}/user"},
    {"method": "GET", "path": "voting/{id}"},
    {"method": "GET", "path": "widget/{id}"},
    {"method": "GET", "path": "widget/{id}/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Podio endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | action/{id} | read | actions | Returns the action with the given id. |
| POST | app_store | write | app market | Shares the app or pack in the app market. |
| GET | app_store/category | read | app market | Returns the categories available in the system. |
| GET | app_store/org | read | app market | Returns all the orgs, that the user is member of, and that has shared private apps. |
| PUT | app_store/{id} | write | app market | Updates the share with changes to abstract, description, etc. |
| DELETE | app_store/{id} | write | app market | Unshares the given app from the app market. |
| GET | app_store/{id}/author/{id} | read | app market | Returns all the apps in the app market created by the given user in the given language. |
| GET | app_store/{id}/category/{id} | read | app market | Returns the apps in the app market in the given category and language. |
| POST | app_store/{id}/install | write | app market | Installs the share with the given id on the space. |
| GET | app_store/{id}/own | read | app market | Returns all the apps that the active user has shared. |
| GET | app_store/{id}/recommended/{id} | read | app market | Returns the recommended apps in the app market for the given "area". |
| GET | app_store/{id}/top | read | app market | Returns the top apps in the app market in the given language. |
| GET | app_store/{id}/v2 | read | app market | Returns the shared app from the app market with the given id. |
| GET | app_store/{id}/{id} | read | app market | Returns the shares of the given object. |
| GET | app | read | apps | Returns all the apps for the active user. |
| POST | app | write | apps | Creates a new app on a space. |
| GET | app/features | read | apps | Returns the features that the given apps and optionally space includes. |
| GET | app/icon/search | read | apps | Search for app icon suggestions. |
| GET | app/org/{id}/space/{id}/{id} | write | apps | Get an app by org, space and app label. Kept out of read: same response as get app, with the app auth token. |
| GET | app/org/{id}/top | read | apps | Returns the top apps for the user inside the given organization. |
| GET | app/space/{id} | read | apps | Returns all the apps on the space that are visible. |
| PUT | app/space/{id}/order | write | apps | Updates the order of the apps on the space. |
| GET | app/space/{id}/{id} | write | apps | Get an app on a space by URL label. Kept out of read: full app object, which can carry the app auth token. |
| GET | app/top | read | apps | Returns the top apps for the active user. |
| GET | app/{id} | write | apps | Get an app definition. Kept out of read: the response includes the app auth token and inbound mailbox. |
| PUT | app/{id} | write | apps | Updates an app. |
| DELETE | app/{id} | write | apps | Deletes the app with the given id. |
| POST | app/{id}/activate | write | apps | Activates a deactivated app. |
| POST | app/{id}/deactivate | write | apps | Deactivates the app with the given id. |
| GET | app/{id}/dependencies | read | apps | Returns the apps that the given app depends on. |
| PUT | app/{id}/description | write | apps | Updates the app with a new description. |
| POST | app/{id}/field | write | apps | Adds a new field to an app. |
| GET | app/{id}/field/{id} | read | apps | Returns a single field from an app. |
| PUT | app/{id}/field/{id} | write | apps | Updates the configuration of an app field. |
| DELETE | app/{id}/field/{id} | write | apps | Deletes a field on an app. |
| POST | app/{id}/install | write | apps | Installs the app with the given id on the space. |
| GET | app/{id}/inverse_dependencies | read | apps | Returns the apps that depend on the given app_id. |
| PUT | app/{id}/usage | write | apps | Updates the usage instructions for the app. |
| PUT | app/{id}/v2 | write | apps | Updates an app. |
| GET | space/{id}/dependencies | read | apps | Returns all the active apps on the space along with their dependencies. |
| GET | batch | read | batch | Returns the batches created by the user. |
| GET | batch/{id} | read | batch | Returns the batch with the given id. |
| GET | batch/{id}/{id}/{id}/running | read | batch | Returns the currently running batches on the given reference. |
| GET | calendar | read | calendar | Returns all items that the user have access to and all tasks that are assigned to the user. |
| GET | calendar/app/{id} | read | calendar | Returns the items and tasks that are related to the given app. |
| POST | calendar/app/{id}/filter | read | calendar | Return the calendar of an app filtered with item filters. |
| GET | calendar/app/{id}/ics/{id}/{id} | read | calendar | Get an app calendar as iCal; the caller must already hold the calendar code used in the path. |
| PUT | calendar/event/{id} | write | calendar | Update the calendar event with the given UID with a new start and end time. |
| GET | calendar/export | read | calendar | Returns the exports configured for the global calendar. |
| GET | calendar/export/linked_account/{id} | read | calendar | Get the global calendar export configured for a linked account. |
| GET | calendar/export/linked_account/{id}/{id}/{id} | read | calendar | Returns the current export for the current linked account and ref. |
| GET | calendar/export/{id}/{id} | read | calendar | Returns the calendar exports for the given reference. |
| GET | calendar/ics/{id}/{id} | read | calendar | Get the global calendar as iCal; the caller must already hold the calendar code used in the path. |
| GET | calendar/item/{id}/field/{id}/ics | read | calendar | Returns the calendar for the given date field of the given item in the iCal format. |
| GET | calendar/linked_account/{id} | read | calendar | Returns the events in the primary calendar of the linked account in the given interval. |
| PUT | calendar/linked_account/{id}/event/{id}/duration | write | calendar | Change duration of external event linked_account_id uid - identifier of the event. |
| POST | calendar/linked_account/{id}/event/{id}/move | write | calendar | Move event in external calendar linked by linked_account linked_account uid - identifier of the event. |
| GET | calendar/personal/summary | read | calendar | Returns the calendar summary for personal tasks and personal spaces and sub-orgs. |
| GET | calendar/space/{id} | read | calendar | Returns all items and tasks that the user have access to in the given space. |
| GET | calendar/space/{id}/ics/{id}/{id} | read | calendar | Get a space calendar as iCal; the caller must already hold the calendar code used in the path. |
| GET | calendar/space/{id}/summary | read | calendar | Returns the calendar summary for the given space for the active user. |
| GET | calendar/summary | read | calendar | Returns the calendar summary for the active user. |
| GET | calendar/task/{id}/ics | read | calendar | Returns the calendar for the given task in the iCal format. |
| GET | comment/{id} | read | comments | Returns the contents of a comment. |
| PUT | comment/{id} | write | comments | Updates an already created comment. |
| DELETE | comment/{id} | write | comments | Deletes a comment made by a user. |
| GET | comment/{id}/revision | read | comments | Returns all the revisions on the given comment, including the current revision. |
| GET | comment/{id}/{id} | read | comments | Used to retrieve the comments that have been made on an object of the given type and with the given id. |
| POST | comment/{id}/{id} | write | comments | Adds a new comment to the object of the given type and id, f.ex. |
| GET | contact | read | contacts | Used to get a list of contacts for the user. |
| GET | contact/app/{id} | read | contacts | Returns all the space contacts referenced by the given app. |
| GET | contact/linked_account/{id} | read | contacts | Loads the contacts from the given linked account. |
| POST | contact/linked_account/{id} | write | contacts | Load one contact from a linked external account by external id; treated as write as it may import the contact. |
| GET | contact/org/{id} | read | contacts | Returns all the profiles of the users contacts on the given organization. |
| GET | contact/skill | read | contacts | Returns the skills of related contacts, ordered by most frequently used. |
| GET | contact/space/{id} | read | contacts | Returns all the profiles of the users contacts on the given space. |
| POST | contact/space/{id} | write | contacts | Creates a new space contact for use by everyone on the space. |
| GET | contact/space/{id}/totals/space | read | contacts | Returns the total number of contacts on the space. |
| GET | contact/totals | read | contacts | Returns the total number of contacts for the active user. |
| GET | contact/totals/v3 | read | contacts | Returns the total number of contacts for the active user. |
| GET | contact/user/{id} | read | contacts | Returns the contact with the given user id. |
| GET | contact/user/{id}/{id} | read | contacts | Returns the value of a contact with the specific field. |
| PUT | contact/{id} | write | contacts | Updates the contact with the given profile id. |
| DELETE | contact/{id} | write | contacts | Deletes the contact(s) with the given id(s). |
| GET | contact/{id}/v2 | read | contacts | Returns all the contact details about the contact(s) with the given profile id(s). |
| GET | contact/{id}/vcard | read | contacts | Returns the vCard for the given contact. |
| PUT | contact/{id}/{id} | write | contacts | Updates the given field on the given contact. |
| DELETE | friend/{id} | write | contacts | Remove from friend(s) the user(s) with the given user id(s). |
| GET | conversation | read | conversations | Returns all the users conversations ordered by time of the last event. |
| POST | conversation | write | conversations | Creates a new conversation with a list of users. |
| GET | conversation/direct/{id} | read | conversations | Returns the existing direct conversation with the user. |
| GET | conversation/event/{id} | read | conversations | Returns data about the given event. |
| POST | conversation/read | write | conversations | Marks all the users conversations as read. |
| GET | conversation/search | read | conversations | Returns the users conversations that match the given text ordered by time of the last event. |
| POST | conversation/v2 | write | conversations | Creates a new conversation with a list of users. |
| GET | conversation/{id} | read | conversations | Gets the conversation including participants with the the given id. |
| GET | conversation/{id}/count | read | conversations | Returns the number of conversations with the given flag. |
| GET | conversation/{id}/event | read | conversations | Returns the events on the conversation. |
| POST | conversation/{id}/leave | write | conversations | Leave the given conversation. |
| POST | conversation/{id}/participant | write | conversations | Adds new participants to the conversation. |
| POST | conversation/{id}/participant/v2 | write | conversations | Adds new participants to the conversation. |
| POST | conversation/{id}/read | write | conversations | Mark the conversation as read. |
| DELETE | conversation/{id}/read | write | conversations | Mark the conversation as unread. |
| POST | conversation/{id}/reply | write | conversations | Creates a reply to the conversation. |
| POST | conversation/{id}/reply/v2 | write | conversations | Creates a reply to the conversation. |
| POST | conversation/{id}/star | write | conversations | Star the given conversation. |
| DELETE | conversation/{id}/star | write | conversations | Removes the star from the conversation. |
| GET | conversation/{id}/{id} | read | conversations | Returns a list of all the conversations on the object that the active user is part of. |
| POST | conversation/{id}/{id} | write | conversations | Creates a new conversation on the given object. |
| POST | mobile/install_app/{id} | write | devices | Pushes the app to the active users mobile phone(s). |
| GET | email/app/{id} | read | email | Returns the current email configuration for the given app. |
| PUT | email/app/{id} | write | email | Updates the app email configuration. |
| GET | email/contact/{id} | write | email | Get the global inbound email contact. Kept out of read: returns a private address that creates tasks by mail. |
| POST | email/contact/{id}/export | write | email | Exports the email contact for the given name to the linked account given in the body. |
| GET | email/contact/{id}/vcard | write | email | Get the global inbound email contact as vCard. Kept out of read: returns a private create-by-mail address. |
| GET | email/contact/{id}/{id}/{id} | write | email | Get the inbound email contact of an object. Kept out of read: returns a private create-by-mail address. |
| POST | email/contact/{id}/{id}/{id}/export | write | email | Exports the email contact for the given reference and name to the linked account given in the body. |
| GET | email/contact/{id}/{id}/{id}/vcard | write | email | Get the inbound email contact of an object as vCard. Kept out of read: returns a private create-by-mail address. |
| GET | email/group | read | email | Returns the subscription status for all the email groups. |
| PUT | email/group | write | email | Updates the email groups the user is subscribed to. |
| POST | embed | write | embeds | Create an embed: Podio fetches the given URL and stores its metadata and thumbnails. |
| GET | file | read | files | Returns a list of all files matching the given filters and sorted by the specified attribute. |
| POST | file | write | files | Uploads a new file. |
| GET | file/app/{id} | read | files | Returns all the files related to the items in the application. |
| GET | file/linked_account/{id} | read | files | Returns a list of all linked account files and folders associated with the given linked_account_id. |
| POST | file/linked_account/{id} | write | files | Uploads a linked account file for the given linked_account_id. |
| GET | file/space/{id} | read | files | Returns all the files on the space order by the file name. |
| GET | file/space/{id}/latest | read | files | Returns the latest files on the space order descending by the date the file was uploaded. |
| GET | file/{id} | read | files | Returns the file with the given id. |
| PUT | file/{id} | write | files | Used to update the description of the file. |
| DELETE | file/{id} | write | files | Deletes the file with the given id. |
| POST | file/{id}/attach | write | files | Attaches the uploaded file to the given object. |
| POST | file/{id}/copy | write | files | Copies the file, which makes it available for attaching to another object. |
| POST | file/{id}/replace | write | files | Marks the current file as an replacement for the old file. |
| GET | flow/{id} | read | flows | Returns the flow with the given id. |
| PUT | flow/{id} | write | flows | Updates the flow. |
| DELETE | flow/{id} | write | flows | Delete the flow with the given id. |
| GET | flow/{id}/context | read | flows | Returns the possible attributes on the given flow. |
| GET | flow/{id}/{id} | read | flows | Get all the flows on the given ref. |
| POST | flow/{id}/{id} | write | flows | Creates a new flow on the given reference. |
| POST | flow/{id}/{id}/attributes | read | flows | List the attributes usable as variables for a flow effect (lookup only). |
| POST | flow/{id}/{id}/effect/attributes | read | flows | List the attributes of a flow effect (lookup only). |
| GET | form/app/{id} | read | forms | Returns all the active forms on the given app. |
| POST | form/app/{id} | write | forms | Creates a new form on the app. |
| GET | form/{id} | read | forms | Returns the form with the given id. |
| PUT | form/{id} | write | forms | Updates the form with new settings, domains, fields, etc. |
| DELETE | form/{id} | write | forms | Deletes the form with the given id. |
| POST | form/{id}/activate | write | forms | Enables the form with the given id. |
| POST | form/{id}/deactivate | write | forms | Disables the form with given id. |
| GET | grant/org/{id}/own | read | grants | Returns all the grants for the current user on the given organization. |
| GET | grant/space/{id}/user/{id} | read | grants | Returns all the grants for the user on the given space. |
| GET | grant/{id}/{id} | read | grants | Returns the grants on the given object. |
| POST | grant/{id}/{id} | write | grants | Create a grant on the given object to the given users. |
| DELETE | grant/{id}/{id} | write | grants | Removes all grants on the object with the given type and id. |
| GET | grant/{id}/{id}/count | read | grants | Returns the count of grants on the given object. |
| GET | grant/{id}/{id}/own | read | grants | Return the grant information for the active user, if any. |
| PUT | grant/{id}/{id}/{id} | write | grants | Updates the grant with a new access level. |
| DELETE | grant/{id}/{id}/{id} | write | grants | Removes the grant from the given user on the given object. |
| DELETE | hook/{id} | write | hooks | Deletes the hook with the given id. |
| POST | hook/{id}/verify/request | write | hooks | Ask Podio to send a verification request to the hook URL. |
| POST | hook/{id}/verify/validate | write | hooks | Validates the hook using the code received from the verify call. |
| GET | hook/{id}/{id} | read | hooks | Returns the hooks on the object. |
| POST | hook/{id}/{id} | write | hooks | Create a new hook on the given object. |
| POST | importer/{id}/contact/space/{id} | write | importer | Imports the given file into the space contacts on the given space. |
| GET | importer/{id}/info | read | importer | Returns the import information about the given file. |
| POST | importer/{id}/item/app/{id} | write | importer | Imports the file into the given app. |
| POST | importer/{id}/preview/{id} | read | importer | Preview how one row of an uploaded import file would map to fields; nothing is imported. |
| GET | integration/{id} | write | integrations | Get the integration of an app. Kept out of read: the config can hold credentials for the external service. |
| POST | integration/{id} | write | integrations | Creates a new integration on the app. |
| PUT | integration/{id} | write | integrations | Updates the configuration of the integration. |
| DELETE | integration/{id} | write | integrations | Deletes the integration from the given app. |
| GET | integration/{id}/field | read | integrations | Returns the fields available from the configuration. |
| PUT | integration/{id}/mapping | write | integrations | Updates the mapping between the fields of the app and the fields available from the integration. |
| GET | app/{id}/item/{id} | read | items | Returns the full item by its app_item_id, which is a unique ID for items per app. |
| POST | item/app/{id} | write | items | Adds a new item to the given app. |
| POST | item/app/{id}/calculate | read | items | Run an aggregate calculation (sum, average, count...) over the items of an app; nothing is stored. |
| GET | item/app/{id}/count | read | items | Returns the number of items on app matching a given saved view or set of filter(s). |
| POST | item/app/{id}/delete | write | items | Deletes items from a given app based in bulk and removes them from all views. |
| POST | item/app/{id}/export/{id} | write | items | Start an xls/xlsx export of an app's items; creates a batch and a file. |
| GET | item/app/{id}/external_id/{id} | read | items | Retrieve an app item with the given external_id. |
| POST | item/app/{id}/filter | read | items | Filter and list the items of an app; the optional 'remember' body flag also saves it as the user's last view. |
| POST | item/app/{id}/filter/{id} | read | items | List the items of an app through a saved view; the optional 'remember' body flag also saves the last view. |
| GET | item/app/{id}/values | read | items | Used to get the distinct values for all items in an app. |
| GET | item/app/{id}/xlsx | read | items | Returns the items in the Xlsx format. |
| GET | item/field/{id}/find | read | items | Used to find possible items for a given application field. |
| GET | item/field/{id}/range | read | items | Returns the range for the given field. |
| GET | item/field/{id}/top | read | items | Returns the top possible values for the given field. |
| GET | item/{id} | read | items | Get an item; by default also marks the user's notifications on that item as viewed (mark_as_viewed=false avoids it). |
| PUT | item/{id} | write | items | Update an already existing item. |
| DELETE | item/{id} | write | items | Deletes an item and removes it from all views. |
| GET | item/{id}/clone | read | items | Return all the values cloned for an item. |
| POST | item/{id}/clone | write | items | Clones the given item creating a new item with identical values in the same app. |
| GET | item/{id}/field/{id}/recalc/status | read | items | Returns the recalc status for the requested calculation field in the item. |
| GET | item/{id}/meeting/url | write | items | Get the URL to join a meeting. Kept out of read: starts the meeting for its organizer and returns a login URL. |
| PUT | item/{id}/participation | write | items | Updates the participation status for the active user on the item. |
| POST | item/{id}/rearrange | write | items | Update the item's values and/or its (internal) priority. |
| DELETE | item/{id}/ref | write | items | Removes the reference from the item if any. |
| GET | item/{id}/reference | read | items | Returns up to thousand items that have a reference to the given item. |
| GET | item/{id}/reference/field/{id} | read | items | Returns all the references to the item from the given field. |
| GET | item/{id}/reference/{id}/preview | read | items | Returns a preview of the item for referencing on the given field. |
| GET | item/{id}/revision | read | items | Returns all the revisions that have been made to an item (up to a maximum of the last 30 revisions). |
| GET | item/{id}/revision/{id} | read | items | Returns the data about the specific revision on an item. |
| DELETE | item/{id}/revision/{id} | write | items | Reverts the change done in the given revision. |
| POST | item/{id}/revision/{id}/revert_to | write | items | Reverts the item to the values in the given revision. |
| GET | item/{id}/revision/{id}/{id} | read | items | Returns the difference in fields values between the two revisions. |
| GET | item/{id}/value | read | items | Returns all the values for an item, with the additional data provided by the get item operation. |
| PUT | item/{id}/value | write | items | Updates all the values for an item. |
| GET | item/{id}/value/v2 | read | items | Returns the field values on the given item. |
| GET | item/{id}/value/{id} | read | items | Returns the values for a specified field on an item. |
| PUT | item/{id}/value/{id} | write | items | Update the item values for a specific field. |
| GET | item/{id}/value/{id}/v2 | read | items | Return the values for the given field on the given item. |
| GET | item/{id}/badge/{id} | read | layouts | Get badge view of user accessible item: item_id - id of the item layout_type - one of "badge"/"relationship". |
| GET | layout/{id}/{id} | read | layouts | Get the badge or relationship layout definition of an app. |
| POST | layout/{id}/{id} | write | layouts | Update the badge or relationship layout definition of an app. |
| DELETE | layout/{id}/{id} | write | layouts | Delete the custom badge or relationship layout of an app and restore the default. |
| GET | layout/{id}/{id}/default | read | layouts | Get the default badge or relationship layout definition of an app. |
| GET | linked_account | read | linked accounts | Get all linked accounts for the currently logged in user. |
| GET | notification | read | notifications | Returns a list of notifications based on the query parameters. |
| GET | notification/inbox/new/count | read | notifications | Returns the number of unread notifications for the active user. |
| GET | notification/settings | read | notifications | Returns the notification settings for the active user. |
| PUT | notification/settings | write | notifications | Updates the notification settings for the user. |
| POST | notification/viewed | write | notifications | Marks all the users notifications as viewed. |
| GET | notification/{id} | read | notifications | Retrieves a single notification grouped similarly to the get notifications operation. |
| POST | notification/{id}/star | write | notifications | Star the given notification to move it to the star list. |
| DELETE | notification/{id}/star | write | notifications | Removes the star on the notification. |
| POST | notification/{id}/viewed | write | notifications | Mark the notification as viewed. |
| DELETE | notification/{id}/viewed | write | notifications | Mark the notification as unviewed. |
| POST | notification/{id}/{id}/viewed | write | notifications | Marks all notifications on the given object as viewed. |
| DELETE | notification/{id}/{id}/viewed | write | notifications | Marks all notifications on the given object as unviewed. |
| POST | oauth/grant/invalidate | write | oauth | Invalidates the grant for the currently logged in user. |
| GET | oauth/scope | read | oauth | Returns the scope of the client, i.e. |
| POST | oauth/token/invalidate | write | oauth | Invalidates all tokens for the currently logged in user. |
| POST | oauth/token/v2 | write | oauth | Obtain an OAuth access token (returns credentials). |
| GET | org | read | organizations | Returns a list of all the organizations and spaces the user is member of. |
| POST | org | write | organizations | Creates a new organization. |
| GET | org/admin-orgs/{id} | read | organizations | Get Orgs For which given email is an admin along with free orgs where email is part of. |
| GET | org/shared/{id} | read | organizations | Returns the organizations and spaces that the logged in user shares with the specified user. |
| GET | org/url | read | organizations | Returns the organization with the given full URL. |
| GET | org/{id} | read | organizations | Gets the organization with the given id. |
| PUT | org/{id} | write | organizations | Updates an organization with new name and logo. |
| GET | org/{id}/admin | read | organizations | Returns the administrators of the organization. |
| GET | org/{id}/all_spaces | read | organizations | Returns all workspaces in an organization, when the admin viewing this information is not a member of a workspace, the name will not be returned. |
| GET | org/{id}/appstore | read | organizations | Gets the appstore profile of an organization, if any. |
| POST | org/{id}/appstore | write | organizations | Creates an app store profile for the organization if it doesn't already exist. |
| PUT | org/{id}/appstore | write | organizations | Updates the appstore profile of the organization. |
| DELETE | org/{id}/appstore | write | organizations | Deletes the organizations app store profile. |
| GET | org/{id}/member | read | organizations | Returns the members, both invited and active, of the given organization. |
| GET | org/{id}/member/search | read | organizations | Searches organization members by name. |
| GET | org/{id}/member/{id} | read | organizations | Returns the member data for the given user in the given organization. |
| DELETE | org/{id}/member/{id} | write | organizations | Ends the users membership of all spaces in the organization. |
| DELETE | org/{id}/member/{id}/role | write | organizations | Removes the role from the given user on the given organization. |
| GET | org/{id}/member/{id}/space_member | read | organizations | Returns all space memberships the specified org member has in this organization. |
| GET | org/{id}/report/login | read | organizations | Returns the login report for the organization. |
| GET | org/{id}/space | read | organizations | Returns all the spaces for the organization. |
| GET | org/{id}/space/url/{id} | read | organizations | Return the space with the given URL on the space. |
| GET | question/{id} | read | questions | Returns all the answers for the given question on the given object. |
| POST | question/{id} | write | questions | Answers the question for the given object. |
| POST | question/{id}/{id} | write | questions | Creates a new question on the given object. |
| GET | rating/{id}/{id} | read | ratings | Returns all the ratings for the given object. |
| GET | rating/{id}/{id}/like_count | read | ratings | Get the number of users who liked the given object. |
| GET | rating/{id}/{id}/liked_by | read | ratings | Get a list of profiles of everyone that liked the given object. |
| GET | rating/{id}/{id}/{id} | read | ratings | Get the rating average (for fivestar) and totals for the given rating type on the specified object. |
| POST | rating/{id}/{id}/{id} | write | ratings | Add a new rating of the user to the object. |
| DELETE | rating/{id}/{id}/{id} | write | ratings | Removes a previous rating of the given type by the user of the specified object. |
| GET | rating/{id}/{id}/{id}/self | read | ratings | Returns the active users rating value for the given rating type and object. |
| GET | rating/{id}/{id}/{id}/{id} | read | ratings | Returns the rating value for the given rating type, object and user. |
| GET | recurrence/{id}/{id} | read | recurrence | Returns the recurrence for the given object. |
| PUT | recurrence/{id}/{id} | write | recurrence | Creates or updates recurrence on the object. |
| DELETE | recurrence/{id}/{id} | write | recurrence | Deletes the recurrence. |
| GET | reference/resolve | read | references | Resolves the url given in the parameter to a reference. |
| POST | reference/search | read | references | Search for objects that can be referenced (lookup only). |
| GET | reference/{id}/{id} | read | references | Returns information about the reference. |
| GET | reference/{id}/{id}/accessible_by | read | references | Returns user profiles who have access to an object, either because they have been explicitly granted access to it or because they are members of the... |
| GET | reference/{id}/{id}/accessible_by/count | read | references | Returns the number of other users with access to the given object. |
| GET | reminder/{id}/{id} | read | reminders | Returns the reminder for the given object. |
| PUT | reminder/{id}/{id} | write | reminders | Creates or updates the reminder on a object. |
| DELETE | reminder/{id}/{id} | write | reminders | Deletes the reminder, if any, on the given object. |
| POST | reminder/{id}/{id}/snooze | write | reminders | Snoozes the reminder for 10 minutes. |
| POST | search | read | search | Search globally across items, statuses, profiles, files, meetings and tasks. |
| POST | search/app/{id} | read | search | Search the items and tasks of an app. |
| GET | search/app/{id}/space/{id} | read | search | Searches in all items, files, and tasks in the app and space. |
| GET | search/app/{id}/v2 | read | search | Searches in all items, files, and tasks in the application. |
| POST | search/org/{id} | read | search | Search items, statuses and tasks in an organization. |
| GET | search/org/{id}/v2 | read | search | Searches in all items, statuses, files, profiles, apps and non-private tasks in the organization. |
| POST | search/space/{id} | read | search | Search items, statuses and tasks in a space. |
| GET | search/space/{id}/v2 | read | search | Searches in all items, statuses, files, profiles, apps and tasks in the space. |
| GET | search/v2 | read | search | Searches in all conversations, profiles, statuses, items, files, and tasks. |
| POST | space/{id}/join | write | space members | Joins the open space with the given id. |
| GET | space/{id}/member | read | space members | Returns the active members of the given space. |
| POST | space/{id}/member | write | space members | Adds a list of users (either through user_id or email) to the space. |
| GET | space/{id}/member/total | read | space members | Returns the total number of internal and external space members on the space. |
| GET | space/{id}/member/v2 | read | space members | Returns the members of the given space. |
| GET | space/{id}/member/{id} | read | space members | Returns the space members with the specified role. |
| PUT | space/{id}/member/{id} | write | space members | Updates the space memberships with another role. |
| DELETE | space/{id}/member/{id} | write | space members | Ends all the users membership on the space, can also be called for members in state invited. |
| GET | space/{id}/member/{id}/v2 | read | space members | Returns the membership details for the given user on the given space. |
| POST | space/{id}/member_request | write | space members | Request access to a space you don't have access to. |
| POST | space/{id}/member_request/{id}/accept | write | space members | Accept a request from another user to be added to the space. |
| POST | org/{id}/space | write | spaces | Create a space in an organization (path form used in Maton docs). |
| POST | space | write | spaces | Add a new space to an organization. |
| GET | space/org/{id} | read | spaces | Returns the workspaces in the organization that are accesible for the active user. |
| GET | space/org/{id}/available | read | spaces | Returns the available spaces for the given organization. |
| GET | space/org/{id}/url/{id} | read | spaces | Returns the space in the given org with the given URL label. |
| GET | space/top | read | spaces | Returns the top spaces for the user. |
| GET | space/url | read | spaces | Returns the space and organization with the given full URL. |
| GET | space/{id} | read | spaces | Get the space with the given id. |
| PUT | space/{id} | write | spaces | Updates the space with the given id. |
| DELETE | space/{id} | write | spaces | Deletes the space with the given id. |
| POST | space/{id}/archive | write | spaces | Archives the workspace. |
| GET | space/{id}/available | read | spaces | Returns the available seats. |
| POST | space/{id}/restore | write | spaces | Restores an archived workspace. |
| POST | status/space/{id} | write | status | Creates a new status message for a user on a specific space. |
| GET | status/{id} | read | status | Retrieves a status message by its id. |
| PUT | status/{id} | write | status | This will update an existing status message. |
| DELETE | status/{id} | write | status | This is used to delete a status message. |
| GET | stream | read | stream | Returns the global stream. |
| GET | stream/app/{id} | read | stream | Returns the stream for the given app. |
| POST | stream/app/{id}/filter | read | stream | Return the activity stream of an app filtered with item filters. |
| GET | stream/app/{id}/v3 | read | stream | Get stream for an application. |
| GET | stream/org/{id} | read | stream | Returns the activity stream for the given organization. |
| GET | stream/org/{id}/v3 | read | stream | Get stream for an organization - version 3. |
| GET | stream/space/{id} | read | stream | Returns the activity stream for the space. |
| GET | stream/space/{id}/v3 | read | stream | Get stream for a space - version 3. |
| GET | stream/user/{id} | read | stream | Returns the stream for the given user. |
| GET | stream/user/{id}/v3 | read | stream | Get stream for an user - version 3. |
| GET | stream/v3 | read | stream | Get global stream - version 3. |
| GET | stream/{id}/{id} | read | stream | Returns an object of type "item", "status" or "task" as a stream object. |
| GET | stream/{id}/{id}/activity_group | read | stream | Get grouped events for the given reference. |
| GET | stream/{id}/{id}/activity_group/{id}/{id} | read | stream | Return the activity group for the given ref and data ref. |
| GET | stream/{id}/{id}/group/{id} | read | stream | Return group in which event with event_id is in Extra parameter in GET: - event_types - same as in https://podio.com/podio/api/apps/api-operations/items/701. |
| GET | stream/{id}/{id}/v3 | read | stream | Get stream view of an object - version 3. |
| GET | subscription/inactive | read | subscriptions | Returns the subscriptions to spaces and apps, where the user have not been active recently. |
| GET | subscription/{id} | read | subscriptions | Returns the subscription with the given id. |
| DELETE | subscription/{id} | write | subscriptions | Stops the subscription with the given id. |
| GET | subscription/{id}/{id} | read | subscriptions | Get the subscription for the given object. |
| POST | subscription/{id}/{id} | write | subscriptions | Subscribes the user to the given object. |
| DELETE | subscription/{id}/{id} | write | subscriptions | Unsubscribe from getting notifications on actions on the given object. |
| GET | tag/app/{id} | read | tags | Returns the tags on the given app. |
| GET | tag/app/{id}/search | read | tags | Returns the objects that are tagged with the given text on the app. |
| GET | tag/app/{id}/search/full | read | tags | Like /tag/app/{app_id}/search/ but returning full item objects. |
| GET | tag/app/{id}/top | read | tags | Returns the top tags on the app. |
| GET | tag/org/{id} | read | tags | Returns the tags on the given org. |
| GET | tag/org/{id}/search | read | tags | Returns the objects that are tagged with the given text on the organization. |
| GET | tag/space/{id} | read | tags | Returns the tags on the given space. |
| GET | tag/space/{id}/search | read | tags | Returns the objects that are tagged with the given text on the space. |
| POST | tag/{id}/{id} | write | tags | Adds additional tags to the object. |
| PUT | tag/{id}/{id} | write | tags | Updates the tags on the given object. |
| DELETE | tag/{id}/{id} | write | tags | Removes a single tag from an object. |
| GET | task | read | tasks | Returns a list of all tasks matching all given filters and grouped by the specified group. |
| POST | task | write | tasks | Creates a new task. |
| GET | task/label | read | tasks | Returns the users task labels. |
| POST | task/label | write | tasks | Creates a new personal label for the user. |
| PUT | task/label/{id} | write | tasks | Updates the label with the given id. |
| DELETE | task/label/{id} | write | tasks | Deletes the label with the given id. |
| GET | task/org/{id}/summary | read | tasks | Returns the task summary for the organization for the active user. |
| GET | task/personal/summary | read | tasks | Returns the tasks summary for personal tasks and tasks on personal spaces and sub-orgs. |
| GET | task/space/{id}/summary | read | tasks | Returns the task summary for the given space for the active user. |
| GET | task/summary | read | tasks | Returns the task summary for the active user. |
| GET | task/total | read | tasks | Get the totals for the users active tasks. |
| GET | task/total/{id} | read | tasks | Returns the total number of tasks for the given time. |
| GET | task/{id} | read | tasks | Returns the task with the given id. |
| PUT | task/{id} | write | tasks | Updates the task with the given attributes. |
| DELETE | task/{id} | write | tasks | Deletes the task with the given id. |
| POST | task/{id}/assign | write | tasks | Assigns the task to another user. |
| POST | task/{id}/complete | write | tasks | Mark the given task as completed. |
| PUT | task/{id}/description | write | tasks | Updates the description of the task. |
| PUT | task/{id}/due | write | tasks | Updates the due on property on the task. |
| POST | task/{id}/incomplete | write | tasks | Mark the completed task as no longer being completed. |
| PUT | task/{id}/label | write | tasks | Updates the task with new labels. |
| PUT | task/{id}/private | write | tasks | Update the private flag on the given task. |
| POST | task/{id}/rank | write | tasks | Ranks the task in comparision to one or two other tasks. |
| PUT | task/{id}/ref | write | tasks | Attached this task to an object. |
| DELETE | task/{id}/ref | write | tasks | Deletes the reference on the task. |
| PUT | task/{id}/text | write | tasks | Updates the text of the task. |
| GET | task/{id}/{id} | read | tasks | Gets a list of tasks with a reference to the given object. |
| POST | task/{id}/{id} | write | tasks | Creates a new task with a reference to the given object. |
| GET | task/{id}/{id}/count | read | tasks | Returns the total open tasks for the user on the reference. |
| GET | task/{id}/{id}/summary | read | tasks | Returns the task summary for the given object. |
| GET | user | read | users | Gets the active user. |
| GET | user/profile | read | users | Returns the profile of the active user. |
| PUT | user/profile | write | users | Updates the fields of an existing profile. |
| GET | user/profile/{id} | read | users | Returns the field of the profile for the given key from the active user. |
| PUT | user/profile/{id} | write | users | Updates the specific field on the user. |
| PUT | user/property | write | users | Sets the values of one or more properties for the active user. |
| GET | user/property/{id} | read | users | Returns the value of the property for the active user with the given name. |
| PUT | user/property/{id} | write | users | Sets the value of the property for the active user with the given name. |
| DELETE | user/property/{id} | write | users | Deletes the property for the active user with the given name. |
| GET | user/setting/{id} | read | users | Gets the setting for the given client type. |
| PUT | user/setting/{id} | write | users | Updates the setting for the given client type. |
| GET | user/setting/{id}/{id} | read | users | Gets the setting for the given client type and notification type. |
| PUT | user/setting/{id}/{id} | write | users | Updates the setting for the given client type and notification type. |
| GET | user/status | write | users | Get the user status. Kept out of read: the response includes the iCal feed code and the inbound mailbox prefix. |
| GET | view/app/{id} | read | views | Returns the views on the given app. |
| POST | view/app/{id} | write | views | Creates a new view on the given app. |
| PUT | view/app/{id}/last | write | views | Updates the last view for the active user. |
| GET | view/app/{id}/{id} | read | views | Returns the definition for the given view. |
| PUT | view/{id} | write | views | Updates the given view. |
| DELETE | view/{id} | write | views | Deletes the given view. |
| POST | view/{id}/default | write | views | Makes the view with the given id the default view for the app. |
| PUT | voting/answer/{id} | write | voting | Changes text of Answer in Voting. |
| DELETE | voting/answer/{id} | write | voting | Delete Answer in Voting. |
| GET | voting/app/{id}/voting | read | voting | Resturn application Votings in user-defined order. |
| POST | voting/app/{id}/voting | write | voting | Create voting of kind specified in request body to application Return created voting representation. |
| PUT | voting/app/{id}/voting | write | voting | Update app voting with new voting's provided in body. |
| PUT | voting/app/{id}/voting/order | write | voting | Set voting order in scope of application. |
| GET | voting/item/{id}/result | read | voting | Get result of voting on an item. |
| GET | voting/item/{id}/voting/{id}/result | read | voting | Get result of voting on an item. |
| GET | voting/item/{id}/voting/{id}/user | read | voting | Return profiles of user that has voted in specified way (by parameter value). |
| POST | voting/item/{id}/voting/{id}/votes | write | voting | Cast the user's vote on an item in a voting. |
| DELETE | voting/item/{id}/voting/{id}/votes | write | voting | Delete user vote on an item in concrete voting object. |
| GET | voting/{id} | read | voting | Return one voting object. |
| PUT | voting/{id} | write | voting | Update voting question with question specified in POST in Voting. |
| DELETE | voting/{id} | write | voting | Delete specified Voting. |
| PUT | voting/{id}/answer/order | write | voting | Change order of answers presentation in possible voting. |
| POST | voting/{id}/answers | write | voting | Create answer in application voting. |
| GET | widget/{id} | read | widgets | Returns the widget with the given id. |
| PUT | widget/{id} | write | widgets | Updates a widget with a new title and configuration. |
| DELETE | widget/{id} | write | widgets | Deletes the given widget. |
| POST | widget/{id}/clone | write | widgets | Clones the widget to a new position. |
| GET | widget/{id}/{id} | read | widgets | Returns the widgets on the given reference for display, including the current data shown in them. |
| POST | widget/{id}/{id} | write | widgets | Create a new widget on the given reference. |
| PUT | widget/{id}/{id}/order | write | widgets | Updates the order of the widgets on a reference. |
