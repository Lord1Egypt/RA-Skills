# LinkdAPI — Complete API Reference

> Source of truth: https://linkdapi.com/apispec.yml

**Base URL:** `https://linkdapi.com`  
**Auth Header:** `X-linkdapi-apikey: YOUR_KEY`  ← exact header name, case matters in some clients  
**Response envelope:** `{ success, statusCode, message, errors, data }`

Get API key: https://linkdapi.com/?p=signup (100 free credits)

---

## PROFILE ENDPOINTS

### GET `/api/v1/profile/overview`
Basic LinkedIn profile info by username. **Returns URN needed for all other profile endpoints.**

| Param | Type | Required |
|---|---|---|
| `username` | string | ✅ |

Returns: `firstName, lastName, fullName, headline, publicIdentifier, followerCount, connectionsCount, creator, qualityProfile, joined, profileID, urn, CurrentPositions[], isTopVoice, premium, influencer, location{countryCode,countryName,city,region,fullLocation}, backgroundImageURL, profilePictureURL, supportedLocales[]`

---

### GET `/api/v1/profile/details`
Detailed LinkedIn profile by URN.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ |

Returns: `about, featuredPosts[]{postLink,postText}, positions[]{jobTitle,company,location,duration,companyLink,companyId,jobDescription}, education[]{duration,durationParsed{start,end},university,universityLink,degree}, languages{languages[]{Language,Level},deepLink}`

---

### GET `/api/v1/profile/contact-info`
LinkedIn contact details by username. Email/phone only if user made them public.

| Param | Type | Required |
|---|---|---|
| `username` | string | ✅ |

Returns: `emailAddress (null if private), phoneNumber (null if private), websites[]{url, category}`

---

### GET `/api/v1/profile/about`
About section and verification info by URN.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ |

---

### GET `/api/v1/profile/full`
Complete LinkedIn profile in one request. Higher credit cost, fewer round trips.

| Param | Type | Required |
|---|---|---|
| `username` | string | one of |
| `urn` | string | one of |

---

### GET `/api/v1/profile/full-experience`
Complete work history with parsed start/end dates.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ |

Returns: `experience[]{companyName, companyId, companyLink, companyLogo, location, title, subTitle, description, duration, durationParsed{start{year,month,day}, end{year,month,day}, present, period}, positions[], isMultiPositions, totalDuration}`

---

### GET `/api/v1/profile/certifications`
Professional certifications by URN.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ |

Returns: `certifications[]{issuedBy, certificationLink, certificationName, issuedDate, issuerId, issuerLink, issuedDateParsed{year,month,day}}`

---

### GET `/api/v1/profile/education`
Education history by URN.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ |

Returns: `education[]{duration, durationParsed{start,end}, university, universityLink, degree, description, subDescription}`

---

### GET `/api/v1/profile/skills`
Skills and endorsement counts by URN.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ |

Returns: `skills[]{skillName, endorsementsLink, textActionTarget, isPassedLinkedInSkillAssessment, endorsementsCount}`

---

### GET `/api/v1/profile/social-matrix`
Follower and connection counts by username.

| Param | Type | Required |
|---|---|---|
| `username` | string | ✅ |

Returns: `{ connectionsCount, followersCount }`

---

### GET `/api/v1/profile/recommendations`
Given and received recommendations by URN.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ |

Returns: `Received[]{Text, Caption, Recommendee{name,headline,urn,url}}, Given[]{...}, Total, TotalGiven, TotalReceived`

---

### GET `/api/v1/profile/similar`
Similar profiles by URN.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ |

Returns: `[]{id, urn, publicIdentifier, firstName, lastName, headline, creator, profilePictureURL}`

---

### GET `/api/v1/profile/reactions`
All profile reactions, paginated.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ |
| `cursor` | string | ❌ |

---

### GET `/api/v1/profile/interests`
Profile interests by URN.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ |

---

### GET `/api/v1/profile/services`
Services offered by a profile.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ |

Returns: `services{servicesProvided[], servicePageURL, serviceId, requestProposalURL}`

---

### GET `/api/v1/profile/username-to-urn`
Get profile URN from username directly.

| Param | Type | Required |
|---|---|---|
| `username` | string | ✅ |

---

## COMPANIES ENDPOINTS

> Note: base path is `/api/v1/companies/` (plural), and company ID param is `id=` not `company_id=`

### GET `/api/v1/companies/name-lookup`
Search LinkedIn companies by name.

| Param | Type | Required |
|---|---|---|
| `query` | string | ✅ |

---

### GET `/api/v1/companies/company/info`
LinkedIn company details by ID or name.

| Param | Type | Required |
|---|---|---|
| `id` | string | one of |
| `name` | string | one of |

Returns: `id, name, universalName, description, website, industry, companySize, followerCount, employeeCount, founded, logoURL, specialties[], linkedinURL, headquartersCity, headquartersCountry`

