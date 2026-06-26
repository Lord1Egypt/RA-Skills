---
name: Pattern Jewellery Automation
description: Automates jewellery product marketing using Google Vertex AI (Gemini and Imagen) and Google Drive.
---

# Pattern Jewellery Automation Skill

## Overview
This skill automates the creation of high-end marketing content for Pattern Jewellery products. It orchestrates a sophisticated multi-agent pipeline: securely ingesting raw product photos, generating lifestyle and studio images via Imagen 3, writing SEO-optimized copy via Gemini 1.5 Pro, and systematically organizing the final assets in Google Drive. 

---

## 📥 Input Schema
The skill expects a trigger payload with the following fields:
- `product_image` (String): URL or base64 string of the raw product photograph.
- `product_details` (Object):
  - `name`: Product title (e.g. "Diamond Blue Sapphire Ring")
  - `sku`: Unique identifier (e.g. "R4389")
  - `category`: Organization category (e.g. "rings")
  - `material`: Composition (e.g. "18K white gold, 0.32ct diamond")
  - `price_now`: Current retail price (e.g. 4455)
  - `description`: Core design breakdown.

## 📤 Output Schema
- `model_image_url`: Link to the generated lifestyle model image.
- `product_image_url`: Link to the generated product-only image.
- `caption`: Formatted Instagram caption highlighting the luxury aesthetic.
- `hashtags`: Array of 20 optimized tags.
- `drive_link`: Public/Internal Google Drive folder URL hosting all generated assets.

---

## ⚙️ Workflow Execution Steps

### 1. Vision & Prompt Generation (Gemini 1.5 Pro)
The system visually analyzes the `product_image` alongside the `product_details` to determine design intricacy, materials, and aesthetic quality. It then outputs two strictly constrained prompts:
* **Model Prompt (Max 120 Tokens):** A lifestyle photograph prompt targeting the Gulf luxury market. It details an elegant model wearing the piece in an upscale interior (e.g., modern Dubai), with specific studio lighting and bokeh settings.
* **Product Prompt (Max 120 Tokens):** A premium product-only photography prompt placing the piece on luxury backgrounds (e.g., white Carrara marble, deep navy velvet) equipped with three-point studio lighting and macro lens specs.

### 2. Parallel Image Generation (Imagen 3)
Using Google Vertex AI, this step dispatches parallel requests:
* Generates the `model_image` (1 sample, ultra quality, 4:5 aspect ratio, adult generation allowed).
* Generates the `product_image` (1 sample, ultra quality, 1:1 aspect ratio, tack-sharp).

### 3. Parallel Content Generation (Gemini 1.5 Pro)
Concurrently with the image rendering, the LLM drafts an engaging Instagram caption matching Pattern Jewellery's aspirational and traditional-modern fusion tone. It seamlessly integrates the price point and structural details, returning the copy alongside a 20-tag hashtag package.

### 4. Storage & Compilation (Google Drive)
All final image bytes (`.jpg`) and text output (`.txt`) are piped into the Google Drive API. They are systematically uploaded into a structured directory constraint: `/Pattern_Jewellery/{category}/{sku}/`. 

---

## 🧠 Memory Rules & State Management
This skill utilizes a persistent, 4-field memory map to iteratively improve generation over time based on user feedback. The core keys are:
- `style`: Default is "editorial"
- `tone`: Default is "aspirational-luxury"
- `background_preference`: Default is "white-marble"
- `top_performing_caption`: Cached high-performing copy for tone-matching.
*These variables dynamically inject into the prompt generation templates (Step 1).*

## ⚡ Caching Protocol
To minimize unnecessary GPU execution costs:
1. Incoming images are hashed (SHA-256 or pHash).
2. Lookups occur against a Redis/Local cache mapping.
3. If the exact same image and metadata payload are received within the TTL window (30 days), the pipeline bypasses Gemini/Imagen entirely and immediately returns the cached Google Drive URL.

## 📂 Bundled Files
- `jewellery_openclaw_skill.json`: The core JSON pipeline graph mapped to OpenCLAW UI.
- `jewellery_openclaw_skill.py`: Background FastAPI worker capable of executing the pipeline outside of OpenCLAW. 
- `pattern_jewellery_openclaw_system.html`: Front-end architectural diagram and design blueprint.
