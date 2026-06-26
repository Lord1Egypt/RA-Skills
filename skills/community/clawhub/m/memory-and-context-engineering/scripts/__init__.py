# Agent Memory System
# Copyright (C) 2024 kiwifruit
#
# This file is part of Agent Memory System.
#
# Agent Memory System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Agent Memory System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Agent Memory System.  If not, see <https://www.gnu.org/licenses/>.


"""
Agent Memory System - Scripts Package

为智能体提供记忆能力的核心基础设施
"""

__version__ = "3.0.0"

# 核心模块
from .type_defs import *
from .type_defs import SemanticBucketType
from .perception import PerceptionMemoryStore
from .short_term import SemanticBucket, ShortTermMemoryManager, AsynchronousExtractor
from .short_term_insight import (
    TopicCluster,
    TopicRelation,
    ExtractionDecision,
    ShortTermInsightResult,
    ShortTermInsightAnalyzer,
)
from .long_term import LongTermMemoryManager
from .context_reconstructor import (
    QualityEvaluator,
    WeightAdapter,
    ContextReconstructor,
)
from .insight_module import InsightPool, DetachedObserver, InsightModule
from .state_capture import GlobalStateCapture
from .type_defs import GlobalState, GlobalStateSnapshot
from .heat_manager import HeatManager
from .conflict_resolver import ConflictResolver
from .privacy import (
    ConsentStatus,
    DataSensitivity,
    StoragePolicy,
    RetentionPeriod,
    ConsentRecord,
    PrivacyConfig,
    DataClassification,
    PrivacyAuditLog,
    SensitiveDataDetector,
    PrivacyManager,
    PRIVACY_NOTICE_TEMPLATE,
)
from .encryption import (
    EncryptedData,
    KeyInfo,
    EncryptionConfig,
    KeyManager,
    DataEncryptor,
    EncryptedFileStorage,
    encrypt_data_with_password,
    decrypt_data_with_password,
    generate_encryption_key,
    CRYPTO_AVAILABLE,
)
from .memory_index import (
    TextProcessor,
    MemoryIndexer,
    MemoryDocument,
    SearchResult,
    IndexStats,
)
from .incremental_sync import (
    SyncStatus,
    SyncState,
    ExtractionRecord,
    SyncStats,
    IncrementalSync,
)
from .credential_manager import (
    CredentialRecord,
    CredentialStorage,
    CredentialManager,
    create_credential_manager,
)
from .chain_reasoning import (
    ChainReasoningEnhancer,
    create_chain_reasoning_enhancer,
    extract_causal_chains,
)
from .knowledge_gap_identifier import (
    KnowledgeGapIdentifier,
    KnowledgeType,
    GapAnalysisResult,
    IdentifiedGap,
)
from .retrieval_decision_engine import (
    RetrievalDecisionEngine,
    RetrievalNeed,
    RetrievalDecision,
)
from .causal_chain_extractor import (
    CausalChainExtractor,
    ExtractedCausalChain,
)
from .context_orchestrator import (
    ContextOrchestrator,
    create_context_orchestrator,
    ContextCompressor,
    CompressionStrategy,
    PriorityResolver,
    MetadataQualityAssessor,
    CustomTypeLifecycleManager,
    UsageMonitor,
    LRUCache,
    PerformanceMonitor,
    BatchProcessor,
)
# 链模块
from .chains import (
    ExtractedCausalChain,
    ExtractedLogicChain,
    ExtractedOperationChain,
    ExtractedNarrativeChain,
    ExtractedTimeChain,
    ChainBuffer,
    ChainType,
    BaseExtractedChain,
)
# Redis 基础设施层
from .redis_adapter import (
    REDIS_AVAILABLE,
    RedisConfig,
    RedisKeyBuilder,
    RedisAdapter,
    create_redis_adapter,
)
from .short_term_redis import (
    ShortTermMemoryItemRedis,
    ShortTermRedisConfig,
    ShortTermMemoryRedis,
    create_short_term_redis,
)
from .token_budget import (
    TokenType,
    BudgetPolicy,
    TokenBudgetConfig,
    TokenCounter,
    TokenBudgetManager,
    create_token_budget_manager,
)
# Context Orchestrator（总控层）
from .context_orchestrator import (
    ContextPriority,
    ContextSource,
    ContextBlock,
    ContextConfig,
    PreparedContext,
    ContextOrchestrator,
    create_context_orchestrator,
)
from .type_defs import ContextPackage
# 异步写入（性能优化）
from .async_writer import (
    AsyncWriter,
    WriterConfig,
    WriterStats,
    get_async_writer,
    shutdown_async_writer,
)
from .batched_writer import (
    BatchedWriter,
    BatchedWriterConfig,
    BatchedWriterStats,
    get_long_term_writer,
    get_state_sync_writer,
)

