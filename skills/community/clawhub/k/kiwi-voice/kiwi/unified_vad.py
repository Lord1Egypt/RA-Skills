"""
Unified VAD Pipeline - Single Voice Activity Detection module

Combines:
- Silero VAD (neural network)
- Energy-based VAD (volume)
- Whisper VAD (no_speech_prob from transcription)

Provides a unified interface with confidence score.
"""

import numpy as np
import time
from typing import Optional, Callable, Tuple
from dataclasses import dataclass
from collections import deque

from kiwi.utils import kiwi_log


@dataclass
class VADResult:
    """VAD analysis result."""
    is_speech: bool
    confidence: float  # 0.0 - 1.0
    source: str        # 'silero', 'energy', 'whisper', 'combined'
    volume: float      # RMS volume
    raw_scores: dict   # Raw scores from all sources


class UnifiedVAD:
    """
    Unified VAD pipeline.

    Uses multiple sources and combines them
    for more accurate speech detection.
    """
    
    def __init__(
        self,
        sample_rate: int = 16000,
        # Silero VAD settings
        silero_threshold: float = 0.5,
        silero_min_speech_duration_ms: int = 250,
        silero_min_silence_duration_ms: int = 100,
        # Energy VAD settings
        energy_threshold_multiplier: float = 1.5,
        energy_min_threshold: float = 0.008,
        energy_max_threshold: float = 0.1,
        # Combining
        use_silero: bool = True,
        use_energy: bool = True,
        use_whisper: bool = True,
        # Smoothing
        smoothing_window: int = 5,
    ):
        self.sample_rate = sample_rate
        
        # Настройки Silero
        self.silero_threshold = silero_threshold
        self.silero_min_speech_duration_ms = silero_min_speech_duration_ms
        self.silero_min_silence_duration_ms = silero_min_silence_duration_ms
        
        # Настройки energy
        self.energy_threshold_multiplier = energy_threshold_multiplier
        self.energy_min_threshold = energy_min_threshold
        self.energy_max_threshold = energy_max_threshold
        
        # Включение/выключение источников
        self.use_silero = use_silero
        self.use_energy = use_energy
        self.use_whisper = use_whisper
        
        # Smoothing
        self.smoothing_window = smoothing_window
        self._confidence_history = deque(maxlen=smoothing_window)

        # Silero model (lazy loading)
        self._silero_model = None
        self._silero_available = False
        
        # Adaptive noise threshold
        self._noise_floor = 0.0
        self._adaptive_threshold = energy_min_threshold
        self._noise_history = deque(maxlen=100)  # ~3 seconds at 30ms chunks

        # Statistics
        self._total_calls = 0
        self._speech_detected_count = 0
        self._last_call_time = 0.0
        
    def _load_silero(self) -> bool:
        """Lazy load Silero VAD."""
        if self._silero_model is not None:
            return self._silero_available
        
        try:
            import torch
            self._silero_model, utils = torch.hub.load(
                repo_or_dir='snakers4/silero-vad',
                model='silero_vad',
                force_reload=False,
                onnx=True,
            )
            self._silero_available = True
            kiwi_log("VAD", "Silero VAD loaded (ONNX)")
            return True
        except Exception as e:
            kiwi_log("VAD", f"Silero not available: {e}", level="WARNING")
            self._silero_available = False
            return False
    
    def calibrate_noise_floor(self, audio_chunks: list):
        """Calibrate noise threshold from provided chunks."""
        if not audio_chunks:
            return
        
        volumes = [self._calculate_rms(chunk) for chunk in audio_chunks]
        self._noise_floor = np.median(volumes)
        self._adaptive_threshold = max(
            self._noise_floor * self.energy_threshold_multiplier,
            self.energy_min_threshold
        )
        kiwi_log("VAD", f"Noise floor calibrated: {self._noise_floor:.6f}, "
              f"threshold: {self._adaptive_threshold:.6f}")
    
    def _calculate_rms(self, audio: np.ndarray) -> float:
        """Calculate RMS volume."""
        if len(audio) == 0:
            return 0.0
        return np.sqrt(np.mean(audio ** 2))
    
    def _silero_check(self, audio: np.ndarray) -> Tuple[bool, float]:
        """Check via Silero VAD."""
        if not self.use_silero or not self._load_silero():
            return False, 0.0
        
        try:
            import torch
            
            # Silero expects tensor
            audio_tensor = torch.from_numpy(audio).float()
            
            # Minimum length for Silero - 512 samples
            if len(audio_tensor) < 512:
                return False, 0.0
            
            # Get confidence
            with torch.no_grad():
                confidence = self._silero_model(audio_tensor, self.sample_rate).item()
            
            is_speech = confidence > self.silero_threshold
            return is_speech, confidence
            
        except Exception as e:
            kiwi_log("VAD", f"Silero error: {e}", level="ERROR")
            return False, 0.0
    
    def _energy_check(self, audio: np.ndarray) -> Tuple[bool, float]:
        """Check via energy-based VAD."""
        if not self.use_energy:
            return False, 0.0
        
        volume = self._calculate_rms(audio)
        
        # Update adaptive threshold
        self._noise_history.append(volume)
        if len(self._noise_history) >= 50:
            # Recalculate threshold every 50 chunks
            self._noise_floor = np.percentile(self._noise_history, 10)
            self._adaptive_threshold = max(
                self._noise_floor * self.energy_threshold_multiplier,
                self.energy_min_threshold
            )
        
        # Check threshold
        is_speech = volume > self._adaptive_threshold
        
        # Normalize confidence
        if is_speech:
            # Louder = higher confidence (up to 1.0)
            confidence = min(volume / (self._adaptive_threshold * 2), 1.0)
        else:
            # Quieter = more confident it is not speech
            confidence = max(0.0, 1.0 - (volume / self._adaptive_threshold))
        
        return is_speech, confidence
    
    def process_whisper_result(
        self,
        no_speech_prob: float,
        avg_logprob: float,
        text: str
    ) -> Tuple[bool, float]:
        """
        Обработка VAD информации из Whisper.
        
        Returns:
            (is_speech, confidence)
        """
        if not self.use_whisper:
            return True, 1.0
        
        # no_speech_prob > 0.6 - most likely no speech
        # avg_logprob < -1.0 - hallucination
        
        speech_confidence = 1.0 - no_speech_prob
        
        # Account for logprob
        if avg_logprob < -1.0:
            speech_confidence *= 0.5
        elif avg_logprob > -0.5:
            speech_confidence = min(1.0, speech_confidence * 1.2)
        
        is_speech = speech_confidence > 0.5
        return is_speech, speech_confidence
    
    def is_speech(
        self,
        audio: np.ndarray,
        whisper_context: Optional[dict] = None
    ) -> VADResult:
        """
        Unified speech detection method.

        Args:
            audio: numpy array with audio
            whisper_context: optional Whisper results for improvement

        Returns:
            VADResult with combined result
        """
        self._total_calls += 1
        self._last_call_time = time.time()
        
        raw_scores = {}
        volume = self._calculate_rms(audio)
        
        # Silero
        silero_speech, silero_conf = self._silero_check(audio)
        raw_scores['silero'] = {
            'is_speech': silero_speech,
            'confidence': silero_conf
        }
        
        # Energy
        energy_speech, energy_conf = self._energy_check(audio)
        raw_scores['energy'] = {
            'is_speech': energy_speech,
            'confidence': energy_conf,
            'volume': volume,
            'threshold': self._adaptive_threshold
        }
        
        # Whisper (if provided)
        whisper_speech, whisper_conf = True, 1.0
        if whisper_context:
            whisper_speech, whisper_conf = self.process_whisper_result(
                whisper_context.get('no_speech_prob', 0.0),
                whisper_context.get('avg_logprob', 0.0),
                whisper_context.get('text', '')
            )
            raw_scores['whisper'] = {
                'is_speech': whisper_speech,
                'confidence': whisper_conf
            }
        
        # Combining results
        # Weights for different sources
        weights = {
            'silero': 0.4 if self.use_silero else 0.0,
            'energy': 0.3 if self.use_energy else 0.0,
            'whisper': 0.3 if self.use_whisper and whisper_context else 0.0
        }
        
        # Normalize weights
        total_weight = sum(weights.values())
        if total_weight > 0:
            weights = {k: v / total_weight for k, v in weights.items()}
        
        # Calculate weighted confidence
        combined_confidence = 0.0
        if weights.get('silero', 0) > 0:
            combined_confidence += weights['silero'] * silero_conf
        if weights.get('energy', 0) > 0:
            combined_confidence += weights['energy'] * energy_conf
        if weights.get('whisper', 0) > 0:
            combined_confidence += weights['whisper'] * whisper_conf
        
        # Voting
        votes = []
        if weights.get('silero', 0) > 0:
            votes.append(silero_speech)
        if weights.get('energy', 0) > 0:
            votes.append(energy_speech)
        if weights.get('whisper', 0) > 0:
            votes.append(whisper_speech)
        
        # Simple majority
        is_speech = sum(votes) >= len(votes) / 2 if votes else True
        
        # Smoothing
        self._confidence_history.append(combined_confidence)
        smoothed_confidence = np.mean(self._confidence_history)
        
        # Final decision with smoothing
        final_is_speech = smoothed_confidence > 0.5
        
        if final_is_speech:
            self._speech_detected_count += 1
        
        # Determine source
        if len(votes) > 1:
            source = 'combined'
        elif votes and silero_speech == votes[0]:
            source = 'silero'
        elif votes and energy_speech == votes[0]:
            source = 'energy'
        else:
            source = 'whisper'
        
        return VADResult(
            is_speech=final_is_speech,
            confidence=smoothed_confidence,
            source=source,
            volume=volume,
            raw_scores=raw_scores
        )
    
    def is_barge_in(
        self,
        audio: np.ndarray,
        kiwi_is_speaking: bool,
        tts_volume: float = 0.0
    ) -> bool:
        """
        Specialized method for barge-in detection.

        Args:
            audio: current audio chunk
            kiwi_is_speaking: whether Kiwi is currently speaking
            tts_volume: current TTS volume (for threshold adaptation)

        Returns:
            True if barge-in detected
        """
        if not kiwi_is_speaking:
            return False
        
        volume = self._calculate_rms(audio)
        
        # Adaptive threshold: louder TTS -> higher threshold
        barge_in_threshold = max(
            self._adaptive_threshold * 2.0,
            tts_volume * 0.5,
            0.02  # absolute minimum
        )
        
        # Check via VAD
        result = self.is_speech(audio)
        
        # Barge-in: volume above threshold AND VAD confident it is speech
        if volume > barge_in_threshold and result.confidence > 0.7:
            kiwi_log("VAD", f"Barge-in detected! "
                  f"vol={volume:.4f} > thr={barge_in_threshold:.4f}, "
                  f"conf={result.confidence:.2f}")
            return True
        
        return False
    
    def get_stats(self) -> dict:
        """Return VAD statistics."""
        uptime = time.time() - self._last_call_time if self._last_call_time > 0 else 0
        return {
            'total_calls': self._total_calls,
            'speech_detected': self._speech_detected_count,
            'speech_ratio': self._speech_detected_count / max(1, self._total_calls),
            'noise_floor': self._noise_floor,
            'adaptive_threshold': self._adaptive_threshold,
            'silero_available': self._silero_available,
        }
    
    def reset(self):
        """Reset VAD state."""
        self._confidence_history.clear()
        self._noise_history.clear()
        self._total_calls = 0
        self._speech_detected_count = 0
        
        # Reset Silero VAD hidden state
        if self._silero_model is not None and hasattr(self._silero_model, 'reset_states'):
            try:
                self._silero_model.reset_states()
                kiwi_log("VAD", "State reset (Silero hidden state cleared)")
            except Exception as e:
                kiwi_log("VAD", f"Error resetting Silero state: {e}", level="ERROR")
        else:
            kiwi_log("VAD", "State reset")
