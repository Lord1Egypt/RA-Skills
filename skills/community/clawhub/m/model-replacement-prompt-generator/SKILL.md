---
name: model-replacement-prompt-generator
description: Generate model replacement prompts based on user-uploaded model images, replacing the character and scene while preserving clothing and shoes. 
---

# Model Replacement Prompt Generator

Generate model replacement prompts from images, preserving clothing and shoes while only replacing the character and scene.

## Use Cases

Use when users need "real person to model replacement", "swap person", or "replace model".

## Workflow

### 1. Analyze Image

Use the `image` tool to analyze the user-uploaded image, extracting:
- **Character Features**: Gender, approximate age, appearance characteristics, pose
- **Clothing Information**: Clothing style, color, material, shoe style
- **Season Determination**: Determine the applicable season based on clothing to ensure the new scene matches
- **Original Style**: Overall photography style and atmosphere

### 2. Generate Prompt

Generate prompts based on image analysis results, which must include:

#### Character Replacement
- Gender must match the original image (male→male, female→female)
- Character must be Chinese
- Describe new character features: gender, age, appearance, temperament
- Clearly state "do not change clothing and shoes"

#### Scene Replacement
- New scene season must match the clothing
- Describe background and environmental details
- Maintain the same photography style as the original image

### 3. Output

Output the prompt directly, ≤300 characters:

```
[Prompt]
```

## Constraints

- Prompt ≤300 characters
- Character must be Chinese
- Gender must match the original image
- Must explicitly state "do not change clothing and shoes, only replace character and scene"
- Scene season must match the clothing
- If the user does not provide specific requirements, generate based on the image