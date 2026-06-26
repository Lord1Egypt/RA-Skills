<div align="center">
  <img src="https://assets.modelslab.com/generations/08645a0f-83a8-4842-88fd-a5cf44c5fbd8.png" alt="ModelsLab Banner" width="100%">
</div>

<div align="center">
  <a href="https://discord.gg/ujtGyjY2">
    <img src="https://img.shields.io/badge/Discord-Join%20Us-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord">
  </a>
  <a href="https://x.com/ModelsLabAI">
    <img src="https://img.shields.io/badge/X-@ModelsLabAI-000000?style=for-the-badge&logo=twitter&logoColor=white" alt="X/Twitter">
  </a>
  <a href="https://github.com/ModelsLab">
    <img src="https://img.shields.io/badge/GitHub-ModelsLab-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
  </a>
</div>

# ModelsLab Agent Skills

Official agent skills for [ModelsLab](https://modelslab.com) - the comprehensive AI API platform for image generation, video creation, audio synthesis, 3D modeling, and more.

## Quick Start

```bash
# Install all ModelsLab skills
npx skills add modelslab/skills --all

# Install specific skills
npx skills add modelslab/skills --skill modelslab-image-generation

# List available skills
npx skills add modelslab/skills --list
```

## Available Skills

### Generation Skills

| Skill | Description | Use Cases |
|-------|-------------|-----------|
| 🎨 [**Image Generation**](image-generation/SKILL.md)<br/>`modelslab-image-generation` | Generate high-quality AI images from text prompts or transform existing images. Access 10,000+ models including FLUX, Realtime, and Community models. | Product photos, marketing graphics, concept art, social media content |
| 🎬 [**Video Generation**](video-generation/SKILL.md)<br/>`modelslab-video-generation` | Generate videos from text descriptions or animate static images using AI video generation models like CogVideoX. | Product demos, social media videos, animations, visual storytelling |
| 🎵 [**Audio Generation**](audio-generation/SKILL.md)<br/>`modelslab-audio-generation` | Generate speech, music, sound effects, and more using AI audio synthesis with voice cloning. | Audiobooks, podcasts, voice assistants, game audio, music production |
| ✂️ [**Image Editing**](image-editing/SKILL.md)<br/>`modelslab-image-editing` | Professional AI-powered image editing tools for background removal, upscaling, and more. | E-commerce photos, real estate, social media, photo restoration |
| 🎲 [**3D Generation**](3d-generation/SKILL.md)<br/>`modelslab-3d-generation` | Generate 3D models from text descriptions or convert 2D images to 3D. | Game assets, product prototypes, 3D printing, AR/VR content |
| 🎭 [**Deepfake & Face Swap**](deepfake/SKILL.md)<br/>`modelslab-deepfake` | High-quality face swapping in images and videos using advanced AI. | Entertainment content, personalized videos, character variations |
| 🏠 [**Interior Design**](interior-design/SKILL.md)<br/>`modelslab-interior-design` | AI-powered interior design, room decoration, and space transformation. | Virtual staging, renovation planning, real estate, design mockups |

### Agent Control Plane Skills

| Skill | Description | Use Cases |
|-------|-------------|-----------|
| 🔑 [**Account Management**](account-management/SKILL.md)<br/>`modelslab-account-management` | Signup, login, email verification, token refresh, profile updates, API key CRUD, and team management via the Agent Control Plane API. Supports full headless agent flow. | Agent bootstrapping, headless signup, API key rotation, team onboarding |
| 💳 [**Billing & Subscriptions**](billing-subscriptions/SKILL.md)<br/>`modelslab-billing-subscriptions` | Manage billing, wallet balance, payment methods, subscriptions, invoices, and coupons programmatically. Includes headless card tokenization and direct subscriptions. | Auto-recharge wallets, headless billing, subscription lifecycle, wallet ledger |
| 🔍 [**Model Discovery**](model-discovery/SKILL.md)<br/>`modelslab-model-discovery` | Search and discover 50,000+ AI models, check usage analytics, and monitor generation history. | Model selection, usage monitoring, cost tracking |

### Platform Skills

| Skill | Description | Use Cases |
|-------|-------------|-----------|
| 🔔 [**Webhooks**](webhooks/SKILL.md)<br/>`modelslab-webhooks` | Handle async operations efficiently with real-time webhook notifications. | Batch processing, background jobs, scalable applications |
| 📦 [**SDK Usage**](sdk-usage/SKILL.md)<br/>`modelslab-sdk-usage` | Official SDKs for easier integration with type safety (Python, TypeScript, PHP, Go, Dart). | Type safety, autocomplete, better error handling, cleaner code |

## Installation

```bash
# Install all skills
npx skills add modelslab/skills --all

# Install specific skills
npx skills add modelslab/skills --skill modelslab-image-generation --skill modelslab-video-generation

# Install to specific agents
npx skills add modelslab/skills --all -a claude-code -a cursor
```

## Getting Started

1. **Get API Key**: Sign up at [modelslab.com](https://modelslab.com) and get your API key from the [dashboard](https://modelslab.com/dashboard)

2. **Install Skills**: `npx skills add modelslab/skills --all`

3. **Start Using**: Your coding agent now has access to all ModelsLab capabilities!

**Example prompts**:
- "Generate an image of a sunset over mountains"
- "Create a video showing a spaceship flying through space"
- "Convert this text to speech with a professional voice"
- "Remove the background from this product photo"
- "Sign up for a ModelsLab account and create an API key"
- "Search for the best Flux image models on ModelsLab"
- "Check my ModelsLab wallet balance and fund it if low"

## Resources

- **Documentation**: https://docs.modelslab.com
- **Dashboard**: https://modelslab.com/dashboard
- **Model Library**: https://modelslab.com/models (10,000+ models)
- **Discord**: https://discord.gg/modelslab
- **Support**: support@modelslab.com

## Contributing

Want to add a skill or improve existing ones? PRs welcome!

## License

MIT

---

Built with ❤️ by the ModelsLab team
