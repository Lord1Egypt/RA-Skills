import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import onnxruntime as ort
import sys

def load_labels(csv_path):
    df = pd.read_csv(csv_path)
    tag_names = df["name"].tolist()
    general_indexes = list(range(4, len(tag_names)))
    return tag_names, general_indexes

def preprocess_image(image_path, size=448):
    image = Image.open(image_path).convert("RGB")
    image = np.array(image)
    image = image[:, :, ::-1]  # RGB to BGR
    h, w = image.shape[:2]
    max_side = max(h, w)
    pad_h = (max_side - h) // 2
    pad_w = (max_side - w) // 2
    image = cv2.copyMakeBorder(image, pad_h, max_side - h - pad_h, pad_w, max_side - w - pad_w, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    image = cv2.resize(image, (size, size), interpolation=cv2.INTER_AREA)
    image = image.astype(np.float32)
    return np.expand_dims(image, axis=0)

def run(target_dir):
    model_path = "/Users/mini/.openclaw/workspace/tools/wd14-tagger/models/model.onnx"
    csv_path = "/Users/mini/.openclaw/workspace/tools/wd14-tagger/models/selected_tags.csv"
    threshold = 0.35

    if not os.path.exists(target_dir):
        print(f"Directory {target_dir} not found")
        return

    ort_sess = ort.InferenceSession(model_path)
    input_name = ort_sess.get_inputs()[0].name
    label_names, general_idx = load_labels(csv_path)

    image_files = [f for f in os.listdir(target_dir) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
    print(f"Tagging {len(image_files)} images in {target_dir}...")

    for filename in image_files:
        img_path = os.path.join(target_dir, filename)
        txt_filename = os.path.splitext(filename)[0] + ".txt"
        txt_path = os.path.join(target_dir, txt_filename)

        try:
            input_data = preprocess_image(img_path)
            outputs = ort_sess.run(None, {input_name: input_data})[0][0]
            found_tags = [label_names[i].replace("_", " ") for i in general_idx if outputs[i] > threshold]
            with open(txt_path, "w") as f:
                f.write(", ".join(found_tags))
        except Exception as e:
            print(f"Error tagging {filename}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 tag_batch.py <directory>")
    else:
        run(sys.argv[1])
