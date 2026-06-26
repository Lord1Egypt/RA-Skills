---
name: moark-image-gen
description: Generate high-quality images from text descriptions.
metadata:
  {
    "openclaw":
      {
        "emoji":"🖼️",
        "requires": { "env": ["GITEEAI_API_KEY"]},
        "primaryEnv": "GITEEAI_API_KEY"
      }
  }
---

# Image Generator
This skill allows users to generate high-quality images based on text descriptions using an external image generation API(Gitee AI).

## Usage

Ensure you have installed the required dependencies (`pip install openai`). Use the bundled script to generate images.

**Qwen-Image (Default)**
```bash
python {baseDir}/scripts/perform_image_gen.py --prompt "your image description" --model Qwen-Image --size 1024x1024 --negative-prompt "elements to avoid" --num-inference-steps 30 --api-key YOUR_API_KEY
```

**Kolors**
```bash
python {baseDir}/scripts/perform_image_gen.py --prompt "your image description" --model Kolors --size 1024x1024 --num-inference-steps 25 --guidance-scale 7.5 --api-key YOUR_API_KEY
```

**GLM-Image**
```bash
python {baseDir}/scripts/perform_image_gen.py --prompt "your image description" --model GLM-Image --size 1024x1024 --negative-prompt "elements to avoid" --num-inference-steps 30 --guidance-scale 1.5 --api-key YOUR_API_KEY
```

**HunyuanDiT-v1.2-Diffusers-Distilled**
```bash
python {baseDir}/scripts/perform_image_gen.py --prompt "your image description" --model HunyuanDiT-v1.2-Diffusers-Distilled --size 1024x1024 --negative-prompt "elements to avoid" --num-inference-steps 25 --guidance-scale 5.0 --api-key YOUR_API_KEY
```

**FLUX.2-dev**
```bash
python {baseDir}/scripts/perform_image_gen.py --prompt "your image description" --model FLUX.2-dev --size 1024x1024 --negative-prompt "elements to avoid" --num-inference-steps 20 --guidance-scale 7.5 --api-key YOUR_API_KEY
```

## Options
**Sizes:**
- `256x256`  - Small square format
- `512x512`  - Square format
- `1024x1024`(default) - Square format
- `1024x576` - 16:9 landscape
- `576x1024` - 9:16 portrait
- `1024x768` - 4:3 format
- `768x1024` - 3:4 portrait
- `1024x640` - 16:10 landscape
- `640x1024` - 10:16 portrait
- `2048x2048` - High-resolution square format

**Additional flags:**
- `--model` - Specify the model to use. Options include `Qwen-Image` (default), `Kolors`, `GLM-Image`, `FLUX.2-dev`, `HunyuanDiT-v1.2-Diffusers-Distilled`.
- `--negative-prompt` - Specify what elements users want to avoid in the generated image(default: "低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。").
- `--size` - Specify the size of the generated image. Options include `256x256`, `512x512`, `1024x1024` (default), `1024x576`, `576x1024`, `1024x768`, `768x1024`, `1024x640`, `640x1024`, `2048x2048`.
- `--guidance-scale` - Float value to control how closely the model adheres to the prompt (default depends on model).
- `--num-inference-steps` - Integer for denoise steps (default depends on model). Higher values typically increase quality but take longer.

**Model Specific Defaults:**
- `Kolors`: steps 25 (range 20-30), scale 7.5 (range 0-100)
- `Qwen-Image`: steps 30 (range 4-50)
- `GLM-Image`: steps 30 (range 10-50), scale 1.5 (range 0-10)
- `HunyuanDiT-v1.2-Diffusers-Distilled`: steps 25 (range 25-50), scale 5 (range 0-20)
- `FLUX.2-dev`: steps 20 (range 10-50), scale 7.5 (range 0-100)

## Workflow

1. Execute the perform_image_gen.py script with the parameters from the user.
2. Parse the script output and find the line starting with `IMAGE_URL:`.
3. Extract the image URL from that line (format: `IMAGE_URL: https://...`).
4. Display the image to the user using markdown syntax: `🖼️[Generated Image](URL)`.

## Notes
- You should not only return the image URL but also describe the image based on the user's prompt, and claim the hyperparameters used for generation.
- You should always wait for the script to finish executing, don't shut it down prematurely.
- The Lanaguage of your answer should be consistent with the user's question.
- By default, return image URL directly without downloading.
- If GITEEAI_API_KEY is none, the user must provide --api-key argument.
- The script prints `IMAGE_URL:` in the output - extract this URL and display it using markdown image syntax: `🖼️[Generated image](URL)`.
- Always look for the line starting with `IMAGE_URL:` in the script output and render the image for the user.
- You should honestly repeat the description of the image from user without any additional imaginations.
- **Handling User Feedback on Quality**: If the user states the image quality is low or lacks details, you should retry generating with a higher `--num-inference-steps` (e.g. 25 → 30). 
- **Handling User Feedback on Prompt Adherence**: If the user states the image doesn't follow the prompt closely enough or ignores details, increase the `--guidance-scale` parameter (e.g. 7.5 → 15). If they say it's oversaturated or distorted, decrease it.