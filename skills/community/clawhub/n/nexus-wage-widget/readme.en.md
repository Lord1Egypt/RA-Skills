# Daily Wage Dashboard Pro

A single-file HTML+CSS+JS desktop widget that combines real-time wage calculation with a Pomodoro focus timer, featuring a glassmorphism design, 7 visual themes, and responsive layout.

## Features

### Real-time Wage Calculation
- Automatically calculates today's earned amount based on monthly salary, work hours, and standard working days (21.75 days/month)
- Refreshes every second with precise, up-to-the-minute cumulative earnings
- Progress bar showing completion ratio of today's work hours
- Payday countdown

### Pomodoro Focus Timer
- 25-minute countdown timer with start/pause controls
- Desktop notification + title bar flashing alert when time is up
- Independent layouts for wide and square modes

### 7 Visual Themes
| Theme Key | Name | Style |
|-----------|------|-------|
| dark | Geek Night | Dark purple gradient, default |
| hermes | Hermes Orange | Warm orange-gold, luxury |
| business | Black Gold | Black and gold, sophisticated |
| girly | Girly Pink | Pink tones, soft and vibrant |
| zen | Zen Forest | Blue-green zen, refreshing |
| light | Minimal White | Light background, clean |
| cyber | Cyber Neon | Fluorescent colors, futuristic |

### Responsive Layout
- **Wide mode** (>900px): 3-column x 2-row grid, max-width 740px
- **Square mode** (<=900px): Single column flex, max-width 340px, suitable for small screens or floating widgets

### Glassmorphism Design
- Rounded glass cards with customizable opacity and blur
- Multi-layer box-shadow simulating ambient light and highlight
- Pseudo-element top edge highlight
- Panel hover animations (lift, border glow, deeper shadow)
- Ambient light particles (3 ambient-light elements) with slow breathing animation

### Settings Panel
- Click the gear button to open the modal
- Configurable: layout mode, visual theme, monthly salary, payday, work hours, glass opacity, glass blur
- Theme changes preview instantly
- All settings persisted via localStorage (key prefix `widget_`)

## File Structure

```
nexus-wage-widget/
  references/
    daily_wage.html    # Core widget file (single-file HTML+CSS+JS)
  SKILL.md             # Skill description (complete restoration guide)
  LICENSE.txt          # MIT License
  readme.md            # Chinese readme
  readme.en.md         # This file (English readme)
```

## Usage

1. Open `references/daily_wage.html` in a browser
2. Defaults to Geek Night theme, auto-starts the timer
3. Click the "Focus" panel to start the Pomodoro timer
4. Click the gear button (bottom-right) to open settings

### Configuration Parameters
| Parameter | Description | Default |
|-----------|-------------|---------|
| Display Mode | Wide / Square layout | Wide |
| Theme | 7 options | Geek Night |
| Monthly Salary | Pre-tax salary (CNY) | 10000 |
| Payday | Day of month | 10 |
| Work Start | Format HH:MM | 09:00 |
| Work End | Format HH:MM | 18:00 |
| Glass Opacity | 0.1 ~ 0.9 | 0.4 |
| Glass Blur | 4px ~ 40px | 24px |

## Visual Guidelines

- Chinese font: Noto Sans SC (served via fonts.loli.net CDN)
- Monospace: Source Code Pro
- All font-size values must be even px numbers
- Glass card border-radius: 28px, panel border-radius: 20px
- Progress bar height: 6px, border-radius: 3px

## Technical Notes

- Pure frontend, no external dependencies (except Google Fonts China mirror CDN)
- Storage: localStorage
- Real-time updates: requestAnimationFrame loop
- Pomodoro state machine: IIFE closure pattern (no class/this)
- Respects `prefers-reduced-motion: reduce` accessibility setting

## License

MIT License - see LICENSE.txt for details.

Copyright (c) 2026 Neway Lau