# Recolor Execution Guardrails

Current runtime does **not** use different recolor strategies for silk, wool, denim, knit, or other fabric categories.

## Rules

### 1. Do Not Branch by Material
- Do not generate separate execution strategies for satin, knit, wool, linen, leather, or similar fabric labels.
- Use the same recolor workflow regardless of garment material.

### 2. Confirm Color, Not Fabric Logic
- If the user cares about "premium" or "realistic" output, confirm the target color and the requested garment parts.
- Do not promise fabric-specific highlight preservation or weave-aware saturation control unless the runtime actually supports it.

### 3. Warn on Extreme Dark-to-Light Changes
- Black-to-white or very dark-to-very-light recolors can still look less natural because source shadows remain image-dependent.
- In these cases, warn the user and offer a softer alternative such as off-white, oat, or light gray.
