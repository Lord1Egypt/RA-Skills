# Google Classroom scopes

The OAuth scopes Google Classroom connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-classroom#permissions.

```bash
maton connection create google-classroom --scopes https://www.googleapis.com/auth/classroom.courses.readonly
```

| Scope | Requested |
| --- | --- |
| `https://www.googleapis.com/auth/classroom.topics` | By default |
| `https://www.googleapis.com/auth/classroom.addons.teacher` | By default |
| `https://www.googleapis.com/auth/classroom.addons.student` | By default |
| `https://www.googleapis.com/auth/classroom.announcements` | By default |
| `https://www.googleapis.com/auth/classroom.courses` | By default |
| `https://www.googleapis.com/auth/classroom.coursework.me` | By default |
| `https://www.googleapis.com/auth/classroom.coursework.students` | By default |
| `https://www.googleapis.com/auth/classroom.courseworkmaterials` | By default |
| `https://www.googleapis.com/auth/classroom.guardianlinks.students` | By default |
| `https://www.googleapis.com/auth/classroom.profile.emails` | By default |
| `https://www.googleapis.com/auth/classroom.rosters` | By default |
| `https://www.googleapis.com/auth/classroom.courses.readonly` | Optional |
| `https://www.googleapis.com/auth/classroom.rosters.readonly` | Optional |
| `https://www.googleapis.com/auth/classroom.coursework.me.readonly` | Optional |
| `https://www.googleapis.com/auth/classroom.coursework.students.readonly` | Optional |
| `https://www.googleapis.com/auth/classroom.announcements.readonly` | Optional |
| `https://www.googleapis.com/auth/classroom.topics.readonly` | Optional |
| `https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly` | Optional |
| `https://www.googleapis.com/auth/classroom.guardianlinks.students.readonly` | Optional |
| `https://www.googleapis.com/auth/userinfo.email` | Always |
