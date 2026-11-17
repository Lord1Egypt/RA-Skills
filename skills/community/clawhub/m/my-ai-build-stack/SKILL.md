---
name: my-ai-build-stack
description: "Set up a new project the same way every time, in plain words, with any stack you choose. Tell your AI agent what you want to build, pick your builder, database, hosting, version control, and judge, or use the default example stack, and get a full setup plan. Default example stack: Claude Code to build, Supabase to store data, Netlify to host, GitHub to keep versions, and Muse to judge the work. Setup plan with file list, database tables, deploy steps, review steps, and choose a piece notes for each piece, ready to brief any AI builder, or a human developer."
---

# My AI Build Stack

## Headline

Set Up a New Project the Same Way Every Time, in Plain Words

## Hook

Tell your AI agent what you want to build. Pick your stack, or use the default example stack. Answer a few questions. Get a full setup plan for your chosen stack, ready to review.

## Pain, in plain words

Most new projects start in a different way every time. One app uses one database, the next app uses another one, the hosting is different, the files are in a different place, and no one remembers how the last app was built. When something breaks, no one knows where to look. The fix is not a new tool. The fix is one stack, used the same way every time, with a plan you can check before anything is built.

## What you get

A setup plan for a new project, made for your project only, for any stack you choose. The plan names your chosen stack, lists the files, lists the database tables, lists the deploy steps, and lists the review steps. It gives you draft setup work to review, never a live change by itself.

## Who this is for

Founders with no code, who want to start a new app or website the same way every time, in plain words, with any stack. Small business owners who want one clear stack to hand to a builder. Freelancers and builders who need a clear setup plan, with files, tables, deploy, and review in it.

## Why this saves money

Starting the same way every time is cheaper than starting from zero every time. A clear plan stops the builder from picking a new tool for every project, rebuilding the database, or deploying in a way no one can repeat.

## Technical, for coders

Structured setup plan for any stack: builder, database, hosting and deployment, version control, and architecture and quality judge, all chosen by the owner. Default example stack is Claude Code as builder, Supabase as database, Netlify as hosting and deployment, GitHub as version control, and Muse as architecture and quality judge. File list, database table list with columns, deploy steps with cache and build checks, and a review checklist, ready to brief any AI builder, or a human developer. No guarantee of users, speed, or money, and no claim that a plan alone makes an app work. The plan is a draft for owner review, not a live change.

## Purpose

Set up a new project from any stack you choose, the same way every time. The skill asks first, then plans. It does not create a repo, create a database, deploy, or publish anything by itself.

## The stack, in plain words

This is one stack, with five pieces. You choose the tool for each piece, or you say use the default. The default example stack is below, labelled Default example stack, not the only stack. The choose a piece notes are in the setup plan.

### Default example stack

### 1. Judge, default example Muse
The judge decides the plan, checks the work, and says what is right and what is wrong, in plain words. The judge does not write the code. The judge checks the builder's work, line by line, before anything goes live. Default example judge is Muse.

### 2. Builder, default example Claude Code
The builder writes the code, makes the files, and fixes what the judge flags. The builder is the worker. The builder does not decide the plan, and does not publish anything live by itself. Default example builder is Claude Code.

### 3. Version control, default example GitHub
Version control keeps every version of the code, in one place, with a record of what changed and when. If a change breaks the app, the old version is still there. The repo is the source of truth, not a file on one laptop. Default example version control is GitHub.

### 4. Database, default example Supabase
The database stores the data, in tables, with rules on who can see what and who can change what. It is the database for the app, not a spreadsheet, and not a file on a laptop. Default example database is Supabase.

### 5. Hosting and deployment, default example Netlify
Hosting puts the app on the web, so people can open it in a browser. A deploy makes a new live version. A deploy only happens when the owner says so, and only after the judge checks the work. Default example hosting is Netlify.

### How the pieces connect
The judge writes the plan. The builder builds from the plan, and puts the code in version control. The app reads and writes data in the database. Hosting takes the code from version control, or from a deploy file, and puts it live. The judge checks the live result, and the builder fixes what the judge flags. That loop repeats, plan, build, check, fix, deploy only on owner approval. With the default example stack, that is: Muse writes the plan, Claude Code builds, code goes in GitHub, data goes in Supabase, Netlify puts it live, Muse checks it, Claude Code fixes what Muse flags.

