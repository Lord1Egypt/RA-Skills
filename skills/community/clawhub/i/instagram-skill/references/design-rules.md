# Design rules

Numbers are for a 1080 px wide slide. The renderer applies them; this file explains why, so
you can judge a slide the script can't judge.

## Canvas

- **1080x1350 (4:5) JPEG.** The Instagram API accepts 4:5 to 1.91:1 and JPEG only, so this is
  the tallest size that posts through the API. All slides in a carousel use the size of the
  first one.
- **3:4 (1080x1440)** fills the profile grid without cropping, but only for manual upload in
  the app. The API rejects it.
- The profile grid shows a 4:5 post cropped to 3:4, losing about 34 px on each side. Keep cover
  text inside the side margins and it survives.

## Margins and safe areas

- Sides 88 px, top 100 px, bottom 120 px.
- The small creator header (avatar and name) sits top-left on every slide, including photo
  slides. It is the only element that repeats.
- Text starts at the same height (300 px) on every text slide, so nothing jumps when people
  swipe. Only very tall blocks are centred instead.
- Keep important text away from the top-right corner (Instagram's slide counter) and the
  bottom-left corner (the tag icon) when the post is viewed in the app.

## Type

| Role | Size | Limit |
|---|---|---|
| Cover headline | 150 to 200 px serif, 130 to 150 px sans | 8 words, 10 at most |
| Slide headline | 128 px serif, 96 px sans (floor 72 / 64) | 8 words, 2 lines |
| Body | 54 px, never below 40 | 30 words, 45 at most |
| Step number | 164 px sans | |
| Big number | 280 to 340 px | one per slide, with a source |
| List item | 52 px | 7 items at most |
| Tweet card text | 60 px (cover 84) | 280 characters |
| Name, handle | 22 to 26 px | |

At phone size a 1080 px slide shows at roughly a third of its width. 32 px body text ends up
around 11 pt, which is too small to read comfortably; that's why the floor is 40. When text
doesn't fit at the floor, the script warns: split the slide, don't shrink it.

- Accent colour on one to three words per slide, never whole paragraphs.
- Two font families at most: Inter (sans) and Instrument Serif (serif headlines), both bundled
  under the SIL Open Font License.
- No emoji on slides (no emoji font is bundled); emoji go in the caption.

## What reads as a template (avoid)

- A progress bar, slide numbers or a swipe arrow on every slide. The renderer adds a small
  arrow on the cover only.
- A logo on every slide. Use the name and handle; the logo, if any, belongs on the last slide.
- Headline plus a small subline plus an icon plus a button on one slide.
- Six stock photos from six different shoots.
- Floating phone mockups. Show the real screenshot instead.

## Presets

| Preset | Look | Good for |
|---|---|---|
| `editorial` + `light` | Off-white paper, near-black text, one accent | Step-by-step, frameworks, lists |
| `editorial` + `dark` | Near-black, warm white text | The same, for dark brands |
| `editorial` + `"headline_font": "sans"` | Heavy Inter headlines | Bold, punchy lists |
| `notes` + `light` / `dark` | Plain phone-notes look, amber date line | Honest lists, lessons, lo-fi |
| `tweet` + `light` / `dark` | Tweet-card thread (the user's own voice only) | Opinions, short lessons |

Photo slides (`photo`, or a `cover` with an `image`) work with every preset: the photo fills the
slide, the text sits on a soft shade at the top or bottom.

## Spec

```json
{
  "theme": {"preset": "editorial", "mode": "light", "headline_font": "serif",
            "accent": "#D9480F", "name": "plodd", "handle": "@plodd.app", "avatar": "avatar.png"},
  "slides": [
    {"type": "cover", "kicker": "for anyone who restarts every Monday",
     "title": "Missed a day? Your habit is *fine*.", "alt": "..."},
    {"type": "text", "title": "Rule 1: never miss *twice*.", "body": "...", "alt": "..."},
    {"type": "step", "number": "2", "title": "Shrink it on bad days", "body": "...", "alt": "..."},
    {"type": "list", "title": "The 4 rules", "items": ["Never miss twice", "..."], "alt": "..."},
    {"type": "myth", "myth": "A habit takes 21 days", "fact": "Closer to *66 days*.", "source": "...", "alt": "..."},
    {"type": "stat", "number": "66", "body": "days to form a habit, on average", "source": "...", "alt": "..."},
    {"type": "beforeafter", "before": "old.png", "after": "new.png", "caption": "...", "alt": "..."},
    {"type": "tweet", "text": "...", "alt": "..."},
    {"type": "photo", "image": "photos/desk.jpg", "text": "...", "position": "top", "alt": "..."},
    {"type": "screenshot", "image": "screens/app.png", "title": "...", "body": "...", "alt": "..."},
    {"type": "cta", "title": "Send this to the friend who restarts every Monday.", "alt": "..."}
  ]
}
```

- Image paths are relative to the spec file.
- `"\n"` in a headline sets the line break; the renderer shrinks the headline until each
  written line fits.
- A `cover` with `"screenshot"` puts a cropped screenshot in the bottom 45%; with `"image"` it
  becomes a full photo cover.
- `focus_y` (0 to 1) on a photo slide moves the crop up or down.
- Tall phone screenshots are shown wide and run off the bottom edge, like a phone held up.
- With OpenCV installed (`pip install opencv-python`), the script warns when text sits on a face.
