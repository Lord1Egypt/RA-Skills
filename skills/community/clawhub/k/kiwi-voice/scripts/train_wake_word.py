#!/usr/bin/env python3
"""Helper script for training custom OpenWakeWord models.

Guides the user through training a custom wake word model
(e.g. "kiwi", "hey kiwi", "ok computer") using Google Colab.
No manual voice recordings required — training uses synthetic speech.

Usage:
    python scripts/train_wake_word.py
    python scripts/train_wake_word.py --phrase "hey kiwi"
"""

import argparse
import sys


COLAB_URL = "https://colab.research.google.com/drive/1q1oe2zOyZp7UsB3jJiQ1IFn8z5YfjwEb"


def main():
    parser = argparse.ArgumentParser(
        description="Train a custom wake word model for Kiwi Voice"
    )
    parser.add_argument(
        "--phrase",
        type=str,
        default="kiwi",
        help="Wake phrase to train (default: kiwi)",
    )
    args = parser.parse_args()

    phrase = args.phrase

    print("""
================================================================================
  CUSTOM WAKE WORD TRAINING FOR KIWI VOICE
================================================================================

  This script guides you through training a custom OpenWakeWord model
  so Kiwi can respond to any wake phrase you choose.

  Training uses Google Colab (free GPU) and generates synthetic voice
  samples automatically -- no manual recordings needed.

  Estimated time: ~45 minutes on Colab free tier.

================================================================================
""")

    print(f"  Target wake phrase: \"{phrase}\"\n")

    print(f"""  STEP 1: Open the OpenWakeWord training notebook
  -------
  {COLAB_URL}

  STEP 2: Configure the notebook
  -------
  In the notebook, set these parameters:
    - target_phrase = "{phrase}"
    - n_samples = 1500          (synthetic samples to generate)
    - n_negative_samples = 5000 (negative examples)
    - epochs = 50

  STEP 3: Run all cells
  -------
  The notebook will:
    a) Generate synthetic speech samples of "{phrase}"
    b) Download negative samples (common speech that is NOT the wake word)
    c) Train a small ONNX model (~1-3 MB)
    d) Provide a download link for the .onnx file

  STEP 4: Download and install the model
  -------
  Save the .onnx file to your Kiwi Voice project:

    assets/{phrase.replace(' ', '_')}.onnx

  STEP 5: Update config.yaml
  -------
  Edit config.yaml to use the new wake word model:

    wake_word:
      engine: "openwakeword"
      model: "assets/{phrase.replace(' ', '_')}.onnx"
      threshold: 0.5

  STEP 6: Test it
  -------
  Start Kiwi Voice and say "{phrase}" -- you should hear
  the wake confirmation sound.

  TIP: If detection is too sensitive (false positives), increase
  the threshold to 0.6-0.8.  If it misses your voice, lower it
  to 0.3-0.4.

================================================================================
  Built-in models (no training needed):
    - hey_jarvis
    - alexa
    - hey_mycroft

  To use a built-in model, set:
    wake_word:
      engine: "openwakeword"
      model: "hey_jarvis"
      threshold: 0.5
================================================================================
""")


if __name__ == "__main__":
    main()
