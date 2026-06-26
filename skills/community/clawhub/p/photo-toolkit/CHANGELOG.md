# Changelog — photo-toolkit

All notable changes to this skill will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This skill carries its own version per [strategy C in RELEASING.md](../RELEASING.md).

## [Unreleased]

## [1.0.0] - 2026-05-20

Initial public release on [ClawHub](https://clawhub.ai).

### Added

- Convert RAW / JPG / HEIC to JPG thumbnails (`convert.py`).
- Find photos by EXIF shooting date (`find_by_date.py`), supports timelapse sequence detection.
- Generate before/after layout previews (`layout_preview.py`).
- Deflicker timelapse frames (`deflicker.py`).
- Assemble JPG frames into MP4 (`assemble.py`).
- Supports Nikon (NEF), Canon (CR2/CR3), Sony (ARW), Fujifilm (RAF), Olympus (ORF), Panasonic (RW2), Pentax (PEF), Samsung (SRW), Leica (DNG), Hasselblad (3FR), Phase One (IIQ), Sigma (X3F), plus standard JPEG and Apple HEIC/HEIF.
