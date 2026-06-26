import os
import sys
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

# Load API key from local .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("Error: GROQ_API_KEY not found in .env file.")
    sys.exit(1)

client = Groq(api_key=api_key)

# The output path where OpenClaw canvas files go
# We resolve it relative to the script's location to make it portable (VPS-ready)
# speech.py is in .openclaw/workspace/skills/groq-arabic-tts/
base_dir = Path(__file__).resolve().parent.parent.parent.parent
output_dir = base_dir / "canvas"
output_dir.mkdir(parents=True, exist_ok=True)
speech_file_path = output_dir / "speech.wav"

# Get input text, optional language, and optional voice from command line arguments
if len(sys.argv) < 2:
    print("Usage: python speech.py \"text to speak\" [ar|en] [voice_name]")
    sys.exit(1)

input_text = sys.argv[1]
lang = sys.argv[2] if len(sys.argv) > 2 else "ar"
voice_arg = sys.argv[3] if len(sys.argv) > 3 else None

# Configuration and Voice defaults
if lang == "en":
    model_id = "canopylabs/orpheus-v1-english"
    voice_id = voice_arg if voice_arg else "autumn"
else:
    model_id = "canopylabs/orpheus-arabic-saudi"
    voice_id = voice_arg if voice_arg else "fahad"

speech_file_path = output_dir / "speech.wav"

try:
    response = client.audio.speech.create(
        model=model_id,
        voice=voice_id,
        response_format="wav",
        input=input_text,
    )
    # BinaryAPIResponse in Groq SDK uses write_to_file
    response.write_to_file(speech_file_path)
    print(f"Success: Speech generated at {speech_file_path}")
    print("MANDATORY: You MUST now paste this link in your chat response: http://127.0.0.1:18789/__openclaw__/canvas/speech.wav")
except Exception as e:
    print(f"Error calling Groq API: {e}")
    sys.exit(1)
