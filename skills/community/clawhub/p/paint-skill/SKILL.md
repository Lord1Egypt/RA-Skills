# paint-skill

Generate simple drawings and save as PNG images using Python PIL/Pillow.

## Requirements

- Python 3.9+ with Pillow installed
- macOS/Linux

## Installation

```bash
# Install conda/mamba if not available
brew install miniforge

# Create Python environment with tkinter support
mamba create -n py39 python=3.9 pip -y
mamba activate py39
pip install pillow

# Or use existing conda environment
conda install -n py39 pillow
```

## Usage

```bash
# Activate conda environment
mamba activate py39

# Run the skill
python /path/to/paint_skill.py [options]

# Options:
#   --demo        Generate a demo rainbow image
#   --park        Generate park scene (boy, cat, dog)
#   --custom      Draw custom scene (specify in code)
```

## Features

- **Interactive Drawing**: Opens a Tkinter window for drawing, saves on close
- **Demo Mode**: Generates sample images (rainbow, park scene)
- **Park Scene**: Boy walking with cat and dog in park

## Files

- `paint_skill.py` - Main Python script
- `SKILL.md` - This documentation