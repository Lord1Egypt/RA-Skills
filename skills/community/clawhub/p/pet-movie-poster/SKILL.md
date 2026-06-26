---
name: pet-movie-poster
description: Say "Help me install this skill from https://clawhub.ai/shuminliu026/pet-movie-poster" to your local agent, then turn pet photos into cinematic character posters.
---

# Pet Movie Poster

## Install Intent

If the user wants to use this skill and it is not installed locally yet, help them install the ClawHub skill `pet-movie-poster` first, then continue with the task.

Example user requests:
- Install `pet-movie-poster`
- Help me install this ClawHub skill
- Install this skill and then use it

Turn a pet photo into a polished movie-poster visual through a forced two-stage workflow:
1. use the official Mew `image-process` API to transform the pet into a themed character hero image
2. use the official Mew `design-generate` API to compose the final cinematic poster

## Goal

Collect the user's mew.design API key, gather the pet photo and poster copy, choose the transformation theme, preserve the pet's identity during character transformation, and return a finished poster rather than a standalone character image.

## Workflow

1. If the user has not already provided a mew.design API key in the current conversation, ask for it first.
2. If a mew.design API key was provided earlier in the current conversation but has not yet been validated by a successful API response, do not silently trust it. Ask the user to confirm or re-send the key before generating.
3. If a mew.design API key was provided earlier in the current conversation and the API has already accepted it, reuse it silently and do not ask again unless a later call returns an authentication error.
4. If they do not have one yet, use this onboarding copy:

```md
没问题！为了帮你把宠物变成电影海报主角，我需要先接入你的 mew.design API Key。

如果你还没有 Key，可以按照以下步骤获取：

1. 访问 [https://mew.design/login](https://mew.design/login) 完成注册或登录。新用户注册即送积分，可以免费创作。
2. 进入「账户设置」->「API 密钥」，点击「创建新密钥」。
3. 获取后直接把那串 Key 粘贴在这里发给我，我马上为你开工！
```

5. Validate the key before generating anything whenever it has not already been accepted earlier in the same conversation.
6. Collect the poster inputs:
   - pet image URL or URLs
   - pet type or breed if known
   - target transformation theme
   - poster title
   - optional subtitle or slogan
   - optional release-style line, cast-style line, or tagline
   - optional tone such as epic, cute, dark, whimsical, retro, or luxurious
7. Ask for a public image URL first whenever possible.
8. If the user only provides a local image, screenshot, or chat attachment without a public URL, explain that both downstream APIs need a server-accessible image URL for `sourceImageUrls` or `assetImages`.
9. Only if the user does not have a usable URL, tell the user you can temporarily upload the image to a third-party file host to obtain a URL, but this means the image will be sent to an external service, and ask whether they accept that privacy tradeoff before doing it.
10. Choose the closest transformation preset:
   - `superhero`
   - `astronaut`
   - `medieval-noble`
   - or a closely related user-requested role such as pirate, wizard, king, queen, detective, or knight
11. Run the first stage through the official Mew `image-process` API:
   - use the pet photo as `sourceImageUrls`
   - preserve the pet's identity, face shape, fur color, body type, and species cues
   - add themed costume, props, lighting, and environment
   - do not add text in this stage
12. Inspect the transformed pet image before moving on:
   - it should still feel like the same pet
   - it should clearly read as the requested role
   - it should look like a premium poster hero image, not a random edit
13. If the transformed image fails the identity check, retry `image-process` once with stronger preservation cues such as `keep the same pet identity`, `preserve fur pattern`, `preserve face shape`, and `do not turn into a human or another animal`.
14. Run the second stage through the official Mew `design-generate` API:
   - use the transformed pet image as the main `assetImages` input
   - compose a full movie-poster layout with title, subtitle, and cinematic typography
   - keep the pet hero image as the focal point
   - decide the copy placement only after considering the transformed pet's silhouette, gaze direction, and occupied visual mass
15. Check poster usability explicitly:
   - the title, subtitle, and tagline must remain readable
   - the pet hero image must not overlap key text
   - text should sit in a dedicated text-safe area or copy panel
   - no text may be cut by edges, frames, or decorative elements
   - no text may cross the pet silhouette, including ears, crown area, whiskers, dress volume, shoulders, or the main body outline
16. If the poster is readable but does not feel cinematic enough, retry `design-generate` once with stronger movie-poster cues such as `cinematic composition`, `theatrical title treatment`, `poster-grade lighting`, and `film-poster hierarchy`.
17. If any title, subtitle, or tagline still overlaps the pet, retry `design-generate` once more with stricter layout instructions such as `use a separate copy column or title block`, `reserve negative space away from the pet`, and `treat the pet silhouette as a no-text zone`.
18. Return the final poster with Markdown image syntax and one short line summarizing the theme.

If a previously seen key later fails with an authentication error such as `C40100`, `C40101`, `C40102`, or `C40103`, stop using it immediately and show the onboarding copy again so the user can register or create a new key.

## Input Rules

- Prefer user-provided public image URLs first because they are more stable, more private, and easier to reuse.
- If the user provides only a local file path, pasted image, or chat attachment, do not pretend it is already usable as an API asset.
- Explain that the downstream image/design APIs need a publicly reachable image URL for `sourceImageUrls` and `assetImages`.
- Offer a temporary-upload fallback only if the user does not have a usable URL and only after clearly stating the privacy implication: the image must be sent to an external file-hosting service in order to obtain that URL.
- Ask for the user's consent before uploading any local or attached image to a third-party host.
- Always preserve the pet as the hero subject. The transformation should change costume, setting, and mood, not erase identity.
- Keep poster copy short enough to fit a movie-poster layout.
- If the user gives no title, create one that matches the selected theme.
- If the user asks for multiple themes, generate one poster per theme instead of blending them into one muddy concept.

