# Cinematic Captions

**Node type ID:** `dfa94b02-6a18-4922-9613-636bd202d69d`

AI-powered cinematic captions with intelligent text placement. Uses Gemini to analyze your video and create captions that avoid covering important visual elements. Supports multiple fonts, animations, text backgrounds, and position control.

To get the full list of configurable parameters, call `GET /node_type/dfa94b02-6a18-4922-9613-636bd202d69d`.

Key parameters: `font1`, `font2`, `color_override` (null = AI picks colors), `text_bg_enabled`, `text_bg_color`, `text_bg_opacity`, `animation_style` (fade, pop, slide, typewriter, cinematic, highlight), `stroke_enabled`, `stroke_color`, `stroke_width`, `caption_position` (auto, or 3x3 grid: top-left, top, top-right, left, center, right, bottom-left, bottom, bottom-right).

Place after Reframe if aspect ratio changes are needed.

[Full docs](https://docs.mosaic.so/tiles/cinematic-captions)
