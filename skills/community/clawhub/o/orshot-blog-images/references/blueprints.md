# Blueprints

Each file in `blueprints/` is one finished page (`name`, `canvas`, `elements`) in the Orshot studio schema. Covers are 1200x630, in-article pages 1200x960.

How to use one:

1. Read the file. Keep `canvas` and the element positions.
2. Replace every text and image with the post's content. The example copy ("Vendor A", "Vendor B", "Programmatic SEO") is only there to show line lengths.
3. Replace `{{LOGO_URL}}` and `{{PRODUCT_IMAGE_URL}}`, and swap the accent colors (SKILL.md, Step 2).
4. Put the edited page objects in `pages_data` for `orshot_create_template_design`.

Not installed locally? Fetch them from `https://raw.githubusercontent.com/Orshot-HQ/orshot-agent-skills/main/skills/orshot-blog-images/references/blueprints/<name>.json`.

## cover-prompt-card

1200x630, 20 layers. Title in a white card over a photo, 4 tilted logo tiles, your logo top left. Default for roundups and comparisons.

Dynamic fields: `bg_image`, `card_halo`, `card`, `card_glow`, `overline`, `title_line_1`, `title_line_2`, `plus`, `logo`, `tile_1`, `logo_1`, `tile_2`, `logo_2`, `tile_3`, `logo_3`, `tile_4`, `logo_4`

## cover-product-window

1200x630, 21 layers. Title card on top, a product screenshot in a browser window below, 4 small logos.

Dynamic fields: `bg_image`, `card_halo`, `card`, `title_line_1`, `title_line_2`, `visual_1`, `logo`, `tile_1`, `logo_1`, `tile_2`, `logo_2`, `tile_3`, `logo_3`

## cover-flow

1200x630, 28 layers. Title, then your stack's logos, an arrow to your product, an arrow to the outputs.

Dynamic fields: `bg_image`, `card_halo`, `card`, `card_glow`, `overline`, `title_line_1`, `title_line_2`, `tile_4`, `logo_4`, `tile_3`, `logo_3`, `tile_2`, `logo_2`, `tile_1`, `logo_1`, `logo`, `output_1`, `output_2`, `output_3`, `lab1`, `lab2`, `lab3`

## cover-output-collage

1200x630, 20 layers. Title and logos on the left, three real outputs fanned on the right.

Dynamic fields: `bg_image`, `card_halo`, `card`, `card_glow`, `overline`, `title_line_1`, `title_line_2`, `logo_tile`, `logo`, `tile_1`, `logo_1`, `tile_2`, `logo_2`, `tile_3`, `logo_3`, `tile_4`, `logo_4`, `visual_1`, `visual_2`, `visual_3`

## cover-code-result

1200x630, 22 layers. Title, then a code card joined by an arrow to the output it made.

Dynamic fields: `bg_image`, `card_halo`, `card`, `title_line_1`, `title_line_2`, `card_glow`, `fname`, `code_line_1`, `code_line_2`, `code_line_3`, `status`, `visual_1`, `logo`, `tile_1`, `logo_1`

## cover-prompt-chips

1200x630, 23 layers. A typed prompt with highlighted words in a card, 6 app icons around it. For AI and agent posts.

Dynamic fields: `bg_image`, `prompt_line_1`, `plus`, `prompt_line_2`, `prompt_line_3`, `logo`, `icon_1`, `icon_2`, `icon_3`, `icon_4`, `icon_5`, `icon_6`

## article-hero-stat

1200x960, 32 layers. Chip, two-line headline, two stat cards (big number, label, pill) on the left, a real output with two smaller ones on the right.

Dynamic fields: `w1`, `w4`, `w5`, `w6`, `w9`, `w10`, `w12`, `w13`, `w15`, `w17`, `w18`, `w20`, `w21`, `w23`, `w25`, `w27`, `w29`, `w31`, `w32`

## article-compare-rows

1200x960, 37 layers. Three row cards (mono pill, label, grey value pill, accent value pill) and a note card.

Dynamic fields: `w355`, `w357`, `w358`, `w361`, `w364`, `w365`, `w366`, `w368`, `w370`, `w373`, `w374`, `w375`, `w377`, `w379`, `w382`, `w383`, `w384`, `w386`, `w388`, `w390`, `w391`

## article-picker-grid

1200x960, 43 layers. 3x2 numbered cards: two-line serif title, logo and tool name.

Dynamic fields: `w62`, `w64`, `w65`, `w68`, `w71`, `w72`, `w73`, `w74`, `w77`, `w78`, `w79`, `w80`, `w83`, `w84`, `w85`, `w86`, `w89`, `w90`, `w91`, `w92`, `w95`, `w96`, `w97`, `w98`, `w101`, `w102`, `w103`, `w104`

## article-step-cards

1200x960, 29 layers. Three numbered step cards with a time line, and a note.

Dynamic fields: `w435`, `w437`, `w438`, `w441`, `w444`, `w445`, `w446`, `w448`, `w451`, `w452`, `w453`, `w455`, `w458`, `w459`, `w460`, `w462`, `w463`

## article-before-after-flow

1200x960, 44 layers. Two pipelines of chips with logos joined by arrows (before, after), and a note card.

Dynamic fields: `w105`, `w107`, `w108`, `w111`, `w113`, `w115`, `w116`, `w119`, `w120`, `w123`, `w126`, `w127`, `w130`, `w131`, `w132`, `w134`, `w136`, `w137`, `w140`, `w143`, `w144`, `w145`, `w147`, `w148`

## article-request-result

1200x960, 30 layers. Dark code card, an arrow, the output card with two pills and a caption.

Dynamic fields: `w464`, `w466`, `w467`, `w470`, `w472`, `w473`, `w474`, `w475`, `w476`, `w477`, `w478`, `w479`, `w480`, `w482`, `w483`, `w484`, `w488`, `w490`, `w492`, `w493`

## article-side-by-side

1200x960, 19 layers. Two output cards side by side, each with a pill, a label and one line.

Dynamic fields: `w268`, `w270`, `w271`, `w274`, `w276`, `w278`, `w279`, `w280`, `w282`, `w284`, `w285`, `w286`
