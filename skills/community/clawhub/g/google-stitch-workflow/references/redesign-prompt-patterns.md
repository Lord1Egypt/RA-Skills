# Redesign Prompt Patterns

Use these patterns when a Stitch session needs tighter prompt structure than
the base skill alone provides.

## Generate-first exploration

Use when the direction is still open:

```text
Create a mobile screen for <feature>.
Use a <style direction> visual language.
Focus on <1-2 primary goals>.
Use a <structural pattern> composition rather than a generic centered hero/card stack.
Do not invent metrics, testimonials, logos, prices, or social proof.
Do not build the whole app. Generate one canonical screen only.
```

## Preservation-first edit

Use when a real screen already exists and must stay recognizable:

```text
<screen>. Mobile.
Keep <required elements>.
Improve only <layout / spacing / hierarchy / polish>.
Do not remove <critical elements>.
Do not add fake browser/device/app chrome or new proof claims.
```

## Reference-driven redesign

Use when imported or named references define current structure:

```text
Use the uploaded real app references in this project.
The relevant images are named <reference-1>, <reference-2>, and <reference-3>.
Those images show what exists now.
Keep the real structure and improve only hierarchy, spacing, and polish.
Do not invent new sections.
Extract design logic from the references; do not copy proprietary brand details,
logos, exact copy, or pixel structure.
```

## Visual cleanup pass

Use after the structure is already accepted:

```text
Keep the current structure and content.
Improve only spacing, typography hierarchy, button emphasis, and alignment.
Do not add new sections or change the screen flow.
Remove decorative visuals or fake chrome that do not clarify the workflow.
```

## Anti-generic redesign pass

Use when the result looks generated, bland, or too close to a template:

```text
Redesign this screen while preserving its content and primary task.
Change the structural rhythm first: avoid centered hero plus repeated cards.
Use a more specific composition: <index-first / stat-led / workbench / catalogue / dense task surface>.
Keep all real copy and actions. Do not invent proof, metrics, logos, or testimonials.
Make the first viewport feel like one deliberate composition.
```

## Prompt discipline

- prefer one screen and one major intent per prompt
- preserve explicitly; do not assume unchanged elements will stay unchanged
- use plain language over abstract creative language
- choose structure before style
- avoid invented proof and fake chrome
- review the result visually before the next major change
