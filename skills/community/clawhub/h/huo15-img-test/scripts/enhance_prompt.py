#!/usr/bin/env python3
"""
huo15-img-test — T2I 提示词增强脚本 v2.2

核心能力：
1. 88 风格预设（摄影 / 动漫 / 插画 / 3D / 设计 / 艺术 / 场景 / 游戏 / 东方传统 九大类）
2. 意图解析（主体类型 / 画幅 / 构图 / 情绪 / 时间 / 天气 / 季节）
3. 一致性五锁（camera + lighting + palette + aspect + seed）
4. 系列批量模式（-s N：共享锁，差异化动作）
5. 角色设定图模式（--character-sheet：T-pose 多视图，喂给 MJ --cref）
6. 质量档位（-t basic / pro / master）
7. 负向需求识别（"不要 X" / "no X" / "avoid X" 自动入负面）
8. 多模型精细化适配（Midjourney / SD / SDXL / Flux / DALL-E 3）
9. 别名 & 中英混输入（anime / cyberpunk / 原神 / 敦煌 均可）
10. 混合预设 v2.2：`-p A+B --mix 0.6` 加权融合两套风格（赛博+水墨 / 原神+敦煌 ...）
"""

import sys
import os
import json
import re
import argparse
import hashlib
from typing import Dict, List, Optional, Tuple

VERSION = "2.3.0"

# ─────────────────────────────────────────────────────────
# 通用质量 / 负面词
# ─────────────────────────────────────────────────────────
UNIVERSAL_QUALITY = "masterpiece, best quality, ultra detailed, 8k"
UNIVERSAL_NEG = (
    "low quality, worst quality, lowres, blurry, jpeg artifacts, "
    "watermark, signature, text, logo, username, "
    "bad anatomy, bad hands, extra fingers, missing fingers, "
    "extra limbs, deformed, mutated, disfigured, ugly, "
    "out of frame, cropped, duplicate"
)

# 这些预设天然需要 logo / text / signature，把它们从全局负面词中剔除，避免语义冲突
PRESET_NEG_EXCLUDE: Dict[str, List[str]] = {
    "Logo设计": ["logo", "text"],
    "图标设计": ["logo", "text"],
    "表情包": ["text"],
    "复古海报": ["text"],
    "电影海报": ["text"],
    "专辑封面": ["text"],
    "品牌KV": ["text"],
    "信息图": ["text"],
    "水墨": ["signature"],
    "工笔国画": ["signature"],
    "浮世绘": ["text", "signature"],
    "霓虹灯牌": ["text"],
}


def _filter_neg(universal: str, exclude: List[str]) -> str:
    if not exclude:
        return universal
    tokens = [t.strip() for t in universal.split(",")]
    kept = [t for t in tokens if t.lower() not in {e.lower() for e in exclude}]
    return ", ".join(kept)

# ─────────────────────────────────────────────────────────
# 风格预设 — 每个预设 7 个字段
#   tags     风格标签
#   quality  画质标签
#   neg      负面标签（与 UNIVERSAL_NEG 合并）
#   camera   机位 / 镜头（摄影专用，其它留空）
#   lighting 光影锁
#   palette  色板锁（系列一致性关键）
#   aspect   默认画幅
# ─────────────────────────────────────────────────────────

