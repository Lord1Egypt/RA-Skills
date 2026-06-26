# Ranking Rubric

Score each candidate on four axes from 1 to 5.

## 1. Utility

Ask:

- Does it solve a repeated workflow?
- Is the trigger easy to understand?
- Will a normal user benefit quickly after install?

Prefer concrete helpers over vague "AI platform" wrappers.

## 2. Popularity

Use current visible signals:

- ClawHub installs
- ClawHub stars
- GitHub stars
- version count when relevant

Use ClawHub popularity as the primary signal for actual skill adoption.

## 3. Maintenance

Check:

- recent repository activity
- current version freshness
- issue hygiene when visible
- coherent docs and examples
- credible upstream source that matches the marketplace claim

Low maintenance can outweigh high popularity.

If no credible upstream GitHub source can be found, downgrade confidence unless the skill is extremely simple and low-risk.

## 4. Safety And Friction

Penalize:

- suspicious flags
- unclear runtime dependencies
- undeclared network or binary requirements
- weak install or usage instructions
- broad dangerous filesystem behavior
- hard-coded paths, sandbox assumptions, or environment-specific workflow constraints

## Recommendation bands

- `yes`: strong utility, acceptable safety, active enough to try now
- `maybe`: useful but has setup, safety, or maintenance caveats
- `no`: low signal, suspicious, stale, or not meaningfully practical
