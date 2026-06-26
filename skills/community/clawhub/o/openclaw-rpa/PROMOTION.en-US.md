# OpenClaw RPA skill — promotional copy (English)

> Use for product pages, newsletters, or ClawHub blurbs. Links and model tips at the end.

---

## Main copy (short)

When you use OpenClaw to let a large model **drive the browser or local files** for repetitive work, three pains show up again and again:

1. **Hallucinations** — wrong clicks, wrong elements, or steps that never existed.  
2. **Cost** — every run burns tokens and tool calls.  
3. **Speed** — waiting on reasoning each step is an order of magnitude slower than a script.

**openclaw-rpa** addresses all three with one idea:

**Record real actions once → generate a standalone Playwright Python script → replay that script later.**

On replay you **do not call the LLM**: stable paths, predictable results, much faster, cost ≈ local Python only.

**What you can record (not just the browser)**

| Capability | Notes |
|------------|--------|
| **Browser** | Real Chrome, step-by-step; selectors come from the DOM, not model guesses. |
| **HTTP API** | `GET` / `POST` REST calls, save JSON; keys can be embedded in the generated script (trigger with **`#rpa-api`**). |
| **Excel (.xlsx)** | Create/update workbooks, multiple sheets, headers, freeze row — **openpyxl**, no Microsoft Excel required. |
| **Word (.docx)** | Paragraphs + table reports — **python-docx**, no Microsoft Word required. |
| **Auto-login** | **`#rpa-login`** — you log in once manually; cookies are saved and **injected on later recordings and replays**, reducing SMS / slider / QR loops on complex sites. |
| **Mixed flows** | Web + API + Excel + Word in **one** task (e.g. reconciliation: fetch API → match sheets → Word report). |

**Why people use it**

- Multi-step tasks can be split to reduce single-request timeouts.  
- Output is plain `.py`; you can run it with `python3` outside OpenClaw.  
- Browser + local file output (e.g. Desktop).  
- With OpenClaw + IM, **`#rpa-run:task-name`** triggers runs or scheduled jobs.

**Typical use cases**

E‑commerce login/checkout, quotes/news scraping, movie reviews aggregation, **pure API pulls**, **local Excel/Word reports** — record once, replay many times with the same stable path.

---

## Ultra-short (card / summary)

LLM-driven browsing is slow, expensive, and error-prone. **openclaw-rpa**: **record once** in a real environment → **Python + Playwright** script; **replay without the model**. Besides the **web**, it supports **REST APIs**, **Excel / Word** (no Office apps), and **`#rpa-login` cookie reuse** for gnarly logins. Best for high-repeat, stability-first workflows.

---

## Case highlights + links

**Hub**

- English README — **Case videos**:  
  https://github.com/laziobird/openclaw-rpa/blob/main/README.md#case-videos  
- Chinese README (more video links in some sections):  
  https://github.com/laziobird/openclaw-rpa/blob/main/README.zh-CN.md  

**Sauce demo (browser recording)**

- Flow: login → sort → add to cart → logout.  
- Docs:  
  https://github.com/laziobird/openclaw-rpa/blob/main/README.md#1-sauce-online-shopping-website-demo-browser-recording  

**Douban movie (browser + save to Desktop)**

- https://github.com/laziobird/openclaw-rpa/blob/main/README.md  

**Yahoo Finance NVDA (browser)**

- https://github.com/laziobird/openclaw-rpa/blob/main/README.md#yahoo-finance-nvda-demo  

**API + news + local brief (`#rpa-api`)**

- https://github.com/laziobird/openclaw-rpa/blob/main/README.md  

**Feishu / Lark: `#rpa-list` / `#rpa-run`**

- https://github.com/laziobird/openclaw-rpa/blob/main/README.md#openclaw--feishulark-rpa-list-rpa-run-and-scheduled-run  

**Auto-login (cookies): Sauce replay**

- **`#rpa-login`** saves cookies → injected on record/replay.  
- **English tutorial**:  
  https://github.com/laziobird/openclaw-rpa/blob/main/articles/autologin-tutorial.en-US.md  

**AP reconciliation (API + Excel + Word)**

- Mock GET + local Excel matching + Word table report (illustrative).  
- **EN**: https://github.com/laziobird/openclaw-rpa/blob/main/articles/scenario-ap-reconciliation.en-US.md  

---

## Links & models

