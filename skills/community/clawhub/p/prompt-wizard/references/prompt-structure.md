# GPT-Image-2 Prompt Structure Reference

## The 6 Dimensions

A high-quality GPT-Image-2 prompt covers these dimensions. Not every prompt needs all six, but each missing dimension is a decision left to the model.

### 1. Subject

Who or what is the main focus? Describe physical features, pose, expression, clothing, accessories.

Key questions:
- Person, product, scene, or abstract concept?
- Age, expression, body language?
- Key visual features (hair, skin, build, clothing layers)?
- Props or objects carried?

### 2. Environment

Where is the subject placed? What is the spatial and temporal context?

Key questions:
- Indoor/outdoor? Specific setting type?
- Time of day, season, weather?
- Background elements, architecture, nature?
- Negative space or dense detail?

### 3. Lighting

Lighting defines mood, depth, and realism. Be specific about source, quality, and color.

Key questions:
- Natural (golden hour, overcast, moonlight) or artificial (studio, neon, flash)?
- Direction: front/side/back/rim/top?
- Quality: soft diffused vs. hard/high-contrast?
- Color temperature: warm/amber, cool/blue, neutral, colored gels?
- Special: volumetric rays, lens flares, rim highlights, chiaroscuro?

### 4. Composition & Camera

Framing and lens choices strongly influence the final look.

Key questions:
- Shot distance: extreme close-up, close-up, medium, wide, establishing?
- Angle: eye-level, low angle, high angle, bird's eye, Dutch tilt?
- Lens feel: wide (24mm), normal (50mm), telephoto (85-135mm)?
- Aperture: shallow DOF (f/1.2-1.8) for separation, deep (f/8+) for landscapes?
- Special: anamorphic, macro, tilt-shift, fisheye?

### 5. Style & Aesthetic

Reference genres, art movements, media formats, or specific artists.

Key questions:
- Medium: photorealistic, illustration, 3D/CGI, oil painting, ink, pixel art?
- Genre: cinematic, editorial, street, commercial, fine art, anime, concept art?
- Era/style: vintage 80s, cyberpunk, baroque, minimalist, brutalist?
- Color palette keywords: muted/pastel/vibrant/monochrome/desaturated?
- Reference: "in the style of [artist/genre]" or film/era references?

### 6. Technical Parameters

Specify output constraints and quality controls.

Key questions:
- Aspect ratio: 1:1, 3:2, 4:5, 9:16, 16:9?
- Resolution keywords: 4K, 8K, high detail, sharp focus?
- Negative prompts: what to exclude (text, watermark, distortion, etc.)?
- Special: transparent background, multi-panel grid, consistent character sheets?

## Prompt Assembly Template

```
[Subject description] in [environment/setting]. [Lighting details]. [Composition and camera specs]. [Style reference and aesthetic]. [Technical parameters].

Optional negative prompt: [exclusions]
```

## Writing Tips

- Be **specific, not vague**: "golden hour sunlight streaming through venetian blinds" > "nice lighting"
- Use **technical vocabulary**: f-stop, focal length, lighting setups, film stocks
- Add **sensory adjectives**: glossy, matte, rough, smooth, translucent, iridescent
- Include **motion clues**: static, dynamic, mid-stride, flowing, suspended, drifting
- **Relative positioning**: foreground, midground, background, left/right/center
- **Count objects** for precision: "exactly 3 visible vehicles"
- **Parameterize** with `{argument name="label" default="value"}` for reusable templates
