# TokenSaver (토큰세이버) API Reference

> **96% AI Cost Reduction / AI 비용 96% 절약**  
> Korean Context DB for AI Agents / AI 에이전트용 한국어 Context DB  
> Version / 버전: 3.1.0 | Python 3.8+

---

## Quick Start / 빠른 시작

```python
from 토큰세이버 import TokenSaver  # or: from tokensaver import TokenSaver

# Initialize / 클라이언트 초기화
client = TokenSaver()

# Save with auto-compression / 저장 (자동 압축)
client.save("project/memo", "Important memo content here", level=2)

# Search / 검색
results = client.find("important memo", level=2, limit=5)
```

---

## Main Classes / 주요 클래스

### `TokenSaver`

메인 클라이언트 클래스

```python
class TokenSaver(base_path: str = "~/.tokensaver")
```

#### 메서드

##### `save(uri, content, category, level)`

Context 저장 (자동 4단계 압축)

| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|--------|------|
| `uri` | `str` | - | 고유 식별자 |
| `content` | `str` | - | 원본 내용 |
| `category` | `str` | `"memories"` | 카테고리 |
| `level` | `0-3` | `2` | 압축 레벨 |

**반환값**: `Dict` - 저장된 데이터

**예시**:
```python
data = client.save("work/memo", "회의 내용...", category="work", level=2)
```

##### `save_batch(items)`

배치 저장

| 파라미터 | 타입 | 설명 |
|---------|------|------|
| `items` | `List[Dict]` | 저장할 항목 목록 |

**반환값**: `BatchResult` - 성공/실패 통계

**예시**:
```python
items = [
    {"uri": "a/1", "content": "내용1", "category": "work"},
    {"uri": "a/2", "content": "내용2", "category": "work"},
]
result = client.save_batch(items)
print(f"성공: {result.success}, 실패: {result.failed}")
```

##### `find(query, category, level, limit)`

한국어 검색

| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|--------|------|
| `query` | `str` | - | 검색어 |
| `category` | `str` | `None` | 카테고리 필터 |
| `level` | `0-3` | `2` | 반환할 압축 레벨 |
| `limit` | `int` | `10` | 최대 결과 수 |

**반환값**: `List[SearchResult]` - 검색 결과 목록

**예시**:
```python
results = client.find("마케팅 전략", level=0, limit=5)
for r in results:
    print(f"{r.uri}: {r.content} (관련도: {r.score})")
```

##### `export(output_path, category)`

백업 익스포트

| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|--------|------|
| `output_path` | `str` | - | 출력 파일 경로 |
| `category` | `str` | `None` | 특정 카테고리만 |

**반환값**: `bool` - 성공 여부

**예시**:
```python
client.export("backup_2026.json")
```

##### `import_backup(input_path, merge)`

백업 임포트

| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|--------|------|
| `input_path` | `str` | - | 입력 파일 경로 |
| `merge` | `bool` | `False` | 기존 데이터 병합 여부 |

**반환값**: `BatchResult` - 임포트 통계

**예시**:
```python
result = client.import_backup("backup_2026.json", merge=True)
print(f"임포트: {result.success}, 스킵: {result.failed}")
```

##### `auto_compress_old(days, target_level)`

오래된 데이터 자동 압축

| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|--------|------|
| `days` | `int` | `7` | 기준 일수 |
| `target_level` | `0-3` | `1` | 목표 압축 레벨 |

**반환값**: `Dict` - 압축 통계

**예시**:
```python
stats = client.auto_compress_old(days=7, target_level=1)
print(f"압축: {stats['compressed']}, 스킵: {stats['skipped']}")
```

---

## Compression Levels / 압축 레벨

| 레벨 | 이름 | 절감률 | 설명 | 용도 |
|------|------|--------|------|------|
| **0** | Abstract | **99%** | 키워드 5개만 | 빠른 미리보기 |
| **1** | Overview | **96%** | 핵심 문장 3개 | 일반 검색 |
| **2** | Summary | **91%** | 요약 + 키워드 | 기본 (권장) |
| **3** | Full | **0%** | 원본 전체 | 상세 보기 |

**예시**:
```python
# 동일한 내용, 다른 레벨
text = "인공지능과 머신러닝은 미래의 중요한 기술입니다. 많은 기업들이 투자하고 있어요."

l0 = client.compressor.compress(text, 0)  # "[인공지능][머신러닝][미래][기술][기업]"
l1 = client.compressor.compress(text, 1)  # "인공지능과 머신러닝은 미래의 중요한 기술입니다"
l2 = client.compressor.compress(text, 2)  # "[인공지능/머신러닝/미래/기술/기업] 인공지능과 머신러닝은 미래의 중요한 기술입니다 많은 기업들이 투자하고 있어요"
l3 = client.compressor.compress(text, 3)  # 원본 그대로
```

---

## Async API / 비동기 API

고성능 비동기 처리

### `save_async(uri, data)`

```python
await client.store.save_async("uri", data)
```

### `save_batch_async(items)`

```python
items = [{"uri": "a", "content": "내용"}, ...]
result = await client.save_batch_async(items)
```

**장점**: 
- I/O 블로킹 없음
- 100개 배치 저장 시 10x 속도 향상
- 메인 봇 응답성 유지

---

## Performance Tips / 성능 최적화 팁

### 1. orjson 설치 (3-10x 속도)

```bash
pip install orjson
```

### 2. aiofiles 설치 (비동기 I/O)

```bash
pip install aiofiles
```

### 3. 캐시 활용

```python
# 동일 텍스트 반복 호출 시 캐시 자동 사용
tokenizer.tokenize("같은 텍스트")  # 첫 호출
tokenizer.tokenize("같은 텍스트")  # 캐시 히트 (1000x 빠름)
```

---

## Examples / 예제

### Example 1: Basic Usage / 예제 1: 기본 사용

```python
from 토큰세이버 import TokenSaver

client = TokenSaver()

# 저장
client.save("diary/2026-03-29", "오늘은 좋은 날이었다...")

# 검색
results = client.find("좋은 날")
for r in results:
    print(f"{r.uri}: {r.content}")
```

### Example 2: Batch Processing / 예제 2: 배치 처리

```python
import asyncio

async def batch_process():
    items = [
        {"uri": f"batch/{i}", "content": f"내용{i}"}
        for i in range(100)
    ]
    
    result = await client.save_batch_async(items)
    print(f"처리 완료: {result.success}/{len(items)}")

asyncio.run(batch_process())
```

### Example 3: Backup & Restore / 예제 3: 백업/복원

```python
# 백업
client.export("backup.json")

# 다른 환경에서 복원
client2 = TokenSaver("~/.tokensaver2")
client2.import_backup("backup.json")
```

---

## Error Handling / 에러 처리

```python
from 토큰세이버 import TokenSaver

client = TokenSaver()

result = client.save_batch([
    {"uri": "a", "content": "내용"},
    {"uri": "", "content": ""},  # 잘못된 데이터
])

if result.failed > 0:
    for error in result.errors:
        print(f"에러: {error['uri']} - {error['error']}")
```

---

## References / 참고

- **GitHub**: https://github.com/dorongs/tokensaver
- **ClawHub**: https://clawhub.com/skills/tokensaver
- **문의**: support@tokensaver.pro