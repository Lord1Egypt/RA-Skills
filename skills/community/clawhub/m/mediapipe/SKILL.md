---
name: mediapipe
description: on-device ML pipeline framework for vision, text, audio, and LLM inference. Cross-platform deployment to Android, iOS, web, desktop, edge devices, and IoT. 
---

# Google MediaPipe

## Overview

MediaPipe is Google's open-source framework for building on-device machine learning pipelines. It provides cross-platform APIs for vision, text, audio, and LLM inference tasks, plus a low-level graph-based pipeline framework for custom ML workloads. 

## Covers

- Computer vision tasks (face detection, face mesh, hand tracking, pose estimation, holistic landmarks, object detection, image classification/segmentation, gesture recognition)
- Text tasks (text classification, text embedding, language detection)
- Audio classification, (4) On-device LLM inference with MediaPipe GenAI/Tasks
- Model customization with MediaPipe Model Maker
- Visualizing/building ML pipelines with the MediaPipe Framework (graphs, calculators, packets)
- Drawing/rendering landmarks and detection results onto images/video
- Understanding MediaPipe's architecture and component ecosystem (Solutions, Tasks, Model Maker, Studio, Framework)

### Architecture

MediaPipe has two layers:

1. **MediaPipe Solutions** (high-level) — Pre-built, ready-to-use ML tasks via cross-platform APIs. Use these for most applications.
2. **MediaPipe Framework** (low-level) — Graph-based pipeline builder (packets, graphs, calculators) for custom on-device ML pipelines. C++ core with Android/iOS bindings.

The Solutions layer consists of:
- **MediaPipe Tasks** — Cross-platform libraries (Python, Android, iOS, Web/JS, C++) wrapping pre-trained models
- **MediaPipe Models** — Pre-trained TFLite model bundles downloadable per task
- **MediaPipe Model Maker** — Fine-tune/customize models with your own data
- **MediaPipe Studio** — Browser-based no-code benchmarking and prototyping tool

## Installation

### Python

```bash
pip install mediapipe
```

Latest version as of 2026-05: `0.10.35`. The Python package bundles all tasks. Models are downloaded separately at runtime or pre-downloaded.

### Android

Add to `build.gradle`:
```
implementation 'com.google.mediapipe:tasks-vision:0.10.35'
```

Replace `vision` with `text`, `audio`, or `genai` as needed.

### Web / JavaScript

```bash
npm install @mediapipe/tasks-vision
```

Available packages: `@mediapipe/tasks-vision`, `@mediapipe/tasks-text`, `@mediapipe/tasks-audio`, `@mediapipe/tasks-genai`.

### iOS (CocoaPods)

```
pod 'MediaPipeTasksVision'
```

## Quick Start — Python Examples

### Face Detection

```python
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = '/absolute/path/to/blaze_face_short_range.tflite'
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.FaceDetectorOptions(base_options=base_options)
detector = vision.FaceDetector.create_from_options(options)

image = mp.Image.create_from_file('photo.jpg')
result = detector.detect(image)
for detection in result.detections:
    bbox = detection.bounding_box
    print(f"Face at x={bbox.origin_x}, y={bbox.origin_y}, "
          f"w={bbox.width}, h={bbox.height}, "
          f"score={detection.categories[0].score}")
```

### Hand Landmark Detection

```python
model_path = '/path/to/hand_landmarker.task'
options = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=model_path),
    num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

image = mp.Image.create_from_file('hands.jpg')
result = detector.detect(image)
for hand_landmarks in result.hand_landmarks:
    for lm in hand_landmarks:
        print(f"Landmark: x={lm.x}, y={lm.y}, z={lm.z}")
```

### Pose Landmark Detection

```python
model_path = '/path/to/pose_landmarker_lite.task'
options = vision.PoseLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=model_path))
detector = vision.PoseLandmarker.create_from_options(options)

image = mp.Image.create_from_file('person.jpg')
result = detector.detect(image)
# result.pose_landmarks is a list of NormalizedLandmark lists (33 landmarks each)
# result.pose_world_landmarks provides 3D world coordinates
```

