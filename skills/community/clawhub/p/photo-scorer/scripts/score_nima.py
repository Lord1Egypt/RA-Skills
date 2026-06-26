#!/usr/bin/env python3
"""
NIMA (Neural Image Assessment) - Detailed Quality Analysis Script
Uses MobileNet + Keras/TensorFlow backbone.
Model path: Set via MODEL_DIR environment variable, or default to F:/software/skill/aesthetic-scorer/models/neural-image-assessment
Base Weight: 55% (dynamic, adjustable 30%-55% based on score consensus)
"""

import os
import sys
import json
import argparse
import numpy as np

# ── Model location ─────────────────────────────────────────────────────────────
# Override via environment variable: set AESTHETIC_SCORER_NIMA_DIR
_DEFAULT_MODEL_DIR = r"F:\software\skill\aesthetic-scorer\models\neural-image-assessment"
MODEL_DIR = os.environ.get("AESTHETIC_SCORER_NIMA_DIR", _DEFAULT_MODEL_DIR)
DEFAULT_WEIGHTS = os.path.join(MODEL_DIR, "weights", "mobilenet_weights.h5")


def _get_keras():
    """
    Return (Model, Dense, Dropout, MobileNet, preprocess_input, load_img, img_to_array).
    Tries tf_keras first (Keras 2 compatible API), then tensorflow.keras, then standalone keras.
    """
    # tf_keras preserves the Keras 2 API under TF 2.x
    try:
        import tf_keras as keras2
        from tf_keras import Model
        from tf_keras.layers import Dense, Dropout
        from tf_keras.applications.mobilenet import MobileNet, preprocess_input
        from tf_keras.preprocessing.image import load_img, img_to_array
        return Model, Dense, Dropout, MobileNet, preprocess_input, load_img, img_to_array
    except Exception:
        pass

    # Standard tensorflow.keras
    try:
        from tensorflow.keras.models import Model
        from tensorflow.keras.layers import Dense, Dropout
        from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input
        from tensorflow.keras.preprocessing.image import load_img, img_to_array
        return Model, Dense, Dropout, MobileNet, preprocess_input, load_img, img_to_array
    except Exception:
        pass

    raise ImportError("Cannot import Keras. Install tf_keras or tensorflow.")


def build_nima_model(weights_path=None):
    """Build NIMA MobileNet model and load weights."""
    try:
        Model, Dense, Dropout, MobileNet, preprocess_input, load_img, img_to_array = _get_keras()
    except ImportError as e:
        print(f"Error: {e}")
        sys.exit(1)

    wp = weights_path or DEFAULT_WEIGHTS
    if not os.path.exists(wp):
        print(f"Error: NIMA weight file not found: {wp}")
        sys.exit(1)

    # NIMA MobileNet architecture (same as evaluate_mobilenet.py)
    base_model = MobileNet((None, None, 3), alpha=1, include_top=False, pooling="avg", weights=None)
    x = Dropout(0.75)(base_model.output)
    x = Dense(10, activation="softmax")(x)
    model = Model(base_model.input, x)
    model.load_weights(wp)
    return model


def predict_with_nima(image_path, model_path=None):
    """
    Predict aesthetic score using NIMA MobileNet model.
    Returns dict with 'mean_score' key (1-10 scale).
    """
    if not os.path.exists(image_path):
        print(f"Error: Image not found: {image_path}")
        return None

    try:
        Model, Dense, Dropout, MobileNet, preprocess_input, load_img, img_to_array = _get_keras()
    except ImportError as e:
        print(f"Error: TensorFlow/Keras not installed.\n{e}")
        return None

    from PIL import Image as PILImage

    # Build & load model
    model = build_nima_model(model_path)

    # Load and preprocess image (NIMA uses variable input size)
    pil_img = PILImage.open(image_path).convert("RGB")
    img_size = pil_img.size  # (W, H)

    img = load_img(image_path)
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # Predict probability distribution over 10 score classes (1-10)
    scores_dist = model.predict(x, batch_size=1, verbose=0)[0]  # shape: (10,)

    # Mean and std
    score_labels = np.arange(1, 11, dtype=np.float32)
    mean_score = float(np.sum(scores_dist * score_labels))
    std_score = float(np.sqrt(np.sum(scores_dist * (score_labels - mean_score) ** 2)))

    # Quality breakdown
    quality_breakdown = {
        "excellent": float(np.sum(scores_dist[8:10])),   # scores 9-10
        "good":      float(np.sum(scores_dist[5:8])),    # scores 6-8
        "fair":      float(np.sum(scores_dist[3:5])),    # scores 4-5
        "poor":      float(np.sum(scores_dist[0:3])),    # scores 1-3
    }

    return {
        "model": "nima-mobilenet",
        "mean_score": mean_score,
        "std_score": std_score,
        "probability_distribution": scores_dist.tolist(),
        "quality_breakdown": quality_breakdown,
        "image_path": image_path,
        "image_size": list(img_size),
    }


def main():
    parser = argparse.ArgumentParser(description="NIMA MobileNet quality analysis")
    parser.add_argument("image_path", type=str, help="Path to the image file")
    parser.add_argument("--model", type=str, default=None, help="Custom .h5 weights path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    result = predict_with_nima(args.image_path, args.model)
    if result is None:
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        qb = result["quality_breakdown"]
        print(f"\n{'='*70}")
        print("QUALITY ANALYSIS (NIMA - Neural Image Assessment, MobileNet)")
        print(f"{'='*70}")
        print(f"Mean Score : {result['mean_score']:.3f}/10")
        print(f"Std Dev    : {result['std_score']:.3f}")
        print(f"\nQuality Distribution:")
        print(f"  Excellent (9-10): {qb['excellent']*100:.1f}%")
        print(f"  Good      (6-8) : {qb['good']*100:.1f}%")
        print(f"  Fair      (4-5) : {qb['fair']*100:.1f}%")
        print(f"  Poor      (1-3) : {qb['poor']*100:.1f}%")
        print(f"\nImage  : {result['image_path']}")
        print(f"Size   : {result['image_size'][0]}x{result['image_size'][1]}")
        print(f"Weights: {DEFAULT_WEIGHTS}")
        print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
