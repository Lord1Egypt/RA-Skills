# JotForm access policy

An access policy limits which endpoints JotForm connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/jotform#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for JotForm: its 26 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create jotform --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "form/{id}/files"},
    {"method": "GET", "path": "folder/{id}"},
    {"method": "GET", "path": "user/folders"},
    {"method": "GET", "path": "form/{id}"},
    {"method": "GET", "path": "user/forms"},
    {"method": "GET", "path": "user/history"},
    {"method": "GET", "path": "user/invoices"},
    {"method": "GET", "path": "label/{id}"},
    {"method": "GET", "path": "label/{id}/resources"},
    {"method": "GET", "path": "user/labels"},
    {"method": "GET", "path": "form/{id}/properties"},
    {"method": "GET", "path": "form/{id}/properties/{id}"},
    {"method": "GET", "path": "form/{id}/question/{id}"},
    {"method": "GET", "path": "form/{id}/questions"},
    {"method": "GET", "path": "form/{id}/reports"},
    {"method": "GET", "path": "report/{id}"},
    {"method": "GET", "path": "user/reports"},
    {"method": "GET", "path": "user/settings"},
    {"method": "GET", "path": "form/{id}/submissions"},
    {"method": "GET", "path": "submission/{id}"},
    {"method": "GET", "path": "user/submissions"},
    {"method": "GET", "path": "user/subusers"},
    {"method": "GET", "path": "system/plan/{id}"},
    {"method": "GET", "path": "user/usage"},
    {"method": "GET", "path": "user"},
    {"method": "GET", "path": "form/{id}/webhooks"}
  ],
  "deny": []
}
```

## Endpoints

The JotForm endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | form/{id}/files | read | files | List of files uploaded on a form. |
| POST | folder | write | folders | Create a folder with specified parameters. |
| GET | folder/{id} | read | folders | Get the details of a folder, including the forms in it (deprecated in favor of labels). |
| PUT | folder/{id} | write | folders | Update a folder with specified parameters. |
| DELETE | folder/{id} | write | folders | Delete a folder and its subfolders. |
| GET | user/folders | read | folders | Get a list of form folders for this account (deprecated in favor of labels). |
| POST | form | write | forms | Create new forms with questions, properties and email settings. |
| PUT | form | write | forms | Create new forms with questions, properties and email settings. |
| GET | form/{id} | read | forms | Get basic information about a form. |
| DELETE | form/{id} | write | forms | Delete an existing form. |
| POST | form/{id}/clone | write | forms | Clone a single form. |
| GET | user/forms | read | forms | Get a list of forms for this account. |
| POST | user/forms | write | forms | Create new forms with questions, properties and email settings. |
| PUT | user/forms | write | forms | Create new forms with questions, properties and email settings. |
| GET | user/history | read | history | User activity log about things like forms created/modified/deleted, account logins and other operations. |
| GET | user/invoices | read | invoices | Get the list of invoices for this account. |
| POST | label | write | labels | Create a label by defining attributes such as name and color. |
| GET | label/{id} | read | labels | Get the details of a label, including its name and color. |
| PUT | label/{id} | write | labels | Update an existing label with specified parameters, such as name and color. |
| DELETE | label/{id} | write | labels | Delete a label along with all its sublabels. |
| PUT | label/{id}/add-resources | write | labels | Add the specified assets, identified by their IDs and types, into a label. |
| PUT | label/{id}/remove-resources | write | labels | Remove the specified assets, identified by their IDs and types, from a label. |
| GET | label/{id}/resources | read | labels | Get a list of assets in a label and their associated information. |
| GET | user/labels | read | labels | Get all labels in a user’s account, with optional support for including related resources via parameter. |
| GET | form/{id}/properties | read | properties | Get a list of all properties on a form. |
| POST | form/{id}/properties | write | properties | Edit a form property or add a new one. |
| PUT | form/{id}/properties | write | properties | Edit a form property or add a new one. |
| GET | form/{id}/properties/{id} | read | properties | Get a specific property of the form. |
| GET | form/{id}/question/{id} | read | questions | Get the details and properties of a single form question. |
| POST | form/{id}/question/{id} | write | questions | Edit a question property or add a new one. |
| DELETE | form/{id}/question/{id} | write | questions | Delete a single form question. |
| GET | form/{id}/questions | read | questions | Get a list of all questions on a form. |
| POST | form/{id}/questions | write | questions | Add new question to specified form. |
| PUT | form/{id}/questions | write | questions | Add new questions to specified form. |
| GET | form/{id}/reports | read | reports | Get all the reports of a specific form. |
| POST | form/{id}/reports | write | reports | Create new report of a form with intended fields, type and title. |
| GET | report/{id} | read | reports | Get the details of a report. |
| DELETE | report/{id} | write | reports | Delete an existing report. |
| GET | user/reports | read | reports | List of URLS for reports in this account. |
| GET | user/settings | read | settings | Get user's time zone and language. |
| POST | user/settings | write | settings | Update user's settings like time zone and language. |
| GET | form/{id}/submissions | read | submissions | List of form responses. |
| POST | form/{id}/submissions | write | submissions | Submit data to this form using the API. |
| PUT | form/{id}/submissions | write | submissions | Submit data to this form using the API. |
| GET | submission/{id} | read | submissions | Get the data of a single submission. |
| POST | submission/{id} | write | submissions | Edit a single submission. |
| DELETE | submission/{id} | write | submissions | Delete a single submission. |
| GET | user/submissions | read | submissions | Get a list of all submissions for all forms on this account. |
| GET | user/subusers | read | subusers | Get a list of sub users for this accounts and list of forms and form folders with access privileges. |
| GET | system/plan/{id} | read | system | Get limit and prices of a plan. |
| GET | user/usage | read | usage | Get number of form submissions received this month. |
| GET | user | read | user | Get user account details for this Jotform user. |
| POST | user/login | write | user | Login user with given credentials. |
| GET | user/logout | write | user | Log the user out of the current session. Kept out of read: it ends the current user session. |
| POST | user/register | write | user | Register a new Jotform user account. |
| GET | form/{id}/webhooks | read | webhooks | List the webhooks of a form. |
| POST | form/{id}/webhooks | write | webhooks | Webhooks can be used to send form submission data as an instant notification. |
| DELETE | form/{id}/webhooks/{id} | write | webhooks | Delete a webhook of a specific form. |
