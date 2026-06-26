# Publish Copy

Use this file as the local source for GitHub README sections, ClawHub listing
text, npm/release notes, and product-page copy.

Policy for this release: describe the **skill layer**. Do not list external chat
platforms as supported channels unless those adapters are tested separately.
Channel delivery belongs to the OpenClaw host and adapter configuration.

## Product Name

- Public product name: `OpenClaw Continuity`
- Technical package / slug: `personal-hooks`
- Current local version target: `2.0.21`
- Contact: `adarobot666@gmail.com`
- Product illustration: `assets/publish/product-story-bilingual.svg`
- Setup wizard comic: `assets/publish/comic-01-setup-wizard.svg`
- Adjust-anytime comic: `assets/publish/comic-02-adjust-anytime.svg`
- Natural-language settings comic: `assets/publish/comic-03-natural-language-settings.svg`
- Command settings comic: `assets/publish/comic-04-command-settings.svg`

## One-Line Positioning

English:

> State-backed continuity for OpenClaw: remember the right thing, reconnect the
> right topic after `/new`, and follow up naturally with time-aware context.

中文：

> 替 OpenClaw 補上狀態支撐的延續感：記住對的事、`/new` 後接回對的主題，
> 並用時間感自然關心與追蹤。

## Short Description

English:

> A skill-layer continuity engine for OpenClaw agents. It separates ordinary
> chat, staged memory, and tracked follow-up; adds `/new` carryover, time sense,
> guided setup, natural-language settings, daily-memory writeback, and
> frontstage safety guards.

中文：

> OpenClaw 的技能層延續引擎。它會分辨一般聊天、暫存記憶與正式追蹤，
> 補上 `/new` 承接、時間感、安裝精靈、自然語言設定、每日記憶寫回與前台安全守門。

## ClawHub First Screen Copy

### English First

OpenClaw Continuity makes an OpenClaw agent feel coherent after interruption,
delay, or `/new`.

It is not a generic cron sender. It decides whether something should stay
ordinary chat, become staged memory, or become tracked follow-up. It can carry
the right thread into a new conversation, respect sleep/wake and quiet-hour
context, and let users adjust behavior by talking naturally.

### 中文接續

OpenClaw Continuity 不是單純排程發訊息。它的重點是讓 agent 記住「該記住的事」，
而不是把所有內容都塞進記憶或變成吵人的主動訊息。

它會把對話分成一般聊天、暫存記憶、正式追蹤；在 `/new` 後接回正確主題；
並且讓使用者可以用自然語言調整作息、勿擾、關心節奏與新對話承接方式。

## Minimal Telegram/TG Showcase Block

Use this only as a minimal live example, not as a channel-support matrix.

English:

> If your OpenClaw host is already connected to Telegram/TG, this skill can be
> demonstrated there through the normal host reply pipeline. Example: park a
> topic, start `/new`, and confirm the agent reconnects the selected continuity
> anchor instead of falling back to generic small talk. The Telegram adapter is
> host configuration; the continuity behavior comes from this skill.

中文：

> 如果你的 OpenClaw host 已經接好 Telegram/TG，可以用它做最小 live 展示：
> 先讓使用者說「這件事晚點再接」，再輸入 `/new`，確認 agent 接回正確承接點，
> 而不是掉回空泛閒聊。Telegram adapter 屬於 host 設定；這個技能提供的是
> continuity 行為本身。

Minimal demo script:

```text
TG user: 這個上架檢查先放著，晚點再接。
Agent: 好，我先幫你接住這條線，不會當成普通閒聊丟掉。

TG user: /new
Agent: 前面那個上架檢查我還接得住。要從最近 4 輪、最後意圖，還是追蹤焦點接？

TG user: 新對話改成看最後使用者意圖。
Agent: 已更新。之後新對話會優先從最後使用者意圖承接。
```

## Human-Friendly Feature List

- Remembers what still matters after a pause or new session.
- Keeps casual chat casual.
- Lets "talk later" become staged memory instead of disappearing.
- Promotes truly important items into tracked follow-up.
- Reconnects the right topic after `/new`.
- Uses routine/time context as support, not as the main thread.
- Supports quiet hours, sleep/rest suppress, cooldown, closure, dedupe, and dispatch caps.
- Lets users change settings in plain language.
- Writes concise daily-memory traces from structured state.
- Keeps internal runtime confusion out of frontstage chat.

中文：

- 中斷或新開對話後，還能接回真正重要的事。
- 一般聊天不會被硬塞成追蹤。
- 「晚點再說」可以先暫存，不會直接消失。
- 真的重要的事才升成正式追蹤。
- `/new` 後可以選擇承接方式。
- 作息與時間感只是輔助，不搶走主線。
- 支援勿擾、睡眠/休息抑制、冷卻、退場、去重與發送上限。
- 使用者可以用口語調整設定。
- 每日記憶寫回來自結構化狀態，不靠模型亂猜。
- 避免內部 runtime 訊息漏到前台。

