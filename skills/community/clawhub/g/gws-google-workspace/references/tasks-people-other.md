# Tasks, People, Meet, Classroom Reference

## Tasks

```bash
gws tasks tasklists list 2>/dev/null | tail -n +2 | jq '.items[]|{title,id}'
gws tasks tasks list --params '{"tasklist":"@default"}'
gws tasks tasks insert --json '{"title":"Task","notes":"Desc"}' --params '{"tasklist":"@default"}'
gws tasks tasks patch --params '{"tasklist":"@default","task":"TASK_ID"}' --json '{"status":"completed"}'
gws tasks tasks delete --params '{"tasklist":"@default","task":"TASK_ID"}'
gws tasks tasks clear --params '{"tasklist":"@default"}'
```

## People

`searchContacts` requires `readMask` — omitting it causes a 400 error.

```bash
gws people people get --params '{"resourceName":"people/me","personFields":"names,emailAddresses"}'
gws people people searchContacts --params '{"query":"john","pageSize":10,"readMask":"names,emailAddresses,phoneNumbers"}'
gws people connections list --params '{"resourceName":"people/me","personFields":"names,emailAddresses","pageSize":10}'
gws people people createContact --json '{"names":[{"givenName":"First","familyName":"Last"}],"emailAddresses":[{"value":"e@example.com"}]}' --params '{"readMask":"names,emailAddresses"}'
gws people contactGroups list --params '{"pageSize":10}'
```

## Meet / Classroom

```bash
gws meet conferenceRecords list --params '{"pageSize":10}'
gws classroom courses list --params '{"pageSize":10}'
gws classroom courses students list --params '{"courseId":"COURSE_ID"}'
gws classroom courses courseWork list --params '{"courseId":"COURSE_ID"}'
```
