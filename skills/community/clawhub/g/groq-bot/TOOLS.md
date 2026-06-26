# TOOLS.md - Local Notes

## Groq Bot Spezifische Tools

### API Integration
- **Groq API**: Schnelle Textgeneration mit llama-3.1-8b-instant
- **Rate Limit**: <500 Anfragen/min empfohlen
- **Modelle**: llama-3.1-8b-instant, llama-3.3-70b-versatile, whisper-large-v3

### Skills
- **Text Generation**: Schnelle Low-Latency Antworten
- **Tool Assistance**: Unterstützt Tool-Nutzung (wenn aktiviert)
- **Optimiert für**: Kurze bis mittellange Antworten

### Performance
- **Latency**: Extrem niedrig dank Groqs LPU-Infrastruktur
- **Kosten**: Günstigere Inferenz im Vergleich zu anderen Anbietern

### Environment
- **API Key**: Aus .env (GROQ_API_KEY)
- **Provider**: Groq
- **Default Model**: llama-3.1-8b-instant