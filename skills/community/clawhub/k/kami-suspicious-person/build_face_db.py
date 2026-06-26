"""
Face Database Builder (ONNX version)
Extracts face embeddings from face_db/<person_name>/xxx.jpg directory structure,
generates face_db/face_db.pkl cache file for faster subsequent loading.

Uses SCRFD (det_10g.onnx) + ArcFace (w600k_r50.onnx) directly via onnxruntime.
No insightface package dependency.

Usage:
  .venv/bin/python build_face_db.py --face_db ./face_db
"""

import cv2
import numpy as np
import os
import sys
import pickle
import argparse
from pathlib import Path

script_dir = os.path.dirname(os.path.abspath(__file__))

# Import the ONNX-based face processor from the main script
from suspicious_person_detector import SCRFDDetector, ArcFaceEmbedder, align_face


def main():
    parser = argparse.ArgumentParser(description="Build face embedding database (ONNX)")
    parser.add_argument("--face_db", type=str, default=os.path.join(script_dir, "face_db"),
                        help="Face database directory, structure: <dir>/<person_name>/xxx.jpg")
    parser.add_argument("--det_model", type=str, default=os.path.join(script_dir, "models", "det_10g.onnx"),
                        help="SCRFD detection model path")
    parser.add_argument("--rec_model", type=str, default=os.path.join(script_dir, "models", "w600k_r50.onnx"),
                        help="ArcFace recognition model path")
    args = parser.parse_args()

    db_path = args.face_db
    if not os.path.isdir(db_path):
        print(f"ERROR: Directory not found: {db_path}")
        sys.exit(1)

    detector = SCRFDDetector(args.det_model)
    embedder = ArcFaceEmbedder(args.rec_model)

    records = []
    for person_dir in sorted(Path(db_path).iterdir()):
        if not person_dir.is_dir():
            continue
        person_name = person_dir.name
        for img_file in person_dir.glob("*"):
            if img_file.suffix.lower() not in (".jpg", ".jpeg", ".png", ".bmp"):
                continue
            img = cv2.imread(str(img_file))
            if img is None:
                print(f"  SKIP (cannot read): {img_file}")
                continue
            det, kpss = detector.detect(img)
            if len(det) == 0:
                print(f"  SKIP (no face detected): {img_file}")
                continue
            # Take the largest face
            areas = (det[:, 2] - det[:, 0]) * (det[:, 3] - det[:, 1])
            best_idx = np.argmax(areas)
            landmarks = kpss[best_idx]
            emb = embedder.get_embedding(img, landmarks)
            records.append({"name": person_name, "embedding": emb})
            print(f"  OK: {person_name} <- {img_file.name}")

    if not records:
        print("WARNING: No face embeddings extracted")
        sys.exit(0)

    pkl_path = os.path.join(db_path, "face_db.pkl")
    with open(pkl_path, "wb") as f:
        pickle.dump(records, f)

    print(f"\nDone! {len(records)} records saved to: {pkl_path}")


if __name__ == "__main__":
    main()
