---
name: "mysteries-prep"
description: "Refined DaVinci API workflow: images are now imported strictly into a Media Pool bin first, and timeline injection requires explicit user confirmation to prevent errors in complex projects."
---

# Mysteries Prep Protocol

This skill automates the Farsight Mysteries preparation workflow, which includes transcription, target cross-examination, AI image generation, and DaVinci Resolve integration.

## Trigger
Use this skill when the user asks to run the "Mysteries Prep Protocol", prepare a Farsight target, or process an audio file for a Farsight project.

## Phase 1: Preliminary Questions
Before starting the workflow, the AI MUST ask the user the following questions in chat:
1. **Audio Location:** "Where is the audio file located?" (Needed to generate the transcript).
2. **Target Information Sheet:** "Where is the target information sheet for this project?" (The AI MUST read this sheet to understand the true nature of the target to properly bridge viewer descriptions).
3. **Image Density Mode:** "Are we doing this with 'full' or 'semi' image settings?"
   - **Full Mode:** Generate an image for *every single sentence/segment*.
   - **Semi Mode:** Generate an image every 1-2 minutes for the hardest-hitting sentence.
4. **Art Style:** "What art style should be applied to the generated images?" (This ensures aesthetic consistency across the media).
5. **DaVinci Resolve Readiness:** "Do you have the appropriate DaVinci Resolve project open right now?"

## Phase 2: Transcription & Directory Setup
1. **Extract/Obtain:** Get the `.wav` file of the raw video from the provided location.
2. **Transcribe:** Generate a word-for-word transcript from the `.wav` file. Make sure **each sentence/segment has a timestamp**. *(Note: Use local tools like `whisper-cpp` if available to ensure millisecond-accurate timestamps and bypass API auth errors.)*
3. **Create Image Directory:** Create a dedicated folder for the generated images in the exact same directory as the audio and transcript files.
   - The folder name must follow this format: `[Agent Name] [Relevant Words] ai images` (e.g., `raphael intysam solos 11 ai images`).

## Phase 3: Image Generation
- **Media Specs:** ALL generated images MUST be strictly **1080p HD (1920x1080) resolution**.
- **Media Format (Critical):** All generated images MUST be saved as `.jpg` files. If the generator outputs JPEGs with a `.png` extension, you MUST rename them to `.jpg` before importing to DaVinci Resolve to prevent "Media Offline" errors.
- **Filename Sanitization (Critical):** Ensure all generated image filenames contain NO spaces and NO parentheses (use underscores instead).
- **Safety Filter Bypass:** If prompts involving human forms or bodies are blocked by safety filters, tweak the phrasing to be abstract (e.g., "abstract glowing human silhouettes").
- **Cross-Examine the Target:** Use the target information sheet to understand the target truth.
- **Generate Prompts:** Craft image prompts that bridge the gap between the remote viewer's blind transcript descriptions and the actual target truth. **Integrate the user-specified Art Style** into every prompt.
- Generate the required images based on the chosen mode (Full/Semi) and save them to the AI images directory.

## Phase 4: DaVinci Resolve Integration
*(CRITICAL: Do NOT export standard XML or FCPXML. DaVinci's XML import is bugged and causes unresolvable "Media Offline" errors. You MUST use the DaVinci Resolve Python API exclusively for this phase.)*
- **DaVinci Resolve Studio Environment:** Ensure the Python script is executed externally with the correct environment variables for DaVinci Resolve Studio. Example:
  ```bash
  export RESOLVE_SCRIPT_API="/Applications/DaVinci Resolve Studio.app/Contents/Resources/Developer/Scripting"
  export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve Studio.app/Contents/Libraries/Fusion/fusionscript.so"
  export PYTHONPATH="$RESOLVE_SCRIPT_API/Modules/"
  python3 resolve_insert.py
  ```
- **Media Pool Subfolder & Import (Critical):** You MUST create an appropriately named subfolder in the DaVinci Media Pool (e.g., `mediaPool.AddSubFolder(root_folder, "Raphael AI Gens")`), set it as the current folder (`mediaPool.SetCurrentFolder(target_folder)`), and explicitly import the `.jpg` files into it. 
- **Wait for User Confirmation:** After importing into the bin, the script must STOP. The AI must explicitly ask the user: *"The images have been imported into the bin. Would you like me to inject the clips into the timeline on a new video layer?"*
- **Timeline Injection (Upon Approval Only):** If the user confirms, run a second script to append the clips to the active timeline. Map the imported media items from the bin by base name for the timeline placement step.
- **Timeline Start Offset (Critical):** Resolve timelines often start at `01:00:00:00` (e.g., frame 107892). You MUST retrieve the timeline start offset using `start_offset = timeline.GetStartFrame()` and add it to your frame calculations (`record_frame = int(start_offset + (timestamp_sec * fps))`). Otherwise, clips will vanish into the negative space before the timeline starts (the "phantom zone").
- **Add Video Track:** Add a new video track to the top of the currently open DaVinci Resolve timeline (`timeline.AddTrack("video")`).
- **Base Zoom (API Step):** All images MUST be inserted with a **1.02 baseline zoom** on the X and Y axis via the Resolve API (`item.SetProperty("ZoomX", 1.02)`) to prevent edge-bleeding during dynamic zoom.
- **Placement (FULL Mode):** Place each image at the exact offset-adjusted timestamp indicated by the transcript. Each image MUST last the exact length of the sentence. No gaps, **NO cross dissolves**.
- **Placement (SEMI Mode):** Place each image at the exact offset-adjusted timestamp indicated by the transcript. (Due to DaVinci API limitations, still images default to exactly 5 seconds upon placement).

## Phase 5: Verbal Reminders for Manual UI Steps
Because the DaVinci Resolve Python API cannot apply transitions or effects, the AI MUST verbally remind the user in the chat to do the following:
- **If Full Mode:** "Please select all the newly placed images and toggle 'Dynamic Zoom' ON in the Inspector panel. (Remember, no cross dissolves are used in Full Mode!)"
- **If Semi Mode:** "Please note that the images are 5 seconds long by default due to API limits, so you may need to manually extend them to match the pacing. Select all the newly placed images, press `Cmd+T` (Mac) or `Ctrl+T` (Windows) to add instant cross dissolves, and toggle 'Dynamic Zoom' ON in the Inspector panel."

---
*Original Protocol Architects: Fuchikoma & Daemon King*
*Updated by: Raphael (Split DaVinci integration into separate bin-import and timeline-injection phases requiring user confirmation)*
