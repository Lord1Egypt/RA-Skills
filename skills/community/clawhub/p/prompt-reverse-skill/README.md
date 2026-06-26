# Prompt Reverse Skill

A multimodal AI system that converts images into structured prompts for generative models (Stable Diffusion, Midjourney, DALL·E).

---

## Overview

This project implements a complete AI pipeline that:

- Analyzes images using a vision model  
- Extracts structured semantic features (JSON)  
- Classifies visual types (photography, illustration, etc.)  
- Generates optimized prompts for multiple AI models  
- Provides a web interface for real-time interaction  

Unlike typical AI demos, this project focuses on **prompt engineering and system design**, not just API calls.

---

## Demo

Upload an image → Automatically generate prompts

Features:

- Image preview  
- Multi-model prompt generation  
- Copy-to-clipboard support  

---

## Architecture

    Image Input
    ↓
    Analyzer (Vision Model)
    ↓
    Structured Data (JSON)
    ↓
    Classifier (7 types)
    ↓
    Prompt Builder (NLG)
    ↓
    Multi-model Prompts
    ↓
    Web Interface

---

## Features

- Multimodal processing (image → text)  
- Structured semantic extraction  
- Category-aware prompt generation  
- Negative prompt optimization  
- Multi-model support:
  - Stable Diffusion  
  - Midjourney  
  - DALL·E  
- Web demo (Flask)

---

## Tech Stack

- Python  
- Flask  
- OpenAI API  
- HTML / CSS  
- Prompt Engineering  

---

## Project Structure

    prompt-reverse-skill/
    │
    ├── core/
    │   ├── analyzer.py
    │   ├── classifier.py
    │   ├── prompt_builder.py
    │   ├── pipeline.py
    │   └── templates.py
    │
    ├── web/
    │   ├── app.py
    │   └── templates/
    │       └── index.html
    │
    ├── examples/
    │   └── demo.py
    │
    ├── SKILL.md
    └── README.md

---

## Installation

git clone https://github.com/YOUR_USERNAME/prompt-reverse-skill.git  
cd prompt-reverse-skill  

pip install -r requirements.txt  

---

## Setup

Create a `.env` file:

OPENAI_API_KEY=your_api_key_here

---

## Run Demo

python -m web.app  

Open in browser:  
http://127.0.0.1:5000  

---

## Example Output

a cluster of fresh blueberries with green leaves, stylized text overlay,  
clean composition, centered layout,  
macro photography, bright natural lighting,  
high detail, realistic texture,  
(best quality:1.2), ultra detailed, 8k  

---

## Key Design Highlights

- Structured → Natural Language Transformation  
- Category-aware Prompting  
- Negative Prompt Optimization  
- Modular Pipeline Design  

---

## Skill Integration

This project is also published as a Skill.

- Input: image  
- Output: structured prompts  

---

## Future Work

- Better UI (React / Tailwind)  
- Prompt scoring system  
- Support for more models  
- Batch processing  

---

## Author

Kewei Zhan  
USC MS Computer Engineering  

---

## License

MIT License