---
name: hwp-extract-pipeline
description: "HWP/HWPX/PDF extraction pipeline: attempt hwp-reader, then pyhwp, then OCR, with safe fallbacks. Use when agent needs reliable text extraction from Korean HWP/HWPX or PDF/scan attachments."
---

# hwp-extract-pipeline

간단한 HWP/HWPX/PDF 추출 파이프라인 스킬입니다. 핵심 목표는 로컬에 저장된 공고문(한글 파일)을 안정적으로 텍스트로 변환해 JSON 형식으로 반환하는 것입니다.

간단 사용법

- 실행 스크립트: scripts/extract_hwp.py
- 입력: 로컬 파일 경로(예: /home/vorox/.openclaw/agents/nalda-mail-opt/data/<PBLN_ID>/getImageFile.do)
- 출력: JSON 출력(표준출력) 및 데이터 폴더에 <id>_extracted.json으로 저장

우선순위(폴백 방식)
1. hwp-reader 호출 (외부 skill 호출 가능시)
2. pyhwp(venv) 기반 추출
3. 시스템 OCR (poppler + tesseract) — 시스템 설치 필요할 수 있음
4. strings 기반 폴백

참고 문서
- scripts/README.md (간단 사용 예시 및 통합 방법)

