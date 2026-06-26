---
name: pick-your
description: "Generates multi-themed food collages (Burgers, Pizzas, Sushi, Salads, Desserts) with circle-masked images. Use when user asks for a collage of specific food categories, layouts with circle-masked images, or when they want to 'pick' items from a curated list."
---

# Pick Your

This skill generates high-quality food collages based on predefined themes.

## Usage

Use the `make_wings_collage.py` script to generate collages. 

```bash
python3 /root/.openclaw/workspace/skills/pick-your/scripts/make_wings_collage.py
```

## Features

- **Collage Layout**: Generates a 3x3 grid of circular-masked images.
- **Dynamic Titles**: Automatically handles "PICK [X] [THEME]" titles.
- **Customizable**: Handles themes like Burgers, Pizzas, Sushi, Salads, and Desserts.

## Themes

- Gourmet_Burgers
- Artisan_Pizzas
- Sushi_Rolls
- Healthy_Salads
- Dessert_Delights
