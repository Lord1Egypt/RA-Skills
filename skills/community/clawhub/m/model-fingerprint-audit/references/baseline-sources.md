# Trusted reference sources

A behavioral fingerprint is trusted only when collected from a direct provider endpoint or a provider whose routing and model identity are documented.

| Claimed model | Candidate reference source | Expected model ID | Access note |
|---|---|---|---|
| Kimi K3 | https://api.moonshot.ai/v1 or NVIDIA NIM `https://integrate.api.nvidia.com/v1` | `kimi-k3` or provider-qualified K3 ID | Provider API key required |
| GLM-5.3 Flash | Z.ai / a documented GLM provider | `glm-5.3-flash` | Provider API key required |
| GLM-5.2 | Z.ai / a documented GLM provider | `glm-5.2` | Provider API key required |
| Qwen3.8-Max | Alibaba Cloud Model Studio / Qwen Cloud | `qwen3.8-max` | Provider API key required |

## Baseline collection

1. Confirm the provider's model ID using its authenticated `/models` endpoint or official documentation.
2. Run the same fixed probe set used for the target proxy, with 16 repetitions and bounded concurrency.
3. Store only normalized probe outputs, response metadata, and the provider/model/version label. Never store API keys.
4. Keep the baseline endpoint and collection date beside the fingerprint file.
5. Compare the proxy against this baseline with the same API format and sampling parameters.

A provider model catalog or a response `model` field is not itself a fingerprint. If no direct reference key is available, report `无法判断`.