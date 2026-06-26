# TASK.md — Generic Mission Brief

## Mission

Build a **viral, physically expressive frontend prototype** using **Pretext** and **Three.js**.

The result should feel like a custom internet artifact, not a normal product page.

It must combine:

- typographic clarity
- reactive motion
- a memorable hero interaction
- controlled chaos
- production-minded structure

## Output target

Produce one of these:

1. a standalone HTML/CSS/JS prototype
2. a Vite + TypeScript prototype
3. a React + Three.js / R3F prototype

Default to **standalone** unless a framework is clearly useful.

## Required qualities

- readable at rest
- dramatic under interaction
- fast enough to feel instant
- visually coherent
- sharable in a short screen recording
- easy for another agent to continue

## Required feature mix

The prototype should include at least:

### 1. One signature hero

Examples:

- morphing wordmark
- glyph swarm
- text-built mascot or symbol
- spatial title wall
- cursor-reactive text organism

### 2. One controlled destruction or disruption mechanic

Examples:

- tearing text apart
- magnetic pull
- cursor blast
- burning or dissolving glyphs
- spring reconstruction
- breakout / breaker mechanic

### 3. One stable readable zone

Examples:

- info panel
- project list
- card stack
- caption rail
- editorial paragraph section

### 4. One secondary ambient system

Examples:

- side rails
- floating labels
- signal text
- slow cards in depth
- tunnel background
- variable typographic ASCII strip

## Default technical stack

- Pretext for measurement and line layout
- Three.js for spatial rendering and particles
- Canvas 2D if game-like destruction is needed
- plain JS or TypeScript
- no backend assumptions

## Optional ecosystem modes

Pick **one** if useful:

- **Textura mode** — DOM-free multi-block layout
- **Pinch-Type mode** — intentional mobile text scaling
- **Breaker mode** — text-as-brick gameplay
- **Dokobot mode** — obstacle-aware relayout playground
- **Editorial mode** — multi-column flow around masks or cards

## Rules

### Do

- measure text once, animate many times
- keep home positions for all glyph bodies
- use pooled particles
- build a clean calm state and an energetic active state
- keep the interaction local before making it global
- reduce density on mobile
- make one ecosystem pattern explicit in the code/comments

### Do not

- animate every text block constantly
- make the whole interface unreadable
- require camera or microphone permissions by default
- use heavy framework overhead for a tiny prototype
- duplicate the same words decoratively everywhere
- bolt on five demo ideas at once with no hierarchy

## Deliverables

- working code
- clear file structure
- comments only where useful
- no dead experimental branches left in place
- one obvious place to tune copy, colors, and forces

## Preferred structure

### Standalone

- `index.html`
- optional `styles.css`
- optional `app.js`

### Vite / TS

- `src/main.ts`
- `src/styles.css`
- `src/scene/*`
- `src/text/*`
- `src/game/*`

## Acceptance summary

The prototype is successful when:

- the hero is memorable within 3 seconds
- the interaction feels intentional, not random
- the text is readable when calm
- the motion feels premium, not messy
- another agent can extend it quickly
