#!/usr/bin/env python3
"""
speaker.py — iaworker TTS and display output
Speaks steps aloud and renders markdown to terminal.
"""

import os
import sys
import time
import tempfile
import subprocess
from pathlib import Path
from typing import Optional

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


PLATFORM = sys.platform
console = Console() if RICH_AVAILABLE else None


class Speaker:
    def __init__(self, lang: str = "en", tts_enabled: bool = True,
                 engine: str = "gtts", speed: float = 1.0, volume: float = 1.0):
        self.lang = lang
        self.tts_enabled = tts_enabled and (GTTS_AVAILABLE or PYTTSX3_AVAILABLE)
        self.engine = engine
        self.speed = speed
        self.volume = volume
        self._pyttsx3_engine = None
        self._init_offline_engine()

    def _init_offline_engine(self):
        if self.engine == "pyttsx3" and PYTTSX3_AVAILABLE:
            try:
                self._pyttsx3_engine = pyttsx3.init()
                self._pyttsx3_engine.setProperty("rate", 150 * self.speed)
                self._pyttsx3_engine.setProperty("volume", self.volume)
            except Exception as e:
                print(f"[speaker] pyttsx3 init failed: {e}")
                self._pyttsx3_engine = None

    def speak(self, text: str, block: bool = True) -> None:
        if not self.tts_enabled:
            return
        if self.engine == "gtts" and GTTS_AVAILABLE:
            self._speak_gtts(text, block)
        elif self._pyttsx3_engine:
            self._speak_pyttsx3(text, block)
        else:
            self._speak_gtts(text, block)

    def _speak_gtts(self, text: str, block: bool) -> None:
        try:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                tmp = f.name
            tts = gTTS(text=text, lang=self.lang, slow=(self.speed < 0.8))
            tts.save(tmp)
            self._play_audio_file(tmp, block)
            Path(tmp).unlink(missing_ok=True)
        except Exception as e:
            print(f"[speaker] gTTS error: {e}")

    def _speak_pyttsx3(self, text: str, block: bool) -> None:
        if self._pyttsx3_engine:
            self._pyttsx3_engine.say(text)
            if block:
                self._pyttsx3_engine.runAndWait()

    def _play_audio_file(self, path: str, block: bool) -> None:
        cmd = []
        if PLATFORM == "darwin":
            cmd = ["afplay", path]
        elif PLATFORM.startswith("linux"):
            cmd = ["aplay", path] if subprocess.run(["which", "aplay"], capture_output=True).returncode == 0 \
                  else ["paplay", path]
        elif PLATFORM == "win32":
            cmd = ["powershell", "-c", f"(New-Object Media.SoundPlayer '{path}').PlaySync()"]
        if cmd:
            if block:
                subprocess.run(cmd, capture_output=True)
            else:
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def speak_only(self, text: str) -> None:
        self.speak(text, block=True)

    def display_step(self, step: dict) -> None:
        if RICH_AVAILABLE:
            self._display_step_rich(step)
        else:
            self._display_step_plain(step)

    def _display_step_rich(self, step: dict) -> None:
        difficulty_color = {"easy": "green", "medium": "yellow", "hard": "red", "expert": "bold red"}
        color = difficulty_color.get(step.get("difficulty", "medium"), "white")
        body = step.get("description", "")
        if step.get("tools"):
            body += f"\n\n🔧 **Tools:** {', '.join(step['tools'])}"
        if step.get("time_estimate"):
            body += f"  ⏱ **Time:** {step['time_estimate']}"
        if step.get("safety_warning"):
            body += f"\n\n⚠️  **Safety:** {step['safety_warning']}"
        if step.get("common_mistakes"):
            body += f"\n\n❌ **Avoid:** {', '.join(step['common_mistakes'])}"
        panel = Panel(
            body.strip(),
            title=f"[bold cyan]Step {step['number']}:[/bold cyan] {step.get('title', '')}",
            border_style=color,
            expand=False
        )
        console.print(panel)

    def _display_step_plain(self, step: dict) -> None:
        sep = "=" * 60
        print(sep)
        print(f"STEP {step['number']}: {step.get('title', '').upper()}")
        print(sep)
        print(step.get("description", ""))
        if step.get("tools"):
            print(f"\n🔧 Tools: {', '.join(step['tools'])}")
        if step.get("time_estimate"):
            print(f"⏱  Time: {step['time_estimate']}")
        if step.get("safety_warning"):
            print(f"⚠️  Safety: {step['safety_warning']}")
        if step.get("common_mistakes"):
            print(f"❌ Avoid: {', '.join(step['common_mistakes'])}")
        print()

    def display_steps(self, steps: list[dict], speak: bool = False,
                      step_by_step: bool = False) -> None:
        if not steps:
            print("[iaworker] No steps to display.")
            return
        for step in steps:
            self.display_step(step)
            if speak:
                self._speak_step(step)
            if step_by_step and step["number"] < steps[-1]["number"]:
                self.wait_for_user()

    def _speak_step(self, step: dict) -> None:
        parts = [f"Step {step['number']}: {step.get('title', '')}"]
        if step.get("difficulty"):
            parts.append(f"Difficulty: {step['difficulty']}")
        if step.get("safety_warning"):
            parts.append(f"Safety warning: {step['safety_warning']}")
        text = ". ".join(parts)
        self.speak(text, block=True)

    def display_and_speak(self, text: str) -> None:
        if RICH_AVAILABLE:
            console.print(Panel(text, border_style="cyan", expand=False))
        else:
            print(f"📋 {text}")
        self.speak(text, block=True)

    def wait_for_user(self, prompt: str = None) -> None:
        if prompt is None:
            prompt = "Press Enter to continue to the next step..."
        if RICH_AVAILABLE:
            console.print(f"[bold yellow]{prompt}[/bold yellow]")
        else:
            print(f"\n{prompt}")
        input()


if __name__ == "__main__":
    speaker = Speaker(lang="en", tts_enabled=False)
    test_steps = [
        {
            "number": 1, "title": "Inspect the chain",
            "description": "Flip the bike and visually inspect the chain for rust, kinks, or stiff links.",
            "tools": ["work light"], "time_estimate": "2 min", "difficulty": "easy",
            "safety_warning": "Keep fingers clear of chain",
            "common_mistakes": ["Not checking every link"]
        },
        {
            "number": 2, "title": "Adjust chain tension",
            "description": "Loosen the rear axle bolts and slide the wheel to take up chain slack.",
            "tools": ["hex keys (5mm)"], "time_estimate": "10 min", "difficulty": "medium",
            "safety_warning": "Ensure axle bolts are torqued properly before riding",
            "common_mistakes": ["Over-tightening causing drivetrain drag"]
        },
    ]
    speaker.display_steps(test_steps, speak=False, step_by_step=False)