STYLE_PRESETS: Dict[str, Dict[str, str]] = {
    # ========== 摄影 Photography ==========
    "写实摄影": {
        "category": "摄影",
        "tags": "photorealistic, hyperrealistic, dslr photography, sharp focus",
        "quality": "raw photo, detailed skin texture, film grain subtle",
        "neg": "cartoon, anime, painting, drawing, illustration, cgi",
        "camera": "Canon EOS R5, 85mm f/1.4 lens, shallow depth of field",
        "lighting": "professional studio lighting, softbox key light, rim light",
        "palette": "natural color grading, balanced exposure",
        "aspect": "3:4",
    },
    "胶片摄影": {
        "category": "摄影",
        "tags": "analog film photography, film grain, analog aesthetic",
        "quality": "kodak portra 400 film stock, scanned film",
        "neg": "digital, oversaturated, hdr, plastic skin",
        "camera": "35mm film camera, 50mm prime, shot on film",
        "lighting": "natural window light, golden hour",
        "palette": "muted earth tones, slightly faded film colors",
        "aspect": "3:2",
    },
    "黑白摄影": {
        "category": "摄影",
        "tags": "black and white photography, monochrome, high contrast",
        "quality": "silver gelatin print, fine art photography, rich grayscale",
        "neg": "color, colorful, saturated, low contrast",
        "camera": "Leica M6, 35mm f/2, classic reportage framing",
        "lighting": "dramatic chiaroscuro, strong directional light",
        "palette": "pure black and white, deep blacks, crisp whites",
        "aspect": "1:1",
    },
    "人像摄影": {
        "category": "摄影",
        "tags": "portrait photography, shallow depth of field, bokeh background",
        "quality": "flawless skin retouch, detailed eyes, catch light",
        "neg": "full body, wide shot, plastic skin, uncanny",
        "camera": "85mm f/1.4, eye-level portrait, rule of thirds",
        "lighting": "rembrandt lighting, soft key with fill",
        "palette": "warm skin tones, complementary backdrop",
        "aspect": "3:4",
    },
    "时尚大片": {
        "category": "摄影",
        "tags": "high fashion editorial, vogue style, avant-garde styling",
        "quality": "magazine cover quality, haute couture",
        "neg": "amateur, casual, snapshot, cluttered set",
        "camera": "medium format, 50mm, full body or waist-up",
        "lighting": "hard strobe with deep shadows, beauty dish",
        "palette": "high-contrast, bold monochromatic set",
        "aspect": "3:4",
    },
    "美食摄影": {
        "category": "摄影",
        "tags": "food photography, overhead flatlay, appetizing presentation",
        "quality": "detailed steam and texture, drool-worthy, michelin plating",
        "neg": "greasy, unappealing, blurry plate, messy",
        "camera": "macro 100mm, 45-degree angle or top-down",
        "lighting": "soft window light from side, subtle rim highlight",
        "palette": "warm appetite-triggering tones, natural food colors",
        "aspect": "1:1",
    },
    "产品摄影": {
        "category": "摄影",
        "tags": "commercial product photography, clean composition, minimal scene",
        "quality": "crisp reflections, seamless background, advertising grade",
        "neg": "cluttered, messy background, amateur lighting",
        "camera": "90mm macro, eye-level product shot",
        "lighting": "large softbox key, gradient sweep background",
        "palette": "neutral white or brand-matched seamless",
        "aspect": "1:1",
    },
    "微距摄影": {
        "category": "摄影",
        "tags": "macro photography, extreme close-up, micro world",
        "quality": "razor sharp details at micro scale, focus stacking",
        "neg": "soft focus, wide view, lack of detail",
        "camera": "100mm macro lens, 1:1 magnification",
        "lighting": "ring flash or twin macro flash, even diffused",
        "palette": "nature-true colors, intense saturation",
        "aspect": "1:1",
    },
    "航拍摄影": {
        "category": "摄影",
        "tags": "aerial photography, drone shot, bird's eye view",
        "quality": "ultra wide sweeping vista, high altitude clarity",
        "neg": "ground level, close-up, people center frame",
        "camera": "drone camera, 24mm equivalent, top-down or 45-degree",
        "lighting": "natural sunlight, long soft shadows",
        "palette": "earth tones with atmospheric blue haze",
        "aspect": "16:9",
    },
    "街拍纪实": {
        "category": "摄影",
        "tags": "street photography, decisive moment, candid documentary",
        "quality": "authentic raw feeling, unposed human story",
        "neg": "staged, fake, overprocessed",
        "camera": "35mm prime, hip-level snap, off-center subject",
        "lighting": "available ambient light, urban neon or sunlight",
        "palette": "slightly desaturated urban tones",
        "aspect": "3:2",
    },

    # ========== 动漫 / 插画 Illustration ==========
    "动漫": {
        "category": "动漫",
        "tags": "anime style, cel shading, clean line art, vibrant anime colors",
        "quality": "detailed anime eyes, pixiv trending, high quality anime",
        "neg": "photorealistic, 3d render, western cartoon, low quality",
        "camera": "",
        "lighting": "anime-style soft light, rim light on hair",
        "palette": "vibrant saturated anime palette",
        "aspect": "3:4",
    },
    "新海诚": {
        "category": "动漫",
        "tags": "Makoto Shinkai style, volumetric cloudscape, realistic anime backgrounds",
        "quality": "your name aesthetic, weathering with you mood, incredibly detailed skyscape",
        "neg": "flat background, dark mood, gritty",
        "camera": "",
        "lighting": "magic hour sunlight streaming, god rays through clouds",
        "palette": "sky blue, warm orange sunset, pink hour",
        "aspect": "16:9",
    },
    "宫崎骏": {
        "category": "动漫",
        "tags": "Studio Ghibli style, hand-painted background, whimsical warmth",
        "quality": "Totoro aesthetic, Spirited Away mood, hayao miyazaki inspired",
        "neg": "dark, edgy, hyperdetailed, cgi",
        "camera": "",
        "lighting": "soft daylight through leaves, gentle diffuse",
        "palette": "pastoral greens, cream, sky blue",
        "aspect": "16:9",
    },
    "美漫": {
        "category": "动漫",
        "tags": "American comic book style, bold ink lines, halftone shading",
        "quality": "marvel / DC inspired, dynamic pose, action panel",
        "neg": "anime, soft shading, watercolor",
        "camera": "",
        "lighting": "dramatic cel lighting, high contrast shadows",
        "palette": "saturated primary colors, comic book palette",
        "aspect": "2:3",
    },
    "Q版": {
        "category": "动漫",
        "tags": "chibi style, super-deformed, cute mascot, 3-head-tall proportions",
        "quality": "adorable, clean vector look, sticker worthy",
        "neg": "realistic proportion, detailed anatomy, dark mood",
        "camera": "",
        "lighting": "even flat light, gentle cel shading",
        "palette": "bright pastel palette, sugary",
        "aspect": "1:1",
    },
    "童话绘本": {
        "category": "动漫",
        "tags": "children's book illustration, storybook style, hand drawn warmth",
        "quality": "gouache texture, paper warmth, beatrix potter meets pixar",
        "neg": "dark, horror, hyper-realistic, edgy",
        "camera": "",
        "lighting": "soft overall illumination, enchanted glow",
        "palette": "warm buttery pastels, cream page base",
        "aspect": "4:3",
    },
    "水彩": {
        "category": "插画",
        "tags": "watercolor painting, wet-on-wet technique, paper texture, soft bleeding edges",
        "quality": "traditional watercolor, transparent wash layers, artistic",
        "neg": "digital vector, hard edges, heavy outlines, 3d",
        "camera": "",
        "lighting": "natural daylight on paper",
        "palette": "translucent pastel layers, white paper showing through",
        "aspect": "1:1",
    },
    "油画": {
        "category": "插画",
        "tags": "oil painting, thick impasto brushstrokes, canvas texture",
        "quality": "museum quality oil on canvas, old master technique",
        "neg": "digital, flat colors, vector, pixel art",
        "camera": "",
        "lighting": "chiaroscuro, warm rembrandt glow",
        "palette": "rich earth tones, deep jewel colors",
        "aspect": "4:5",
    },
    "水墨": {
        "category": "插画",
        "tags": "Chinese ink wash painting, sumi-e, negative space, calligraphic strokes",
        "quality": "zen atmosphere, rice paper texture, ink bleed",
        "neg": "colorful, dense composition, western painting, cartoon",
        "camera": "",
        "lighting": "flat paper light, no harsh shadows",
        "palette": "sumi black on rice-paper beige, occasional vermillion seal",
        "aspect": "3:4",
    },
    "工笔国画": {
        "category": "插画",
        "tags": "Chinese gongbi painting, meticulous fine brush, intricate floral detail",
        "quality": "Song dynasty court painting style, mineral pigment",
        "neg": "loose brushstrokes, abstract, western style",
        "camera": "",
        "lighting": "flat even pigment, no modeling light",
        "palette": "azurite blue, malachite green, cinnabar red, gold leaf",
        "aspect": "3:4",
    },
    "浮世绘": {
        "category": "插画",
        "tags": "Ukiyo-e woodblock print, Edo period, Hokusai / Hiroshige style",
        "quality": "traditional Japanese woodcut, flat color blocks, outlined figures",
        "neg": "modern anime, 3d, photorealistic",
        "camera": "",
        "lighting": "no modeling light, flat graphic",
        "palette": "prussian blue, earth reds, muted greens",
        "aspect": "2:3",
    },
    "线稿": {
        "category": "插画",
        "tags": "clean line art, black ink on white, single weight or dynamic line",
        "quality": "architectural line drawing precision, tattoo flash clarity",
        "neg": "color, shading, painterly, texture",
        "camera": "",
        "lighting": "no lighting, pure linework",
        "palette": "pure black on white",
        "aspect": "1:1",
    },
    "像素艺术": {
        "category": "插画",
        "tags": "pixel art, 16-bit sprite, pixelated, retro game aesthetic",
        "quality": "clean pixel clusters, limited palette, dithering",
        "neg": "anti-aliased, smooth, photorealistic, 3d render, high resolution",
        "camera": "",
        "lighting": "flat pixel shading or 2-tone",
        "palette": "NES / SNES limited palette, 16 colors",
        "aspect": "1:1",
    },

    # ========== 3D / 手工 3D & Craft ==========
    "3DC4D": {
        "category": "3D",
        "tags": "3d render, octane render, c4d style, subsurface scattering, glossy materials",
        "quality": "ray traced reflections, detailed shader, behance trending",
        "neg": "2d flat, sketch, line art",
        "camera": "3d viewport camera, 50mm equivalent",
        "lighting": "hdri environment light, colored accent rims",
        "palette": "vibrant candy colors, pastel gradients",
        "aspect": "1:1",
    },
    "盲盒手办": {
        "category": "3D",
        "tags": "blind box figurine, pop mart style, chibi 3d toy, kawaii collectible",
        "quality": "vinyl toy finish, pristine product shot, pop mart aesthetic",
        "neg": "realistic human, gritty, damaged",
        "camera": "50mm product shot, eye level toy perspective",
        "lighting": "soft studio light, gentle rim, clean shadow",
        "palette": "pastel macaron palette",
        "aspect": "1:1",
    },
    "低多边形": {
        "category": "3D",
        "tags": "low poly 3d, faceted geometry, minimalist polygons",
        "quality": "crisp flat shaded polygons, geometric stylization",
        "neg": "high detail, smooth subdivisions, realistic",
        "camera": "3/4 perspective, isometric-ish",
        "lighting": "flat faceted shading, 2-3 light setup",
        "palette": "limited flat palette, often pastel",
        "aspect": "1:1",
    },
    "等距视图": {
        "category": "3D",
        "tags": "isometric illustration, 2.5d isometric scene, game-dev isometric tile",
        "quality": "clean vector isometric look, detailed miniature diorama",
        "neg": "perspective distortion, top-down, first-person",
        "camera": "true isometric projection, 30-degree angles",
        "lighting": "even diffuse light, directional accent",
        "palette": "bright clean pastel palette",
        "aspect": "1:1",
    },
    "粘土": {
        "category": "3D",
        "tags": "claymation style, stop motion clay, aardman-like tactile figures",
        "quality": "handmade clay texture, fingerprint detail",
        "neg": "clean digital, plastic, smooth 3d",
        "camera": "stop motion rig perspective, slight depth of field",
        "lighting": "warm tungsten key with practical fill",
        "palette": "warm terracotta tones",
        "aspect": "1:1",
    },
    "毛毡手工": {
        "category": "3D",
        "tags": "felted wool craft, needle felt texture, handmade plush character",
        "quality": "fuzzy fiber detail, cute handmade imperfection",
        "neg": "smooth digital render, photorealistic animal",
        "camera": "close macro product shot",
        "lighting": "soft diffuse daylight",
        "palette": "muted natural wool colors",
        "aspect": "1:1",
    },
    "纸艺": {
        "category": "3D",
        "tags": "paper craft, layered paper art, quilling, origami composition",
        "quality": "intricate cut paper layers, shadow depth between layers",
        "neg": "flat 2d, digital illustration",
        "camera": "front-on with slight tilt, shallow depth",
        "lighting": "rim light casting paper-edge shadows",
        "palette": "pastel construction paper colors",
        "aspect": "1:1",
    },

    # ========== 设计 Design ==========
    "极简主义": {
        "category": "设计",
        "tags": "minimalist design, negative space, swiss style, geometric composition",
        "quality": "clean typography-friendly, editorial layout",
        "neg": "cluttered, ornate, busy, excess detail",
        "camera": "",
        "lighting": "flat studio light or ambient, no drama",
        "palette": "monochrome + single accent, lots of white",
        "aspect": "1:1",
    },
    "平面设计": {
        "category": "设计",
        "tags": "flat design, vector graphic, bold shapes, brand illustration",
        "quality": "clean vectors, designer grade composition",
        "neg": "photorealistic, gradient 3d, sketchy",
        "camera": "",
        "lighting": "flat shading, no highlights",
        "palette": "brand-forward 3-color palette",
        "aspect": "1:1",
    },
    "Logo设计": {
        "category": "设计",
        "tags": "logo design, brand mark, vector logotype, scalable emblem",
        "quality": "professional logo, centered composition on clean background",
        "neg": "photorealistic scene, complex background, cluttered",
        "camera": "",
        "lighting": "flat vector, no light gradient",
        "palette": "2-color max, high contrast",
        "aspect": "1:1",
    },
    "图标设计": {
        "category": "设计",
        "tags": "icon design, app icon, rounded square, centered glyph",
        "quality": "apple hig compliant, clean icon grid, crisp at 1024px",
        "neg": "cluttered, off-center, photo, low contrast",
        "camera": "",
        "lighting": "subtle highlight gradient, soft inner glow",
        "palette": "vibrant gradient with 2-3 colors",
        "aspect": "1:1",
    },
    "信息图": {
        "category": "设计",
        "tags": "infographic design, data visualization, icon system, explanatory layout",
        "quality": "clean editorial infographic, behance level",
        "neg": "messy, illustrative painting, photograph",
        "camera": "",
        "lighting": "flat, no drama",
        "palette": "brand palette + grayscale structure",
        "aspect": "3:4",
    },
    "品牌KV": {
        "category": "设计",
        "tags": "brand key visual, advertising campaign hero image, marketing KV",
        "quality": "commercial campaign quality, headline-ready negative space",
        "neg": "casual, amateur, low contrast",
        "camera": "hero wide or 3/4 product hero",
        "lighting": "brand-defined dramatic key, colored rim",
        "palette": "brand palette dominant + accent",
        "aspect": "16:9",
    },
    "专辑封面": {
        "category": "设计",
        "tags": "album cover art, music artwork, square format composition",
        "quality": "iconic album design, strong concept, emotive",
        "neg": "cluttered, literal, stock imagery",
        "camera": "",
        "lighting": "concept-driven, mood-heavy",
        "palette": "2-3 color highly intentional palette",
        "aspect": "1:1",
    },
    "复古海报": {
        "category": "设计",
        "tags": "vintage poster design, 1950s retro, letterpress print, screenprint texture",
        "quality": "saul bass meets mid-century, weathered paper feel",
        "neg": "modern flat design, digital gradient, 3d render",
        "camera": "",
        "lighting": "flat two-tone",
        "palette": "muted primary + cream background",
        "aspect": "3:4",
    },
    "电影海报": {
        "category": "设计",
        "tags": "movie poster, cinematic key art, title-ready composition",
        "quality": "theatrical one-sheet, dramatic hero composition",
        "neg": "casual snapshot, cluttered, amateur",
        "camera": "hero portrait or symmetric icon layout",
        "lighting": "strong single direction light, volumetric",
        "palette": "teal & orange or moody duotone",
        "aspect": "2:3",
    },
    "表情包": {
        "category": "设计",
        "tags": "sticker design, emoji style, expressive meme-ready character",
        "quality": "transparent background ready, bold outline, readable at 128px",
        "neg": "complex scene, photorealistic, subtle",
        "camera": "",
        "lighting": "flat cel shading",
        "palette": "bright saturated 4-color",
        "aspect": "1:1",
    },

    # ========== 艺术史 Art Movement ==========
    "印象派": {
        "category": "艺术",
        "tags": "impressionist painting, visible brushstrokes, plein air, monet inspired",
        "quality": "late 19th century impressionism, atmospheric perspective",
        "neg": "photorealistic, digital, sharp outlines",
        "camera": "",
        "lighting": "dappled natural light, sun-drenched scene",
        "palette": "broken color technique, complementary dabs",
        "aspect": "4:5",
    },
    "后印象派": {
        "category": "艺术",
        "tags": "post-impressionist, van gogh style, expressive brushstroke, emotive color",
        "quality": "starry night swirls, dynamic brush texture",
        "neg": "realistic, photographic, flat",
        "camera": "",
        "lighting": "emotional not physical light",
        "palette": "bold yellows cobalt and burnt sienna",
        "aspect": "4:5",
    },
    "新艺术": {
        "category": "艺术",
        "tags": "art nouveau, alphonse mucha, flowing organic lines, floral ornament border",
        "quality": "belle époque poster, feminine ornate frame",
        "neg": "geometric minimal, modern flat, 3d",
        "camera": "",
        "lighting": "flat even decorative light",
        "palette": "muted golds, soft earth tones, sage",
        "aspect": "2:3",
    },
    "装饰艺术": {
        "category": "艺术",
        "tags": "art deco, 1920s geometric ornament, gatsby aesthetic, gold and black lacquer",
        "quality": "symmetric art deco pattern, streamline moderne elegance",
        "neg": "rustic, organic nouveau, grunge",
        "camera": "",
        "lighting": "strong geometric shadow play",
        "palette": "black gold ivory with emerald accents",
        "aspect": "2:3",
    },

    # ========== 场景 / 氛围 Scene ==========
    "赛博朋克": {
        "category": "场景",
        "tags": "cyberpunk, neon-soaked, blade runner aesthetic, megacity dystopia, holographic ads",
        "quality": "detailed cyberpunk cityscape, rainy night ambiance",
        "neg": "rustic, medieval, natural countryside",
        "camera": "low angle wide, 24mm anamorphic",
        "lighting": "neon magenta and cyan rim, wet reflective streets",
        "palette": "magenta cyan black, neon highlights",
        "aspect": "21:9",
    },
    "蒸汽朋克": {
        "category": "场景",
        "tags": "steampunk, brass gears and copper pipes, victorian industrial, airship era",
        "quality": "intricate clockwork detail, rich leather and patina",
        "neg": "clean sci-fi, modern, plastic",
        "camera": "",
        "lighting": "warm gaslight glow, smoky haze",
        "palette": "brass copper sepia, burgundy leather",
        "aspect": "3:2",
    },
    "科幻": {
        "category": "场景",
        "tags": "sci-fi concept art, futuristic technology, clean spaceship interior, holographic UI",
        "quality": "blade runner 2049 palette, hard-sci-fi plausible",
        "neg": "medieval, fantasy magic, primitive",
        "camera": "cinematic wide, 21:9 framing",
        "lighting": "cool blue practical strips, volumetric haze",
        "palette": "cool blue cyan with warm accent",
        "aspect": "21:9",
    },
    "奇幻": {
        "category": "场景",
        "tags": "epic fantasy art, magical atmosphere, artstation trending, tolkien inspired",
        "quality": "detailed fantasy concept, elven architecture, dragon-scale atmosphere",
        "neg": "modern city, cyberpunk, mundane",
        "camera": "epic wide establishing, 24mm",
        "lighting": "ethereal god rays through mist",
        "palette": "golden hour warm with magical cyan glow",
        "aspect": "16:9",
    },
    "黑暗奇幻": {
        "category": "场景",
        "tags": "dark fantasy, grimdark, eldritch horror atmosphere, berserk aesthetic",
        "quality": "frank frazetta meets zdzisław beksiński",
        "neg": "cheerful, bright, cartoonish",
        "camera": "low angle hero or dread pov",
        "lighting": "blood moon crimson, torch flicker",
        "palette": "black crimson sickly green, rusted iron",
        "aspect": "2:3",
    },
    "国潮": {
        "category": "场景",
        "tags": "guochao Chinese neo-trend, modern hanfu revival, oriental modernism",
        "quality": "contemporary Chinese style illustration, editorial fashion",
        "neg": "western medieval, european style",
        "camera": "",
        "lighting": "warm accent on oriental red-gold",
        "palette": "vermillion jade gold, ink black accents",
        "aspect": "3:4",
    },
    "Y2K": {
        "category": "场景",
        "tags": "Y2K aesthetic, early 2000s digital, chrome bubble UI, frosted plastic",
        "quality": "low-fi cd-rom graphic, holographic stickers",
        "neg": "ultra clean modern, analog retro",
        "camera": "",
        "lighting": "glossy chrome highlights",
        "palette": "baby blue pink lilac, iridescent chrome",
        "aspect": "1:1",
    },
    "Vaporwave": {
        "category": "场景",
        "tags": "vaporwave, retro 80s 90s computer graphics, roman bust, palm tree grid",
        "quality": "synthwave aesthetic, low-fi jpeg nostalgia",
        "neg": "modern clean, natural, high detail",
        "camera": "",
        "lighting": "sunset gradient, neon grid horizon",
        "palette": "hot pink teal purple, retro sunset",
        "aspect": "16:9",
    },
    "霓虹灯牌": {
        "category": "场景",
        "tags": "neon sign typography, glowing tube letters, dark brick wall backdrop",
        "quality": "realistic neon glass tube glow, chromatic bloom",
        "neg": "daylight, printed sign, flat vector",
        "camera": "straight-on product shot, 50mm",
        "lighting": "self-emissive neon, dark ambient",
        "palette": "magenta cyan on deep black",
        "aspect": "3:2",
    },
    "建筑可视化": {
        "category": "场景",
        "tags": "architectural visualization, V-Ray / Lumion render, interior design magazine",
        "quality": "award-winning archviz, photorealistic materials",
        "neg": "sketchy, doodle, distorted perspective",
        "camera": "wide 24mm architectural tilt-corrected",
        "lighting": "realistic sun study plus artificial, product-ready",
        "palette": "natural materials, neutral brand-defined",
        "aspect": "16:9",
    },
    "电影感": {
        "category": "场景",
        "tags": "cinematic film still, anamorphic lens flare, letterboxed framing",
        "quality": "ARRI Alexa quality, professional color grade, movie still",
        "neg": "snapshot, amateur, flat lighting, instagram filter",
        "camera": "anamorphic 2.39:1 framing, low angle hero",
        "lighting": "motivated practical + volumetric haze",
        "palette": "teal & orange cinematic grade",
        "aspect": "21:9",
    },
    "概念艺术": {
        "category": "场景",
        "tags": "concept art, matte painting, production design, pre-visualization",
        "quality": "ILM / weta concept sketch, narrative-driven composition",
        "neg": "finished illustration, cartoon, low detail",
        "camera": "cinematic wide establishing",
        "lighting": "narrative-lit hero with atmosphere",
        "palette": "mood-defined limited palette",
        "aspect": "21:9",
    },

    # ========== 游戏艺术 Game Art (v2.1 新增) ==========
    "原神": {
        "category": "游戏",
        "tags": "Genshin Impact style, miHoYo aesthetic, stylized anime rendering, cel shaded 3d",
        "quality": "gacha game hero card quality, detailed anime character portrait",
        "neg": "photorealistic, western cartoon, gritty",
        "camera": "3/4 character hero shot, slightly upward angle",
        "lighting": "rim light on hair, soft key + colored fill",
        "palette": "vibrant saturated anime palette, element-themed accents",
        "aspect": "3:4",
    },
    "崩铁星穹": {
        "category": "游戏",
        "tags": "Honkai Star Rail style, space fantasy JRPG anime, miHoYo rendering",
        "quality": "splash art quality, dynamic pose, elemental VFX",
        "neg": "photorealistic, rustic, medieval",
        "camera": "dynamic dutch angle hero shot",
        "lighting": "glowing elemental rim light",
        "palette": "cosmic gradient + neon accent",
        "aspect": "3:4",
    },
    "英雄联盟": {
        "category": "游戏",
        "tags": "League of Legends splash art style, Riot Games painterly illustration",
        "quality": "champion splash quality, dramatic action pose",
        "neg": "anime chibi, flat vector, photo",
        "camera": "dynamic low angle hero pose",
        "lighting": "dramatic rim with colored ability VFX",
        "palette": "saturated fantasy palette with magical accent",
        "aspect": "16:9",
    },
    "暗黑4": {
        "category": "游戏",
        "tags": "Diablo IV style, dark gothic fantasy, blizzard illustration",
        "quality": "ARPG splash quality, grim dark atmosphere",
        "neg": "cheerful, pastel, chibi, flat",
        "camera": "low-angle menacing hero shot",
        "lighting": "infernal red rim, volumetric fog",
        "palette": "charcoal black, ember red, corrupted green",
        "aspect": "3:2",
    },
    "Valorant": {
        "category": "游戏",
        "tags": "Valorant agent art, stylized flat anime realism, Riot FPS aesthetic",
        "quality": "agent reveal quality, confident hero pose",
        "neg": "painterly fantasy, chibi",
        "camera": "3/4 hero standoff",
        "lighting": "clean cel shaded with colored ability glow",
        "palette": "agent signature color + urban neutral",
        "aspect": "3:4",
    },
    "Pokemon": {
        "category": "游戏",
        "tags": "Pokemon style, Ken Sugimori illustration, round cute creature design",
        "quality": "Pokedex official art, clean cel shading",
        "neg": "gritty, realistic, complex anatomy",
        "camera": "3/4 creature portrait on white",
        "lighting": "flat cel shading with soft shadow",
        "palette": "clean primary colors per type",
        "aspect": "1:1",
    },
    "暴雪风": {
        "category": "游戏",
        "tags": "Blizzard stylized art, Overwatch / WoW concept style, exaggerated anatomy",
        "quality": "blizzard cinematic quality, heroic pose, strong silhouette",
        "neg": "photorealistic, anime chibi, flat",
        "camera": "heroic low angle, dynamic posing",
        "lighting": "dramatic three-point hero light",
        "palette": "rich saturated fantasy palette",
        "aspect": "3:2",
    },

    # ========== 东方传统 Chinese/Japanese Traditional (v2.1 新增) ==========
    "敦煌壁画": {
        "category": "东方",
        "tags": "Dunhuang mural style, Tang dynasty fresco, flying apsara figures, silk road art",
        "quality": "weathered ancient mural texture, mineral pigment on plaster",
        "neg": "modern digital, anime, western",
        "camera": "flat mural frontal view",
        "lighting": "no modeling light, flat pigment",
        "palette": "mineral ochre, malachite green, azurite blue, gold leaf",
        "aspect": "4:3",
    },
    "青花瓷": {
        "category": "东方",
        "tags": "Chinese blue and white porcelain motif, Ming dynasty pattern, cobalt underglaze",
        "quality": "porcelain surface detail, intricate floral motif",
        "neg": "full color, western, abstract",
        "camera": "",
        "lighting": "soft glazed porcelain highlight",
        "palette": "cobalt blue on pure white porcelain",
        "aspect": "1:1",
    },
    "民国月份牌": {
        "category": "东方",
        "tags": "Republic of China calendar poster, 1920s Shanghai art deco fusion, qipao glamour",
        "quality": "vintage advertising print, lithograph texture",
        "neg": "modern digital, anime, photo",
        "camera": "",
        "lighting": "flat poster illumination",
        "palette": "faded pastel with gold gilt accents",
        "aspect": "2:3",
    },
    "年画": {
        "category": "东方",
        "tags": "Chinese new year folk woodblock, auspicious symbols, chubby child figures",
        "quality": "traditional woodblock print texture, folk decorative",
        "neg": "photorealistic, minimalist, western",
        "camera": "",
        "lighting": "flat festive graphic",
        "palette": "festive vermillion, gold, pine green",
        "aspect": "3:4",
    },
    "剪纸": {
        "category": "东方",
        "tags": "Chinese paper cutting art, red paper silhouette, intricate symmetric cutout",
        "quality": "fine paper cut detail, traditional folk craft",
        "neg": "full color, 3d, photorealistic",
        "camera": "",
        "lighting": "flat silhouette with background paper",
        "palette": "pure vermillion red on neutral background",
        "aspect": "1:1",
    },
    "和风": {
        "category": "东方",
        "tags": "Japanese wafu aesthetic, traditional kimono elegance, wagashi sensibility",
        "quality": "refined Japanese traditional design",
        "neg": "western, modern pop, grunge",
        "camera": "",
        "lighting": "soft shoji-diffused light",
        "palette": "indigo, vermillion, sumi ink, cream washi",
        "aspect": "3:4",
    },
    "汉服写真": {
        "category": "东方",
        "tags": "hanfu photography, Chinese traditional dress, oriental portrait",
        "quality": "ethereal hanfu fashion editorial, flowing silk",
        "neg": "western dress, modern clothing, cyberpunk",
        "camera": "85mm portrait, soft 3/4",
        "lighting": "diffuse morning light, soft bounce",
        "palette": "silk ink tones, jade, cream, plum",
        "aspect": "3:4",
    },

    # ========== 动漫扩展 Anime extras (v2.1 新增) ==========
    "萌系": {
        "category": "动漫",
        "tags": "moe anime style, cute girl aesthetic, large sparkling eyes",
        "quality": "moekko illustration, clean lineart, rich anime shading",
        "neg": "gritty, adult, western comic",
        "camera": "",
        "lighting": "soft diffuse with catchlight in eyes",
        "palette": "pastel pink cream sky-blue",
        "aspect": "3:4",
    },
    "厚涂": {
        "category": "动漫",
        "tags": "painterly anime, thick paint anime illustration, semi-realistic rendering",
        "quality": "artstation anime painting, detailed brushwork",
        "neg": "flat cel shading, vector, chibi",
        "camera": "",
        "lighting": "rembrandt on face, painterly shadows",
        "palette": "desaturated muted painterly tones",
        "aspect": "3:4",
    },
    "轻小说封面": {
        "category": "动漫",
        "tags": "light novel cover illustration, Japanese LN art, glossy anime portrait",
        "quality": "bookshelf-ready cover composition, eye-catching character",
        "neg": "dark horror, western comic, 3d",
        "camera": "3/4 character hero, title-friendly negative space",
        "lighting": "cinematic anime key light",
        "palette": "vibrant anime palette with atmosphere",
        "aspect": "2:3",
    },
    "赛璐璐": {
        "category": "动漫",
        "tags": "traditional cel-shaded anime, sharp shadow boundaries, limited anime palette",
        "quality": "classic 2d cel animation look, detailed line art",
        "neg": "painterly, 3d render, gradient shading",
        "camera": "",
        "lighting": "two-tone cel shading, hard shadow edges",
        "palette": "saturated flat anime palette",
        "aspect": "16:9",
    },

    # ========== 现代设计 Modern Design (v2.1 新增) ==========
    "玻璃拟态": {
        "category": "设计",
        "tags": "glassmorphism, frosted glass UI, transparent blur layers, depth card stack",
        "quality": "modern UI glass effect, realistic refraction, clean layout",
        "neg": "flat 2d, skeuomorphic wood, pixel art",
        "camera": "",
        "lighting": "subtle inner glow, soft backlight through glass",
        "palette": "pastel gradient backdrop with translucent glass",
        "aspect": "3:4",
    },
    "新拟态": {
        "category": "设计",
        "tags": "neumorphism, soft UI, extruded plastic button, subtle dual shadow",
        "quality": "modern minimal UI, monochrome neumorphic elements",
        "neg": "flat, photorealistic, grunge",
        "camera": "",
        "lighting": "soft dual light and dark shadow",
        "palette": "monochrome beige or gray single-tone",
        "aspect": "1:1",
    },
    "孟菲斯": {
        "category": "设计",
        "tags": "Memphis design, 1980s postmodern, geometric shapes, squiggle pattern, bold primaries",
        "quality": "playful postmodern graphic, bold composition",
        "neg": "minimalist, photorealistic, classical",
        "camera": "",
        "lighting": "flat graphic, no modeling",
        "palette": "hot pink, cyan, yellow, black squiggle pattern",
        "aspect": "1:1",
    },
    "杂志编排": {
        "category": "设计",
        "tags": "editorial magazine layout, bold serif typography, grid-based design",
        "quality": "international typographic style, vogue spread quality",
        "neg": "amateur, overcluttered, cute",
        "camera": "",
        "lighting": "clean flat studio-style",
        "palette": "monochrome with single bold accent",
        "aspect": "3:4",
    },
    "包豪斯": {
        "category": "设计",
        "tags": "Bauhaus design, de stijl geometric, primary color blocks, constructivist",
        "quality": "1920s modernist design school, pure geometry",
        "neg": "ornate, victorian, realistic",
        "camera": "",
        "lighting": "flat geometric",
        "palette": "primary red yellow blue + black on white",
        "aspect": "1:1",
    },
    "奶油风": {
        "category": "设计",
        "tags": "cream style, soft beige palette, warm minimal aesthetic, korean lifestyle",
        "quality": "instagram lifestyle aesthetic, soft velvety texture",
        "neg": "dark, saturated, edgy",
        "camera": "",
        "lighting": "natural soft window light",
        "palette": "cream, soft beige, butter yellow, milk tea",
        "aspect": "4:5",
    },

    # ========== 建筑 & 氛围扩展 (v2.1 新增) ==========
    "粗野主义": {
        "category": "场景",
        "tags": "brutalist architecture, raw concrete, heavy geometric mass, béton brut",
        "quality": "mid-century brutalist landmark, imposing scale",
        "neg": "ornate, baroque, flimsy",
        "camera": "wide low-angle heroic architecture shot",
        "lighting": "harsh sun shadow across concrete",
        "palette": "raw concrete gray with sky contrast",
        "aspect": "16:9",
    },
    "北欧极简": {
        "category": "场景",
        "tags": "scandinavian interior, nordic minimalism, light wood, warm neutral",
        "quality": "hygge lifestyle, interior magazine quality",
        "neg": "ornate, cluttered, dark gothic",
        "camera": "wide 24mm interior architectural",
        "lighting": "large window natural light",
        "palette": "warm wood, white wall, soft gray",
        "aspect": "16:9",
    },
    "侘寂": {
        "category": "场景",
        "tags": "wabi-sabi aesthetic, imperfect natural beauty, weathered texture, zen japanese",
        "quality": "quiet imperfection, aged material detail",
        "neg": "glossy modern, bright colors, ornate",
        "camera": "",
        "lighting": "soft diffused natural, muted",
        "palette": "muted earth, weathered gray, aged beige",
        "aspect": "4:5",
    },

    # ========== 摄影扩展 (v2.1 新增) ==========
    "暗黑美食": {
        "category": "摄影",
        "tags": "dark food photography, moody cuisine, chiaroscuro plating",
        "quality": "michelin-level dark food styling, dramatic shadow",
        "neg": "bright cheerful, flat, cluttered",
        "camera": "100mm macro 45-degree, side low-key",
        "lighting": "single hard key from behind, deep shadow",
        "palette": "deep black with food color accent",
        "aspect": "4:5",
    },
    "日杂": {
        "category": "摄影",
        "tags": "Japanese lifestyle magazine, natural light still life, clean minimalism",
        "quality": "muji aesthetic, calm everyday beauty",
        "neg": "dark moody, dramatic, saturated",
        "camera": "50mm still life, slight top-down",
        "lighting": "soft window daylight, no drama",
        "palette": "cream, light wood, pale pastel",
        "aspect": "4:5",
    },
    "街头潮流": {
        "category": "摄影",
        "tags": "streetwear fashion, urban hypebeast, sneaker culture",
        "quality": "street style magazine editorial, confident pose",
        "neg": "formal suit, fantasy, kawaii",
        "camera": "35mm full body street fashion",
        "lighting": "harsh urban daylight or neon",
        "palette": "high contrast monochrome + brand accent",
        "aspect": "3:4",
    },

    # ========== 综合 (v2.1 新增) ==========
    "疗愈治愈": {
        "category": "场景",
        "tags": "healing cozy aesthetic, soft warm interior, cat sunlight, tea steam",
        "quality": "soothing slow-life scene",
        "neg": "dramatic action, dark, cyberpunk",
        "camera": "",
        "lighting": "warm golden hour through window",
        "palette": "warm honey, cream, dusty pink",
        "aspect": "4:5",
    },
    "美式复古": {
        "category": "场景",
        "tags": "americana retro, 1950s diner, vintage coca-cola americana",
        "quality": "Norman Rockwell meets mid-century ad",
        "neg": "asian, modern sleek, futuristic",
        "camera": "",
        "lighting": "warm diner fluorescent or golden",
        "palette": "cherry red, cream, turquoise",
        "aspect": "3:2",
    },
}

