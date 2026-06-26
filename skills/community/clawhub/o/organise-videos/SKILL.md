---
name: organise-videos
description: Organize a video folder by cleaning non-video files, removing short/bad videos, and classifying videos into numbered subfolders using AI vision analysis.
---

# Video Folder Organizer

Intelligently organize a video folder: clean up non-video files, remove bad footage, analyze content with AI, and sort into categorized subfolders.

## Usage

User wants to organize a video folder: $ARGUMENTS

If the user has not provided a folder path, ask them to provide one.

**Language note**: Detect the language the user is writing in and respond in that language throughout the entire session. Category folder names should also be in the user's language.

---

## Step 1: Scan the Folder

Scan the folder for all files (non-recursive at root level first):

```bash
# List all files with sizes
ls -la "$FOLDER"

# Find video files (common extensions)
find "$FOLDER" -maxdepth 1 -type f \( \
  -iname "*.mp4" -o -iname "*.mov" -o -iname "*.avi" -o -iname "*.mkv" \
  -o -iname "*.m4v" -o -iname "*.wmv" -o -iname "*.flv" -o -iname "*.webm" \
  -o -iname "*.mts" -o -iname "*.m2ts" -o -iname "*.mpg" -o -iname "*.mpeg" \
  -o -iname "*.3gp" -o -iname "*.hevc" -o -iname "*.ts" \
\)

# Find non-video files
find "$FOLDER" -maxdepth 1 -type f ! \( \
  -iname "*.mp4" -o -iname "*.mov" -o -iname "*.avi" -o -iname "*.mkv" \
  -o -iname "*.m4v" -o -iname "*.wmv" -o -iname "*.flv" -o -iname "*.webm" \
  -o -iname "*.mts" -o -iname "*.m2ts" -o -iname "*.mpg" -o -iname "*.mpeg" \
  -o -iname "*.3gp" -o -iname "*.hevc" -o -iname "*.ts" \
\)
```

Report to user:
- Total files found
- Number of video files
- Number of non-video files (list them)

---

## Step 2: Handle Non-Video Files

**Use AskUserQuestion** to ask what to do with non-video files (only if any exist):

Question: "Found N non-video file(s). How would you like to handle them?"
Options:
- "Move to _misc subfolder (Recommended)" — move non-video files into `$FOLDER/_misc/`
- "Delete all non-video files" — permanently delete them
- "Leave them as-is" — do nothing

If user chooses to move:
```bash
mkdir -p "$FOLDER/_misc"
mv [non-video files] "$FOLDER/_misc/"
```

If user chooses to delete:
```bash
rm [non-video files]
```

---

## Step 3: Remove Short Videos

**Use AskUserQuestion** to ask about short video threshold:

Question: "Would you like to remove very short videos?"
Options:
- "Yes, remove videos shorter than 1 second (default)"
- "Yes, let me specify a duration"
- "No, keep all videos"

If user wants to specify duration, ask them to type the threshold in seconds.

Use `ffprobe` to check each video's duration:

```bash
ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$VIDEO_FILE"
```

List all videos shorter than the threshold, show their filenames and durations, then confirm deletion:

```bash
rm "$SHORT_VIDEO"
```

---

## Step 4: Extract Frames and Analyze Videos with AI Vision

For each remaining video file, extract representative frames using ffmpeg:

```bash
# Create temp directory for frames
mkdir -p /tmp/video_frames

# Extract 4 evenly-spaced frames from each video
# (at 10%, 30%, 60%, 90% of duration)
DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$VIDEO")
ffmpeg -ss $(echo "$DURATION * 0.10" | bc) -i "$VIDEO" -frames:v 1 /tmp/video_frames/"${BASENAME}_01.jpg" -y -loglevel quiet
ffmpeg -ss $(echo "$DURATION * 0.30" | bc) -i "$VIDEO" -frames:v 1 /tmp/video_frames/"${BASENAME}_02.jpg" -y -loglevel quiet
ffmpeg -ss $(echo "$DURATION * 0.60" | bc) -i "$VIDEO" -frames:v 1 /tmp/video_frames/"${BASENAME}_03.jpg" -y -loglevel quiet
ffmpeg -ss $(echo "$DURATION * 0.90" | bc) -i "$VIDEO" -frames:v 1 /tmp/video_frames/"${BASENAME}_04.jpg" -y -loglevel quiet
```

