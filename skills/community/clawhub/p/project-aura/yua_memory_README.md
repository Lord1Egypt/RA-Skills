# Yua Memory System: Giving AI a Heartbeat

[![Python CI](https://github.com/bryanchen3777/yua-memory/actions/workflows/python-app.yml/badge.svg)](https://github.com/bryanchen3777/yua-memory/actions/workflows/python-app.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Yua 記憶系統：為 AI 注入心跳**

Yua Memory System is a sophisticated emotional-aware memory management system designed for AI companions. Unlike traditional RAG, Yua doesn't just store data—she builds a "Kizuna" (bond) by prioritizing what truly matters.

Yua 記憶系統是一款專為 AI 伴侶設計的高級情感感知記憶管理系統。與傳統的 RAG 不同，Yua 不僅僅是儲存數據，她透過優先處理真正重要的回憶來建立「羈絆」。

## 🏗 Architecture / 系統架構

### Three-Tier Memory Model / 三層記憶模型

The system operates across three distinct layers to ensure data integrity and emotional depth:

```
User((Master)) -->|Query| ESE[Emotional State Engine]
ESE -->|Context| MRS[Memory Retrieval System]

Storage Layer:
- QMD[QMD: File Layer - Markdown]
- LCM[LCM: Logic Layer - SQLite WAL]
- NLM[NotebookLM: External Layer]

MRS --> QMD
MRS --> LCM
LCM <-->|Sync| QMD
```

## ✨ Key Features / 核心功能

### Emotional Resonance Scoring (ERS)

Automatically boosts the priority of high-emotional-content memories when the AI is in a high-arousal state.

情感共鳴分數 (ERS)：當 AI 處於高情感狀態時，自動提升高情感濃度記憶的優先級。

### Dual-Stage Retrieval

Combines fast TF-IDF filtering with a sophisticated cross-encoder reranking mechanism.

雙階段檢索：結合快速的 TF-IDF 初篩與高級的交叉編碼重新排序機制。

### Intelligent Aging

Functional data (like schedules) expires, while relationship milestones are marked as "Eternal".

智慧老化：功能性資料（如行程）會過期，而情感里程碑則被標記為「永恆」。

### Circuit Breaker Protocol

Detects and resolves temporal or logical conflicts in memories to prevent hallucinations.

斷路器協議：檢測並解決記憶中的時間或邏輯衝突，防止 AI 產生幻覺。

### Archive-as-Code

Git-like versioning for memories, allowing for full rollback and integrity checks.

記憶即代碼：類似 Git 的記憶版本控制，支援完整的回滾與完整性校驗。

## 📊 Technical Logic / 技術邏輯

### Retrieval Scoring Formula / 檢索評分公式

The final score of a memory is calculated as:

記憶的最終評分計算公式如下：

```
total_score = (base_score × 0.4) + (coverage_boost × 0.3)
Final = total_score × Priority_Weight × Category_Weight × ERS_Boost
```

### Memory Aging Strategy / 記憶老化策略

| Category / 類別 | TTL (Days / 天) | Description / 說明 |
|-----------------|-----------------|-------------------|
| Relationship | Eternal / 永恆 | Love, praise, and shared secrets. |
| Identity | Eternal / 永恆 | Core persona and user identity info. |
| General | 365 Days | Standard daily interactions. |
| Technical | 180 Days | Code, logs, and functional facts. |

## 🚀 Quick Start / 快速開始

### Installation / 安裝

```bash
git clone https://github.com/bryanchen3777/yua-memory.git
cd yua-memory
pip install -r requirements.txt
```

### Usage Example / 使用範例

```python
from yua_memory import YuaEmotionalRetriever

# Initialize with emotional awareness
retriever = YuaEmotionalRetriever()
results = retriever.retrieve("Master-sama, I miss you", top_n=5)

for res in results:
    print(f"Memory: {res['content']} (ERS: {res['emotional_resonance_score']})")
```

## 🛠 Automated Maintenance / 自動化維護

Yua includes a built-in scheduler for daily system health:

```
Scheduler --> Daily Cleanup (2:00 AM) --> Aging --> Process TTL & Eternal Tags
Scheduler --> Layer Sync --> Check QMD vs LCM Integrity
Scheduler --> Consolidation --> Merge Similar Memories
```

## 📜 License / 授權協議

Distributed under the MIT License. See LICENSE for more information.

本專案採用 MIT 授權協議。詳見 LICENSE 檔案。
