# 📸 PhotoIndexWithLLM — 한국어

## 개요

PhotoIndexWithLLM 은 비전-언어(VL) 대형 모델을 활용하여 사진의 스마트 인덱싱, 분석 및 검색을 제공하는 시스템입니다.

## 빠른 시작

```bash
# 종속성 설치
pip install requests

# 사진 스캔
python skill.py scan --dir /home/user/Photos

# 사진 검색
python skill.py search "바다 석양"

# JSON 출력
python skill.py search "바다" --format json
```

## 지원 플랫폼

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

## 지원 이미지 형식 (17종)

| 유형 | 형식 |
|------|------|
| 일반 | `.jpg` `.jpeg` `.png` `.webp` `.bmp` `.tiff` `.gif` |
| iPhone/Apple | `.heic` `.heif` |
| Canon DSLR | `.cr2` |
| Nikon DSLR | `.nef` |
| Sony DSLR | `.arw` |
| 기타 RAW | `.orf` `.raf` `.dng` `.rw2` `.pef` `.sr2` |

## 개인정보 보호

- 기본적으로 로컬 모드만 사용
- 사진은 외부로 전송되지 않습니다
- 원격 모델 전송에는 사용자 확인이 필요합니다

## 전체 명령어 목록

```bash
# 사진 스캔
python skill.py scan --dir /home/user/Photos

# 사진 검색
python skill.py search "바다 석양"

# 스캔 및 검색
python skill.py scan_and_search --dir /home/user/Photos --query "바다"

# 주석 추가
python skill.py annotate --photo /photos/img001.jpg --type person --name 김철수

# 모델 훈련
python skill.py train

# 통계 확인
python skill.py stats

# 연결 테스트
python skill.py test
```

## 연락처

**작성자**: 北京老李（beijingLL）
**ClawHub ID**: 43622283
