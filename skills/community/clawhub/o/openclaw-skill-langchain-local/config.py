# config.py
OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "phi4-mini"

LLM_CONFIG = {
    "coding": {
        "temperature": 0.1,
        "num_predict": 512,
        "top_p": 0.9,
        "repeat_penalty": 1.1
    },
    "chat": {
        "temperature": 0.7,
        "num_predict": 1024,
        "top_p": 0.95,
        "repeat_penalty": 1.0
    },
    "devops": {
        "temperature": 0.1,
        "num_predict": 256,
        "top_p": 0.9,
        "repeat_penalty": 1.1
    }
}