---

### GET `/api/v1/companies/company/info-v2`
Extended company info including `peopleAlsoFollow`, `affiliatedByJobs`, etc.

| Param | Type | Required |
|---|---|---|
| `id` | string | ✅ |

---

### GET `/api/v1/companies/company/similar`
Similar companies by ID.

| Param | Type | Required |
|---|---|---|
| `id` | string | ✅ |

---

### GET `/api/v1/companies/company/employees-data`
Employee count and distribution stats.

| Param | Type | Required |
|---|---|---|
| `id` | string | ✅ |

Returns: `totalEmployees, distribution{function, seniority, geography}`

---

### GET `/api/v1/companies/company/affiliated-pages`
Subsidiaries and affiliated pages.

| Param | Type | Required |
|---|---|---|
| `id` | string | ✅ |

---

### GET `/api/v1/companies/company/posts`
Posts published by a company.

| Param | Type | Required |
|---|---|---|
| `id` | string | ✅ |
| `start` | int | ❌ (default: 0) |

---

### GET `/api/v1/companies/company/universal-name-to-id`
Get company numeric ID from universalName (slug).

| Param | Type | Required |
|---|---|---|
| `universalName` | string | ✅ |

---

### GET `/api/v1/companies/jobs`
Active LinkedIn job listings for one or more companies.

| Param | Type | Required | Notes |
|---|---|---|---|
| `companyIDs` | string | ✅ | Comma-separated company IDs |
| `start` | int | ❌ | default: 0 |

---

## JOBS ENDPOINTS

### GET `/api/v1/jobs/search`
Search LinkedIn jobs — version 1 (simpler filters).

| Param | Type | Values/Notes |
|---|---|---|
| `keyword` | string | Job title, skills, keywords |
| `location` | string | City, state, region text |
| `geoId` | string | LinkedIn geo ID (from geos/name-lookup) |
| `companyIds` | string | Comma-separated company IDs |
| `jobTypes` | string | `full_time`, `part_time`, `contract`, `temporary`, `internship`, `volunteer` |
| `experience` | string | `internship`, `entry_level`, `associate`, `mid_senior`, `director` |
| `regions` | string | Region codes |
| `timePosted` | string | `any`, `24h`, `1week`, `1month` (default: `any`) |
| `salary` | string | `any`, `40k`, `60k`, `80k`, `100k`, `120k` |
| `workArrangement` | string | `onsite`, `remote`, `hybrid` |
| `start` | int | Pagination offset (default: 0) |

---

### GET `/api/v1/jobs/job/details`
Full LinkedIn job details. **Only works for open/active jobs.**

| Param | Type | Required |
|---|---|---|
| `jobId` | string | ✅ |

Returns: `title, company, companyId, companyLogoURL, location, workplaceType, employmentType, experienceLevel, description, applicantsCount, postedAt, salary, applyURL, hiringTeam[]`

---

### GET `/api/v1/jobs/job/details-v2`
Job details v2. **Supports all job statuses** (open, closed, expired, etc.).

| Param | Type | Required |
|---|---|---|
| `jobId` | string | ✅ |

---

### GET `/api/v1/jobs/job/similar`
Similar LinkedIn jobs.

| Param | Type | Required |
|---|---|---|
| `jobId` | string | ✅ |

---

### GET `/api/v1/jobs/job/people-also-viewed`
Related jobs people also viewed.

| Param | Type | Required |
|---|---|---|
| `jobId` | string | ✅ |

---

### GET `/api/v1/jobs/job/hiring-team`
Hiring team members for a specific job.

| Param | Type | Required |
|---|---|---|
| `jobId` | string | ✅ |
| `start` | int | ❌ (default: 0) |

---

### GET `/api/v1/jobs/posted-by-profile`
Jobs posted by a specific LinkedIn profile.

| Param | Type | Required |
|---|---|---|
| `profileUrn` | string | ✅ |
| `start` | int | ❌ (default: 0) |
| `count` | int | ❌ (default: 25) |

---

## SEARCH ENDPOINTS

### GET `/api/v1/search/jobs`
Search LinkedIn jobs **version 2** — comprehensive filters. Prefer over `jobs/search` for complex queries.

