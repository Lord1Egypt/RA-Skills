# Caption File Check reference

Read this reference before running the source-file preflight or comparison.

## Tool roles

`powmcp-caption-file-check:caption_check` preflights one frozen WebVTT, SRT, or TTML/IMSC caption file.

`powmcp-caption-file-check:caption_compare` applies the same bounded checks to exactly two tracks and compares their measured results by cue index.

Both tools are read-only. Fetching and parsing a full-length track, or two live comparison files, can take up to 60 seconds.

## What the checks measure

The app detects format from content and detects byte encoding and BOM.

WebVTT uses the WebVTT spec parser, SRT uses a dedicated SRT parser, and TTML/IMSC uses the imscJS TTML/IMSC profile engine.

The checks report structural specification and IMSC profile-conformance errors.

They measure cue count and identify overlapping, negative, out-of-order, and empty cues.

They measure per-line length and per-cue and summary reading speed in characters per second under the selected named profile.

`caption_compare` additionally reports side-by-side pass status, detected-format and encoding differences, cue-count delta, timing drift and overlap differences, CPS regressions, structural-error deltas, and a winner only when measured checks separate the tracks.

Comparison aligns cues by index. It does not establish that aligned cues have the same meaning.

## Inputs requiring judgment

For `caption_check`, choose one attached file or one public HTTP(S) URL. Do not provide both.

For `caption_compare`, choose exactly two attached files or exactly two public HTTP(S) URLs in the intended side-by-side order. Do not provide both forms.

Attachments may be WebVTT `.vtt`, SRT `.srt`, or TTML/IMSC `.ttml` or `.xml`. Detection is based on content rather than extension.

Public URLs cannot be pasted caption bodies, data URLs, FTP/SFTP URLs, or resources requiring credentials, headers, or cookies.

Choose one profile:

- `netflix-adult-20`: default, 20 CPS, specification-backed.
- `netflix-children-17`: 17 CPS, specification-backed.
- `youtube`: advisory reading-speed profile at about 17 CPS.
- `ebu-tt`: advisory reading-speed profile at about 17 CPS.

The Netflix profiles generally apply a 42-character Latin-script line limit. Quote the result rather than reconstructing its threshold decision.

Apply the same profile to both comparison tracks.

Each source file is bounded to 2 MB. The packet does not state a numerical cue cap, so do not invent one when the result reports truncation.

## Output used in the report

For `caption_check`, quote the returned pass status and `structuralErrorCounts` first.

Also quote the detected format and encoding, cue count, structural and profile-conformance findings, timing and overlap findings, empty-cue findings, line-length findings, CPS findings, selected profile, and truncation status when returned.

For `caption_compare`, quote both pass statuses before the detected-format and encoding differences, cue-count delta, timing drift, overlap differences, CPS regressions, structural-error deltas, and measured winner.

Preserve returned figures and messages verbatim. Do not round, re-derive, or embellish them.

A rule identifier names a rule rather than a diagnosis. Open the returned location and apply the returned message without assigning a broader meaning.

## What a pass proves

A `caption_check` pass means at least one cue was checked with no structural, timing, line-length, or reading-speed failure under the selected profile.

It is evidence about the submitted attachment or fetched public resource on the recorded date, within the 2 MB source-file bound and any reported truncation.

A comparison pass describes each track under the identical selected checks. A measured winner applies only to the reported differences.

A pass does not establish platform acceptance, complete destination compliance, translation quality, transcription accuracy, caption meaning, or synchronization against the actual video.

It does not assess burn-in, positioning, or styling requirements.

An advisory readability failure is a threshold failure, not a specification violation or platform rejection.

## Structurally unassessable cases

An arbitrary XML or text file that is not a caption track is unsupported because the app detects format from content.

A file beyond the 2 MB bound is outside the stated assessment scope.

A failed fetch leaves the source file unassessed.

Reported cue-cap truncation leaves the omitted content unassessed.

A comparison with an unpreflighted file is incomplete.

Unassessable content is not clean content. Absence from findings is not endorsement.

## Failure handling

When invalid arguments identify a field, correct that field and call the same tool again. Do not classify this as a missing tool.

For a missing or conflicting single-file input, report the returned error verbatim, then request either one public caption URL or one attached caption file, never both.

For comparison input errors, report the returned error verbatim. If both input forms were supplied, ask for either two public caption URLs or two attached caption files, not both. If neither complete form was supplied, ask for two public caption URLs or two attached caption files.

For unsupported content, report the returned unsupported-format error verbatim and state that no source-file verdict is available.

For a failed fetch, report the returned error verbatim and ask for an accessible public HTTP(S) URL or an attached file. Do not repeat a URL query string.

Do not convert an error, truncation, or unpreflighted file into a pass or fail for content that was not assessed.

## Non-PowMCP path

For WebVTT, use the Subtitle Toolkit WebVTT validator. For SRT and TTML/IMSC, use a local subtitle editor or dedicated validator, configure the client's complete delivery profile, and run structural, encoding, timing, overlap, line-length, and reading-speed checks.

Fix every evidenced issue and rerun the same checks. Then compare the captions with the actual media for transcription, translation, speaker and non-speech cues, synchronization, positioning, and styling.

This path diverges because it does not return the PowMCP result from the app's format-specific engines for the delivered artifact.

## Source of truth

- Caption File Check: https://powmcp.com/apps/caption-file-check/
- Netflix Timed Text Style Guide, General Requirements: https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements
- Netflix Timed Text Style Guide, Subtitle Timing Guidelines: https://partnerhelp.netflixstudios.com/hc/en-us/articles/360051554394-Timed-Text-Style-Guide-Subtitle-Timing-Guidelines
- Common subtitle format errors: https://subtitletoolkit.tools/guides/common-subtitle-format-errors-and-fixes/
- WebVTT validator documentation: https://subtitletoolkit.tools/tools/webvtt-validator/
