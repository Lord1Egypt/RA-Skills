---
name: photo-analyzer
description: Analyzes an uploaded photograph, provides detailed feedback on exposure, focus, composition, lighting, and suggests concrete camera settings and shooting technique. Generates a simulated improved image based on the recommendations.
agent_created: true
---

# Photo Analyzer

## Overview

This skill processes a user‑provided image, extracts visual characteristics (exposure, focus, color balance, composition), returns text suggestions for camera parameters and shooting technique, and optionally produces a simulated version of the corrected photo.

## Task‑Based Structure

### 1. Analyze Photo
- Detect key attributes: exposure level, focal point, rule‑of‑thirds compliance, dynamic range, noise.
- Identify common issues: over‑/under‑exposure, blur, poor lighting, distracting background.

### 2. Suggest Adjustments
- Recommend ISO, shutter speed, aperture, white‑balance, and lighting improvements.
- Offer composition advice (framing, angle, foreground/background, leading lines).
- Provide actionable tips for post‑processing.

### 3. Simulate Improved Photo (optional)
- Use a generative image model to apply suggested adjustments and render a preview.
- Return the simulated image alongside the textual advice.

## Resources

### scripts/
- `analyze_image.py` – placeholder script using OpenCV/ML to extract attributes.
- `suggest_adjustments.py` – logic to map analysis results to camera settings and composition tips.
- `simulate_image.py` – stub for invoking an image‑to‑image model (e.g., stable diffusion).

### references/
- `photography_guidelines.md` – curated best‑practice notes on exposure, composition, and lighting.
- `model_usage.md` – instructions for calling the image generation model.

### assets/
- Example asset files (e.g., sample before/after images) can be placed here.

---