## How to use it

Fast path: If the user already gives project details and stack in their first message, do NOT force all 13 questions one at a time. Ask only the missing answers, in one short list, then in the SAME reply do the setup plan. If the user answers one question at a time, after the last answer, always finish with the full setup plan in that same reply, never stop at the questionnaire alone.

Step 1: ask the user these questions, one at a time, in plain words.
Step 2: set up the new project from the chosen stack below, step by step, with choose a piece notes for each piece.
Step 3: run the missing checks at the end, and list what is complete, missing, or not confirmed.

Ask these questions first, one at a time:
1. Which builder do you want, for example Claude Code, Cursor, ChatGPT, or another builder, or use the default, Claude Code?
2. Which database do you want, for example Supabase, PostgreSQL, Firebase, or another database, or use the default, Supabase?
3. Which hosting do you want, for example Netlify, Vercel, Azure, or another host, or use the default, Netlify?
4. What does your new app or website do, in plain words?
5. Who uses it, and what do they do first when they open it?
6. What are the main screens or pages, in plain words?
7. What data must it store, for example names, orders, notes, or bookings?
8. Who signs in, and who must never see private data?
9. Do you have a domain name yet, or is that Not confirmed?
10. What language must it use, English, Arabic, or both?
11. Is it used on a phone first, on a laptop first, or both?
12. Is the free tier enough to start, or is there a budget, in plain words?
13. Who will build it, an AI builder, a human developer, or you with help, and who will review it? If you already answered Question 1, use that answer here, and do not ask it again.

If the user does not know an answer, mark it Not confirmed, and use the most common answer for their app type, and say so. Do not invent an answer. If the user says use the default for a stack question, use the default example tool for that piece, and write Default used in the plan.

## Step 2: set up the new project, step by step

Do these steps in order. Each step is a draft for owner review. Do not create a repo, create a database, deploy, or publish anything without a separate approval from the owner. Use the chosen stack in every step, not the default example stack, unless the owner chose the default.

### Step 2.1: Name the project and the repo
Write the project name, in plain words, and the repo name, in lower case letters, with no spaces. If the owner has not confirmed a name, mark it Not confirmed, and use a working name, marked Suggested, not confirmed. Do not create the repo yet.

### Step 2.2: List the files
List the files the app needs, in plain words, with what each file does. Keep the list short: a home page, the main screens from Question 6, one file for the app logic, one file for the style, and one file for the settings. Add a file only if the owner confirms it is needed.

### Step 2.3: List the database tables
List the tables the app needs, in plain words, with the columns for each table. Keep it to the data from Question 7 only. Add a table only if the owner confirms it is needed. Do not create any table yet.

### Step 2.4: Set the data rules
For each table, write who can see it, who can change it, and who must never see it. Private data stays private. If a rule is not confirmed, mark it Not confirmed.

### Step 2.5: Set the deploy plan
Write how the app will go live on your chosen hosting, step by step: build the files, check the build, deploy only on owner approval, open the live link, and check it in a logged out browser. Do not deploy yet. With the default example stack, the host is Netlify.

### Step 2.6: Set the review plan
Write how your chosen judge will check the work: read the code, check the files, check the tables, check the live link, and list what is right and what must be fixed. No live link is called ready until the judge checks it. With the default example stack, the judge is Muse.

