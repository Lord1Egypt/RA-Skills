# CLI Master - Project Specification

## Overview
- **Project name:** CLI Master
- **Type:** Gamified educational web app (single-page application)
- **Core functionality:** Duolingo-style Linux CLI learning platform with lessons, exercises, XP, achievements, and progress tracking
- **Target users:** Beginners wanting to learn Linux command line

## Tech Stack
- Vanilla HTML, CSS, JavaScript (no frameworks)
- Vite for development (optional, plain JS works too)
- GitHub Pages for hosting
- LocalStorage for data persistence
- GitHub Gist for leaderboard (future)

## UI/UX Specification

### Visual Design
- **Theme:** Dark terminal-inspired with modern gamification accents
- **Color Palette:**
  - Background: `#0d1117` (deep dark)
  - Surface: `#161b22` (card backgrounds)
  - Primary: `#58a6ff` (interactive elements, links)
  - Accent XP: `#ffd700` (gold for XP/streaks)
  - Success: `#3fb950` (correct answers)
  - Error: `#f85149` (wrong answers)
  - Text Primary: `#e6edf3`
  - Text Secondary: `#8b949e`
- **Typography:**
  - Headings: "JetBrains Mono", monospace (terminal feel)
  - Body: "Inter", system-ui, sans-serif
  - Code/CLI: "JetBrains Mono", monospace
- **Spacing:** 8px base unit (8, 16, 24, 32, 48)
- **Border radius:** 8px for cards, 4px for buttons
- **Animations:** Smooth transitions (200ms), XP pop animations, progress bar fills

### Layout Structure
- **Header:** Logo, XP counter, streak flame, settings gear
- **Sidebar (collapsible on mobile):** Unit navigation, progress indicators
- **Main Content:** Lesson cards, exercise areas
- **Footer:** Minimal, version info

### Responsive Breakpoints
- Mobile: < 768px (single column, bottom nav)
- Tablet: 768px - 1024px (sidebar collapses)
- Desktop: > 1024px (full sidebar + content)

### Components

#### Progress Bar
- Shows lesson completion within unit
- Animated fill with glow effect
- Percentage label

#### XP Display
- Current XP with animated counter
- Level badge with progress ring
- Streak counter with flame icon

#### Lesson Card
- Unit icon + title
- Progress indicator (lessons completed/total)
- Lock icon for locked units
- Hover: slight lift + glow

#### Exercise Types
1. **Multiple Choice** - 4 options, single correct
2. **Fill in the Blank** - Type the command
3. **Terminal Simulation** - Execute pseudo-commands, see output
4. **Drag & Drop** - Reorder command parts
5. **True/False** - Statement about command behavior

#### Achievement Toast
- Slides in from top-right
- Icon + title + XP reward
- Auto-dismiss after 3s
- Confetti for major achievements

#### Leaderboard (Gist-based - future)
- GitHub-authenticated users can submit scores
- Weekly/Monthly/All-time tabs
- Top 10 display

## Data Structure

### Units
```json
{
  "id": "file-management",
  "title": "File Management",
  "icon": "📁",
  "description": "Learn to navigate and manipulate files",
  "lessons": [
    {
      "id": "ls-basics",
      "title": "Listing Files",
      "exercises": [...]
    }
  ],
  "requiredXp": 0
}
```

### User Data (LocalStorage)
```json
{
  "xp": 150,
  "level": 2,
  "streak": 5,
  "lastActive": "2026-04-06",
  "completedLessons": ["ls-basics", "cd-basics"],
  "unitProgress": {
    "file-management": 40
  },
  "achievements": ["first-command", "streak-3"],
  "settings": {
    "soundEnabled": true,
    "animationsEnabled": true
  }
}
```

### Achievements
- `first-command` - Complete first exercise (50 XP)
- `streak-3` - 3-day streak (100 XP)
- `streak-7` - 7-day streak (250 XP)
- `unit-complete` - Complete a unit (200 XP)
- `perfect-lesson` - All exercises correct first try (100 XP)
- `ten-lessons` - Complete 10 lessons (150 XP)
- `explorer` - Try 5 different exercise types (100 XP)

## Units & Lessons Structure

### Unit 1: Getting Started (Free, unlocked)
- Lesson 1: What is the Terminal?
- Lesson 2: Your First Command (echo)
- Lesson 3: Clearing the Screen (clear)

### Unit 2: File Navigation
- Lesson 1: Listing Files (ls)
- Lesson 2: Current Directory (pwd)
- Lesson 3: Changing Directory (cd)
- Lesson 4: Absolute vs Relative Paths

### Unit 3: File Management
- Lesson 1: Creating Files (touch)
- Lesson 2: Creating Directories (mkdir)
- Lesson 3: Copying Files (cp)
- Lesson 4: Moving Files (mv)
- Lesson 5: Removing Files (rm)
- Lesson 6: Removing Directories (rmdir)

### Unit 4: Working with Files
- Lesson 1: Viewing File Content (cat)
- Lesson 2: Head and Tail
- Lesson 3: Word Count (wc)
- Lesson 4: Searching in Files (grep basics)

### Unit 5: Permissions (Advanced)
- Lesson 1: Understanding Permissions (ls -l)
- Lesson 2: Changing Permissions (chmod)
- Lesson 3: Changing Ownership (chown)

### Unit 6: Networking
- Lesson 1: Checking Connectivity (ping)
- Lesson 2: Download Files (curl/wget)
- Lesson 3: SSH Basics

## Functionality

### Core Features
1. **Lesson Browser** - Browse units, see progress, select lessons
2. **Lesson Player** - Step through exercises, get immediate feedback
3. **XP System** - Earn XP for completions, bonuses for streaks/perfect scores
4. **Level System** - Level up every 500 XP (levels 1-50)
5. **Achievement System** - Unlock badges, earn bonus XP
6. **Progress Tracking** - Track completed lessons, unit progress
7. **Streak System** - Daily login bonus, streak tracking
8. **Settings** - Reset progress, toggle sounds/animations

### User Flow
1. Land on home → See dashboard with progress overview
2. Select unit → View lessons in unit with progress
3. Start lesson → Work through exercises
4. Complete lesson → See summary, earn XP, check achievements
5. Return home → See updated progress, streak maintained

### Exercise Logic
- 5 exercises per lesson
- Must get 3+ correct to pass
- Can retry exercises
- XP: 10 per correct, 5 bonus for perfect lesson

## GitHub Pages Deployment
- Build output in `/docs` folder
- Set Pages source to "gh-pages" branch or `/docs folder
- Custom domain support (future)

## Acceptance Criteria
1. [x] Single HTML file works without build step
2. [] Unit 1: Getting Started with lessons load correctly
3. [] Unit 2: File Navigation with lessons load correctly
4. [] Unit 3: File Management with lessons load correctly
5. [] Unit 4: Working with Files with lessons load correctly
6. [] Unit 5: Permissions with lessons load correctly
7. [] Unit 6: Networking with lessons load correctly
8. [] At least 3 exercise types implemented
9. [] XP/level/streak system works
10. [] Achievements unlock and display toasts
11. [] Progress persists in LocalStorage
12. [] Settings allow reset and toggles
13. [] Responsive on mobile/tablet/desktop
14. [] Nice UI that's not intimidating
15. [] Deployed on GitHub Pages