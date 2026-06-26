# Pipeline Reference

Use this reference when the task is operational rather than editorial.

## Durable layers

1. `data/raw_transcripts`
   - timestamped source segments with uncertainty notes
2. `data/lessons`
   - normalized lesson JSON with summaries, conspects, vocabulary, grammar,
     pronunciation, drills, and tests
3. `docs/lessons`
   - learner-facing Markdown derived from lesson JSON
4. `exports/drive`
   - compact local export bundles that can be copied to a managed Drive mount
5. `references/course-data`
   - sanitized lesson bundle, lesson plans, HSK practice, and roleplay payloads
     included in the published GitHub/ClawHub skill artifact
6. `references/system-prompts`
   - public tutor prompt packs and the shared runtime contract mirrored from
     the public repo `prompts/system` directory

## Command Handling

- Use only commands documented by the checked-out source repo.
- Inspect the command implementation or project documentation before proposing
  execution.
- Present the exact command and wait for explicit user confirmation before
  running it.
- For video-only sources, stop in the published ClawHub skill and ask for a
  transcript/subtitle input or a source-repo-specific private workflow.
- For optional mounted-Drive sync, stop if the user has not supplied a trusted
  local mount path through `--drive-root`.

## Quality rule

- Extraction is allowed to be ugly.
- Editorial review is allowed to be slow.
- Publication is not allowed to leak.
- A published skill without `references/course-data` is not a valid release.
- A published skill without `references/system-prompts` is not a valid release.
- Missing audited commands are blockers. Do not improvise replacement network,
  Drive, transcription, media-extraction, or credential-discovery behavior.
