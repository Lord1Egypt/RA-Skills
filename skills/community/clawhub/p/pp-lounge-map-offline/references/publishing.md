# Offline Publishing Notes

This bundle is the marketplace-facing offline variant.

Before publishing:

1. Run `npm run build:offline-skill`.
2. Run `npm run validate:publish:offline`.
3. Run `npm run skill:validate:offline`.
4. Run `npm run skill:export:offline`.
5. Review the staged bundle in `out/pp-lounge-map-offline-skill/`.

Publish the offline bundle separately from the online skill so users can choose between local-only and remote-connected workflows.