- **Full skill spec (English)**: [SKILL.en-US.md](https://github.com/laziobird/openclaw-rpa/blob/main/SKILL.en-US.md)  
- **Install & overview**: [README.md](https://github.com/laziobird/openclaw-rpa/blob/main/README.md)  
- **ClawHub**: [clawhub.ai/laziobird/openclaw-rpa](https://clawhub.ai/laziobird/openclaw-rpa)  
- **Source**: [github.com/laziobird/openclaw-rpa](https://github.com/laziobird/openclaw-rpa)

**Recommended models** (for recording / planning only): Minimax 2.7, Gemini Pro 3.0+, Claude Sonnet 4.6. **Replay does not use a large model.**

---

## One-liner titles

- “Record once, run forever: browser + API + Excel + Word — zero LLM tokens on replay.”  
- “Stop paying the model for every click: freeze the flow as Python, stable and cheap.”

---

## Discord `#self-promotion` (English, copy-paste)

Use in **OpenClaw Discord → self-promotion** (keep under ~2000 characters if the channel limits length). Links in `<>` reduce embed spam; drop the brackets if you want previews.

**Compact (~1.1k chars)** — copy everything below the rule line:

---

openclaw-rpa — OpenClaw skill: record once (Chrome, local files, REST API) → one Playwright Python script → replay with python3, no LLM (faster, cheaper, DOM-backed selectors).

Records: browser · #rpa-api (GET/POST, JSON, keys in script) · Excel .xlsx (openpyxl) · Word .docx (python-docx) · #rpa-login + #rpa-login-done (log in once manually → cookies auto-injected) · mixed API + browser + Office in one task.

Triggers: #RPA / #rpa · #rpa-api · #rpa-list · #rpa-run:TaskName · #rpa-login …

README (Sauce, Yahoo NVDA, API+brief, Feishu/Lark + install): <https://github.com/laziobird/openclaw-rpa/blob/main/README.md#case-videos>  
Skill spec: <https://github.com/laziobird/openclaw-rpa/blob/main/SKILL.en-US.md>  
Auto-login: <https://github.com/laziobird/openclaw-rpa/blob/main/articles/autologin-tutorial.en-US.md>  
AP scenario (API+Excel+Word): <https://github.com/laziobird/openclaw-rpa/blob/main/articles/scenario-ap-reconciliation.en-US.md>  
ClawHub: <https://clawhub.ai/laziobird/openclaw-rpa> · Repo: <https://github.com/laziobird/openclaw-rpa>

Obey site terms & law; heavy CAPTCHA may still need a human.

---

**Longer variant** (every README anchor on its own line) is ~2.2k+ characters; use git history on this file if you need that list back.

---

## Discord blurbs — other tech servers (shorter)

Pick one tone/length for **Playwright / Python / RPA / LLM** communities (not OpenClaw-only). Wrap links in `<>` on Discord if you want fewer embeds.

**A. One-liner (~350 chars)**

openclaw-rpa (OpenClaw skill): record browser + API + Excel/Word once → generates a standalone **Playwright + Python** script; **`python3` replay = no LLM**. Repo: <https://github.com/laziobird/openclaw-rpa>

**B. Elevator (~550 chars)**

**openclaw-rpa** — RPA-style recorder for **OpenClaw**: AI helps you capture real **Chrome** steps, **REST** calls (`#rpa-api`), and **.xlsx / .docx** writes; output is plain **Python** you run with Playwright. Replay does **not** call an LLM — good for repetitive flows and cutting token burn. Cookie reuse: `#rpa-login` + `#rpa-login-done`. Docs & demos: <https://github.com/laziobird/openclaw-rpa/blob/main/README.md> · spec: <https://github.com/laziobird/openclaw-rpa/blob/main/SKILL.en-US.md>

**C. Dev-focused (~400 chars)**

Local-first automation: **record once** (headed Chrome + optional httpx-style API + openpyxl/python-docx) → **one `.py`** with Playwright. No model at run time. Triggers live in the skill doc if you use OpenClaw; the generated script runs anywhere with deps. <https://github.com/laziobird/openclaw-rpa>

**D. LLM audience (~320 chars)**

Tired of **computer-use** burning tokens every run? Record the flow once, compile to **Playwright Python**, replay offline. Browser + API + Office file steps. OpenClaw skill **openclaw-rpa**: <https://github.com/laziobird/openclaw-rpa>

---

## Twitter / X (character limits)

**Classic post (≤280 characters)** — fits the legacy limit with **Sauce e‑commerce demo video** + repo link:

```
openclaw-rpa: record real browser once → Playwright Python; replay with python3, no LLM.

🛒 E‑commerce demo (Sauce: login → sort → cart): https://github.com/user-attachments/assets/965fbecc-a0fc-4795-9f63-a5ef126f97f8

https://github.com/laziobird/openclaw-rpa
```

(~260 chars; `t.co` shortening may differ slightly if you paste elsewhere first.)

**Shorter (video only, ~190 chars)** — put the repo in a reply or your profile:

```
openclaw-rpa — record once, replay forever (Playwright Python, no LLM at run time).

🛒 Sauce shopping demo: https://github.com/user-attachments/assets/965fbecc-a0fc-4795-9f63-a5ef126f97f8
```

**Longer posts / threads (X Premium)** — add hashtags sparingly (`#OpenClaw` `#Playwright` `#RPA`) and link README case section: <https://github.com/laziobird/openclaw-rpa/blob/main/README.md#1-sauce-online-shopping-website-demo-browser-recording>

**Video source:** same file as README “Sauce Demo” — `saucedemo-readme` / shopping flow on [saucedemo.com](https://www.saucedemo.com). Bilibili mirror (CN audience): <https://www.bilibili.com/video/BV1YfXrBBE9u/>
