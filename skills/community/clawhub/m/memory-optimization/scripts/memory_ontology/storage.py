"""
Storage module for memory_ontology package.
Handles file I/O, locking, and graph compaction.
"""

import fcntl
import json
import time
from pathlib import Path
from typing import Any, Dict, List

from .config import (
    GRAPH_FILE,
    ONTOLOGY_DIR,
    LOCK_TIMEOUT_SECONDS,
)


def _acquire_lock_with_timeout(lock_file_path: Path, lock_type: int, timeout: float = LOCK_TIMEOUT_SECONDS) -> Any:
    """使用非阻塞 flock + 重试获取锁，超时后抛出明确异常。

    Args:
        lock_file_path: .lock 文件路径
        lock_type: fcntl.LOCK_EX 或 fcntl.LOCK_SH
        timeout: 超时秒数

    Returns:
        lock 文件对象（调用方用完后需 unlock 并 close）

    Raises:
        TimeoutError: 锁获取超时
    """
    import time as time_module
    lock_f = open(lock_file_path, 'a')
    start = time_module.time()
    interval = 0.1  # 初始重试间隔
    max_interval = 1.0
    while True:
        try:
            fcntl.flock(lock_f.fileno(), lock_type | fcntl.LOCK_NB)
            return lock_f
        except BlockingIOError:
            elapsed = time_module.time() - start
            if elapsed >= timeout:
                lock_f.close()
                lock_type_name = "EX" if lock_type == fcntl.LOCK_EX else "SH"
                raise TimeoutError(
                    f"KG lock timeout after {timeout}s waiting for {'exclusive' if lock_type == fcntl.LOCK_EX else 'shared'} lock. "
                    f"Another process may be holding the lock. "
                    f"File: {lock_file_path}"
                )
            time_module.sleep(interval)
            interval = min(interval * 1.5, max_interval)


def _write_to_graph(data: str):
    """写入 graph.jsonl（带文件锁）

    使用 fcntl.flock 实现原子写入，防止并发写入冲突。
    使用 'a' 模式避免 TOCTOU race（truncate-before-lock）。
    锁获取有 10 秒超时，防止死锁导致永久阻塞。
    """
    lock_file = GRAPH_FILE.with_suffix('.lock')
    lock_f = _acquire_lock_with_timeout(lock_file, fcntl.LOCK_EX)
    try:
        with open(GRAPH_FILE, 'a', encoding='utf-8') as f:
            f.write(data)
    finally:
        fcntl.flock(lock_f.fileno(), fcntl.LOCK_UN)
        lock_f.close()


def ensure_ontology_dir():
    """确保 ontology 目录存在"""
    ONTOLOGY_DIR.mkdir(parents=True, exist_ok=True)
    if not GRAPH_FILE.exists():
        GRAPH_FILE.touch()
        print(f"✓ Created graph file: {GRAPH_FILE}")