### Choose a piece notes, for each piece
If the owner wants to choose a piece, write the choice in the plan, with what changes and what stays the same. Do not choose a piece by yourself.
- Database choice: if the owner already uses another database, name it, and say what changes, the table list stays the same, the data rules stay the same, only the database tool changes. Common choices are PostgreSQL, Firebase, or MySQL, all marked Suggested, not confirmed, unless the owner confirms one. Default example is Supabase.
- Hosting choice: if the owner already uses another host, name it, and say what changes, the files stay the same, the deploy steps stay the same in plain words, only the host changes. Common choices are Vercel or Azure, both marked Suggested, not confirmed, unless the owner confirms one. Default example is Netlify.
- Version control choice: if the owner already uses another version control tool, name it, and say what changes, the file list stays the same, only where the versions are kept changes. Common choices are GitLab or Bitbucket, both marked Suggested, not confirmed, unless the owner confirms one. Default example is GitHub.
- Builder choice: if the owner uses another builder, for example Cursor or ChatGPT, name it, and say what changes, the plan stays the same, only who writes the code changes. Common choices are Cursor or ChatGPT, both marked Suggested, not confirmed, unless the owner confirms one. Default example is Claude Code.
- Judge choice: if another judge reviews the work, name the role, and say what changes, the review checklist stays the same, only who checks it changes. A builder must never judge its own work. Common choices are Muse, or a human reviewer, both marked Suggested, not confirmed, unless the owner confirms one. Default example is Muse.

## Extra checks

These are not part of the setup plan above, but report them separately as Notes. Do not mix them into the plan score.
- Cost: list what will cost money as users grow, for example database reads, or hosting, in plain words, with no invented price.
- Mobile: say if the app is used on a phone, and if the setup must work on a phone first.
- Language: say if Arabic is needed, and if the text must read right to left.
- Backup: say if the data needs a backup, and how often it must be checked, or Not confirmed.

## Hard rules

- Never mark Pass without evidence.
- Never invent a project name, a database, a table, a column, a hosting name, a domain, a price, a user number, or a client.
- Never claim a project is live unless it was deployed and checked in a logged out browser. A plan is not a live app.
- Never create a repo, create a database, create a table, deploy, or publish anything, without a separate approval from the owner.
- Suggested items must be marked Suggested, not confirmed.
- A setup plan is not a promise of users, speed, or money.
- Keep the plan in plain, short sentences. The owner may not be a technical reader.

## Setup plan format

Always finish with this format, in this order, labelled DRAFT, NOT LIVE, Owner approval needed:

### Setup plan: [project name]
### What it does: [plain words] | Users: [plain words] | Language: [English, Arabic, or both]

**Verdict: Ready to build / Needs decisions first / Not ready to build**

Use Ready to build only if the project name, the main screens, the tables, and the data rules are all confirmed. Otherwise use Needs decisions first, or Not ready to build if a blocker was found.

**The stack**

| # | Piece | Chosen tool | Default example | What it does |
|---|---|---|---|---|
| 1 | Judge | [chosen judge] | Muse | Decides the plan, checks the work |
| 2 | Builder | [chosen builder] | Claude Code | Writes the code, fixes what is flagged |
| 3 | Version control | [chosen version control] | GitHub | Keeps every version of the code |
| 4 | Database | [chosen database] | Supabase | Stores the data, in tables |
| 5 | Hosting | [chosen hosting] | Netlify | Puts the app on the web |

**Choose a piece notes**

- [Piece chosen, or Default used, with what changes and what stays the same, or Not confirmed]

**Files**

- [File name, what it does]

**Database tables**

| Table | Columns | Who can see it | Who can change it |
|---|---|---|---|
| [table name] | [columns, in plain words] | [user type] | [user type] |

**Deploy plan**

1. [Build the files]
2. [Check the build]
3. [Deploy only on owner approval]
4. [Open the live link in a logged out browser]
5. [Chosen judge checks the live result]

**Review plan**

- [Chosen judge reads the code, checks the files, checks the tables, checks the live link, lists what is right and what must be fixed]

**Owner steps, needs the client**

- [For example: confirm the project name]
- [For example: approve the table list before any table is made]
- [For example: approve the deploy, and the live link check]

**Notes**

- [Any note from the Extra checks section, or None.]

**What was not set up, and why**

- [For example: no repo was created, owner approval is needed.]

## Missing checks

After the plan, run these 9 checks, and list the result for each one:
1. Stack chosen by the owner, or default used, for all five pieces?
2. Project name confirmed by the owner, or marked Not confirmed?
3. Main screens or pages listed?
4. File list made?
5. Database table list made, with columns?
6. Data rules made, for each table?
7. Deploy plan made, with owner approval step?
8. Review plan made?
9. Choose a piece notes made, or marked Default used?

List the results as Complete, Missing, or Not confirmed. Do not add a missing item without owner approval.
