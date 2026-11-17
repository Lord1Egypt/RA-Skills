# Writing pins

People find pins by searching, and decide in a glance whether the page behind it is worth a click.
Every word does one of those two jobs.

## Keywords

- Start from the page: its title, headings and the words its readers use.
- Search each phrase on Pinterest itself before using it: the results show what people mean by it
  ("moon phases meaning" is mostly astrology, not astronomy).
- Add what people type: the user's own search data, Pinterest's search bar suggestions (type the
  topic and read the list), Pinterest Trends. Never invent search volumes.
- One main phrase per pin, plus one or two close variants ("moon phases", "phases of the moon",
  "lunar cycle"). Different pins for one link can lead with different variants.

## Title (up to 100 characters, about 40 shown)

The phrase first, then the promise. It should read like a page title, not a list of tags.

- Moon phases in order: all 8, from new Moon to waning crescent
- Sourdough starter schedule: feed it once a day, bake on day 7
- Small balcony ideas: 12 layouts for under 4 square meters

Avoid: "AMAZING!!!", all caps, a title that only makes sense next to the image, the same title on
two pins.

## Description (up to 800 characters; the point in the first 500)

One to three plain sentences, the point in the first one (only the start shows in the close-up):
what the page gives, for whom, and one detail that proves it. The
main phrase once, a variant once. End with what to do if it fits ("Save it for your next bake").

> The 8 Moon phases in order: new Moon, waxing crescent, first quarter, waxing gibbous, full Moon,
> waning gibbous, third quarter and waning crescent. The cycle repeats every 29.5 days.

No hashtags, no keyword lists, no "link in bio", no URL (it isn't clickable).

## Alt text (up to 500 characters)

What the image shows, for someone who can't see it, in a sentence or two. Include the words on the
image if they carry the message. Not a second description.

> A full Moon glowing red-orange low over a dark tree line, under the headline: Why we always see
> the same side of the Moon.

## The headline on the image

- 3 to 8 words, the same promise as the title but shorter. It must read at feed size (the preview
  shows it at 236 px wide); `render_pins.py` reports its size in the feed.
- One idea per pin: a number, a result, a question the page answers.
- Patterns that work: "[Number] [things] for [person/situation]", "How to [result] in [time]",
  "[Thing], explained in one picture", "When to [do/see the thing]", "Why [surprising fact]".
- Never promise what the page doesn't deliver.

## Several pins for one link

Change the angle, not just the colours: the result, the steps, a number, a checklist, the photo
alone, a video. Each gets its own picture, headline, title and description. Space them a week
apart (`schedule.py` does it).

## Boards

Specific, named the way people search ("Moon and night sky", not "Stuff I love"), with a one-line
description that uses the phrase. A pin goes to the one board that fits best.
