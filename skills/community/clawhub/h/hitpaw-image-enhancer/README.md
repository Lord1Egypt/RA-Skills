# HitPaw Image & Video Enhancer

[![ClawHub](https://img.shields.io/badge/ClawHub-hitpaw--image--enhancer-blue)](https://clawhub.com/skill/hitpaw-image-enhancer)
[![GitHub](https://img.shields.io/badge/GitHub-HitPaw--Official%2Fopenclaw--skill--hitpaw--enhancer-181717?logo=github)](https://github.com/HitPaw-Official/openclaw-skill-hitpaw-enhancer)
[![Version](https://img.shields.io/badge/version-1.0.3-green)](https://clawhub.com/skill/hitpaw-image-enhancer)

> OpenClaw skill integrating HitPaw's AI-powered image and video enhancement API

## 🎯 Features

This skill brings HitPaw's professional-grade AI enhancement capabilities to OpenClaw, supporting 16 specialized models for images and videos.

### Core Capabilities

- **Image Enhancement**: 2x/4x upscaling, face recovery, denoise, generative restoration
- **Video Enhancement**: Upscale to 4K, portrait restoration, temporal stability
- **Async Processing**: Polling-based job tracking with real-time status
- **Coin Tracking**: Monitor API consumption per job

## 📸 Screenshots

<!-- Actual screenshots from HitPaw official website -->

### Image Enhancement Examples

| Before | After |
|--------|-------|
| ![Before Enhancement](images/image-official-before.jpg) | ![After Enhancement](images/image-official-after.jpg) |

*Official HitPaw enhancement example (source: hitpaw.com)*

### Unblur / Sharpen Examples

| Before | After |
|--------|-------|
| ![Before Unblur](images/unblur-official-before.jpg) | ![After Unblur](images/unblur-official-after.jpg) |

*Official HitPaw unblur example (source: hitpaw.com)*

### Video Enhancement Examples

| Original Frame | Enhanced Frame |
|----------------|----------------|
| Placeholder: add video frame comparison | Placeholder: add video frame comparison |

> **Note**: Video example placeholders. Replace with actual screenshots from HitPaw video enhancement results.

---

## 🎯 Feature Highlights

Based on official [HitPaw API Documentation](https://developer.hitpaw.com/image/Introduction):

- **Quality**: Industry-defining quality fit for professional use cases
- **Fidelity**: Preserves original details and identities
- **Efficiency**: Optimized for low latency and high throughput

### Supported Models

**Image Models** (16 total):
- General Enhance (2x/4x)
- Portrait Models (Clear/Natural)
- High Fidelity (2x/4x)
- Denoise & Sharpen models
- Generative Portrait & General

**Video Models**:
- Ultra HD Restore
- General Restore
- Portrait Restore
- Face Soft
- Generative Video

See [SKILL.md](SKILL.md) for complete model documentation and usage examples.

## 🚀 Quick Start

### Installation

```bash
clawhub install hitpaw-image-enhancer
```

### Configuration

Set your HitPaw API key:

```bash
export HITPAW_API_KEY="your_api_key_here"
```

Get your API key at: https://playground.hitpaw.com/

### Usage

```bash
# Enhance an image
enhance-image -u photo.jpg -m general_2x -o output.jpg

# Enhance a video
enhance-video -u input.mp4 -m general_restore_2x -r 1920x1080 -o output.mp4
```

## 📚 Documentation

For comprehensive documentation, including all model options, configuration details, and troubleshooting, see [SKILL.md](SKILL.md).

## 🔗 Links

- **ClawHub Skill**: https://clawhub.com/skill/hitpaw-image-enhancer
- **GitHub Repository**: https://github.com/HitPaw-Official/openclaw-skill-hitpaw-enhancer
- **HitPaw API Docs**: https://developer.hitpaw.com/
- **HitPaw Playground**: https://playground.hitpaw.com/

## 📄 License

MIT © HitPaw-Official
