# MotuArt Color Engine — crop specs overview (M16 purpose crop)

The live catalog is authoritative — run `scripts/crop-specs.sh` (or `GET
/v1/crop/specs`) to list current ids/sizes. This is a quick orientation to the
three categories and the shipping specs.

## Three categories

- **id_photo** — official ID/passport/visa/license photo standards. Fixed pixel size
  + physical `width_mm`/`height_mm` + `dpi` (embedded on save, so exports print at the
  right physical size). Most declare a `bg_colors` palette for background replacement
  (换底) since these documents require a specific solid background. ID-photo specs may
  also include `compliance`, `upload`, and `print` metadata used by `id-pack`,
  `id-check`, upload optimization, and print-sheet layout.
- **portrait** — professional/editorial portrait framings (headshot to full body).
  Pixel-only, no print standard, no background palette (original background kept).
- **avatar** — square social-avatar framing. Pixel-only, no background palette.

Pass only a `spec` id — the engine auto-detects the face/head and positions it to
that spec's `head_ratio` (crown-to-chin as a fraction of output height) and margins;
you never draw a crop box by hand.

## id_photo specs (fixed background palette, mostly white/blue/red)

| id | Use | Size | Print |
| --- | --- | --- | --- |
| `one_inch` | 简历/证件 general 1-inch | 295×413px | 25×35mm@300dpi |
| `two_inch` | Standard 2-inch | 413×579px | 35×49mm@300dpi |
| `small_two_inch` | Small 2-inch (passport/visa common) | 413×531px | 35×45mm@300dpi |
| `small_one_inch` | Driver's license / some certificates | 260×378px | 22×32mm@300dpi |
| `big_two_inch` | Diploma (blue background common) | 413×626px | 35×53mm@300dpi |
| `id_card_cn` | CN ID card / social security card (GA 461) | 358×441px | 26×32mm@350dpi |
| `shanghai_compulsory_education_cn` | 上海义务教育入学免冠证件照 | 272×354px | 20×26mm@350dpi |
| `college_graduation_image_cn` | 大学生毕业图像信息采集免冠证件照 | 480×640px | 41×54mm@300dpi |
| `national_k12_student_status_cn` | 全国中小学生学籍电子版照片 | 358×441px | 26×32mm@350dpi |
| `passport_cn` | CN passport / HK-Macau-Taiwan permit / CN visa | 390×567px | 33×48mm@300dpi |
| `us_visa` | US visa 2×2 | 600×600px | 51×51mm@300dpi |
| `schengen_visa` | Schengen/UK visa | 413×531px | 35×45mm@300dpi |
| `japan_visa` | Japan visa | 531×531px | 45×45mm@300dpi |
| `canada_visa` | Canada visa/immigration | 590×826px | 50×70mm@300dpi |
| `china_visa` | China visa printed photo | 390×567px | 33×48mm@300dpi; digital upload uses a separate crop |
| `us_passport_printed` | US passport (paper application) | 600×600px | 51×51mm@300dpi |
| `japan_passport` | Japan passport | 413×531px | 35×45mm@300dpi |
| `canada_passport_printed` | Canada passport (paper application) | 590×826px | 50×70mm@300dpi |
| `uk_passport_printed` | UK printed passport photo | 413×531px | 35×45mm@300dpi |
| `uk_visa` | UK visa or permission digital photo | 600×750px minimum | JPG/JPEG, 50KB–6MB |
| `malaysia_passport_photo` / `malaysia_evisa` | Malaysia passport supplied-photo cases / eVISA | 413×591px | 35×50mm@300dpi |
| `thailand_passport_photo` | Thailand passport capture preparation | 413×531px illustrative crop | live capture; not a submission file |
| `thailand_visa` | Thailand visa | 413×531px | 35×45mm@300dpi |
| `vietnam_passport_photo` / `vietnam_evisa` | Vietnam passport / e-visa | 472×709px | 40×60mm@300dpi |
| `philippines_passport_photo` | Philippines passport live-capture readiness reference | 413×531px | 35×45mm@300dpi |
| `philippines_visa_online` | Philippines online visa | 600×600px | digital only |
| `australia_passport_printed` | Australia passport (paper application) | 413×531px | 35×45mm@300dpi |
| `australia_visa_photo` | Australia visa supplied photo when explicitly requested | 35×45mm @300dpi | channel-specific |
| `korea_passport` / `korea_visa` | Korea passport / visa | 413×531px | 35×45mm@300dpi |
| `singapore_passport_online` / `singapore_visa_online` | Singapore passport / visa online | 400×514px | digital only |

Some passport and visa channels capture the applicant live instead of accepting a
prepared file. Specs marked `capture_channel_limited` or `live_capture_only` must
surface that limitation; they are not a substitute for an in-person or in-app capture.
Specs marked `editing_restricted` should be used without grading, smoothing, outfit
replacement, background synthesis, or other appearance-changing processing.

## portrait specs (no background palette)

| id | Use | Size | head_ratio |
| --- | --- | --- | --- |
| `headshot_3x4` | Close face headshot (actor/streamer/résumé) | 900×1200px | 0.55 |
| `profile_4x5` | Professional headshot (LinkedIn/website/business card) | 1200×1500px | 0.42 |
| `bust_3x4` | Chest-up bust portrait (team page/instructor bio) | 1200×1600px | 0.33 |
| `half_body_2x3` | Waist-up half body (magazine-style, needs waist+ in source) | 1200×1800px | 0.26 |
| `three_quarter_2x3` | Knee-up three-quarter body (needs knee+ in source) | 1200×1800px | 0.19 |
| `full_body_9x16` | Full body, vertical poster/social (needs full body in source) | 1080×1920px | 0.13 |
| `banner_16x9` | Wide head-and-shoulders banner (website/video cover) | 1920×1080px | 0.45 |

## avatar specs (no background palette)

| id | Use | Size | head_ratio |
| --- | --- | --- | --- |
| `avatar_1x1` | Square social avatar (WeChat/DingTalk/general) | 800×800px | 0.45 |

## Background replacement (换底)

Only `id_photo` specs declare a `bg_colors` palette (e.g. `{"white": "#FFFFFF",
"blue": "#438EDB", "light_blue": "#D6EAF8", "red": "#FF0000"}` for the CN sizes). Pass a palette name, `default`
(the spec's standard choice), or an explicit `#RRGGBB` as `bg_color` — an
unrecognized name is rejected (the palette *is* the compliance rule for these
documents). Background swap runs a portrait-matting pass on the crop window at source
resolution, so hair/ear edges stay clean (no crude-cutout fringe).

## Framing guarantee

Cropping only repositions the frame (head ratio + margins) — it never stretches or
compresses facial proportions. Wide framings (`half_body_2x3`, `three_quarter_2x3`,
`full_body_9x16`) require the source photo to actually contain that much of the body;
the engine pads (edge-replicate or `pad_color`) rather than invent missing content.
