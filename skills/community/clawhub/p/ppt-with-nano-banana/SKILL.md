# ppt-with-nano-banana

Create whiteboard hand-drawn style presentations using Nano Banana Pro for image generation and PptxGenJS for PPT creation.

## Overview

This skill combines:
- **Nano Banana Pro** - Generate whiteboard hand-drawn style images for each slide
- **PptxGenJS** - Create professional PPT with images as full-slide backgrounds

## Design Principles

### 1. Whiteboard Hand-Drawn Style
- Every slide uses a whiteboard-style background image
- Hand-drawn marker lines with slight sketchy appearance
- Clean white background, professional presentation style

### 2. Chinese Content First
- All content in Chinese as primary language
- English as notes in parentheses, e.g., "智能体（Agent）"
- Clear, concise, presentation-ready text

### 3. Strategic Color Usage
Use colors purposefully to highlight key points, not for decoration:

| Color | Usage | Example |
|-------|-------|---------|
| 🔴 **Red** | Critical issues, important concepts, warnings | "上下文丢失", "存储层" |
| 🟢 **Green** | Normal flow, correct practices, success | "记忆管理层", working state |
| 🔵 **Blue** | Technical components, architecture elements | "应用层", API interfaces |

### 4. Clean & Professional
- Clear visual hierarchy
- Minimalist design with plenty of white space
- Suitable for professional presentations

## Workflow

```
User Request
    ↓
Generate Images (nano-banana-pro)
    - Create whiteboard-style image for each slide
    - Use strategic colors (red/green/blue) for emphasis
    - Chinese content, clean professional style
    ↓
Create PPT (pptxgenjs)
    - Set up 16:9 layout
    - Add each image as full-slide background
    - Save final presentation
    ↓
Deliver PPT to User
```

## Image Generation Prompt Template

```
Whiteboard hand-drawn style [content description] on clean white background.
[Specific elements with strategic color accents].
Hand-drawn black marker lines with slight sketchy appearance.
All text in Chinese with English notes in parentheses where appropriate.
Professional whiteboard presentation style, minimalist design, plenty of white space.
```

### Example Prompts

**Slide 1 - Title:**
```
Whiteboard hand-drawn style title slide on clean white background.
Large hand-written Chinese title: '智能体（Agent）长期记忆技术架构'.
Subtitle: '让AI拥有持续学习和记忆的能力'.
Red circle accent highlighting the word '记忆' (memory), blue underline beneath '智能体'.
Clean black marker lines, professional whiteboard style.
```

**Slide 2 - Problem Statement:**
```
Whiteboard hand-drawn style diagram on clean white background, all content in Chinese.
Title: '为什么需要长期记忆？'.
Three hand-drawn boxes: Left box with red accent - '上下文丢失（Context Loss）' with broken chain icon and note '每次对话重新开始'.
Middle box with green accent - '知识孤岛（Knowledge Isolation）' with island icons and note '信息无法关联'.
Right box with blue accent - '缺乏个性化（No Personalization）' with person icon and note '无法定制服务'.
Hand-drawn arrows connecting the concepts. Professional whiteboard style.
```

## PPT Creation Code Template

```javascript
const PptxGenJS = require('pptxgenjs');
const path = require('path');

async function createWhiteboardPPT() {
    const pptx = new PptxGenJS();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'AI Assistant';
    pptx.title = 'Your Title Here';
    pptx.subject = 'Your Subject Here';

    const imgDir = '/path/to/your/images';

    // Slide 1
    const slide1 = pptx.addSlide();
    slide1.addImage({
        path: path.join(imgDir, 'slide1-image.png'),
        x: 0, y: 0, w: 10, h: 5.625
    });

    // Slide 2
    const slide2 = pptx.addSlide();
    slide2.addImage({
        path: path.join(imgDir, 'slide2-image.png'),
        x: 0, y: 0, w: 10, h: 5.625
    });

    // Add more slides as needed...

    // Save PPT
    const outputPath = '/path/to/output/Your-PPT-Name.pptx';
    await pptx.writeFile({ fileName: outputPath });
    console.log('✅ Whiteboard style PPT created successfully!');
    console.log('📁 File path: ' + outputPath);
}

createWhiteboardPPT().catch(err => {
    console.error('❌ Error creating PPT:', err);
    process.exit(1);
});
```

## Dependencies

```bash
# Install required packages
npm install pptxgenjs

# For nano-banana-pro (if using locally)
# Ensure uv and nano-banana-pro skill are configured
```

## Best Practices

1. **Image Quality**: Use 2K resolution for crisp whiteboard images
2. **Color Strategy**: Plan which elements need color emphasis before generating images
3. **Text Clarity**: Ensure Chinese characters are clear and readable in generated images
4. **Consistency**: Maintain consistent visual style across all slides
5. **File Organization**: Keep generated images organized by project/date

## Example Output Structure

```
project-folder/
├── ppt_images/
│   ├── slide1-title.png
│   ├── slide2-problem.png
│   ├── slide3-architecture.png
│   └── ...
├── create_ppt.js
└── output.pptx
```

## Troubleshooting

**Issue**: Generated images don't match expected whiteboard style
**Solution**: Refine prompt to emphasize "hand-drawn", "marker sketch", "whiteboard presentation style"

**Issue**: Chinese text not clear in generated images
**Solution**: Specify "clear Chinese characters" and use higher resolution (2K or 4K)

**Issue**: Colors not prominent enough
**Solution**: Specify color usage explicitly: "red accent circle", "green checkmark", "blue underline"
