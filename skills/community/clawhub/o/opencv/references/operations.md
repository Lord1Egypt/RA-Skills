# OpenCV WASM Operations Reference

Complete reference for all operations supported by `opencv-component.wasm`.

## Tool Usage

**Important:** Use `--` separator to pass arguments directly to the component:

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/opencv/files/opencv-component.wasm",
  args: ["--", "<command>", "<subcommand>", "-i", "image.jpg", "-o", "out.jpg", ...options]
})
```

The `--` tells wasm-sandbox-run to pass all following arguments directly to the component.

For file access, map directories:
```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/opencv/files/opencv-component.wasm",
  args: ["--", "process", "resize", "-i", "input.jpg", "-o", "out.jpg", "--width", "800", "--height", "600"],
  workDir: "/path/to/images"
})
```

---

## Image Process (`process`)

### resize
```
args: ["process", "resize", "--input", "<input>", "--output", "<output>", "--width", "<px>", "--height", "<px>"]
```
Options: `--interp` (nearest|linear|cubic|lanczos, default: linear)

### grayscale
```
args: ["process", "grayscale", "--input", "<input>", "--output", "<output>"]
```

### blur
```
args: ["process", "blur", "--input", "<input>", "--output", "<output>", "--ksize", "<odd_number>"]
```

### median
```
args: ["process", "median", "--input", "<input>", "--output", "<output>", "--ksize", "<odd_number>"]
```

### bilateral
```
args: ["process", "bilateral", "--input", "<input>", "--output", "<output>"]
```

### canny
```
args: ["process", "canny", "--input", "<input>", "--output", "<output>"]
```

### sobel
```
args: ["process", "sobel", "--input", "<input>", "--output", "<output>"]
```

### rotate
```
args: ["process", "rotate", "--input", "<input>", "--output", "<output>", "--angle", "<degrees>"]
```

### flip
```
args: ["process", "flip", "--input", "<input>", "--output", "<output>", "--mode", "<0|1|-1>"]
```

### threshold
```
args: ["process", "threshold", "--input", "<input>", "--output", "<output>", "--thresh", "<0-255>", "--maxval", "<0-255>"]
```

### morphology
```
args: ["process", "morphology", "--input", "<input>", "--output", "<output>", "--op", "<erode|dilate|open|close|gradient>"]
```

### adjust
```
args: ["process", "adjust", "--input", "<input>", "--output", "<output>", "--alpha", "<contrast>", "--beta", "<brightness>"]
```

### equalize
```
args: ["process", "equalize", "--input", "<input>", "--output", "<output>"]
```

### sharpen
```
args: ["process", "sharpen", "--input", "<input>", "--output", "<output>"]
```

### colorspace
```
args: ["process", "colorspace", "--input", "<input>", "--output", "<output>", "--space", "<BGR|HSV|GRAY|YUV>"]
```

### crop
```
args: ["process", "crop", "--input", "<input>", "--output", "<output>", "--x", "<px>", "--y", "<px>", "--width", "<px>", "--height", "<px>"]
```

### watermark
```
args: ["process", "watermark", "--input", "<input>", "--output", "<output>", "--text", "<text>"]
```

### perspective
```
args: ["process", "perspective", "--input", "<input>", "--output", "<output>", "--src", "<x1,y1,x2,y2,x3,y3,x4,y4>", "--dst", "<x1,y1,x2,y2,x3,y3,x4,y4>"]
```

### stats
```
args: ["process", "stats", "--input", "<input>"]
```

### grid
```
args: ["process", "grid", "--input", "<input>", "--output", "<output>", "--cols", "<n>", "--rows", "<n>"]
```

---

## Detection (`detect`)

### cascade
```
args: ["detect", "cascade", "--input", "<input>", "--output", "<output>", "--cascade", "<cascade_xml>"]
```

### dnn
```
args: ["detect", "dnn", "--input", "<input>", "--output", "<output>", "--model", "<model.onnx>"]
```

### hog
```
args: ["detect", "hog", "--input", "<input>", "--output", "<output>"]
```

### contour
```
args: ["detect", "contour", "--input", "<input>", "--output", "<output>"]
```

### circle
```
args: ["detect", "circle", "--input", "<input>", "--output", "<output>"]
```

### line
```
args: ["detect", "line", "--input", "<input>", "--output", "<output>"]
```

---

## Features (`feature`)

### orb
```
args: ["feature", "orb", "--input", "<input>", "--output", "<output>"]
```

### sift
```
args: ["feature", "sift", "--input", "<input>", "--output", "<output>"]
```

### akaze
```
args: ["feature", "akaze", "--input", "<input>", "--output", "<output>"]
```

### match
```
args: ["feature", "match", "--input", "<img1>", "--ref", "<img2>", "--output", "<output>"]
```

### homography
```
args: ["feature", "homography", "--input", "<img1>", "--ref", "<img2>", "--output", "<output>"]
```

### optflow
```
args: ["feature", "optflow", "--input", "<frame1>", "--ref", "<frame2>", "--output", "<output>"]
```

### template
```
args: ["feature", "template", "--input", "<input>", "--template", "<template>", "--output", "<output>"]
```

---

## Stitching (`stitch`)

```
args: ["stitch", "--inputs", "<img1>", "<img2>", "...", "--output", "<output>", "--mode", "<panorama|scans>"]
```

Example:
```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/opencv/files/opencv-component.wasm",
  args: ["stitch", "--inputs", "left.jpg", "center.jpg", "right.jpg", "--output", "panorama.jpg", "--mode", "panorama"],
  workDir: "/path/to/images"
})
```

---

## Photo (`photo`)

### denoise
```
args: ["photo", "denoise", "--input", "<input>", "--output", "<output>"]
```

### inpaint
```
args: ["photo", "inpaint", "--input", "<input>", "--mask", "<mask>", "--output", "<output>"]
```

### stylize
```
args: ["photo", "stylize", "--input", "<input>", "--output", "<output>"]
```

### pencil
```
args: ["photo", "pencil", "--input", "<input>", "--output", "<output>"]
```

### detail
```
args: ["photo", "detail", "--input", "<input>", "--output", "<output>"]
```

### edge-preserve
```
args: ["photo", "edge-preserve", "--input", "<input>", "--output", "<output>"]
```

### hdr
```
args: ["photo", "hdr", "--input", "<input>", "--output", "<output>"]
```

### seamless-clone
```
args: ["photo", "seamless-clone", "--input", "<input>", "--mask", "<mask>", "--output", "<output>"]
```

### decolor
```
args: ["photo", "decolor", "--input", "<input>", "--output", "<output>"]
```

---

## Calibration (`calib`)

### chessboard
```
args: ["calib", "chessboard", "--input", "<input>", "--output", "<output>"]
```

### undistort
```
args: ["calib", "undistort", "--input", "<input>", "--output", "<output>"]
```

### corners
```
args: ["calib", "corners", "--input", "<input>", "--output", "<output>"]
```

---

## ML (`ml`)

### train-knn
```
args: ["ml", "train-knn", "--data", "<data_dir>", "--labels", "<labels_file>", "--output", "<model.xml>"]
```

### train-svm
```
args: ["ml", "train-svm", "--data", "<data.txt>", "--labels", "<labels.txt>", "--output", "<model.xml>"]
```

### predict
```
args: ["ml", "predict", "--model", "<model.xml>", "--input", "<test.jpg>"]
```

### kmeans
```
args: ["ml", "kmeans", "--input", "<input>", "--output", "<output>", "--clusters", "<K>"]
```

---

## Batch (`batch`)

### process
```
args: ["batch", "process", "--inputs", "<input_dir>", "--outputs", "<output_dir>", "--op", "<resize|blur|...>", "--width", "800", "--height", "600"]
```

### convert
```
args: ["batch", "convert", "--inputs", "<input_dir>", "--outputs", "<output_dir>", "--format", "<jpg|png|webp>"]
```

### stats
```
args: ["batch", "stats", "--inputs", "<input_dir>"]
```

---

## Info

```
args: ["info"]
```
Prints OpenCV build info and available modules.

---

## Global Options

| Option | Description |
|--------|-------------|
| `-v, --verbose` | Enable verbose/debug output |
| `-f, --format <FORMAT>` | Output format: text or json (default: text) |
| `-h, --help` | Print help |
| `-V, --version` | Print version |

---

## Sandbox Notes

- Input/output paths are relative to mapped `workDir`
- Use `--map-dir ./local::/guest` or `--work-dir` to expose directories
- Use `--wasm-timeout` for long operations on large images (recommended: 30+ seconds)
- No network access unless explicitly allowed with `--allowed-outbound-hosts`
