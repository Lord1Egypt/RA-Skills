# Google Workspace Admin access policy

An access policy limits which endpoints Google Workspace Admin connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-workspace-admin#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Google Workspace Admin: its 45 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create google-workspace-admin --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "admin/directory/v1/groups/{id}/aliases"},
    {"method": "GET", "path": "admin/directory/v1/users/{id}/aliases"},
    {"method": "GET", "path": "admin/directory/v1/users/{id}/asps"},
    {"method": "GET", "path": "admin/directory/v1/users/{id}/asps/{id}"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/resources/buildings"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/resources/buildings/{id}"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/resources/calendars"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/resources/calendars/{id}"},
    {"method": "GET", "path": "admin/directory/v1/customers/{id}/chrome/printServers"},
    {"method": "GET", "path": "admin/directory/v1/customers/{id}/chrome/printServers/{id}"},
    {"method": "GET", "path": "admin/directory/v1/customers/{id}/chrome/printers"},
    {"method": "GET", "path": "admin/directory/v1/customers/{id}/chrome/printers/{id}"},
    {"method": "GET", "path": "admin/directory/v1/customers/{id}/chrome/printers:listPrinterModels"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/devices/chromeos"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/devices/chromeos/{id}"},
    {"method": "GET", "path": "admin/directory/v1/customers/{id}"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/devices/chromeos/{id}/commands/{id}"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/devices/chromeos:countChromeOsDevices"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/domainaliases"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/domainaliases/{id}"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/domains"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/domains/{id}"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/resources/features"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/resources/features/{id}"},
    {"method": "GET", "path": "admin/directory/v1/groups"},
    {"method": "GET", "path": "admin/directory/v1/groups/{id}"},
    {"method": "GET", "path": "admin/directory/v1/groups/{id}/hasMember/{id}"},
    {"method": "GET", "path": "admin/directory/v1/groups/{id}/members"},
    {"method": "GET", "path": "admin/directory/v1/groups/{id}/members/{id}"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/devices/mobile"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/devices/mobile/{id}"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/orgunits"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/orgunits/{id}"},
    {"method": "GET", "path": "admin/directory/v1/users/{id}/photos/thumbnail"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/roles/ALL/privileges"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/roleassignments"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/roleassignments/{id}"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/roles"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/roles/{id}"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/schemas"},
    {"method": "GET", "path": "admin/directory/v1/customer/{id}/schemas/{id}"},
    {"method": "GET", "path": "admin/directory/v1/users/{id}/tokens"},
    {"method": "GET", "path": "admin/directory/v1/users/{id}/tokens/{id}"},
    {"method": "GET", "path": "admin/directory/v1/users"},
    {"method": "GET", "path": "admin/directory/v1/users/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Google Workspace Admin endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | admin/directory/v1/groups/{id}/aliases | read | aliases | Lists all aliases for a group. |
| POST | admin/directory/v1/groups/{id}/aliases | write | aliases | Adds an alias for the group. |
| DELETE | admin/directory/v1/groups/{id}/aliases/{id} | write | aliases | Removes an alias. |
| GET | admin/directory/v1/users/{id}/aliases | read | aliases | Lists all aliases for a user. |
| POST | admin/directory/v1/users/{id}/aliases | write | aliases | Adds an alias. |
| POST | admin/directory/v1/users/{id}/aliases/watch | write | aliases | Watches for changes in users list. |
| DELETE | admin/directory/v1/users/{id}/aliases/{id} | write | aliases | Removes an alias. |
| GET | admin/directory/v1/users/{id}/asps | read | asps | Lists the ASPs issued by a user. |
| GET | admin/directory/v1/users/{id}/asps/{id} | read | asps | Gets information about an ASP issued by a user. |
| DELETE | admin/directory/v1/users/{id}/asps/{id} | write | asps | Deletes an ASP issued by a user. |
| GET | admin/directory/v1/customer/{id}/resources/buildings | read | buildings | Retrieves a list of buildings for an account. |
| POST | admin/directory/v1/customer/{id}/resources/buildings | write | buildings | Inserts a building. |
| GET | admin/directory/v1/customer/{id}/resources/buildings/{id} | read | buildings | Retrieves a building. |
| PUT | admin/directory/v1/customer/{id}/resources/buildings/{id} | write | buildings | Updates a building. |
| PATCH | admin/directory/v1/customer/{id}/resources/buildings/{id} | write | buildings | Patches a building. |
| DELETE | admin/directory/v1/customer/{id}/resources/buildings/{id} | write | buildings | Deletes a building. |
| GET | admin/directory/v1/customer/{id}/resources/calendars | read | calendars | Retrieves a list of calendar resources for an account. |
| POST | admin/directory/v1/customer/{id}/resources/calendars | write | calendars | Inserts a calendar resource. |
| GET | admin/directory/v1/customer/{id}/resources/calendars/{id} | read | calendars | Retrieves a calendar resource. |
| PUT | admin/directory/v1/customer/{id}/resources/calendars/{id} | write | calendars | Updates a calendar resource. |
| PATCH | admin/directory/v1/customer/{id}/resources/calendars/{id} | write | calendars | Patches a calendar resource. |
| DELETE | admin/directory/v1/customer/{id}/resources/calendars/{id} | write | calendars | Deletes a calendar resource. |
| POST | admin/directory_v1/channels/stop | write | channels | Stops watching resources through this channel. |
| GET | admin/directory/v1/customers/{id}/chrome/printServers | read | chrome | Lists print server configurations. |
| POST | admin/directory/v1/customers/{id}/chrome/printServers | write | chrome | Creates a print server. |
| GET | admin/directory/v1/customers/{id}/chrome/printServers/{id} | read | chrome | Returns a print server's configuration. |
| PATCH | admin/directory/v1/customers/{id}/chrome/printServers/{id} | write | chrome | Updates a print server's configuration. |
| DELETE | admin/directory/v1/customers/{id}/chrome/printServers/{id} | write | chrome | Deletes a print server. |
| POST | admin/directory/v1/customers/{id}/chrome/printServers:batchCreatePrintServers | write | chrome | Creates multiple print servers. |
| POST | admin/directory/v1/customers/{id}/chrome/printServers:batchDeletePrintServers | write | chrome | Deletes multiple print servers. |
| GET | admin/directory/v1/customers/{id}/chrome/printers | read | chrome | List printers configs. |
| POST | admin/directory/v1/customers/{id}/chrome/printers | write | chrome | Creates a printer under given Organization Unit. |
| GET | admin/directory/v1/customers/{id}/chrome/printers/{id} | read | chrome | Returns a `Printer` resource (printer's config). |
| PATCH | admin/directory/v1/customers/{id}/chrome/printers/{id} | write | chrome | Updates a `Printer` resource. |
| DELETE | admin/directory/v1/customers/{id}/chrome/printers/{id} | write | chrome | Deletes a `Printer`. |
| POST | admin/directory/v1/customers/{id}/chrome/printers:batchCreatePrinters | write | chrome | Creates printers under given Organization Unit. |
| POST | admin/directory/v1/customers/{id}/chrome/printers:batchDeletePrinters | write | chrome | Deletes printers in batch. |
| GET | admin/directory/v1/customers/{id}/chrome/printers:listPrinterModels | read | chrome | Lists the supported printer models. |
| GET | admin/directory/v1/customer/{id}/devices/chromeos | read | chromeosdevices | Retrieves a paginated list of Chrome OS devices within an account. |
| POST | admin/directory/v1/customer/{id}/devices/chromeos/moveDevicesToOu | write | chromeosdevices | Moves or inserts multiple Chrome OS devices to an organizational unit. |
| GET | admin/directory/v1/customer/{id}/devices/chromeos/{id} | read | chromeosdevices | Retrieves a Chrome OS device's properties. |
| PUT | admin/directory/v1/customer/{id}/devices/chromeos/{id} | write | chromeosdevices | Updates a device's updatable properties, such as `annotatedUser`, `annotatedLocation`, `notes`, `orgUnitPath`, or `annotatedAssetId`. |
| PATCH | admin/directory/v1/customer/{id}/devices/chromeos/{id} | write | chromeosdevices | Updates a device's updatable properties, such as `annotatedUser`, `annotatedLocation`, `notes`, `orgUnitPath`, or `annotatedAssetId`. |
| POST | admin/directory/v1/customer/{id}/devices/chromeos/{id}/action | write | chromeosdevices | Use [BatchChangeChromeOsDeviceStatus](https://developers.google.com/workspace/admin/directory/reference/rest/v1/customer.devices.chromeos/batchChangeStatus) ins |
| GET | admin/directory/v1/customers/{id} | read | customers | Retrieves a customer. |
| PUT | admin/directory/v1/customers/{id} | write | customers | Updates a customer. |
| PATCH | admin/directory/v1/customers/{id} | write | customers | Patches a customer. |
| GET | admin/directory/v1/customer/{id}/devices/chromeos/{id}/commands/{id} | read | devices | Gets command data a specific command issued to the device. |
| POST | admin/directory/v1/customer/{id}/devices/chromeos/{id}:issueCommand | write | devices | Issues a command for the device to execute. |
| POST | admin/directory/v1/customer/{id}/devices/chromeos:batchChangeStatus | write | devices | Changes the status of a batch of ChromeOS devices. |
| GET | admin/directory/v1/customer/{id}/devices/chromeos:countChromeOsDevices | read | devices | Counts ChromeOS devices matching the request. |
| GET | admin/directory/v1/customer/{id}/domainaliases | read | domainAliases | Lists the domain aliases of the customer. |
| POST | admin/directory/v1/customer/{id}/domainaliases | write | domainAliases | Inserts a domain alias of the customer. |
| GET | admin/directory/v1/customer/{id}/domainaliases/{id} | read | domainAliases | Retrieves a domain alias of the customer. |
| DELETE | admin/directory/v1/customer/{id}/domainaliases/{id} | write | domainAliases | Deletes a domain Alias of the customer. |
| GET | admin/directory/v1/customer/{id}/domains | read | domains | Lists the domains of the customer. |
| POST | admin/directory/v1/customer/{id}/domains | write | domains | Inserts a domain of the customer. |
| GET | admin/directory/v1/customer/{id}/domains/{id} | read | domains | Retrieves a domain of the customer. |
| DELETE | admin/directory/v1/customer/{id}/domains/{id} | write | domains | Deletes a domain of the customer. |
| GET | admin/directory/v1/customer/{id}/resources/features | read | features | Retrieves a list of features for an account. |
| POST | admin/directory/v1/customer/{id}/resources/features | write | features | Inserts a feature. |
| GET | admin/directory/v1/customer/{id}/resources/features/{id} | read | features | Retrieves a feature. |
| PUT | admin/directory/v1/customer/{id}/resources/features/{id} | write | features | Updates a feature. |
| PATCH | admin/directory/v1/customer/{id}/resources/features/{id} | write | features | Patches a feature. |
| DELETE | admin/directory/v1/customer/{id}/resources/features/{id} | write | features | Deletes a feature. |
| POST | admin/directory/v1/customer/{id}/resources/features/{id}/rename | write | features | Renames a feature. |
| GET | admin/directory/v1/groups | read | groups | Retrieves all groups of a domain or of a user given a userKey (paginated). |
| POST | admin/directory/v1/groups | write | groups | Creates a group. |
| GET | admin/directory/v1/groups/{id} | read | groups | Retrieves a group's properties. |
| PUT | admin/directory/v1/groups/{id} | write | groups | Updates a group's properties. |
| PATCH | admin/directory/v1/groups/{id} | write | groups | Updates a group's properties. |
| DELETE | admin/directory/v1/groups/{id} | write | groups | Deletes a group. |
| GET | admin/directory/v1/groups/{id}/hasMember/{id} | read | members | Checks whether the given user is a member of the group. |
| GET | admin/directory/v1/groups/{id}/members | read | members | Retrieves a paginated list of all members in a group. |
| POST | admin/directory/v1/groups/{id}/members | write | members | Adds a user to the specified group. |
| GET | admin/directory/v1/groups/{id}/members/{id} | read | members | Retrieves a group member's properties. |
| PUT | admin/directory/v1/groups/{id}/members/{id} | write | members | Updates the membership of a user in the specified group. |
| PATCH | admin/directory/v1/groups/{id}/members/{id} | write | members | Updates the membership properties of a user in the specified group. |
| DELETE | admin/directory/v1/groups/{id}/members/{id} | write | members | Removes a member from a group. |
| GET | admin/directory/v1/customer/{id}/devices/mobile | read | mobiledevices | Retrieves a paginated list of all user-owned mobile devices for an account. |
| GET | admin/directory/v1/customer/{id}/devices/mobile/{id} | read | mobiledevices | Retrieves a mobile device's properties. |
| DELETE | admin/directory/v1/customer/{id}/devices/mobile/{id} | write | mobiledevices | Removes a mobile device. |
| POST | admin/directory/v1/customer/{id}/devices/mobile/{id}/action | write | mobiledevices | Takes an action that affects a mobile device. |
| GET | admin/directory/v1/customer/{id}/orgunits | read | orgunits | Retrieves a list of all organizational units for an account. |
| POST | admin/directory/v1/customer/{id}/orgunits | write | orgunits | Adds an organizational unit. |
| GET | admin/directory/v1/customer/{id}/orgunits/{id} | read | orgunits | Retrieves an organizational unit. |
| PUT | admin/directory/v1/customer/{id}/orgunits/{id} | write | orgunits | Updates an organizational unit. |
| PATCH | admin/directory/v1/customer/{id}/orgunits/{id} | write | orgunits | Updates an organizational unit. |
| DELETE | admin/directory/v1/customer/{id}/orgunits/{id} | write | orgunits | Removes an organizational unit. |
| GET | admin/directory/v1/users/{id}/photos/thumbnail | read | photos | Retrieves the user's photo. |
| PUT | admin/directory/v1/users/{id}/photos/thumbnail | write | photos | Adds a photo for the user. |
| PATCH | admin/directory/v1/users/{id}/photos/thumbnail | write | photos | Adds a photo for the user. |
| DELETE | admin/directory/v1/users/{id}/photos/thumbnail | write | photos | Removes the user's photo. |
| GET | admin/directory/v1/customer/{id}/roles/ALL/privileges | read | privileges | Retrieves a paginated list of all privileges for a customer. |
| GET | admin/directory/v1/customer/{id}/roleassignments | read | roleAssignments | Retrieves a paginated list of all roleAssignments. |
| POST | admin/directory/v1/customer/{id}/roleassignments | write | roleAssignments | Creates a role assignment. |
| GET | admin/directory/v1/customer/{id}/roleassignments/{id} | read | roleAssignments | Retrieves a role assignment. |
| DELETE | admin/directory/v1/customer/{id}/roleassignments/{id} | write | roleAssignments | Deletes a role assignment. |
| GET | admin/directory/v1/customer/{id}/roles | read | roles | Retrieves a paginated list of all the roles in a domain. |
| POST | admin/directory/v1/customer/{id}/roles | write | roles | Creates a role. |
| GET | admin/directory/v1/customer/{id}/roles/{id} | read | roles | Retrieves a role. |
| PUT | admin/directory/v1/customer/{id}/roles/{id} | write | roles | Updates a role. |
| PATCH | admin/directory/v1/customer/{id}/roles/{id} | write | roles | Patches a role. |
| DELETE | admin/directory/v1/customer/{id}/roles/{id} | write | roles | Deletes a role. |
| GET | admin/directory/v1/customer/{id}/schemas | read | schemas | Retrieves all schemas for a customer. |
| POST | admin/directory/v1/customer/{id}/schemas | write | schemas | Creates a schema. |
| GET | admin/directory/v1/customer/{id}/schemas/{id} | read | schemas | Retrieves a schema. |
| PUT | admin/directory/v1/customer/{id}/schemas/{id} | write | schemas | Updates a schema. |
| PATCH | admin/directory/v1/customer/{id}/schemas/{id} | write | schemas | Patches a schema. |
| DELETE | admin/directory/v1/customer/{id}/schemas/{id} | write | schemas | Deletes a schema. |
| GET | admin/directory/v1/users/{id}/tokens | read | tokens | Returns the set of tokens specified user has issued to 3rd party applications. |
| GET | admin/directory/v1/users/{id}/tokens/{id} | read | tokens | Gets information about an access token issued by a user. |
| DELETE | admin/directory/v1/users/{id}/tokens/{id} | write | tokens | Deletes all access tokens issued by a user for an application. |
| POST | admin/directory/v1/users/{id}/twoStepVerification/turnOff | write | twoStepVerification | Turns off 2-Step Verification for user. |
| GET | admin/directory/v1/users | read | users | Retrieves a paginated list of either deleted users or all users in a domain. |
| POST | admin/directory/v1/users | write | users | Creates a user. |
| POST | admin/directory/v1/users/watch | write | users | Watches for changes in users list. |
| GET | admin/directory/v1/users/{id} | read | users | Retrieves a user. |
| PUT | admin/directory/v1/users/{id} | write | users | Updates a user. |
| PATCH | admin/directory/v1/users/{id} | write | users | Updates a user using patch semantics. |
| DELETE | admin/directory/v1/users/{id} | write | users | Deletes a user. |
| POST | admin/directory/v1/users/{id}/makeAdmin | write | users | Makes a user a super administrator. |
| POST | admin/directory/v1/users/{id}/signOut | write | users | Signs a user out of all web and device sessions and reset their sign-in cookies. |
| POST | admin/directory/v1/users/{id}/undelete | write | users | Undeletes a deleted user. |
| POST | admin/directory/v1/users:createGuest | write | users | Create a guest user with access to a [subset of Workspace capabilities](https://support.google.com/a/answer/16558545). |
| GET | admin/directory/v1/users/{id}/verificationCodes | write | verificationCodes | Returns the current set of valid backup verification codes for the specified user. Kept out of read: returns the user's 2-step verification backup codes. |
| POST | admin/directory/v1/users/{id}/verificationCodes/generate | write | verificationCodes | Generates new backup verification codes for the user. |
| POST | admin/directory/v1/users/{id}/verificationCodes/invalidate | write | verificationCodes | Invalidates the current backup verification codes for the user. |
