# image2pptx

Claude Code skill for converting static images to editable PowerPoint files.

**Full source & docs:** [github.com/JadeLiu-tech/px-image2pptx](https://github.com/JadeLiu-tech/px-image2pptx)

## Install as Claude Code skill

Copy the folder to your skills directory:

```bash
cp -r . ~/.claude/skills/image2pptx/
```

Then use it in Claude Code:

```
convert slide.png to an editable pptx
```

## Requirements

```bash
pip install Pillow numpy opencv-python python-pptx paddleocr paddlepaddle simple-lama-inpainting torch
```

## License

MIT-0
