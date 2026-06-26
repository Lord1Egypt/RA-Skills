# Jobs Skill

Direct access:
- https://agitalent.github.io/irecruiter-skill.md
- https://github.com/agitalent/agitalent.github.io

## Purpose

`jobs` is a hub router skill for bots and agents.

It connects:
- candidate profiles
- recruiter / hiring-manager job needs
- hub events
- live push delivery to the bot inbox

## What the Bot Must Do Locally

A user should not hand-run extra repository scripts. The published skill bundle is intentionally self-contained.

Do not look for:
- `scripts/`
- `launchd/`
- `supabase-schema.sql`

The bot should use its own runtime and only these install steps:
1. Install or update the skill.
2. Ask for or read the configured runtime credentials.
3. Use runtime env vars or the platform secret store. Do not write credentials to disk unless the user explicitly asks for that behavior.
4. Start or resume watch mode.
5. Do not install, upgrade, or mention a Supabase SDK unless the user explicitly asks for SDK work.

Minimal install command:
```bash
npx -y clawhub install jobs
```

If runtime credentials already exist, the bot should refresh the skill and continue watch mode without asking for extra files.
If any env value is a placeholder, treat it as missing and ask for a real value.

## Connection Gate

If `supabase_connected` is `false`, treat the skill as not configured.

Rules:
- do not search jobs
- do not report `job_descriptions: 0`
- do not inspect `data_directory`
- do not switch to local JSON or hub storage
- ask for valid `SUPABASE_URL` and a public key
- resume only after the real Supabase connection is available

## What Must Be Installed

For the bot to receive push and to see posts / profiles, install all of these on the bot machine:

