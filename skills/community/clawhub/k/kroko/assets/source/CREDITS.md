# Logo source and credits

## The photograph

`croc_front.jpg` — a large crocodile facing the camera with its mouth open.

- **Title:** A large crocodile faces the camera with its mouth open showing its many sharp teeth
- **Author:** NPS photo (National Park Service)
- **Credit:** [NPGallery](https://npgallery.nps.gov/)
- **Licence:** Public domain
- **Date:** 10 August 2013
- **Source:** https://commons.wikimedia.org/wiki/File:A_large_crocodile_faces_the_camera_with_its_mouth_open_showing_its_many_sharp_teeth._(e50fa56e-28cc-4925-b2ae-ed75c1c20fe2).jpg
- **Keyword:** Everglades

The headline image used here is a 1920 px Wikimedia thumbnail of the original.

Public domain means no permission is required and no attribution is legally necessary.
It is recorded anyway, because a logo whose provenance nobody can establish is a
liability the day someone asks.

## How the mark is made

`tools/render_logo.html` renders the mark in a browser using the halftone engine in
`tools/halftone-core.js` (from the `halftone-art` skill). Nothing is drawn by hand.

The crop is explicit, in source pixels: `crop=460,220,1040` — a 1040 px square centred
on the head.

The photograph carries the image; a 45° mono halftone screen carries the print texture,
blended over it at 34% opacity. A screen *alone* was tried first and failed: the photo is
hard-lit from one side, so inverting the tone for bone-ink-on-green dropped the shadowed
half of the face into the ground, and every mapping produced an abstract field rather
than an animal. Blending keeps the animal while the dots do the printing.

Reproduce:

```bash
cd /Users/sakibdalal/Projects/KROKO
python3 -m http.server 8765 --bind 127.0.0.1 &
# then open, and screenshot the 1024x1024 canvas:
# http://127.0.0.1:8765/tools/render_logo.html?mode=1&alpha=0.34&cell=7&status=0
#   &gamma=0.88&brightness=0.04&lin=0.08,0.88&contrast=1.06
#   &tint=saturate(0.5) sepia(0.55) contrast(1.12) brightness(1.02)
```

Palette: ground `#0a2418`, bone `#e8e1ce`, and the photograph's own tones warmed into
that pair. Three inks, no more.
