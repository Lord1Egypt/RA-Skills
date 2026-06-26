# MasterPiece Clone

**MasterPiece Clone** transfers the visual style of a reference image to your target photo. Upload a reference image with your desired aesthetic (lighting, mood, composition), and the workflow will transform your photo to match that style while preserving your subject.

---

## ✨ Features

- **Style Transfer**: Apply the visual aesthetic of a high-end reference photo to your own images
- **Cinematic Enhancement**: Transform standard photos into editorial-quality images with professional lighting and composition
- **Composition Cloning**: Replicate the lighting, color grading, and mood of a reference image
- **Async Execution**: Robust asynchronous API handling for complex AI generation tasks

---

## 🚀 How It Works

1. **Prepare Two Images**:
   - **Reference Image**: A photo with the visual style you want to transfer (lighting, mood, color grading)
   - **Target Photo**: Your image that you want to transform

2. **Submit in Correct Order**:
   - First parameter (`Image Input`): Reference image
   - Second parameter (`Image Input 1`): Target photo to be transformed

3. **Get Results**: Receive your target photo transformed with the reference style applied

⚠️ **Important: Image order matters!** Swapping the images will produce different results.

---

## 🧪 Example

### Input
```json
{
  "Image Input": "https://example.com/reference-style.png",
  "Image Input 1": "https://example.com/target-photo.png"
}
```

**What happens:**
- The workflow analyzes the reference image's visual characteristics (lighting, color grading, composition)
- It applies these characteristics to transform your target photo
- You receive a new image that maintains your subject while adopting the reference style

### Preview

| Reference Style | Target Photo | Result |
| :---: | :---: | :---: |
| ![Reference](https://cdn.miraskill.cc/__skill_publish_files__/wangyang/adopted_20260324081228_0_compressed.png) | ![Target](https://cdn.miraskill.cc/__skill_publish_files__/wangyang/20251219_200547_ivy_runway_fullbody_916_dramatic_013_compressed450.png) | ![Result](https://cdn.miraskill.cc/__skill_publish_files__/wangyang/generated-kM43NBVXDjluTGUiozmE-0_compressed.png) |

---

## 💡 Use Cases

- **Editorial Photography**: Transform your photos into magazine-quality images
- **Brand Consistency**: Apply a consistent visual style across multiple photos
- **Creative Direction**: Reimagine your photos with the artistic direction of a reference image
- **Professional Enhancement**: Upgrade standard photos with cinematic lighting and mood

---

🤖 Generated with [Pixify](https://ai.ngmob.com)
