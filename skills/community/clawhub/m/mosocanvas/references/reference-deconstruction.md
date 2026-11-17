# Reference Deconstruction

Load this file when the task uses one or more reference images, asks to reproduce a visual
mechanism, or requires authorized reconstruction.

## Choose the reference mode

1. `mechanism-transfer`: create new content using selected mechanisms.
2. `owned-reconstruction`: reproduce an authorized design with measurable fidelity.
3. `restricted-imitation`: translate a request involving protected identity, signature, or a
   living artist into non-identifying mechanisms.

State the mode. Do not blur inspiration, reconstruction, and copying.

## Separate measurement from interpretation

Record two layers:

- **Measured or directly observed:** dimensions, aspect ratio, palette samples and area, luminance
  distribution, edge density, spatial divisions, text regions, repeated marks, and visible light
  direction.
- **Interpreted:** hierarchy, tension, nostalgia, intimacy, cultural association, narrative
  distance, and likely function.

Never present an interpretation as a sampled fact. Include confidence and at least one alternative
interpretation for strong contextual claims.

## Deconstruct in functional order

1. **Carrier and viewing condition:** size, crop, distance, material, and thumbnail behavior.
2. **Composition:** dominant masses, focal region, horizon or axes, negative space, depth layers,
   cropping, and subject-to-frame relationship.
3. **Hierarchy:** first read, second read, discovery layer, and competing elements.
4. **Color:** palette roles, coverage, luminance contrast, saturation contrast, temperature
   distribution, and accent budget.
5. **Light:** source direction, hardness, falloff, affected surfaces, and narrative function.
6. **Line and texture:** edge behavior, grain scale, mark density, regularity, and material cues.
7. **Typography:** copy role, type category, width, weight, spacing, alignment, and integration with
   the image.
8. **Narrative distance:** staged versus observed, calm versus alert, explicit versus withheld.

Do not force every category into the final design. Select at most three decisive mechanisms.

## Map mechanisms into execution

For every selected mechanism record:

```yaml
observation: <what is visible or measured>
function_in_reference: <what it appears to do>
transfer_to_task: <how it changes in the new brief>
execution_constraint: <what the generator or layout tool must do>
failure_signs: [<surface imitation>, <overuse>, <lost function>]
verification: <observable comparison>
confidence: low|medium|high
```

Examples:

- Do not map “blue and pink” directly. Map a cold dominant field, a small warm alert accent, and
  the exact surfaces the accent light affects.
- Do not map “minimal composition” directly. Map the dominant mass ratio, protected negative
  space, and the information reserved for that space.
- Do not map “film grain” directly. Map grain scale, uniformity, edge interaction, and whether it
  masks or supports material detail.

## Combine multiple references

- Identify shared mechanisms before differences.
- Give each reference a role; do not average all references.
- Reject a reference whose decisive mechanism conflicts with the confirmed proposition or carrier.
- Keep provenance and `do_not_copy` items for every source.

## Validate the result

Check separately:

1. proposition and task fit;
2. selected mechanism retention;
3. surface-only imitation risk;
4. copied subject, composition, mark, or signature risk;
5. new technical defects introduced by the transfer.

For authorized reconstruction, compare geometry, text, color, and assets with deterministic tools.
For mechanism transfer, do not optimize toward exact pixel similarity.
