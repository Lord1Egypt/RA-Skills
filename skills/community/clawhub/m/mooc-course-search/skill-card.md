## Description: <br>
MOOC course search and recommendation service for finding courses, comparing options, filtering by learning goals, and considering certificates and reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acse-yz219](https://clawhub.ai/user/acse-yz219) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and learning advisors use this skill to search China University MOOC courses, compare candidate courses, and produce actionable course-selection recommendations aligned to goals such as exams, employment, interest, or transfer study. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Course-search queries are sent to disclosed Youdao endpoints. <br>
Mitigation: Use the skill only when users are comfortable sending course-search terms to those endpoints, and avoid including unnecessary personal or sensitive information in queries. <br>
Risk: Users may paste credentials even though normal use does not require them. <br>
Mitigation: Do not paste long-lived credentials into prompts or write credentials to files or logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/acse-yz219/mooc-course-search) <br>
- [Youdao Course Search API Endpoint](https://mcp.study.youdao.com/public/mm-course/course/search) <br>
- [Youdao Course Detail API Endpoint](https://mcp.study.youdao.com/public/mm-course/course/detail) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Guidance, Shell commands] <br>
**Output Format:** [Markdown with course recommendations, summaries, query terms, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the queryList used for search and optional course-detail information when explicitly requested by the user.] <br>

## Skill Version(s): <br>
1.0.4 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