__all__ = [
    # 版本
    "__version__",
    # 类型
    "types",
    "SemanticBucketType",
    # 感知记忆
    "PerceptionMemoryStore",
    # 短期记忆
    "SemanticBucket",
    "ShortTermMemoryManager",
    "AsynchronousExtractor",
    # 短期记忆洞察
    "TopicCluster",
    "TopicRelation",
    "ExtractionDecision",
    "ShortTermInsightResult",
    "ShortTermInsightAnalyzer",
    # 长期记忆
    "LongTermMemoryManager",
    # 上下文重构
    "QualityEvaluator",
    "WeightAdapter",
    "ContextReconstructor",
    # 洞察模块
    "InsightPool",
    "DetachedObserver",
    "InsightModule",
    # 状态捕捉
    "GlobalStateCapture",
    "GlobalState",
    "GlobalStateSnapshot",
    # 冷热度管理
    "HeatManager",
    # 冲突解决
    "ConflictResolver",
    # 隐私配置
    "ConsentStatus",
    "DataSensitivity",
    "StoragePolicy",
    "RetentionPeriod",
    "ConsentRecord",
    "PrivacyConfig",
    "DataClassification",
    "PrivacyAuditLog",
    "SensitiveDataDetector",
    "PrivacyManager",
    "PRIVACY_NOTICE_TEMPLATE",
    # 加密模块
    "EncryptedData",
    "KeyInfo",
    "EncryptionConfig",
    "KeyManager",
    "DataEncryptor",
    "EncryptedFileStorage",
    "encrypt_data_with_password",
    "decrypt_data_with_password",
    "generate_encryption_key",
    "CRYPTO_AVAILABLE",
    # 记忆索引
    "TextProcessor",
    "MemoryIndexer",
    "MemoryDocument",
    "SearchResult",
    "IndexStats",
    # 增量同步
    "SyncStatus",
    "SyncState",
    "ExtractionRecord",
    "SyncStats",
    "IncrementalSync",
    # 凭证管理
    "CredentialRecord",
    "CredentialStorage",
    "CredentialManager",
    "create_credential_manager",
    # 链式推理增强
    "ChainReasoningEnhancer",
    "create_chain_reasoning_enhancer",
    "extract_causal_chains",
    # 链模块
    "ExtractedCausalChain",
    "ExtractedLogicChain",
    "ExtractedOperationChain",
    "ExtractedNarrativeChain",
    "ExtractedTimeChain",
    "ChainBuffer",
    "ChainType",
    "BaseExtractedChain",
    # Redis 基础设施层
    "REDIS_AVAILABLE",
    "RedisConfig",
    "RedisKeyBuilder",
    "RedisAdapter",
    "create_redis_adapter",
    "ShortTermMemoryItemRedis",
    "ShortTermRedisConfig",
    "ShortTermMemoryRedis",
    "create_short_term_redis",
    "TokenType",
    "BudgetPolicy",
    "TokenBudgetConfig",
    "TokenCounter",
    "TokenBudgetManager",
    "create_token_budget_manager",
    # Context Orchestrator
    "ContextPriority",
    "ContextSource",
    "ContextBlock",
    "ContextConfig",
    "PreparedContext",
    "ContextOrchestrator",
    "create_context_orchestrator",
    "ContextCompressor",
    "CompressionStrategy",
    "PriorityResolver",
    "MetadataQualityAssessor",
    "CustomTypeLifecycleManager",
    "UsageMonitor",
    "LRUCache",
    "PerformanceMonitor",
    "BatchProcessor",
    "ContextPackage",
    # 异步写入（性能优化）
    "AsyncWriter",
    "WriterConfig",
    "WriterStats",
    "get_async_writer",
    "shutdown_async_writer",
    "BatchedWriter",
    "BatchedWriterConfig",
    "BatchedWriterStats",
    "get_long_term_writer",
    "get_state_sync_writer",
]