# ─────────────────────────────────────────────────────────
# 别名 (英文 / 同义词 → 规范预设名)
# ─────────────────────────────────────────────────────────
ALIASES: Dict[str, str] = {
    # 英文
    "realistic": "写实摄影",
    "photo": "写实摄影",
    "photography": "写实摄影",
    "film": "胶片摄影",
    "analog": "胶片摄影",
    "bw": "黑白摄影",
    "blackwhite": "黑白摄影",
    "monochrome": "黑白摄影",
    "portrait": "人像摄影",
    "fashion": "时尚大片",
    "editorial": "时尚大片",
    "food": "美食摄影",
    "product": "产品摄影",
    "ecommerce": "产品摄影",
    "macro": "微距摄影",
    "aerial": "航拍摄影",
    "drone": "航拍摄影",
    "street": "街拍纪实",
    "documentary": "街拍纪实",
    "anime": "动漫",
    "ghibli": "宫崎骏",
    "miyazaki": "宫崎骏",
    "shinkai": "新海诚",
    "makoto": "新海诚",
    "comic": "美漫",
    "marvel": "美漫",
    "chibi": "Q版",
    "kawaii": "Q版",
    "storybook": "童话绘本",
    "childrensbook": "童话绘本",
    "watercolor": "水彩",
    "oil": "油画",
    "ink": "水墨",
    "sumi": "水墨",
    "gongbi": "工笔国画",
    "ukiyoe": "浮世绘",
    "lineart": "线稿",
    "pixel": "像素艺术",
    "3d": "3DC4D",
    "c4d": "3DC4D",
    "octane": "3DC4D",
    "blindbox": "盲盒手办",
    "popmart": "盲盒手办",
    "lowpoly": "低多边形",
    "isometric": "等距视图",
    "iso": "等距视图",
    "claymation": "粘土",
    "felt": "毛毡手工",
    "papercraft": "纸艺",
    "minimal": "极简主义",
    "minimalist": "极简主义",
    "flat": "平面设计",
    "vector": "平面设计",
    "logo": "Logo设计",
    "icon": "图标设计",
    "infographic": "信息图",
    "kv": "品牌KV",
    "album": "专辑封面",
    "poster": "复古海报",
    "movieposter": "电影海报",
    "sticker": "表情包",
    "emoji": "表情包",
    "impressionist": "印象派",
    "vangogh": "后印象派",
    "postimpressionist": "后印象派",
    "artnouveau": "新艺术",
    "mucha": "新艺术",
    "artdeco": "装饰艺术",
    "cyberpunk": "赛博朋克",
    "steampunk": "蒸汽朋克",
    "scifi": "科幻",
    "fantasy": "奇幻",
    "darkfantasy": "黑暗奇幻",
    "grimdark": "黑暗奇幻",
    "guochao": "国潮",
    "y2k": "Y2K",
    "vaporwave": "Vaporwave",
    "synthwave": "Vaporwave",
    "neon": "霓虹灯牌",
    "archviz": "建筑可视化",
    "architecture": "建筑可视化",
    "cinematic": "电影感",
    "cinema": "电影感",
    "concept": "概念艺术",
    "conceptart": "概念艺术",
    # v2.1 游戏
    "genshin": "原神",
    "mihoyo": "原神",
    "honkai": "崩铁星穹",
    "starrail": "崩铁星穹",
    "lol": "英雄联盟",
    "leagueoflegends": "英雄联盟",
    "diablo": "暗黑4",
    "valorant": "Valorant",
    "pokemon": "Pokemon",
    "blizzard": "暴雪风",
    "overwatch": "暴雪风",
    "wow": "暴雪风",
    # v2.1 东方
    "dunhuang": "敦煌壁画",
    "qinghua": "青花瓷",
    "porcelain": "青花瓷",
    "yuefenpai": "民国月份牌",
    "wafu": "和风",
    "hanfu": "汉服写真",
    "papercut": "剪纸",
    "nianhua": "年画",
    # v2.1 动漫扩展
    "moe": "萌系",
    "painterlyanime": "厚涂",
    "lightnovel": "轻小说封面",
    "lncover": "轻小说封面",
    "cellshaded": "赛璐璐",
    "celshaded": "赛璐璐",
    # v2.1 设计
    "glassmorphism": "玻璃拟态",
    "glass": "玻璃拟态",
    "neumorphism": "新拟态",
    "memphis": "孟菲斯",
    "editorial": "杂志编排",
    "bauhaus": "包豪斯",
    "cream": "奶油风",
    "korean": "奶油风",
    # v2.1 建筑 / 氛围
    "brutalism": "粗野主义",
    "brutalist": "粗野主义",
    "nordic": "北欧极简",
    "scandinavian": "北欧极简",
    "wabisabi": "侘寂",
    "zen": "侘寂",
    # v2.1 摄影
    "darkfood": "暗黑美食",
    "muji": "日杂",
    "streetwear": "街头潮流",
    "hypebeast": "街头潮流",
    # v2.1 综合
    "healing": "疗愈治愈",
    "cozy": "疗愈治愈",
    "americana": "美式复古",
}


