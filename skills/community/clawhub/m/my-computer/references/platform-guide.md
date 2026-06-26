# Platform-Specific Guide

## Table of Contents
1. [macOS](#macos)
2. [Linux](#linux)
3. [Windows](#windows)

---

## macOS

### File System Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `mdfind` | Spotlight search (fast, indexed) | `mdfind "kind:image date:today" -onlyin ~/Desktop` |
| `mdls` | Read Spotlight metadata | `mdls -name kMDItemContentType file.jpg` |
| `xattr` | Extended attributes | `xattr -l file.pdf` (check quarantine, etc.) |
| `ditto` | Smart copy (preserves metadata, resources) | `ditto src/ dst/` |
| `textutil` | Document conversion | `textutil -convert html doc.docx` |
| `sips` | Image manipulation | `sips -Z 1024 photo.jpg` (resize max dimension) |
| `qlmanage` | Quick Look from CLI | `qlmanage -p file.pdf` |
| `hdiutil` | Disk image management | `hdiutil create -volname "App" -srcfolder dist/ -ov app.dmg` |
| `diskutil` | Disk management | `diskutil list` |
| `tmutil` | Time Machine | `tmutil listbackups` |

### Spotlight Metadata Attributes (for `mdfind` and `mdls`)

```bash
# Common search predicates
mdfind "kMDItemContentType == 'com.adobe.pdf'"           # PDFs
mdfind "kMDItemPixelHeight > 2000"                        # High-res images
mdfind "kMDItemContentCreationDate > $time.today(-7)"    # Created last 7 days
mdfind "kMDItemFSSize > 100000000"                        # Files > 100MB
mdfind "kMDItemAuthors == 'John'"                         # By author
mdfind "kMDItemMusicalGenre == 'Jazz'"                    # Music by genre
mdfind "kMDItemDurationSeconds > 3600"                    # Videos > 1 hour

# Useful metadata keys
# kMDItemContentType        - UTI type (com.adobe.pdf, public.jpeg, etc.)
# kMDItemContentCreationDate - When content was created
# kMDItemFSCreationDate     - When file was created on disk
# kMDItemPixelWidth/Height  - Image dimensions
# kMDItemAcquisitionModel   - Camera model (photos)
# kMDItemLatitude/Longitude - GPS coordinates (photos)
# kMDItemDurationSeconds    - Audio/video duration
# kMDItemNumberOfPages      - PDF page count
# kMDItemTitle              - Document title
# kMDItemAuthors            - Document authors
```

### AppleScript / JXA Patterns

**Control Finder:**
```bash
# Get selected files in Finder
osascript -e 'tell application "Finder" to get POSIX path of (selection as alias list)'

# Set Finder view to column view
osascript -e 'tell application "Finder" to set current view of front window to column view'

# Get info about a file
osascript -e 'tell application "Finder" to get {name, size, modification date} of (POSIX file "/path/to/file" as alias)'

# Create alias/shortcut
osascript -e 'tell application "Finder" to make new alias file at desktop to POSIX file "/path/to/original"'
```

**Control System:**
```bash
# Set volume
osascript -e 'set volume output volume 50'

# Get/set display brightness (approximate)
osascript -e 'tell application "System Events" to tell process "SystemUIServer" to get value of slider 1 of group 1 of window "Control Center"'

# Show notification
osascript -e 'display notification "Done!" with title "My Computer" sound name "Glass"'

# Show dialog with choices
osascript -e 'choose from list {"Option A", "Option B", "Option C"} with prompt "Select one:"'

# Open System Preferences to a specific pane
osascript -e 'tell application "System Preferences" to reveal pane id "com.apple.preference.security"'
```

**JXA (JavaScript for Automation) — for complex logic:**
```bash
osascript -l JavaScript -e '
  const fm = $.NSFileManager.defaultManager;
  const contents = fm.contentsOfDirectoryAtPathError($("/Users/me/Desktop"), null);
  const arr = [];
  for (let i = 0; i < contents.count; i++) arr.push(contents.objectAtIndex(i).js);
  JSON.stringify(arr);
'
```

### macOS Shortcuts CLI

```bash
# List all shortcuts
shortcuts list

# Run a shortcut with file input
shortcuts run "My Shortcut" --input-path /path/to/input.txt

# Run and capture output
shortcuts run "Process Data" --input-path data.csv --output-path result.txt

# Useful built-in shortcuts (vary by system):
# - "Make PDF" — convert files to PDF
# - "Resize Image" — resize images
# - "Get Current Weather" — weather data
# - "Encode Media" — media conversion
```

### Homebrew Essentials for Automation

```bash
# Tools that significantly enhance automation capabilities
brew install exiftool     # Rich EXIF/metadata for photos
brew install ffmpeg       # Media conversion/processing
brew install imagemagick  # Image manipulation
brew install pandoc       # Document format conversion
brew install jq           # JSON processing
brew install ripgrep      # Fast content search
brew install fd           # Fast file finder
brew install tree         # Directory visualization
brew install trash        # Safe delete to Trash
brew install duti         # Set default applications
brew install pdfgrep      # Search inside PDFs
```

---

## Linux

### File System Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `locate` / `plocate` | Fast indexed search | `locate "*.pdf"` (run `updatedb` first) |
| `file` | Detect file type | `file document.unknown` |
| `stat` | File details | `stat --format="%s %y %n" file.txt` |
| `rsync` | Smart sync/copy | `rsync -avh --progress src/ dst/` |
| `rename` | Perl-based rename | `rename 's/\.jpeg$/.jpg/' *.jpeg` |
| `inotifywait` | Watch for file changes | `inotifywait -m -r ~/Downloads` |

### Desktop Automation

```bash
# Window management with wmctrl
wmctrl -l                           # List windows
wmctrl -a "Firefox"                 # Activate window by title
wmctrl -r "Terminal" -e 0,0,0,800,600  # Resize/move

# Simulate input with xdotool
xdotool key ctrl+c                  # Send keystroke
xdotool type "hello world"         # Type text
xdotool mousemove 100 200 click 1  # Click at coordinates

# Desktop notifications
notify-send -t 5000 "Task Complete" "Files organized successfully"

# Clipboard
echo "text" | xclip -selection clipboard  # Copy
xclip -selection clipboard -o             # Paste
```

### Systemd Timers (modern alternative to cron)

```bash
# Create service: ~/.config/systemd/user/cleanup.service
cat > ~/.config/systemd/user/cleanup.service << 'EOF'
[Unit]
Description=Daily Downloads Cleanup

[Service]
Type=oneshot
ExecStart=/home/user/scripts/cleanup.sh
EOF

# Create timer: ~/.config/systemd/user/cleanup.timer
cat > ~/.config/systemd/user/cleanup.timer << 'EOF'
[Unit]
Description=Run cleanup daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Enable
systemctl --user daemon-reload
systemctl --user enable --now cleanup.timer
systemctl --user list-timers  # Verify
```

---

## Windows

### PowerShell Automation (when not using WSL)

```powershell
# File organization
Get-ChildItem -Path ~/Downloads -Recurse | Group-Object Extension | Sort-Object Count -Descending

# Bulk rename
Get-ChildItem *.jpg | Rename-Item -NewName { $_.Name -replace 'IMG_','photo_' }

# Disk usage
Get-ChildItem -Path C:\ -Recurse -ErrorAction SilentlyContinue |
  Sort-Object Length -Descending | Select-Object -First 20 FullName, @{N='Size(MB)';E={[math]::Round($_.Length/1MB,2)}}

# Task Scheduler
schtasks /create /tn "DailyCleanup" /tr "powershell.exe -File C:\scripts\cleanup.ps1" /sc daily /st 09:00

# Open files/apps
Start-Process "notepad.exe" "file.txt"
Invoke-Item "document.pdf"  # Open with default app
```

### WSL Integration

```bash
# Access Windows files from WSL
ls /mnt/c/Users/username/Documents/

# Run Windows programs from WSL
explorer.exe .                    # Open current dir in Explorer
cmd.exe /c "dir C:\\Users"       # Run Windows command
powershell.exe -c "Get-Process"  # Run PowerShell

# Clipboard
echo "text" | clip.exe           # Copy to Windows clipboard
powershell.exe -c "Get-Clipboard"  # Read from clipboard
```
