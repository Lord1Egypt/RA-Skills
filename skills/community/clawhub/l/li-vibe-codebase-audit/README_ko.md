# 🔒 Vibe Codebase Audit - 한국어 사용 가이드

## 📋 개요

**Vibe Codebase Audit**은 AI 생성 코드베이스를 위한 종합 보안 감사 도구입니다. 에이전트 네이티브 통합, 다중 제공자 지원, 의존성 보안 스캔을 제공합니다.

> 🎉 **v2.0의 새로운 기능**: 에이전트 네이티브 감사 (API 키 불필요), 다중 제공자 지원, 의존성 스캔, 구성 감사

---

## ⚡ 빠른 시작

### 방법 1: 에이전트 네이티브 감사 (권장, 설정 불필요!)

```python
# API 키 불필요! 현재 에이전트의 LLM 직접 사용
from vibe_audit_enhanced import vibe_audit_enhanced

result = await vibe_audit_enhanced(
    project_path=".",
    primary_provider="agent_llm"  # 현재 에이전트의 LLM 사용
)
```

### 방법 2: API 키 사용

```python
# 자신의 OpenAI/Claude/기타 API 사용
result = await vibe_audit_enhanced(
    project_path=".",
    primary_provider="openai",  # 또는 "claude", "ollama", "deepseek"
    fallback_provider="claude"
)
```

### 방법 3: CLI 사용

```bash
# 에이전트의 LLM 사용 (API 키 불필요)
python vibe_audit_enhanced.py /path/to/project --provider agent_llm

# OpenAI 사용
python vibe_audit_enhanced.py /path/to/project --provider openai

# 로컬 Ollama 모델 사용
python vibe_audit_enhanced.py /path/to/project --provider ollama
```

---

## 🆕 v2.0의 새로운 기능

### 1. 🤖 에이전트 네이티브 통합
- **설정 불필요** - API 키 불필요
- 현재 에이전트의 LLM 연결 사용
- OpenCode, Hermes, OpenClaw와 원활한 통합

### 2. 🔌 다중 제공자 지원
- **Agent LLM** - 현재 에이전트 사용 (권장)
- **OpenAI** - GPT-4, GPT-4-turbo
- **Claude** - Claude-3 Sonnet/Opus
- **DeepSeek** - 비용 효율적인 대안
- **Qwen/통의천문** - 알리바바 모델
- **Ollama** - 로컬 모델 실행 (무료!)

### 3. 📦 의존성 보안 스캔
- 알려진 취약점 (CVE) 확인
- 오래된 의존성 감지
- 라이선스 규정 준수 확인
- 지원: npm, pip, maven, cargo, go mod

---

## 📊 도구 비교

| 도구 | 속도 | 정확도 | 기능 | API 키 | 최적 용도 |
|------|------|--------|------|--------|----------|
| `vibe_audit_enhanced` | 중속 | 높음 | 모든 기능 | 선택 | **프로덕션** |
| `vibe_audit_scan` | 빠름 | 중간 | 기본 | 불필요 | 빠른 확인 |
| `vibe_audit_multi_model` | 느림 | 최고 | AI 합의 | 필요 | 중요 프로젝트 |
| `vibe_audit_incremental` | 매우 빠름 | 중간 | Git 인식 | 선택 | CI/CD |

---

## 🌐 제공자 설정

### 에이전트 LLM (권장)
```python
# 설정 불필요! 바로 사용:
primary_provider="agent_llm"
```

### OpenAI
```bash
export OPENAI_API_KEY="sk-..."
```

### Claude
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Ollama (로컬, 무료)
```bash
# Ollama 설치
curl -fsSL https://ollama.com/install.sh | sh

# 모델 다운로드
ollama pull llama2

# 감사에서 사용
primary_provider="ollama"
```

---

## 🚨 위험 수준

| 수준 | 점수 | 조치 |
|------|------|------|
| ✅ 안전 | 0 | 게시 가능 |
| 🟢 낮음 | 1-19 | 사소한 문제, 검토 권장 |
| 🟡 보통 | 20-49 | 게시 전 검토 및 수정 |
| 🟠 높음 | 50-79 | 중요한 문제, 수정 필요 |
| 🔴 심각 | 80-100 | **게시 금지** |

---

## 🤝 지원되는 에이전트

- **OpenCode** - 네이티브 스킬
- **Hermes** - 플러그인
- **OpenClaw** - 모듈 가져오기
- **MCP Clients** - 프로토콜 지원

---

## 📞 지원

- **이슈**: [GitHub Issues](https://github.com/csmoove530/vibe-codebase-audit/issues)
- **문서**: SKILL.md 참조
- **예제**: examples/ 디렉토리 참조

---

**자신 있게 배포하십시오. 엄격하게 감사하십시오. 안심하고 코딩하십시오.** 🚀
