---
name: kakao-local-cli
description: Kakao Local API CLI: keyword/category search, geocode, reverse
version: 0.1.1
metadata:
  openclaw:
    requires:
      env:
        - KAKAO_REST_API_KEY
    primaryEnv: KAKAO_REST_API_KEY
    homepage: https://github.com/ChloePark85/kakao-local-cli
---

Kakao Local API를 위한 경량 CLI 도구이다. 키워드/카테고리 장소검색, 주소→좌표(geocode), 좌표→주소(reverse-geocode)를 지원한다. Linux/macOS/Windows 어디서나 실행 가능하며 STDIN/STDOUT 기반 JSON 출력을 기본으로 하여 에이전트·자동화 파이프라인에 적합하다. 인증은 환경변수 KAKAO_REST_API_KEY로 설정한다.

설치
- pipx install . 또는 pip install . (레포 클론 후)
- 저장소: https://github.com/ChloePark85/kakao-local-cli

사용법 예시
- 키워드 검색
  kakao-local search --query "카카오프렌즈" --x 126.9784 --y 37.5666 --radius 5000
- 카테고리 검색 (카페: CE7)
  kakao-local search --category CE7 --x 126.9784 --y 37.5666 --radius 1000
- 지오코딩 (주소→좌표)
  kakao-local geocode --query "서울특별시 중구 세종대로 110"
- 리버스 지오코딩 (좌표→주소)
  kakao-local reverse --x 126.9784 --y 37.5666

환경변수
- KAKAO_REST_API_KEY: Kakao Developers REST API 키 (필수)
