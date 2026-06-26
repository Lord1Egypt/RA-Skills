# NovelCraft Module Template: Images

## Task for Subagent

Generate images for the book using configured provider.

**STEP 1: Load Configuration**
Read these files:
1. `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/project-manifest.md`
2. `/home/felix/.openclaw/workspace/novelcraft/config/module-images.md`
3. `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/00-concept/image_requests.md`

**EXTRACT IMAGE DIMENSIONS from module-images.md:**
Look for resolution configuration in the "Auflösungen pro Bildtyp" section.
If not found, use these defaults:
- cover: 768×1024
- portraits: 512×768
- world_visuals: 1024×512
- chapter_visuals: 512×512

**STEP 2: Generate Images**
Provider: MFLUX-WebUI at http://192.168.2.150:7861
Settings: low_ram=true

**STEP 3: Output Files**
Save to: `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/images/`

Use dimensions from config (STEP 1). If config specifies different sizes, use those.

| File | Priority | Default Size | Config Key |
|------|----------|--------------|------------|
| cover.png | 1 - First | 768×1024 | cover |
| {character}.png | 2 | 512×768 | portraits |
| {setting}.png | 3 - Optional | 1024×512 | world_visuals |
| chapter_{NN}.png | 4 - Optional | 512×512 | chapter_visuals |

**STEP 4: Rules**
- Start immediately, don't wait
- Note estimated time (~40-55 min)
- Retry failed images once
- Report completion but DON'T block

**STEP 5: Report**
List all generated files with paths.
