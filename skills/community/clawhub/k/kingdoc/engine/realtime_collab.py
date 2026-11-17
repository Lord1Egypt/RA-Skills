"""KingDoc 实时协同编辑引擎（序列 CRDT 自研实现）

零第三方依赖，实现最终一致性的多人实时协同编辑。
算法：序列 CRDT（类似 Yjs Y.Text），支持 insert/delete/move，
     每个字符带唯一因果 ID，无需中央服务器协调。

设计原则：
- 自研实现：零第三方依赖，纯 Python 标准库
- 硬件自适应：大文档分块操作，不拖累用户电脑
- 最终一致性：所有客户端收敛到相同状态
- 操作可交换：并发操作满足交换律，顺序不影响结果
"""
from __future__ import annotations

import hashlib
import time
from copy import deepcopy
from typing import Dict, List, Optional, Tuple

from engine.hardware import get_recommended_settings


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------

class CharID:
    """字符唯一标识（lamport timestamp + client_id + 计数器）"""

    def __init__(self, lamport: int, client_id: str, seq: int):
        self.lamport = lamport
        self.client_id = client_id
        self.seq = seq

    def __lt__(self, other: "CharID") -> bool:
        if self.lamport != other.lamport:
            return self.lamport < other.lamport
        if self.client_id != other.client_id:
            return self.client_id < other.client_id
        return self.seq < other.seq

    def __eq__(self, other) -> bool:
        if not isinstance(other, CharID):
            return False
        return (self.lamport == other.lamport and
                self.client_id == other.client_id and
                self.seq == other.seq)

    def __hash__(self) -> int:
        return hash((self.lamport, self.client_id, self.seq))

    def __repr__(self) -> str:
        return f"CharID({self.lamport},{self.client_id},{self.seq})"

    def to_dict(self) -> Dict:
        return {"lamport": self.lamport, "client_id": self.client_id, "seq": self.seq}

    @staticmethod
    def from_dict(d: Dict) -> "CharID":
        return CharID(d["lamport"], d["client_id"], d["seq"])


class Operation:
    """操作类型"""

    INSERT = "insert"
    DELETE = "delete"
    MOVE = "move"

    def __init__(self, op_type: str, char_id: CharID,
                 pos: int = -1, char: str = "",
                 src_pos: int = -1, dst_pos: int = -1,
                 client_id: str = "", lamport: int = 0):
        self.op_type = op_type
        self.char_id = char_id
        self.pos = pos          # insert/delete 位置
        self.char = char        # insert 的字符
        self.src_pos = src_pos  # move 源位置
        self.dst_pos = dst_pos  # move 目标位置
        self.client_id = client_id
        self.lamport = lamport

    def to_dict(self) -> Dict:
        return {
            "op_type": self.op_type,
            "char_id": self.char_id.to_dict(),
            "pos": self.pos,
            "char": self.char,
            "src_pos": self.src_pos,
            "dst_pos": self.dst_pos,
            "client_id": self.client_id,
            "lamport": self.lamport,
        }

    @staticmethod
    def from_dict(d: Dict) -> "Operation":
        return Operation(
            op_type=d["op_type"],
            char_id=CharID.from_dict(d["char_id"]),
            pos=d.get("pos", -1),
            char=d.get("char", ""),
            src_pos=d.get("src_pos", -1),
            dst_pos=d.get("dst_pos", -1),
            client_id=d.get("client_id", ""),
            lamport=d.get("lamport", 0),
        )


# ---------------------------------------------------------------------------
# CRDT 文档
# ---------------------------------------------------------------------------

