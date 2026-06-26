# GLM / Zhipu Protocol Rules

## Default probe order
1. OpenAI-compatible endpoints first:
   - `GET /models`
   - `POST /responses`
   - `POST /chat/completions`
2. If vendor documentation or response headers clearly indicate native Zhipu/GLM behavior, add vendor-native probes.

## Notes
- Many GLM routes are exposed through OpenAI-compatible gateways.
- Treat route labels like `glm-4`, `glm-5` as claimed model IDs, not proof of native provenance.
- Focus on stability, schema coherence, and catalog composition.
