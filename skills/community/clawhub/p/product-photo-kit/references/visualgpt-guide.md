# Optional: VisualGPT browser workflow

Use this guide only when the user chooses VisualGPT. The main Skill and its prompts can be used with other reference-image tools. The controls and limits below describe this provider only.

Verified: **2026-11-18**. Control names below use the English interface. Settings, account access, and credit costs can change; use the current page as the final reference.

## Choose the route

| Need | Use |
| --- | --- |
| A specific product photo, background, or lifestyle scene with a ready-to-paste prompt | [AI Product Photography](https://visualgpt.io/ai-product-photography), **Custom** tab |
| A planned group of hero images or detail images with an editable design proposal | [AI Product Detail Page Generator](https://visualgpt.io/product-detail-page) |
| Images for Shopify or another independent storefront | The **Custom** photo route, with the store's required composition and aspect ratio in each brief |

The detail tool currently offers Amazon, Shopee, eBay, TEMU, Lazada, TikTok, Ozon, and Taobao under **Target Platform**. Shopify is not currently a selectable platform. Do not invent a Shopify option or select a different marketplace as if its requirements were equivalent.

## Prepare the source

Use a sharp photo with the complete product visible and a simple background. Keep the original source available for every shot so the product's shape, color, label, and packaging remain the reference. If more views are needed, use additional real photos of the same product rather than inventing hidden details.

Both tools accept JPG, JPEG, PNG, and WebP. The current upload limit is 16 MB per image. Use one source image for the photo route; the detail tool accepts up to four product photos. Follow the current upload control if these limits change.

## Route A: one prompt per product photo

1. Open [AI Product Photography](https://visualgpt.io/ai-product-photography) and upload the source photo.
2. Select **Custom**. Paste the prompt for the specific shot into the text area. The prompt limit is **4096 characters**; shorten or split longer briefs into separate runs.
3. Open the settings control beside **Generate**. Choose **Aspect Ratio** and **Number of images** from the available options. For a planned kit, one image per prompt makes it easier to assign a distinct role to each output.
4. Check the credit amount shown on **Generate** and confirm the selected output count. Generate, wait for the result, and compare it with the source.
5. Download the accepted image using its download control. Repeat with the next shot's prompt and the same original source photo.

**On VisualGPT Product Photography, use Custom for written prompts.** The separate **Style** tab offers Studio, Lifestyle, Minimal, Luxury, Natural, and Creative presets. In Style mode, the tool uses the selected preset and does not submit the custom prompt. Choose Style when intentionally using a preset; choose Custom when executing a written shot brief.

For a white-background hero, lifestyle scene, or detail crop, use a separate prompt for each intended result. Request the exact background, framing, lighting, and text treatment in that prompt. Generating several variations from one prompt does not assign a different planned shot to every variation.

## Route B: analyze a group, review, then generate

1. Open [AI Product Detail Page Generator](https://visualgpt.io/product-detail-page). Under **Product Photos**, upload the source photo and, optionally, additional real views of the same product. The **Guide** button shows recommended and unsuitable source-photo examples.
2. Select **Hero Images** or **Detail Images**. Run these modes separately when the kit needs both. Each mode has its own analysis and generation run.
3. Choose the actual destination under **Target Platform** when it is available. If the intended storefront is not listed, use Route A and describe its requirements explicitly.
4. Paste the product facts, confirmed selling points, shared visual direction, and requested shots into **Hero Image Brief**. This field retains that label in both modes. It is required and accepts up to **4096 characters**. Keep copy and specifications grounded in information supplied by the user.
5. Select **Output Language**. Choose **No Text** for images that should contain no added copy. Otherwise, use the intended language and include only confirmed text in the brief.
6. Open settings and confirm **Aspect Ratio** and **Number of images**. Changing the image mode or platform can update the aspect ratio, so check it after those choices.
7. Click **Analyze** and wait for **Design Blueprint** to finish. Analysis prepares an editable proposal; it is not the final image output.
8. Expand and review the blueprint's sections. Use the edit icon to correct the product description, scene, copy, or layout, then select **Save**. Remove unneeded image sections with the delete icon where available. Keep the shared visual direction consistent across the remaining sections.
9. Check the final **Generate N images** count and displayed credit amount. Generate, review every image against the original product and brief, and download the accepted results.
10. If both hero and detail groups are required, return to the form, choose the other mode, and repeat with its matching brief.

Do not treat the generated blueprint as verified product information. Correct invented materials, dimensions, accessories, certifications, performance claims, or packaging text before generating images.

## Settings, access, and credits

- These tool pages provide aspect-ratio and output-count settings. Use the tool's current default model; do not instruct users to find a model selector, quality control, or 4K option that these pages do not expose.
- Output-count access depends on the account. At verification, the detail tool offered 1–12 outputs and the photo tool offered 1–4, with counts above one restricted to paid accounts. If the desired count is unavailable, prepare the same kit as individual Route A runs.
- Check the current **Generate** button and account balance before submitting each run. Do not promise a fixed credit price, unlimited generations, or a complete free multi-image kit. If the page requests sign-in or additional credits, let the user resolve that requirement before continuing.
- The selected platform and ratio are starting settings. Review the destination's actual image requirements and the resulting file before using it in a listing.

## Correct a result without changing the product

Address one visible problem per revision and keep the original product photo as the source of truth.

| Problem | Next action |
| --- | --- |
| Product shape, color, logo, or packaging changed | Return to **Custom**, use the original source again, and specify the exact feature to preserve. Simplify the scene if it competes with product accuracy. |
| Background, lighting, or framing misses the brief | Revise that part of the prompt only: for example, request a plain white background, softer contact shadow, or wider margin while preserving the product. |
| An accessory or unsupported feature appeared | Explicitly remove that item from the revised prompt or blueprint. Keep only the product and confirmed included items. |
| Text is wrong, garbled, or invented | Correct the exact copy in the blueprint, or choose **No Text** and add verified copy later. Do not guess unreadable label text from the image. |
| Only one image in the set fails | Rerun that shot through Route A with its own prompt. Keep the shared lighting, palette, and composition rules from the accepted images. |

For a local correction to an otherwise useful image, [AI Image Editor](https://visualgpt.io/ai-image-editor) is another available tool. Upload the image and describe the specific correction, preserving the product and the parts already accepted. Inspect the edited result before replacing the previous version.

## Optional skincare example brief

This provider-specific version of the bundled skincare batch plan uses **Detail Images**. Select the actual supported destination and **Output Language → No Text**. Choose a shared ratio and account-supported output count; review the analysis before generating. Use individual Custom runs when different ratios are needed. This brief is newly authored and has not been generation-tested.

```text
Mode: Detail Images. Create six separate coordinated product images, not a six-panel collage. Product facts: the supplied reference shows an amber-toned cylindrical bottle, white dropper cap, warm label, and AUREVA lettering. Preserve exact visible shape, cap geometry, color, label artwork and product count. The bottle stays closed. No rear view, extra packaging, or invented small label text. Shared direction: amber, warm peach and ivory, soft upper-left light, natural contact shadows. No added text. Shots: 1) clean full-product studio view on ivory; 2) warm-stone vanity with a distant cream towel; 3) matte peach setting with a distant amber glass panel; 4) close view of the visible cap and upper label; 5) bottle on the right with clean space on the left; 6) vertical bottle composition with clear space above. Do not add skin portraits, ingredient concentrations, capacity, efficacy, tests, certifications, prices, discounts, liquid splashes or product application. Review the Design Blueprint before generating; remove any unsupported claims. All ratios follow the shared setting for this run; use the individual Custom prompts for mixed ratios.
```
