#!/usr/bin/env python3
import argparse
from pathlib import Path

from common import MiniMaxError, download_url, print_json, request_json, request_multipart, resolve_output_path


def upload_file(path: str, purpose: str):
    p = Path(path).expanduser().resolve()
    with p.open("rb") as f:
        files = {"file": (p.name, f)}
        data = {"purpose": purpose}
        return request_multipart("/v1/files/upload", data=data, files=files, timeout=600)


def cmd_upload_clone(args):
    data = upload_file(args.file, "voice_clone")
    print_json({"ok": True, "file": data.get("file"), "base_resp": data.get("base_resp")})


def cmd_upload_prompt(args):
    data = upload_file(args.file, "prompt_audio")
    print_json({"ok": True, "file": data.get("file"), "base_resp": data.get("base_resp")})


def cmd_clone(args):
    body = {
        "file_id": int(args.file_id),
        "voice_id": args.voice_id,
        "need_noise_reduction": args.noise_reduction,
        "need_volume_normalization": args.volume_normalization,
        "aigc_watermark": args.watermark,
    }
    if args.text:
        body["text"] = args.text
        body["model"] = args.model
    if args.language_boost:
        body["language_boost"] = args.language_boost
    if args.prompt_audio_id or args.prompt_text:
        if not (args.prompt_audio_id and args.prompt_text):
            raise SystemExit("clone_prompt requires both --prompt-audio-id and --prompt-text")
        body["clone_prompt"] = {
            "prompt_audio": int(args.prompt_audio_id),
            "prompt_text": args.prompt_text,
        }
    data = request_json("POST", "/v1/voice_clone", json_body=body, timeout=600)
    result = {
        "ok": True,
        "voice_id": args.voice_id,
        "demo_audio": data.get("demo_audio"),
        "input_sensitive": data.get("input_sensitive"),
        "base_resp": data.get("base_resp"),
    }
    if args.download_demo and data.get("demo_audio"):
        out = resolve_output_path(args.output, "voice-demo", ".mp3")
        download_url(data["demo_audio"], out)
        result["demo_path"] = str(out)
    print_json(result)


def cmd_clone_from_files(args):
    clone_upload = upload_file(args.clone_file, "voice_clone")
    file_id = clone_upload.get("file", {}).get("file_id")
    prompt_audio_id = None
    if args.prompt_audio:
        prompt_upload = upload_file(args.prompt_audio, "prompt_audio")
        prompt_audio_id = prompt_upload.get("file", {}).get("file_id")
    clone_args = argparse.Namespace(
        file_id=file_id,
        voice_id=args.voice_id,
        text=args.text,
        model=args.model,
        language_boost=args.language_boost,
        prompt_audio_id=prompt_audio_id,
        prompt_text=args.prompt_text,
        noise_reduction=args.noise_reduction,
        volume_normalization=args.volume_normalization,
        watermark=args.watermark,
        download_demo=args.download_demo,
        output=args.output,
    )
    cmd_clone(clone_args)


def main():
    ap = argparse.ArgumentParser(description="MiniMax voice cloning wrapper")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("upload-clone")
    p1.add_argument("file")
    p1.set_defaults(func=cmd_upload_clone)

    p2 = sub.add_parser("upload-prompt")
    p2.add_argument("file")
    p2.set_defaults(func=cmd_upload_prompt)

    p3 = sub.add_parser("clone")
    p3.add_argument("--file-id", required=True)
    p3.add_argument("--voice-id", required=True)
    p3.add_argument("--text")
    p3.add_argument("--model", default="speech-2.8-hd")
    p3.add_argument("--language-boost")
    p3.add_argument("--prompt-audio-id")
    p3.add_argument("--prompt-text")
    p3.add_argument("--noise-reduction", action="store_true")
    p3.add_argument("--volume-normalization", action="store_true")
    p3.add_argument("--watermark", action="store_true")
    p3.add_argument("--download-demo", action="store_true")
    p3.add_argument("--output")
    p3.set_defaults(func=cmd_clone)

    p4 = sub.add_parser("clone-from-files")
    p4.add_argument("--clone-file", required=True)
    p4.add_argument("--voice-id", required=True)
    p4.add_argument("--prompt-audio")
    p4.add_argument("--prompt-text")
    p4.add_argument("--text")
    p4.add_argument("--model", default="speech-2.8-hd")
    p4.add_argument("--language-boost")
    p4.add_argument("--noise-reduction", action="store_true")
    p4.add_argument("--volume-normalization", action="store_true")
    p4.add_argument("--watermark", action="store_true")
    p4.add_argument("--download-demo", action="store_true")
    p4.add_argument("--output")
    p4.set_defaults(func=cmd_clone_from_files)

    args = ap.parse_args()
    try:
        args.func(args)
    except MiniMaxError as e:
        raise SystemExit(str(e))


if __name__ == "__main__":
    main()
