## Description: <br>
Google Classroom API integration with managed OAuth for managing courses, assignments, students, teachers, announcements, and submissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to work with Google Classroom data through a Maton-managed OAuth connection, including course, coursework, submission, roster, invitation, topic, and announcement workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Maton-mediated OAuth access to Google Classroom data and requires a sensitive MATON_API_KEY. <br>
Mitigation: Keep MATON_API_KEY private, install only when this access is intended, and revoke unused Google Classroom connections. <br>
Risk: Write operations can create, update, delete, grade, return, or invite resources in the connected Google Classroom account. <br>
Mitigation: Confirm the target resource, selected connection, and intended effect with the user before any create, update, delete, grade, return, or invitation action. <br>
Risk: Multiple active Google Classroom connections can route requests to the wrong account if no connection is selected. <br>
Mitigation: Include the Maton-Connection header when multiple connections exist and verify the selected connection before acting. <br>


## Reference(s): <br>
- [Google Classroom API Documentation](https://developers.google.com/workspace/classroom/reference/rest) <br>
- [Course Resource Reference](https://developers.google.com/workspace/classroom/reference/rest/v1/courses) <br>
- [CourseWork Resource Reference](https://developers.google.com/workspace/classroom/reference/rest/v1/courses.courseWork) <br>
- [StudentSubmissions Reference](https://developers.google.com/workspace/classroom/reference/rest/v1/courses.courseWork.studentSubmissions) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with API examples and inline Bash, Python, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an authorized Google Classroom connection.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
