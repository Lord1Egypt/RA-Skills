# Scenario Cards

Use these scenario cards to translate natural-language LinkedIn requests into a small, stable set of inputs. They are routing hints only; the exact method, `/v1/...` path, parameters, body shape, pagination, and response contract must come from `https://docs.keyapi.ai/llms.txt` and the linked endpoint page before execution.

Do not start by listing raw endpoints. First identify the user's business goal, choose the closest scenario, collect only missing high-value inputs, resolve the current docs, then execute through `scripts/keyapi-api.mjs` when available.

## Core Entities

people, companies, jobs, posts, comments, videos, images, experience, education, skills, certifications, publications, honors, recommendations, interests, followers, connections, and contact information

## Scenario Modules

| User intent | Reference module | Docs path family |
|---|---|---|
| People search, profile detail, contact info, career background, skills, and social proof | `linkedin-user-rules.md` | /linkedin/ |
| Company profile, employees, company posts, and company hiring footprint | `linkedin-company-rules.md` | /linkedin/ |
| Job listings, job counts, and job detail | `linkedin-jobs-rules.md` | /linkedin/ |

## 1. Find and qualify people

- User intent: Search professionals and build a reliable profile baseline.
- Primary entity: person / profile
- Ask for: keyword, role, company, location or other search filters from docs, profile URL/URN if known, and whether contact info is required.
- Default workflow: Use people search for discovery, then profile/about/follower-contact endpoints only for shortlisted users.
- Reference module: `linkedin-user-rules.md`
- Endpoint shortlist:
  - [Search people](https://docs.keyapi.ai/en/linkedin/search_people.md) - Search LinkedIn users
  - [Get user profile](https://docs.keyapi.ai/en/linkedin/get_user_profile.md) - Get LinkedIn user profile information
  - [Get user about](https://docs.keyapi.ai/en/linkedin/get_user_about.md) - Get LinkedIn user about/bio information
  - [Get user contact information](https://docs.keyapi.ai/en/linkedin/get_user_contact.md) - Get LinkedIn user contact information
  - [Get user follower and connection](https://docs.keyapi.ai/en/linkedin/get_user_follower_and_connection.md) - Get LinkedIn user follower and connection count

## 2. Assess professional background

- User intent: Analyze a person's experience, education, skills, credentials, publications, honors, or recommendations.
- Primary entity: career profile sections
- Ask for: profile identifier and the specific sections needed for the report.
- Default workflow: Fetch the profile baseline first, then call only the requested background sections to avoid unnecessary calls.
- Reference module: `linkedin-user-rules.md`
- Endpoint shortlist:
  - [Get user experience](https://docs.keyapi.ai/en/linkedin/get_user_experience.md) - Get LinkedIn user work experience
  - [Get user educations](https://docs.keyapi.ai/en/linkedin/get_user_educations.md) - Get LinkedIn user education background
  - [Get user skills](https://docs.keyapi.ai/en/linkedin/get_user_skills.md) - Get LinkedIn user skills
  - [Get user certifications](https://docs.keyapi.ai/en/linkedin/get_user_certifications.md) - Get LinkedIn user certifications
  - [Get user publications](https://docs.keyapi.ai/en/linkedin/get_user_publications.md) - Get LinkedIn user publications
  - [Get user honors](https://docs.keyapi.ai/en/linkedin/get_user_honors.md) - Get LinkedIn user honors and awards
  - [Get user recommendations](https://docs.keyapi.ai/en/linkedin/get_user_recommendations.md) - Get LinkedIn user recommendations

## 3. Review a person's content activity

- User intent: Inspect posts, comments, videos, images, and interests for a LinkedIn user.
- Primary entity: user activity / interests
- Ask for: profile identifier, content surfaces, page depth, and whether interests should be included.
- Default workflow: Use posts/comments/images/videos for activity; use interests companies/groups when the user asks for affinity or ecosystem context.
- Reference module: `linkedin-user-rules.md`
- Endpoint shortlist:
  - [Get user posts](https://docs.keyapi.ai/en/linkedin/get_user_posts.md) - Get posts published by a LinkedIn user
  - [Get user comments](https://docs.keyapi.ai/en/linkedin/get_user_comments.md) - Get comments by a LinkedIn user
  - [Get user videos](https://docs.keyapi.ai/en/linkedin/get_user_videos.md) - Get videos published by a LinkedIn user
  - [Get user images](https://docs.keyapi.ai/en/linkedin/get_user_images.md) - Get images published by a LinkedIn user
  - [Get user interests companies](https://docs.keyapi.ai/en/linkedin/get_user_interests_companies.md) - Get LinkedIn user interest companies
  - [Get user interests groups](https://docs.keyapi.ai/en/linkedin/get_user_interests_groups.md) - Get LinkedIn user interest groups

## 4. Analyze a company

- User intent: Profile a company, inspect employees, and review company-published content.
- Primary entity: company
- Ask for: company identifier, whether people and posts are needed, and page depth.
- Default workflow: Fetch company profile first, then company people and posts; use job endpoints only when hiring analysis is requested.
- Reference module: `linkedin-company-rules.md`
- Endpoint shortlist:
  - [Get company profile](https://docs.keyapi.ai/en/linkedin/get_company_profile.md) - Get LinkedIn company profile information
  - [Get company people](https://docs.keyapi.ai/en/linkedin/get_company_people.md) - Get LinkedIn company employee list
  - [Get company posts](https://docs.keyapi.ai/en/linkedin/get_company_posts.md) - Get posts published by a LinkedIn company
  - [Get company job count](https://docs.keyapi.ai/en/linkedin/get_company_job_count.md) - Get LinkedIn company job count

## 5. Research jobs and hiring demand

- User intent: Find company job listings, quantify open roles, or inspect a specific job.
- Primary entity: job / company hiring
- Ask for: company identifier, job filters from docs, job ID if known, and desired result size.
- Default workflow: Use job count for hiring footprint, company jobs for listings, and job detail for a selected role.
- Reference module: `linkedin-jobs-rules.md`
- Endpoint shortlist:
  - [Get company job count](https://docs.keyapi.ai/en/linkedin/get_company_job_count.md) - Get LinkedIn company job count
  - [Get company jobs](https://docs.keyapi.ai/en/linkedin/get_company_jobs.md) - Get LinkedIn company job listings
  - [Get job detail](https://docs.keyapi.ai/en/linkedin/get_job_detail.md) - Get LinkedIn job details

## Docs Search Strategy

1. Map the user's natural-language request to the closest scenario and API concept, then search `llms.txt` for the platform slug plus that semantic entity/action. Do not rely on literal keyword matching when the user wording is vague, translated, or business-oriented.
2. Prefer the narrowest endpoint whose title and description match the requested workflow.
3. Resolve the selected endpoint page before any live call; never infer method or path from this file.
4. Compose multiple endpoints only when the user asks for a report, comparison, enrichment, or explanation that one endpoint cannot answer.
5. API calls are live by default. Repeating the same parameters calls the API again. Large payloads may return a stdout preview; when complete fields are needed for analysis, rerun the same documented request with `--output-file <temp-or-workspace-.tmp-keyapi-file>.json` and read the API payload from `data.data`. Use a user-facing output path only when the user asks to save or export results.

## User Input Compression

Compress parameter-heavy tasks into:

- Goal: search, detail, enrichment, ranking, comparison, monitoring, or report
- Entity: the object being searched, analyzed, compared, ranked, or monitored
- Scope: market, country, language, category, keyword, identifier, date window, and page depth
- Sort or metric: freshness, relevance, growth, engagement, rating, sales, price, audience, or other documented metric
- Pagination depth: one page, top N, until enough evidence, or all available within the user's approved scope
- Output format: concise answer, table, raw JSON, or structured report
