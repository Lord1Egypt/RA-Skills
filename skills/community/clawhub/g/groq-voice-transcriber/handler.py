from groq import Groq
import os

class GroqVoiceTranscriber:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY", "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")
        self.client = Groq(api_key=api_key)
    
    def transcribe(self, audio_path: str, language: str = "ru") -> str:
        """Расшифровка аудио через Groq Whisper"""
        try:
            with open(audio_path, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                    file=(os.path.basename(audio_path), file.read()),
                    model="whisper-large-v3",
                    language=language
                )
            return transcription.text
        except Exception as e:
            return f"Ошибка расшифровки: {str(e)}"
    
    def get_response(self, text: str) -> str:
        """Получение ответа от Groq LLM"""
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Ты полезный ассистент. Отвечай кратко и по делу на русском языке."},
                    {"role": "user", "content": text}
                ],
                model="llama-3.1-8b-instant"
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Ошибка ответа: {str(e)}"
    
    def process_voice(self, audio_path: str) -> str:
        """Полный цикл: аудио → текст → ответ"""
        text = self.transcribe(audio_path)
        if text.startswith("Ошибка"):
            return text
        return self.get_response(text)

# Точка входа для OpenClaw
def handle(audio_path: str, **kwargs) -> str:
    transcriber = GroqVoiceTranscriber()
    return transcriber.process_voice(audio_path)