def load_all_entities() -> Dict[str, Dict]:
    """加载所有实体（带共享锁）

    使用 fcntl.LOCK_SH 共享锁，允许并发读取。
    与 _write_to_graph 的独占锁互斥，防止读到部分写入的数据。
    锁获取有 10 秒超时，防止死锁导致永久阻塞。
    """
    entities = {}

    if not GRAPH_FILE.exists():
        return entities

    lock_file = GRAPH_FILE.with_suffix('.lock')
    lock_f = _acquire_lock_with_timeout(lock_file, fcntl.LOCK_SH)
    try:
        # Read all records first
        records = []
        with open(GRAPH_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    operation = json.loads(line)
                    records.append(operation)
                except json.JSONDecodeError:
                    continue

        # Sort by timestamp to ensure correct order
        records.sort(key=lambda x: x.get('timestamp', ''))

        # Process in order: create first, then updates
        for operation in records:
            if operation.get('op') == 'create':
                if 'entity' in operation:
                    entity = operation['entity']
                    entities[entity['id']] = entity
                elif 'relation' in operation:
                    # Skip relation records
                    continue
            elif operation.get('op') == 'update':
                if 'entity' in operation:
                    entity = operation['entity']
                    entity_id = entity.get('id')
                    if entity_id:
                        if entity_id in entities:
                            # Update existing entity
                            entities[entity_id]['properties'].update(entity.get('properties', {}))
                            entities[entity_id]['updated'] = entity.get('updated', entities[entity_id].get('updated'))
                            # Also update type if missing
                            if not entities[entity_id].get('type') and entity.get('type'):
                                entities[entity_id]['type'] = entity['type']
                        else:
                            # Create from update (if no create record exists)
                            entities[entity_id] = entity
    finally:
        fcntl.flock(lock_f.fileno(), fcntl.LOCK_UN)
        lock_f.close()

    return entities


def load_all_relations() -> List[Dict]:
    """加载所有关系（带共享锁）"""
    relations = []

    if not GRAPH_FILE.exists():
        return relations

    lock_file = GRAPH_FILE.with_suffix('.lock')
    lock_f = _acquire_lock_with_timeout(lock_file, fcntl.LOCK_SH)
    try:
        with open(GRAPH_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    operation = json.loads(line)
                    if operation['op'] == 'relate':
                        relations.append(operation)
                except json.JSONDecodeError:
                    continue
    finally:
        fcntl.flock(lock_f.fileno(), fcntl.LOCK_UN)
        lock_f.close()

    return relations


def compact_graph() -> Dict[str, int]:
    """压缩 graph.jsonl — 保留每个实体的最新版本

    读取所有操作，只保留每个实体的最新版本（create 或 update），
    然后重写文件。可选的维护操作，用于减少文件大小。

    Returns:
        Dict with 'kept' (entities retained) and 'total_ops' (original operations)
    """

    if not GRAPH_FILE.exists():
        return {'kept': 0, 'total_ops': 0}

    # Step 1: Load with read lock — collect entities and relations
    entities: Dict[str, Dict] = {}
    relations: List[Dict] = []
    total_ops = 0

    lock_file = GRAPH_FILE.with_suffix('.lock')
    lock_f = _acquire_lock_with_timeout(lock_file, fcntl.LOCK_SH)
    try:
        with open(GRAPH_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    op = json.loads(line)
                    total_ops += 1
                    if op.get('op') == 'create':
                        entities[op['entity']['id']] = op['entity']
                    elif op.get('op') == 'update':
                        eid = op['entity']['id']
                        if eid in entities:
                            entities[eid]['properties'].update(op['entity']['properties'])
                            entities[eid]['updated'] = op['entity'].get('updated', op.get('timestamp', ''))
                    elif op.get('op') == 'relate':
                        relations.append(op)
                except json.JSONDecodeError:
                    continue
    finally:
        fcntl.flock(lock_f.fileno(), fcntl.LOCK_UN)
        lock_f.close()

    if total_ops == len(entities) + len(relations):
        # No compaction needed
        return {'kept': len(entities), 'total_ops': total_ops}

    # Step 2: Write compacted version atomically
    compacted_lines = 0
    tmp_file = GRAPH_FILE.with_suffix('.jsonl.tmp')
    tmp_lock = GRAPH_FILE.with_suffix('.tmp.lock')

    tmp_lock_f = open(tmp_lock, 'a')
    try:
        fcntl.flock(tmp_lock_f.fileno(), fcntl.LOCK_EX)
        try:
            with open(tmp_file, 'w', encoding='utf-8') as f:
                for entity in entities.values():
                    op = {'op': 'create', 'entity': entity, 'timestamp': entity.get('updated', entity.get('timestamp', ''))}
                    f.write(json.dumps(op, ensure_ascii=False) + '\n')
                    compacted_lines += 1
                for rel in relations:
                    f.write(json.dumps(rel, ensure_ascii=False) + '\n')
                    compacted_lines += 1
            # Atomic rename
            tmp_file.rename(GRAPH_FILE)
        finally:
            fcntl.flock(tmp_lock_f.fileno(), fcntl.LOCK_UN)
    finally:
        tmp_lock_f.close()
        if tmp_lock.exists():
            tmp_lock.unlink()

    return {'kept': len(entities), 'total_ops': total_ops, 'compacted_to': compacted_lines}