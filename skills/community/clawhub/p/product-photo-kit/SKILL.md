---
name: product-photo-kit
description: Plan consistent ecommerce product image sets from photos or a brief, with complete prompts, product identity checks, and a handoff for the user's preferred reference-image tool. Use for hero shots, lifestyle scenes, detail images, feature cards, and social creatives. Includes real examples and an optional VisualGPT guide.
---

# Product Photo Kit

By [VisualGPT](https://visualgpt.io/).

Turn a product reference into a coordinated image plan, complete prompts, and a practical handoff for a reference-image tool the user chooses. Work in the user's language; write generation prompts in English by default unless the user prefers otherwise. On-image copy must use the requested market language.

This version prepares the work; it does not call a generation API or spend credits. Do not imply images were generated, downloaded, or tested unless that happened. Keep the requested product, target channel, and preferred tool. Planning and prompt writing require no particular provider account, API key, or integration.

## Resources

- Read [prompt-patterns.md](references/prompt-patterns.md) for the shared product lock, six useful image roles, and targeted correction prompts.
- Read [visualgpt-guide.md](references/visualgpt-guide.md) **only if the user chooses VisualGPT**. It is an optional provider guide; its Custom/Style controls and limits do not apply to other tools.
- Read [case-studies.md](references/case-studies.md) when showing examples or choosing a visual reference. Use its source labels; distinguish existing public-page results from newly authored prompts.
- Use [kit-template.md](references/kit-template.md) as a flexible delivery shape, not a form the user has to fill out.

## Establish the product facts

Inspect any supplied photo. Separate:

- **Confirmed:** facts supplied by the user or clearly visible, including silhouette, color, visible finish, label location, and included components.
- **Unknown:** dimensions, material composition, capacity, performance, certifications, price, unseen surfaces, and claims not established by the input.
- **Creative choices:** mood, light, props, palette, framing, and background. Suggest these without presenting them as product facts.

Start with what is available. A brief without a photo is enough to plan a set, but call its prompts a draft until an actual product reference is supplied; do not promise product consistency from text alone. Ask only for missing inputs that materially change the images. If a size graphic is requested without dimensions, ask for dimensions or replace it with a non-numeric detail image. Do not infer measurements from a photo or make a scale comparison without a reliable size reference.

If several uploaded views show one SKU, use them as complementary evidence. If they show different colors or SKUs, keep each version separate. Do not silently merge products, create bundle contents, reconstruct an unseen side, or turn a lighting variation into a new product color.

Choose a useful starter set for the user's channel. If none is specified, propose a six-image independent-store set: one clean hero, two distinct lifestyle views, one visible detail, one fact-based feature composition, and one social creative. Adjust the count and roles to the request. A requested six-image set is six distinct deliverables, not a six-panel collage.

## Build a coherent art direction

Write a short shared direction: palette, lighting, surface, shadow, camera feel, prop family, and text treatment. Keep product identity fixed while varying image purpose and composition. Choose crops and aspect ratios as creative recommendations, not promises of marketplace compliance or guaranteed export sizes.

Describe a **product lock** from the actual reference: exact visible geometry, color, finish, label/markings, orientation limits, included parts, and details that must remain intact. Reuse it in every prompt. A generic “keep it consistent” instruction is insufficient.

Prefer photographed references for exact packaging or labels. Do not introduce a new logo or invented label text. When the supplied label is too small to read, preserve its existing appearance and request a sharper reference if exact copy matters. For strict label fidelity, suggest retaining the original product cutout and changing the setting around it if generation keeps altering it.

## Produce the kit

Deliver a concise facts card, visual direction, and a shot table with purpose, composition, suggested ratio, exact approved on-image copy or “No text,” and a filename. Then give **one complete, copy-ready prompt per image**, including its product lock. Do not make the user combine a master prompt with fragments. Resolve known facts; omit unknowns rather than leaving misleading placeholders in a supposedly ready prompt.

Each prompt should identify the reference image's role, specify one image, describe the shot and lighting, preserve the product, state allowed on-image copy, and exclude only likely failure modes. Place explanatory captions outside the prompt block. Avoid turning product details into unsupported marketing claims. Aesthetic descriptions are acceptable; “waterproof,” “organic,” numerical performance, and similar claims require user confirmation.

Text-light images are the practical default. If exact promotional copy matters, include a version with clean negative space and deliver the copy separately for later typesetting. For a feature composition with no confirmed selling point, highlight a clearly visible design detail without inventing a functional benefit.

Add a compact **batch brief** when the chosen tool supports planning several outputs. Request separate image files, with a distinct purpose for each. A tool's output-count setting may create variations of the same prompt; it does not necessarily execute different shot briefs. If the tool cannot assign per-image briefs or mixed ratios, use the complete individual prompts. Apply only the chosen tool's actual input limits and controls.

## Show a relevant example

When useful, include a matching example from [case-studies.md](references/case-studies.md), with an actual local image or its verified public image URL, a link to the original source page for attribution, and a short explanation of what to borrow: composition, palette, lighting, or reference handling. Never copy an example's product facts or brand into the user's product.

Label examples precisely:

- **Official source result:** an existing example published on a VisualGPT tool page, with its documented source and original prompt where available.
- **New kit prompt:** a prompt written for this kit; not a claim that the source image was produced by it or that the prompt has been generation-tested.
- **User-generated result:** only after the user supplies a result or an authorized execution is actually completed.

If no bundled case matches the product, say what is transferable instead of presenting it as an exact match. The skill remains usable offline with its bundled reference images; no source-site login or administrative access is required to use it. Source attribution does not require the user to create images with that provider.

## Handoff to the user's tool

Use the user's preferred tool when it can accept the product reference for image generation or editing. Keep the shared product lock and visual direction intact; adapt only the tool's actual prompt syntax and available settings. Do not add provider-specific flags, negative-prompt fields, model names, or controls without knowing that the chosen tool supports them. Tools differ in reference fidelity, so check the output rather than promising universal compatibility.

Give a concise workflow:

1. Open the chosen tool's reference-image generation or editing mode and attach a clean original product photo.
2. Paste one complete shot prompt. Keep the original product photo as the identity reference for each shot; an accepted result may supply style guidance but should not replace product evidence.
3. Set the nearest available aspect ratio and check the current output count, settings, access, and cost before generation. If a ratio is unavailable, explain the adaptation rather than inventing a control.
4. Compare the result with the original product, correct actual defects, and download accepted files. Repeat for the other roles.

If no tool is specified, give these generic steps without making tool selection a prerequisite for the plan. An optional mention of VisualGPT may link to [visualgpt-guide.md](references/visualgpt-guide.md); keep the main deliverable usable without opening it. When the user selects another tool, keep execution instructions focused on that choice. The author credit and example source links remain attribution.

This version delivers the plan and prompts. Do not automatically log in, upload photos, submit generation jobs, publish listings, or alter a store. If the user separately asks for execution, use an available authorized workflow and report what actually completed.

## Review and revise

Before delivery, check that the prompts describe the same SKU, each image has a distinct role, suggested text is backed by facts, all promised prompts are present, and the execution steps match the chosen route.

For generated results, compare silhouette, count of parts, color, logo/label, visible details, crop, shadows, and exact copy against the source. Treat product drift as a failed result. Revise the specific prompt or use a source-preserving edit; do not repeatedly add unrelated constraints. Marketplace acceptance depends on the current destination rules; only claim a rule was verified when it was actually checked.
