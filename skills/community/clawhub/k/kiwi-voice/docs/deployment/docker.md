# Docker

## Docker Run

```bash
docker build -t kiwi-voice .

docker run -d \
  --name kiwi-voice \
  --device /dev/snd \
  -v ./config.yaml:/app/config.yaml \
  -v ./.env:/app/.env \
  -v ./data:/app/data \
  -p 7789:7789 \
  kiwi-voice
```

!!! note
    `--device /dev/snd` passes the sound devices to the container (Linux only). For audio output on macOS/Windows, use the [Web Microphone](../features/web-microphone.md) instead.

## Docker Compose

```yaml
version: "3.8"
services:
  kiwi-voice:
    build: .
    restart: unless-stopped
    devices:
      - /dev/snd:/dev/snd
    volumes:
      - ./config.yaml:/app/config.yaml
      - ./.env:/app/.env
      - ./data:/app/data
    ports:
      - "7789:7789"
    environment:
      - KIWI_LANGUAGE=en
      - KIWI_TTS_PROVIDER=kokoro
```

### With GPU (NVIDIA)

```yaml
version: "3.8"
services:
  kiwi-voice:
    build: .
    restart: unless-stopped
    devices:
      - /dev/snd:/dev/snd
    volumes:
      - ./config.yaml:/app/config.yaml
      - ./.env:/app/.env
      - ./data:/app/data
    ports:
      - "7789:7789"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - KIWI_LANGUAGE=en
      - KIWI_TTS_PROVIDER=kokoro
```

Requires the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).

## Volumes

| Mount | Purpose |
|-------|---------|
| `config.yaml` | Configuration |
| `.env` | Secrets |
| `data/` | Voice profiles, cached models |

## Dashboard Access

The dashboard is available at `http://localhost:7789` (or your server IP).
