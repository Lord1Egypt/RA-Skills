#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Acoustic Pipeline - Enhanced ASR processing pipeline

Built on top of the Qwen3-ASR skill:
1. Automatic audio extraction from video
2. Multi-format support (MP4, MP3, WAV, etc.)
3. Automated processing (folder watch or batch)
4. Direct LLM callable API

Usage:
  python acoustic_pipeline.py --file "audio.mp4" --language Chinese
  python acoustic_pipeline.py --watch "C:\\inbox"
  python acoustic_pipeline.py --batch "C:\\audio\\library"
"""

import json
import subprocess
import sys
import argparse
import os
import importlib.util
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any


TRANSCRIBE_SUBPROCESS_TIMEOUT = 3600


class AcousticPipeline:
    """Audio/video transcription pipeline."""
    
    # Supported formats
    AUDIO_FORMATS = {'.wav', '.mp3', '.flac', '.m4a', '.ogg', '.aac', '.wma', '.opus'}
    VIDEO_FORMATS = {'.mp4', '.mkv', '.webm', '.flv', '.mov', '.avi', '.mts', '.m2ts', '.ts', '.m3u8'}
    ALL_FORMATS = AUDIO_FORMATS | VIDEO_FORMATS
    
    # Class-level cache to avoid repeated environment checks
    _cached_state = None
    _cached_venv_py = None
    _cache_timestamp = 0
    # Class-level cache for the transcribe module so _MODEL_CACHE survives across instances
    _transcribe_module = None
    _transcribe_module_path = None
    
    def __init__(self, asr_skill_dir: Optional[str] = None, auto_bootstrap: bool = False):
        """
        Initialize the pipeline.

        Args:
            asr_skill_dir: ASR skill directory (default: auto-detect *_openvino/asr)
            auto_bootstrap: run setup.py + download_model.py automatically when env is missing
        """
        if asr_skill_dir:
            self.asr_dir = Path(asr_skill_dir)
        else:
            # auto-scan all drives for *_openvino/asr
            self.asr_dir = self._find_openvino_asr_dir() or Path.cwd()
        
        # use cache or locate state file
        self.state_file = self._find_state_json_cached()
        self.venv_py = self._find_venv_python_cached()

        self.runtime_asr_dir = self.asr_dir
        if self.state_file:
            try:
                state = json.loads(self.state_file.read_text(encoding="utf-8"))
                asr_runtime = Path(state.get("ASR_DIR", ""))
                if asr_runtime.exists():
                    self.runtime_asr_dir = asr_runtime
            except Exception:
                pass

        self.transcribe_py = self.runtime_asr_dir / 'transcribe.py'
        if not self.transcribe_py.exists():
            local_transcribe = self.asr_dir / 'transcribe.py'
            if local_transcribe.exists():
                self.transcribe_py = local_transcribe

        if not self.transcribe_py.exists() and auto_bootstrap:
            self._bootstrap_asr_skill()
            # re-locate after bootstrap (state.json may now exist)
            self.state_file = self._find_state_json()
            self.venv_py = self._find_venv_python()

            self.runtime_asr_dir = self.asr_dir
            if self.state_file:
                try:
                    state = json.loads(self.state_file.read_text(encoding="utf-8"))
                    asr_runtime = Path(state.get("ASR_DIR", ""))
                    if asr_runtime.exists():
                        self.runtime_asr_dir = asr_runtime
                except Exception:
                    pass
            self.transcribe_py = self.runtime_asr_dir / 'transcribe.py'

        if not self.transcribe_py.exists():
            raise FileNotFoundError(
                "transcribe.py not found. Ensure ASR is initialized or use --auto-bootstrap.\n"
                f"Checked: {self.runtime_asr_dir / 'transcribe.py'}"
            )

        # prefer in-process call to avoid subprocess overhead
        self._transcribe_fn = self._load_transcribe_callable()

    def _load_transcribe_callable(self):
        """Load the transcribe() function from transcribe.py.
        Module is cached at class level so _MODEL_CACHE survives across instances.
        Returns None on failure; caller falls back to subprocess.
        """
        transcribe_path = str(self.transcribe_py)
        # reuse cached module (preserves _MODEL_CACHE in its globals)
        if (AcousticPipeline._transcribe_module is not None and
                AcousticPipeline._transcribe_module_path == transcribe_path):
            fn = getattr(AcousticPipeline._transcribe_module, "transcribe", None)
            return fn if callable(fn) else None
        try:
            module_name = f"local_transcribe_{abs(hash(transcribe_path))}"
            spec = importlib.util.spec_from_file_location(module_name, transcribe_path)
            if spec is None or spec.loader is None:
                return None
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            AcousticPipeline._transcribe_module = module
            AcousticPipeline._transcribe_module_path = transcribe_path
            fn = getattr(module, "transcribe", None)
            return fn if callable(fn) else None
        except Exception as e:
            print(f"[DEBUG] Direct transcribe load failed, fallback to subprocess: {e}", file=sys.stderr)
            return None
    
    def _find_venv_python_cached(self) -> Path:
        """Find venv Python with 5-minute cache."""
        import time
        current_time = time.time()
        
        # use cache if fresh (< 5 min)
        if (self._cached_venv_py and 
            current_time - self._cache_timestamp < 300):
            return self._cached_venv_py
        
        result = self._find_venv_python()
        self._cached_venv_py = result
        self._cache_timestamp = current_time
        return result
    
    def _find_state_json_cached(self) -> Optional[Path]:
        """Find state.json with 5-minute cache."""
        import time
        current_time = time.time()
        
        # sentinel 'NOT_FOUND' means we already checked and found nothing
        if (self._cached_state is not None and 
            current_time - self._cache_timestamp < 300):
            return self._cached_state if self._cached_state != 'NOT_FOUND' else None
        
        result = self._find_state_json()
        self._cached_state = result if result else 'NOT_FOUND'
        self._cache_timestamp = current_time
        return result
    
    def _find_venv_python(self) -> Path:
        """Locate the venv Python executable."""
        # strategy 1: read from state.json
        state_file = self._find_state_json()
        if state_file:
            try:
                state = json.loads(state_file.read_text(encoding="utf-8"))
                venv_py_str = state.get('VENV_PY', '')
                if venv_py_str:
                    venv_py = Path(venv_py_str)
                    if venv_py.exists():
                        return venv_py
                    else:
                        # path may be stale, try next strategy
                        print(f"[DEBUG] VENV_PY from state.json not found: {venv_py_str}", file=sys.stderr)
            except Exception as e:
                print(f"[DEBUG] Failed to read state.json: {e}", file=sys.stderr)
        
        # strategy 2: common locations
        username = os.environ.get('USERNAME', 'user').lower()
        common_paths = [
            # user's *_openvino directory
            Path.home() / f"{username}_openvino" / "venv" / "Scripts" / "python.exe",
            Path(f"C:\\{username}_openvino\\venv\\Scripts\\python.exe"),
            # current ASR directory
            self.asr_dir / "venv" / "Scripts" / "python.exe",
        ]
        
        for path in common_paths:
            if path.exists():
                print(f"[DEBUG] Found python.exe at: {path}", file=sys.stderr)
                return path
        
        # strategy 3: scan all drives for *_openvino/venv
        import string
        for drive in string.ascii_uppercase:
            base_path = Path(f"{drive}:\\")
            if not base_path.exists():
                continue
            try:
                for item in base_path.iterdir():
                    if item.is_dir() and "_openvino" in item.name:
                        venv_py = item / "venv" / "Scripts" / "python.exe"
                        if venv_py.exists():
                            print(f"[DEBUG] Found python.exe in {item.name}: {venv_py}")
                            return venv_py
            except PermissionError:
                continue
        
        # fallback: system Python
        print(f"[DEBUG] Falling back to system python.exe: {sys.executable}")
        return Path(sys.executable)
    
    def _find_openvino_asr_dir(self) -> Optional[Path]:
        """Scan all drives for a *_openvino/asr directory."""
        import string

        for drive in string.ascii_uppercase:
            base_path = Path(f"{drive}:\\")
            if not base_path.exists():
                continue
            
            # look for *_openvino/asr under this drive
            try:
                for item in base_path.iterdir():
                    if item.is_dir() and "_openvino" in item.name:
                        asr_candidate = item / "asr"
                        if asr_candidate.exists():
                            return asr_candidate
            except PermissionError:
                continue

        return None

    def _find_state_json(self) -> Optional[Path]:
        """Locate state.json."""
        import string

        username = os.environ.get('USERNAME', 'user').lower()

        for drive in string.ascii_uppercase:
            state_file = Path(f"{drive}:\\{username}_openvino\\asr\\state.json")
            if state_file.exists():
                return state_file

        local_state = self.asr_dir / "state.json"
        if local_state.exists():
            return local_state

        return None

    def _run_bootstrap_script(self, script_name: str):
        """Run a bootstrap script (setup.py or download_model.py)."""
        script_path = self.asr_dir / script_name
        if not script_path.exists():
            raise FileNotFoundError(f"Bootstrap script not found: {script_path}")

        cmd = [str(Path(sys.executable)), str(script_path)]
        # run in the ASR directory so generated files land in the right place
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            timeout=1800,
            cwd=str(self.asr_dir)  # run inside ASR dir
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"{script_name} failed:\n{result.stderr or result.stdout}"
            )

    def _bootstrap_asr_skill(self):
        """Auto-initialize ASR environment and model when not yet set up."""
        print("[INFO] ASR not initialized - running setup.py ...")
        self._run_bootstrap_script("setup.py")
        print("[INFO] Running download_model.py ...")
        self._run_bootstrap_script("download_model.py")

    def _archive_transcript(
        self,
        source_file: Path,
        result: Dict[str, Any],
        archive_mode: str = "none",
        archive_dir: Optional[str] = None,
    ) -> Dict[str, str]:
        """Save transcript in the requested format(s)."""
        if archive_mode == "none":
            return {}

        out_dir = Path(archive_dir) if archive_dir else source_file.parent / "transcripts"
        out_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{source_file.stem}_{timestamp}"
        saved = {}

        if archive_mode in {"txt", "both"}:
            txt_path = out_dir / f"{base_name}.txt"
            txt_path.write_text(str(result.get("text", "")), encoding="utf-8")
            saved["txt"] = str(txt_path)

        if archive_mode in {"json", "both"}:
            json_path = out_dir / f"{base_name}.json"
            json_path.write_text(
                json.dumps(result, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            saved["json"] = str(json_path)

        return saved

    def _is_video(self, file_path: Path) -> bool:
        """Return True if file_path is a supported video format."""
        return file_path.suffix.lower() in self.VIDEO_FORMATS
    
    def _is_audio(self, file_path: Path) -> bool:
        """Return True if file_path is a supported audio format."""
        return file_path.suffix.lower() in self.AUDIO_FORMATS
    
    def _extract_audio_from_video(self, video_path: Path, output_wav: Optional[Path] = None) -> Path:
        """
        Extract audio track from a video file.

        Args:
            video_path: path to the video file
            output_wav: output WAV path (auto-generated if None)

        Returns:
            path to the extracted WAV file
        """
        if output_wav is None:
            output_wav = video_path.parent / f"{video_path.stem}_audio.wav"
        
        print(f"  [VIDEO] Extracting audio: {video_path.name}...")
        
        # try ffmpeg first (most reliable)
        try:
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-q:a', '9',
                '-n',  # do not overwrite
                str(output_wav)
            ]
            result = subprocess.run(cmd, capture_output=True, timeout=300)
            
            if result.returncode == 0 and output_wav.exists():
                print(f"  [OK] Audio extracted: {output_wav.name}")
                return output_wav
        except:
            pass
        
        # fallback: moviepy (slower but reliable)
        try:
            from moviepy.editor import VideoFileClip
            
            print(f"  [INFO] Using moviepy (may be slower)...")
            clip = VideoFileClip(str(video_path))
            if clip.audio is None:
                raise ValueError("Video has no audio track")
            
            clip.audio.write_audiofile(str(output_wav), verbose=False, logger=None)
            clip.close()
            
            print(f"  [OK] Audio extracted: {output_wav.name}")
            return output_wav
        except ImportError:
            raise RuntimeError(
                "ffmpeg or moviepy required for video audio extraction.\n"
                "Install: pip install moviepy\n"
                "Or download ffmpeg: https://ffmpeg.org/download.html"
            )
        except Exception as e:
            raise RuntimeError(f"Audio extraction failed: {e}")
    
    def transcribe(
        self,
        file_path: str,
        language: str = "auto",
        keep_extracted: bool = False,
        archive_mode: str = "none",
        archive_dir: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Transcribe an audio or video file.

        Args:
            file_path: path to the file
            language: language hint (default: auto-detect)
            keep_extracted: keep the extracted WAV when input is video
            archive_mode: save format (none/txt/json/both)
            archive_dir: output directory for saved transcripts (default: transcripts/ beside source)

        Returns:
            transcription result dict
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        print(f"\n[ASR] Transcribing: {file_path.name}")
        
        # prepare audio file
        audio_file = file_path
        if self._is_video(file_path):
            audio_file = self._extract_audio_from_video(file_path)
        elif not self._is_audio(file_path):
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        # prefer in-process call to reduce startup overhead
        print(f"  [INFO] Transcribing...")

        transcription = None
        
        try:
            if self._transcribe_fn is not None:
                raw = self._transcribe_fn(str(audio_file), language, "", None)
                if isinstance(raw, dict):
                    transcription = raw
                elif isinstance(raw, str):
                    transcription = json.loads(raw)
                else:
                    raise RuntimeError(f"transcribe returned unsupported type: {type(raw).__name__}")

            if transcription is None:
                cmd = [
                    str(self.venv_py),
                    str(self.transcribe_py),
                    '--audio', str(audio_file),
                    '--language', language
                ]
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    timeout=TRANSCRIBE_SUBPROCESS_TIMEOUT,
                )

                if result.returncode != 0:
                    print(f"[DEBUG] stderr: {result.stderr}", file=sys.stderr)
                    raise RuntimeError(f"Transcription failed: {result.stderr}")

                stdout_content = result.stdout.strip()
                transcription = json.loads(stdout_content)
            
            # append metadata
            transcription['source_file'] = str(file_path)
            transcription['source_format'] = file_path.suffix

            # archive output when requested
            archived = self._archive_transcript(
                source_file=file_path,
                result=transcription,
                archive_mode=archive_mode,
                archive_dir=archive_dir,
            )
            if archived:
                transcription['archive_files'] = archived
                print(f"  [SAVED] Saved to: {', '.join(archived.values())}")

            # clean up temporary extracted audio
            if not keep_extracted and audio_file != file_path:
                try:
                    audio_file.unlink()
                except:
                    pass
            
            print(f"  [OK] Done")
            
            return transcription
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("Transcription timed out (file too large or system busy)")
        except Exception as e:
            raise RuntimeError(f"Transcription error: {e}")
    
    def batch_transcribe(
        self,
        folder_path: str,
        language: str = "auto",
        archive_mode: str = "none",
        archive_dir: Optional[str] = None,
    ):
        """
        Batch-transcribe all audio/video files in a folder.

        Args:
            folder_path: path to the folder
            language: language hint
        """
        folder = Path(folder_path)
        files = []
        
        for ext in self.ALL_FORMATS:
            files.extend(folder.rglob(f'*{ext}'))
            files.extend(folder.rglob(f'*{ext.upper()}'))
        
        print(f"\n[INFO] Found {len(set(files))} audio/video files")
        
        for idx, file_path in enumerate(sorted(set(files)), 1):
            print(f"\n[{idx}/{len(set(files))}]", end=" ")
            try:
                result = self.transcribe(
                    str(file_path),
                    language,
                    archive_mode=archive_mode,
                    archive_dir=archive_dir,
                )
                print(f"Transcribed: {result['text'][:50]}...")
            except Exception as e:
                print(f"[ERROR] {e}")
    
    def watch_folder(
        self,
        folder_path: str,
        language: str = "auto",
        archive_mode: str = "none",
        archive_dir: Optional[str] = None,
    ):
        """
        Watch a folder and auto-transcribe new files.

        Args:
            folder_path: folder to watch
            language: language hint
        """
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler, FileCreatedEvent
        except ImportError:
            raise RuntimeError("watchdog required: pip install watchdog")
        
        folder = Path(folder_path)
        processed = set()
        pipeline_self = self
        supported_formats = self.ALL_FORMATS
        
        class AudioHandler(FileSystemEventHandler):
            def on_created(self, event: FileCreatedEvent):
                if event.is_directory:
                    return
                
                file_path = Path(event.src_path)
                if file_path.suffix.lower() not in supported_formats:
                    return
                
                # simple file-completion wait
                import time
                time.sleep(1)
                
                file_key = str(file_path.resolve())
                if file_key in processed:
                    return
                
                processed.add(file_key)
                
                try:
                    result = pipeline_self.transcribe(
                        str(file_path),
                        language,
                        archive_mode=archive_mode,
                        archive_dir=archive_dir,
                    )
                    print(f"Transcribed: {result.get('text', '')[:80]}...")
                except Exception as e:
                    print(f"[ERROR] {e}")
        
        print(f"[ASR] Watching: {folder}")
        print("Press Ctrl+C to stop")
        
        handler = AudioHandler()
        observer = Observer()
        observer.schedule(handler, str(folder), recursive=True)
        observer.start()
        
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping watcher")
            observer.stop()
            observer.join()


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Audio/video transcription pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python acoustic_pipeline.py --file meeting.mp4 --language Chinese
  python acoustic_pipeline.py --watch "C:\\inbox"
  python acoustic_pipeline.py --batch "C:\\audio"
        '''
    )
    
    parser.add_argument('--file', help='transcribe a single file')
    parser.add_argument('--watch', help='watch a folder and auto-transcribe new files')
    parser.add_argument('--batch', help='batch-transcribe all files in a folder')
    parser.add_argument('--language', default='auto', help='language (default: auto-detect)')
    parser.add_argument('--dir', help='ASR skill directory (default: auto-detect)')
    parser.add_argument('--keep-audio', action='store_true', help='keep extracted audio file')
    parser.add_argument('--archive', choices=['none', 'txt', 'json', 'both'], default='none', help='transcript archive format')
    parser.add_argument('--archive-dir', help='archive directory (default: transcripts/ beside source)')
    parser.add_argument('--auto-bootstrap', action='store_true', help='auto-run setup.py + download_model.py when env is missing')
    
    args = parser.parse_args()
    
    try:
        pipeline = AcousticPipeline(args.dir, auto_bootstrap=args.auto_bootstrap)

        if args.file:
            result = pipeline.transcribe(
                args.file,
                args.language,
                args.keep_audio,
                archive_mode=args.archive,
                archive_dir=args.archive_dir,
            )
            print("\n[RESULT] Transcription:")
            print(result['text'])
            print(f"\n[INFO] Metadata: {json.dumps({k: v for k, v in result.items() if k != 'text'}, ensure_ascii=False, indent=2)}")
            
        elif args.watch:
            pipeline.watch_folder(
                args.watch,
                args.language,
                archive_mode=args.archive,
                archive_dir=args.archive_dir,
            )

        elif args.batch:
            pipeline.batch_transcribe(
                args.batch,
                args.language,
                archive_mode=args.archive,
                archive_dir=args.archive_dir,
            )
            
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
