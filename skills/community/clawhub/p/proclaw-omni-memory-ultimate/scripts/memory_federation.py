#!/usr/bin/env python3
"""
记忆联邦系统
支持多Agent之间的记忆共享和协作

功能:
- 记忆共享协议
- 联邦检索
- 隐私保护
- 记忆同步
"""

import json
import os
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import threading


class SharingLevel(Enum):
    """共享级别"""
    PRIVATE = "private"       # 私有：不共享
    SELECTIVE = "selective"   # 选择性：仅特定Agent
    TEAM = "team"            # 团队：团队成员可见
    PUBLIC = "public"        # 公开：所有Agent可见


class SyncStatus(Enum):
    """同步状态"""
    PENDING = "pending"
    SYNCING = "syncing"
    SYNCED = "synced"
    FAILED = "failed"
    CONFLICT = "conflict"


@dataclass
class AgentProfile:
    """Agent档案"""
    id: str
    name: str
    capabilities: List[str]
    trust_level: float = 0.5
    last_sync: Optional[str] = None
    shared_memories: Set[str] = field(default_factory=set)


@dataclass
class SharedMemory:
    """共享记忆"""
    memory_id: str
    owner_id: str
    sharing_level: SharingLevel
    authorized_agents: Set[str]
    content_hash: str
    shared_time: str
    access_count: int = 0
    sync_status: SyncStatus = SyncStatus.SYNCED


@dataclass
class SyncRecord:
    """同步记录"""
    memory_id: str
    source_agent: str
    target_agent: str
    sync_time: str
    status: SyncStatus
    message: str = ""