| Param | Type | Notes |
|---|---|---|
| `keyword` | string | Search keyword |
| `start` | int | Pagination (increment by 25, default: 0) |
| `count` | int | Results per page (default: 25, max: 50) |
| `sortBy` | string | `relevance` (default) or `date_posted` |
| `datePosted` | string | `24h`, `1week`, `1month` |
| `experience` | string | `internship`, `entry_level`, `associate`, `mid_senior`, `director`, `executive` |
| `jobTypes` | string | `full_time`, `part_time`, `contract`, `temporary`, `internship`, `volunteer`, `other` |
| `workplaceTypes` | string | `onsite`, `remote`, `hybrid` |
| `salary` | string | `20k`, `30k`, `40k`, `50k`, `60k`, `70k`, `80k`, `90k`, `100k` |
| `companies` | string | Company IDs comma-separated |
| `industries` | string | Industry IDs comma-separated |
| `locations` | string | LinkedIn geo IDs comma-separated |
| `functions` | string | Job function codes (e.g. `it,sales,eng`) |
| `titles` | string | Job title IDs |
| `Benefits` | string | `medical_ins`, `dental_ins`, `vision_ins`, `401k`, `pension`, `paid_maternity`, `paid_paternity`, `commuter`, `student_loan`, `tuition`, `disability_ins` |
| `commitments` | string | `dei`, `environmental`, `work_life`, `social_impact`, `career_growth` |
| `easyApply` | bool | `true`/`false` — LinkedIn Easy Apply only |
| `verifiedJob` | bool | Verified postings only |
| `under10Applicants` | bool | Jobs with fewer than 10 applicants |
| `fairChance` | bool | Fair chance employers only |

---

### GET `/api/v1/search/people`
Search for LinkedIn professionals.

| Param | Type | Notes |
|---|---|---|
| `keyword` | string | Free text search |
| `start` | int | Pagination (default: 0) |
| `count` | int | Per page (default: 20, max: 50) |
| `firstName` | string | First name filter |
| `lastName` | string | Last name filter |
| `title` | string | Job title filter (e.g. `founder`) |
| `currentCompany` | string | Current company ID(s) comma-separated |
| `pastCompany` | string | Past company ID(s) comma-separated |
| `geoUrn` | string | Geo URN(s) from `geos/name-lookup` |
| `industry` | string | Industry ID(s) comma-separated |
| `school` | string | School ID(s) comma-separated |
| `profileLanguage` | string | Language code (e.g. `en`) |
| `serviceCategory` | string | Service category ID |

Returns: `[]{urn, publicIdentifier, firstName, lastName, headline, profilePictureURL, location}`

---

### GET `/api/v1/search/companies`
Search for LinkedIn companies.

| Param | Type | Notes |
|---|---|---|
| `keyword` | string | Company name/keyword |
| `start` | int | Pagination (default: 0) |
| `count` | int | Per page (default: 25, max: 50) |
| `geoUrn` | string | Geo URN(s) comma-separated |
| `companySize` | string | `1-10`, `11-50`, `51-200`, `201-500`, `501-1000`, `1001-5000`, `5001-10000`, `10001+` |
| `hasJobs` | bool | Filter companies with active jobs |
| `industry` | string | Industry ID(s) comma-separated |

---

### GET `/api/v1/search/posts`
Search LinkedIn posts with filters.

| Param | Type | Notes |
|---|---|---|
| `keyword` | string | Search term |
| `start` | int | Pagination (default: 10) |
| `sortBy` | string | `relevance` (default) or `date_posted` |
| `authorCompany` | string | Company ID of post author |
| `authorIndustry` | string | Industry ID of post author |
| `authorJobTitle` | string | Job title of author (e.g. `founder`) |
| `contentType` | string | `videos`, `photos`, `jobs`, `liveVideos`, `documents`, `collaborativeArticles` |
| `datePosted` | string | `past-24h`, `past-week`, `past-month`, `past-year` |
| `fromMember` | string | Profile URN of author |
| `fromOrganization` | string | Company ID(s) comma-separated |
| `mentionsMember` | string | Profile URN mentioned in posts |
| `mentionsOrganization` | string | Company ID(s) mentioned comma-separated |

---

### GET `/api/v1/search/services`
Search LinkedIn service providers.

| Param | Type | Notes |
|---|---|---|
| `keyword` | string | Service keyword |
| `start` | int | Pagination (default: 0) |
| `count` | int | Per page (default: 25, max: 50) |
| `geoUrn` | string | Geo URN(s) comma-separated |
| `profileLanguage` | string | Language code (e.g. `en,ch`) |
| `serviceCategory` | string | Service category ID(s) comma-separated |

---

### GET `/api/v1/search/schools`
Search LinkedIn educational institutions.

| Param | Type | Notes |
|---|---|---|
| `keyword` | string | School name |
| `start` | int | Pagination (default: 0) |
| `count` | int | Per page (default: 25, max: 50) |

---

## POSTS ENDPOINTS

### GET `/api/v1/posts/featured`
Featured posts pinned to a LinkedIn profile.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ |

---

### GET `/api/v1/posts/all`
All posts by a profile, paginated.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ |
| `cursor` | string | ❌ (pagination) |
| `start` | int | ❌ (default: 0) |

---

### GET `/api/v1/posts/info`
Single post details.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ |

