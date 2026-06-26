# pollinations_audio_gen.py
import os
import random
import requests
import urllib.parse
import argparse

def sanitize_output_path(output_path, default_dir=None):
    """Sanitize output path to prevent path traversal attacks."""
    if not output_path:
        return "output.mp3"
    
    allowed_dirs = os.getenv("ALLOWED_OUTPUT_DIRS", default_dir or ".").split(",")
    allowed_dirs = [os.path.abspath(d.strip()) for d in allowed_dirs]
    
    if os.path.isabs(output_path):
        output_path = os.path.abspath(output_path)
    else:
        output_path = os.path.abspath(output_path)
    
    is_allowed = any(
        output_path.startswith(ad + os.sep) or output_path == ad 
        for ad in allowed_dirs
    )
    
    if not is_allowed:
        safe_path = os.path.join(allowed_dirs[0], "output.mp3")
        print(f"Warning: Output path not allowed. Using '{safe_path}'")
        return safe_path
    
    if ".." in output_path:
        safe_path = os.path.join(allowed_dirs[0], "output.mp3")
        print(f"Warning: Path traversal detected. Using '{safe_path}'")
        return safe_path
    
    return output_path

class PollinationsAudioGenerator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('POLLINATIONS_API_KEY')
        self.audio_api_base_url = "https://gen.pollinations.ai"

    def generate_audio(self, prompt, model="suno-4", duration=30, seed=None, output_file="output.mp3"):
        """生成音樂"""
        if not prompt:
            raise ValueError("Prompt 唔可以係空")

        if seed is None:
            seed = random.randint(0, 1000000000)

        params = {
            "model": model,
            "duration": duration,
            "seed": seed,
        }

        if self.api_key:
            params['key'] = self.api_key

        encoded_prompt = urllib.parse.quote(prompt)
        req = requests.Request('GET', f"{self.audio_api_base_url}/audio/{encoded_prompt}", params=params)
        prepared = req.prepare()

        # Log URL without exposing API key
        safe_url = prepared.url
        if 'key=' in safe_url:
            safe_url = safe_url.split('key=')[0] + "key=***"
        print(f"Generating audio from URL: {safe_url}")

        with requests.Session() as session:
            response = session.send(prepared)
            response.raise_for_status()

            with open(output_file, 'wb') as f:
                f.write(response.content)

            print(f"Audio successfully saved to {output_file}")
            return output_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pollinations AI Audio Generator CLI")
    parser.add_argument("prompt", type=str, help="描述你想生成嘅音樂 (Prompt)")
    parser.add_argument("--model", type=str, default="suno-4",
                        choices=["suno-4", "suno-3.5", "suno-3", "whisper"],
                        help="選擇 Model (預設: suno-4)")
    parser.add_argument("--duration", type=int, default=30, help="音樂時長（秒），預設: 30")
    parser.add_argument("--seed", type=int, default=None, help="Seed 值（預設: 隨機）")
    parser.add_argument("--output", type=str, default="output.mp3", help="輸出檔案名稱（預設: output.mp3）")

    args = parser.parse_args()

    # Get workspace path and sanitize output
    workspace_path = os.getenv("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
    default_output_dir = os.path.join(workspace_path, "outputs")
    os.makedirs(default_output_dir, exist_ok=True)
    
    args.output = sanitize_output_path(args.output, default_output_dir)

    generator = PollinationsAudioGenerator()
    generator.generate_audio(
        prompt=args.prompt,
        model=args.model,
        duration=args.duration,
        seed=args.seed,
        output_file=args.output
    )