### Object Detection

```python
model_path = '/path/to/efficientdet_lite0.tflite'
options = vision.ObjectDetectorOptions(
    base_options=python.BaseOptions(model_asset_path=model_path),
    max_results=5)
detector = vision.ObjectDetector.create_from_options(options)

image = mp.Image.create_from_file('scene.jpg')
result = detector.detect(image)
for detection in result.detections:
    print(f"Class: {detection.categories[0].category_name}, "
          f"BBox: {detection.bounding_box}")
```

### Text Classification

```python
from mediapipe.tasks.python import text

model_path = '/path/to/text_classifier.tflite'
options = text.TextClassifierOptions(
    base_options=python.BaseOptions(model_asset_path=model_path))
classifier = text.TextClassifier.create_from_options(options)

result = classifier.classify("I absolutely loved this movie!")
for category in result.classifications[0].categories:
    print(f"{category.category_name}: {category.score:.4f}")
```

### Drawing Landmarks on Images

```python
import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2

# ... detect landmarks ...

# Convert result landmarks to NormalizedLandmarkList
hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
hand_landmarks_proto.landmark.extend([
    landmark_pb2.NormalizedLandmark(x=lm.x, y=lm.y, z=lm.z)
    for lm in result.hand_landmarks[0]
])

# Draw on image
annotated = mp.solutions.drawing_utils.draw_landmarks(
    image_rgb,
    hand_landmarks_proto,
    mp.solutions.hands.HAND_CONNECTIONS,
    mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
    mp.solutions.drawing_styles.get_default_hand_connections_style()
)
```

## Vision Tasks

All vision tasks support three running modes: `IMAGE`, `VIDEO`, and `LIVE_STREAM`.

### FaceDetector
- **Models**: `blaze_face_short_range.tflite` (2m), `blaze_face_full_range.tflite` (5m)
- **Output**: bounding boxes with 6 keypoints (eyes, nose, mouth, ears)
- **Options**: `min_detection_confidence`, `min_suppression_threshold`

### FaceLandmarker
- **Models**: `face_landmarker.task` (478 3D landmarks), `face_landmarker_v2_with_blendshapes.task`
- **Output**: 478 face mesh landmarks, 52 blendshape scores, face transformation matrix
- **Options**: `num_faces`, `min_face_detection_confidence`, `min_tracking_confidence`, `output_face_blendshapes`, `output_facial_transformation_matrixes`

### HandLandmarker
- **Models**: `hand_landmarker.task`
- **Output**: 21 hand landmarks per hand, handedness classification (left/right), world landmarks
- **Options**: `num_hands`, `min_hand_detection_confidence`, `min_tracking_confidence`

### PoseLandmarker
- **Models**: `pose_landmarker_lite.task`, `pose_landmarker_full.task`, `pose_landmarker_heavy.task`
- **Output**: 33 body pose landmarks, world 3D landmarks, segmentation mask
- **Options**: `num_poses`, `min_pose_detection_confidence`, `min_tracking_confidence`, `output_segmentations`

### HolisticLandmarker
- **Models**: `holistic_landmarker.task`
- **Output**: Combined face (478), pose (33), and hand (21×2) landmarks simultaneously
- **Options**: `min_face_detection_confidence`, `min_pose_detection_confidence`, `min_hand_landmarks_confidence`, `output_face_blendshapes`

### GestureRecognizer
- **Models**: `gesture_recognizer.task`
- **Output**: Predefined gesture categories from hand landmarks (e.g., "Thumb_Up", "Victory", "Closed_Fist", "Open_Palm", "Pointing_Up", "ILoveYou")
- **Options**: `min_hand_detection_confidence`, `min_tracking_confidence`, `canned_gestures_classifier_options`

### ObjectDetector
- **Models**: `efficientdet_lite0.tflite` through `efficientdet_lite2.tflite` (COCO 80 classes)
- **Output**: Bounding boxes with category labels and scores
- **Options**: `max_results`, `score_threshold`, `category_allowlist`, `category_denylist`

