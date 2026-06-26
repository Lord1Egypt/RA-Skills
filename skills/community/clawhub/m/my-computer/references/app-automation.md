# Application Automation Recipes

## Table of Contents
1. [Finder & File Manager](#finder--file-manager)
2. [Mail & Messaging](#mail--messaging)
3. [Browsers](#browsers)
4. [Media & Creative Apps](#media--creative-apps)
5. [Development Tools](#development-tools)
6. [Office & Productivity](#office--productivity)
7. [System Utilities](#system-utilities)

---

## Finder & File Manager

### macOS Finder

```bash
# Open folder in Finder
open /path/to/folder

# Reveal file in Finder
open -R /path/to/file.txt

# Open file with specific app
open -a "Visual Studio Code" /path/to/project

# Create smart folder search (saved search)
# Smart folders are just XML plist files:
cat > ~/Library/Saved\ Searches/LargeFiles.savedSearch << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>RawQuery</key>
    <string>kMDItemFSSize > 104857600</string>
    <key>SearchScopes</key>
    <array><string>kMDQueryScopeHome</string></array>
</dict>
</plist>
PLIST

# Set default app for file type (requires duti: brew install duti)
duti -s com.microsoft.VSCode .py all      # Open .py with VS Code
duti -s com.apple.Preview .pdf all         # Open .pdf with Preview

# Tag files (macOS color tags)
xattr -w com.apple.metadata:_kMDItemUserTags '("Red")' file.txt
# Multiple tags:
xattr -w com.apple.metadata:_kMDItemUserTags '("Red","Important")' file.txt
```

---

## Mail & Messaging

### macOS Mail.app

```bash
# Send email with attachment
osascript << 'EOF'
tell application "Mail"
    set newMsg to make new outgoing message with properties {
        subject:"Weekly Report",
        content:"Hi team,\n\nPlease find this week's report attached.\n\nBest regards"
    }
    tell newMsg
        set visible to true
        make new to recipient at end of to recipients with properties {address:"team@company.com"}
        make new cc recipient at end of cc recipients with properties {address:"manager@company.com"}
        make new attachment with properties {file name:POSIX file "/Users/me/Reports/weekly-2025-03.pdf"}
    end tell
    send newMsg
end tell
EOF

# Read unread emails
osascript -e '
tell application "Mail"
    set unreadMessages to (messages of inbox whose read status is false)
    set output to ""
    repeat with msg in unreadMessages
        set output to output & subject of msg & " | " & sender of msg & "\n"
    end repeat
    return output
end tell'

# Search for emails
osascript -e '
tell application "Mail"
    set foundMsgs to (messages of inbox whose subject contains "invoice")
    repeat with msg in foundMsgs
        log subject of msg & " from " & sender of msg
    end repeat
end tell'
```

### Slack (via webhook or CLI)

```bash
# Send via incoming webhook
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Task complete: organized 3,247 files into 24 folders"}' \
  "$SLACK_WEBHOOK_URL"

# Send file
curl -F file=@report.pdf -F channels=general \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  https://slack.com/api/files.upload
```

---

## Browsers

### Safari

```bash
# Open URL
osascript -e 'tell application "Safari" to open location "https://example.com"'

# Get current page URL
osascript -e 'tell application "Safari" to get URL of current tab of front window'

# Get current page title
osascript -e 'tell application "Safari" to get name of current tab of front window'

# Get page source
osascript -e 'tell application "Safari" to do JavaScript "document.body.innerText" in current tab of front window'

# Save page as PDF (via print)
osascript -e '
tell application "Safari"
    activate
end tell
delay 1
tell application "System Events"
    keystroke "p" using command down
    delay 1
    -- Click PDF dropdown, save as PDF
    keystroke "p" using {command down, shift down}
end tell'
```

### Chrome

```bash
# Open URL
open -a "Google Chrome" "https://example.com"

# Open in incognito
open -a "Google Chrome" --args --incognito "https://example.com"

# Chrome DevTools protocol (headless)
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless --dump-dom "https://example.com" 2>/dev/null

# Get page as PDF
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless --print-to-pdf="output.pdf" "https://example.com" 2>/dev/null
```

---

## Media & Creative Apps

### Preview (macOS)

```bash
# Open file
open -a Preview /path/to/image.jpg

# Convert image format via sips
sips -s format png input.jpg --out output.png
sips -s format jpeg input.png --out output.jpg -s formatOptions 80  # 80% quality

# Resize
sips -Z 1024 image.jpg          # Max 1024px (preserving aspect ratio)
sips -z 600 800 image.jpg       # Exact 600x800
sips --resampleWidth 500 image.jpg  # Width 500, auto height

# Batch resize all images in directory
sips -Z 1024 *.jpg

# Get image properties
sips -g pixelWidth -g pixelHeight -g format image.jpg

# Rotate
sips -r 90 image.jpg            # Rotate 90 degrees clockwise
sips -f horizontal image.jpg    # Flip horizontal
```

### ffmpeg (Media Processing)

```bash
# Video: extract audio
ffmpeg -i video.mp4 -vn -acodec libmp3lame audio.mp3

# Video: resize
ffmpeg -i input.mp4 -vf scale=1280:720 output.mp4

# Video: compress
ffmpeg -i input.mp4 -crf 28 -preset slow output.mp4

# Video: extract frames
ffmpeg -i video.mp4 -vf "fps=1" frame_%04d.png  # 1 frame/second

# Video: create GIF
ffmpeg -i video.mp4 -vf "fps=10,scale=320:-1" -loop 0 output.gif

# Audio: convert format
ffmpeg -i input.wav -acodec libmp3lame -b:a 192k output.mp3

# Batch convert (all .mov to .mp4)
for f in *.mov; do ffmpeg -i "$f" -c:v libx264 -crf 23 "${f%.mov}.mp4"; done

# Get media info
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4

# Hardware acceleration (macOS)
ffmpeg -i input.mp4 -c:v h264_videotoolbox -b:v 5M output.mp4
```

### ImageMagick

```bash
# Convert with quality
convert input.png -quality 85 output.jpg

# Resize and optimize
convert input.jpg -resize 50% -strip -quality 80 output.jpg

# Batch watermark
for f in *.jpg; do
  convert "$f" -gravity southeast -pointsize 24 \
    -fill "rgba(255,255,255,0.5)" -annotate +10+10 "© 2025" "watermarked_$f"
done

# Create thumbnail grid/contact sheet
montage *.jpg -geometry 200x200+5+5 -tile 5x contact_sheet.jpg

# PDF to images
convert -density 300 document.pdf page_%03d.png
```

---

## Development Tools

### VS Code

```bash
# Open file/folder
code /path/to/project
code /path/to/file.js

# Open file at specific line
code --goto /path/to/file.js:42

# Open diff
code --diff file1.js file2.js

# Install extension
code --install-extension ms-python.python

# List installed extensions
code --list-extensions
```

### Xcode (macOS)

```bash
# Build project
xcodebuild -project MyApp.xcodeproj -scheme MyApp -configuration Release build

# Build workspace (with CocoaPods/SPM)
xcodebuild -workspace MyApp.xcworkspace -scheme MyApp build

# Run tests
xcodebuild test -scheme MyApp -destination 'platform=macOS'

# Clean build
xcodebuild clean -project MyApp.xcodeproj

# Archive and export
xcodebuild archive -scheme MyApp -archivePath build/MyApp.xcarchive
xcodebuild -exportArchive -archivePath build/MyApp.xcarchive \
  -exportOptionsPlist ExportOptions.plist -exportPath build/

# Swift package
swift package init --type executable  # Create package
swift build                           # Build
swift run                             # Build and run
swift test                            # Run tests
```

### Git (advanced operations)

```bash
# Stats and analysis
git log --oneline --since="1 week ago"            # Recent commits
git shortlog -sn --all                             # Commits per author
git log --all --format='%H %aI' | wc -l           # Total commit count
git diff --stat HEAD~10                             # Changes in last 10 commits

# Repository maintenance
git gc --aggressive                                 # Optimize repo
git fsck                                            # Check integrity
git reflog expire --expire=now --all && git gc --prune=now  # Clean reflog
```

---

## Office & Productivity

### Preview / PDF operations (macOS)

```bash
# Merge PDFs (Python — built-in on macOS)
python3 << 'EOF'
import sys
from PyPDF2 import PdfMerger  # pip install PyPDF2
merger = PdfMerger()
for pdf in sorted(glob.glob("*.pdf")):
    merger.append(pdf)
merger.write("merged.pdf")
EOF

# Convert documents to PDF
textutil -convert pdf document.docx
textutil -convert pdf document.rtf

# OCR a scanned PDF (if tesseract installed)
# brew install tesseract
ocrmypdf scanned.pdf searchable.pdf
```

### Calendar (macOS)

```bash
# List today's events
osascript -e '
tell application "Calendar"
    set today to current date
    set todayStart to today - (time of today)
    set todayEnd to todayStart + (1 * days)
    set todayEvents to (every event of every calendar whose start date ≥ todayStart and start date < todayEnd)
    -- flatten and return
end tell'

# Create a calendar event
osascript -e '
tell application "Calendar"
    tell calendar "Work"
        set newEvent to make new event with properties {
            summary:"Meeting with Client",
            start date:date "March 20, 2025 at 2:00 PM",
            end date:date "March 20, 2025 at 3:00 PM",
            description:"Discuss Q2 plans"
        }
    end tell
end tell'
```

---

## System Utilities

### Screen Capture

```bash
# macOS screencapture
screencapture -x screenshot.png          # Full screen (silent)
screencapture -x -R 0,0,800,600 region.png  # Region
screencapture -x -w window.png           # Specific window (interactive)
screencapture -T 3 delayed.png           # 3-second delay

# Linux
import screenshot.png                     # Interactive (ImageMagick)
scrot screenshot.png                      # Full screen
scrot -s region.png                       # Select region
```

### Sound & Audio (macOS)

```bash
# Text to speech
say "Task complete. 3,247 files organized."
say -v Samantha "Hello" -o greeting.aiff  # Save to file

# Set volume
osascript -e 'set volume output volume 50'  # 0-100
osascript -e 'set volume output muted true'

# Play audio file
afplay /System/Library/Sounds/Glass.aiff
```

### Printing

```bash
# macOS
lp document.pdf                           # Print to default printer
lp -d "PrinterName" document.pdf          # Specific printer
lpstat -p -d                              # List printers
cupsctl                                   # CUPS config
```