# ─────────────────────────────────────────────────────────
# 意图关键词 → (推荐预设, 推荐画幅)
# ─────────────────────────────────────────────────────────
INTENT_KEYWORDS: List[Tuple[str, str, str]] = [
    # (关键词, 推荐预设, 推荐画幅)
    ("logo", "Logo设计", "1:1"),
    ("徽标", "Logo设计", "1:1"),
    ("标志", "Logo设计", "1:1"),
    ("icon", "图标设计", "1:1"),
    ("图标", "图标设计", "1:1"),
    ("app图标", "图标设计", "1:1"),
    ("电影海报", "电影海报", "2:3"),
    ("海报", "复古海报", "3:4"),
    ("poster", "复古海报", "3:4"),
    ("封面", "专辑封面", "1:1"),
    ("专辑", "专辑封面", "1:1"),
    ("表情包", "表情包", "1:1"),
    ("贴纸", "表情包", "1:1"),
    ("信息图", "信息图", "3:4"),
    ("infographic", "信息图", "3:4"),
    ("kv", "品牌KV", "16:9"),
    ("主视觉", "品牌KV", "16:9"),
    ("产品", "产品摄影", "1:1"),
    ("电商", "产品摄影", "1:1"),
    ("商品", "产品摄影", "1:1"),
    ("美食", "美食摄影", "1:1"),
    ("食物", "美食摄影", "1:1"),
    ("菜品", "美食摄影", "1:1"),
    ("头像", "人像摄影", "1:1"),
    ("肖像", "人像摄影", "3:4"),
    ("人像", "人像摄影", "3:4"),
    ("时装", "时尚大片", "3:4"),
    ("时尚", "时尚大片", "3:4"),
    ("街拍", "街拍纪实", "3:2"),
    ("纪实", "街拍纪实", "3:2"),
    ("风景", "写实摄影", "16:9"),
    ("风光", "写实摄影", "16:9"),
    ("建筑", "建筑可视化", "16:9"),
    ("室内", "建筑可视化", "4:3"),
    ("手办", "盲盒手办", "1:1"),
    ("盲盒", "盲盒手办", "1:1"),
    ("玩具", "盲盒手办", "1:1"),
    ("航拍", "航拍摄影", "16:9"),
    ("鸟瞰", "航拍摄影", "16:9"),
    ("微距", "微距摄影", "1:1"),
    ("赛博", "赛博朋克", "21:9"),
    ("cyberpunk", "赛博朋克", "21:9"),
    ("蒸汽朋克", "蒸汽朋克", "3:2"),
    ("科幻", "科幻", "21:9"),
    ("未来", "科幻", "21:9"),
    ("奇幻", "奇幻", "16:9"),
    ("魔幻", "奇幻", "16:9"),
    ("黑暗", "黑暗奇幻", "2:3"),
    ("水墨", "水墨", "3:4"),
    ("国画", "工笔国画", "3:4"),
    ("工笔", "工笔国画", "3:4"),
    ("浮世绘", "浮世绘", "2:3"),
    ("童话", "童话绘本", "4:3"),
    ("绘本", "童话绘本", "4:3"),
    ("宫崎骏", "宫崎骏", "16:9"),
    ("新海诚", "新海诚", "16:9"),
    ("动漫", "动漫", "3:4"),
    ("二次元", "动漫", "3:4"),
    ("q版", "Q版", "1:1"),
    ("Q版", "Q版", "1:1"),
    ("chibi", "Q版", "1:1"),
    ("线稿", "线稿", "1:1"),
    ("像素", "像素艺术", "1:1"),
    ("3d", "3DC4D", "1:1"),
    ("c4d", "3DC4D", "1:1"),
    ("粘土", "粘土", "1:1"),
    ("等距", "等距视图", "1:1"),
    ("国潮", "国潮", "3:4"),
    ("霓虹", "霓虹灯牌", "3:2"),
    ("电影", "电影感", "21:9"),
    ("cinema", "电影感", "21:9"),
    ("concept", "概念艺术", "21:9"),
    ("概念图", "概念艺术", "21:9"),
    ("复古", "复古海报", "3:4"),
    ("vintage", "复古海报", "3:4"),
    # v2.1 游戏
    ("原神", "原神", "3:4"),
    ("genshin", "原神", "3:4"),
    ("崩铁", "崩铁星穹", "3:4"),
    ("星穹", "崩铁星穹", "3:4"),
    ("lol", "英雄联盟", "16:9"),
    ("英雄联盟", "英雄联盟", "16:9"),
    ("valorant", "Valorant", "3:4"),
    ("暗黑4", "暗黑4", "3:2"),
    ("diablo", "暗黑4", "3:2"),
    ("pokemon", "Pokemon", "1:1"),
    ("宝可梦", "Pokemon", "1:1"),
    ("暴雪", "暴雪风", "3:2"),
    ("overwatch", "暴雪风", "3:2"),
    # v2.1 东方
    ("敦煌", "敦煌壁画", "4:3"),
    ("壁画", "敦煌壁画", "4:3"),
    ("青花瓷", "青花瓷", "1:1"),
    ("月份牌", "民国月份牌", "2:3"),
    ("民国", "民国月份牌", "2:3"),
    ("剪纸", "剪纸", "1:1"),
    ("年画", "年画", "3:4"),
    ("汉服", "汉服写真", "3:4"),
    ("和风", "和风", "3:4"),
    ("日系", "日杂", "4:5"),
    ("日杂", "日杂", "4:5"),
    # v2.1 动漫扩展
    ("萌", "萌系", "3:4"),
    ("萌系", "萌系", "3:4"),
    ("厚涂", "厚涂", "3:4"),
    ("轻小说", "轻小说封面", "2:3"),
    ("赛璐璐", "赛璐璐", "16:9"),
    # v2.1 现代设计
    ("玻璃拟态", "玻璃拟态", "3:4"),
    ("glassmorphism", "玻璃拟态", "3:4"),
    ("新拟态", "新拟态", "1:1"),
    ("neumorphism", "新拟态", "1:1"),
    ("孟菲斯", "孟菲斯", "1:1"),
    ("memphis", "孟菲斯", "1:1"),
    ("杂志", "杂志编排", "3:4"),
    ("magazine", "杂志编排", "3:4"),
    ("包豪斯", "包豪斯", "1:1"),
    ("bauhaus", "包豪斯", "1:1"),
    ("奶油", "奶油风", "4:5"),
    ("ins风", "奶油风", "4:5"),
    ("韩系", "奶油风", "4:5"),
    # v2.1 建筑 / 氛围
    ("粗野", "粗野主义", "16:9"),
    ("brutalism", "粗野主义", "16:9"),
    ("北欧", "北欧极简", "16:9"),
    ("scandinavian", "北欧极简", "16:9"),
    ("侘寂", "侘寂", "4:5"),
    ("wabi", "侘寂", "4:5"),
    ("禅意", "侘寂", "4:5"),
    # v2.1 摄影
    ("暗黑美食", "暗黑美食", "4:5"),
    ("darkfood", "暗黑美食", "4:5"),
    ("街头", "街头潮流", "3:4"),
    ("潮牌", "街头潮流", "3:4"),
    ("streetwear", "街头潮流", "3:4"),
    # v2.1 综合
    ("治愈", "疗愈治愈", "4:5"),
    ("疗愈", "疗愈治愈", "4:5"),
    ("cozy", "疗愈治愈", "4:5"),
    ("美式复古", "美式复古", "3:2"),
    ("americana", "美式复古", "3:2"),
]

