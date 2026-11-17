# Image to 3D Part STL Builder

[English](README.md) | [简体中文](README_zh.md)

This skill converts user-provided 2D images with labeled dimensions into high-precision 2D SVG floor plans and 3D STL print models. Below is an illustration of the workflow and the outputs generated at each step.

## 1. Input Image and Dimension Analysis
The user provides a reference image of the part along with its core geometric features and key dimension information (e.g., radius, diameter, width across flats, length).

<img src="assets/input_photo.png" alt="Input Photo" width="400">

## 2. Generate High-Precision 2D SVG
Using precise mathematical calculations, we derive the geometric coordinates of each vertex and arc to draw the contour of the part. A standard SVG is generated with red dimension lines marking key constraints. The user reviews and confirms this SVG sketch before proceeding.

<img src="assets/output.svg" alt="SVG Sketch" width="400">

## 3. Generate 3D STL Model
Based on the confirmed dimensions and SVG logic, we modify the template script (`src/generate.py`) to generate a 3D model with the correct extrusion thickness. The model is then exported as an STL file ready for 3D printing.

- **STL File:** [part.stl](assets/part.stl)

Here is a 3D render of the generated STL file:

<img src="assets/part_render.png" alt="STL Render" width="400">

## Workflow Summary
1. **Analyze**: Identify features and dimensions from the image.
2. **Draw**: Generate a precise 2D SVG profile.
3. **Verify**: Ask the user to confirm the SVG profile.
4. **Extrude**: Execute `generate.py` to create the STL file.
5. **Iterate**: Adjust parameters based on actual printing/machining feedback.