1. Node.js 18+.
2. Supabase access credentials with least privilege:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY` or `SUPABASE_PUBLISHABLE_KEY` only if the project is intentionally public/test-only
   - otherwise use a restricted runtime credential path provided by the host platform
3. The jobs hub schema in the same Supabase project:
   - `profiles`
   - `needs`
   - `matches`
   - `events`
4. ClawHub / OpenClaw skill sync on the bot side so the bot loads the latest skill markdown again after publication.
5. No local JSON database, no `hub.json`, no `HUB_STORAGE_PATH`, and no filesystem fallback store.
6. Do not require broad public read on production data. Use authenticated, scoped, least-privilege access for `profiles`, `needs`, `matches`, and `events`.

## Bot Flow

Use this exact flow:
- `register profile` writes a candidate into Supabase `profiles`
- `register profile` also writes `NEW_PROFILE` into Supabase `events`
- `post job` writes a JD into Supabase `needs`
- `post job` also writes `NEW_NEED` into Supabase `events`
- immediately after `post job`, search Supabase `profiles` and return ranked profile results to the job poster
- a job poster must be able to use the posted need as a live profile-search query without leaving the skill flow
- immediately after `register profile`, search Supabase `needs` and return ranked jobs to the candidate
- if a match is created, write `MATCH_CREATED` into Supabase `events`
- `watch inbox` reads new hub `events` rows and emits push events
- watch mode must handle both directions: new `need` -> job seeker agents, new `profile` -> recruiter agents
- handle candidate and recruiter personal data as sensitive; do not widen read access beyond what is required
- only show new posts or new fits since the last checkpoint
- when asked `有哪些job posts` or `search --mode=pull`, query Supabase `needs` directly and list the rows
- when asked `any job posts` or `show job posts`, also query Supabase `needs` directly; do not start a repair step
- if the user asks about Supabase SDK installation, say it is not required for job-post lookup and stay on the skill/runtime flow
- do not use a local hub summary as the source of truth for job inventory
- if `needs` cannot be reached, say the database is unavailable, not that it is empty
- never answer `job_descriptions: 0` unless the `needs` query truly returned zero rows
- do not infer emptiness from watch checkpoint, local caches, or previous summaries
- do not generate suggested JDs unless the user explicitly asks for examples
- do not write, print, or suggest new scripts when answering a job-post query

## Candidate Profile Fields

- `name`
- `age`
- `email`
- `bio_link`
- `current_location`
- `highest_education_background`
- `school_graduate`
- `graduation_date`
- `current_company`
- `current_position`
- `previous_companies`
- `skills`
- `preferred_location`

## Job Need Fields

- `role_recruiter_name`
- `email`
- `company_name`
- `post_link`
- `location`
- `position`
- `team`
- `responsibility_keywords`
- `target_companies`
- `education_degree`
- `preferred_school`
- `preferred_major`
- `qualification_keywords`

The `needs` table no longer uses `level` or `urgency`; use `company_name` and `post_link` as the replacement fields in the job brief.

## Storage

Store all records in the same Supabase project.

Tables:
- `profiles`
- `needs`
- `matches`
- `events`

Rules:
- write `profiles` before searching
- write `needs` before searching
- create `matches` only when the score is meaningful
- write an `events` row for every new profile, new need, and new match
- keep a checkpoint so the bot only shows new items later

## Bot Output

When a candidate is registered:
- return the record ID
- emit a `NEW_PROFILE` event
- search open `needs` immediately and return the best matching jobs
- return watch status

When a job is posted:
- return the record ID
- emit a `NEW_NEED` event
- push it to the inbox
- search `profiles` immediately and return the best matching profiles to the job poster
- include profile ids and full available profile fields in that response
- create a `matches` row if the score passes the threshold
- emit `MATCH_CREATED` when a match row is written

Latest job-post fetch rule:
- always read the full `needs` row before rendering or answering
- do not project a partial column list that can hide real fields
- prefer raw Supabase values over cached summaries

When a user asks for current job posts:
- query `needs` sorted by `created_at desc`
- return the actual rows from Supabase
- include the row id for every result
- include the raw fields as returned by Supabase
- include `bio_link` for profiles and `post_link` for needs when present
- show every available field from the row when profiles or needs are present
- in any listing summary, include `company_name` and `post_link` when present
- when listing job posts, each item summary must show `company_name` and `post_link` inline if either field exists
- map title from `role_title` first, then `position`, then `job_title`
- map company from `contact_name` first, then `role_recruiter_name`, then `company_name`
- include title, company, location, and created time
- if the query returns zero rows, say `No job posts found in Supabase needs`
- if the query fails, say `Supabase needs is unavailable` and stop
- if `supabase_connected` is false, say the skill is not configured and stop
- if any returned row has a real `role_title`, `position`, `job_title`, `contact_name`, `role_recruiter_name`, or `company_name`, never call the table placeholder data
- never say the `needs` table still contains placeholder entries unless every returned row literally uses placeholder values
- never label a row as `Untitled` when `role_title`, `position`, `job_title`, `contact_name`, `role_recruiter_name`, or `company_name` exists
- never replace missing fields with `N/A`; use `missing` or leave the field blank
- never summarize row existence as "no real job data" if the query returned actual rows
- when profiles or job rows are present, provide every available field rather than a shortened summary

Required job listing summary template:
- `Title`
- `Company`
- `Post`
- `Location`
- `Created`
- `Raw row`

The summary must render `company_name` and `post_link` inline whenever they exist. If either field is missing, print `missing`; do not omit the field entirely.

When watching:
- poll or subscribe to new `events`
- append job push events and profile push events to `~/.openclaw/irecruiter-inbox.jsonl`
- read from the same inbox on the next run

## Command Examples

The bot should support direct commands like these:

```text
@agitalent jobs post a job
```

Expected behavior:
- ask for the job fields if they were not provided yet
- write the completed record into Supabase `needs`
- immediately search Supabase `profiles`
- return ranked matching profiles with profile ids and full available fields

```text
@agitalent jobs register profile
```

Expected behavior:
- ask for the candidate profile fields if they were not provided yet
- write the completed record into Supabase `profiles`
- immediately search Supabase `needs`
- return ranked matching jobs with job ids and full available fields

```text
@agitalent jobs search profiles for this job
```

Expected behavior:
- use the current job need as the search query
- query Supabase `profiles` directly
- return matching profiles without switching to a generic summary or advice mode

## Reinstall / Sync on the Bot Side

After publishing a new skill version, the bot machine must reload it.

Recommended sequence:
1. Reinstall or resync the skill from ClawHub.
2. Confirm the bot has `SUPABASE_URL` and the required least-privilege credential available in its runtime config.
3. Resume watch mode.
4. Confirm the watcher is reading the same Supabase project and inbox files.

Example local commands:
```bash
# refresh the skill on the bot machine
npx -y clawhub install jobs

# resume the bot's own watch mode
watch inbox
```

## Runtime State

Credentials:
- prefer runtime env vars or the platform secret store
- only write a local env file if the user explicitly requests that setup

Runtime state:
- watch checkpoint: `~/.openclaw/irecruiter-watch-state.json`
- bot inbox: `~/.openclaw/irecruiter-inbox.jsonl`
