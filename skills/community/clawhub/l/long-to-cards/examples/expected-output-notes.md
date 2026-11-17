Expected output:

- Starts with a source diagnosis before writing cards.
- Selects one narrative structure for the card package.
- Outputs card-by-card title, copy, microcopy, visual direction, and source anchor.
- Adds cover title, first-line hook, body caption, image order, CTA, alt text guidance, source caveats, and follow-up ideas.
- Separates stable topic tags from `verified_hot_tags` and leaves hot tags unverified without a current source and check time.
- Records `delivery_mode`, `platform_profile`, and `asset_url_policy`.
- In the default `publish_ready` mode, produces a complete handoff to `cards-to-images` and does not stop at card copy.
- Stops after copy only when the user explicitly selects `copy_only`.
- Marks claims needing verification instead of presenting them as publish-ready facts.
- Does not claim uploadable images exist until real files and a checked `cards-manifest` return.
