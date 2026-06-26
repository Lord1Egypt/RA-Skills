---
name: movie-manager-claw
description: "Organizes movie recommendations in Obsidian and generates suggestions based on user profile."
---

# Movie Manager Skill

Transform your AI agent into a sophisticated cinematic partner. This skill goes beyond simple lists, offering proactive research, intelligent organization in Markdown/Obsidian, and a personalized recommendation engine that evolves with your tastes.

## 🌟 Key Features

- **Watch Source Integration**: Finds and embeds official YouTube trailers and suggests available streaming platforms.
- **Visual Enrichment**: Fetches poster URLs and displays them inline for a rich browsing experience.
- **Intelligent Organization**: Manages `watchlist/` and `seen/` folders with a centralized `Movies.md` index.
- **Personalized Recommender**: Suggests films based on your evolving profile of preferred actors, genres, and themes.
- **Double-Feature Logic**: Suggests complementary pairs of films for curated marathons.
- **Reflective Journaling**: Includes prompts after watching to capture thoughts and memories.
- **Smart Reminders**: Integrated with `cron` to notify you of upcoming releases.
- **WikiLink Integration**: Links people and genres within your vault (creates `#people` stubs when needed).

## 🛠 Configuration

### Variables
- `MOVIES_ROOT`: Base directory (default: `Movies/`).
- `WATCHLIST_DIR`: New discoveries (default: `Movies/watchlist/`).
- `SEEN_DIR`: Archived films (default: `Movies/seen/`).
- `INDEX_FILE`: Central tracker (default: `Movies/Movies.md`).
- `PROFILE_FILE`: The learning brain (default: `Movies/Cinematic Profile.md`).
- `LANG`: Language for prompts (default: `en`).

## 🚀 Workflow

### 0. Initialization (Auto-Setup)
On first run, the skill ensures:
1. The `MOVIES_ROOT` directory exists.
2. `watchlist/` and `seen/` subdirectories are created.
3. Default `Movies.md` index and `Cinematic Profile.md` are initialized.

### 1. Recommendation ("Find me a movie")
1. **Profile Analysis**: Consults `PROFILE_FILE` for preferred actors, genres, and themes.
2. **Context Check**: May check recent logs or mood to suggest a matching "vibe".
3. **Double-Feature**: Offers a "Power Duo" of two films with a unique connection.

### 2. Saving to Watchlist
- Creates a file: `{Title} ({Year}) - {Actor1}, {Actor2}.md` in `WATCHLIST_DIR`.
- Populates with ratings, streaming sources, poster, and YouTube trailer.
- If the movie is unreleased, creates an `openclaw cron` reminder.

### 3. Archive as Seen & Learning
1. **Archive**: Moves the file to `SEEN_DIR` and checks `[x]` in `Movies.md`.
2. **Reflection**: Asks questions like "What was the most surprising moment?" or "Would you watch more from this director?".
3. **Evolution**: Updates `PROFILE_FILE` with new actors, directors, or genres discovered.

## 📄 Structured Template

```markdown
# {Title} ({Year})
![Poster]({Poster URL})

- **Rating**: ⭐ {IMDb/RT Score}
- **Where to watch**: 📺 {Streaming Platforms}
- **Description**: {Summary}
- **Actors**: [[Actor1]], [[Actor2]]
- **Genre**: [[Gen1]]
- **Trailer**: {YouTube Link}

### 💡 Why it fits you
{Personalized motivation based on actors, genre, and preferred themes}

### ✍️ Post-Watch Reflections
*(Added during archiving)*
- **Memorable Scenes**:
- **Personal Rating**: ⭐ {1-10}
- **Quick Feedback**: +1 / -1
```

---
Created with ❤️ for the OpenClaw community.

Language: prompts and template text are in English (`en`) by default.
