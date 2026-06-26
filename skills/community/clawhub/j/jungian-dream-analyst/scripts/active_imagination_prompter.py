def generate_active_imagination_script(archetype_name, dream_context, symbol=None):
    """
    Generates a structured Active Imagination protocol for the user.
    
    Active Imagination is Jung's technique for consciously engaging with
    unconscious figures while in a waking, meditative state.
    
    Args:
        archetype_name (str): The figure to engage (e.g., "The Shadow", "The Anima")
        dream_context (str): The dream scene to return to
        symbol (str, optional): A specific symbol to focus on
    
    Returns:
        str: A step-by-step Active Imagination protocol
    """
    symbol_line = f"\n   Focus especially on: {symbol}." if symbol else ""

    script = f"""
╔══════════════════════════════════════════════════╗
║         ACTIVE IMAGINATION PROTOCOL              ║
╚══════════════════════════════════════════════════╝

Working with: {archetype_name}
Dream Scene: {dream_context}{symbol_line}

PREPARATION (5–10 minutes)
─────────────────────────
• Find a quiet space where you won't be interrupted.
• Have a journal and pen ready — do NOT use a screen.
• Sit comfortably. Close your eyes. Take 10 slow breaths.

STEP 1 — DESCENT: Return to the Dream
──────────────────────────────────────
• Visualize the dream scene as vividly as possible: {dream_context}
• Notice colors, textures, sounds, smells. Make it real.
• Do NOT force anything. Wait. Allow the scene to animate itself.

STEP 2 — ENCOUNTER: Meet the Figure
─────────────────────────────────────
• Allow {archetype_name} to appear or emerge within the scene.
• Look at them directly. Do not flee or dismiss them.
• Notice: What do they look like? What is their energy?

STEP 3 — DIALOGUE: Ask and Listen
───────────────────────────────────
Ask one or more of these questions — then wait for an answer:

  → "What do you want from me?"
  → "Why have you come to me now?"
  → "What are you trying to show me?"
  → "What do you need that I have not given?"

CRITICAL: Do not *invent* the answers. The answers will arise.
If nothing comes immediately, keep waiting. Trust the process.

STEP 4 — RECORD: Write Without Judgment
─────────────────────────────────────────
• Open your eyes and write down the entire dialogue immediately.
• Transcribe what the figure said verbatim, even if it shocks you.
• Do not edit, censor, or interpret yet. Just record.

STEP 5 — ETHICAL COMMITMENT: The Real-World Bridge
────────────────────────────────────────────────────
This is the most important step — it prevents inflation and keeps
the work grounded.

Ask yourself: "What ONE small, concrete action can I take in my
waking life to honor what {archetype_name} showed me?"

  Examples:
  • Write a letter you've been avoiding
  • Have a difficult conversation
  • Begin a creative project
  • Rest when you have been pushing

Write this commitment down and keep it.

CAUTIONS
─────────────────────────────────────────────────
• If the figure becomes overwhelming, open your eyes immediately.
• Do not engage if you are in acute emotional crisis.
• This work is complementary to — not a replacement for — therapy.

═══════════════════════════════════════════════════
"""
    return script


def generate_symbol_meditation(symbol, dream_context):
    """
    Generates a focused meditation for a specific dream symbol
    rather than an archetypal figure.
    """
    script = f"""
╔══════════════════════════════════════════════════╗
║           SYMBOL AMPLIFICATION PRACTICE          ║
╚══════════════════════════════════════════════════╝

Symbol: {symbol}
From dream: {dream_context}

STEP 1 — CONCENTRATE
• Close your eyes. Picture {symbol} exactly as it appeared.
• Hold the image steady. Don't let it shift or dissolve.

STEP 2 — PERSONAL LAYER
• Ask: "What does {symbol} mean to ME in my life?"
• What memories, feelings, or associations arise? Record all of them.

STEP 3 — ARCHETYPAL LAYER  
• Ask: "Where else have I seen this? In stories, myths, religions?"
• What fairytale, legend, or sacred text contains this image?

STEP 4 — THE GIFT
• Ask: "If this symbol were trying to give me something, what would it be?"
• Write the answer without judgment.

═══════════════════════════════════════════════════
"""
    return script


# Example usage
if __name__ == "__main__":
    print(generate_active_imagination_script(
        archetype_name="The Shadow",
        dream_context="The burning library with no exits",
        symbol="The dark figure setting fire to the books"
    ))
    
    print(generate_symbol_meditation(
        symbol="The golden key",
        dream_context="Found inside a hollowed book in a library"
    ))
