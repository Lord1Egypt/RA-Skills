# Replays

[Chinese edition](https://github.com/gengshupeng/open-x-sys/blob/main/skills/open-x-sys.zh-CN/experience/playground/replays/README.md)

> **For Watch.** A replay is the record of a **real run**, published with the consent of the person who ran it.

**There are no replays yet in this Alpha Preview.** Replays are added only from real runs. Nothing is written to look like a run. When this folder holds only this file, say so plainly and offer the guided tour or Try instead.

## What a replay contains

A replay lets someone watch a run the way it happened:

1. **The sentence typed**, exactly.
2. **The findings, in the order they arrived**, with the time each took.
3. **The route chosen**, and the one line the system gave for choosing it. Forks, and which way was taken.
4. **The deliverable**, as delivered, with its share pack.
5. **The system entry** that was left behind.
6. **What happened next**: the follow-up prompts the person actually sent, if any.
7. **Context**: the model, the host, the date, which dependencies were present, and how long the run took.

## Honesty rules for replays

- **Real runs only.** A replay is never reconstructed, tidied to look faster, or assembled from several attempts.
- **Unedited findings.** Mistakes the run made and corrected stay in.
- **Consent.** The person who ran it approves exactly what is published. Anything personal is removed first, and the personal root is never part of a replay.
- **Chosen, not staged.** A replay may be selected from several real runs because it is a good example. It may not be scripted in advance.
- **Dated.** A replay shows what the system did on that date with that model. Later versions may differ.

## Format

One folder per replay, named by date and subject. Inside: `replay.md` (the items above, in order), the deliverable and share pack as delivered, and the system entry. The website's Watch page reads the same folder.

## Contributing a replay

See `CONTRIBUTING.md`. Sharing a deliverable or a replay is the first rung of the contribution ladder.
