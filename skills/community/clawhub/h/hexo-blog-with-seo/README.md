# blog-hexo Skill

One skill for the entire Hexo workflow—draft ➝ polish ➝ deploy.

## Requirements
- Node.js + npm/npx installed (Hexo CLI).
- Hexo CLI configured in the repo.
- Local access to the Hexo blog repository path (ask if unknown).
- Git credentials/deploy tokens so `hexo deploy` can push to the remote.
- Permission to read/write Markdown and generated output.

## When to Use It
- **Draft mode** when you need to create or revise an unpublished post.
- **Publish mode** when a draft is ready for SEO polish and deployment.

## Draft Mode Steps
1. Confirm topic, target keywords, audience, tone, and word count.
2. Check memory/notes for the blog path. If unknown, ask the user.
3. Create the Markdown file at that path using the front matter template:
   ```
   ---
   title: ''
   published: false
   catalog: true
   header-img: /img/article_header/article_header.png
   date: YYYY-MM-DD HH:mm:ss
   subtitle:
   tags: []
   ---
   ```
4. Draft the content (intro, H2/H3 sections, conclusion). Capture TODOs inline if needed.
5. Optional preview: `npx hexo clean && npx hexo generate` (draft stays hidden because of `published: false`).
6. Update the user with status (in-progress vs. ready for review).

## Publish Mode Steps
1. Gather SEO inputs (target + secondary keywords, search intent, audience, tone, word count).
2. Apply the SEO framework: strong title/meta, keyword placement, scannable sections, snippet-ready answers, internal/external links, image suggestions.
3. Remove `published: false` when the post is ready to go live.
4. Run the Hexo pipeline:
   ```bash
   npx hexo clean
   npx hexo generate
   npx hexo deploy
   ```
5. Capture the deploy commit hash for status updates.
6. Summarize what was updated (sections rewritten, links added, etc.).

## Tips
- If a post should stay draft-only, leave `published: false` and skip the deploy step.
- Always double-check path + tags in memory before writing.
- Mention which mode you ran (draft or publish) in your notes so the user knows what happened.

## Preferred Tags
- AI
- OpenClaw
- Agent
- Technical
- Life
