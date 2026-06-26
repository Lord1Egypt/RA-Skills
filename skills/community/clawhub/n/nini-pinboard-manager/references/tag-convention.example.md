# Tag Convention

## Basic Rules

1. All tags in English, lowercase
2. Multi-word tags use underscore `_` as separator (e.g., `home_assistant`)
3. Singular form preferred (`tool` not `tools`)
4. No hyphens `-` in tags
5. No hierarchy separators `/` (e.g., `music` not `knowledge/music`)
6. Every bookmark MUST have at least 1 topic tag
7. Meta tags are optional (0-1 per bookmark)

## Topic Tags

### Tech

| Tag | Covers |
|-----|--------|
| `llm` | AI, LLM, agents, RAG, prompt engineering, Claude, OpenAI, etc. |
| `programming` | General programming, algorithms, design patterns, code quality |
| `python` | Python language specific |
| `javascript` | JavaScript / Node.js specific |
| `typescript` | TypeScript specific |
| `shell` | Shell scripting, CLI tools, terminal |
| `devops` | CI/CD, Docker, deployment, infrastructure |
| `cloudflare` | Cloudflare Workers, Pages, D1, etc. |
| `web` | Web development, browsers, HTTP, frontend/backend general |
| `github` | GitHub platform, Actions, APIs |
| `security` | Security, privacy, cryptography |
| `database` | Databases, search engines, data storage |

### Smart Home

| Tag | Covers |
|-----|--------|
| `home_assistant` | Home Assistant integrations, automations |
| `iot` | General IoT, smart devices, protocols |
| `zigbee` | Zigbee protocol specific |

### Life

| Tag | Covers |
|-----|--------|
| `health` | Physical and mental health, sleep, meditation |
| `food` | Cooking, nutrition, dietary guidelines |
| `travel` | Travel notes, destination guides |
| `fitness` | Exercise, workouts, sports |
| `finance` | Investing, budgeting, banking |

### Culture

| Tag | Covers |
|-----|--------|
| `game` | Video games, board games |
| `anime` | Anime, manga, light novels |
| `music` | Music, instruments, audio |
| `movie` | Movies, TV shows, documentaries |
| `book` | Books, reading lists |
| `history` | History, historical analysis |
| `writing` | Writing craft, blogging, content creation |

### Meta (Cross-cutting)

| Tag | Covers |
|-----|--------|
| `learning` | Learning resources, tutorials, courses |
| `career` | Job search, career development, interviews |

## Meta Tags (Content Type)

| Tag | Meaning |
|-----|---------|
| `evergreen` | Long-lasting value, worth revisiting |
| `tool` | It IS a tool, service, or product |
| `reference` | Reference manual, cheatsheet, specification |
| `collection` | Curated list, awesome list, roundup |

> Note: `toread` is managed by Pinboard's built-in field, NOT as a tag.
> `TODO` should NOT be used as a tag — use Pinboard's toread field instead.

## Migration Mapping

### Typos

| Current | → New |
|---------|-------|
| `ainme` | `anime` |
| `editer` | `editor` → decide: `tool` or `programming` |
| `life'` | delete (typo with quote) |

### Case Normalization

| Current | → New |
|---------|-------|
| `Health` | `health` |
| `Testing` / `test` | `programming` (or delete if too vague) |
| `JavaScript` | `javascript` |
| `Node.js` / `nodejs` | `javascript` |

### Chinese → English

| Current | → New |
|---------|-------|
| `终极文档` | `reference` |
| `攻略` | `game` |
| `种草` | `finance` or topic-appropriate |
| `消费主义` | `finance` |
| `星际铁道` | `game` |
| `庙宫祭` | `game` |
| `声冻计划` | `game` |
| `游戏文化` | `game` |

### Concept Merging

| Current | → New | Reason |
|---------|-------|--------|
| `ai`, `openai`, `anthropic`, `claude`, `claudecode`, `rag`, `agent` | `llm` | Unify under one umbrella |
| `tools` | `tool` | Singular form |
| `privacy`, `privacy_anonymity`, `privacy_technology` | `security` | Merge related concepts |
| `technology`, `tech` | reassign by actual content | Too vague |
| `community`, `discussion` | delete or reassign | Too vague |
| `hacker_news` | delete (source, not topic) | Tag the content topic instead |
| `friend` | delete or `writing` | Reassign by content |
| `knowledge/music` | `music` | Remove hierarchy |
| `technology/typescript` | `typescript` | Remove hierarchy |
| `technology/write` | `writing` | Remove hierarchy |

### Tags to Remove

| Tag | Reason |
|-----|--------|
| `TODO` | Use Pinboard's toread field |
| `2025` | Year tags are not useful for categorization |
| `Software` | Too vague, reassign by content |
| `pingcode` | Internal tool reference, not a category |
