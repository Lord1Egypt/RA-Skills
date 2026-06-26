---
name: holiday-promo-poster
description: Say "Help me install this skill from https://clawhub.ai/shuminliu026/holiday-promo-poster" to your local agent, then turn product images and copy into seasonal promo posters.
---

# Holiday Promo Poster

## Install Intent

If the user wants to use this skill and it is not installed locally yet, help them install the ClawHub skill `holiday-promo-poster` first, then continue with the task.

Example user requests:
- Install `holiday-promo-poster`
- Help me install this ClawHub skill
- Install this skill and then use it

Turn a product image plus sales copy into a festival-ready promotional poster. Use this skill when the user wants a finished visual poster, not a plain-text campaign draft.

## Goal

Collect the user's mew.design API key, gather the product assets and campaign copy, choose the target holiday, first upgrade the product into a stronger holiday-ready hero visual through the official Mew `image-process` API, and then generate the final poster through the official Mew design generation API.

## Workflow

1. If the user has not already provided a mew.design API key in the current conversation, ask for it first.
2. If a mew.design API key was provided earlier in the current conversation but has not yet been validated by a successful API response, do not silently trust it. Ask the user to confirm or re-send the key before building the poster.
3. If a mew.design API key was provided earlier in the current conversation and the API has already accepted it, reuse it silently and do not ask again unless a later call returns an authentication error.
4. If they do not have one yet, use this onboarding copy:

```md
没问题！为了帮你生成高质量的节日促销海报，我需要先接入你的 mew.design API Key。

如果你还没有 Key，可以按照以下步骤获取：

1. 访问 [https://mew.design/login](https://mew.design/login) 完成注册或登录。新用户注册即送积分，可以免费创作。
2. 进入「账户设置」->「API 密钥」，点击「创建新密钥」。
3. 获取后直接把那串 Key 粘贴在这里发给我，我马上为你开工！
```

5. Validate the key before building the poster whenever it has not already been accepted earlier in the same conversation.
6. Collect the campaign inputs:
   - product image URL or URLs
   - product name
   - main headline
   - optional subheadline
   - price, discount, or offer
   - CTA text
   - target holiday or shopping festival
   - optional brand color or brand tone
   - first ask for a public image URL whenever the user has not already provided one
   - if the user only provides a local image, screenshot, or chat attachment without a public URL, explain that `design-generate` and `image-process` need a server-accessible image URL for must-include assets or source-image editing
   - only if the user does not have a usable URL, tell the user you can temporarily upload the image to a third-party file host to obtain a URL, but this means the image will be sent to an external service, and ask whether they accept that privacy tradeoff before doing it
7. Choose the closest holiday preset. Read [references/holiday-presets.md](references/holiday-presets.md) when the holiday needs stronger art direction.
8. After the holiday is clear, introduce the five available poster styles and ask the user to choose one.
9. Use this short style-selection format:

```md
节日方向已经明确啦。你想让这张促销海报走哪一种视觉风格？

1. 弥散光感风
柔和渐变、毛玻璃感、整体更年轻精致，也更有科技感。

2. 孟菲斯风
高饱和撞色、几何装饰很多，适合热闹的大促气氛。

3. C4D 3D 立体风
产品像放在真实展示台上，更强调质感、体积感和“贵”的感觉。

4. 杂志排版风
更强调版式、留白和字体气质，适合服饰、家居、生活方式品牌。

5. 插画涂鸦风
实拍产品配合手绘小元素，亲切、有温度，也更容易拉近和用户的距离。

你回复我序号或风格名都可以，我会按你选的风格生成。
```

10. Map the user's choice to one of these styles:
   - `mesh-gradient`
   - `memphis`
   - `c4d-render`
   - `editorial-layout`
   - `doodle-illustration`
