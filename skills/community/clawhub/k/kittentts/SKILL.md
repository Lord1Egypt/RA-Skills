# KittenTTS Skill

Génère des réponses audio TTS localement avec le modèle KittenTTS.

## Installation

```bash
pip install https://github.com/KittenML/KittenTTS/releases/download/0.8.1/kittentts-0.8.1-py3-none-any.whl soundfile
```

## Utilisation

```python
from kittentts import KittenTTS

# Charger le modèle (nano = plus léger, mini = meilleure qualité)
model = KittenTTS("KittenML/kitten-tts-nano-0.8-int8")

# Générer audio
audio = model.generate("Bonjour Fred !", voice="Bella")

# Sauvegarder
model.generate_to_file("Bonjour Fred !", "output.wav", voice="Luna")
```

## Voix disponibles

- **Luna** (défaut)
- Bella
- Jasper
- Luna
- Bruno
- Rosie
- Hugo
- Kiki
- Leo

## Modèles

| Modèle | Paramètres | Taille |
|--------|-------------|--------|
| nano-int8 | 15M | 25 MB |
| nano | 15M | 56 MB |
| micro | 40M | 41 MB |
| mini | 80M | 80 MB |

## Outil `kittentts`

Un wrapper CLI est disponible à la racine du workspace :

```bash
python kittentts_cli.py "Ton texte ici" --voice Luna --output audio.wav
```

**Note:** Le venv se trouve dans `skills/kittentts/.venv/`

## Intégration OpenClaw

Pour utiliser avec l'outil `tts` d'OpenClaw, le skill génère le fichier audio et le tool `tts` l'envoie automatiquement sur Telegram.
