#!/usr/bin/env python3
"""
video_analyzer.py — iaworker visual analysis engine
Analyzes images/videos for physical tasks and feeds results to step_engine.
"""

import argparse
import os
import sys
import yaml
import json
import cv2
import numpy as np
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field

try:
    import torch
    from transformers import pipeline, AutoImageProcessor, AutoModelForImageClassification
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from step_engine import StepEngine
from speaker import Speaker


@dataclass
class AnalysisResult:
    task_type: str
    detected_objects: list[str] = field(default_factory=list)
    anomalies: list[str] = field(default_factory=list)
    confidence: float = 0.0
    summary: str = ""
    frame_notes: list[str] = field(default_factory=list)


class VideoAnalyzer:
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.step_engine = StepEngine(lang=self.config.get("analysis", {}).get("lang", "en"))
        self.speaker = Speaker(
            lang=self.config.get("tts", {}).get("lang", "en"),
            tts_enabled=self.config.get("tts", {}).get("enabled", True)
        )
        self._setup_classifier()

    def _load_config(self, config_path: str = None) -> dict:
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        if Path(config_path).exists():
            with open(config_path) as f:
                return yaml.safe_load(f)
        return {
            "analysis": {"lang": "en", "frame_skip": 10, "confidence_threshold": 0.6},
            "tts": {"lang": "en", "enabled": True, "engine": "gtts", "speed": 1.0}
        }

    def _setup_classifier(self):
        if not TRANSFORMERS_AVAILABLE:
            print("[iaworker] Warning: transformers not installed. Using fallback heuristics.")
            self.classifier = None
            return
        try:
            self.classifier = pipeline(
                "image-classification",
                model="microsoft/resnet-50"
            )
        except Exception as e:
            print(f"[iaworker] Classifier init failed: {e}")
            self.classifier = None

    def analyze_image(self, image_path: str, task_type: str = "auto") -> AnalysisResult:
        if not PIL_AVAILABLE:
            raise RuntimeError("Pillow required: pip install pillow")
        img = Image.open(image_path).convert("RGB")
        result = AnalysisResult(task_type=task_type)
        if self.classifier:
            preds = self.classifier(img)
            result.detected_objects = [p["label"] for p in preds[:5]]
            result.confidence = preds[0]["score"]
        result.summary = self._llm_analyze_image(img, task_type)
        result.anomalies = self._extract_anomalies(result.summary)
        result.task_type = self._refine_task_type(task_type, result)
        return result

    def analyze_video(self, video_path: str, task_type: str = "auto",
                      frame_skip: int = 10, output_path: str = None) -> list[AnalysisResult]:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open video: {video_path}")
        results = []
        frame_idx = 0
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx % (frame_skip + 1) == 0:
                pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                result = AnalysisResult(task_type=task_type)
                result.summary = self._llm_analyze_image(pil_img, task_type)
                result.anomalies = self._extract_anomalies(result.summary)
                result.frame_notes.append(f"Frame {frame_count}: {result.summary[:100]}")
                results.append(result)
            frame_idx += 1
            frame_count += 1
        cap.release()
        merged = self._merge_results(results)
        merged.task_type = self._refine_task_type(task_type, merged)
        return [merged]

    def analyze_camera(self, camera_index: int = 0, task_type: str = "inspection",
                       live: bool = True, frame_skip: int = 30):
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open camera index {camera_index}")
        print("[iaworker] Camera active. Press Ctrl+C to stop.")
        try:
            frame_idx = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if frame_idx % (frame_skip + 1) == 0:
                    pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    result = AnalysisResult(task_type=task_type)
                    result.summary = self._llm_analyze_image(pil_img, task_type)
                    result.anomalies = self._extract_anomalies(result.summary)
                    print(f"[iaworker @ frame {frame_idx}] {result.summary}")
                frame_idx += 1
        finally:
            cap.release()

    def _llm_analyze_image(self, img: Image.Image, task_type: str) -> str:
        img_str = f"[Image {img.size}]"
        if task_type == "auto":
            return (
                f"{img_str} Visual analysis available. "
                "Please describe what you see in the image and I will generate repair/debug steps. "
                "Detected: general object. Anomalies: need closer inspection."
            )
        prompts = {
            "repair": f"{img_str} Analyze this image for damage, wear, or breakage. What needs repairing?",
            "debug": f"{img_str} Analyze for faults, misalignments, or malfunction indicators. What is broken?",
            "assembly": f"{img_str} Analyze parts and their relationships. What needs to be assembled?",
            "inspection": f"{img_str} Perform a thorough condition inspection. What is the state of this object?",
        }
        return prompts.get(task_type, f"{img_str} General analysis.")

    def _extract_anomalies(self, summary: str) -> list[str]:
        keywords = ["crack", "loose", "worn", "broken", "leak", "misaligned",
                    "rust", "damage", "fault", "missing", "disconnected", "overheating"]
        return [kw for kw in keywords if kw.lower() in summary.lower()]

    def _refine_task_type(self, task_type: str, result: AnalysisResult) -> str:
        if task_type != "auto":
            return task_type
        if result.anomalies:
            return "repair"
        return "inspection"

    def _merge_results(self, results: list[AnalysisResult]) -> AnalysisResult:
        all_objects = []
        all_anomalies = []
        all_notes = []
        for r in results:
            all_objects.extend(r.detected_objects)
            all_anomalies.extend(r.anomalies)
            all_notes.extend(r.frame_notes)
        merged = AnalysisResult(
            task_type=results[0].task_type if results else "inspection",
            detected_objects=list(dict.fromkeys(all_objects)),
            anomalies=list(dict.fromkeys(all_anomalies)),
            summary="; ".join(r.summary for r in results[:3]),
            frame_notes=all_notes
        )
        return merged

    def generate_and_deliver_steps(self, result: AnalysisResult, speak: bool = False,
                                    step_by_step: bool = False, output_path: str = None):
        steps = self.step_engine.generate(
            task_type=result.task_type,
            objects=result.detected_objects,
            anomalies=result.anomalies,
            context={"summary": result.summary}
        )
        if output_path:
            self._write_steps_md(steps, output_path)
        self.speaker.display_steps(steps, speak=speak, step_by_step=step_by_step)
        return steps

    def _write_steps_md(self, steps: list[dict], output_path: str):
        lines = [f"# Steps — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]
        for s in steps:
            lines.append(f"## Step {s['number']}: {s['title']}")
            lines.append(f"{s['description']}")
            lines.append(f"- **Tools:** {', '.join(s['tools'])}")
            lines.append(f"- **Time:** {s['time_estimate']} | **Difficulty:** {s['difficulty']}")
            if s["safety_warning"]:
                lines.append(f"- ⚠️ **Safety:** {s['safety_warning']}")
            if s["common_mistakes"]:
                lines.append(f"- ❌ **Avoid:** {', '.join(s['common_mistakes'])}")
            lines.append("")
        Path(output_path).write_text("\n".join(lines))
        print(f"[iaworker] Steps written to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="iaworker — Visual Analysis & Step Generation")
    parser.add_argument("--input", required=True,
                        help="Image path, video path, or 'camera'")
    parser.add_argument("--task", default="auto",
                        choices=["repair", "debug", "assembly", "inspection", "auto"])
    parser.add_argument("--lang", default="en", choices=["en", "zh"])
    parser.add_argument("--speak", action="store_true", help="Enable TTS spoken output")
    parser.add_argument("--step-by-step", action="store_true",
                        help="One step at a time, wait for confirmation")
    parser.add_argument("--live", action="store_true", help="Live camera mode")
    parser.add_argument("--output", help="Write steps to markdown file")
    parser.add_argument("--frame-skip", type=int, default=10, help="Frames to skip in video")
    parser.add_argument("--camera-index", type=int, default=0)
    parser.add_argument("--config", help="Path to config.yaml")
    parser.add_argument("--list-devices", action="store_true", help="List available cameras")
    args = parser.parse_args()

    analyzer = VideoAnalyzer(config_path=args.config)
    if args.lang != "en":
        analyzer.config["analysis"]["lang"] = args.lang
        analyzer.config["tts"]["lang"] = args.lang

    if args.list_devices:
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                print(f"Camera {i}: available")
                cap.release()
        return

    if args.input == "camera":
        if args.live:
            analyzer.analyze_camera(args.camera_index, args.task,
                                     live=True, frame_skip=args.frame_skip)
        else:
            print("[iaworker] Use --live for continuous camera analysis")
    elif args.input.endswith((".jpg", ".jpeg", ".png", ".webp")):
        result = analyzer.analyze_image(args.input, args.task)
        analyzer.generate_and_deliver_steps(result, speak=args.speak,
                                             step_by_step=args.step_by_step,
                                             output_path=args.output)
    elif args.input.endswith((".mp4", ".avi", ".mov", ".mkv")):
        results = analyzer.analyze_video(args.input, args.task,
                                          frame_skip=args.frame_skip, output_path=args.output)
        if results:
            analyzer.generate_and_deliver_steps(results[0], speak=args.speak,
                                                 step_by_step=args.step_by_step,
                                                 output_path=args.output)
    else:
        print(f"[iaworker] Unsupported input type: {args.input}")


if __name__ == "__main__":
    main()