### ImageClassifier
- **Models**: `efficientnet_lite0.tflite` through `efficientnet_lite4.tflite` (ImageNet 1k)
- **Output**: Classification category list with scores
- **Options**: `max_results`, `score_threshold`, `category_allowlist/denylist`

### ImageEmbedder
- **Models**: `mobilenet_v3_small.tflite`, `mobilenet_v3_large.tflite`
- **Output**: Feature embedding vectors (float or quantized) for similarity/comparison
- **Options**: `l2_normalize`, `quantize`

### ImageSegmenter
- **Models**: Various segmentation models (DeepLab, selfie segmenter, hair segmenter)
- **Output**: Category mask and/or confidence mask
- **Options**: `output_category_mask`, `output_confidence_masks`

### InteractiveSegmenter
- **Models**: `magic_touch.tflite`, `sam.tflite`
- **Output**: Segmentation mask for a user-specified region of interest (click/tap)
- **Options**: `output_category_mask`, `output_confidence_masks`

## Text Tasks

### TextClassifier
- **Models**: `text_classifier.tflite` (BERT-based), custom models via Model Maker
- **Output**: Classification categories with scores (sentiment, topic, etc.)
- **Options**: `max_results`, `score_threshold`, `category_allowlist/denylist`

### TextEmbedder
- **Models**: `universal_sentence_encoder.tflite`, `bert_embedder.tflite`
- **Output**: Text embedding vectors for semantic similarity, clustering, retrieval
- **Options**: `l2_normalize`, `quantize`

### LanguageDetector
- **Models**: `language_detector.tflite`
- **Output**: Detected language BCP-47 code(s) with probabilities (supports 110+ languages)

## Audio Tasks

### AudioClassifier
- **Models**: `yamnet.tflite` (521 audio event classes), custom models
- **Output**: Audio event classification with timestamps
- **Input**: Audio clips (mono, 16kHz sample rate) or streaming audio buffers
- **Options**: `max_results`, `score_threshold`, `category_allowlist/denylist`
- Supports `AUDIO_CLIPS` and `AUDIO_STREAM` running modes

## LLM Inference (GenAI)

MediaPipe includes on-device LLM inference via MediaPipe Tasks GenAI (as of v0.10.35):

- **JavaScript**: `@mediapipe/tasks-genai` package for web-based LLM inference
- **Android**: Tasks GenAI for NPU-accelerated on-device LLM
- **Python**: LLM converter utilities for blockwise int4 quantization, weight compression
- Supports configurable quantization policies and supervised round quantization (SRQ)

## MediaPipe Model Maker

Customize pre-trained models with your own data without ML expertise:

```bash
pip install mediapipe-model-maker
```

```python
from mediapipe_model_maker import text_classifier

data = text_classifier.Dataset.from_csv('reviews.csv')
model = text_classifier.create(data)
model.export_model()
```

Supports customization for text classification, object detection, image classification, and gesture recognition. Model Maker uses transfer learning with a few hundred examples.

## MediaPipe Framework (Low-Level)

For building custom on-device ML pipelines beyond pre-built solutions:

### Core Concepts
- **Packets** — Typed data containers (images, tensors, landmarks) that flow through the graph
- **Graphs** — Directed acyclic graphs of calculator nodes defining the pipeline topology
- **Calculators** — Processing nodes that consume input packets and produce output packets
- **Streams** — Named data pathways connecting calculator inputs/outputs
- **Side Packets** — Configuration data injected at graph initialization

### Graph Configuration (.pbtxt)
```protobuf
input_stream: "input_video"
output_stream: "output_video"

node {
  calculator: "ImageToTensorCalculator"
  input_stream: "IMAGE:input_video"
  output_stream: "TENSORS:image_tensor"
}

node {
  calculator: "InferenceCalculator"
  input_stream: "TENSORS:image_tensor"
  output_stream: "TENSORS:detection_tensors"
  options {
    [mediapipe.InferenceCalculatorOptions.ext] {
      model_path: "/path/to/model.tflite"
    }
  }
}
```

