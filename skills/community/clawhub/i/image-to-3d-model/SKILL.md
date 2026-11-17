---
name: "image-to-3d-part-stl"
description: "Converts 2D images with labeled dimensions to accurate 3D models in STL files. Invoke when the user provides image(s) and metric constraints, requesting a 3D model or STL file. Useful for engineering plotting and 3D printing. "
---

# Image to 3d Part STL Builder

Used to convert user-provided images with dimensions (or combined with text dimension descriptions) into high-precision 2D SVG floor plans and 3D STL print models.
This Skill has modularly encapsulated environmental dependencies and core code templates, allowing the Agent to directly perform secondary development based on the template.

## Trigger Conditions
Invoke this skill when the user uploads one or more images containing parts, sketches, or objects, and provides (or requests to read from the image) related dimension information, with the ultimate goal of obtaining an STL file for 3D printing or an SVG vector graphic for 2D machining.

## Directory Structure
- `requirements.txt`: Contains Python dependencies required for generating 3D models (`numpy`, `trimesh`, `shapely`, `mapbox_earcut`).
- `src/generate.py`: Python code template for generating STL files. When executing tasks, the AI Agent should **rewrite** the contour generation logic in this file based on the image analysis results.
- `SKILL.md`: Skill description and workflow documentation.

## Workflow

### 1. Image and Dimension Analysis
- Carefully observe the image provided by the user to identify core geometric features.
- Extract key dimension information (radius, diameter, width across flats, length, etc.).


### 2. Draw High-Precision SVG (2D Plan) and Request Confirmation [Interactive Loop]
- Use precise mathematical calculations to derive the geometric coordinates of each vertex and arc.
- Write standard SVG code and save it to the user's working directory (e.g., `output.svg`).
- Must use red dimension lines and text to mark key dimensions.
- **Critical Checkpoint**: After generating the SVG, you must **pause execution**, remind the user to view the SVG plan sketch in a browser or software, and ask the user to confirm whether the contour and dimensions meet expectations.
- If the user suggests modifications, loop to modify the SVG until the user fully confirms.

### 3. Modify 3D Model Script Based on Confirmed Blueprint
- **Execute this step ONLY after the user explicitly confirms the SVG sketch.**
- Read the `src/generate.py` template file in this skill directory.
- Based on the user's confirmed dimensions and calculation results, **overwrite** the generation logic for the outer contour point set (`points`) and inner hole point set (`holes`) in the `generate_3d_model` function.

### 4. Environment Setup and STL Generation
- Create a virtual environment in the user's working directory and install required dependencies via `requirements.txt`:
  ```powershell
  python -m venv venv
  ./venv/Scripts/pip install -r <path_to_skill>/requirements.txt
  ./venv/Scripts/python <path_to_skill>/src/generate.py --output part.stl --thickness 2.0
  ```
- After confirming the STL file is successfully generated, inform the user of the file path.

### 5. Iteration and Fine-tuning
- Respond to the user's actual machining/printing test feedback (e.g., "side wall is too thin", "hole is too tight", etc.).
- Modify geometric parameters and tolerances, synchronously update the SVG file and `generate.py` script, and rerun the script to generate a new STL model.

## Rules
- Use the language that the user asked for.
- If there is any agreement required, ask the user first.