# Examples

Real prompts tested against this skill, with the variable mapping and bridge output each one produces.

---

## Example 1 — Meeting Prep Tool

**Prompt:**
> Build an input form for an AI meeting prep tool. The user enters who they're meeting with, what the meeting is about, and what outcome they want. Modern and professional look.

**Aesthetic Direction:** Refined Minimal — warm off-white background, slate-blue accent, Fraunces display + Figtree body.

**Variable Mapping:**

| Field | Variable | Type |
|-------|----------|------|
| Who are you meeting with? | `attendee` | string |
| What is the meeting about? | `meeting_topic` | string |
| What outcome do you want? | `desired_outcome` | string |

**Bridge Output:**
```tsx
import { submit, useIsRunning } from './bridge'

/**
 * MindStudio Variables Output:
 * - attendee        (string) — who the user is meeting with
 * - meeting_topic   (string) — what the meeting is about
 * - desired_outcome (string) — the outcome the user wants
 */

submit({ attendee, meeting_topic, desired_outcome })
```

**Downstream workflow usage:**
```
{{attendee}}, {{meeting_topic}}, {{desired_outcome}}
```

---

## Example 2 — LinkedIn Post Generator

**Prompt:**
> Build an input form for an AI LinkedIn post generator. It should collect the user's raw idea, let them choose a tone and post length, and have a strong submit button. White background, simple typography, lots of breathing room.

**Aesthetic Direction:** Refined Minimal — white background, generous whitespace, single deep-blue accent.

**Variable Mapping:**

| Field | Variable | Type |
|-------|----------|------|
| Raw idea / topic | `topic` | string |
| Tone of voice | `tone` | string (pill selector) |
| Post length | `post_length` | string (pill selector) |

**Bridge Output:**
```tsx
import { submit, useIsRunning } from './bridge'

/**
 * MindStudio Variables Output:
 * - topic       (string) — the user's raw idea or talking point
 * - tone        (string) — selected tone: Professional, Conversational, Storytelling, Bold
 * - post_length (string) — selected length: Short, Medium, Long
 */

submit({ topic, tone, post_length })
```

**Downstream workflow usage:**
```
{{topic}}, {{tone}}, {{post_length}}
```

---

## Example 3 — Content Research & Generation Tool

**Prompt:**
> Build an input form for a content research and generation tool. The user enters a topic, picks a tone of voice, adds keywords and LSI keywords, then selects which content formats they want like LinkedIn, blog, Instagram, Facebook, and TikTok. Clean modern look.

**Aesthetic Direction:** Dark Technical — deep slate background, electric teal accent, Syne + JetBrains Mono.

**Variable Mapping:**

| Field | Variable | Type |
|-------|----------|------|
| Research topic | `topic` | string |
| Tone of voice | `tone` | string (pill selector) |
| Keywords | `keywords` | string |
| LSI keywords | `lsi_keywords` | string |
| Content formats | `content_formats` | array (multi-select) |

**Bridge Output:**
```tsx
import { submit, useIsRunning } from './bridge'

/**
 * MindStudio Variables Output:
 * - topic           (string) — the user's research topic
 * - tone            (string) — selected tone of voice
 * - keywords        (string) — primary keywords, comma-separated
 * - lsi_keywords    (string) — LSI/semantic keywords, comma-separated
 * - content_formats (array)  — selected formats: linkedin, blog, instagram, facebook, tiktok
 */

submit({ topic, tone, keywords, lsi_keywords, content_formats })
```

**Downstream workflow usage:**
```
{{topic}}, {{tone}}, {{keywords}}, {{lsi_keywords}}, {{content_formats}}
```

---

## Example 4 — Chat Interface

**Prompt:**
> Build a chat interface similar to ChatGPT. User can type messages, see the conversation history, and get responses. Clean and modern.

**Aesthetic Direction:** Refined Minimal — white/light gray surfaces, subtle borders, generous input area, Figtree throughout.

**Variable Mapping:**

| Field | Variable | Type |
|-------|----------|------|
| User message | `user_message` | string |
| Conversation history | `conversation_history` | string (JSON serialized) |

**Bridge Output:**
```tsx
import { submit, useIsRunning } from './bridge'

/**
 * MindStudio Variables Output:
 * - user_message          (string) — the latest message from the user
 * - conversation_history  (string) — JSON array of prior messages for context
 */

submit({ user_message, conversation_history: JSON.stringify(history) })
```

**Downstream workflow usage:**
```
{{user_message}}, {{conversation_history}}
```

---

## Example 5 — Onboarding Wizard (Multi-Step)

**Prompt:**
> Build a multi-step onboarding form for a SaaS product. Collect the user's name, their role, their team size, and their main goal. Warm and professional feel.

**Aesthetic Direction:** Warm & Approachable — cream background, terracotta accent, Nunito display + DM Sans body, step progress indicator.

**Variable Mapping:**

| Field | Variable | Type |
|-------|----------|------|
| Full name | `name` | string |
| Role / job title | `role` | string |
| Team size | `team_size` | string (pill selector) |
| Main goal | `main_goal` | string |

**Bridge Output:**
```tsx
import { submit, useIsRunning } from './bridge'

/**
 * MindStudio Variables Output:
 * - name      (string) — the user's full name
 * - role      (string) — their job title or role
 * - team_size (string) — selected team size bracket
 * - main_goal (string) — their primary goal for using the product
 */

// Called only on the final step
submit({ name, role, team_size, main_goal })
```

**Downstream workflow usage:**
```
{{name}}, {{role}}, {{team_size}}, {{main_goal}}
```

---

## Notes on Variable Naming

The skill always asks for variable names before building. These conventions produce clean, readable workflow references:

| Convention | Example | Use When |
|------------|---------|----------|
| `snake_case` | `meeting_topic` | Multi-word variables (default) |
| Single word | `topic`, `tone`, `name` | Simple single-concept fields |
| Plural for arrays | `content_formats`, `keywords` | Multi-select fields |
| Prefixed for clarity | `lsi_keywords` vs `keywords` | When two similar fields exist |

Avoid generic names like `input1`, `field_value`, `data`, or `text` — these make downstream prompt engineering harder to read and maintain.
