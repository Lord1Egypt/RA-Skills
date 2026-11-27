# Google Classroom access policy

An access policy limits which endpoints Google Classroom connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-classroom#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Google Classroom: its 44 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create google-classroom --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1/courses/{id}/aliases"},
    {"method": "GET", "path": "v1/courses/{id}/announcements"},
    {"method": "GET", "path": "v1/courses/{id}/announcements/{id}"},
    {"method": "GET", "path": "v1/courses/{id}/announcements/{id}/addOnAttachments"},
    {"method": "GET", "path": "v1/courses/{id}/announcements/{id}/addOnAttachments/{id}"},
    {"method": "GET", "path": "v1/courses/{id}/announcements/{id}/addOnContext"},
    {"method": "GET", "path": "v1/courses/{id}/courseWork"},
    {"method": "GET", "path": "v1/courses/{id}/courseWork/{id}"},
    {"method": "GET", "path": "v1/courses/{id}/courseWork/{id}/addOnAttachments"},
    {"method": "GET", "path": "v1/courses/{id}/courseWork/{id}/addOnAttachments/{id}"},
    {"method": "GET", "path": "v1/courses/{id}/courseWork/{id}/addOnAttachments/{id}/studentSubmissions"},
    {"method": "GET", "path": "v1/courses/{id}/courseWork/{id}/addOnAttachments/{id}/studentSubmissions/{id}"},
    {"method": "GET", "path": "v1/courses/{id}/courseWork/{id}/addOnContext"},
    {"method": "GET", "path": "v1/courses/{id}/courseWork/{id}/rubrics"},
    {"method": "GET", "path": "v1/courses/{id}/courseWork/{id}/rubrics/{id}"},
    {"method": "GET", "path": "v1/courses/{id}/courseWork/{id}/studentSubmissions"},
    {"method": "GET", "path": "v1/courses/{id}/courseWork/{id}/studentSubmissions/{id}"},
    {"method": "GET", "path": "v1/courses/{id}/courseWorkMaterials"},
    {"method": "GET", "path": "v1/courses/{id}/courseWorkMaterials/{id}"},
    {"method": "GET", "path": "v1/courses/{id}/courseWorkMaterials/{id}/addOnAttachments"},
    {"method": "GET", "path": "v1/courses/{id}/courseWorkMaterials/{id}/addOnAttachments/{id}"},
    {"method": "GET", "path": "v1/courses/{id}/courseWorkMaterials/{id}/addOnContext"},
    {"method": "GET", "path": "v1/courses"},
    {"method": "GET", "path": "v1/courses/{id}"},
    {"method": "GET", "path": "v1/courses/{id}/gradingPeriodSettings"},
    {"method": "GET", "path": "v1/userProfiles/{id}/guardianInvitations"},
    {"method": "GET", "path": "v1/userProfiles/{id}/guardianInvitations/{id}"},
    {"method": "GET", "path": "v1/userProfiles/{id}/guardians"},
    {"method": "GET", "path": "v1/userProfiles/{id}/guardians/{id}"},
    {"method": "GET", "path": "v1/invitations"},
    {"method": "GET", "path": "v1/invitations/{id}"},
    {"method": "GET", "path": "v1/courses/{id}/posts/{id}/addOnAttachments"},
    {"method": "GET", "path": "v1/courses/{id}/posts/{id}/addOnAttachments/{id}"},
    {"method": "GET", "path": "v1/courses/{id}/posts/{id}/addOnAttachments/{id}/studentSubmissions/{id}"},
    {"method": "GET", "path": "v1/courses/{id}/posts/{id}/addOnContext"},
    {"method": "GET", "path": "v1/courses/{id}/studentGroups"},
    {"method": "GET", "path": "v1/courses/{id}/studentGroups/{id}/studentGroupMembers"},
    {"method": "GET", "path": "v1/courses/{id}/students"},
    {"method": "GET", "path": "v1/courses/{id}/students/{id}"},
    {"method": "GET", "path": "v1/courses/{id}/teachers"},
    {"method": "GET", "path": "v1/courses/{id}/teachers/{id}"},
    {"method": "GET", "path": "v1/courses/{id}/topics"},
    {"method": "GET", "path": "v1/courses/{id}/topics/{id}"},
    {"method": "GET", "path": "v1/userProfiles/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Google Classroom endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v1/courses/{id}/aliases | read | aliases | Returns a list of aliases for a course. |
| POST | v1/courses/{id}/aliases | write | aliases | Creates an alias for a course. |
| DELETE | v1/courses/{id}/aliases/{id} | write | aliases | Deletes an alias of a course. |
| GET | v1/courses/{id}/announcements | read | announcements | Returns a list of announcements that the requester is permitted to view. |
| POST | v1/courses/{id}/announcements | write | announcements | Creates an announcement. |
| GET | v1/courses/{id}/announcements/{id} | read | announcements | Returns an announcement. |
| PATCH | v1/courses/{id}/announcements/{id} | write | announcements | Updates one or more fields of an announcement. |
| DELETE | v1/courses/{id}/announcements/{id} | write | announcements | Deletes an announcement. |
| GET | v1/courses/{id}/announcements/{id}/addOnAttachments | read | announcements | Returns all attachments created by an add-on under the post. |
| POST | v1/courses/{id}/announcements/{id}/addOnAttachments | write | announcements | Creates an add-on attachment under a post. |
| GET | v1/courses/{id}/announcements/{id}/addOnAttachments/{id} | read | announcements | Returns an add-on attachment. |
| PATCH | v1/courses/{id}/announcements/{id}/addOnAttachments/{id} | write | announcements | Updates an add-on attachment. |
| DELETE | v1/courses/{id}/announcements/{id}/addOnAttachments/{id} | write | announcements | Deletes an add-on attachment. |
| GET | v1/courses/{id}/announcements/{id}/addOnContext | read | announcements | Gets metadata for Classroom add-ons in the context of a specific post. |
| POST | v1/courses/{id}/announcements/{id}:modifyAssignees | write | announcements | Modifies assignee mode and options of an announcement. |
| GET | v1/courses/{id}/courseWork | read | courseWork | Returns a list of course work that the requester is permitted to view. |
| POST | v1/courses/{id}/courseWork | write | courseWork | Creates course work. |
| GET | v1/courses/{id}/courseWork/{id} | read | courseWork | Returns course work. |
| PATCH | v1/courses/{id}/courseWork/{id} | write | courseWork | Updates one or more fields of a course work. |
| DELETE | v1/courses/{id}/courseWork/{id} | write | courseWork | Deletes a course work. |
| GET | v1/courses/{id}/courseWork/{id}/addOnAttachments | read | courseWork | Returns all attachments created by an add-on under the post. |
| POST | v1/courses/{id}/courseWork/{id}/addOnAttachments | write | courseWork | Creates an add-on attachment under a post. |
| GET | v1/courses/{id}/courseWork/{id}/addOnAttachments/{id} | read | courseWork | Returns an add-on attachment. |
| PATCH | v1/courses/{id}/courseWork/{id}/addOnAttachments/{id} | write | courseWork | Updates an add-on attachment. |
| DELETE | v1/courses/{id}/courseWork/{id}/addOnAttachments/{id} | write | courseWork | Deletes an add-on attachment. |
| GET | v1/courses/{id}/courseWork/{id}/addOnAttachments/{id}/studentSubmissions | read | courseWork | Returns a list of student submissions that the requester is permitted to view. |
| GET | v1/courses/{id}/courseWork/{id}/addOnAttachments/{id}/studentSubmissions/{id} | read | courseWork | Returns a student submission for an add-on attachment. |
| PATCH | v1/courses/{id}/courseWork/{id}/addOnAttachments/{id}/studentSubmissions/{id} | write | courseWork | Updates data associated with an add-on attachment submission. |
| GET | v1/courses/{id}/courseWork/{id}/addOnContext | read | courseWork | Gets metadata for Classroom add-ons in the context of a specific post. |
| PATCH | v1/courses/{id}/courseWork/{id}/rubric | write | courseWork | Updates a rubric. |
| GET | v1/courses/{id}/courseWork/{id}/rubrics | read | courseWork | Returns a list of rubrics that the requester is permitted to view. |
| POST | v1/courses/{id}/courseWork/{id}/rubrics | write | courseWork | Creates a rubric. |
| GET | v1/courses/{id}/courseWork/{id}/rubrics/{id} | read | courseWork | Returns a rubric. |
| PATCH | v1/courses/{id}/courseWork/{id}/rubrics/{id} | write | courseWork | Updates a rubric. |
| DELETE | v1/courses/{id}/courseWork/{id}/rubrics/{id} | write | courseWork | Deletes a rubric. |
| GET | v1/courses/{id}/courseWork/{id}/studentSubmissions | read | courseWork | Returns a list of student submissions that the requester is permitted to view, factoring in the OAuth scopes of the request. |
| GET | v1/courses/{id}/courseWork/{id}/studentSubmissions/{id} | read | courseWork | Returns a student submission. |
| PATCH | v1/courses/{id}/courseWork/{id}/studentSubmissions/{id} | write | courseWork | Updates one or more fields of a student submission. |
| POST | v1/courses/{id}/courseWork/{id}/studentSubmissions/{id}:modifyAttachments | write | courseWork | Modifies attachments of student submission. |
| POST | v1/courses/{id}/courseWork/{id}/studentSubmissions/{id}:reclaim | write | courseWork | Reclaims a student submission on behalf of the student that owns it. |
| POST | v1/courses/{id}/courseWork/{id}/studentSubmissions/{id}:return | write | courseWork | Returns a student submission. |
| POST | v1/courses/{id}/courseWork/{id}/studentSubmissions/{id}:turnIn | write | courseWork | Turns in a student submission. |
| POST | v1/courses/{id}/courseWork/{id}:modifyAssignees | write | courseWork | Modifies assignee mode and options of a coursework. |
| GET | v1/courses/{id}/courseWorkMaterials | read | courseWorkMaterials | Returns a list of course work material that the requester is permitted to view. |
| POST | v1/courses/{id}/courseWorkMaterials | write | courseWorkMaterials | Creates a course work material. |
| GET | v1/courses/{id}/courseWorkMaterials/{id} | read | courseWorkMaterials | Returns a course work material. |
| PATCH | v1/courses/{id}/courseWorkMaterials/{id} | write | courseWorkMaterials | Updates one or more fields of a course work material. |
| DELETE | v1/courses/{id}/courseWorkMaterials/{id} | write | courseWorkMaterials | Deletes a course work material. |
| GET | v1/courses/{id}/courseWorkMaterials/{id}/addOnAttachments | read | courseWorkMaterials | Returns all attachments created by an add-on under the post. |
| POST | v1/courses/{id}/courseWorkMaterials/{id}/addOnAttachments | write | courseWorkMaterials | Creates an add-on attachment under a post. |
| GET | v1/courses/{id}/courseWorkMaterials/{id}/addOnAttachments/{id} | read | courseWorkMaterials | Returns an add-on attachment. |
| PATCH | v1/courses/{id}/courseWorkMaterials/{id}/addOnAttachments/{id} | write | courseWorkMaterials | Updates an add-on attachment. |
| DELETE | v1/courses/{id}/courseWorkMaterials/{id}/addOnAttachments/{id} | write | courseWorkMaterials | Deletes an add-on attachment. |
| GET | v1/courses/{id}/courseWorkMaterials/{id}/addOnContext | read | courseWorkMaterials | Gets metadata for Classroom add-ons in the context of a specific post. |
| GET | v1/courses | read | courses | Returns a list of courses that the requesting user is permitted to view, restricted to those that match the request. |
| POST | v1/courses | write | courses | Creates a course. |
| GET | v1/courses/{id} | read | courses | Returns a course. |
| PUT | v1/courses/{id} | write | courses | Updates a course. |
| PATCH | v1/courses/{id} | write | courses | Updates one or more fields in a course. |
| DELETE | v1/courses/{id} | write | courses | Deletes a course. |
| GET | v1/courses/{id}/gradingPeriodSettings | read | courses | Returns the grading period settings in a course. |
| PATCH | v1/courses/{id}/gradingPeriodSettings | write | courses | Updates grading period settings of a course. |
| GET | v1/userProfiles/{id}/guardianInvitations | read | guardianInvitations | Returns a list of guardian invitations that the requesting user is permitted to view, filtered by the parameters provided. |
| POST | v1/userProfiles/{id}/guardianInvitations | write | guardianInvitations | Creates a guardian invitation, and sends an email to the guardian asking them to confirm that they are the student's guardian. |
| GET | v1/userProfiles/{id}/guardianInvitations/{id} | read | guardianInvitations | Returns a specific guardian invitation. |
| PATCH | v1/userProfiles/{id}/guardianInvitations/{id} | write | guardianInvitations | Modifies a guardian invitation. |
| GET | v1/userProfiles/{id}/guardians | read | guardians | Returns a list of guardians that the requesting user is permitted to view, restricted to those that match the request. |
| GET | v1/userProfiles/{id}/guardians/{id} | read | guardians | Returns a specific guardian. |
| DELETE | v1/userProfiles/{id}/guardians/{id} | write | guardians | Deletes a guardian. |
| GET | v1/invitations | read | invitations | Returns a list of invitations that the requesting user is permitted to view, restricted to those that match the list request. |
| POST | v1/invitations | write | invitations | Creates an invitation. |
| GET | v1/invitations/{id} | read | invitations | Returns an invitation. |
| DELETE | v1/invitations/{id} | write | invitations | Deletes an invitation. |
| POST | v1/invitations/{id}:accept | write | invitations | Accepts an invitation, removing it and adding the invited user to the teachers or students (as appropriate) of the specified course. |
| GET | v1/courses/{id}/posts/{id}/addOnAttachments | read | posts | Returns all attachments created by an add-on under the post. |
| POST | v1/courses/{id}/posts/{id}/addOnAttachments | write | posts | Creates an add-on attachment under a post. |
| GET | v1/courses/{id}/posts/{id}/addOnAttachments/{id} | read | posts | Returns an add-on attachment. |
| PATCH | v1/courses/{id}/posts/{id}/addOnAttachments/{id} | write | posts | Updates an add-on attachment. |
| DELETE | v1/courses/{id}/posts/{id}/addOnAttachments/{id} | write | posts | Deletes an add-on attachment. |
| GET | v1/courses/{id}/posts/{id}/addOnAttachments/{id}/studentSubmissions/{id} | read | posts | Returns a student submission for an add-on attachment. |
| PATCH | v1/courses/{id}/posts/{id}/addOnAttachments/{id}/studentSubmissions/{id} | write | posts | Updates data associated with an add-on attachment submission. |
| GET | v1/courses/{id}/posts/{id}/addOnContext | read | posts | Gets metadata for Classroom add-ons in the context of a specific post. |
| POST | v1/registrations | write | registrations | Creates a `Registration`, causing Classroom to start sending notifications from the provided `feed` to the destination provided in `cloudPubSubTopic`. |
| DELETE | v1/registrations/{id} | write | registrations | Deletes a `Registration`, causing Classroom to stop sending notifications for that `Registration`. |
| GET | v1/courses/{id}/studentGroups | read | studentGroups | Returns a list of groups in a course. |
| POST | v1/courses/{id}/studentGroups | write | studentGroups | Creates a student group for a course. |
| PATCH | v1/courses/{id}/studentGroups/{id} | write | studentGroups | Updates one or more fields in a student group. |
| DELETE | v1/courses/{id}/studentGroups/{id} | write | studentGroups | Deletes a student group. |
| GET | v1/courses/{id}/studentGroups/{id}/studentGroupMembers | read | studentGroups | Returns a list of students in a group. |
| POST | v1/courses/{id}/studentGroups/{id}/studentGroupMembers | write | studentGroups | Creates a student group member for a student group. |
| DELETE | v1/courses/{id}/studentGroups/{id}/studentGroupMembers/{id} | write | studentGroups | Deletes a student group member. |
| GET | v1/courses/{id}/students | read | students | Returns a list of students of this course that the requester is permitted to view. |
| POST | v1/courses/{id}/students | write | students | Adds a user as a student of a course. |
| GET | v1/courses/{id}/students/{id} | read | students | Returns a student of a course. |
| DELETE | v1/courses/{id}/students/{id} | write | students | Deletes a student of a course. |
| GET | v1/courses/{id}/teachers | read | teachers | Returns a list of teachers of this course that the requester is permitted to view. |
| POST | v1/courses/{id}/teachers | write | teachers | Creates a teacher of a course. |
| GET | v1/courses/{id}/teachers/{id} | read | teachers | Returns a teacher of a course. |
| DELETE | v1/courses/{id}/teachers/{id} | write | teachers | Removes the specified teacher from the specified course. |
| GET | v1/courses/{id}/topics | read | topics | Returns the list of topics that the requester is permitted to view. |
| POST | v1/courses/{id}/topics | write | topics | Creates a topic. |
| GET | v1/courses/{id}/topics/{id} | read | topics | Returns a topic. |
| PATCH | v1/courses/{id}/topics/{id} | write | topics | Updates one or more fields of a topic. |
| DELETE | v1/courses/{id}/topics/{id} | write | topics | Deletes a topic. |
| GET | v1/userProfiles/{id} | read | userProfiles | Returns a user profile. |