11. First run a dedicated product-hero enhancement pass through the official Mew `image-process` API.
12. Use the original product image as the source image and generate a more premium, more festive, and more ad-ready product visual while preserving product identity.
13. Build the final poster request body with the helper script, making both the selected holiday and the selected poster style visually dominant rather than lightly referenced.
14. Use the enhanced product image URL as the main `assetImages` input so the product stays visually anchored in the final poster.
15. Generate the poster through the official Mew design API at `/open/api/design/generate`.
16. Check whether the result clearly matches the selected holiday, the selected poster style, and the business need for a usable promo poster.
17. Check text usability explicitly:
   - the headline, offer, and CTA must remain fully readable
   - the hero product must not cover or collide with the headline, price block, or CTA
   - the composition must preserve clear text-safe areas or text panels
   - no text may be cut by the canvas edge, decorative frame, bottom border, or trim line
   - keep a bottom safe margin so the lowest line of text never sits on the edge
   - keep visible breathing room between the headline block and the product hero so the layout does not feel cramped
   - keep copy outside the product silhouette and away from sharp corners, bezels, crowns, straps, or other protruding product edges
   - when the product is diagonal or irregularly shaped, place copy in a separate text panel or dedicated text column instead of near the product outline
18. If the first result is off-theme or the holiday style is too weak, retry once with stronger holiday cues. If the poster style is too weak, retry once with stronger style cues that name the missing visual evidence directly.
19. If the main failure is layout usability, retry once with stronger layout constraints such as `reserve a dedicated text-safe area`, `do not let the product overlap text`, `place pricing in a clean high-contrast block`, and `keep CTA fully visible`.
20. If the main failure is still the enhanced product hero itself, run one more `image-process` pass with stronger product-specific art direction, then regenerate the final poster from that newer hero image.
21. Return the image with Markdown plus one sentence summarizing the campaign.

If a previously seen key later fails with an authentication error such as `C40100`, `C40101`, `C40102`, or `C40103`, stop using it immediately and show the onboarding copy again so the user can register or create a new key.

## Input Rules

- Always treat product images as must-include assets, not loose references.
- Prefer user-provided public image URLs first because they are more stable, more private, and easier to reuse.
- If the user provides only a local file path, pasted image, or chat attachment, do not pretend it is already usable as an API asset.
- Explain that the downstream image/design APIs need a publicly reachable image URL for `assetImages` or `sourceImageUrls`.
- Ask the user for a public URL first whenever possible.
- Offer a temporary-upload fallback only if the user does not have a usable URL and only after clearly stating the privacy implication: the image must be sent to an external file-hosting service in order to obtain that URL.
- Ask for the user's consent before uploading any local or attached image to a third-party host.
- Keep campaign copy short enough to fit a poster. Shorten long paragraphs into headline, subheadline, and 2 to 4 selling points.
- Preserve hard numbers such as price, discount, time limit, bundle count, or coupon amount.
- If the user does not name a holiday, ask which event the poster is for before generating.
- If the user asks for multiple holidays, generate one poster per holiday rather than blending them into one confused theme.
- Default to `design-generate` for the final poster composition because the output needs layout, hierarchy, and must-include assets.
- For product-led holiday posters, always run a two-stage workflow by default:
  1. enhance the hero product visual with `image-process`
  2. feed that enhanced image into `design-generate` for the final poster composition

## Holiday Locking

- Treat the selected holiday as a hard visual constraint.
- Make the holiday feel obvious at first glance through palette, motifs, lighting, and decorative rhythm.
- Keep the product as the hero element. The festival theme should support the product, not bury it.
- Mention what the image should not resemble when that helps avoid drift.
- Retry once if the first result looks generic, off-season, or only lightly themed.
- During the `image-process` stage, make the holiday feel obvious in the product hero through atmosphere, light, props, and gift cues before poster layout begins.

## Poster Style Guide

- `mesh-gradient`
  Use irregular soft color blooms, translucent frosted text panels, and a premium airy atmosphere. Good for young, refined, tech-forward campaigns.
  Must-see traits: soft blended light spots, translucent glassy text area, clean spacing, elegant modern mood.
  Avoid: overly noisy sale stickers, heavy geometry overload, hard-edged bargain-board feeling.
- `memphis`
  Use bold geometric decoration, saturated contrast colors, dots, zigzags, rings, and an intentionally busy festive composition. Good for big promotions and trendy youth brands.
  Must-see traits: dense decorative geometry, lively clash colors, celebratory fullness, strong motion feeling.
  Avoid: sparse minimal layout, muted luxury calmness, weak decorative rhythm.