Also detect bad footage quality:

```bash
# Check for all-black frames: compute mean brightness of frame
ffmpeg -i "$VIDEO" -ss $(echo "$DURATION * 0.5" | bc) -frames:v 1 -vf "blackdetect=d=0.1:pix_th=0.10" -f null - 2>&1

# Check for excessive shakiness using scene detection / motion vectors
ffmpeg -i "$VIDEO" -vf "select='gt(scene,0.4)',setpts=N/TB" -frames:v 5 /tmp/video_frames/"${BASENAME}_shake_%02d.jpg" -y -loglevel quiet 2>&1
```

**Use the Read tool to load the extracted frame images**, then analyze ALL videos together in one AI analysis pass:

Analyze each video's frames and produce for each video:
1. **Category**: A short label in the user's language describing the content (e.g., highway driving, city street, nature scenery, indoor footage, interview, sports, aerial, food, live event)
2. **Quality issues**:
   - `all_black`: frames are mostly black (>80% black pixels)
   - `shaky`: excessive camera movement/shake visible
   - `blurry`: extremely out of focus
   - `none`: no issues

After analyzing all videos, present a summary table to the user:
```
Filename            Duration  Category         Quality
video001.mp4        00:32     highway driving  none
video002.mp4        01:15     city street      shaky
video003.mp4        00:08     nature scenery   all black
...
```

---

## Step 5: Handle Bad Quality Videos

If any videos were flagged with quality issues (all_black, shaky, blurry):

**Use AskUserQuestion**:

Question: "The following videos have quality issues: [list filenames and issue types]. How would you like to handle them?"
Options:
- "Delete all problematic videos"
- "Move to _rejected subfolder"
- "Keep them, do nothing"
- "Decide one by one"

If "Decide one by one", for each bad video use AskUserQuestion with options: Delete / Move to _rejected / Keep

Execute the chosen action for each video.

---

## Step 6: Classify Videos into Numbered Subfolders

Based on the AI analysis categories, propose a folder structure:

1. Collect all unique categories from the analysis
2. Sort categories by number of videos (most videos first)
3. Assign two-digit numbers: `01_`, `02_`, etc.

Show the proposed structure to the user (folder names in the user's language):
```
Proposed folder structure:
01_highway_driving  (12 videos)
02_city_street      (8 videos)
03_nature_scenery   (5 videos)
04_indoor           (3 videos)
```

**Use AskUserQuestion**:

Question: "Does the proposed folder structure look good?"
Options:
- "Looks good, proceed"
- "I need to rename some categories"
- "I need to merge some categories"

If user wants adjustments, ask them to specify changes (use Other input), then update the plan.

Execute the file moves:
```bash
mkdir -p "$FOLDER/01_highway_driving"
mv "$VIDEO" "$FOLDER/01_highway_driving/"
```

After moving all files, confirm completion and show the final structure:
```bash
find "$FOLDER" -type d | sort
```

---

## Step 7: Refine a Category (Optional)

**Use AskUserQuestion**:

Question: "Would you like to further organize any category folder?"
Options:
- "No, all done"
- "Yes, let me choose a category"

If user wants to refine, ask which category folder they want to work on (list the created folders as options).

Then ask:

Question: "How would you like to organize this folder?"
Options:
- "Group by time of day (morning / afternoon / evening)"
- "Group by quality (picks / normal)"
- "Group by length (short / long)"
- "Let me describe how"

Execute the requested sub-organization using the same AI analysis data already collected, or re-analyze if needed.

After completing, loop back to Step 7 to ask if any other category needs refinement.

---

## Technical Notes

### Prerequisites
- `ffmpeg` and `ffprobe` must be installed (`brew install ffmpeg`)
- Use `which ffmpeg` to verify before starting

### Performance Tips
- Process frames extraction in batches to avoid overwhelming the system
- For large folders (>50 videos), inform the user this may take a few minutes
- Clean up temp frames after analysis: `rm -rf /tmp/video_frames`

### Error Handling
- If a video file is corrupted and ffprobe fails, mark it as "unreadable" and ask user separately
- If ffmpeg frame extraction fails, skip that video's frames and note in analysis

### Folder Safety
- Never delete files without explicit user confirmation
- Always show what will be deleted/moved before executing
- If unsure, prefer moving to a subfolder over permanent deletion
