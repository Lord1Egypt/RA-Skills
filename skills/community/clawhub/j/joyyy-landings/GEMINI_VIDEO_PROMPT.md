# Промпт для Gemini Video (Veo) — Skill Demo

Сгенерируй видео → сохрани как файл → примени скрипт из репо.

---

## 1. Основной промпт (скопируй в Gemini Video)

**English (рекомендуется для Veo):**

```
30–45 second video, 16:9, 1920x1080. Dark background (#050508, near black). Accent color warm orange (#ff8c42). Data visualization and interactive prototype showcase mood.

Scene 1 (0–8 s): Abstract landing page with floating card-like panels in a grid. Subtle orange glow on edges. Slow camera push forward. Monospace typography feel, minimal UI.

Scene 2 (8–16 s): A smooth curve rising then dropping — like a multiplier or bankroll chart. Orange line on dark, thin grid. Graph grows and fades. Clean, analytical.

Scene 3 (16–24 s): Procedural pattern: terrain or map tiles generating from noise. Dark base, orange highlights on peaks or borders. Infinite scroll feel, subtle parallax.

Scene 4 (24–35 s): Dashboard with small charts and numbers. Orange accents, dark cards. Histogram bars or distribution shape appearing. Professional, investor-ready.

Scene 5 (35–45 s): Pull back to a single glowing orange dot or line, then fade to black. No text, no logos. Mood: interactive systems, prototypes, human and AI built. Cinematic, calm, no fast cuts.
```

**Краткая версия (если лимит символов):**

```
45 sec, 16:9. Dark background #050508, orange accent #ff8c42. Data viz / prototype showcase: (1) floating card grid, orange glow, (2) rising curve chart, (3) procedural map tiles, (4) dashboard with charts, (5) fade to black. Cinematic, calm, professional. No text.
```

---

## 2. Сразу после генерации — применить свой скрипт

1. Скачай видео из Gemini (например `gemini_skill_demo.mp4`) в репозиторий (корень или `SMM/`).

2. Обработка в стиле Neuro (bloom, breath, color shift):

```bash
# из корня neuro
python3 SMM/process_video.py gemini_skill_demo.mp4 -o skill_demo_processed.mp4
```

3. Или только пережать/оптимизировать без эффектов — используй тот же скрипт с нужными флагами (см. `SMM/README_VIDEO.md`).

4. Готовый файл `skill_demo_processed.mp4` залей на YouTube/Vimeo и ссылку вставь в листинг ClawHub.

---

## 3. Параметры под скрипт

Чтобы `SMM/process_video.py` отработал без сюрпризов:

- **Формат:** MP4, 16:9.
- **Длительность:** 30–60 сек (скрипт тянет любой размер).
- **Стиль:** тёмный фон, плавное движение — скрипт добавляет glow, breath, сдвиг цвета в палитре Neuro.

---

## 4. Альтернатива без генератора

Если не используешь Gemini Video, собери демо из своих скриншотов:

```bash
cd skills/joyyy-landings
python3 capture_screenshots.py
python3 make_demo_video.py
# → demo_30s.mp4
```