Returns: `text, author, postedAt, likesCount, commentsCount, sharesCount, mediaURL`

---

### GET `/api/v1/posts/comments`
Comments on a post, paginated.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ |
| `start` | int | ❌ |
| `count` | int | ❌ (default: 10) |
| `cursor` | string | ❌ |

---

### GET `/api/v1/posts/likes`
Likes/reactions on a post.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ |
| `start` | int | ❌ (default: 0) |

---

## COMMENTS ENDPOINTS

### GET `/api/v1/comments/all`
All comments made by a LinkedIn profile, paginated.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ |
| `cursor` | string | ❌ |

---

### GET `/api/v1/comments/likes`
Likes on specific comments by URN(s).

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ (comma-separated URNs) |
| `start` | int | ❌ (default: 0) |

---

## ARTICLES ENDPOINTS

### GET `/api/v1/articles/all`
All LinkedIn articles published by a profile, paginated.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ |
| `start` | int | ❌ (default: 0) |

---

### GET `/api/v1/articles/article/info`
Article details from a full LinkedIn article URL.

| Param | Type | Required |
|---|---|---|
| `url` | string | ✅ (full URL e.g. `https://www.linkedin.com/pulse/...`) |

---

### GET `/api/v1/articles/article/reactions`
Reactions on a LinkedIn article.

| Param | Type | Required |
|---|---|---|
| `urn` | string | ✅ (article/thread URN from article/info) |
| `start` | int | ❌ (default: 0) |

---

## LOOKUP ENDPOINTS

### GET `/api/v1/geos/name-lookup`
Search locations — get `geoUrn` IDs for people/company search filters.

| Param | Type | Required |
|---|---|---|
| `query` | string | ✅ (e.g. `San Francisco`) |

---

### GET `/api/v1/g/title-skills-lookup`
Search for job title and skill IDs for advanced search.

| Param | Type | Required |
|---|---|---|
| `query` | string | ✅ |

---

### GET `/api/v1/g/services-lookup`
Search service category IDs.

| Param | Type | Required |
|---|---|---|
| `query` | string | ✅ |

---

## SERVICES ENDPOINTS

### GET `/api/v1/services/service/details`
LinkedIn service page details by vanity name.

| Param | Type | Required |
|---|---|---|
| `vanityname` | string | ✅ |

---

### GET `/api/v1/services/service/similar`
Similar LinkedIn services by vanity name.

| Param | Type | Required |
|---|---|---|
| `vanityname` | string | ✅ |

---

## SYSTEM

### GET `status/`
API health check. No authentication required.

```bash
curl -s "https://linkdapi.com/status/"
```

---

## Response Envelope

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Data retrieved successfully",
  "errors": null,
  "data": { "..." }
}
```

Error:
```json
{
  "success": false,
  "statusCode": 404,
  "message": "Profile not found",
  "errors": "...",
  "data": null
}
```

---

## SDK Usage

### Python (pip install linkdapi)

```python
from linkdapi import LinkdAPI, AsyncLinkdAPI

# Sync
client = LinkdAPI("YOUR_KEY")
profile = client.get_profile_overview("ryanroslansky")

# Async (40x faster for batch)
import asyncio
async with AsyncLinkdAPI("YOUR_KEY") as api:
    urn_data = await api.get_profile_urn("ryanroslansky")
    urn = urn_data['data']['urn']
    overview, experience, skills = await asyncio.gather(
        api.get_profile_overview("ryanroslansky"),
        api.get_full_experience(urn),
        api.get_skills(urn),
    )
```

### Node.js (npm install linkdapi) — requires Node 18+

```js
import { LinkdAPI } from 'linkdapi';
const api = new LinkdAPI({ apiKey: 'YOUR_KEY' });

const overview = await api.getProfileOverview('ryanroslansky');
const company = await api.getCompanyInfo({ name: 'google' });

// Batch concurrent
const [employees, similar, jobs] = await Promise.all([
  api.getCompanyEmployeesData(companyId),
  api.getSimilarCompanies(companyId),
  api.getCompanyJobs([companyId]),
]);
```

---

## Rate Limits & Credits

- Free tier: **100 credits** on signup (https://linkdapi.com/?p=signup)
- Most endpoints: **1 credit** per call
- `profile/full`: higher cost (multiple endpoints in one)
- HTTP `429` → wait and retry with exponential backoff
- Retry config in Python SDK: `max_retries=3, retry_delay=1.0` (exponential)

---

*Python SDK: https://github.com/linkdAPI/linkdapi-SDK*  
*Node SDK: https://github.com/linkdAPI/linkdapi-node-sdk*  
*Go SDK: https://github.com/linkdAPI/linkdapi-go-sdk*  
*Docs: https://linkdapi.com/docs*  
*API Spec: https://linkdapi.com/apispec.yml*
