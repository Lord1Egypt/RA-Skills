---
name: make-song
description: Make a finished song with vocals, or an instrumental, on the user's Musikalis account through the Musikalis MCP server, then hand back the MP3 links. Covers choosing between a plain description and full lyrics, writing lyrics with section tags, the style line, waiting for the result, credits and commercial use. Use when the user asks for a song, jingle, birthday or wedding song, theme song, background track or instrumental, wants their lyrics turned into a song, or asks about their Musikalis songs or credits.
---

# Make a song with Musikalis

[Musikalis](https://musikalis.com) turns a description, or lyrics with a title and style, into a finished song. Each request returns two versions in about one to three minutes, each with an MP3 link and cover art. Songs use the credits on the user's Musikalis account and are saved to their library on musikalis.com.

This skill works through the Musikalis MCP server at `https://musikalis.com/api/mcp` and its four tools: `create_song`, `get_song`, `list_songs` and `get_account`.

## If the tools are missing

If you cannot see `create_song`, the server is not connected. Do not call the HTTP endpoint yourself. Tell the user how to connect in their app, then stop:

- Claude Code: `claude mcp add --transport http musikalis https://musikalis.com/api/mcp`, then run `/mcp` to sign in.
- Claude on the web or desktop: Settings → Connectors → Add custom connector → `https://musikalis.com/api/mcp`.
- ChatGPT: Settings → Apps → turn on developer mode in the advanced settings → create an app with `https://musikalis.com/api/mcp` and OAuth.
- Codex: `codex mcp add musikalis --url https://musikalis.com/api/mcp`, then `codex mcp login musikalis`.
- Cursor, VS Code and other clients: the [Musikalis MCP guide](https://musikalis.com/mcp) and the [config examples](https://github.com/geektao1024/musikalis-mcp/tree/main/mcp).

Signing in opens a Musikalis page in the browser. New accounts get free credits.

If the user would rather not connect anything, they can make the song in the browser with the [Musikalis AI song generator](https://musikalis.com/ai-song-generator).

If a tool answers that the user is not signed in, the connection has expired or the app was disconnected: ask the user to sign in again from the app's MCP or connector settings.

## 1. Check the account when it matters

Call `get_account` before the first song in a conversation and whenever the user asks about credits. It returns:

- `credits`, `song_cost_credits` and `songs_affordable`;
- `commercial_use_for_new_songs` and `license_note`;
- `creative_quality_available`;
- `pricing_url` and `license_url`.

If `songs_affordable` is 0, say so, give the user `pricing_url` and stop. You cannot buy credits or change plans for the user.

If the song is for an ad, a monetized video, a client, a shop or anything else commercial, check `commercial_use_for_new_songs`. When it is false, tell the user before you make the song: songs made without an active paid subscription are for personal, non-commercial use. Give them `license_url`.

## 2. Choose description or lyrics

| The user gives you | Mode | Send |
| --- | --- | --- |
| An idea: "a song for my sister Mia's birthday, she loves cats" | Quick | `description` |
| Their own lyrics | Custom | `lyrics`, `title`, `style` |
| An idea where the words matter (names, a story, an inside joke, a set language), or they want to read the lyrics first | Custom, with lyrics you write | `lyrics`, `title`, `style` |
| No vocals | Either, with `instrumental: true` | `description`, or `title` and `style` |

In quick mode Musikalis writes the lyrics. It usually keeps the names and details in the description, but not always. When a detail has to be sung, write the lyrics yourself.

## 3. Write the request

### Description (quick mode)

Up to 3,000 characters, though two or three sentences usually work best. Say what the song is about, the mood, the genre, the voice and the language:

> A warm acoustic pop song for my sister Mia's 30th birthday. She loves her two cats and weekend hikes. Female vocals, English, an easy sing-along chorus.

### Lyrics (custom mode)

- Up to 5,000 characters. Put each section tag on its own line: `[Intro]`, `[Verse]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, `[Outro]`.
- For about three minutes: Verse, Chorus, Verse, Chorus, Bridge, Chorus. Verses of four to eight lines are enough.
- Keep lines short and easy to sing. Repeat the chorus word for word each time and put the title in it.
- Write only the words to be sung. Leave out chord names, speaker labels and stage directions. Words in parentheses are often sung as backing vocals.
- Write in the language the song should be sung in.
- If you made up personal details, show the lyrics and ask before you spend credits.

### Title and style

- `title`: up to 80 characters. Required in custom mode.
- `style`: up to 1,000 characters: genre, mood, instruments, tempo and voice, for example `warm acoustic pop, fingerpicked guitar, light percussion, 95 bpm, gentle female vocals`. Describe the sound instead of naming real artists. In quick mode the style is added to the description.

### Options

- `quality`: `standard` (default), `fast` (quicker and picks its own length) or `creative` (more adventurous; only when `creative_quality_available` is true).
- `instrumental`: `true` for no vocals. A song cannot be an instrumental and have lyrics.
- `vocal_gender`: `male` or `female`.
- `duration_seconds`: custom mode only, up to 360. Leave it out to fit the length to the lyrics. `fast` ignores it.

## 4. Start the song and wait

1. Call `create_song` once. It returns a `task_id` and the credits it charged.
2. Tell the user the song has started and takes one to three minutes.
3. Wait about a minute, then call `get_song` with the `task_id` every 20 to 30 seconds until `status` is `ready` or `failed`. If you cannot wait, tell the user to ask you again in a few minutes.
4. Never call `create_song` to retry or to check on a song. The same request within ten minutes returns the first task; a changed request makes a new song and charges again.

When the status is `ready`, `get_song` returns two versions. Give the user both: title, length, `audio_url` (MP3) and `cover_url`, and `library_url`, where they can download WAV files and keep working on the song. Offer the lyrics if they want them.

When the status is `failed`, the credits have already been refunded. Suggest one change, such as a simpler description or another style, and ask before you try again.

## 5. After the song

- `list_songs` returns the latest songs (up to 20) with their `song_id`.
- To turn a song into a music video, use the `music-video-storyboard` skill, or give the user `https://musikalis.com/ai-music-video?song=<song_id>&utm_source=skill&utm_medium=agent`, which opens the Musikalis video maker with that song already picked.

## What you cannot do here

Say so plainly if the user asks you to delete songs, buy credits, change their plan or open someone else's account. They can manage their library and plan on musikalis.com.
