import os
import io
import wave
import numpy as np
import librosa
import soundfile as sf
from sklearn.mixture import GaussianMixture
import joblib

MODEL_PATH = "/home/manos/.openclaw/workspace/voice/manos_voice_model.joblib"

def extract_features(audio_data):
    """
    Extract 39-dimensional MFCC features (13 MFCCs + delta + delta-delta).
    Accepts a filepath (str) or raw WAV bytes.
    """
    try:
        if isinstance(audio_data, bytes):
            # Load raw WAV bytes using soundfile
            data, sr = sf.read(io.BytesIO(audio_data))
        else:
            # Load from file
            data, sr = librosa.load(audio_data, sr=16000)
            
        # Ensure mono
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)

        # Extract 13 MFCCs
        mfccs = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=13)
        delta = librosa.feature.delta(mfccs)
        delta2 = librosa.feature.delta(mfccs, order=2)
        
        # Concatenate into a (frames, 39) feature matrix
        features = np.vstack([mfccs, delta, delta2]).T
        return features
    except Exception as e:
        print(f"Error extracting features: {e}")
        return None

def enroll_speaker(audio_paths, model_out_path=MODEL_PATH):
    """
    Train a GMM model on enrollment audio clips.
    """
    all_features = []
    for path in audio_paths:
        features = extract_features(path)
        if features is not None:
            all_features.append(features)
            
    if not all_features:
        raise ValueError("No features extracted from the enrollment audio.")
        
    # Combine features from all files
    X = np.vstack(all_features)
    
    # Train GMM (16 components are perfect for speaker verification)
    gmm = GaussianMixture(n_components=16, covariance_type='diag', max_iter=200, random_state=42)
    gmm.fit(X)
    
    # Calculate baseline scores to calibrate the safety threshold
    scores = gmm.score_samples(X)
    threshold = np.mean(scores) - (2.5 * np.std(scores)) # 2.5 standard deviations margin
    
    # Save model and calibrated threshold
    model_data = {
        "gmm": gmm,
        "threshold": threshold
    }
    joblib.dump(model_data, model_out_path)
    print(f"✅ Enrollment complete! Model saved to {model_out_path}")
    print(f"📊 Calibrated safety threshold: {threshold:.2f}")
    return threshold

def verify_speaker(audio_bytes, model_path=MODEL_PATH):
    """
    Verify if the spoken audio matches the enrolled GMM model.
    Returns (is_verified, score, threshold)
    """
    if not os.path.exists(model_path):
        # If no model is trained yet, fail-safe to True (do not lock out)
        return True, 0.0, 0.0
        
    try:
        # Load GMM and threshold
        model_data = joblib.load(model_path)
        gmm = model_data["gmm"]
        threshold = model_data["threshold"]
        
        # Extract features from newly spoken command
        features = extract_features(audio_bytes)
        if features is None or len(features) == 0:
            return False, -999.0, threshold
            
        # Compute overall average log-likelihood score
        score = gmm.score(features)
        is_verified = score >= threshold
        return is_verified, score, threshold
    except Exception as e:
        print(f"Verification error: {e}")
        return True, 0.0, 0.0 # Fail-safe to true on system errors
