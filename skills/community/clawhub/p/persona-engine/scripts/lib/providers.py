"""
Provider abstraction layer for voice and image services.
Handles config generation for ElevenLabs, Grok TTS, built-in TTS,
Gemini image generation, and Grok Imagine.
"""

import json


# --- Voice Providers ---

def get_voice_provider_config(provider, **kwargs):
    """Generate voice provider configuration for openclaw.json."""
    builders = {
        "elevenlabs": _build_elevenlabs_config,
        "grok": _build_grok_tts_config,
        "builtin": _build_builtin_tts_config,
        "none": lambda **kw: None,
    }
    builder = builders.get(provider)
    if not builder:
        raise ValueError(f"Unknown voice provider: {provider}")
    return builder(**kwargs)


def _build_elevenlabs_config(voice_id="", model_id="eleven_v3",
                             stability=0.5, similarity_boost=0.75,
                             style=0.0, **_kwargs):
    return {
        "provider": "elevenlabs",
        "elevenlabs": {
            "voiceId": voice_id,
            "modelId": model_id,
            "voiceSettings": {
                "stability": stability,
                "similarityBoost": similarity_boost,
                "style": style,
            },
        },
    }


def _build_grok_tts_config(model_id="grok-3-tts", **_kwargs):
    return {
        "provider": "grok",
        "grok": {
            "modelId": model_id,
        },
    }


def _build_builtin_tts_config(voice="nova", **_kwargs):
    return {
        "provider": "builtin",
        "builtin": {
            "voice": voice,
        },
    }


VOICE_PRESETS = {
    "default": {"stability": 0.5, "similarityBoost": 0.75, "style": 0.0},
    "intimate": {"stability": 0.2, "similarityBoost": 0.85, "style": 0.3},
    "excited": {"stability": 0.3, "similarityBoost": 0.8, "style": 0.5},
    "professional": {"stability": 0.7, "similarityBoost": 0.7, "style": 0.0},
}


# --- Image Providers ---

def get_image_provider_config(provider, **kwargs):
    """Generate image provider configuration for openclaw.json."""
    builders = {
        "gemini": _build_gemini_config,
        "grok": _build_grok_imagine_config,
        "both": _build_both_image_config,
        "none": lambda **kw: None,
    }
    builder = builders.get(provider)
    if not builder:
        raise ValueError(f"Unknown image provider: {provider}")
    return builder(**kwargs)


def _build_gemini_config(model="gemini-2.0-flash-preview-image-generation",
                         description="", style="photorealistic",
                         always_include="", reference_image="", **_kwargs):
    config = {
        "provider": "gemini",
        "gemini": {"model": model},
        "canonicalLook": {
            "description": description,
            "style": style,
            "alwaysInclude": always_include,
        },
    }
    if reference_image:
        config["referenceImage"] = reference_image
    return config


def _build_grok_imagine_config(model="grok-imagine-image",
                                description="", style="photorealistic",
                                always_include="", reference_image="",
                                **_kwargs):
    config = {
        "provider": "grok",
        "grok": {"model": model},
        "canonicalLook": {
            "description": description,
            "style": style,
            "alwaysInclude": always_include,
        },
    }
    if reference_image:
        config["referenceImage"] = reference_image
    return config


def _build_both_image_config(**kwargs):
    config = _build_gemini_config(**kwargs)
    config["grok"] = {"model": kwargs.get("grok_model", "grok-imagine-image")}
    return config


# --- Spontaneous Behavior ---

def get_spontaneous_config(voice_enabled=True, image_enabled=True,
                           voice_triggers=None, image_triggers=None):
    """Generate spontaneous behavior configuration."""
    config = {}
    if voice_enabled:
        config["voice"] = {
            "enabled": True,
            "triggers": voice_triggers or [
                "goodnight", "good morning", "story", "tell me"
            ],
        }
    if image_enabled:
        config["image"] = {
            "enabled": True,
            "triggers": image_triggers or [
                "selfie", "show me", "what do you look like", "pic"
            ],
        }
    return config
