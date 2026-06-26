---
name: moodle-claw
description: Interact with Moodle LMS to browse courses, access learning materials, and answer questions about course content.
license: GPL-3.0
metadata: 
  author: Romain M.
  version: "1.0"
  homepage: https://github.com/4strium/moodle-claw
  repository: https://github.com/4strium/moodle-claw
---

# Moodle-Claw Skill

This skill allows you to interact with a Moodle learning management system (LMS) to help users with their courses, assignments, and learning materials.

## Setup
If `moodle-claw` binary is missing, download it:

URL="https://github.com/4strium/moodle-claw/releases/download/v1.0/moodle-claw"
SHA256="0ce9e6ad4e42c626ebe2c4ce79bde23da3386dc8e4b54a87da0a345a1a0252aa"

curl -L -o moodle-claw "$URL"
echo "$SHA256 moodle-claw" | sha256sum -c -
chmod +x moodle-claw

## Configuration

Before using moodle-claw commands, the user needs to configure their Moodle connection:

```bash
moodle-claw configure
```

This will interactively prompt for:
1. **Moodle server URL** - e.g., `https://moodle.university.edu`
2. **Authentication method** - Token (direct), SSO (redirect URL), or Username/Password
3. **Download path** - Where to save downloaded files

### Authentication Methods

#### Option 1: Direct Token
If you already have a 32-character hex token:
```bash
moodle-claw configure --url https://moodle.example.com --token YOUR_32_CHAR_TOKEN --path ~/Documents/Moodle
```

#### Option 2: SSO Authentication (recommended for universities)
For institutions using SSO (Single Sign-On):

1. **Log into your Moodle account** in a web browser
2. **Open the developer console** (press F12) and go to the **Network** tab
3. **Visit this URL** in the same browser tab (replace with your Moodle URL):
   ```
   https://YOUR_MOODLE_URL/admin/tool/mobile/launch.php?service=moodle_mobile_app&passport=12345&urlscheme=moodlemobile
   ```
4. **The page will fail to load** - this is expected! An error will occur.
5. **In the Network tab**, find the failed request (it should be red/failed)
6. **Right-click** on the failed request > **Copy** > **Copy link address**
   - The URL looks like: `moodlemobile://token=BASE64_ENCODED_STRING`
7. **Use the copied URL**:
   ```bash
   moodle-claw configure --url https://moodle.example.com --sso-url "moodlemobile://token=..." --path ~/Documents/Moodle
   ```

Or use interactive mode and select "SSO (redirect URL)":
```bash
moodle-claw configure
```

#### Option 3: Username/Password
For institutions allowing direct login:
```bash
moodle-claw configure --url https://moodle.example.com --username your_user --password your_pass --path ~/Documents/Moodle
```

## Available Commands

### Check Status
```bash
moodle-claw status [--output json]
```
Shows current configuration and connection status.

### List Courses
```bash
moodle-claw courses [--filter "math"] [--refresh] [--output json]
```
Lists all enrolled courses. Use `--refresh` to fetch latest from server.

### View Course Content
```bash
moodle-claw content "Course Name" [--section "TD2"] [--output json]
moodle-claw content 12345  # by course ID
```
Shows the structure of a course (sections, modules, files).

### Search Content
```bash
moodle-claw search "exercise" [--course "Physics"] [--type file] [--output json]
```
Searches for content across courses.

### Download Files
```bash
moodle-claw get "Course/Section/file.pdf" [--course "Math"] [--dest /tmp]
moodle-claw get --url "https://moodle.../pluginfile.php/..." [--dest /tmp]

# Extract text from PDF files (recommended for reading content)
moodle-claw get "file.pdf" --text --output json
```
Downloads a file and returns its local path. Use `--text` (`-t`) to automatically extract text content from PDF files.

### Sync Course
```bash
moodle-claw sync "Course Name" [--dest ~/Courses] [--no-confirm]
moodle-claw sync  # syncs all enabled courses
```
Downloads all files from a course.

## Usage Patterns

### When user asks about a course
1. First, list courses to find the right one: `moodle-claw courses --filter "keyword"`
2. Then get its content: `moodle-claw content "Course Name"`
3. If needed, download specific files: `moodle-claw get "path/to/file.pdf"`

### When user asks about specific content (e.g., "TD2", "exercise 3")
1. Search for the content: `moodle-claw search "TD2" --course "Course Name"`
2. Download and extract text from PDF: `moodle-claw get "path/to/file.pdf" --text`
3. The extracted text will be included in the output for you to analyze

### When user wants to work offline
1. Sync the entire course: `moodle-claw sync "Course Name" --no-confirm`
2. Files will be available locally for reading

## Output Formats

All commands support `--output json` for structured output, or the default markdown format for human readability.

## Example Interactions

**User**: "Explique-moi le cours de mécanique"
```bash
# 1. Find the course
moodle-claw courses --filter "mécanique" --output json

# 2. Get course structure
moodle-claw content "Mécanique" --output json

# 3. Download relevant materials and explain
moodle-claw get "Mécanique/Chapitre 1/cours.pdf" --output json
```

**User**: "Quel est l'exercice 3 du TD2 en maths?"
```bash
# 1. Search for TD2 in math course
moodle-claw search "TD2" --course "maths" --output json

# 2. Download the TD2 file and extract text
moodle-claw get "TD2.pdf" --course "maths" --text --output json

# The text content will be in the JSON output for you to analyze
```

**User**: "Télécharge tous les fichiers du cours de physique"
```bash
moodle-claw sync "Physique" --no-confirm
```

## Notes

- Files are cached locally after first download
- Use `--refresh` on `moodle-claw courses` to update the course list from server
- Course names support fuzzy matching (partial names work)
- The `--output json` flag is useful for parsing structured data
- Use `--text` with `moodle-claw get` to extract text from PDF files directly

## Security / Vetting

- Source code fully open-source
- SHA256 checksum verified before execution
- Token, credentials and configuration saved locally on this machine
