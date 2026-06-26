---
name: icon-generator
description: Professional icon and logo generator for apps and websites. Use when user needs to create app icons, favicons, logos, or brand marks. Supports iOS, Android, web standards. Generates high-quality icons with multiple sizes. 图标生成、Logo制作、App图标。
version: 1.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "🎨", "requires": {"bins": ["python3"], "env": []}}}
dependencies: "pip install pillow"
---

# Icon Generator

Professional icon and logo generator for apps, websites, and branding.

## Features

- 📱 **App Icons**: iOS and Android standards
- 🌐 **Web Icons**: Favicon, OG images
- 🎨 **Logo Design**: Brand marks, wordmarks
- 📐 **Multi-Size**: Auto-export all required sizes
- 🎯 **Customizable**: Colors, shapes, styles

## Supported Formats

### iOS App Icons

| Size | Scale | Usage |
|------|-------|-------|
| 1024×1024 | 1x | App Store |
| 180×180 | 3x | iPhone |
| 120×120 | 2x | iPhone |
| 167×167 | 2x | iPad Pro |
| 152×152 | 2x | iPad |
| 80×80 | 2x | iPad Spotlight |
| 58×58 | 2x | iPhone Settings |
| 40×40 | 2x | iPhone Notification |

### Android App Icons

| Size | Usage |
|------|-------|
| 512×512 | Play Store |
| 192×192 | xxxhdpi |
| 144×144 | xxhdpi |
| 96×96 | xhdpi |
| 72×72 | hdpi |
| 48×48 | mdpi |

### Web Icons

| Size | Usage |
|------|-------|
| 512×512 | PWA icon |
| 192×192 | PWA icon |
| 180×180 | Apple touch |
| 32×32 | Favicon |
| 16×16 | Favicon |

## Trigger Conditions

- "Create app icon" / "生成App图标"
- "Make favicon" / "制作网站图标"
- "Generate logo" / "生成Logo"
- "icon-generator"

---

## Icon Styles

### 1. Flat Icon
- Clean, minimal design
- Single color or gradient
- No shadows or effects
- Best for: Modern apps

### 2. Material Icon
- Google Material style
- Bold shapes
- Limited color palette
- Best for: Android apps

### 3. iOS Style
- Rounded square
- Subtle gradients
- Apple aesthetic
- Best for: iOS apps

### 4. 3D Icon
- Depth and shadows
- Realistic look
- Eye-catching
- Best for: Games, entertainment

### 5. Line Icon
- Outline only
- Minimal, clean
- Elegant
- Best for: Productivity apps

---

## Python Code

