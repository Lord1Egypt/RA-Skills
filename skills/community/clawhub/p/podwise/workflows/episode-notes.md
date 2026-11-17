# Podwise Episode Notes

Use this skill to turn a single processed episode into a well-structured, portable note. It pulls every available AI artifact from Podwise and assembles them into one document shaped for long-term reference — not just a quick read.

## Goals

1. Verify the Podwise MCP connection.
2. Identify the target episode from the user's input.
3. Ensure the episode is processed; if not, ask for confirmation before processing.
4. Fetch all available AI artifacts for the episode.
5. Assemble a structured markdown note.
6. Write the note to a file and guide the user on how to import it into their PKM tool.

## Step 1: Check the Environment

Call `get_me`. If the Podwise tools are unavailable or return an authentication error, stop and follow [../references/installation.md](../references/installation.md) before continuing.

## Step 2: Load the Listener Taste

Look for `taste.md` in the current working directory.

- If found, read the **PKM tool** and **Output Preferences** fields silently. Use these to shape the note format and to give accurate export instructions in Step 7.
- If not found, proceed with default formatting and generic export instructions.

## Step 3: Identify the Target Episode

The user may provide the episode in several ways:

- A Podwise episode URL: `https://app.podwise.ai/dashboard/episodes/{seq}` — extract the trailing integer as `seq`.
- A YouTube URL: `https://www.youtube.com/watch?v=...`
- A Xiaoyuzhou URL: `https://www.xiaoyuzhoufm.com/episode/...`
- A local audio or video file path: `./recording.mp3`
- An episode title or keyword — in this case, search first:

  - `search_episodes` with `query: "{title or keyword}"`

Present the results and ask the user to confirm which episode they want before continuing.

If the user provides a YouTube, Xiaoyuzhou, or local file input, that content must be processed before artifacts can be fetched. Move to Step 4 immediately.

## Step 4: Ensure the Episode Is Processed

For a Podwise episode seq, attempt to fetch the summary to check if processing is complete:

- `get_episode_summary` with the episode `seq`.

- If this succeeds, the episode is already processed. Skip to Step 5.
- If this returns an error indicating the episode is not yet processed, tell the user and ask for confirmation before processing:

> "This episode hasn't been processed yet. Processing will use one credit from your Podwise quota. Proceed?"

Only after explicit confirmation, start processing:

- Podwise episode: `process_episode` with the `seq`.
- YouTube / Xiaoyuzhou: `import_episode` with the URL to get a `seq`, then `process_episode`.
- Local file: `start_audio_upload` → upload bytes to the returned `uploadUrl` (or hand the `browserUploadUrl` to the user) → `complete_audio_upload`.

Processing runs asynchronously. Poll `get_episode` with the `seq` until it is done, then continue. The `seq` is used for all subsequent calls.

Supported local file types: `.mp3 .wav .m4a .mp4 .m4v .mov .webm`.

## Step 5: Fetch All AI Artifacts

Call `get_episode_summary` with the episode `seq`. This single call returns the overview, key takeaways, chapters, highlights, Q&A, keywords, and mind map.

If an individual section is missing, mark that artifact as unavailable in the note rather than stopping the whole skill.

Optionally fetch the transcript if the user specifically requested it or if their taste profile indicates they prefer full transcripts:

- `get_episode_transcript` with the episode `seq` (paginate with `limit` / `offset`).

Do not include the full transcript in the note by default — it is too long for most PKM use cases. Offer it as a separate file if the user wants it.

If the user asked for subtitles, call `export_episode_srt` with the episode `seq` instead of building SRT from transcript segments. Short files return inline; long ones return a download link valid for 10 minutes — share the link.

## Step 6: Assemble the Note

**Rendering options:** The server can render a standard note directly — call `export_episode_markdown` with `dialect` set to match the user's PKM (`obsidian`, `logseq`, or `common`) and write the returned text to disk. Use the manual assembly below when the user wants the Q&A and mind-map sections, a trimmed note, or a format the server export does not cover.

Combine all fetched artifacts into a single markdown document using this structure:

---

```markdown
# {Episode Title}

**Podcast**: {Podcast Name}
**Published**: {publication date}
**Source**: {episode-url}
**Processed**: {date note was generated}

---

## Summary

{Content from `get_episode_summary` overview + takeaways}

---

## Chapters

{Chapters section, formatted as a numbered list with timestamps if available}

---

## Highlights

{Highlights section, formatted as a bulleted list}

---

## Q&A

{Q&A section, formatted as question/answer pairs}

---

## Keywords

{Keywords section, formatted as a comma-separated inline list or tag-style list depending on user's PKM tool}

---

## Mind Map

{Mind map section, rendered as a nested bullet list if the raw output is a tree structure}

---

_Note generated by podwise-episode-notes · {date}_
_Source: {episode-url}_
```

---

Rules for assembling the note:

- Omit any section where the artifact was unavailable — do not show empty section headers.
- Keep the Summary section as returned without paraphrasing or shortening it.
- Highlights should remain verbatim — do not rewrite them.
- If the mind map returns structured data rather than plain text, convert it to a nested markdown bullet list before inserting it.
- If the user's taste profile specifies a preferred output format (bullet points vs prose), apply it only to synthesized sections — do not alter verbatim artifacts.

## Step 7: Write the File and Guide Export

Name the file using the pattern: `{podcast-name}-{episode-slug}-notes.md`

Slugify by lowercasing, replacing spaces with hyphens, and stripping special characters. Example:
`lex-fridman-podcast-elon-musk-notes.md`

Write the file to the current working directory unless the user specifies another path.

If the user's PKM tool is Notion or Readwise and the integration is connected in Podwise settings, you may offer to push directly:

- `send_episode` with the `seq` and `target: "notion"` or `target: "reader"`.

Otherwise, tell the user where the file was saved and provide import instructions based on their PKM tool from the taste profile:

**Notion**
> Drag the `.md` file into any Notion page, or use Notion's "Import" option (File → Import → Markdown & CSV). The headings will map to Notion's heading blocks automatically.

**Obsidian**
> Move the file into your vault folder. It will appear immediately in Obsidian's file explorer. All internal `[[links]]` you add later will connect to it like any other note.

**Logseq**
> Place the file in your Logseq `pages/` directory. Logseq will index it on next open. The `## Highlights` section works well as block references.

**Readwise**
> Use Readwise's manual highlight import or the Readwise Reader upload feature. Note that Readwise is optimised for highlights rather than full notes — consider importing just the Highlights section.

**No PKM tool in taste profile / unknown**
> The note is saved as a plain markdown file at `{path}`. You can open it in any text editor, import it into most note-taking apps, or keep it as a standalone reference.

## Common Failure Cases

- If the episode search returns no results, ask the user to try a different title, keyword, or to paste the episode URL directly.
- If processing fails due to an unsupported file format, stop and list the supported extensions: `.mp3 .wav .m4a .mp4 .m4v .mov .webm`.
- If the user provides a URL that is neither a valid Podwise, YouTube, Xiaoyuzhou, nor local path, tell them the URL format is not recognised and ask for a supported input.
- If `get_episode_summary` still fails after a successful process, tell the user that processing may still be completing and to try again in a few minutes.
- If a note file with the same name already exists, ask the user whether to overwrite it or save with a timestamp suffix.

## Output Contract

Produce exactly one markdown note file per episode.

The note must include at minimum: Summary, Highlights, and the source URL. All other sections are included when available.

The transcript is never included in the note by default — offer it separately only if requested.

Always confirm the file path after writing and always provide PKM import instructions.
