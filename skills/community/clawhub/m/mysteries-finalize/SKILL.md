---
name: "mysteries-finalize"
description: "Updated Phase 4: Smart Thumbnail Generation to output a `Featured_v2` variant that scales the full image and fills margins seamlessly."
---

# Mysteries Finalize Protocol

This skill automates the finalization process of a Farsight video project, handling transcription, translation, and thumbnail generation.

## Trigger
Use this skill when the user asks to "run the mysteries finalize protocol", finalize a project, or prepare the final Farsight assets.

## Phase 1: Pre-flight Verification (CRITICAL)
Before starting any processing, the AI MUST verify the workspace:
1. Navigate to the project's `Renders/Final/` directory.
2. Confirm the presence of ALL three primary assets:
   - The finalized video file (`.mp4` or `.mov`)
   - The finalized audio file (`.wav` or `.mp3`)
   - The base 1080p thumbnail image (`.jpg` or `.png`)
3. If any of these are missing, pause and alert the user to place them in the folder before proceeding. The project title is inferred from these files.

## Phase 2: Audio Processing & Transcription
1. **Convert for Whisper:** Use `ffmpeg` to convert the audio to a 16kHz mono `.wav` file.
   ```bash
   ffmpeg -i "<input>" -ar 16000 -ac 1 -c:a pcm_s16le "<output_16k.wav>"
   ```
2. **Transcribe:** Run `whisper-cli` using the local `ggml-base.en.bin` model to generate:
   - A text transcript (`.txt`)
   - An English subtitle file (`.srt`)

## Phase 3: Global Localization
1. Use a Python script with the `srt` and `deep-translator` libraries to translate the English `.srt` into the 12 Farsight standard languages:
   - Arabic (`Arabic`), Chinese Simplified (`Chinese_Simplified`), German (`Deutsch`), Spanish (`Espanol`), French (`Francais`), Italian (`Italiano`), Japanese (`Japanese`), Swahili (`Kiswahili`), Korean (`Korean`), Portuguese (`Portugues`), Russian (`Russian`), Thai (`Thai`).
2. Ensure API batching and pauses are respected to avoid rate limits during translation.

## Phase 4: Smart Thumbnail Generation
1. **Locate Base Thumbnail:** Use the 1920x1080 base thumbnail verified in Phase 1.
2. **Scale & Crop:** Use a Python script utilizing `PIL.ImageOps.fit` to resize and crop the image *without* stretching or squeezing.
   - For most thumbnails, use `centering=(0.5, 1.0)` (bottom anchor) so the main title at the bottom is never cut off.
   - **Special Rule for "Featured" (Original):** For the 3840x1440 Featured thumbnail, adjust the crop anchor slightly higher (e.g., `centering=(0.5, 0.82)`) to intentionally crop out the "Only Available on Farsight Prime.com" footer text while keeping the main title in frame.
   - **Special Rule for "Featured_v2" (Uncropped):** Generate an additional `Featured_v2` (3840x1440) variant. Do not crop the top. Instead, scale the entire 1920x1080 image to fit the 1440 height perfectly (resulting in 2560x1440), center it, and fill the remaining black space on the left and right margins by taking a large slice of the actual image's edge, mirroring it outwards (flip left/right), and heavily blurring it (e.g., `ImageFilter.GaussianBlur(radius=50)`) to create a seamless extended background.
3. **Generate Targets:**
   - **Base HD:** 1920x1080, optimized to < 3MB.
   - **BIG:** 3840x2160, optimized to < 2MB.
   - **social_media:** 1200x630, optimized to 200KB - 300KB.
   - **Featured:** 3840x1440, no size limit, high quality. (Use Original Crop Rule)
   - **Featured_v2:** 3840x1440, no size limit, high quality. (Use Uncropped Seamless Fill Rule)
   - **email:** 650x366, optimized to < 100KB.

## Phase 5: Organization & Cleanup
1. Create `Transcripts/` and `Thumbnails/` folders inside `Renders/Final/`.
2. Rename the transcript text file to `[Movie_Title]_TRANSCRIPT.txt`.
3. Rename all `.srt` files to `[Movie_Title]_[Language].srt`.
4. Prefix all generated thumbnails with `[Movie_Title]_`.
5. Move the text and SRT files into the `Transcripts/` folder.
6. Move the 6 generated thumbnails into the `Thumbnails/` folder.