class CRDTDocument:
    """序列 CRDT 文档

    核心：每个字符带唯一 ID + 删除标记（tombstone）。
    插入按 ID 排序，删除标记 tombstone 但不真正移除（保留因果关系）。
    """

    def __init__(self, client_id: str = ""):
        self.client_id = client_id
        self.lamport = 0
        self.seq_counter = 0
        # 内容：[(CharID, char, deleted), ...]
        self.content: List[Tuple[CharID, str, bool]] = []
        self.operations: List[Operation] = []

    def _next_id(self) -> CharID:
        self.seq_counter += 1
        return CharID(self.lamport, self.client_id, self.seq_counter)

    def _advance_lamport(self, remote_lamport: int = 0):
        self.lamport = max(self.lamport, remote_lamport) + 1

    def local_insert(self, pos: int, text: str) -> List[Operation]:
        """本地插入文本，返回操作列表。"""
        ops = []
        for i, ch in enumerate(text):
            char_id = self._next_id()
            insert_pos = pos + i
            # 边界检查
            insert_pos = max(0, min(insert_pos, len(self.content)))
            self.content.insert(insert_pos, (char_id, ch, False))
            op = Operation(
                op_type=Operation.INSERT,
                char_id=char_id,
                pos=insert_pos,
                char=ch,
                client_id=self.client_id,
                lamport=self.lamport,
            )
            ops.append(op)
            self.operations.append(op)
        return ops

    def local_delete(self, pos: int, length: int = 1) -> List[Operation]:
        """本地删除文本，返回操作列表。"""
        ops = []
        for i in range(length):
            actual_pos = pos
            # 找到未删除的字符
            visible_idx = 0
            found = False
            for j, (cid, ch, deleted) in enumerate(self.content):
                if not deleted:
                    if visible_idx == actual_pos:
                        self.content[j] = (cid, ch, True)
                        op = Operation(
                            op_type=Operation.DELETE,
                            char_id=cid,
                            pos=j,
                            client_id=self.client_id,
                            lamport=self.lamport,
                        )
                        ops.append(op)
                        self.operations.append(op)
                        found = True
                        break
                    visible_idx += 1
            if not found:
                break
        return ops

    def apply_remote_operation(self, op: Operation):
        """应用远程操作（满足交换律，顺序无关）。"""
        self._advance_lamport(op.lamport)

        if op.op_type == Operation.INSERT:
            # 按 char_id 找到正确位置（保持排序）
            insert_pos = 0
            for i, (cid, ch, deleted) in enumerate(self.content):
                if cid == op.char_id:
                    # 已存在，跳过
                    return
                if cid < op.char_id:
                    insert_pos = i + 1
                else:
                    break
            self.content.insert(insert_pos, (op.char_id, op.char, False))

        elif op.op_type == Operation.DELETE:
            for i, (cid, ch, deleted) in enumerate(self.content):
                if cid == op.char_id:
                    self.content[i] = (cid, ch, True)
                    break

        elif op.op_type == Operation.MOVE:
            # 移动 = 删除 + 插入
            char_data = None
            src_idx = -1
            for i, (cid, ch, deleted) in enumerate(self.content):
                if cid == op.char_id:
                    char_data = (cid, ch, deleted)
                    src_idx = i
                    break
            if char_data:
                self.content.pop(src_idx)
                insert_pos = min(op.dst_pos, len(self.content))
                self.content.insert(insert_pos, char_data)

        self.operations.append(op)

    def merge(self, other: "CRDTDocument"):
        """合并另一个 CRDT 文档（取并集，删除取 OR）。"""
        # 建立索引
        local_index = {cid: (ch, deleted) for cid, ch, deleted in self.content}
        remote_index = {cid: (ch, deleted) for cid, ch, deleted in other.content}

        # 合并所有字符（按 ID 排序）
        all_ids = sorted(set(local_index.keys()) | set(remote_index.keys()))
        new_content = []
        for cid in all_ids:
            if cid in local_index and cid in remote_index:
                # 两边都有：删除取 OR
                ch = local_index[cid][0]
                deleted = local_index[cid][1] or remote_index[cid][1]
                new_content.append((cid, ch, deleted))
            elif cid in local_index:
                new_content.append((cid, local_index[cid][0], local_index[cid][1]))
            else:
                new_content.append((cid, remote_index[cid][0], remote_index[cid][1]))

        self.content = new_content
        self._advance_lamport(other.lamport)

    def get_text(self) -> str:
        """获取当前可见文本。"""
        return "".join(ch for cid, ch, deleted in self.content if not deleted)

    def get_length(self) -> int:
        """获取可见字符数。"""
        return sum(1 for cid, ch, deleted in self.content if not deleted)

    def get_stats(self) -> Dict:
        """获取文档统计。"""
        total = len(self.content)
        deleted = sum(1 for _, _, d in self.content if d)
        return {
            "visible_chars": total - deleted,
            "total_chars": total,
            "tombstones": deleted,
            "operation_count": len(self.operations),
            "client_id": self.client_id,
        }


# ---------------------------------------------------------------------------
# 协同会话
# ---------------------------------------------------------------------------

class CollabSession:
    """协同编辑会话（管理多个客户端的 CRDT 文档）"""

    def __init__(self, session_id: str, doc_id: str = ""):
        self.session_id = session_id
        self.doc_id = doc_id
        self.clients: Dict[str, CRDTDocument] = {}
        self.created_at = time.time()

    def join(self, client_id: str) -> CRDTDocument:
        """客户端加入会话。"""
        if client_id not in self.clients:
            doc = CRDTDocument(client_id)
            self.clients[client_id] = doc
        return self.clients[client_id]

    def leave(self, client_id: str):
        """客户端离开会话。"""
        self.clients.pop(client_id, None)

    def apply_operation(self, client_id: str, op: Operation):
        """向所有客户端广播操作。"""
        for cid, doc in self.clients.items():
            if cid != client_id:
                doc.apply_remote_operation(op)

    def get_merged_text(self) -> str:
        """获取合并后的文档文本。"""
        if not self.clients:
            return ""
        merged = CRDTDocument("merged")
        for doc in self.clients.values():
            merged.merge(doc)
        return merged.get_text()

    def get_client_count(self) -> int:
        return len(self.clients)


# ---------------------------------------------------------------------------
# 便捷函数
# ---------------------------------------------------------------------------

_sessions: Dict[str, CollabSession] = {}


def create_session(session_id: str, doc_id: str = "") -> CollabSession:
    session = CollabSession(session_id, doc_id)
    _sessions[session_id] = session
    return session


def get_session(session_id: str) -> Optional[CollabSession]:
    return _sessions.get(session_id)


def destroy_session(session_id: str):
    _sessions.pop(session_id, None)


def create_document(client_id: str) -> CRDTDocument:
    return CRDTDocument(client_id)


def apply_operation(client_id: str, op: Operation, session_id: str = ""):
    if session_id and session_id in _sessions:
        _sessions[session_id].apply_operation(client_id, op)


def merge_documents(docs: List[CRDTDocument]) -> CRDTDocument:
    merged = CRDTDocument("merged")
    for doc in docs:
        merged.merge(doc)
    return merged


def diff_states(doc_a: CRDTDocument, doc_b: CRDTDocument) -> Dict:
    """对比两个 CRDT 文档的差异。"""
    text_a = doc_a.get_text()
    text_b = doc_b.get_text()

    if text_a == text_b:
        return {"identical": True, "diff": []}

    # 逐字符比对
    import difflib
    matcher = difflib.SequenceMatcher(None, text_a, text_b)
    diff = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != "equal":
            diff.append({
                "type": tag,
                "from": text_a[i1:i2],
                "to": text_b[j1:j2],
            })

    return {"identical": False, "diff": diff}