# ─────────────────────────────────────────────────────────
# 构图关键词
# ─────────────────────────────────────────────────────────
COMPOSITION_KEYWORDS: Dict[str, str] = {
    "特写": "extreme close-up shot",
    "近景": "close-up shot",
    "中景": "medium shot",
    "全身": "full body shot",
    "半身": "medium shot, waist up",
    "远景": "wide shot, establishing shot",
    "全景": "panoramic view",
    "俯拍": "top-down view",
    "俯视": "top-down view",
    "仰拍": "low angle shot, looking up",
    "仰视": "low angle shot, looking up",
    "鸟瞰": "bird's eye view, aerial",
    "平视": "eye-level shot",
    "正面": "front view",
    "侧面": "side profile view",
    "背面": "back view",
    "三分之二": "three-quarter view",
}

# ─────────────────────────────────────────────────────────
# 情绪关键词
# ─────────────────────────────────────────────────────────
MOOD_KEYWORDS: Dict[str, str] = {
    "温暖": "warm cozy atmosphere, golden tones",
    "温馨": "warm cozy atmosphere, golden tones",
    "冷峻": "cold atmosphere, steely blue tones",
    "神秘": "mysterious mood, foggy, dim lighting",
    "梦幻": "dreamy ethereal mood, soft glow, bokeh",
    "欢快": "joyful vibrant, bright cheerful colors",
    "忧郁": "melancholic mood, muted cool palette",
    "压抑": "oppressive mood, deep shadows, heavy atmosphere",
    "史诗": "epic grandeur, cinematic scale",
    "高级": "luxury sophistication, premium materials",
    "治愈": "healing soft ambiance, soothing",
    "清新": "fresh airy light pastel",
    "紧张": "tense suspense mood, high contrast",
    "浪漫": "romantic soft pink glow",
}

