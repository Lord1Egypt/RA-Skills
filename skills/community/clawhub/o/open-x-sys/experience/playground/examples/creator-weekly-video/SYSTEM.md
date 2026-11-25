# The weekly explainer: where the hours go, and what changed

[Chinese edition](https://github.com/gengshupeng/open-x-sys/blob/main/skills/open-x-sys.zh-CN/experience/playground/examples/creator-weekly-video/SYSTEM.md)

> Constructed example for the OpenXSys Playground. The creator, the channel and all figures are invented.

This is your system for making one explainer video a week. It was opened on 5 October 2026 and last updated on 9 November 2026. It lives in this workspace; nothing about you personally is kept here.

## What it comes down to

**You do not have a writing problem or an editing problem. You have a decision problem: each episode waited two days for you to choose its thumbnail and title, and you chose them last.**

Your own numbers show it (`data/episodes.csv`, weeks 1 to 4 before the change): scripting took about 3 hours and editing about 4, steady every week. What varied, and what pushed publishing from Thursday to Saturday three times out of four, was the gap between "edit finished" and "published", which averaged 2.1 days. Nothing was being done in that gap. The episode was waiting for a title and a thumbnail.

This matters because your retention figures are decided in the first 30 seconds, and the first 30 seconds were being written before you knew what the title promised.

## What we changed, and what happened

One practice is in use: **decide the promise first**. The record, with the weekly results, is `practices/episode.md`.

- Before: script, record, edit, then title and thumbnail.
- Now: title and thumbnail are chosen on Monday, before scripting, from three candidates. The first 30 seconds are written to keep that promise.

After five weeks of the new order: the finish-to-publish gap fell from 2.1 days to 0.3. Retention at 30 seconds rose from 58 percent to 66 percent on average. Total hours per episode did not change much (9.5 to 9.1). The evidence is five episodes, which is few: treat the retention change as likely, not proven.

## What is being watched

If hours per episode rise above 11 for two weeks running, or the finish-to-publish gap goes above one day, look at the practice again. Check by running `code/retention.py` on the latest export; it was last run on 9 November 2026 on the export of 8 November.

## Parts of this system

- `practices/episode.md`: the practice record. Read this to run an episode the current way.
- `data/episodes.csv`: one row per episode, from your own analytics export and your time log.
- `code/retention.py`: recomputes the weekly figures from the CSV. Standard library only. Validated on the nine rows now in the file.

## What you already understand

You were the one who noticed that the gap, not the editing, was what moved the publish day; I had started by looking at editing time. You now pick the three title candidates yourself, without prompting. You have not yet looked at whether topics chosen from viewer comments retain better than topics you pick: you said you were curious about it.

## Most worth doing now

1. **Compare comment-sourced topics with your own (recommended).** Three of the nine episodes came from comments. It is too few to conclude from, and it is the question you raised. It needs one new column in the CSV.
2. Test a second thumbnail on one episode after 24 hours.
3. Leave it alone for four weeks and review on 7 December.

## To continue

Read `practices/episode.md`, then run the script on the newest export and compare with the watch condition above. Any AI can do this from these files.
