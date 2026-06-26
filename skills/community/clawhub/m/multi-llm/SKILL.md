---
name: multi-llm
description: >
  Use this skill when the agent needs the highest-quality answer by querying
  multiple LLM providers (Claude, Gemini, GPT, Ollama) in parallel and synthesizing
  the results via Mixture of Agents (MoA). Trigger on: complex reasoning, high-stakes
  decisions, code review, strategic planning, research, or any task where a single
  model's quality is insufficient. Improves actual output quality — not just showing
  multiple answers side-by-side.
metadata:
  {
    "openclaw": {
      "emoji": "🧠",
      "requires": {
        "bins": ["uv"],
        "env": []
      }
    }
  }
---

## How It Works

**Mixture of Agents (MoA)** pattern:
1. All available *proposer* models query the task in parallel (`asyncio.gather`)
2. A *synthesizer* model combines the best elements of all responses
3. Optionally repeat for multiple rounds (higher quality, more latency)

Providers are **auto-detected** from environment variables — no config needed.

| Env Var | Provider | Default models used |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude | claude-sonnet-4-6, claude-haiku-4-5 |
| `OPENAI_API_KEY` | OpenAI | gpt-4o, gpt-4o-mini |
| `GEMINI_API_KEY` | Gemini | gemini-2.0-flash, gemini-1.5-pro |
| `OLLAMA_HOST` (optional) | Ollama | llama3, mistral (auto-listed) |

## Usage

```bash
uv run {baseDir}/scripts/ensemble.py \
  --prompt "분석할 태스크 또는 질문" \
  [--models claude-sonnet-4-6,gpt-4o,gemini-2.0-flash] \
  [--synthesizer claude-opus-4-7] \
  [--rounds 1] \
  [--format text|json] \
  [--output result.txt]
```

**Key options:**
- `--models` / `-m` — 쉼표 구분 모델 목록 (생략 시 감지된 모델 자동 선택)
- `--synthesizer` / `-s` — 합성 모델 지정 (생략 시 가장 강한 모델 자동 선택)
- `--rounds` / `-r` — MoA 반복 횟수. 1=빠름, 2=품질 최대 (기본: 1)
- `--format` — `text` (기본) 또는 `json` (모델별 응답 포함)
- `--output` / `-o` — 파일로 저장 (생략 시 stdout)

## When to Use

- 복잡한 추론, 전략 분석, 의사결정이 필요할 때
- 단일 모델 응답의 품질이 부족하다고 판단될 때
- 코드 리뷰, 버그 분석, 리서치 요약
- 트레이딩 신호 품질 향상 등 정확도가 중요한 작업

## Notes

- API 키 없는 프로바이더는 조용히 제외됨 (오류 아님)
- 한 모델이 실패해도 나머지로 진행
- 자세한 튜닝 옵션: [references/moa-guide.md](references/moa-guide.md)
