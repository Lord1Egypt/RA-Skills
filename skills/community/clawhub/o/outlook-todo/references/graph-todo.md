# Microsoft Graph To Do Notes

Verified against Microsoft Learn on 2026-06-18.

Read task lists:

```text
GET /me/todo/lists
```

Read tasks in a list:

```text
GET /me/todo/lists/{todoTaskListId}/tasks
```

Least delegated permission for reading tasks is `Tasks.Read`; write operations require `Tasks.ReadWrite`.

In this setup the shared public client requests `Tasks.ReadWrite` dynamically during device-code login. Personal Outlook.com accounts can usually consent at login without pre-adding API permissions in Azure Portal. Work/school tenants may require configured permissions plus admin consent.