### Supported Platforms for Framework
- C++ (Bazel build system)
- Android (AAR, JNI bindings)
- iOS (framework)
- Desktop (Linux, macOS, Windows via C++)

The Framework is **not** available for Python or web — use MediaPipe Tasks/Solutions for those platforms.

## Model Management

### Downloading Models

Models are hosted at `https://storage.googleapis.com/mediapipe-models/`. Download programmatically:

```python
# Python: download helper (if available) or manual curl
# wget https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task
```

For production, download models ahead of time and bundle with your app.

### Model Path Requirements

- **Python**: Must use absolute paths for `model_asset_path`. Relative paths or `pathlib.Path` objects may fail.
- **Web**: Pass Wasm file URLs; must be served from same origin or with CORS headers.
- **Android**: Place `.task`/`.tflite` files in `src/main/assets/`.

## Common Patterns & Best Practices

### Running Modes
```python
# IMAGE mode — single image inference
options = vision.FaceDetectorOptions(
    base_options=python.BaseOptions(model_asset_path=model_path),
    running_mode=vision.RunningMode.IMAGE)

# VIDEO mode — frame sequence with timestamps
options = vision.FaceDetectorOptions(
    base_options=python.BaseOptions(model_asset_path=model_path),
    running_mode=vision.RunningMode.VIDEO)
# result = detector.detect_for_video(image, timestamp_ms)

# LIVE_STREAM mode — async callback-based for camera streams
def on_result(result, image, timestamp):
    pass  # handle result asynchronously

options = vision.FaceDetectorOptions(
    base_options=python.BaseOptions(model_asset_path=model_path),
    running_mode=vision.RunningMode.LIVE_STREAM,
    result_callback=on_result)
```

### Lazy Resource Cleanup
All task objects implement context manager protocol:
```python
with vision.FaceDetector.create_from_options(options) as detector:
    result = detector.detect(image)
# detector is automatically closed
```

### Image Handling
```python
import mediapipe as mp

# From file
image = mp.Image.create_from_file('photo.jpg')

# From numpy array (must be RGB, uint8)
import cv2
cv_image = cv2.imread('photo.jpg')
rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
```

### GPU Delegation
```python
base_options = python.BaseOptions(
    model_asset_path=model_path,
    delegate=python.BaseOptions.Delegate.GPU)  # or .CPU (default)
```

### Error Handling
```python
try:
    detector = vision.FaceDetector.create_from_options(options)
except Exception as e:
    print(f"Failed to create detector: {e}")
    # Common issues: wrong model path, incompatible model version, missing TFLite runtime
```

## Model Versions & Compatibility

- Model `.task` bundles (new format) vs legacy `.tflite` + metadata
- Task bundle encapsulates model + metadata + pre/post processing configs
- Always check model/task version compatibility — model versions are tied to specific MediaPipe SDK versions
- Download latest models from the official model hub

## Legacy Notes

- Legacy solutions (pre-2023) are deprecated as of March 2023 — use Tasks API instead
- Old `mp.solutions.hands`, `mp.solutions.pose`, `mp.solutions.face_mesh` APIs are legacy
- The new Tasks API (`mediapipe.tasks.python.vision.HandLandmarker`) supersedes legacy APIs
- Legacy code still in `mediapipe.solutions.*` namespace; use Tasks for new projects
- The Framework layer continues to be maintained for custom pipeline development

## Key Links

- **Official Docs**: https://developers.google.com/mediapipe
- **GitHub**: https://github.com/google-ai-edge/mediapipe
- **Samples**: https://github.com/google-ai-edge/mediapipe-samples
- **Model Hub**: https://developers.google.com/mediapipe/solutions/models
- **Studio**: https://mediapipe-studio.web.app
- **PyPI**: https://pypi.org/project/mediapipe/
- **Model Maker**: https://developers.google.com/mediapipe/solutions/model_maker
- **Paper**: https://arxiv.org/abs/1906.08172
