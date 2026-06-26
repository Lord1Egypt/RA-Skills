#!/usr/bin/env python3
"""
Telegram Voice Message Handler
Интеграция с OpenClaw для обработки голосовых сообщений.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tempfile
import base64
from pathlib import Path
from typing import Optional

import httpx
from faster_whisper import WhisperModel

from kiwi.tts.runpod import TTSClient, TTSConfig
from kiwi.utils import kiwi_log


class TelegramVoiceHandler:
    """
    Обработчик голосовых сообщений из Telegram.
    
    Используется OpenClaw для:
    1. Получения голосовых сообщений
    2. Транскрипции через Faster Whisper
    3. Отправки ответа текстом или голосом
    """
    
    def __init__(
        self,
        whisper_model: str = "small",
        whisper_device: str = "cuda",
        tts_config: Optional[TTSConfig] = None,
    ):
        kiwi_log("TELEGRAM", f"Loading Whisper model: {whisper_model}...")
        self.whisper = WhisperModel(
            whisper_model,
            device=whisper_device,
            compute_type="float16" if whisper_device == "cuda" else "int8",
        )
        kiwi_log("TELEGRAM", "Whisper loaded")
        
        self.tts_client = None
        if tts_config and tts_config.endpoint_id:
            self.tts_client = TTSClient(tts_config)
            kiwi_log("TELEGRAM", "TTS client initialized")
    
    def transcribe_audio(self, audio_path: str, language: str = "ru") -> str:
        """Транскрипция аудио файла."""
        segments, info = self.whisper.transcribe(
            audio_path,
            language=language if language != "auto" else None,
            vad_filter=True,
        )
        
        text = " ".join([s.text.strip() for s in segments])
        return text.strip()
    
    def transcribe_base64(self, audio_base64: str, format: str = "ogg") -> str:
        """Транскрипция аудио из base64."""
        audio_bytes = base64.b64decode(audio_base64)
        
        with tempfile.NamedTemporaryFile(suffix=f".{format}", delete=False) as f:
            f.write(audio_bytes)
            temp_path = f.name
        
        try:
            return self.transcribe_audio(temp_path)
        finally:
            os.unlink(temp_path)
    
    async def generate_voice_response(
        self,
        text: str,
        style: Optional[str] = None,
    ) -> Optional[bytes]:
        """Генерация голосового ответа через TTS."""
        if not self.tts_client:
            return None
        
        result = await self.tts_client.generate_async(
            text,
            style=style,
            auto_emotion=True,
        )
        
        if result is None:
            return None
        
        audio, sr = result
        
        # Конвертируем в OGG для Telegram
        import soundfile as sf
        import subprocess
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as wav_file:
            sf.write(wav_file.name, audio, sr)
            wav_path = wav_file.name
        
        ogg_path = wav_path.replace(".wav", ".ogg")
        
        try:
            # Конвертируем в OGG Opus (формат Telegram voice)
            subprocess.run([
                "ffmpeg", "-y", "-i", wav_path,
                "-c:a", "libopus", "-b:a", "64k",
                ogg_path
            ], capture_output=True, check=True)
            
            with open(ogg_path, "rb") as f:
                return f.read()
        finally:
            os.unlink(wav_path)
            if os.path.exists(ogg_path):
                os.unlink(ogg_path)


def process_voice_message(
    audio_path: str,
    respond_with_voice: bool = False,
    whisper_model: str = "small",
) -> dict:
    """
    Обработка голосового сообщения.
    
    Вызывается из OpenClaw при получении голосового сообщения.
    
    Args:
        audio_path: Путь к аудио файлу
        respond_with_voice: Ответить голосом
        whisper_model: Размер модели Whisper
        
    Returns:
        {
            "transcription": "текст сообщения",
            "voice_response": bytes | None
        }
    """
    handler = TelegramVoiceHandler(whisper_model=whisper_model)
    
    transcription = handler.transcribe_audio(audio_path)
    
    return {
        "transcription": transcription,
        "voice_response": None,  # TTS добавляется при необходимости
    }


# CLI для тестирования
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python telegram_voice.py <audio_file>")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    
    if not os.path.exists(audio_path):
        print(f"File not found: {audio_path}")
        sys.exit(1)
    
    handler = TelegramVoiceHandler()
    text = handler.transcribe_audio(audio_path)
    
    print(f"Transcription: {text}")
