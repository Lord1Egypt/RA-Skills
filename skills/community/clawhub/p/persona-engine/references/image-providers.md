# Image Providers Guide

The AI Persona Engine supports two image providers for visual identity and selfie generation.

| Provider | Style | Reference Image Support | Restrictions | API Key |
|----------|-------|------------------------|--------------|---------|
| Gemini | Photorealistic | Yes (image-to-image) | Standard | Required (Google) |
| Grok Imagine | Creative | No | Fewer restrictions | Required (xAI) |

You can use one or both. When both are configured, Gemini is the default and Grok Imagine is used for creative or unrestricted content.

---

## Gemini

Best for photorealistic personas. Supports reference image input for facial consistency across generations.

### Setup

1. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com)
2. Run the wizard or configure manually:

```bash
openclaw persona update --image-provider gemini
```

### Config Example

```json
{
  "persona": {
    "image": {
      "provider": "gemini",
      "referenceImage": "~/.openclaw/workspace/persona-reference.png",
      "canonicalLook": {
        "description": "Warm caramel skin, jet black hair, angular face, high cheekbones, full lips",
        "style": "photorealistic",
        "alwaysInclude": "gold hoop earrings, gold chain necklace"
      },
      "gemini": {
        "model": "gemini-2.0-flash-preview-image-generation"
      }
    }
  }
}
```

### How Reference Images Work

When the wizard generates a reference image you approve, it gets saved as `persona-reference.png` in your workspace. This image is then used as input for all future image generations, so the agent's face stays consistent across selfies, avatars, and reactions.

- Gemini's image-to-image pipeline uses the reference to maintain facial features
- The `canonicalLook.description` provides text guidance alongside the image
- `canonicalLook.alwaysInclude` specifies accessories or features that must appear in every generation

### Generating the Reference Image

During `persona create`:
```
Step 4/7: Visual Identity
  Describe your agent's appearance:
  > Warm caramel skin, jet black sleek hair, angular modelesque face...

  Generate a reference image now? (y/n): > y
  Saved to ~/.openclaw/workspace/persona-reference.png
  Does this look right? (y/n): > y
  Locked as canonical reference image.
```

To regenerate later:
```bash
openclaw persona update --regen-image
```

---

## Grok Imagine

xAI's image generation. More creative freedom and fewer content restrictions than Gemini.

### Setup

1. Get an xAI API key at [console.x.ai](https://console.x.ai)
2. Run the wizard or configure manually:

```bash
openclaw persona update --image-provider grok
```

### Config Example

```json
{
  "persona": {
    "image": {
      "provider": "grok",
      "canonicalLook": {
        "description": "Warm caramel skin, jet black hair, angular face",
        "style": "photorealistic",
        "alwaysInclude": "gold hoop earrings"
      },
      "grok": {
        "model": "grok-imagine-image"
      }
    }
  }
}
```

### When to Use Grok Imagine

- Creative or artistic image styles
- Content that falls outside Gemini's safety filters
- As a fallback when Gemini refuses a generation

---

## Using Both Providers

Configure both and set a default. The agent will use the default for standard generations and fall back or switch to the other when appropriate.

```json
{
  "persona": {
    "image": {
      "provider": "gemini",
      "gemini": {
        "model": "gemini-2.0-flash-preview-image-generation"
      },
      "grok": {
        "model": "grok-imagine-image"
      }
    }
  }
}
```

During wizard setup, choose option `[3] Both` when prompted:
```
Choose an image provider:
  [1] Gemini (photorealistic, reference image support)
  [2] Grok Imagine (creative, fewer restrictions)
  [3] Both (Gemini default, Grok for creative)
  [4] None (no visual identity)
```

---

## Canonical Look

The `canonicalLook` object defines what your agent looks like. It is used in every image generation prompt.

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Physical appearance description (freeform) |
| `style` | string | Art style: `photorealistic`, `anime`, `illustration`, `3d-render` |
| `alwaysInclude` | string | Accessories or features to include in every image |

---

## Spontaneous Images

The agent can send selfies unprompted when trigger words appear in conversation.

```json
{
  "persona": {
    "image": {
      "spontaneous": {
        "enabled": true,
        "triggers": ["selfie", "show me", "what do you look like", "pic"]
      }
    }
  }
}
```

The agent generates mood-appropriate expressions based on the conversation context. For example, a "good morning" selfie will show a warm, sleepy expression, while a celebration prompt will show excitement.

The `agent-selfie` skill is automatically installed during persona creation to handle ongoing selfie generation.