```python
from PIL import Image, ImageDraw, ImageFont
import os
import math

class IconGenerator:
    def __init__(self):
        self.ios_sizes = [
            ('AppStore', 1024),
            ('iPhone_3x', 180),
            ('iPhone_2x', 120),
            ('iPadPro', 167),
            ('iPad', 152),
            ('iPadSpotlight', 80),
            ('iPhoneSettings', 58),
            ('iPhoneNotification', 40),
        ]
        
        self.android_sizes = [
            ('PlayStore', 512),
            ('xxxhdpi', 192),
            ('xxhdpi', 144),
            ('xhdpi', 96),
            ('hdpi', 72),
            ('mdpi', 48),
        ]
        
        self.web_sizes = [
            ('PWA_512', 512),
            ('PWA_192', 192),
            ('AppleTouch', 180),
            ('Favicon_32', 32),
            ('Favicon_16', 16),
        ]
    
    def _load_font(self, size):
        paths = [
            '/System/Library/Fonts/PingFang.ttc',
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        ]
        for p in paths:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except:
                    continue
        return ImageFont.load_default()
    
    def create_flat_icon(self, symbol, bg_color, symbol_color, size=(512, 512)):
        """Flat design icon"""
        img = Image.new('RGBA', size, (*bg_color, 255))
        draw = ImageDraw.Draw(img)
        
        font = self._load_font(size[0] // 3)
        bbox = draw.textbbox((0, 0), symbol, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x, y = (size[0] - w) // 2, (size[1] - h) // 2
        
        draw.text((x, y), symbol, font=font, fill=(*symbol_color, 255))
        return img
    
    def create_material_icon(self, symbol, color, size=(512, 512)):
        """Material Design icon"""
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Circular background
        margin = size[0] // 10
        draw.ellipse([(margin, margin), (size[0]-margin, size[1]-margin)], 
                     fill=(*color, 255))
        
        # Icon
        font = self._load_font(size[0] // 3)
        bbox = draw.textbbox((0, 0), symbol, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x, y = (size[0] - w) // 2, (size[1] - h) // 2
        draw.text((x, y), symbol, font=font, fill=(255, 255, 255, 255))
        
        return img
    
    def create_ios_icon(self, symbol, bg_color, symbol_color, size=(1024, 1024)):
        """iOS style icon with rounded corners"""
        import numpy as np
        
        # Create base image
        img = Image.new('RGBA', size, (*bg_color, 255))
        draw = ImageDraw.Draw(img)
        
        # Add subtle gradient
        for y in range(size[1]):
            ratio = y / size[1]
            r = int(bg_color[0] * (1 - ratio * 0.2))
            g = int(bg_color[1] * (1 - ratio * 0.2))
            b = int(bg_color[2] * (1 - ratio * 0.2))
            draw.line([(0, y), (size[0], y)], fill=(r, g, b, 255))
        
        # Add symbol
        font = self._load_font(size[0] // 3)
        bbox = draw.textbbox((0, 0), symbol, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x, y = (size[0] - w) // 2, (size[1] - h) // 2
        draw.text((x, y), symbol, font=font, fill=(*symbol_color, 255))
        
        return img
    
    def create_line_icon(self, path_points, color, size=(512, 512)):
        """Line/outline style icon"""
        img = Image.new('RGBA', size, (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        if len(path_points) > 1:
            draw.line(path_points, fill=(*color, 255), width=max(2, size[0] // 50))
        
        return img
    
    def apply_rounded_corners(self, img, radius=None):
        """Apply iOS-style rounded corners"""
        if radius is None:
            radius = img.size[0] // 5
        
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
        
        result = Image.new('RGBA', img.size, (0, 0, 0, 0))
        result.paste(img, mask=mask)
        return result
    
    def export_all_sizes(self, img, output_dir, platform='all'):
        """Export icon in all required sizes"""
        os.makedirs(output_dir, exist_ok=True)
        
        sizes = []
        if platform in ['ios', 'all']:
            sizes.extend(self.ios_sizes)
        if platform in ['android', 'all']:
            sizes.extend(self.android_sizes)
        if platform in ['web', 'all']:
            sizes.extend(self.web_sizes)
        
        exported = []
        for name, size in sizes:
            resized = img.resize((size, size), Image.LANCZOS)
            path = os.path.join(output_dir, f'icon_{name}_{size}x{size}.png')
            resized.save(path)
            exported.append(path)
        
        return exported

# Example
gen = IconGenerator()

# Create iOS icon
icon = gen.create_ios_icon('A', (30, 60, 114), (255, 255, 255))

# Apply rounded corners
icon = gen.apply_rounded_corners(icon)

# Export all sizes
gen.export_all_sizes(icon, 'output/')
```

---

## Usage Examples

```
User: "Create an app icon for my note-taking app"
Agent: Generate icon with notebook symbol

User: "Make a favicon for my website"
Agent: Generate 32×32 and 16×16 icons

User: "Generate all icon sizes for iOS and Android"
Agent: Export 20+ sizes for both platforms
```

---

## Notes

- All icons generated locally with Pillow
- Auto-export all required sizes
- Cross-platform compatible
- Supports Chinese and English symbols
