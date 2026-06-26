# Style Picker

> Source: <https://getdesign.md/>
> Quick reference for choosing a style and routing to the correct full spec.
> The full ask-flow lives in `SKILL.md` (Critical Rule 2). This file is read AFTER the user has chosen.

## Decision Flow

```
User said "use <style>"?  ─yes─→  read styles/style-<style>.md
                          ─no──→  ask via ask_followup_question
                                  ↓
        ┌─────────────┬─────────────┬─────────────┐
        Vercel        Linear        Stripe        Notion
        Raycast       Supabase      Airtable      Apple
        Browse more   Default Shadcn Dark
        ↓             ↓             ↓             ↓
        style-X.md    style-X.md    getdesign.md  pen-format.md
                                                  (Shadcn Dark template)
```

## 1-Line Style Cards

| Style | Mode | Identity | Best for |
|-------|------|----------|----------|
| **Vercel** | Light | B&W precision · Geist · shadow-as-border | Dev tools, deployment, tech marketing |
| **Linear** | Dark | Indigo monochrome · Inter weight 510 · luminance-step elevation | SaaS, task management, dark UI |
| **Stripe** | Light | sohne-var weight 300 · blue-tinted shadows · navy headings | Fintech, payment, premium B2B |
| **Notion** | Light | Warm grays · whisper borders · 4-layer soft shadows | Productivity, docs, content apps |
| **Raycast** | Dark | macOS multi-layer shadows · positive tracking · red punctuation | Productivity, premium dark UI |
| **Supabase** | Dark | No shadows · border-hierarchy depth · emerald accent · 1.00 line-height | Dev portals, BaaS, OSS |
| **Airtable** | Light | Haas Grotesk · near-black pill CTA · full-bleed signature surface cards | Data tools, multi-color SaaS, structured data |
| **Apple** | Light/Dark mix | SF Pro · single Action Blue · alternating full-bleed tiles · museum gallery | Premium consumer products, cinematic marketing |
| **Shadcn Dark** | Dark | Zinc palette · unified token system | Generic UI (default fallback) |

## Selection Question (bilingual)

When asking the user, present this menu:

```
Please choose a design style / 请选择设计风格：

1. Vercel    — Monochrome precision, Geist font / 黑白精准，Geist 字体
2. Linear    — Deep dark, indigo accent / 深黑暗色，靛紫强调
3. Stripe    — Clean white, weight-300 luxury / 白底精致，weight-300 优雅
4. Notion    — Warm minimalism / 温暖极简
5. Raycast   — macOS-native dark, red punctuation / macOS 原生深黑，红色点缀
6. Supabase  — Dev-native dark, emerald accent / 开发者深黑，祖母绿强调
7. Airtable  — Editorial light, near-black pill CTA, signature color cards / 编辑感白底，近黑胶囊按钮，签名色块
8. Apple     — Photography-first, single Action Blue, alternating tiles / 照片优先，单一蓝色，明暗交替
9. Browse more / 浏览更多 → https://getdesign.md/
10. Default Shadcn Dark / 使用默认 Shadcn Dark 风格
```

After the user picks: read `style-<choice>.md`, copy its `variables` block into your `.pen` file.

## When User Cannot Decide

Direct them to **https://getdesign.md/** — visual gallery of 66+ brand styles with category filters (AI / dev tools / fintech / automotive / etc.). They browse, name a style, and you continue.

## Conversion Rules: style-spec → `.pen` variables

1. Copy the `variables` JSON block from the chosen `style-*.md` file directly.
2. For dark-first styles (Linear / Raycast / Supabase): set `theme: { "Mode": "Dark" }` on top-level frames.
3. For Apple (mixed-mode): keep top-level frame `Mode: "Light"`. Apply `Mode: "Dark"` only on dark-tile frames where you want true tile inversion.
4. If the style's font is not available in Pencil, fall back to `Inter` and keep the documented weight + letter-spacing values.
5. For rgba-based borders (Linear / Raycast / Notion): the variable file uses a solid hex approximation. For exact rgba, set `stroke.fill` directly on the frame (skipping the variable).
6. Apple's product shadow (`rgba(0,0,0,0.22) 3px 5px 30px`) and Airtable's sub-system rules (pricing-only `pill` radius) must be applied at the component level, not the variables level.

## See Also

- [`pen-format.md`](pen-format.md) — variables block syntax
- [`design-tokens.md`](design-tokens.md) — token system, theming
- Each `style-*.md` — full spec, copy-ready variables block, component recipes
