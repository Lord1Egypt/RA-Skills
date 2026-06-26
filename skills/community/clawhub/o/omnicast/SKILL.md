# OmniCast Studio 

## Description
OmniCast Studio is a local Node.js application that provides a multi-modal pipeline for processing text, audio, and video into podcast scripts and social media assets. It exposes a set of local API endpoints to orchestrate these tasks.

## Setup Requirements
This application requires the following environment variables to be set in a local `.env` file:
* `GEMINI_API_KEY`: Required for text analysis, translation, and script drafting.
* `OPENAI_API_KEY`: Required for audio transcription and synthesis.
* `PORT`: Defaults to 7860.

**System Requirements:**
* Node.js >= 20.0.0
* FFmpeg installed and available in the system PATH.

## API Endpoints (Localhost:7860)

The service runs strictly on `http://127.0.0.1:7860`. The following endpoints are available:

### 1. Media Ingestion
* **Endpoint:** `POST /api/ingest`
* **Purpose:** Accepts a URL or file upload. It extracts the text, detects the language, and translates it to English if necessary.

### 2. Script Drafting
* **Endpoint:** `POST /api/draft-script`
* **Purpose:** Utilizes the ingested text to format a conversational, two-host script suitable for audio synthesis.

### 3. Audio Synthesis
* **Endpoint:** `POST /api/synthesize`
* **Purpose:** Converts the drafted script into a final audio file using TTS services.

### 4. LinkedIn Packaging
* **Endpoint:** `POST /api/generate-linkedin`
* **Purpose:** Generates a social media text post and renders a looping MP4 video of the podcast cover art with the synthesized audio.