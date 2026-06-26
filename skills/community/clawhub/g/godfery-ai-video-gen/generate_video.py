#!/usr/bin/env python3
"""
AI Video Generator - End-to-end video creation from text prompts
Powered by SkillBoss API Hub: image generation, video synthesis, voice-over, and FFmpeg editing.
"""

import os
import sys
import argparse
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SKILLBOSS_API_KEY = os.getenv('SKILLBOSS_API_KEY')
API_BASE = "https://api.heybossai.com/v1"


def pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()


class VideoGenerator:
    def __init__(self, output_dir='output'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_image(self, prompt, size="1024x1024", prefer="quality"):
        """Generate image using SkillBoss API Hub"""
        if not SKILLBOSS_API_KEY:
            raise ValueError("SKILLBOSS_API_KEY not set")

        print(f"Generating image: {prompt[:50]}...")

        result = pilot({"type": "image", "inputs": {"prompt": prompt, "size": size}, "prefer": prefer})
        image_url = result["result"]["image_url"]

        # Download image
        img_path = self.output_dir / f"image_{int(time.time())}.png"
        img_data = requests.get(image_url).content
        with open(img_path, 'wb') as f:
            f.write(img_data)

        print(f"Image saved: {img_path}")
        return str(img_path)

    def image_to_video(self, image_path, prompt=None, duration=5):
        """Convert image to video using SkillBoss API Hub"""
        if not SKILLBOSS_API_KEY:
            raise ValueError("SKILLBOSS_API_KEY not set")

        print(f"Creating video from image...")

        result = pilot({
            "type": "video",
            "inputs": {
                "prompt": prompt or "animate this image",
                "image": image_path,
                "duration": duration
            },
            "prefer": "balanced"
        })
        video_url = result["result"]["video_url"]

        # Download video
        video_path = self.output_dir / f"video_{int(time.time())}.mp4"
        video_data = requests.get(video_url).content
        with open(video_path, 'wb') as f:
            f.write(video_data)

        print(f"Video saved: {video_path}")
        return str(video_path)

    def add_audio(self, text, voice="alloy"):
        """Generate audio using SkillBoss API Hub TTS"""
        if not SKILLBOSS_API_KEY:
            raise ValueError("SKILLBOSS_API_KEY not set")

        print(f"Generating voiceover: {text[:50]}...")

        result = pilot({"type": "tts", "inputs": {"text": text, "voice": voice}, "prefer": "balanced"})
        audio_url = result["result"]["audio_url"]

        audio_path = self.output_dir / f"audio_{int(time.time())}.mp3"
        audio_data = requests.get(audio_url).content
        with open(audio_path, 'wb') as f:
            f.write(audio_data)

        print(f"Audio saved: {audio_path}")
        return str(audio_path)

    def combine_video_audio(self, video_path, audio_path, output_path):
        """Combine video and audio using FFmpeg"""
        import subprocess

        print(f"Combining video and audio...")

        cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-i', audio_path,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-shortest',
            output_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"FFmpeg error: {result.stderr}")

        print(f"Final video saved: {output_path}")
        return output_path


def main():
    parser = argparse.ArgumentParser(description='Generate AI videos from text prompts via SkillBoss API Hub')
    parser.add_argument('--prompt', required=True, help='Text prompt for video generation')
    parser.add_argument('--voiceover', help='Text for voiceover narration')
    parser.add_argument('--output', default='output.mp4', help='Output video file')
    parser.add_argument('--voice', default='alloy', help='Voice for TTS (alloy, echo, fable, onyx, nova, shimmer)')

    args = parser.parse_args()

    try:
        generator = VideoGenerator()

        # Step 1: Generate image
        image_path = generator.generate_image(args.prompt)

        # Step 2: Convert to video
        video_path = generator.image_to_video(image_path, args.prompt)

        # Step 3: Add voiceover if requested
        if args.voiceover:
            audio_path = generator.add_audio(args.voiceover, args.voice)
            final_path = generator.combine_video_audio(video_path, audio_path, args.output)
        else:
            # Just rename/move the video
            os.rename(video_path, args.output)
            final_path = args.output

        print(f"\n✅ SUCCESS! Video created: {final_path}")

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
