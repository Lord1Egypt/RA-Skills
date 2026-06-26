#!/usr/bin/env python3
"""
Guardian Shield — Ward Model Training

Trains the Ward model (TF-IDF + Logistic Regression) on the Spectre dataset,
then exports to ONNX format.

Run on a machine with the training data:
  python3 train_ward.py --data /path/to/training/data --output ../models/

Expects training data in the same format as Spectre:
  - attacks.jsonl: {"text": "...", "label": 1}
  - benign.jsonl: {"text": "...", "label": 0}

Or a combined file:
  - training_data.jsonl: {"text": "...", "label": 0|1}

(c) Fallen Angel Systems LLC — All rights reserved.
"""

import os
import sys
import json
import argparse
import logging
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ward-trainer")


def load_data(data_dir: str) -> tuple:
    """Load training data from directory."""
    texts = []
    labels = []

    data_path = Path(data_dir)

    # Try combined file first
    combined = data_path / "training_data.jsonl"
    if combined.exists():
        logger.info(f"Loading combined data from {combined}")
        with open(combined) as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    texts.append(item["text"])
                    labels.append(item["label"])
        return texts, labels

    # Try separate files
    for fname, label in [("attacks.jsonl", 1), ("benign.jsonl", 0)]:
        fpath = data_path / fname
        if fpath.exists():
            logger.info(f"Loading {fname}")
            with open(fpath) as f:
                for line in f:
                    if line.strip():
                        item = json.loads(line)
                        texts.append(item.get("text", item.get("prompt", "")))
                        labels.append(label)

    # Also try CSV format
    for fname in ["train.csv", "training.csv"]:
        fpath = data_path / fname
        if fpath.exists():
            import csv
            logger.info(f"Loading {fname}")
            with open(fpath) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    texts.append(row.get("text", row.get("prompt", "")))
                    labels.append(int(row.get("label", row.get("is_attack", 0))))

    return texts, labels


def train_and_export(texts: list, labels: list, output_dir: str, max_features: int = 10000):
    """Train TF-IDF + LogReg pipeline and export to ONNX."""
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, accuracy_score, f1_score

    logger.info(f"Dataset: {len(texts)} samples ({sum(labels)} attacks, {len(labels) - sum(labels)} benign)")

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.15, random_state=42, stratify=labels
    )
    logger.info(f"Train: {len(X_train)} | Test: {len(X_test)}")

    # TF-IDF
    logger.info(f"Fitting TF-IDF (max_features={max_features})...")
    tfidf = TfidfVectorizer(
        max_features=max_features,
        ngram_range=(1, 2),
        sublinear_tf=True,
        strip_accents="unicode",
        lowercase=True,
    )
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)
    logger.info(f"Vocabulary size: {len(tfidf.vocabulary_)}")

    # Train LogReg
    logger.info("Training Logistic Regression...")
    start = time.time()
    model = LogisticRegression(
        max_iter=1000,
        C=1.0,
        solver="liblinear",
        class_weight="balanced",
    )
    model.fit(X_train_tfidf, y_train)
    train_time = time.time() - start
    logger.info(f"Training done in {train_time:.1f}s")

    # Evaluate
    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    logger.info(f"Accuracy: {accuracy:.4f} | F1: {f1:.4f}")
    print("\n" + classification_report(y_test, y_pred, target_names=["benign", "attack"]))

    # Export to ONNX
    logger.info("Exporting to ONNX...")
    try:
        from skl2onnx import to_onnx
        from skl2onnx.common.data_types import FloatTensorType

        # We need to export with float input matching our TF-IDF output
        initial_type = [("X", FloatTensorType([None, X_train_tfidf.shape[1]]))]
        onnx_model = to_onnx(model, initial_types=initial_type)

        os.makedirs(output_dir, exist_ok=True)
        model_path = os.path.join(output_dir, "ward.onnx")
        with open(model_path, "wb") as f:
            f.write(onnx_model.SerializeToString())
        logger.info(f"ONNX model saved: {model_path} ({os.path.getsize(model_path) / 1024:.1f}KB)")

    except ImportError:
        logger.error("skl2onnx not installed! Run: pip install skl2onnx")
        logger.info("Saving sklearn model as fallback...")
        import pickle
        fallback_path = os.path.join(output_dir, "ward_sklearn.pkl")
        with open(fallback_path, "wb") as f:
            pickle.dump(model, f)
        logger.info(f"Fallback model saved: {fallback_path}")

    # Save vocabulary + IDF weights (needed for inference)
    vocab_path = os.path.join(output_dir, "ward_vocab.json")
    # Convert numpy types to native Python for JSON serialization
    vocab_dict = {k: int(v) for k, v in tfidf.vocabulary_.items()}
    vocab_data = {
        "vocab": vocab_dict,
        "idf": dict(zip(tfidf.get_feature_names_out().tolist(), tfidf.idf_.tolist())),
        "max_features": max_features,
        "ngram_range": [1, 2],
        "accuracy": accuracy,
        "f1": f1,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
    }
    with open(vocab_path, "w") as f:
        json.dump(vocab_data, f, indent=2)
    logger.info(f"Vocabulary saved: {vocab_path} ({os.path.getsize(vocab_path) / 1024:.1f}KB)")

    # Quick ONNX verify
    try:
        import onnxruntime as ort
        sess = ort.InferenceSession(model_path)
        test_input = X_test_tfidf[0].toarray().astype(np.float32)
        result = sess.run(None, {sess.get_inputs()[0].name: test_input})
        logger.info(f"ONNX verification: label={result[0][0]}, probs={result[1][0]}")
    except Exception as e:
        logger.warning(f"ONNX verification skipped: {e}")

    return accuracy, f1


def main():
    parser = argparse.ArgumentParser(description="Train Ward model for Guardian Shield")
    parser.add_argument("--data", required=True, help="Path to training data directory")
    parser.add_argument("--output", default="../models", help="Output directory for model files")
    parser.add_argument("--max-features", type=int, default=10000, help="Max TF-IDF features")
    args = parser.parse_args()

    texts, labels = load_data(args.data)
    if not texts:
        logger.error(f"No training data found in {args.data}")
        sys.exit(1)

    train_and_export(texts, labels, args.output, args.max_features)


if __name__ == "__main__":
    main()