## Complete Public Feature Checklist

- `casual_chat / staged_memory / tracked_followup` routing
- tracked categories:
  - `parked_topic`
  - `watchful_state`
  - `delegated_task`
  - `sensitive_event`
- `candidate -> incident -> hook` promotion
- structured `event_chain`
- structured `causal_memory`
- assistant commitment support
- `/new` carryover
- user-selectable `/new` continuity mode:
  - `recent_4_turns_first`
  - `last_user_intent_first`
  - `followup_focus_first`
  - `assistant_commitment_first`
  - `balanced`
- routine/time context as support-only signal
- quiet hours
- sleep/rest suppress
- cooldown
- closure
- dedupe
- dispatch cap
- daily-memory writeback
- deterministic onboarding
- guided settings
- natural-language settings changes
- command-style settings changes
- host-neutral voice/image continuity preference
- skill/tool-layer frontstage guards
- regression harness and release acceptance checks

## Scope Boundary

Use this wording when reviewers ask whether the skill supports a specific chat
platform:

> This package is the OpenClaw skill layer. It provides continuity state,
> memory routing, `/new` carryover, setup, and safety guards. Message delivery
> depends on the OpenClaw host and its adapter configuration.

Do not advertise a channel matrix inside the skill listing.

## Setup Wizard Copy

Recommended image:

- `assets/publish/comic-01-setup-wizard.svg`

First install can guide the user through:

- timezone
- sleep time
- wake time
- relationship/use case
- proactive care preference
- quiet hours
- care tone
- tracking keywords
- new conversation carryover mode
- voice/image continuity preference when the host already supports those modalities

Natural-language examples:

```text
Help me adjust my follow-up settings.
Make follow-up quieter after midnight.
Use the last user intent when a new conversation starts.
新對話承接改成最近 4 輪摘要。
把主動關心改保守一點。
半夜不要主動追蹤我。
```

Command examples:

```bash
python3 scripts/personal_hooks.py setup-check
python3 scripts/personal_hooks.py setup-apply --payload-json '{"new_session_continuity_mode":"recent_4_turns_first"}'
python3 scripts/personal_hooks.py setup-apply --payload-json '{"modality_continuity_mode":"preserve_when_supported"}'
python3 scripts/personal_hooks.py setup-apply --payload-json '{"sleep_time":"23:00","wake_time":"07:00"}'
```

## Install Placement Copy

```text
openclaw-workspace/
  skills/
    personal-hooks/
      SKILL.md
      scripts/
      docs/
      examples/
      assets/
```

Initialize:

```bash
python3 openclaw-workspace/skills/personal-hooks/scripts/personal_hooks.py init
```

Verify:

```bash
python3 openclaw-workspace/skills/personal-hooks/scripts/followup_skill_harness.py --absence-minutes 3
```

Expected:

```json
{
  "summary": {
    "pass_count": 14,
    "fail_count": 0
  }
}
```

## GitHub README Structure

Recommended order:

1. Product promise and bilingual comic image
2. Four quick comics:
   - setup wizard
   - adjust anytime
   - natural-language settings
   - command settings
3. "For Everyone" explanation
4. Example of `/new` continuity
5. Full feature list
6. Scope boundary
7. Setup wizard
8. Natural-language and command settings
9. Install
10. Verify
11. Technical map
12. Contact and star request

## GitHub Release Notes Draft

### English

`OpenClaw Continuity 2.0.21` focuses the public package on the portable skill
core and expands the product-facing documentation.

Highlights:

- adds user-selectable `/new` continuity modes
- adds host-neutral modality continuity preference
- makes first-install guided setup include those preference fields
- documents natural-language and command-style setting changes
- clarifies that channel delivery belongs to the OpenClaw host/adapter
- keeps public copy free of untested external-channel claims
- includes a bilingual product-story illustration and four focused setup/settings comics
- keeps the regression harness at `14/14` expected pass
- uses the official ClawHub YAML metadata format for runtime requirements

### 中文

`OpenClaw Continuity 2.0.21` 聚焦公開技能核心，並補齊產品化說明。

重點：

- 新增可選 `/new` 承接模式
- 新增 host-neutral 的語音/圖片延續偏好設定
- 第一次安裝精靈會詢問這些偏好
- 補齊自然語言與指令式設定方式
- 明確區分技能層與 OpenClaw host/adapter 的通訊交付責任
- 不在公開文案宣稱未驗證的外部渠道支援
- 加入雙語產品漫畫式示意圖
- regression harness 維持預期 `14/14` pass
- 使用 ClawHub 官方 YAML metadata 格式宣告 runtime requirements

## Star Request

English:

> If this skill helps and you want to keep improvements and maintenance moving,
> please star the GitHub repository.

中文：

> 如果這個技能對你有幫助，而且你也期待它持續優化與維護，歡迎在 GitHub
> 給一顆星，這會是最直接的支持。