class MemoryFederation:
    """
    记忆联邦系统
    
    管理多Agent之间的记忆共享
    """
    
    def __init__(self, agent_id: str, memory_path: str = "./memory"):
        self.agent_id = agent_id
        self.memory_path = memory_path
        self.federation_path = os.path.join(memory_path, "federation")
        os.makedirs(self.federation_path, exist_ok=True)
        
        # Agent档案
        self.agents: Dict[str, AgentProfile] = {}
        
        # 共享记忆索引
        self.shared_memories: Dict[str, SharedMemory] = {}
        
        # 同步记录
        self.sync_records: List[SyncRecord] = []
        
        # 访问控制
        self.access_control: Dict[str, Set[str]] = {}  # memory_id -> authorized_agent_ids
        
        # 隐私过滤器
        self.privacy_patterns = [
            "password", "secret", "token", "key", "credential",
            "private", "confidential", "sensitive"
        ]
        
        # 锁
        self._lock = threading.Lock()
        
        # 统计
        self.stats = {
            'total_shared': 0,
            'total_synced': 0,
            'total_accessed': 0,
            'active_agents': 0
        }
        
        self._load_state()
        
        # 注册自己
        self._register_self()
    
    def _register_self(self) -> None:
        """注册当前Agent"""
        if self.agent_id not in self.agents:
            self.agents[self.agent_id] = AgentProfile(
                id=self.agent_id,
                name=f"Agent_{self.agent_id[:8]}",
                capabilities=["memory", "reasoning", "communication"],
                trust_level=1.0
            )
    
    def register_agent(self, agent_id: str, name: str = None,
                       capabilities: List[str] = None,
                       trust_level: float = 0.5) -> AgentProfile:
        """注册Agent"""
        profile = AgentProfile(
            id=agent_id,
            name=name or f"Agent_{agent_id[:8]}",
            capabilities=capabilities or [],
            trust_level=trust_level
        )
        
        self.agents[agent_id] = profile
        self.stats['active_agents'] = len(self.agents)
        self._save_state()
        
        return profile
    
    def share_memory(self, memory_id: str, memory_data: Dict,
                     sharing_level: SharingLevel = SharingLevel.SELECTIVE,
                     authorized_agents: List[str] = None) -> Optional[SharedMemory]:
        """共享记忆"""
        with self._lock:
            # 隐私检查
            if self._contains_private_data(memory_data):
                sharing_level = SharingLevel.PRIVATE
                print(f"警告: 记忆 {memory_id} 包含敏感数据，自动设为私有")
            
            # 计算内容哈希
            content_hash = self._hash_content(memory_data)
            
            # 确定授权Agent
            authorized = set()
            if sharing_level == SharingLevel.SELECTIVE:
                authorized = set(authorized_agents or [])
            elif sharing_level == SharingLevel.TEAM:
                # 团队成员（信任度 >= 0.7）
                authorized = {aid for aid, a in self.agents.items() 
                             if a.trust_level >= 0.7}
            elif sharing_level == SharingLevel.PUBLIC:
                authorized = set(self.agents.keys())
            
            shared = SharedMemory(
                memory_id=memory_id,
                owner_id=self.agent_id,
                sharing_level=sharing_level,
                authorized_agents=authorized,
                content_hash=content_hash,
                shared_time=datetime.now().isoformat()
            )
            
            self.shared_memories[memory_id] = shared
            self.access_control[memory_id] = authorized
            
            self.stats['total_shared'] += 1
            self._save_state()
            
            return shared
    
    def request_memory(self, memory_id: str, 
                       requesting_agent: str) -> Tuple[bool, Optional[Dict], str]:
        """请求共享记忆"""
        with self._lock:
            if memory_id not in self.shared_memories:
                return False, None, "记忆不存在"
            
            shared = self.shared_memories[memory_id]
            
            # 检查访问权限
            if requesting_agent not in shared.authorized_agents:
                return False, None, "无访问权限"
            
            # 检查信任度
            if requesting_agent in self.agents:
                trust = self.agents[requesting_agent].trust_level
                if trust < 0.3:
                    return False, None, "信任度不足"
            
            # 加载记忆数据
            memory_data = self._load_memory(memory_id)
            if memory_data is None:
                return False, None, "记忆数据加载失败"
            
            # 更新访问计数
            shared.access_count += 1
            self.stats['total_accessed'] += 1
            
            # 记录同步
            self._record_sync(memory_id, shared.owner_id, requesting_agent)
            
            return True, memory_data, "成功"
    
    def sync_with_agent(self, target_agent: str,
                        memory_ids: List[str] = None) -> Dict[str, SyncStatus]:
        """与目标Agent同步记忆"""
        results = {}
        
        if target_agent not in self.agents:
            return {mid: SyncStatus.FAILED for mid in (memory_ids or [])}
        
        # 确定要同步的记忆
        if memory_ids is None:
            memory_ids = [
                mid for mid, sm in self.shared_memories.items()
                if target_agent in sm.authorized_agents and 
                   sm.sharing_level != SharingLevel.PRIVATE
            ]
        
        for memory_id in memory_ids:
            status = self._sync_single_memory(memory_id, target_agent)
            results[memory_id] = status
        
        self.stats['total_synced'] += sum(
            1 for s in results.values() if s == SyncStatus.SYNCED
        )
        self._save_state()
        
        return results
    
    def _sync_single_memory(self, memory_id: str, target_agent: str) -> SyncStatus:
        """同步单个记忆"""
        if memory_id not in self.shared_memories:
            return SyncStatus.FAILED
        
        shared = self.shared_memories[memory_id]
        
        if target_agent not in shared.authorized_agents:
            return SyncStatus.FAILED
        
        # 检查目标Agent是否有更新版本
        # （在实际实现中，需要与目标Agent通信）
        
        # 模拟同步
        shared.sync_status = SyncStatus.SYNCED
        
        self._record_sync(memory_id, self.agent_id, target_agent)
        
        return SyncStatus.SYNCED
    
    def _record_sync(self, memory_id: str, source: str, target: str) -> None:
        """记录同步"""
        record = SyncRecord(
            memory_id=memory_id,
            source_agent=source,
            target_agent=target,
            sync_time=datetime.now().isoformat(),
            status=SyncStatus.SYNCED
        )
        self.sync_records.append(record)
    
    def federated_search(self, query: str, 
                        include_remote: bool = True) -> List[Tuple[str, float, str]]:
        """
        联邦检索
        
        在本地和授权的远程记忆中搜索
        """
        results = []
        
        # 本地搜索
        local_results = self._local_search(query)
        for memory_id, score in local_results:
            results.append((memory_id, score, self.agent_id))
        
        # 远程搜索
        if include_remote:
            for agent_id, profile in self.agents.items():
                if agent_id == self.agent_id:
                    continue
                
                # 检查信任度
                if profile.trust_level < 0.5:
                    continue
                
                # 模拟远程搜索
                remote_results = self._remote_search(agent_id, query)
                results.extend(remote_results)
        
        # 排序
        results.sort(key=lambda x: -x[1])
        
        return results
    
    def _local_search(self, query: str) -> List[Tuple[str, float]]:
        """本地搜索"""
        # 简化的关键词匹配
        results = []
        
        for memory_id, shared in self.shared_memories.items():
            memory_data = self._load_memory(memory_id)
            if memory_data:
                content = memory_data.get('content', '')
                score = self._simple_match_score(query, content)
                if score > 0:
                    results.append((memory_id, score))
        
        return results
    
    def _remote_search(self, agent_id: str, query: str) -> List[Tuple[str, float, str]]:
        """远程搜索（模拟）"""
        # 在实际实现中，需要通过通信协议查询其他Agent
        # 这里返回空列表作为示例
        return []
    
    def _simple_match_score(self, query: str, content: str) -> float:
        """简单匹配评分"""
        query_terms = set(query.lower().split())
        content_terms = set(content.lower().split())
        
        if not query_terms:
            return 0.0
        
        overlap = len(query_terms & content_terms)
        return overlap / len(query_terms)
    
    def _contains_private_data(self, memory_data: Dict) -> bool:
        """检查是否包含私有数据"""
        content = json.dumps(memory_data).lower()
        
        for pattern in self.privacy_patterns:
            if pattern in content:
                return True
        
        return False
    
    def _hash_content(self, memory_data: Dict) -> str:
        """计算内容哈希"""
        content = json.dumps(memory_data, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _load_memory(self, memory_id: str) -> Optional[Dict]:
        """加载记忆数据"""
        # 在实际实现中，从存储加载
        memory_file = os.path.join(self.memory_path, "reference", f"{memory_id}.json")
        
        if os.path.exists(memory_file):
            try:
                with open(memory_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return None
    
    def update_trust_level(self, agent_id: str, delta: float) -> None:
        """更新信任度"""
        if agent_id in self.agents:
            current = self.agents[agent_id].trust_level
            self.agents[agent_id].trust_level = max(0.0, min(1.0, current + delta))
            self._save_state()
    
    def get_shared_with_me(self) -> List[SharedMemory]:
        """获取共享给我的记忆"""
        return [
            sm for sm in self.shared_memories.values()
            if self.agent_id in sm.authorized_agents and sm.owner_id != self.agent_id
        ]
    
    def get_my_shared(self) -> List[SharedMemory]:
        """获取我共享的记忆"""
        return [
            sm for sm in self.shared_memories.values()
            if sm.owner_id == self.agent_id
        ]
    
    def _load_state(self) -> None:
        """加载状态"""
        state_file = os.path.join(self.federation_path, 'federation_state.json')
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r') as f:
                    data = json.load(f)
                
                self.stats = data.get('stats', self.stats)
                
                # 加载Agent档案
                for aid, ap in data.get('agents', {}).items():
                    self.agents[aid] = AgentProfile(
                        id=ap['id'],
                        name=ap['name'],
                        capabilities=ap.get('capabilities', []),
                        trust_level=ap.get('trust_level', 0.5),
                        last_sync=ap.get('last_sync'),
                        shared_memories=set(ap.get('shared_memories', []))
                    )
            except:
                pass
    
    def _save_state(self) -> None:
        """保存状态"""
        state_file = os.path.join(self.federation_path, 'federation_state.json')
        
        data = {
            'stats': self.stats,
            'agents': {
                aid: {
                    'id': ap.id,
                    'name': ap.name,
                    'capabilities': ap.capabilities,
                    'trust_level': ap.trust_level,
                    'last_sync': ap.last_sync,
                    'shared_memories': list(ap.shared_memories)
                }
                for aid, ap in self.agents.items()
            }
        }
        
        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_report(self) -> Dict:
        """获取报告"""
        return {
            'agent_id': self.agent_id,
            'stats': self.stats,
            'agents_count': len(self.agents),
            'shared_memories_count': len(self.shared_memories),
            'sync_records_count': len(self.sync_records)
        }


def demo_federation():
    """演示联邦系统"""
    print("=" * 60)
    print("记忆联邦系统演示")
    print("=" * 60)
    
    # 创建两个Agent的联邦
    federation1 = MemoryFederation("agent_001")
    federation2 = MemoryFederation("agent_002")
    
    # 注册Agent
    print("\n注册Agent...")
    federation1.register_agent("agent_002", "HelperAgent", ["memory", "search"], 0.8)
    federation2.register_agent("agent_001", "MainAgent", ["memory", "reasoning"], 0.9)
    
    # 共享记忆
    print("\n共享记忆...")
    memory_data = {
        'id': 'mem_001',
        'content': '这是一个关于项目架构的重要决策',
        'type': 'knowledge',
        'importance': 0.8
    }
    
    shared = federation1.share_memory(
        "mem_001", memory_data,
        SharingLevel.SELECTIVE,
        ["agent_002"]
    )
    
    if shared:
        print(f"共享成功: {shared.memory_id}")
        print(f"共享级别: {shared.sharing_level.value}")
        print(f"授权Agent: {shared.authorized_agents}")
    
    # 请求记忆
    print("\n请求共享记忆...")
    success, data, msg = federation1.request_memory("mem_001", "agent_002")
    print(f"请求结果: {msg}")
    
    # 联邦搜索
    print("\n联邦搜索...")
    results = federation1.federated_search("项目架构")
    print(f"找到 {len(results)} 条结果")
    
    # 报告
    print("\n联邦报告:")
    report = federation1.get_report()
    for k, v in report.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    demo_federation()
