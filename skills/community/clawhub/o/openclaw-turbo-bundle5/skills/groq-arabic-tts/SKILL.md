---
slug: groq-arabic-english-tts
name: Groq Arabic & English TTS
display_name: Groq Arabic & English TTS
version: 1.0.0
tags: [vocal, arabic, english, groq, saudi]
description: Génère des messages vocaux réalistes en Arabe Saoudien et Anglais via l'API ultra-rapide de Groq.
---

# Groq Arabic TTS

Cette compétence permet à l'agent de générer des messages vocaux réalistes en arabe.

## Utilisation

L'agent utilise cette compétence via le script `speech.py`.

```bash
python speech.py "Le texte à dire ici"
```

Le script génère un fichier `speech.wav` dans le dossier `C:\Users\inves\.openclaw\canvas\`.

**INSTRUCTION CRUCIALE** : Après chaque génération, vous DEVEZ afficher ce lien exact dans votre réponse pour l'utilisateur :
`http://127.0.0.1:18789/__openclaw__/canvas/speech.wav`
