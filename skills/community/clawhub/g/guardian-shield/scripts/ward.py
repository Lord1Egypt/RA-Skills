"""
Guardian Shield — Ward ML Model

Tiny ONNX model (TF-IDF + Logistic Regression) for prompt injection detection.
Provides ML-based scoring as a second layer after regex pattern matching.

GPU support: CUDA > DirectML > CPU (auto-detected).

(c) Fallen Angel Systems LLC — All rights reserved.
"""

import os
import json
import logging
from typing import Optional, Tuple

logger = logging.getLogger("guardian-shield.ward")

# Model paths (relative to this file's directory)
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_MODEL_DIR = os.path.join(os.path.dirname(_SCRIPT_DIR), "models")
_MODEL_PATH = os.path.join(_MODEL_DIR, "ward.onnx")
_VOCAB_PATH = os.path.join(_MODEL_DIR, "ward_vocab.json")

# Lazy-loaded globals
_session = None
_vocab = None
_idf = None
_initialized = False


def _get_providers(gpu_enabled: str = "auto") -> list:
    """Get ONNX Runtime execution providers based on config."""
    try:
        import onnxruntime as ort
        available = ort.get_available_providers()
    except ImportError:
        return ["CPUExecutionProvider"]

    if gpu_enabled == "off":
        return ["CPUExecutionProvider"]

    preferred = []
    if "CUDAExecutionProvider" in available:
        preferred.append("CUDAExecutionProvider")
    if "DmlExecutionProvider" in available:
        preferred.append("DmlExecutionProvider")
    preferred.append("CPUExecutionProvider")
    return preferred


def _load_model(gpu_enabled: str = "auto") -> bool:
    """Load the Ward ONNX model and vocabulary. Returns True on success."""
    global _session, _vocab, _idf, _initialized

    if _initialized:
        return _session is not None

    _initialized = True

    if not os.path.exists(_MODEL_PATH):
        logger.warning(f"Ward model not found at {_MODEL_PATH}")
        return False

    if not os.path.exists(_VOCAB_PATH):
        logger.warning(f"Ward vocabulary not found at {_VOCAB_PATH}")
        return False

    try:
        import onnxruntime as ort

        providers = _get_providers(gpu_enabled)
        _session = ort.InferenceSession(_MODEL_PATH, providers=providers)

        with open(_VOCAB_PATH, "r") as f:
            vocab_data = json.load(f)
            _vocab = vocab_data.get("vocab", {})
            _idf = vocab_data.get("idf", {})

        provider_used = _session.get_providers()[0] if _session.get_providers() else "unknown"
        logger.info(f"Ward model loaded ({provider_used}), vocab size: {len(_vocab)}")
        return True

    except ImportError:
        logger.warning("onnxruntime not installed — Ward ML scanning disabled")
        return False
    except Exception as e:
        logger.error(f"Failed to load Ward model: {e}")
        return False


def _tfidf_vectorize(text: str) -> list:
    """Convert text to TF-IDF feature vector using stored vocabulary."""
    if not _vocab or not _idf:
        return []

    # Tokenize (simple whitespace + lowercase)
    text_lower = text.lower()
    tokens = text_lower.split()
    token_counts = {}
    for t in tokens:
        token_counts[t] = token_counts.get(t, 0) + 1

    total_tokens = len(tokens) if tokens else 1

    # Build feature vector in vocab order
    vector = [0.0] * len(_vocab)
    for token, count in token_counts.items():
        if token in _vocab:
            idx = _vocab[token]
            tf = count / total_tokens
            idf_val = _idf.get(token, 1.0)
            vector[idx] = tf * idf_val

    return vector


def is_available() -> bool:
    """Check if the Ward model can be loaded."""
    return os.path.exists(_MODEL_PATH) and os.path.exists(_VOCAB_PATH)


def predict(text: str, gpu_enabled: str = "auto") -> Optional[Tuple[bool, float]]:
    """
    Run Ward ML prediction on text.

    Returns:
        Tuple of (is_threat: bool, confidence: float 0.0-1.0)
        None if model is not available.
    """
    if not _load_model(gpu_enabled):
        return None

    try:
        import numpy as np

        vector = _tfidf_vectorize(text)
        if not vector:
            return None

        # Run inference
        input_name = _session.get_inputs()[0].name
        input_data = np.array([vector], dtype=np.float32)
        outputs = _session.run(None, {input_name: input_data})

        # Output[0] = predicted label, Output[1] = probabilities
        if len(outputs) >= 2:
            label = int(outputs[0][0])
            probabilities = outputs[1][0]
            # Class 1 = threat, Class 0 = benign
            if hasattr(probabilities, '__len__') and len(probabilities) >= 2:
                confidence = float(probabilities[1])  # threat probability
            else:
                confidence = float(probabilities) if label == 1 else 1.0 - float(probabilities)
        else:
            label = int(outputs[0][0])
            confidence = 1.0 if label == 1 else 0.0

        is_threat = label == 1
        return (is_threat, confidence)

    except Exception as e:
        logger.error(f"Ward prediction failed: {e}")
        return None


def get_model_info() -> dict:
    """Get Ward model metadata."""
    info = {
        "name": "Ward",
        "type": "TF-IDF + Logistic Regression",
        "format": "ONNX",
        "available": is_available(),
        "loaded": _session is not None,
    }

    if _vocab:
        info["vocab_size"] = len(_vocab)
    if _session:
        try:
            info["provider"] = _session.get_providers()[0]
        except Exception:
            pass

    return info
