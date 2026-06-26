# Workflow Confirmation

The current image runtime executes a single generation step after routing.

Clarification is required before execution when:

- the prompt implies reference continuity or transformation
- no usable image input was supplied

This seam stays intentionally thin so future multi-step image workflows can add confirmation without changing the public CLI contract.
