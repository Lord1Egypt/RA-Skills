# AI Brand Hallucination — Reference

## Problem
AI image models (especially `google/nano-banana-2/text-to-image`) frequently hallucinate brand names and logos on product images. This is a near-universal pattern when generating consumer electronics.

## Observed Hallucinations (from production sessions)
| Image Type | Hallucinated Brand/Text |
|---|---|
| Headphones | "SONY", "Bose", "Sennheiser", "AXIS AUDIO" |
| Gaming mouse | "Razer" (triple-snake logo) |
| Vinyl record sleeves | "ANALOG VIBRATIONS" |
| Smartphones | Fake model names |
| Cameras | Fake brand text |

## Prevention Prompt Additions
Always append these to every product image prompt:
```
no visible branding, no text, no logos, unbranded, generic design
```

## Detection Workflow
After generating each image:
1. Run `vision_analyze` on the saved file
2. Ask: "Is there any brand text or logo visible?"
3. If yes → proceed to edit fix
4. If no → integrate into page

## Fix: Brand Removal via seedream-v4.5/edit
```bash
# Upload original
URL=$(npx @wavespeed/cli upload ./image.png --json | jq -r .url)

# Targeted removal (be SPECIFIC about which object)
PROMPT="Remove all text and brand logos from the [SPECIFIC OBJECT]. Keep everything else identical — same lighting, pose, composition, colors."

npx @wavespeed/cli run bytedance/seedream-v4.5/edit \
  -i prompt="$PROMPT" \
  -i images="[\"$URL\"]" \
  --json --download "./clean-{index}.{ext}"
```

## Key Insight
Generic prompts like "remove all branding" are LESS effective than targeted prompts like:
- "Remove the Razer triple-snake logo from the gaming mouse"
- "Remove the brand text on the vinyl record sleeves"
- "Remove 'AXIS AUDIO' text from the headphone earcup"

## Cost
~$0.04 per edit round. Typically 1-2 edits needed per branded image.
