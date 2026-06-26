# MoA (Mixture of Agents) 상세 가이드

## 패턴 개요

MoA는 여러 LLM이 동일한 태스크에 대해 독립적으로 응답하고, synthesizer가 이를 통합하는 앙상블 기법.
단일 모델 대비 벤치마크(MMLU, HumanEval, GSM8K)에서 일관된 품질 향상이 입증됨.

```
Prompt ──┬──▶ Claude    ─┐
         ├──▶ GPT-4o    ─┼──▶ Synthesizer ──▶ 최종 답변
         ├──▶ Gemini    ─┘
         └──▶ Ollama   ─
```

---

## 라운드 수 선택

| `--rounds` | 특성 | 권장 용도 |
|---|---|---|
| 1 | 빠름 (~proposer 지연 + synth) | 일반 태스크, 실시간 응답 |
| 2 | 품질 최대화 | 복잡한 추론, 전략 수립, 코드 리뷰 |
| 3+ | 수익 체감, 비용↑ | 거의 불필요 |

2라운드: 1라운드 합성 결과를 다시 proposer들에 보내 "개선"을 요청 → 더 정제된 최종 합성.

---

## 모델 조합 추천

### 범용 (기본)
```
--models claude-sonnet-4-6,gpt-4o,gemini-2.0-flash
```

### 추론/분석 특화
```
--models claude-opus-4-7,gpt-4o,gemini-1.5-pro --rounds 2
```

### 코드 리뷰
```
--models claude-sonnet-4-6,gpt-4o --synthesizer claude-opus-4-7
```

### 비용 절감 (빠른 모델만)
```
--models claude-haiku-4-5-20251001,gpt-4o-mini,gemini-2.0-flash
```

### 로컬 전용 (API 키 없이)
```
OLLAMA_HOST=http://localhost:11434
--models llama3,mistral,qwen2
```

---

## Synthesizer 선택 기준

Synthesizer는 proposer들보다 강한 모델을 쓸수록 효과적.

우선순위 (자동 감지 시):
1. `claude-opus-4-7` (가장 강력, 비용 높음)
2. `claude-sonnet-4-6`
3. `gpt-4o`
4. `gemini-1.5-pro`

강제 지정:
```bash
--synthesizer claude-opus-4-7
```

---

## JSON 출력 형식

`--format json` 사용 시:
```json
{
  "synthesis": "최종 합성 답변",
  "synthesizer": "anthropic/claude-sonnet-4-6",
  "rounds": 2,
  "proposer_responses": [
    {
      "model": "claude-haiku-4-5-20251001",
      "provider": "anthropic",
      "content": "모델 응답...",
      "error": null
    }
  ]
}
```

JSON 출력 활용 예: 개별 모델 응답 비교, 품질 로깅, 파이프라인 연동.

---

## 환경변수 설정

```bash
# Linux/macOS
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
export GEMINI_API_KEY=AI...

# Ollama (선택)
export OLLAMA_HOST=http://localhost:11434
```

OpenClaw에서는 `openclaw.json`의 `env` 섹션 또는 `.env` 파일로 설정 가능.

---

## 트레이딩 봇 연동 예시

복잡한 시장 분석 신호를 여러 모델로 크로스 검증:

```bash
uv run ensemble.py \
  --prompt "현재 BTC/USDT 4시간봉 RSI=68, MACD 골든크로스, 거래량 20% 증가. 진입 여부와 손절/목표가를 분석해줘." \
  --models claude-sonnet-4-6,gpt-4o,gemini-2.0-flash \
  --synthesizer claude-opus-4-7 \
  --rounds 2 \
  --format json \
  --output signal_analysis.json
```

---

## 성능 vs 비용

| 구성 | 품질 | 비용 | 지연 |
|---|---|---|---|
| 단일 모델 | 기준 | 1x | 1x |
| 3 proposer + synth (1라운드) | +15~25% | ~4x | ~1.5x (병렬) |
| 3 proposer + synth (2라운드) | +25~40% | ~8x | ~3x |

병렬 처리 덕분에 지연 증가는 모델 수에 비례하지 않음.
