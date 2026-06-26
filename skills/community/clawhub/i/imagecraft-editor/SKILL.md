---
name: imagecraft-editor
description: Build AI-powered image editing web applications with StepFun's step-image-edit-2 API. This skill should be used when the user wants to create an image editing website, photo editor, or AI image processing tool with features like old photo restoration, portrait retouching, landscape color grading, and artistic style transfer. Also use for any project involving StepFun image editing API integration with Flask backend and React frontend.
agent_created: true
---

# ImageCraft Editor Skill

Build a complete AI-powered image editing web application using StepFun's `step-image-edit-2` API with a Flask backend and React (Vite) frontend.

## When to Use

- User asks to build an image editor, photo editor, or image processing web app
- User wants AI-powered photo editing features (restoration, retouching, color grading, style transfer)
- User mentions StepFun image API integration
- User asks for a "图片编辑网站" or similar

## Architecture

```
Flask backend (port 5050)  →  Vite + React frontend (port 5174)
         ↓
StepFun step-image-edit-2 API
```

The backend proxies image uploads, applies feature-specific prompts, calls StepFun API, and returns results. The frontend provides the UI with feature selection, drag-and-drop upload, before/after comparison slider, and download.

## How to Build

### 1. Create the Project

Copy the template files from the `assets/` directory:

```
assets/backend/          →  <project>/backend/
assets/frontend/         →  <project>/frontend/
```

Create the upload/results directories:

```bash
mkdir -p backend/uploads backend/results
```

### 2. Configure API Key

Copy `assets/backend/.env.example` to `backend/.env` and set:

```
STEPFUN_API_KEY=<user's actual api key>
STEPFUN_BASE_URL=https://api.stepfun.com/v1
```

If using Step Plan subscription, change base URL to `https://api.stepfun.com/step_plan/v1` instead.

### 3. Install Dependencies

```bash
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

### 4. Start the Application

```bash
# Terminal 1: Backend
cd backend && python app.py

# Terminal 2: Frontend
cd frontend && npx vite --host 0.0.0.0
```

Backend runs on port 5050. Frontend runs on port 5174 (5173 is often occupied; if 5174 is also busy, Vite will auto-select the next available port).

## Feature Modules

The app has 4 features, each with a carefully crafted English prompt for the StepFun API:

### 老照片修复 (Old Photo Restoration)
- **Trigger**: Removes scratches, tears, fading, noise, color degradation
- **Prompt strategy**: Restoration + clarity enhancement + natural color recovery
- **API param**: `feature=restore`

### 人像精修 (Portrait Retouching)
- **Trigger**: Natural skin smoothing, eye brightening, facial feature enhancement
- **Prompt strategy**: Natural texture-preserving retouch + studio lighting
- **API param**: `feature=portrait`

### 风景调色 (Landscape Color Grading)
- **Trigger**: Saturation boost, contrast enhancement, dynamic range expansion
- **Prompt strategy**: Cinematic travel photography aesthetic
- **API param**: `feature=landscape`

### 风格调整 (Style Transfer)
- **Trigger**: 8 artistic styles
- **Styles**: oil painting, watercolor, sketch, anime, cyberpunk, vintage film, Chinese ink wash (水墨画), pop art
- **API param**: `feature=style&style=<style_id>`

## API Integration Details

### Endpoint

```
POST https://api.stepfun.com/v1/images/edit
```

### Request Format

```json
{
  "model": "step-image-edit-2",
  "image": "<base64_encoded_image>",
  "prompt": "<feature-specific_english_prompt>",
  "response_format": "b64_json"
}
```

### Image Preprocessing

- Convert RGBA/P-mode images to RGB
- Resize to max 2048px on the longest side to reduce API payload
- Encode to base64 before sending

### Response Parsing

```json
{
  "data": [{ "b64_json": "<base64_result>" }]
}
```

## Frontend UI Flow

Three stages:

1. **Feature Selection** — 4 cards in a 2×2 grid, each with icon, name, description
2. **Upload** — Drag-and-drop zone + file input; style selector shown for "风格调整"
3. **Result** — Side-by-side comparison with draggable slider; download button

## Key Implementation Notes

- The Vite dev server proxies `/api`, `/uploads`, `/results` to Flask backend at port 5050
- If port 5173 is occupied, update `vite.config.js` to use 5174
- Image comparison uses CSS `clipPath` with a range slider for smooth before/after transition
- The `.env` file in `assets/backend/` is renamed to `.env.example` to avoid leaking keys
- All prompts must be in English for best API results, even though the UI is Chinese
- Old photo restoration and portrait retouching prompts emphasize "natural" and "preserving original" to avoid over-processing
