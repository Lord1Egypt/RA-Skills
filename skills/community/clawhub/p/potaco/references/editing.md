# Image Editing Modes

The `potaco edit` command supports three modes based on which mask-related flags are provided. The mode is determined automatically by the CLI.

## Mode 1: Basic Edit (no mask flags)

No `--mask`, `--mask-rect`, `--mask-circle`, or `--extend` flags.

```sh
potaco edit --prompt "make it look like a painting" --image photo.jpg
```

The provider applies the prompt to the entire image. Supported by OpenAI, fal, and custom OpenAI-compatible providers.

**Dry run output**: mode is `"basic"` in the JSON body.

## Mode 2: Inpainting (masked edit)

Use `--mask`, `--mask-rect`, or `--mask-circle` to edit a specific region. The mask is a PNG where transparent pixels (alpha=0) indicate the area to edit and opaque pixels (alpha=255) indicate areas to keep unchanged.

### Mask from file

```sh
potaco edit --prompt "remove the person" --image photo.png --mask mask.png
```

The mask file should match the source image dimensions. If dimensions differ, potaco resizes it to match before sending it.

### Rectangular mask

```sh
potaco edit --prompt "add a tree" --image landscape.png --mask-rect 100,200,300,400
```

Format: `x,y,w,h` in pixels. Transparent rectangle means edit; opaque background means keep.

### Circular mask

```sh
potaco edit --prompt "add sunglasses" --image face.png --mask-circle 256,256,100
```

Format: `cx,cy,r` in pixels (center x, center y, radius).

### Mask validation

- If `--mask` file does not exist, the command returns an image error (exit code 4) with the file path in the message.
- If the source image cannot be read, returns an image error.
- Only one mask type should be used per command. If multiple are provided, `--mask` takes priority, then `--mask-rect`, then `--mask-circle`.
- All mask modes require the source image to be a valid PNG, JPEG, or WebP file. Source images are validated for file size and dimensions before processing to prevent OOM.

**Dry run output**: mode is `"inpaint"` with mask/rect/circle values shown.

## Mode 3: Outpainting (canvas extension)

Use `--extend` to expand the canvas in one or more directions. Extended areas are editable; the original image area is preserved.

```sh
potaco edit --prompt "extend the landscape" --image photo.png --extend right=256
```

### Extend format

```
top=N,bottom=N,left=N,right=N
all=N
```

Examples:
```
--extend top=128,bottom=128           # extend canvas vertically
--extend left=256,right=256           # extend canvas horizontally
--extend all=200                      # extend all sides by 200px
--extend top=100,bottom=200,left=50   # different values per side
```

### Dimension validation

The expanded canvas is checked against a pixel budget. If the expanded dimensions exceed the maximum, the command returns an image error before making any API call.

**Dry run output**: mode is `"outpaint"` with the parsed extend config shown.

## Edit with Vercel provider

The Vercel AI Gateway does not support image editing. If the active provider is `vercel`, the edit command returns:

```
Error: Image editing is not supported by the Vercel AI Gateway provider.
Hint: Use 'potaco use' to switch to a provider that supports editing.
```

Switch to a provider that supports editing:
```sh
potaco use openai
# or
potaco use fal
# or
potaco use custom
```

## Edit flags vs gen flags

The edit command shares most flags with gen but omits `--quality`, `--seed`, `--guidance-scale`, and `--negative-prompt`. It adds the mask and extend flags. Common shared flags: `--model`, `--size`, `--n`, `--response-format`, `--output`, `--output-format`, `--stdout`, all provider override flags, and `--dry-run`.

## Output behavior

Edit output follows the same rules as gen:
- Default: auto-generated filename, prints `Saved to: <path>`.
- `-o path.png`: saves to specified path.
- `--stdout`: pipes raw image bytes (requires `--n 1`).
- `--json`: prints JSON metadata including the source image path and edit mode.