# ─────────────────────────────────────────────────────────
# 时间 / 天气 / 季节 关键词（v2.1 新增）
# ─────────────────────────────────────────────────────────
TIME_KEYWORDS: Dict[str, str] = {
    "清晨": "early morning, dawn, soft first light",
    "早晨": "morning light, fresh daylight",
    "上午": "bright morning sunshine",
    "正午": "high noon, overhead sun",
    "下午": "afternoon light, long soft shadows",
    "黄昏": "dusk, golden hour, magic hour",
    "傍晚": "dusk, golden hour, magic hour",
    "日落": "sunset, golden hour",
    "夜晚": "night time, dark ambient",
    "深夜": "late night, moonlit, dim",
    "午夜": "midnight, dark sky",
    "黎明": "dawn, blue hour breaking",
    "蓝调时刻": "blue hour, twilight gradient sky",
    "魔法时刻": "magic hour, warm golden glow",
}

WEATHER_KEYWORDS: Dict[str, str] = {
    "晴天": "sunny clear sky",
    "多云": "cloudy overcast sky",
    "阴天": "overcast gray sky",
    "下雨": "raining, wet reflective surfaces",
    "雨天": "rainy weather, soft rain",
    "大雨": "heavy rain, downpour, water droplets",
    "暴雨": "stormy rain, dramatic weather",
    "下雪": "snowing, snowflakes in air",
    "雪天": "snowy landscape, white blanket",
    "暴雪": "blizzard, heavy snow storm",
    "雾天": "foggy misty atmosphere",
    "有雾": "foggy misty atmosphere",
    "晨雾": "morning mist, dreamy fog",
    "风暴": "stormy weather, dramatic clouds",
    "雷雨": "thunderstorm, lightning in sky",
}

SEASON_KEYWORDS: Dict[str, str] = {
    "春天": "spring season, cherry blossoms, fresh green",
    "春季": "spring season, cherry blossoms, fresh green",
    "夏天": "summer season, lush greenery, warm sun",
    "夏季": "summer season, lush greenery, warm sun",
    "秋天": "autumn season, golden foliage, maple leaves",
    "秋季": "autumn season, golden foliage, maple leaves",
    "冬天": "winter season, snow, bare branches",
    "冬季": "winter season, snow, bare branches",
    "樱花季": "cherry blossom season, sakura petals falling",
    "枫叶季": "maple season, red foliage",
}

# ─────────────────────────────────────────────────────────
# 质量档位（v2.1 新增）
# ─────────────────────────────────────────────────────────
QUALITY_TIERS: Dict[str, str] = {
    "basic": "high quality, detailed",
    "pro": "masterpiece, best quality, ultra detailed, 8k",
    "master": "masterpiece, best quality, ultra detailed, 8k, hdr, "
              "intricate details, sharp focus, award winning, trending on artstation, "
              "professional, highly polished",
}

# ─────────────────────────────────────────────────────────
# 负向需求识别（v2.1 新增）
# 匹配 "不要X" / "no X" / "avoid X" / "without X" / "没有X" / "避免X"
# ─────────────────────────────────────────────────────────
NEGATIVE_PATTERNS = [
    re.compile(r"不要([^,，。.;；]{1,20})"),
    re.compile(r"没有([^,，。.;；]{1,20})"),
    re.compile(r"避免([^,，。.;；]{1,20})"),
    re.compile(r"\bno\s+([a-zA-Z\s]{1,30})(?=[,.]|\s*$)"),
    re.compile(r"\bavoid\s+([a-zA-Z\s]{1,30})(?=[,.]|\s*$)"),
    re.compile(r"\bwithout\s+([a-zA-Z\s]{1,30})(?=[,.]|\s*$)"),
]

# ─────────────────────────────────────────────────────────
# 画幅 → 模型特定写法
# ─────────────────────────────────────────────────────────
ASPECT_TO_MJ = {
    "1:1": "--ar 1:1",
    "3:4": "--ar 3:4",
    "4:3": "--ar 4:3",
    "3:2": "--ar 3:2",
    "2:3": "--ar 2:3",
    "16:9": "--ar 16:9",
    "9:16": "--ar 9:16",
    "21:9": "--ar 21:9",
    "4:5": "--ar 4:5",
}

ASPECT_TO_SDXL = {
    "1:1": "1024x1024",
    "3:4": "896x1152",
    "4:3": "1152x896",
    "3:2": "1216x832",
    "2:3": "832x1216",
    "16:9": "1344x768",
    "9:16": "768x1344",
    "21:9": "1536x640",
    "4:5": "912x1144",
}


# ─────────────────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────────────────
def resolve_preset(name: Optional[str]) -> str:
    """预设名归一化：支持中文 / 英文别名 / 大小写不敏感。"""
    if not name:
        return ""
    key = name.strip().lower().replace(" ", "").replace("-", "").replace("_", "")
    if key in ALIASES:
        return ALIASES[key]
    for p in STYLE_PRESETS:
        if p.lower() == key or p.lower().replace(" ", "") == key:
            return p
    return name if name in STYLE_PRESETS else ""


def parse_requirement(text: str) -> Dict[str, str]:
    """从用户输入中解析意图、画幅、构图、情绪、时间、天气、季节、负向需求。

    返回 dict 字段：
        preset_suggestion  推荐预设（可能为空）
        aspect_suggestion  推荐画幅
        composition        构图片段（英文，可为空）
        mood               情绪片段（英文，可为空）
        time_of_day        时间片段（英文，可为空）
        weather            天气片段（英文，可为空）
        season             季节片段（英文，可为空）
        user_negatives     用户抽出的负向关键词（原文，英/中）
    """
    lower = text.lower()
    out = {
        "preset_suggestion": "",
        "aspect_suggestion": "",
        "composition": "",
        "mood": "",
        "time_of_day": "",
        "weather": "",
        "season": "",
        "user_negatives": [],
    }

    for kw, preset, aspect in INTENT_KEYWORDS:
        if kw.lower() in lower:
            out["preset_suggestion"] = preset
            out["aspect_suggestion"] = aspect
            break

    for zh, en in COMPOSITION_KEYWORDS.items():
        if zh in text:
            out["composition"] = en
            break

    for zh, en in MOOD_KEYWORDS.items():
        if zh in text:
            out["mood"] = en
            break

    for zh, en in TIME_KEYWORDS.items():
        if zh in text:
            out["time_of_day"] = en
            break

    for zh, en in WEATHER_KEYWORDS.items():
        if zh in text:
            out["weather"] = en
            break

    for zh, en in SEASON_KEYWORDS.items():
        if zh in text:
            out["season"] = en
            break

    # 负向需求抽取
    negs: List[str] = []
    for pat in NEGATIVE_PATTERNS:
        for m in pat.finditer(text):
            token = m.group(1).strip().rstrip(",.， ；;")
            if token and token not in negs:
                negs.append(token)
    out["user_negatives"] = negs

    return out


