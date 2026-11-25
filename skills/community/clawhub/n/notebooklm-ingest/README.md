# NotebookLM → Wiki Ingest

> ⚠️ **Requires the HiJavis iPhone app.** This skill runs inside HiJavis —
> install the app first, then connect NotebookLM from your chat.
> 📲 https://apps.apple.com/us/app/hijavis/id6745134765

The research you keep in NotebookLM — your notes, your study guides, the reports
you generated against your own sources — never reaches the rest of what Javis
knows about you. This brings it across: you pick the notebooks, and the notes in
them become pages in your personal wiki, linked to everything else you have
captured.

## Picture this

- You spent a month reading papers in one notebook. Six months later the
  conclusions are on a wiki page next to the conversation where you first
  mentioned the problem.
- A study guide you asked NotebookLM to write lands in your wiki, woven into
  the topics it belongs to, so it shows up when you search for them rather than
  only inside Google.
- You add a note on Tuesday. Wednesday morning it is already in your wiki, and
  you were not asked to do anything.
- A note you brought in last month turns out to be wrong. One undo takes its
  pages back out and leaves everything else alone.

## What it does

You sign in to Google **once**, yourself, in a real sign-in window. From then on
Javis reads the notebooks you chose, on the schedule you set, and hands each
note to the same machinery that already turns your Obsidian notes and your
recordings into wiki pages.

Before anything is written you can ask for a **preview**: it tells you exactly
which pages it would create and which it would update, and writes nothing.

## How to use it

### Turn it on

Open your HiJavis chat and say "fetch my notebooklm". Javis offers a **Connect**
button, Google's own sign-in opens, and you type your password — Javis never
does. Then pick the notebooks you want mirrored and say when it should run.

### Ask for it now

- "fetch my notebooklm"
- "ingest my notebooklm"
- "notebooklm to wiki"
- "同步我的 notebooklm"

### Ask what it has done

- "what have you ingested from notebooklm" — the list, newest first, with the
  notebook, the note, what triggered it, when, and how many pages it wrote.
- "where does the notebooklm bridge run" — the host it is set to.
- "when does the notebooklm sync run" — the schedule.

## What makes it handy

- **Preview before it writes.** Ask for a dry run and you see the page list with
  nothing committed.
- **Undo is real.** Removing an ingest takes out the pages that ingest fed, and
  only those.
- **It tells you when it breaks.** Google signs a stored session out when you
  change your password, and it will happen. Javis says so, tells you nothing in
  your wiki was lost, and offers to reconnect — rather than going quiet and
  leaving your wiki looking current when it is not.
- **It never asks for your password.** Sign-in is yours, in a real browser
  window, once.
- **One message per run.** Including the runs that found nothing, so a quiet
  week never looks the same as a broken connection.

## Good to know

- **Read-only.** It reads notes, reports and study guides. It never writes into
  NotebookLM, never adds a source, and never generates anything there.
- **Text only.** Audio overviews are not read — there is no supported way to get
  their text.
- **Notebooks other people shared with you** are not included; there is no
  machine-readable way to reach them.
- **This is unofficial access.** Google publishes no API that can read notes, so
  this rides the same interface the website uses. It works today and it will
  break at some point; when it does, you can still paste text into your wiki
  directly and nothing you have already ingested is affected.
- **History lives on your container.** If your Javis container is rebuilt, the
  list of past ingests starts over. Your wiki pages are not affected — those
  live on the server.
