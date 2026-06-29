#!/usr/bin/env python3
"""
LYGO Video Resonance Engine
Extracts audio from video by analyzing motion and frame geometry over time.
Full source from https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html
"""

import cv2
import numpy as np
import soundfile as sf
import math
import argparse
from pathlib import Path
from resonance_engine import ResonanceEngine, PRESETS

class VideoResonanceEngine:
    def __init__(self, config=None):
        self.engine = ResonanceEngine(config)
    
    def process_video(self, video_path, output_path="video_soundscape.wav", 
                      fps=10, style="cinematic", duration_factor=1.0):
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
        
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        cap.release()
        
        if not frames:
            raise ValueError("No frames extracted from video.")
        
        src_fps = cap.get(cv2.CAP_PROP_FPS)
        if src_fps <= 0:
            src_fps = 30
        step = max(1, int(src_fps / fps))
        frames = frames[::step]
        actual_fps = src_fps / step
        
        print(f"Extracted {len(frames)} frames at ~{actual_fps:.1f} FPS")
        
        # Use last frame for feature extraction
        temp_img_path = "_temp_video_frame.jpg"
        cv2.imwrite(temp_img_path, frames[-1])
        
        # Get baseline config from preset
        config = dict(PRESETS.get(style, {}))
        config["duration"] = len(frames) / actual_fps * duration_factor
        config["verbose"] = True
        
        engine = ResonanceEngine(config)
        features = engine.analyze_image(temp_img_path)
        
        # Generate audio segment for each frame with interpolation
        sr = engine.config["sr"]
        duration = config["duration"]
        audio = np.zeros((int(sr * duration), 2), dtype=np.float32)
        
        # Motion detection (optical flow between frames)
        prev_gray = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        motion_scores = []
        
        for i, frame in enumerate(frames):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            motion_score = np.mean(mag)
            motion_scores.append(motion_score)
            prev_gray = gray
        
        # Normalize motion scores
        max_motion = max(motion_scores) if motion_scores else 1
        motion_scores = [m / max_motion for m in motion_scores]
        
        # Generate audio
        for i, frame in enumerate(frames):
            cv2.imwrite(temp_img_path, frame)
            seg_features = engine.analyze_image(temp_img_path)
            
            # Adjust parameters based on motion
            motion = motion_scores[i] if i < len(motion_scores) else 0
            config["glitch_vol"] = 0.032 + (motion * 0.08)
            config["noise_vol"] = 0.095 + (motion * 0.06)
            config["drone_vol"] = 0.075 - (motion * 0.03)
            
            engine.config.update(config)
            
            # Generate short segment
            seg_duration = 1.0 / actual_fps
            engine.config["duration"] = seg_duration
            seg_audio = np.zeros((int(sr * seg_duration), 2), dtype=np.float32)
            
            # Simplified segment synthesis (reuse analyze/synthesize)
            # For efficiency, we use the full synthesis but only for a short duration
            engine.synthesize(seg_features, "_temp_seg.wav")
            seg, _ = sf.read("_temp_seg.wav")
            
            # Place in main audio
            start_idx = int(i * sr / actual_fps)
            end_idx = min(start_idx + len(seg), len(audio))
            seg_len = end_idx - start_idx
            audio[start_idx:end_idx] += seg[:seg_len]
        
        # Cleanup
        if Path("_temp_video_frame.jpg").exists():
            Path("_temp_video_frame.jpg").unlink()
        if Path("_temp_seg.wav").exists():
            Path("_temp_seg.wav").unlink()
        
        # Normalize and save
        peak = np.max(np.abs(audio))
        if peak > 0:
            audio = audio / peak * 0.97
        sf.write(output_path, audio, sr)
        print(f"✓ Video soundscape saved: {output_path}")
        return output_path


def main():
    parser = argparse.ArgumentParser(
        description="LYGO Video Resonance — Turn a video into a motion-driven soundscape"
    )
    parser.add_argument("video", help="Input video path")
    parser.add_argument("-o", "--output", default="video_soundscape.wav", help="Output .wav path")
    parser.add_argument("--fps", type=float, default=10, help="Frames per second to extract")
    parser.add_argument("--style", choices=list(PRESETS.keys()), default="cinematic",
                        help="Artistic preset")
    parser.add_argument("--duration-factor", type=float, default=1.0,
                        help="Multiply final duration (e.g., 0.5 for half speed, 2.0 for double)")
    args = parser.parse_args()
    
    engine = VideoResonanceEngine()
    engine.process_video(
        args.video,
        output_path=args.output,
        fps=args.fps,
        style=args.style,
        duration_factor=args.duration_factor
    )


if __name__ == "__main__":
    main()