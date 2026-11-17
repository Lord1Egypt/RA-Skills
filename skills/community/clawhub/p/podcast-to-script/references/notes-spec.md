# Shownotes format spec (notes.md)

Every episode MUST have `notes.md` — it becomes the RSS description / platform show
notes. **Not optional.** The publish command refuses to run without `--notes`
(explicit `--no-notes` is the only bypass).

`notes.md` is **Markdown**, converted to HTML at publish time — podcast clients render
the description as HTML, and plain-text newlines collapse into one block. Follow
Markdown rules: blank line before lists, links must be real Markdown links.

## Template

```markdown
本期{导语}。一句话主线：{主线}

{配图，Markdown 图片语法，引用 TOS URL}

**内容速览**

- {要点 1：关键概念/论点}
- {要点 2：具名系统/数据点}
- ...

{可选：阅读推荐顺序，串讲类适用}

**时间轴**

- 00:00 段落名
- 02:16 段落名
- ...

**原文链接**

- [原文：{标题}]({source URL})
- [相关链接]({URL})
```

## Quality requirements

1. **Opening hook line**: one sentence on what this episode covers and why it's worth
   listening, followed by `一句话主线：{主线}`.
2. **Images** go after the hook, before 内容速览 (when the source has images).
3. **内容速览** is outline-style bullets — each a concrete point (key concept, named
   system, data point, conclusion), not vague chapter titles.
4. **时间轴** maps 1:1 to script segments, format `- MM:SS 段落名`; draft from char
   counts (260 chars/min), calibrate after synthesis with
   `scripts/generate_timeline.py --mp3 podcast.mp3 --script script.md --calibrate`.
5. **原文链接** last; fold related links into the same bullet with parentheses.
6. Chinese throughout (matching the show's language); keep technical terms in English.
7. Don't paste the full script — this is a short overview, not a transcript.
8. Timeline entries (e.g. `02:31 主题名`) become tappable jump links on Xiaoyuzhou —
   only include real timestamps, never invent them.
9. **Source images**: after downloading and uploading to TOS, reference the TOS URL with
   Markdown image syntax, placed near the related bullet. See `references/images-guide.md`.
   TOS path convention: `podcasts/episodes/{slug}/images/{filename}.jpg` (must match the
   publish script's actual upload path; URLs in notes.md must match TOS filenames
   character-for-character — no local numbering prefixes).
