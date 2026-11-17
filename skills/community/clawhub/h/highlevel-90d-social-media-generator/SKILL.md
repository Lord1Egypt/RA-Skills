---
name: "90-day-social-generator"
description: "Generate a 90-day social media calendar (HL Social Planner CSV): pulls the client's sitemap for link-back URLs and post topics, AI writes posts + images per client, with or without HighLevel connection. Requires HighLevel to import, AI model for content, image API + SSH/FTP host for image uploads."
---

# 90-Day Social Media Calendar Generator

Generate a full 90-day social media calendar for any client: post copy, one
linking URL per post, and one AI-generated image per post. Output is a CSV in
HighLevel Social Planner import format.

## How it knows what to post

The client's **sitemap** is the source of truth. The pipeline fetches
`<domain>/sitemap.xml`, filters out junk pages (about, sitemap, terms,
privacy, contact, faq, login, cart, blog index, etc.), and keeps the
service, area, and blog post pages. Individual blog posts are included as
valid link-back targets and post topics, only the blog index and pagination
pages are dropped. Each post then links back to one of those real pages,
and the post content is written around that page's topic. No sitemap, no
posts: the URLs and what to post come straight from the client's own site.

## Tested and working

- Content API: DeepSeek and ChatGPT (OpenAI) both tested for post and image-prompt generation
- Image API: DeepSeek, ChatGPT, Gemini, and FAL tested for image generation
- Pipeline: tested end to end (sitemap fetch, post generation, CSV output, SSH upload)

## Requirements

- **HighLevel CRM** - the finished CSV is imported into a client's HighLevel
  Social Planner. You need a HighLevel account to use the output.
- **An AI model API key** for post content and image prompts (DeepSeek,
  OpenAI, ChatGPT, or any OpenAI-compatible provider)
- **An image API key** (Gemini free tier, FAL, or Kling) for images
- **FTP or SSH access to a web host** so the package can upload the generated
  images and write real public URLs into the CSV `imageUrls` column
  (`--ssh-host/--ssh-user/--ssh-key` or `--ftp-host/--ftp-user/--ftp-pass`)
- Optional: a HighLevel API key, ONLY for Mode A (auto-fetch client details)

## Quick start

```bash
./run.sh --details "Company Name|website.com|City|ST|Business Category|Company description" \
  --llm-key sk-...
```

Output: `output/<domain>-social-90d.csv` (HighLevel Social Planner import).

Using a ChatGPT/OpenAI key instead of DeepSeek:

```bash
./run.sh --details "Company Name|website.com|City|ST|Business Category|Company description" \
  --llm-key sk-you…-key \
  --llm-model gpt-4o-mini \
  --llm-base https://api.openai.com/v1/chat/completions
```

## Two ways to provide client details

- **Mode A (HL-connected):** `./run.sh --email client@example.com` - pulls the
  contact + custom fields from your HighLevel subaccount. The ONLY env var in
  the package, `HIGHLEVEL_ACCESS_TOKEN`, is used here.
- **Mode B (no HighLevel):** `./run.sh --details "..."`,
  `./run.sh --client-json file.json`, or just `./run.sh` (interactive: it asks
  for each client detail one question at a time). Hand over client details
  directly and still get the importable CSV. No env vars needed.

## Pipeline

1. Client details (either mode) -> normalized client JSON
2. Sitemap -> filtered page list from the client's site
3. Posts -> LLM writes the calendar (45 posts, every other day, 9am, one URL
   per post, no emojis, hashtags)
4. Images (optional) -> one image per post, uploaded to your web host over
   SSH or FTP, public URLs written into the CSV `imageUrls` column
5. Import the CSV into the client's HighLevel Social Planner

See README.md for the full flag reference.
