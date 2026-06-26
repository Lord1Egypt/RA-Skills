# groq-voice-transcriber

Автоматическая расшифровка голосовых сообщений через Groq Whisper API.

## Что делает

- Перехватывает входящие аудио из Telegram
- Расшифровывает через Groq Whisper API
- Отправляет текст в LLM для ответа
- Возвращает ответ пользователю

## Настройка

1. Установи зависимости: `pip install -r requirements.txt`
2. Создай `.env` с `GROQ_API_KEY`
3. Установи навык: `clawhub install ./skills/groq-voice-transcriber`

## Автор

Создано для Андрея (Tr0n2321)