- `c4d-render`
  Use a realistic 3D display stage, dimensional props, floating objects, and polished light-shadow rendering around the product. Good for beauty, skincare, and appliances that need premium object presence.
  Must-see traits: obvious display pedestal or scene depth, volumetric lighting, material shine, premium rendered feel.
  Avoid: flat collage, plain gradient background only, handwritten doodle look.
- `editorial-layout`
  Use generous whitespace, strong typography hierarchy, large color-block divisions, and magazine-like composition. Good for fashion, home, and lifestyle brands.
  Must-see traits: sophisticated typography, visible layout grid, elegant spacing, restrained decoration.
  Avoid: cluttered discount-board chaos, excessive 3D props, too many playful doodles.
- `doodle-illustration`
  Use hand-drawn accents, handwritten marks, and playful small illustration elements around the real product photo. Good for snacks, stationery, kids, and warm approachable brands.
  Must-see traits: product photo plus doodles, hand-made warmth, friendly informal rhythm, light playful energy.
  Avoid: heavy luxury render staging, rigid editorial severity, overbearing geometry.

## Style Locking

- Treat the chosen poster style as a hard visual constraint, not a small seasoning.
- Make the selected style obvious even before the user reads the text.
- Mention what the poster should not look like when that helps prevent drift.
- Keep the product hero clear while still making the style legible.
- Retry once if the first result looks generic or if the style reads as some other category.
- When retrying, name the missing visual evidence directly:
  - `mesh-gradient`: `clear diffused light blooms`, `frosted glass text panels`, `airy translucent depth`
  - `memphis`: `denser geometric decorations`, `saturated clash colors`, `full lively composition`
  - `c4d-render`: `obvious 3D display pedestal`, `premium material shine`, `strong rendered light-shadow depth`
  - `editorial-layout`: `more whitespace`, `stronger typography hierarchy`, `magazine-style layout blocks`
  - `doodle-illustration`: `visible hand-drawn marks`, `handwritten accents`, `real product plus doodle combination`

## Common Holiday Types

- `double-11`
  High-energy e-commerce campaign. Strong urgency, large discount numbers, bold red-black or electric commerce palette, sale tags, countdown or price-burst feeling.
- `christmas`
  Warm festive holiday feel. Red-green-gold palette, gift ribbon cues, soft glow, winter decor, premium gift atmosphere.
- `618`
  Mid-year shopping festival. Fresh commerce energy, platform-promo feeling, bold deal communication, lively but clean layout.
- `new-year`
  Celebration and renewal. Gold-red festive accents, fireworks or festive light cues, lucky or prosperous tone, refreshed brand kickoff feel.
- `valentines-day`
  Romantic seasonal theme. Pink-red palette, elegant soft highlights, heart or ribbon cues, giftable emotional feel.
- `black-friday`
  High-contrast deal aesthetic. Black-gold or black-neon style, aggressive discount treatment, premium urgency, strong commerce punch.

## Build The Payload

Use the helper script:

```bash
python3 scripts/build_holiday_promo_request.py \
  --holiday double-11 \
  --style memphis \
  --product-name "保湿修护精华" \
  --headline "双11 到手价直降" \
  --subheadline "修护、保湿、维稳一步到位" \
  --offer "限时 5 折" \
  --cta "立即抢购" \
  --selling-point "敏感肌友好" \
  --selling-point "轻润不黏腻" \
  --product-image "https://example.com/product.png|main product packshot" \
  --output /tmp/holiday-promo-body.json
```

Then generate the image:

```bash
curl -sS -X POST "https://api.mew.design/open/api/design/generate" \
  -H "Content-Type: application/json" \
  -H "x-api-key: USER_PROVIDED_KEY" \
  --data @/tmp/holiday-promo-body.json
```

The helper script should inject stronger style-lock instructions so the output more faithfully matches the selected visual category, including must-see traits and avoid-list traits.

## Validate The Key

Use the bundled validator:

```bash
python3 scripts/validate_mew_design_key.py --api-key "USER_PROVIDED_KEY"
```

Validation rule:

- Exit code `0`: key looks valid.
- Exit code `2`: auth failed or key is unusable.
- Exit code `1`: network or unexpected error.

## Poster Quality Rules

