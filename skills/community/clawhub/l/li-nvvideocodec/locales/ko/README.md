# li_nvvideocodec - NVIDIA AV1 비디오 압축 도구

**버전**: 1.0.1  
**언어**: 한국어 (ko)

## 📋 개요

NVIDIA GPU 하드웨어 가속 AV1 인코딩을 사용한 배치 비디오 압축 도구입니다. 지능형 검증 및 여러 압축 프로필로 효율적으로 비디오를 압축합니다.

## ✨ 특징

- 🎯 **스마트 검증** - 압축 효과 자동 테스트
- 📊 **3가지 프로필** - 보수적/균형/공격적
- 🖥️ **크로스 플랫폼** - Windows & Ubuntu Linux
- 📈 **실시간 진행** - 라이브 진행 표시
- 🔒 **안전** - 원본 파일 보호

## 🚀 빠른 시작

```bash
# 대화형 모드
python scripts/compress_videos.py

# 명령줄 모드
python scripts/compress_videos.py -i "/path/to/videos" -p B --no-confirm

# 테스트 모드
python scripts/compress_videos.py -i "/path/to/videos" -p B --test
```

## 📊 압축 프로필

| 프로필 | 해상도 | CRF | FPS | 오디오 | 절약 |
|--------|--------|-----|-----|--------|------|
| **A** | 유지 | 23 | 유지 | 128k | 40-60% |
| **B** ⭐ | 1280x720 | 24 | 24 | 96k | 65-75% |
| **C** | 1280x720 | 28 | 15 | 64k | 78-85% |

## ⚙️ 요구 사항

- **FFmpeg** (av1_nvenc 지원)
- **NVIDIA GPU** (GTX 1650+)
- **Python 3.7+**

## 🤖 에이전트 사용법

```bash
# 환경 확인
python agent_interface.py --action check

# 비디오 분석
python agent_interface.py --action analyze -i "/path/to/videos"

# 압축
python agent_interface.py --action compress -i "/path/to/videos" -p B
```
