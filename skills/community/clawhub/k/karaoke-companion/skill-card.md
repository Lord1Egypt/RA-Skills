## Description:

歌詞隨唱伴侶 — 跟著歌詞學唱歌、卡拉 OK 模式練歌、填詞創作（含韻腳表）、中英日翻譯對照。LRCLIB 即時歌詞，支援減速、段落反覆。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuan905](https://clawhub.ai/user/xuan905)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to practice singing with synchronized lyrics, run karaoke-style rehearsal flows, create lyric drafts with rhyme and BPM helpers, and compare Chinese, English, and Japanese translations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A save command can write outside the intended songs directory or overwrite user-writable .txt files when a title is used as a path-like filename.

Mitigation: Sanitize saved filenames, resolve and check paths remain inside ~/.karaoke-companion/songs/, and refuse to overwrite existing files unless the user explicitly confirms.

Risk: Song titles, artist names, lyric text, and search terms may be sent to third-party services for lyrics lookup, fallback search, or translation.

Mitigation: Review user input before network-backed commands and avoid submitting sensitive, private, or unreleased lyrics to LRCLIB, LibreTranslate, or DuckDuckGo.

Risk: LRCLIB track retrieval is described as ID-based, but the scanner guidance calls for stricter validation.

Mitigation: Validate LRCLIB IDs as digits only before making retrieval requests.

## Reference(s):

- [LRCLIB](https://lrclib.net)
- [LibreTranslate](https://libretranslate.com)
- [ClawHub Skill Page](https://clawhub.ai/xuan905/skills/karaoke-companion)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and generated lyric, karaoke, translation, and songwriting text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local cache, state, or song files under ~/.karaoke-companion and may use network services for lyrics search and translation.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
