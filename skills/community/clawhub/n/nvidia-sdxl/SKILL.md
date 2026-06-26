# NVIDIA SDXL Image Generator

This skill leverages the NVIDIA NIM API to generate high-fidelity, photorealistic, or artistic images using the Stable Diffusion XL (SDXL) model. It allows the agent to create visual assets directly from text descriptions.

## Tools

### generate_image

Converts a detailed text description into a high-resolution PNG image saved locally to the OpenClaw workspace.

**Parameters:**

- `prompt` (string, required): A comprehensive description of the desired image. Include specifics about subject, setting, lighting (e.g., "cinematic lighting", "golden hour"), and artistic style (e.g., "photorealistic", "oil painting", "3D render").
- `negative_prompt` (string, optional): A list of elements to strictly exclude from the generation, such as "blurry, distorted hands, low resolution, text, watermark".
- `width` (integer, optional, default=1024): The horizontal resolution. Supported values include 1024, 768, or 512.
- `height` (integer, optional, default=1024): The vertical resolution. Supported values include 1024, 768, or 512.

**Usage Example:**

"Generate a high-detail cinematic shot of a futuristic Tokyo street under heavy rain, neon lights reflecting in puddles, 8k resolution, photorealistic style."

**Output:**

Returns a success message containing the absolute local file path to the generated `.png` file.

