#!/usr/bin/env python3
"""Real-time noise level monitor for Kiwi Voice."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import sounddevice as sd
import time

from kiwi.utils import kiwi_log

SAMPLE_RATE = 16000
CHUNK_DURATION = 0.1  # 100ms chunks for fast updates

def main():
    chunk_samples = int(CHUNK_DURATION * SAMPLE_RATE)
    
    kiwi_log("NOISE", "=" * 60)
    kiwi_log("NOISE", "Kiwi Voice - Noise Level Monitor")
    kiwi_log("NOISE", "=" * 60)
    kiwi_log("NOISE", f"Sample rate: {SAMPLE_RATE} Hz")
    kiwi_log("NOISE", f"Chunk duration: {CHUNK_DURATION}s ({chunk_samples} samples)")
    kiwi_log("NOISE", "Speak into your microphone to see levels...")
    kiwi_log("NOISE", "Press Ctrl+C to stop")
    
    # Bar settings
    BAR_WIDTH = 50
    MAX_DISPLAY_DB = 60  # Maximum dB to show on bar
    
    def audio_callback(indata, frames, time_info, status):
        if status:
            kiwi_log("NOISE", f"Status: {status}", level="WARNING")
        
        audio = indata[:, 0]
        
        # Calculate metrics
        peak = np.abs(audio).max()
        rms = np.sqrt(np.mean(audio**2))
        
        # Convert to dB (relative to full scale)
        peak_db = 20 * np.log10(peak + 1e-10)
        rms_db = 20 * np.log10(rms + 1e-10)
        
        # Create visual bar for peak
        bar_fill = int((peak_db + MAX_DISPLAY_DB) / MAX_DISPLAY_DB * BAR_WIDTH)
        bar_fill = max(0, min(BAR_WIDTH, bar_fill))
        
        # Color based on level
        if peak < 0.01:
            color = "\033[90m"  # Gray - silence
        elif peak < 0.1:
            color = "\033[32m"  # Green - normal speech
        elif peak < 0.5:
            color = "\033[33m"  # Yellow - loud
        else:
            color = "\033[31m"  # Red - clipping
        
        reset = "\033[0m"
        
        bar = "█" * bar_fill + "░" * (BAR_WIDTH - bar_fill)
        
        # Print on same line
        sys.stdout.write(f"\r{color}|{bar}|{reset} "
                        f"Peak: {peak_db:5.1f}dB ({peak:.4f})  "
                        f"RMS: {rms_db:5.1f}dB ({rms:.4f})  ")
        sys.stdout.flush()
    
    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype=np.float32,
            blocksize=chunk_samples,
            callback=audio_callback
        ):
            while True:
                time.sleep(0.01)
    except KeyboardInterrupt:
        kiwi_log("NOISE", "Stopped.")
    except Exception as e:
        kiwi_log("NOISE", f"Error: {e}", level="ERROR")

if __name__ == "__main__":
    main()