def strip_negative_clauses(text: str) -> str:
    """从主体描述中去除 "不要X" 类子句，只保留正向描述。"""
    cleaned = text
    for pat in NEGATIVE_PATTERNS:
        cleaned = pat.sub("", cleaned)
    # 清理多余标点和空白
    cleaned = re.sub(r"\s*,\s*,+", ", ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" ,，。.;；")
    return cleaned


def sanitize_subject(text: str) -> str:
    """清理主体描述：去除首尾标点和多余空白。"""
    return re.sub(r"\s+", " ", text).strip().rstrip(".,，、。;；")


def stable_seed(subject: str, preset: str) -> int:
    """根据主体 + 预设生成稳定的种子建议（32-bit 正整数）。"""
    h = hashlib.md5(f"{subject}|{preset}".encode("utf-8")).hexdigest()
    return int(h[:8], 16)


def parse_mix_preset(preset_arg: str) -> Tuple[str, Optional[str]]:
    """支持 `-p A+B` 语法。返回 (primary, secondary or None)。"""
    if not preset_arg:
        return "", None
    if "+" not in preset_arg:
        return preset_arg, None
    parts = [p.strip() for p in preset_arg.split("+", 1)]
    if len(parts) != 2 or not parts[0] or not parts[1]:
        return preset_arg, None
    return parts[0], parts[1]


def mix_presets(primary: str, secondary: str, ratio: float = 0.6, model: str = "通用") -> Dict[str, str]:
    """加权融合两个预设，主预设 ratio，副预设 1-ratio。

    融合策略：
        tags     按权重前置主预设标签，SD 模式额外加 (tag:weight) 语法
        quality  主预设主导
        neg      合并去重
        camera   主预设（主导镜头语言）
        lighting 主预设主导，副预设为辅
        palette  混合两者（主在前）
        aspect   主预设
        category mix
    """
    p1 = STYLE_PRESETS[primary]
    p2 = STYLE_PRESETS[secondary]
    ratio = max(0.1, min(0.9, ratio))

    primary_tags = [t.strip() for t in p1["tags"].split(",") if t.strip()]
    secondary_tags = [t.strip() for t in p2["tags"].split(",") if t.strip()]

    is_sd = model in ("Stable Diffusion", "SD", "sd", "SDXL", "sdxl")
    if is_sd:
        w1 = round(0.8 + ratio * 0.6, 2)
        w2 = round(0.8 + (1 - ratio) * 0.6, 2)
        merged_tags = [f"({t}:{w1})" for t in primary_tags] + [f"({t}:{w2})" for t in secondary_tags]
    else:
        n1 = max(1, int(round(len(primary_tags) * (0.5 + ratio))))
        n2 = max(1, int(round(len(secondary_tags) * (0.5 + (1 - ratio)))))
        merged_tags = primary_tags[:n1] + secondary_tags[:n2]

    merged_palette = ", ".join([
        x for x in [p1.get("palette", ""), p2.get("palette", "")] if x
    ])
    if p1.get("lighting") and p2.get("lighting"):
        merged_lighting = f"{p1['lighting']}, blended with {p2['lighting']}"
    else:
        merged_lighting = p1.get("lighting") or p2.get("lighting", "")

    neg_tokens = []
    seen = set()
    for src in (p1["neg"], p2["neg"]):
        for t in src.split(","):
            t = t.strip()
            if t and t.lower() not in seen:
                seen.add(t.lower())
                neg_tokens.append(t)

    return {
        "category": f"{p1['category']}+{p2['category']}",
        "tags": ", ".join(merged_tags),
        "quality": p1["quality"],
        "neg": ", ".join(neg_tokens),
        "camera": p1.get("camera", "") or p2.get("camera", ""),
        "lighting": merged_lighting,
        "palette": merged_palette,
        "aspect": p1.get("aspect", "1:1"),
    }


def build_prompt(
    subject: str,
    preset: str,
    model: str = "通用",
    aspect: str = "",
    extra_mood: str = "",
    extra_composition: str = "",
    extra_negatives: str = "",
    seed: Optional[int] = None,
    quality_tier: str = "pro",
    character_sheet: bool = False,
    mix_secondary: Optional[str] = None,
    mix_ratio: float = 0.6,
) -> Dict:
    """构建增强后的提示词。

    v2.1 新增参数：
        extra_negatives  额外负面词，逗号分隔
        quality_tier     质量档位 basic / pro / master
        character_sheet  角色设定图模式（T-pose 多视图）
    v2.2 新增参数：
        mix_secondary    副预设名（已 resolve），与主预设融合
        mix_ratio        主预设权重 0.1-0.9
    """
    preset = resolve_preset(preset) or "写实摄影"
    if mix_secondary:
        mix_secondary = resolve_preset(mix_secondary) or ""
    if mix_secondary and mix_secondary != preset:
        data = mix_presets(preset, mix_secondary, mix_ratio, model)
        mixed_label = f"{preset}+{mix_secondary}@{mix_ratio:.2f}"
    else:
        data = STYLE_PRESETS[preset]
        mixed_label = ""

    auto = parse_requirement(subject)
    subject_clean = sanitize_subject(strip_negative_clauses(subject))

    if not extra_composition:
        extra_composition = auto["composition"]
    if not extra_mood:
        extra_mood = auto["mood"]
    if not aspect:
        aspect = data.get("aspect", "1:1")

    # 时间 / 天气 / 季节
    ambient_parts = [auto["time_of_day"], auto["weather"], auto["season"]]
    ambient = ", ".join([x for x in ambient_parts if x])

    # 角色设定图模式
    if character_sheet:
        subject_clean = (
            f"character design sheet of {subject_clean}, "
            f"multiple views: front view, three-quarter view, side view, back view, "
            f"T-pose, clean white background, reference sheet, "
            f"consistent character design"
        )
        aspect = "16:9"

    consistency_parts = [
        data["tags"],
        data.get("camera", ""),
        data.get("lighting", ""),
        data.get("palette", ""),
    ]
    consistency = ", ".join([x for x in consistency_parts if x])

    # 质量档位（替换 UNIVERSAL_QUALITY）
    tier_quality = QUALITY_TIERS.get(quality_tier, QUALITY_TIERS["pro"])
    quality_combined = f"{data['quality']}, {tier_quality}"

    # 负面词：预设 + 全局过滤 + 用户抽出 + 显式追加
    neg_exclude = list(PRESET_NEG_EXCLUDE.get(preset, []))
    if mix_secondary and mix_secondary in PRESET_NEG_EXCLUDE:
        neg_exclude.extend(PRESET_NEG_EXCLUDE[mix_secondary])
    universal_neg_filtered = _filter_neg(UNIVERSAL_NEG, neg_exclude)
    user_neg_from_subject = ", ".join(auto["user_negatives"])
    neg_parts = [data["neg"], universal_neg_filtered, user_neg_from_subject, extra_negatives]
    neg_combined = ", ".join([x for x in neg_parts if x])

    extras = ", ".join([x for x in [extra_composition, extra_mood, ambient] if x])

    seed_key = mixed_label or preset

    # 按模型生成不同形式
    if model in ("Midjourney", "MJ", "mj"):
        core = f"{subject_clean}, {consistency}"
        if extras:
            core = f"{core}, {extras}"
        core = f"{core}, {quality_combined}"
        flags = [ASPECT_TO_MJ.get(aspect, "--ar 1:1"), "--stylize 250"]
        positive = f"{core} {' '.join(flags)}"
        negative = f"--no {neg_combined}"
        hint = (
            "Midjourney tips：\n"
            "  • 角色/产品系列一致：加 --cref <url> 或 --sref <url>\n"
            f"  • 想要更风格化加 --stylize 500~750；更写实降到 --stylize 50\n"
            f"  • 建议 seed 锁定：--seed {seed or stable_seed(subject_clean, seed_key)}"
        )

    elif model in ("Stable Diffusion", "SD", "sd"):
        positive = (
            f"({subject_clean}:1.2), {consistency}"
            + (f", {extras}" if extras else "")
            + f", {quality_combined}"
        )
        negative = neg_combined
        hint = (
            "Stable Diffusion tips：\n"
            f"  • 强化权重: (word:1.2~1.5), 减弱: [word:0.7]\n"
            f"  • 建议尺寸 (SD 1.5): 512x{{hw_from_aspect}}; (SDXL): {ASPECT_TO_SDXL.get(aspect,'1024x1024')}\n"
            f"  • 采样: DPM++ 2M Karras, 30 steps, CFG 6.5\n"
            f"  • 建议 seed 锁定: {seed or stable_seed(subject_clean, seed_key)}（系列同 seed 提升一致性）"
        )

    elif model in ("SDXL", "sdxl"):
        positive = (
            f"{subject_clean}, {consistency}"
            + (f", {extras}" if extras else "")
            + f", {quality_combined}"
        )
        negative = neg_combined
        hint = (
            "SDXL tips：\n"
            f"  • 推荐尺寸: {ASPECT_TO_SDXL.get(aspect,'1024x1024')}\n"
            f"  • 采样: DPM++ SDE Karras, 25-30 steps, CFG 5-7\n"
            f"  • Refiner 使用率 0.2-0.3\n"
            f"  • seed: {seed or stable_seed(subject_clean, seed_key)}"
        )

    elif model in ("DALL-E", "DALL·E", "dalle", "DALLE"):
        parts = [f"A {preset} style image of {subject_clean}"]
        if data.get("camera"):
            parts.append(f"captured with {data['camera']}")
        if data.get("lighting"):
            parts.append(f"lit by {data['lighting']}")
        if data.get("palette"):
            parts.append(f"with a color palette of {data['palette']}")
        if extras:
            parts.append(extras)
        parts.append("highly detailed, professional composition")
        positive = ". ".join(parts) + "."
        negative = "(DALL-E 3 忽略负面提示，已通过正向描述规避)"
        hint = (
            "DALL-E 3 tips：\n"
            "  • 用自然语言句子 + 细节形容词效果最佳\n"
            f"  • 画幅: {aspect} (仅支持 1:1, 16:9, 9:16 在 ChatGPT 内)\n"
            "  • 一致性: 在同一会话连续生成并引用 \"use the same character\""
        )

    elif model in ("Flux", "flux"):
        positive = (
            f"{subject_clean}. {consistency}."
            + (f" {extras}." if extras else "")
            + f" {quality_combined}."
        )
        negative = neg_combined
        hint = (
            "Flux tips：\n"
            "  • 支持长自然语言提示，可加句式结构 \"The subject is...\"\n"
            f"  • 建议 Flux Dev: guidance 3.5; Flux Schnell: guidance 0\n"
            f"  • seed: {seed or stable_seed(subject_clean, seed_key)}"
        )

    else:  # 通用
        positive = (
            f"{subject_clean}, {consistency}"
            + (f", {extras}" if extras else "")
            + f", {quality_combined}"
        )
        negative = neg_combined
        hint = "通用格式：Midjourney / SD / Flux 皆可直接使用。"

    return {
        "version": VERSION,
        "original": subject,
        "preset": preset,
        "mix_secondary": mix_secondary or "",
        "mix_ratio": mix_ratio if mix_secondary else None,
        "mix_label": mixed_label,
        "model": model,
        "aspect": aspect,
        "composition": extra_composition,
        "mood": extra_mood,
        "time_of_day": auto.get("time_of_day", ""),
        "weather": auto.get("weather", ""),
        "season": auto.get("season", ""),
        "quality_tier": quality_tier,
        "character_sheet": character_sheet,
        "user_negatives": auto.get("user_negatives", []),
        "seed_suggestion": seed or stable_seed(subject_clean, seed_key),
        "positive": positive,
        "negative": negative,
        "hint": hint,
        "consistency_lock": {
            "camera": data.get("camera", ""),
            "lighting": data.get("lighting", ""),
            "palette": data.get("palette", ""),
            "aspect": aspect,
        },
    }


def build_series(
    subject: str,
    preset: str,
    model: str,
    aspect: str,
    variations: List[str],
    seed: Optional[int] = None,
    quality_tier: str = "pro",
    mix_secondary: Optional[str] = None,
    mix_ratio: float = 0.6,
) -> List[Dict]:
    """系列批量生成：共享 camera/lighting/palette/seed 锁，仅替换主体描述。"""
    if seed is None:
        seed_key = f"{preset}+{mix_secondary}@{mix_ratio:.2f}" if mix_secondary else preset
        seed = stable_seed(subject, seed_key)
    results = []
    for i, v in enumerate(variations, 1):
        full = f"{subject}, {v}" if v and v != subject else subject
        r = build_prompt(
            full, preset, model, aspect, seed=seed, quality_tier=quality_tier,
            mix_secondary=mix_secondary, mix_ratio=mix_ratio,
        )
        r["series_index"] = i
        r["series_total"] = len(variations)
        results.append(r)
    return results


# ─────────────────────────────────────────────────────────
# 输出
# ─────────────────────────────────────────────────────────
def print_prompt(result: Dict):
    sep = "═" * 60
    print(f"\n{sep}")
    if "series_index" in result:
        print(f"📸 系列生成 [{result['series_index']}/{result['series_total']}]")
    if result.get("character_sheet"):
        print("👤 角色设定图模式：T-pose 多视图（喂给 MJ --cref / IP-Adapter）")
    print(f"📌 原始描述   : {result['original']}")
    if result.get("mix_label"):
        print(f"🎨 风格预设   : {result['mix_label']} (混合)")
    else:
        print(f"🎨 风格预设   : {result['preset']}")
    print(f"🤖 目标模型   : {result['model']}")
    print(f"📐 画幅       : {result['aspect']}")
    print(f"⭐ 质量档位   : {result.get('quality_tier', 'pro')}")
    if result.get("composition"):
        print(f"🎥 构图       : {result['composition']}")
    if result.get("mood"):
        print(f"🎭 情绪       : {result['mood']}")
    if result.get("time_of_day"):
        print(f"🕐 时间       : {result['time_of_day']}")
    if result.get("weather"):
        print(f"☁️  天气       : {result['weather']}")
    if result.get("season"):
        print(f"🍂 季节       : {result['season']}")
    if result.get("user_negatives"):
        print(f"🚫 用户负向   : {', '.join(result['user_negatives'])}  → 已入负面")
    print(f"🎲 种子建议   : {result['seed_suggestion']}")
    print(f"\n✅ 正向提示词：")
    print(f"{result['positive']}")
    print(f"\n❌ 负向提示词：")
    print(f"{result['negative']}")
    print(f"\n🔒 一致性锁：")
    for k, v in result["consistency_lock"].items():
        if v:
            print(f"   {k:8s}: {v}")
    print(f"\n💡 {result['hint']}")
    print(f"{sep}\n")


def list_presets():
    by_cat: Dict[str, List[str]] = {}
    for name, data in STYLE_PRESETS.items():
        by_cat.setdefault(data["category"], []).append(name)
    print(f"\n🎨 可用风格预设 (共 {len(STYLE_PRESETS)} 款)")
    print("─" * 50)
    order = ["摄影", "动漫", "插画", "3D", "设计", "艺术", "场景", "游戏", "东方"]
    for cat in order:
        if cat not in by_cat:
            continue
        print(f"\n【{cat}】 {len(by_cat[cat])} 款")
        for name in by_cat[cat]:
            print(f"  • {name}")
    print(
        "\n💡 同义别名示例：anime, ghibli, cyberpunk, genshin, lol, "
        "dunhuang, hanfu, glassmorphism, bauhaus, brutalism, healing, cozy ...\n"
    )


# ─────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description=f"huo15-img-test v{VERSION} — T2I 提示词增强工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础
  enhance_prompt.py "一只赛博朋克风格的猫" -p 赛博朋克 -m Midjourney

  # 自动意图 + 时间 / 天气 / 季节 / 负向需求识别
  enhance_prompt.py "雨天黄昏的东京巷弄，忧郁氛围，不要人物"
  enhance_prompt.py "秋天樱花季汉服写真"

  # 新预设（v2.1）
  enhance_prompt.py "双马尾少女" -p 原神 -t master
  enhance_prompt.py "手持月亮的神女" -p 敦煌壁画
  enhance_prompt.py "极简仪表盘UI" -p 玻璃拟态

  # 角色设定图（给 Midjourney --cref 做参考）
  enhance_prompt.py "银发机甲少女" -p 动漫 --character-sheet -m Midjourney

  # 混合预设（v2.2）
  enhance_prompt.py "持剑女侠" -p "赛博朋克+水墨" --mix 0.6 -m Midjourney
  enhance_prompt.py "山中神女" -p "原神+敦煌壁画" --mix 0.5 -m SDXL

  # 系列一致性（4 张共享 camera/lighting/palette/seed）
  enhance_prompt.py "一个红发女侠" -p 动漫 -s 4 \\
      --variations "持剑站立,骑马奔驰,弯弓射箭,与龙对视"

  # 质量档位 + 显式负面追加
  enhance_prompt.py "品牌展台" -p 品牌KV -t master --avoid "cluttered, people"

  # JSON 输出
  enhance_prompt.py "极简Logo一朵山茶花" -p Logo设计 -j
""",
    )
    parser.add_argument("subject", nargs="?", help="要生成图片的主体描述")
    parser.add_argument(
        "-p", "--preset",
        help="风格预设（中文 / 英文别名）。混合：'赛博朋克+水墨' 或 'genshin+dunhuang'（v2.2）",
    )
    parser.add_argument(
        "--mix", type=float, default=0.6,
        help="主预设权重 0.1-0.9，仅在 -p A+B 混合时生效（默认 0.6，主导主预设）",
    )
    parser.add_argument(
        "-m", "--model", default="通用",
        help="目标模型: Midjourney / SD / SDXL / DALL-E / Flux / 通用",
    )
    parser.add_argument("-a", "--aspect", default="", help="画幅: 1:1 / 3:4 / 16:9 / 21:9 ...")
    parser.add_argument("--mood", default="", help="情绪覆盖")
    parser.add_argument("--composition", default="", help="构图覆盖")
    parser.add_argument("--avoid", default="", help="额外负面词，逗号分隔（v2.1）")
    parser.add_argument(
        "-t", "--tier", choices=["basic", "pro", "master"], default="pro",
        help="质量档位 basic/pro/master，默认 pro（v2.1）",
    )
    parser.add_argument(
        "-cs", "--character-sheet", action="store_true",
        help="角色设定图模式：T-pose 多视图，适合给 MJ --cref 做角色参考（v2.1）",
    )
    parser.add_argument("--seed", type=int, help="种子（不给则哈希生成稳定 seed）")
    parser.add_argument("-s", "--series", type=int, default=1, help="系列张数（配合 --variations 使用）")
    parser.add_argument("--variations", default="", help="系列变体，逗号分隔，如 '持剑,骑马,射箭'")
    parser.add_argument("--polish", action="store_true",
                        help="先用 Claude API 智能润色（需 ANTHROPIC_API_KEY）后再增强（v2.3）")
    parser.add_argument("--safety", default="",
                        help="平台合规润色：DALL-E/MJ/SD/SDXL/Flux，自动重写艺术词避免误判（v2.3）")
    parser.add_argument("-l", "--list", action="store_true", help="列出所有预设")
    parser.add_argument("-j", "--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{VERSION}")

    args = parser.parse_args()

    if args.list:
        list_presets()
        return

    if not args.subject:
        parser.print_help()
        sys.exit(1)

    subject = args.subject
    polish_meta: Optional[Dict] = None
    safety_meta: Optional[Dict] = None
    preset_override = args.preset
    aspect_override = args.aspect
    mix_override = None

    # v2.3: Claude 智能润色（前置）
    if args.polish:
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from claude_polish import call_claude, parse_claude_json
            resp = call_claude(subject)
            polished = parse_claude_json(resp)
            if polished.get("error"):
                print(f"❌ Claude 润色拒答: {polished['error']}", file=sys.stderr)
                sys.exit(2)
            subject = polished.get("subject_refined_zh") or subject
            if not preset_override:
                pri = polished.get("style_preset", "")
                sec = polished.get("style_preset_secondary", "")
                if pri and sec:
                    preset_override = f"{pri}+{sec}"
                    mix_override = polished.get("mix_ratio", 0.6)
                elif pri:
                    preset_override = pri
            if not aspect_override and polished.get("aspect"):
                aspect_override = polished["aspect"]
            polish_meta = polished
        except Exception as e:
            print(f"⚠️  Claude 润色失败，回退到原描述: {e}", file=sys.stderr)

    # v2.3: 平台合规润色
    if args.safety:
        try:
            from safety_lint import lint as safety_lint
            r = safety_lint(subject, platform=args.safety)
            if r["verdict"] == "REJECT":
                print(f"🚫 命中红线: {r['reason']}\n类别: {', '.join(r.get('categories', []))}", file=sys.stderr)
                print(r.get("advice", ""), file=sys.stderr)
                sys.exit(2)
            if r["verdict"] == "REWRITE":
                subject = r["rewritten"]
            safety_meta = r
        except ImportError:
            print(f"⚠️  safety_lint 模块未找到", file=sys.stderr)

    # 自动推荐
    auto = parse_requirement(subject)
    raw_preset = preset_override or auto["preset_suggestion"] or "写实摄影"
    primary_raw, secondary_raw = parse_mix_preset(raw_preset)
    preset = primary_raw
    mix_secondary = secondary_raw

    # 校验混合预设
    if mix_secondary:
        primary_resolved = resolve_preset(preset)
        secondary_resolved = resolve_preset(mix_secondary)
        if not primary_resolved or not secondary_resolved:
            unknown = [n for n, r in [(preset, primary_resolved), (mix_secondary, secondary_resolved)] if not r]
            print(f"❌ 未知预设：{', '.join(unknown)}（运行 -l 查看列表）", file=sys.stderr)
            sys.exit(1)
        preset = primary_resolved
        mix_secondary = secondary_resolved

    aspect = aspect_override or auto["aspect_suggestion"] or STYLE_PRESETS.get(resolve_preset(preset) or "写实摄影", {}).get("aspect", "1:1")

    # 混合权重（polish 推荐 > CLI --mix）
    effective_mix = mix_override if mix_override is not None else args.mix

    # 系列模式
    if args.series > 1 or args.variations:
        variations = [v.strip() for v in args.variations.split(",") if v.strip()]
        if not variations:
            variations = [subject] * args.series
        elif len(variations) < args.series:
            variations += [variations[-1]] * (args.series - len(variations))
        results = build_series(
            subject, preset, args.model, aspect,
            variations[: max(args.series, len(variations))],
            seed=args.seed, quality_tier=args.tier,
            mix_secondary=mix_secondary, mix_ratio=effective_mix,
        )
        if args.json:
            out = {"version": VERSION, "series": results}
            if polish_meta: out["claude_polish"] = polish_meta
            if safety_meta: out["safety_lint"] = safety_meta
            print(json.dumps(out, ensure_ascii=False, indent=2))
        else:
            if polish_meta:
                print(f"✨ Claude 已润色 → 主体: {subject}")
            if safety_meta and safety_meta.get("verdict") == "REWRITE":
                print(f"🛡  平台合规重写 → {subject}")
            for r in results:
                print_prompt(r)
            print(f"🔐 本系列 {len(results)} 张共享 seed = {results[0]['seed_suggestion']}，一致性锁见每张「🔒」区块。")
        return

    # 单张
    result = build_prompt(
        subject, preset, args.model, aspect,
        extra_mood=args.mood, extra_composition=args.composition,
        extra_negatives=args.avoid, seed=args.seed,
        quality_tier=args.tier, character_sheet=args.character_sheet,
        mix_secondary=mix_secondary, mix_ratio=effective_mix,
    )
    if polish_meta:
        result["claude_polish"] = polish_meta
    if safety_meta:
        result["safety_lint"] = safety_meta

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if polish_meta:
            print(f"✨ Claude 已润色 (in={polish_meta.get('_usage',{}).get('input_tokens',0)}/out={polish_meta.get('_usage',{}).get('output_tokens',0)} tokens)")
        if safety_meta and safety_meta.get("verdict") == "REWRITE":
            print(f"🛡  平台合规已重写: {len(safety_meta.get('substitutions',[]))} 处替换 (target={safety_meta['platform']})")
        print_prompt(result)


if __name__ == "__main__":
    main()
