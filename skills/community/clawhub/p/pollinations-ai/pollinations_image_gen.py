# pollinations_image_gen.py
import os
import random
import requests
import urllib.parse
import argparse
import subprocess

def send_via_telegram(image_path, caption=None):
    """Send image via Telegram using openclaw message command"""
    if not os.path.exists(image_path):
        print(f"Error: File {image_path} not found")
        return False
    
    # Get chat ID from environment - must be explicitly set for security
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not chat_id:
        print("Warning: TELEGRAM_CHAT_ID not set. Telegram send skipped.")
        print("To enable Telegram sending, set TELEGRAM_CHAT_ID environment variable.")
        return False
    
    # Validate chat_id is numeric only (basic security)
    if not chat_id.isdigit():
        print("Error: TELEGRAM_CHAT_ID must be numeric")
        return False
    
    try:
        # Send to specified chat ID
        cmd = ["openclaw", "message", "send", "--target", chat_id, "--media", image_path]
        if caption:
            cmd.extend(["--message", caption])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Image sent via Telegram: {image_path}")
            return True
        else:
            print(f"Failed to send via Telegram: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error sending via Telegram: {e}")
        return False

class PollinationsImageGenerator:
    def __init__(self, api_key=None):
        # 如果冇傳入 api_key，會自動搵環境變數 POLLINATIONS_API_KEY
        self.api_key = api_key or os.getenv('POLLINATIONS_API_KEY')
        self.text_api_url = "https://gen.pollinations.ai/v1/chat/completions"
        self.image_api_base_url = "https://gen.pollinations.ai"

    def enhance_prompt(self, prompt):
        """利用 Pollinations 內建嘅 LLM 潤飾 Prompt"""
        if not prompt:
            raise ValueError("Prompt 唔可以係空")

        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"

        payload = {
            "model": "openai",
            "messages": [
                {"role": "system", "content": "Rewrite as high-quality English image prompt. Raw text only."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(self.text_api_url, json=payload, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        return data['choices'][0]['message']['content']

    def generate_image(self, prompt, model="flux", width=1024, height=1024,
                       seed=None, safe=False, enhance=False, output_file="output.jpg"):
        """產生並下載圖片"""
        if not prompt:
            raise ValueError("Prompt 唔可以係空")

        if seed is None:
            seed = random.randint(0, 1000000000)

        params = {
            "model": model,
            "width": width,
            "height": height,
            "seed": seed,
            "nologo": "true",
            "safe": str(safe).lower(),
            "enhance": str(enhance).lower()
        }

        if self.api_key:
            params['key'] = self.api_key

        encoded_prompt = urllib.parse.quote(prompt)
        # 用 requests.Request 組合 URL 方便 debug
        req = requests.Request('GET', f"{self.image_api_base_url}/image/{encoded_prompt}", params=params)
        prepared = req.prepare()
        
        # Log URL without exposing API key
        safe_url = prepared.url
        if 'key=' in safe_url:
            safe_url = safe_url.split('key=')[0] + "key=***"
        print(f"Generating image from URL: {safe_url}")

        with requests.Session() as session:
            response = session.send(prepared)
            response.raise_for_status()

            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            print(f"Image successfully saved to {output_file}")
            return output_file

def sanitize_output_path(output_path, default_dir=None):
    """
    Sanitize output path to prevent path traversal attacks.
    Only allows relative paths or paths within allowed directories.
    """
    if not output_path:
        return "output.jpg"
    
    # Get allowed directories from environment or use default
    allowed_dirs = os.getenv("ALLOWED_OUTPUT_DIRS", default_dir or ".").split(",")
    allowed_dirs = [os.path.abspath(d.strip()) for d in allowed_dirs]
    
    # Resolve the output path
    if os.path.isabs(output_path):
        output_path = os.path.abspath(output_path)
    else:
        output_path = os.path.abspath(output_path)
    
    # Check if path is within allowed directories
    is_allowed = any(
        output_path.startswith(ad + os.sep) or output_path == ad 
        for ad in allowed_dirs
    )
    
    if not is_allowed:
        # Default to first allowed directory
        safe_path = os.path.join(allowed_dirs[0], "output.jpg")
        print(f"Warning: Output path '{output_path}' not allowed. Using '{safe_path}'")
        return safe_path
    
    # Prevent path traversal with ..
    if ".." in output_path:
        safe_path = os.path.join(allowed_dirs[0], "output.jpg")
        print(f"Warning: Path traversal detected. Using '{safe_path}'")
        return safe_path
    
    return output_path

if __name__ == "__main__":
    # Get workspace path from environment or use default
    workspace_path = os.getenv("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
    default_output_dir = os.path.join(workspace_path, "outputs")
    
    # Create outputs directory if not exists
    os.makedirs(default_output_dir, exist_ok=True)
    parser = argparse.ArgumentParser(description="Pollinations AI Image Generator CLI")
    parser.add_argument("prompt", type=str, help="描述你想產生嘅圖片 (Prompt)")
    parser.add_argument("--enhance", action="store_true", help="使用 AI 潤飾 Prompt")
    parser.add_argument("--model", type=str, default="flux",
                        choices=["flux", "flux-2-dev", "zimage", "gptimage", "gptimage-large", "kontext",
                                 "seedream", "seedream-pro", "seedream5", "nanobanana", "nanobanana-2", "nanobanana-pro",
                                 "klein", "klein-large", "imagen-4", "grok-imagine"],
                        help="選擇 Model (預設: flux)")
    parser.add_argument("--width", type=int, default=1024, help="圖片闊度")
    parser.add_argument("--height", type=int, default=1024, help="圖片高度")
    parser.add_argument("--seed", type=int, default=None, help="Seed 值 (預設隨機)")
    parser.add_argument("--safe", action="store_true", help="開啟 Safe Mode")
    parser.add_argument("--output", type=str, default="output.jpg", help="輸出檔案名稱 (預設: output.jpg)")
    parser.add_argument("--telegram", action="store_true", help="生成後透過 Telegram 發送圖片")

    args = parser.parse_args()

    generator = PollinationsImageGenerator()
    
    final_prompt = args.prompt
    if args.enhance:
        print("Enhancing prompt...")
        final_prompt = generator.enhance_prompt(args.prompt)
        print(f"Enhanced Prompt: {final_prompt}")

    # Sanitize output path before generating
    args.output = sanitize_output_path(args.output, default_output_dir)

    generator.generate_image(
        prompt=final_prompt,
        model=args.model,
        width=args.width,
        height=args.height,
        seed=args.seed,
        safe=args.safe,
        output_file=args.output
    )
    
    # 如果開啟 --telegram flag，發送圖片到 Telegram
    if args.telegram:
        # Get workspace path from environment
        workspace_path = os.getenv("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
        
        # If output is in /tmp, copy to workspace outputs folder
        if args.output.startswith("/tmp"):
            import shutil
            safe_output = os.path.join(workspace_path, "outputs", os.path.basename(args.output))
            os.makedirs(os.path.dirname(safe_output), exist_ok=True)
            shutil.copy(args.output, safe_output)
            args.output = safe_output
            print(f"Copied to allowed directory: {safe_output}")
        
        caption = f"🎨 {args.model.upper()} - {final_prompt[:100]}{'...' if len(final_prompt) > 100 else ''}"
        send_via_telegram(args.output, caption)
