# GT7 Tuning Knowledge Base

> Last updated: 2026-03-20 via Perplexity research
> Covers patches up to 1.66 (December 2025)

## Patch Changes Affecting Tuning

### Update 1.55 (January 2025)
- **Suspension model reworked**: reduced sudden damping limits ("grinding out") over bumps
- **Tire physics**: load dependency adjustments during cornering, reduced grip loss on wet racing lines, faster grip recovery after going off-track
- **LSD defaults changed** for some road cars
- **Force feedback** calculations improved for wheels and gamepads
- **PP updates** for some cars, aero tweaks for Gr.1 and race cars
- **Flywheel inertia** tweaks: Hyundai N2025 Vision GT GR1, Aston Martin Valkyrie

### Update 1.66 (December 2025)
- **Downshift exploit patched**: blocks manual downshift at extremely high RPMs — no more rapid shuffling for extra deceleration/rotation
- Forces disciplined braking and timing
- Paddle shifters still work but need adapted technique

## Current Tuning Meta (Post-1.66)

### Suspension
- **Spring rates**: softer than pre-1.55 — reduced bump sensitivity means less need for stiff springs
- **Damper ratios**: tune to exploit reduced bump "grind" — can be more aggressive than real-world
- **Anti-roll bars**: soften post-patch to avoid oversteer
- **Body height**: lower = better aero, but bottoming risk on bumpy tracks

### Tires
- Load dependency during cornering is exaggerated vs real life → recovers faster
- Aggressive camber/toe works better than conservative real-world setups
- Wet: reduced grip loss on racing lines, faster recovery from dirty tires
- Soft compounds benefit more on damp tracks post-1.55

### LSD (Limited Slip Differential)
- **Initial torque**: tune LOWER post-update (prevents over-rotation with refined suspension/tire load)
- **Acceleration sensitivity**: HIGHER for better corner exit traction
- **Braking sensitivity**: 10-20% for stability
- Focus on throttle modulation over shift exploits (downshift trick patched)

### Transmission
- Downshift exploit gone → prioritize trail braking
- Gear ratios: optimize for PP, not just lap time
- Top speed vs acceleration balance depends on track character

### Aerodynamics
- PP dominance: BoP shifts frequently → optimize PP first
- Default aero changed for Gr.1 and race cars
- Real-world aero scaling ≠ GT7 aero scaling

## GT7-Specific Physics Quirks (NOT like real racing)

1. **Tire load sensitivity** is exaggerated — aggressive setups work
2. **Suspension is more forgiving** — stiffer springs/dampers don't bottom as easily as IRL
3. **Downshift braking patched** — no more high-RPM shift abuse
4. **TCS/ABS integration** — the game assumes you use assists, tune LSD conservatively if you don't
5. **PP optimization > absolute performance** — BoP changes frequently
6. **Camber/toe more aggressive** than real-world optimal
7. **ARBs need to be softer** post-patch to prevent oversteer

## Tuning Workflow

### For Circuit Racing (Nürburgring, Spa, etc.)
1. Start with GT Pro Tune baseline
2. Soften ARBs 1-2 clicks from calculated
3. Lower LSD initial torque
4. Raise acceleration LSD
5. Set braking LSD to 10-20%
6. Test and iterate in-game

### For Top Speed / Highway
1. Minimize downforce
2. Maximize gear ratios for top speed
3. Stiffer suspension for stability at speed
4. Higher tire pressure for less rolling resistance

### For Drift
1. Rear bias weight distribution
2. High LSD initial + acceleration
3. Low LSD braking
4. Soft rear springs, stiff front
5. Maximum steering angle