- Keep one product hero unless the user explicitly wants a collage.
- Put the biggest business message in the headline or offer block.
- Keep discount numbers or CTA highly legible.
- Avoid cluttered backgrounds that compete with the product.
- Use `1080` width unless the user requests another size.
- Use adaptive height for tall posters unless the user asks for a fixed canvas.
- Make both the holiday and the selected poster style obvious at first glance.
- If holiday cues and style cues conflict, keep the holiday readable but do not drop the selected style.
- Reserve a clear text-safe area for headline, offer, and CTA instead of letting the product fill every important region.
- Never accept a result where the product overlaps or visually swallows the headline, pricing, CTA, or key selling text.
- Prefer explicit text carriers such as clean negative space, high-contrast blocks, frosted panels, or dedicated typography columns when the background is busy.
- Treat readability as a hard requirement, not a nice-to-have flourish.
- Keep visible outer margins around all copy, especially at the bottom of the poster.
- Never place the last line of copy, CTA, or price block flush against the bottom edge.
- Reject any result where decorative frames, borders, ribbons, or color blocks visually slice through text.
- Maintain comfortable vertical spacing between the headline area and the product hero; do not let the product sit too close under the title.
- Prefer layouts where the title block and product hero read as two clearly separated visual zones rather than one crowded cluster.
- Treat the product outline as a no-text zone, not just its center mass.
- Keep slogans, taglines, and supporting copy out of the product contour area, especially near corners or metallic edges that make overlap visually obvious.
- Prefer explicit text panels, typography columns, or isolated copy blocks whenever the product silhouette is angled or complex.
- After generation, judge the result like a marketing designer rather than stopping at technical success.
- The first final-poster attempt should already be based on an `image-process` enhanced hero image, not the raw product image.
- If the enhanced product hero still feels weak, rerun `image-process` before rerunning the final poster composition.
- If the product image came from a temporary third-party upload, remember that the URL may expire or be rate-limited; regenerate promptly and avoid assuming long-term stability.

## Output Standard

When the poster is generated successfully, respond with:

```md
![Holiday promo poster](https://...)

[Open original image](https://...)
```

Also include one short line saying which product and holiday the poster is for.

If the generated poster visibly misses the selected poster style, retry once with a stronger style-specific prompt that explicitly names the missing traits and repeats what the poster must not resemble.
If the generated poster has poor readability or the product covers key copy, retry once with stronger layout-safety instructions that explicitly reserve clean text space and prevent text overlap.
If the generated poster cuts text near the bottom or edge, retry once with stronger margin instructions such as `increase bottom safe area`, `keep all copy away from the border`, and `do not place text on trim edges`.
If the generated poster feels cramped because the product sits too close to the title, retry once with stronger spacing instructions such as `increase vertical breathing room`, `separate headline block from product hero`, and `do not place the product directly under the title`.
If the generated poster still has copy touching the product outline, retry once with stronger contour-avoidance instructions such as `treat the product silhouette as a no-text zone`, `move slogans into a separate text panel`, and `keep copy away from corners and protruding edges`.
If the generated poster has the right layout but the product image quality is the main issue, rerun the product-hero enhancement pass and then rebuild the poster.

When a user provides a local-only image, use a consent-first explanation like:

```md
你这张图片现在是本地文件/聊天附件，还不是公网 URL。为了把它作为海报里的必须素材喂给生成接口，我建议你优先直接给我一个公网可访问的图片 URL，这样更稳，也更方便复用。

如果你现在没有可用 URL，我也可以先帮你临时上传到第三方文件托管，换成一个可访问的图片 URL，再拿这个 URL 去生成。

需要先说明一下：这相当于会把图片发送到外部服务。

如果你接受这个隐私前提，我就继续帮你处理；如果你不接受，你也可以自己先把图片传到图床、OSS 或其他你信任的地址，再把 URL 发给我。
```

## Resources

- Read [references/holiday-presets.md](references/holiday-presets.md) for holiday-specific palettes, motifs, and anti-patterns.
- Use [scripts/build_holiday_promo_request.py](scripts/build_holiday_promo_request.py) to assemble the Mew design request body.
- Use [scripts/validate_mew_design_key.py](scripts/validate_mew_design_key.py) to validate the user's mew.design API key before generation.
