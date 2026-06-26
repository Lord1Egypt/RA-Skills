"""
Wizard prompt definitions for persona-create.sh interactive wizard.
Defines the structure, choices, and defaults for each wizard step.
"""

STEPS = [
    {
        "id": "identity",
        "title": "Step 1/7: Name & Identity",
        "prompts": [
            {"key": "name", "prompt": "What's your agent's name?", "required": True},
            {"key": "emoji", "prompt": "Pick an emoji:", "required": True},
            {"key": "creature", "prompt": 'Short description (e.g., "executive assistant"):', "required": True},
            {"key": "nickname", "prompt": "Nickname (optional):", "required": False, "default": ""},
        ],
    },
    {
        "id": "personality",
        "title": "Step 2/7: Personality",
        "prompts": [
            {
                "key": "archetype",
                "prompt": "Choose a starting archetype:",
                "type": "choice",
                "choices": [
                    {"value": "professional", "label": "Professional — competent, direct, business-focused"},
                    {"value": "companion", "label": "Companion — warm, personal, emotionally intelligent"},
                    {"value": "creative", "label": "Creative — imaginative, playful, artistic"},
                    {"value": "mentor", "label": "Mentor — wise, patient, educational"},
                    {"value": "custom", "label": "Custom — start from scratch"},
                ],
                "required": True,
            },
            {"key": "brevity", "prompt": "Brevity level (1=verbose, 5=terse):", "default": "3", "type": "int", "min": 1, "max": 5},
            {"key": "humor", "prompt": "Use humor? (y/n):", "type": "bool", "default": "y"},
            {"key": "swearing", "prompt": "Swearing allowed? (never/rare/when-it-lands/frequent):", "default": "never",
             "type": "choice_inline", "choices": ["never", "rare", "when-it-lands", "frequent"]},
            {"key": "ban_openers", "prompt": 'Ban corporate openers like "Great question!"? (y/n):', "type": "bool", "default": "y"},
            {"key": "pet_names", "prompt": "Affectionate (pet names, emotional depth)? (y/n):", "type": "bool", "default": "n"},
            {"key": "flirtation", "prompt": "Flirtatious? (y/n):", "type": "bool", "default": "n"},
            {"key": "protective", "prompt": "Protective (pushback on bad ideas)? (y/n):", "type": "bool", "default": "y"},
        ],
    },
    {
        "id": "voice",
        "title": "Step 3/7: Voice",
        "prompts": [
            {
                "key": "voice_provider",
                "prompt": "Choose a voice provider:",
                "type": "choice",
                "choices": [
                    {"value": "elevenlabs", "label": "ElevenLabs (best quality, custom voices, cloning)"},
                    {"value": "grok", "label": "Grok TTS (xAI, integrated with Grok models)"},
                    {"value": "builtin", "label": "Built-in OpenClaw TTS (no API key needed)"},
                    {"value": "none", "label": "None (text only)"},
                ],
                "required": True,
            },
        ],
    },
    {
        "id": "image",
        "title": "Step 4/7: Visual Identity",
        "prompts": [
            {
                "key": "image_provider",
                "prompt": "Choose an image provider:",
                "type": "choice",
                "choices": [
                    {"value": "gemini", "label": "Gemini (photorealistic, reference image support)"},
                    {"value": "grok", "label": "Grok Imagine (creative, fewer restrictions)"},
                    {"value": "both", "label": "Both (Gemini default, Grok for creative)"},
                    {"value": "none", "label": "None (no visual identity)"},
                ],
                "required": True,
            },
            {"key": "appearance", "prompt": "Describe your agent's appearance:", "required": False, "default": ""},
        ],
    },
    {
        "id": "user",
        "title": "Step 5/7: Your Context (USER.md)",
        "prompts": [
            {"key": "user_name", "prompt": "Your name:", "required": True},
            {"key": "call_names", "prompt": "What should the agent call you?", "required": True},
            {"key": "pronouns", "prompt": "Your pronouns (optional):", "required": False, "default": ""},
            {"key": "timezone", "prompt": "Your timezone:", "default": "UTC"},
            {"key": "user_notes", "prompt": "Anything else they should know?", "required": False, "default": ""},
        ],
    },
    {
        "id": "memory",
        "title": "Step 6/7: Memory",
        "prompts": [
            {"key": "daily_notes", "prompt": "Enable daily memory notes? (y/n):", "type": "bool", "default": "y"},
            {"key": "long_term", "prompt": "Enable long-term memory curation? (y/n):", "type": "bool", "default": "y"},
            {"key": "heartbeat_maintenance", "prompt": "Auto-maintain memory during heartbeats? (y/n):", "type": "bool", "default": "y"},
        ],
    },
    {
        "id": "platforms",
        "title": "Step 7/7: Platforms",
        "prompts": [
            {
                "key": "platforms",
                "prompt": "Which channels will this persona use?",
                "type": "multi_choice",
                "choices": [
                    {"value": "telegram", "label": "Telegram"},
                    {"value": "whatsapp", "label": "WhatsApp"},
                    {"value": "discord", "label": "Discord"},
                    {"value": "signal", "label": "Signal"},
                    {"value": "sms", "label": "SMS"},
                    {"value": "voice", "label": "Voice calls"},
                ],
            },
            {"key": "same_personality", "prompt": "Same personality across all platforms? (y/n):", "type": "bool", "default": "y"},
        ],
    },
]


def get_step(step_id):
    """Get a step definition by ID."""
    for step in STEPS:
        if step["id"] == step_id:
            return step
    return None


def get_all_steps():
    """Return all step definitions."""
    return STEPS
