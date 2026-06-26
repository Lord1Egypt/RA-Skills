---
name: meeting-minutes-retriever
description: Read meeting minutes or notes from a local file path or URL, or inspect a local meeting-notes directory and report the file count plus file list. Use when the user asks about meetings, notes, minutes, conclusions, decisions, action items, what was discussed, or how many meeting-note files exist in a folder, and the content lives in a file, a directory, or a web document such as a Feishu link. If no path, directory, or URL is available in the conversation, ask the user for one before proceeding.
---

# Meeting Minutes Retriever

Use this skill to fetch raw meeting text first, then answer the user's question from that text.
Use the directory lister when the user wants counts or file listings instead of reading one document body.

## Trigger Rules

Use this skill when:

- The user asks about meeting notes, meeting minutes, meeting conclusions, decisions, action items, owners, blockers, or what was discussed.
- The user asks how many meeting-note files exist, which files exist, what the directory contains, or asks for a meeting-note file list.
- The answer depends on a meeting record stored in a local text file, a local directory, or a URL.
- The user refers to a Feishu document link as the source of the meeting content.

Do not use this skill when:

- The user already pasted the full meeting text into the chat and only wants summarization or Q and A on that pasted text.
- The request is general knowledge and does not depend on a meeting record.
- The user explicitly says not to open files or URLs.

## Workflow

1. Check the conversation for a meeting-notes location.
2. Accept either:
   - a local file path such as `D:\docs\meeting.txt`
   - a local directory path such as `D:\docs\meetings`
   - a URL such as `https://...`
3. If no location is available, stop and ask: `Please send the local file path, directory path, or Feishu link for the meeting notes.`
4. Resolve skill resources relative to the skill directory that contains this `SKILL.md`.
5. If the user asks for counts, directory contents, file totals, or file lists, use `scripts/list_meeting_files.py`.
6. If the user asks about the contents of one meeting record, use `scripts/read_meeting_data.py` or the same logic to read the content into a single string.
7. If the script result starts with `ERROR:`, show that error to the user and ask for a corrected path, directory, or URL.
8. If the directory listing succeeds, answer with the count and the file list.
9. If the file read succeeds, read the full raw text and answer the original question from that source text.

## Rules

- Do not parse, summarize, classify, or structure the document inside the reader tool.
- Do not assume file type from the extension. Just attempt to read it as text.
- Treat Feishu links as best-effort URLs only. Direct requests may fail for login-protected, permission-gated, or JavaScript-rendered Feishu pages.
- Keep the tool interface stable as `read_meeting_data(location)`.
- Future Feishu API logic should be added inside the same reader function without changing its argument shape.
- Keep the directory tool interface stable as `list_meeting_files(location, recursive=False)`.
- Prefer the directory tool for requests containing words such as `多少`, `几个`, `数量`, `列表`, `目录`, `有哪些文件`, `file count`, or `list files`.

## Tool Contract

Implement a function named `read_meeting_data(location)` with this behavior:

- Local path:
  - Resolve to an absolute path.
  - Try multiple text encodings before failing.
  - Return the file contents as a string.
- URL:
  - Fetch with a basic timeout on a best-effort basis.
  - Return the response text as a string.
- Errors:
  - Return human-readable error strings starting with `ERROR:`.

Implement a function named `list_meeting_files(location, recursive=False)` with this behavior:

- Local directory:
  - Resolve to an absolute path.
  - Detect the current OS and use an OS-appropriate system command first.
  - Return a JSON string containing `directory`, `total_files`, and `files`.
- File filtering:
  - Count supported meeting-note files only: `.md` and `.txt`.
- Errors:
  - Return human-readable error strings starting with `ERROR:`.

## Resource

- Reader script: `scripts/read_meeting_data.py` relative to this skill directory
- Directory lister script: `scripts/list_meeting_files.py` relative to this skill directory
