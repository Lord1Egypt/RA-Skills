# zimage — 무료 AI 이미지 생성 스킬

<p align="center">
  <img src="../icon.png" alt="Z-Image Skill" width="128" height="128">
</p>

<p align="center">
  <strong>AI 코딩 어시스턴트에서 텍스트로 무료 이미지를 생성하세요.</strong><br>
  Claude Code · OpenClaw · Codex · Antigravity · Paperclip 지원
</p>

<p align="center">
  <a href="../README.md">English</a> ·
  <a href="./README_TW.md">繁體中文</a> ·
  <a href="./README_JA.md">日本語</a> ·
  <a href="./README_KO.md">한국어</a> ·
  <a href="./README_ES.md">Español</a> ·
  <a href="./README_DE.md">Deutsch</a> ·
  <a href="./README_FR.md">Français</a> ·
  <a href="./README_IT.md">Italiano</a>
</p>

---

## 개요

**zimage**는 AI 어시스턴트에 텍스트에서 이미지를 생성하는 기능을 추가하는 스킬입니다. Alibaba Tongyi-MAI 팀이 개발한 오픈소스 모델 [Z-Image-Turbo](https://github.com/Tongyi-MAI/Z-Image)(60억 파라미터)를 ModelScope의 무료 API를 통해 호출합니다.

```
사용자:  도서관에서 책을 읽는 여우 이미지를 만들어줘
AI:     제출 중: 도서관에서 책을 읽는 여우
        태스크 91204 — 결과 대기 중…
        저장 완료 → fox_library.jpg
```

### 비교

|  | zimage | DALL-E 3 | Midjourney |
|--|--------|----------|------------|
| 가격 | **무료** | $0.04–0.08 / 장 | $10+/월 |
| 오픈소스 | Apache 2.0 | 아니오 | 아니오 |
| 설정 시간 | 약 5분 | 결제 설정 필요 | Discord 필요 |

> **무료 할당량:** 하루 총 2,000회, 모델당 500회/일. 한도는 동적으로 조정될 수 있습니다. ([공식 한도](https://modelscope.ai/docs/model-service/API-Inference/limits))

---

## 설정

### 1단계 — Alibaba Cloud 계정 (무료)

여기서 가입: **https://www.alibabacloud.com/campaign/benefits?referral_code=A9242N**

가입 시 전화번호 인증과 결제 수단 등록이 필요합니다. **Z-Image 자체는 무료이며 요금이 부과되지 않습니다**. 단, Alibaba Cloud는 계정에 결제 정보 등록을 요구합니다.

### 2단계 — ModelScope 계정 + 연동

1. **https://modelscope.ai/register?inviteCode=futurizerush&invitorName=futurizerush&login=true&logintype=register** 에서 가입 (GitHub 로그인 지원)
2. **설정 → Bind Alibaba Cloud Account**에서 1단계 계정 연동

### 3단계 — API 토큰

1. **https://modelscope.ai/my/access/token** 방문
2. **Create Your Token** 클릭
3. 토큰 복사 (형식: `ms-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

---

## 설치

<details>
<summary><b>Claude Code</b></summary>

Claude Code에서 이렇게 말하세요:

```
Install the zimage skill from https://github.com/FuturizeRush/zimage-skill
```

그 다음:

```
Set my MODELSCOPE_API_KEY environment variable to ms-당신의토큰
```

Claude Code를 재시작하세요.
</details>

<details>
<summary><b>OpenClaw / ClawHub</b></summary>

```bash
openclaw skills install zimage
# 또는
npx clawhub@latest install zimage
```

```bash
export MODELSCOPE_API_KEY="ms-당신의토큰"
```
</details>

<details>
<summary><b>Codex / Antigravity / Paperclip / 기타</b></summary>

```bash
git clone https://github.com/FuturizeRush/zimage-skill.git
cd zimage-skill
pip install Pillow  # 선택 사항 (형식 변환용)
export MODELSCOPE_API_KEY="ms-당신의토큰"
```

```bash
python3 imgforge.py "바다 위의 석양" sunset.jpg
```
</details>

---

## 사용법

### AI 어시스턴트를 통해

자연어로 요청하세요:

```
아늑한 카페 이미지를 만들어줘, 따뜻한 조명, 시네마틱
불을 뿜는 픽셀 아트 드래곤을 그려줘
미니멀한 로고를 만들어줘, 파란 그라데이션
```

### CLI 직접 실행

```bash
# 기본
python3 imgforge.py "화성의 우주비행사"

# 커스텀 사이즈 (가로형)
python3 imgforge.py "골든아워의 산 파노라마" -o panorama.jpg -W 2048 -H 1024

# JSON 출력
python3 imgforge.py "추상 예술" --json
```

---

## 문제 해결

| 문제 | 해결 방법 |
|------|----------|
| `MODELSCOPE_API_KEY is not set` | [설정](#설정)을 완료하세요 |
| `401 Unauthorized` | **modelscope.ai** (.cn 아님) 사용. Alibaba Cloud 연동 확인. 토큰 재생성. |
| 타임아웃 | API 부하 — 1분 후 재시도 |
| 콘텐츠 모더레이션 | 프롬프트를 수정하세요 |

---

## 라이선스

MIT-0 — 자유롭게 사용하세요. 저작자 표시 불필요.
