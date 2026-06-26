# 베이지안 업데이트 방법론 (Phase 2)

## 개요

Phase 1에서 형성된 prior를 일상 대화에서 관찰되는 의사결정 데이터로 지속 업데이트한다.

```
posterior ∝ prior × likelihood
```

## Prior 표현

각 차원을 Beta 분포로 모델링:

```
prior_i ~ Beta(α_i, β_i)
```

- α: 양방향(자율/깊이/혁신) 관찰 수
- β: 음방향(구조/폭/안정) 관찰 수
- Phase 1 결과 → 초기 α, β 설정 (예: strong prior = α=8, β=2)

## Likelihood 계산

일상 대화에서 벡터 추출 시:

```python
# 관찰된 벡터 v의 i번째 컴포넌트
if v.direction[i] > 0:
    α_i += v.intensity * v.confidence
else:
    β_i += v.intensity * v.confidence
```

### Confidence 가중치

- confidence < 0.3 → 무시 (노이즈로 판단)
- confidence 0.3-0.7 → 가중치 0.5 적용
- confidence > 0.7 → 전체 가중치 적용

```python
weight = 0 if conf < 0.3 else (0.5 if conf < 0.7 else 1.0)
effective_update = intensity * weight
```

## Posterior 계산

```
posterior_i = Beta(α_i + Δα, β_i + Δβ)
```

- 기대값: E[θ_i] = α_i / (α_i + β_i)
- 이것이 해당 차원의 현재 방향성 추정치

### 자화 벡터 도출

```python
magnetization = [
    (α_x - β_x) / (α_x + β_x),  # X: 자율↔구조
    (α_y - β_y) / (α_y + β_y),  # Y: 깊이↔폭
    (α_z - β_z) / (α_z + β_z),  # Z: 혁신↔안정
]
```

범위: [-1, +1] 각 축

## 방향 전환 감지

### 기준
연속 3개 이상의 벡터가 기존 posterior와 반대 방향(cosine similarity < -0.3)이면 **방향 전환 시그널** 발생.

### 대응
1. timeline.md에 전환 이벤트 기록
2. prior의 α, β를 감쇠 (× 0.7) → 새 데이터에 더 민감하게
3. 사용자에게 알림: "최근 의사결정 패턴이 기존 방향과 달라지고 있습니다"

## 데이터 오염 방어

### 1. Strong Prior Anchor
Phase 1의 변증법적 토론 결과는 α, β 초기값이 크므로 (8-10), 소수의 노이즈에 흔들리지 않음.

### 2. Outlier Detection
기존 posterior에서 3σ 이상 벗어나는 벡터는 자동 플래그:
- confidence를 자동으로 0.3으로 하향
- 별도 마킹: `tags: [outlier]`

### 3. Temporal Weighting
오래된 벡터는 가중치 감쇠:
```python
decay = 0.95 ** (days_since_observation / 30)  # 월 5% 감쇠
```

### 4. Context Filtering
감정적 극단 상태(스트레스, 피로)에서의 의사결정은 confidence 하향:
- 감정 강도가 높고 평소 패턴과 크게 다르면 → `context: emotional` 태그
- 이 벡터들은 별도 분석 가능하나 주 posterior에는 약하게 반영

## 수렴 지표

### 자화도 (Magnetization)
```
M = |Σ(v_i × w_i)| / N
```
- M → 1: 모든 벡터가 같은 방향 (강한 정체성)
- M → 0: 벡터들이 분산 (탐색 중 / 혼란)

### Entropy
```
H = -Σ p_i log(p_i)  (클러스터 분포에 대해)
```
- H 낮음: 소수 클러스터에 집중 (명확한 방향)
- H 높음: 다양한 클러스터에 분산 (다면적)

## 업데이트 주기

- 벡터 추출: 매 대화 (실시간)
- Posterior 재계산: 벡터 5개 축적마다 또는 주 1회
- 자화도 리포트: 월 1회 또는 요청 시
- 방향 전환 체크: 매 posterior 업데이트 시
