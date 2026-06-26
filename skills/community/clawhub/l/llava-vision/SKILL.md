---
name: llava-vision-local
version: 0.1.0
description: Call a local llama.cpp server with the LLaVA model to analyze images.
license: MIT
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: []
    os:
      - linux
      - darwin
      - win32
---

# LLaVA Vision Skill

> This skill forwards an image to a locally running **llama.cpp** server that hosts a LLaVA model and returns the model’s text description of the image. It accepts either a local file path or a remote image URL.

## Usage

```sh
clawhub llava-vision --image /path/to/photo.jpg
# or
clawhub llava-vision --image https://example.com/photo.jpg
```

The skill uses the built‑in **vision_analyze** tool, which expects an image file path. If the image cannot be read or the server is unreachable, an error message will be returned.

## Dependencies

- Node.js (the skill itself)
- A local **llama.cpp** server with the LLaVA model exposed at the default endpoint.

## Example

```sh
$ clawhub run llava-vision --image ./cat.png
The image contains a cat sitting on a windowsill, looking out at a sunny garden.
```
