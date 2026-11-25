"""Exercise the stream routing and interruption semantics on small, generated MP4s."""
import argparse
import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import qa

FF = "ffmpeg"
FP = "ffprobe"


class QualityChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="vlog-qa-test-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        (cls.root / "workspace_config.json").write_text(json.dumps({"executables": {"ffmpeg": FF, "ffprobe": FP}}), encoding="utf-8")

        def create(*args):
            subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-nostdin", "-n", *args],
                           check=True, cwd=cls.root, timeout=30)
        create("-f", "lavfi", "-i", "color=white:s=320x180:r=24:d=7",
               "-f", "lavfi", "-i", "sine=f=440:r=48000:d=7", "-f", "lavfi", "-i", "sine=f=880:r=48000:d=7",
               "-map", "0:v", "-map", "1:a", "-map", "2:a",
               "-vf", "drawbox=w=iw:h=ih:color=black:t=fill:enable='lt(t,0.75)+between(t,4,5)'",
               "-filter:a:0", "volume=0.25", "-filter:a:1", "volume=2", "-c:v", "libx264", "-threads:v", "2",
               "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
               "-disposition:a:0", "default", "-disposition:a:1", "0", "two-audio.mp4")
        for i, name in enumerate(("quiet", "loud")):
            create("-i", "two-audio.mp4", "-map", "0:v:0", "-map", f"0:a:{i}", "-c", "copy", name + ".mp4")
        create("-i", "two-audio.mp4", "-map", "0", "-c", "copy",
               "-disposition:a:0", "0", "-disposition:a:1", "default", "other-default.mp4")
        create("-i", "quiet.mp4", "-map", "0:v:0", "-c", "copy", "picture-only.mp4")
        create("-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-i", "picture-only.mp4", "-t", "7",
               "-map", "1:v:0", "-map", "0:a:0", "-c:v", "copy", "-c:a", "aac", "silence.mp4")
        create("-f", "lavfi", "-i", "color=white:s=160x90:r=24:d=7", "-c:v", "libx264", "-threads:v", "2", "preview.mp4")
        create("-i", "preview.mp4", "-i", "quiet.mp4", "-map", "0:v:0", "-map", "1:v:0", "-map", "1:a:0",
               "-c", "copy", "-disposition:v:0", "0", "-disposition:v:1", "default", "two-video.mp4")
        create("-f", "lavfi", "-i", "color=black:s=64x64:d=1", "-frames:v", "1", "-threads:v", "1", "cover.jpg")
        create("-i", "quiet.mp4", "-i", "cover.jpg", "-map", "0", "-map", "1:v:0", "-c", "copy",
               "-disposition:v:1", "attached_pic", "with-cover.mp4")

    def check_clip(self, clip, *options, expect=0):
        with tempfile.TemporaryDirectory(dir=self.root) as directory:
            out = Path(directory) / "report.json"
            args = ["--root", str(self.root), "--input", clip + ".mp4", "--out", str(out), *options]
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                code = qa.main(args)
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(code, expect, data)
            return data

    def test_single_pass_with_sound_without_sound_and_silence(self):
        for clip in ("quiet", "picture-only", "silence", "with-cover"):
            with self.subTest(clip=clip):
                result = self.check_clip(clip, "--expected-duration", "7")
                self.assertEqual(result["mode"], "single_pass")
                self.assertEqual(len(result["attempts"]), 1)
                self.assertTrue(result["duration_passed"] and result["decode_passed"] and result["signal_scan_passed"])
                self.assertFalse(result["actual_listening"] or result["continuous_playback"])
                spans = [(b["start"], b["end"]) for b in result["black_intervals_for_review"]]
                self.assertEqual(len(spans), 2)
                for actual, goal in zip(spans, ((0, .75), (4, 5 + 1 / 24))):
                    for measured, expected in zip(actual, goal):
                        self.assertAlmostEqual(measured, expected, places=4)
                self.assertEqual(result["mean_volume_dbfs"] is None, clip == "picture-only")
                if clip == "silence":
                    self.assertLessEqual(float(result["sample_peak_dbfs"]), -90)

    def test_audio_results_are_attributed_to_each_stream_and_default(self):
        quiet, loud = [self.check_clip(name)["sample_peak_dbfs"] for name in ("quiet", "loud")]
        self.assertGreater(float(loud) - float(quiet), 12)
        for clip, expected in (("two-audio", quiet), ("other-default", loud)):
            for _ in range(3):
                result = self.check_clip(clip)
                self.assertEqual(result["mode"], "per_stream")
                self.assertEqual(result["sample_peak_dbfs"], expected)
                peaks = {t["index"]: t["sample_peak_dbfs"] for t in result["track_checks"] if t["codec_type"] == "audio"}
                self.assertEqual(peaks, {1: quiet, 2: loud})
                self.assertTrue(all(len(a["stream_indices"]) == 1 for a in result["attempts"]))
        selected = self.check_clip("two-audio", "--audio-stream", "2")
        self.assertEqual(selected["sample_peak_dbfs"], loud)
        self.assertEqual([t["index"] for t in selected["track_checks"]], [0, 2])

    def test_main_video_and_explicit_preview_have_independent_black_intervals(self):
        result = self.check_clip("two-video")
        self.assertEqual(result["primary_video_index"], 1)
        self.assertEqual(len(result["black_intervals_for_review"]), 2)
        by_index = {t["index"]: t for t in result["track_checks"]}
        self.assertEqual(by_index[0]["black_intervals_for_review"], [])
        selected = self.check_clip("two-video", "--video-stream", "0", "--video-stream", "1")
        self.assertEqual(selected["primary_video_index"], 0)
        self.assertEqual(selected["black_intervals_for_review"], [])
        self.assertEqual(len(selected["track_checks"][1]["black_intervals_for_review"]), 2)

    def test_interrupted_ffmpeg_scan_discards_partial_results_and_rechecks(self):
        real_popen = subprocess.Popen
        timers = []
        def stop_first(command, *args, **kwargs):
            if "-progress" not in command or timers:
                return real_popen(command, *args, **kwargs)
            slowed = list(command)
            i = slowed.index("-i")
            slowed[i:i] = ["-readrate", "2"]
            process = real_popen(slowed, *args, **kwargs)
            timer = threading.Timer(1.1, process.terminate)
            timers.append(timer)
            timer.start()
            return process
        with patch.object(qa.subprocess, "Popen", side_effect=stop_first):
            result = self.check_clip("quiet")
        for timer in timers:
            timer.join()
        self.assertEqual([a["status"] for a in result["attempts"]], ["incomplete"] + ["passed"] * 4)
        self.assertEqual([a["operation"] for a in result["attempts"][1:]], ["decode", "signal"] * 2)
        self.assertEqual(len(result["black_intervals_for_review"]), 2)
        self.assertEqual(result["status"], "passed")

    def test_user_cancel_saves_incomplete_result_without_retry(self):
        with patch.object(qa, "scan", side_effect=KeyboardInterrupt):
            result = self.check_clip("quiet", expect=130)
        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(len(result["attempts"]), 1)
        self.assertIsNone(result["sample_peak_dbfs"])
        self.assertFalse(result["decode_passed"] or result["signal_scan_passed"])

    def test_advancing_longer_scan_continues_past_idle_interval(self):
        real_popen = subprocess.Popen
        def paced(command, *args, **kwargs):
            if "-progress" in command:
                command = list(command)
                i = command.index("-i")
                command[i:i] = ["-readrate", "2", "-threads", "1"]
            return real_popen(command, *args, **kwargs)
        with patch.object(qa.subprocess, "Popen", side_effect=paced):
            start = time.monotonic()
            result = self.check_clip("quiet", "--idle-timeout", "1.5")
        self.assertGreater(time.monotonic() - start, 1.5)
        self.assertEqual([a["status"] for a in result["attempts"]], ["passed"])

    def test_unchanging_progress_is_stopped_and_reaped(self):
        real_popen = subprocess.Popen
        children = []
        def stationary(command, *args, **kwargs):
            toy = "import time\nfor i in range(100):\n print('frame=1', flush=True)\n time.sleep(.06)"
            child = real_popen([sys.executable, "-u", "-c", toy], *args, **kwargs)
            children.append(child)
            return child
        with patch.object(qa.subprocess, "Popen", side_effect=stationary):
            start = time.monotonic()
            res = qa.scan(FF, self.root / "quiet.mp4", [{"index": 0, "codec_type": "video"}], "decode", .5)
        self.assertEqual(res["status"], "incomplete")
        self.assertLess(time.monotonic() - start, 3.5)
        self.assertIsNotNone(children[0].poll())

    def test_incomplete_signals_never_publish_partial_values(self):
        real_scan = qa.scan
        def missing_end(ffmpeg, source, tracks, operation, idle):
            if operation == "signal" and tracks[0]["codec_type"] == "audio":
                return {"status": "incomplete", "detail": "Interrupted", "black": [],
                        "levels": {"max_volume": "0.0", "mean_volume": "-0.1"}}
            return real_scan(ffmpeg, source, tracks, operation, idle)
        with patch.object(qa, "scan", side_effect=missing_end):
            result = self.check_clip("quiet", "--separate", expect=1)
        self.assertEqual(result["status"], "incomplete")
        self.assertTrue(result["decode_passed"])
        self.assertFalse(result["signal_scan_passed"])
        self.assertIsNone(result["mean_volume_dbfs"])
        self.assertEqual(len(result["black_intervals_for_review"]), 2)

    def test_invalid_selection_and_duration_mismatch(self):
        self.assertEqual(self.check_clip("quiet", "--audio-stream", "0", expect=1)["status"], "incomplete")
        result = self.check_clip("quiet", "--expected-duration", "10", expect=1)
        self.assertTrue(result["decode_passed"])
        self.assertFalse(result["duration_passed"])
        self.assertEqual(result["status"], "failed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--ffprobe", default="ffprobe")
    args, test_args = parser.parse_known_args()
    FF = str(Path(shutil.which(args.ffmpeg) or args.ffmpeg).resolve())
    FP = str(Path(shutil.which(args.ffprobe) or args.ffprobe).resolve())
    unittest.main(argv=[sys.argv[0], *test_args], verbosity=2)
