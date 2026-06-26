# Core Behavior Reference

This reference documents the local audio wrapper behavior without embedding machine-specific paths. Optional engine binaries are discovered from `--app-dir`, environment variables, or system `PATH`.

## Tool Discovery

The script looks for these tools:

- `ffmpeg`: required for conversion, compression, merge, split, clip, and video-to-audio.
- `ffprobe`: required for `info` and duration-aware `split`.
- `um`: optional local music-cache decode helper.
- `music_tool`: optional local music-cache decode helper.
- `silk`: optional SILK decode helper.
- `kgg_helper`: optional Kugou `.kgg` decode helper.

Environment variables:

```text
LUIS_AUDIO_TRANSLATOR_ENGINE_DIR
LUIS_AUDIO_TRANSLATOR_FFMPEG
LUIS_AUDIO_TRANSLATOR_FFPROBE
LUIS_AUDIO_TRANSLATOR_UM
LUIS_AUDIO_TRANSLATOR_MUSIC_TOOL
LUIS_AUDIO_TRANSLATOR_SILK
LUIS_AUDIO_TRANSLATOR_KGG_HELPER
LUIS_AUDIO_TRANSLATOR_KUGOU_INFRA_DLL
LUIS_AUDIO_TRANSLATOR_KUGOU_DB
```

If `LUIS_AUDIO_TRANSLATOR_ENGINE_DIR` or `--app-dir` is set, the scripts also check for a `resources/library` layout containing `ffmpeg-shared`, `um`, `music-tool-v2`, `silk`, and `kgg` subdirectories.

## Input Extensions

Common audio/media inputs:

```text
mp3 wav ogg flac m4a m4r mp2 aiff ac3 wma amr aifc caf aac ape mmf wv au voc 3gpp mka tkm awb m4b dff dsd dsf dst sacd cda kgm kgma mid msf adx ncm aif dts mpa mod ram tta kwm kgtemp opus weba tak webm f4v ogv avi flv mkv mov mp4 mpg mpeg ps rmvb swf vob wmv wtv rm asf m2v m2ts mts m2t ts dv mxf m4v m4s h264 h265 gif 3gp qmc mflac mgg mggh
```

Common video inputs:

```text
mp4 flv f4v webm m4v mov 3gp 3g2 rm rmvb wmv avi asf mpg mpeg mpe ts div dv divx vob dat mkv lavf cpk dirac ram qt fli flc mod
```

Supported cache/decode extension routing:

```text
qmc0 qmc2 qmc3 qmcflac qmcogg tkm bkcmp3 bkcflac tm0 tm2 tm3 tm6 mflac mgg mflac0 mggl ofl_en oggl ncm kwm kgm kgma vpr x2m x3m mg3d silk
```

Kugou-specific converter inputs:

```text
kgm kgma kgtemp kgm.flac kgg
```

## FFmpeg Option Mapping

- Conversion and video-to-audio use `-vn`.
- `--volume` adds an audio volume filter.
- `--sample-rate` maps to `-ar`.
- `--bitrate` maps to `-b:a`.
- `--channels` maps to `-ac`.
- Metadata fields map to FFmpeg `-metadata`.
- `amr` forces 8000 Hz and mono.
- `flac` adds `-sample_fmt s16`.
- `m4r` uses an MP4 container.

Merge uses FFmpeg `concat` filter over all input audio streams. Split creates one output file per segment.

## Decode Helper Behavior

- `.silk`: decode to PCM with the configured SILK helper, then convert PCM to WAV via FFmpeg.
- Generic cache formats such as `.ncm`, `.kgm`, `.kgma`, `.kwm`, `.tm*`, `.bk*`, `.vpr`, `.x2m`, `.x3m`, `.mg3d`: use the configured `um` helper.
- `.mflac` and `.mgg` files ending with `musicex\0`: use the configured `music_tool` helper, then append `.flac` or `.ogg`.
- `.kgg`: use `scripts/kugou_audio_converter.py`, which calls `kgg-helper` with a compatible Kugou `infra.dll` and optional `KGMusicV3.db`.
- `.xm`: use `decrypt --engine xm` or `decrypt --engine auto`. This calls `scripts/xm_audio_decoder.py`, reads the `.xm` ID3 metadata, uses pure-Python AES-CBC logic, and writes the decoded audio payload. No Node.js, WebAssembly, or external helper is required.

Use `decrypt --engine auto` first. If auto fails, try `--engine um`, `--engine music-tool`, `--engine silk`, or `--engine xm` based on the extension and configured tools.

## Kugou Converter

`scripts/kugou_audio_converter.py` is the dedicated batch tool for Kugou formats.

It supports:

- `diagnose`: report FFmpeg, `um`, `kgg-helper`, `infra.dll`, and `KGMusicV3.db` discovery.
- `convert`: scan files or directories, decode supported Kugou special formats, and write a target format such as MP3.

Discovery:

- `kgg-helper`: `LUIS_AUDIO_TRANSLATOR_KGG_HELPER`, then `<engine-dir>/resources/library/kgg/kgg-helper.exe`.
- `infra.dll`: `LUIS_AUDIO_TRANSLATOR_KUGOU_INFRA_DLL`, then common Kugou install and user data locations.
- `KGMusicV3.db`: `LUIS_AUDIO_TRANSLATOR_KUGOU_DB`, then the standard user data location.