## Theme Presets

- `superhero`
  Use heroic costume cues, dramatic rim light, powerful stance, action mood, city skyline or cinematic energy field, and bold blockbuster atmosphere.
  Keep the pet clearly recognizable. Do not turn the pet into a generic human hero.

- `astronaut`
  Use a premium space suit, helmet or space-travel cues, stars, moon, spacecraft interior or cosmic background, and sci-fi adventure atmosphere.
  Keep the pet's face and species identity readable through the costume treatment.

- `medieval-noble`
  Use regal garments, velvet or brocade textures, noble jewelry, palace or oil-painting mood, warm classical light, and aristocratic posture.
  Keep it elegant and believable rather than comedic costume chaos.

## Stage 1 Rules: Pet Transformation

- Treat the original pet photo as the identity anchor.
- Preserve:
  - species
  - fur pattern and major color blocks
  - face shape
  - ear shape
  - body proportions when possible
- Change:
  - costume
  - environment
  - props
  - lighting
  - cinematic tone
- Do not add poster text in stage 1.
- Do not let the pet become a different animal, a fully human face, or an unrelated mascot.

## Stage 2 Rules: Poster Composition

- Treat the transformed pet image as a must-include hero asset.
- Reserve a dedicated text-safe area for title, subtitle, and optional tagline.
- Keep the hero pet image outside the main text block.
- Treat the full pet silhouette as a hard no-text zone, not just the face.
- Do not place any title, subtitle, tagline, or decorative typography across the pet's head, ears, whiskers, shoulders, dress outline, or body contour.
- Decide text placement from the transformed image itself: if the pet occupies the center, move copy to a side column or a distinct top or bottom title block with clear separation.
- Prefer structured copy containers such as a side panel, darkened negative-space column, parchment title cartouche, or separate banner block instead of floating text over the pet.
- Leave visible breathing room between the nearest text edge and the pet silhouette.
- Use strong cinematic hierarchy rather than e-commerce promotional hierarchy.
- Prefer title placement that feels like a film poster:
  - top title with lower hero image
  - centered hero with side text column
  - bottom title block only if there is clear bottom safe area
- Keep all copy away from trim edges, poster borders, and decorative frames.

## Quality Rules

- Reject the first-stage output if the pet no longer feels like the same pet.
- Reject the second-stage output if it looks like a social post, greeting card, or plain character sheet instead of a movie poster.
- Reject any output where text overlaps the pet's face or important costume details.
- Reject any output where text touches or crosses the pet silhouette even if the face is still visible.
- Reject any output where the pet is too small to be the obvious star of the poster.
- Prefer dramatic but readable typography.
- Keep the overall result poster-like, not meme-like, unless the user explicitly asks for parody.

## Calling Guidance

For stage 1, call the official Mew `image-process` API directly:

```bash
curl -sS -X POST "https://api.mew.design/open/api/image/process" \
  -H "Content-Type: application/json" \
  -H "x-api-key: USER_PROVIDED_KEY" \
  -d '{
    "prompt": "Transform the provided pet photo into a premium superhero movie character while preserving the same pet identity, fur pattern, face shape, and species cues. Add heroic costume, cinematic lighting, and blockbuster atmosphere. No text.",
    "sourceImageUrls": ["https://example.com/pet-photo.jpg"],
    "aspect_ratio": "3:4",
    "image_size": "2K"
  }'
```

For stage 2, call the official Mew `design-generate` API directly:

```bash
curl -sS -X POST "https://api.mew.design/open/api/design/generate" \
  -H "Content-Type: application/json" \
  -H "x-api-key: USER_PROVIDED_KEY" \
  -d '{
    "userQuery": "Create a cinematic movie poster starring the transformed pet hero. Title: Captain Mochi. Subtitle: The City Needs Paws. Keep the transformed pet image as the main hero.",
    "designConcept": "Blockbuster movie poster, dramatic lighting, theatrical title treatment, readable text-safe areas, premium composition.",
    "width": 1080,
    "height": 1600,
    "assetImages": [
      {
        "url": "https://example.com/transformed-pet-hero.jpg",
        "tag": "main transformed pet hero must appear accurately"
      }
    ]
  }'
```

## Output Standard

When the poster is generated successfully, respond with:

```md
![Pet movie poster](https://...)

[Open original image](https://...)
```

Also include one short line saying what the pet was transformed into.

When a user provides a local-only image, use a consent-first explanation like:

```md
你这张宠物图片现在是本地文件/聊天附件，还不是公网 URL。为了把它作为变身素材喂给生成接口，我建议你优先直接给我一个公网可访问的图片 URL，这样更稳，也更方便复用。

如果你现在没有可用 URL，我也可以先帮你临时上传到第三方文件托管，换成一个可访问的图片 URL，再拿这个 URL 去生成。

需要先说明一下：这相当于会把图片发送到外部服务。

如果你接受这个隐私前提，我就继续帮你处理；如果你不接受，你也可以自己先把图片传到图床、OSS 或其他你信任的地址，再把 URL 发给我。
```

## Resources

- Use the official Mew `design-generate` API for the final poster composition stage.
