# Output Modes

Use these patterns to turn ranking data into user-facing results.

## Listener Discovery

Use when the user wants to know what is worth hearing now.

Unless the user explicitly asks for a channel, column, or show page, default this mode to episode-level results even if the user says `热门播客`.

Recommended shape:

1. One short takeaway
2. A ranked or lightly curated list
3. Each item should include:
   - episode name first, or show name only when channel-level wording is explicit
   - genre
   - one or two concrete reasons
   - link

Good reasons:

- strong current ranking
- fresh recent release
- clear topic fit for the user's interest
- recognizable guest or hook from the title

## Creator Benchmarking

Use when the user wants shows to study, compare against, or learn from.

This mode is usually show-level and therefore a good fit for `*-podcasts`.

Recommended shape:

1. A short benchmark summary
2. A list of shows
3. Each item should include:
   - show name
   - genre / host
   - freshness
   - attention signal
   - why it is relevant as a benchmark

Benchmark angles:

- title style
- guest strategy
- publishing cadence
- audience size proxy
- comment intensity proxy

## Curation and Distribution

Use when the user wants a list to recommend, package, or adapt downstream.

If the user is curating “what to hear now”, prefer episodes first.
If the user is curating “which channels to follow”, prefer podcasts.

Recommended shape:

1. A one-paragraph curation angle
2. A list of shows or episodes
3. Each item should include:
   - title
   - podcast name
   - why it fits the brief
   - what makes it easy to recommend or expand on
   - original link

Helpful framing:

- who it is for
- when to listen
- what makes it travel well as a recommendation
- what downstream use it could support, such as a roundup, reading list, or topic packet

## What Not To Do

- do not dump API fields with no editorial help
- do not overclaim that a single ranking equals quality
- do not pretend missing genre data is precise
- do not fetch extra details unless the shortlist is already small
