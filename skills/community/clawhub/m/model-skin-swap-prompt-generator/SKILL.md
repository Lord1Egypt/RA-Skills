---
name: model-skin-swap-prompt-generator
description: Generate skin swap prompts for model images, producing precise AI skin replacement instructions based on user-specified target skin tone/region while preserving original clothing, lighting, background, hairstyle, and composition. 
---

# Model Skin Swap Prompt Generator

Generate precise model skin swap prompts adapted to aesthetic standards of different countries and regions.

## Use Cases

Use when users need "model skin swap", "change skin tone", or "model skin tone change".

## Workflow

### 1. Parse Requirements

Extract from user input:
- **Target Skin Tone**: e.g., Asian cool fair, Western tan, Middle Eastern olive, South Asian honey, African deep brown, etc.
- **Target Region**: e.g., China/Japan/Korea, Europe/Americas, Middle East, Southeast Asia, South Asia, Africa, etc.
- **Reference Image** (optional): If the user uploads a model image, use the `image` tool to analyze original image features

### 2. Generate Prompt

The generated prompt must meet the following requirements:

#### Skin Tone Replacement
- Focus on model skin tone and posture, excluding clothing and product details
- Seamlessly replace skin tone while preserving original clothing, lighting, background, hairstyle, and composition
- New skin tone should be natural and realistic, matching target region facial features (eye shape, nose bridge, jawline, skin tone)
- Avoid exaggerated stereotypes

#### Style Preservation
- Maintain high-definition commercial fashion photography style
- Optimize posture to better suit the character after skin swap
- Reflect popular aesthetic standards of the target country

### 3. Output

Output the prompt directly without asking additional questions:

```
Change the model's skin tone in the original image to [target skin tone], [skin tone feature description], with delicate and natural skin texture, strictly preserve original clothing, lighting, background, hairstyle, hair color, and composition, skin tone should be realistic and harmonious, while reflecting the popular aesthetic standards of that country, do not modify the original high-definition commercial fashion photography style
```

## Constraints

- Provide the prompt directly; do not ask the user additional questions
- Prompt should be concise and clear, ready for direct use
- All product details (fabric texture, color, folds, accessories, posture, brand logos) must remain 100% identical
- New skin tone should be natural and realistic; avoid exaggerated stereotypes
- Maintain high-definition commercial fashion photography style