# Lazy Storage Manager
# 按需加载存储管理器 - 实现分层存储，只加载相关记忆

import os
import json
from typing import List, Dict, Optional, Set
from datetime import datetime
from collections import OrderedDict

# 导入模型（使用相对路径）
from ..core.models import Neuron, Synapse


class LRUCache:
    """LRU 缓存实现"""
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self._cache: OrderedDict = OrderedDict()
    
    def get(self, key: str):
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        return None
    
    def put(self, key: str, value):
        if key in self._cache:
            self._cache.move_to_end(key)
        else:
            if len(self._cache) >= self.max_size:
                self._cache.popitem(last=False)
            self._cache[key] = value
    
    def contains(self, key: str) -> bool:
        return key in self._cache
    
    def clear(self):
        self._cache.clear()
    
    def size(self) -> int:
        return len(self._cache)


class NeuronIndex:
    """神经元索引 - 只存储元数据，不存储完整内容"""
    def __init__(self):
        self._index: Dict[str, Dict] = {}
        self._name_index: Dict[str, List[str]] = {}
        self._tag_index: Dict[str, List[str]] = {}
        self._type_index: Dict[str, List[str]] = {}
    
    def add(self, neuron: Neuron):
        meta = {
            'id': neuron.id,
            'name': neuron.name,
            'type': neuron.type,
            'tags': neuron.tags,
            'activationCount': neuron.activationCount,
            'lastActivated': neuron.lastActivated
        }
        self._index[neuron.id] = meta
        
        name_lower = neuron.name.lower()
        if name_lower not in self._name_index:
            self._name_index[name_lower] = []
        self._name_index[name_lower].append(neuron.id)
        
        for tag in neuron.tags:
            tag_lower = tag.lower()
            if tag_lower not in self._tag_index:
                self._tag_index[tag_lower] = []
            self._tag_index[tag_lower].append(neuron.id)
        
        if neuron.type not in self._type_index:
            self._type_index[neuron.type] = []
        self._type_index[neuron.type].append(neuron.id)
    
    def remove(self, neuron_id: str):
        if neuron_id not in self._index:
            return
        meta = self._index[neuron_id]
        name_lower = meta['name'].lower()
        if name_lower in self._name_index:
            if neuron_id in self._name_index[name_lower]:
                self._name_index[name_lower].remove(neuron_id)
            if not self._name_index[name_lower]:
                del self._name_index[name_lower]
        for tag in meta.get('tags', []):
            tag_lower = tag.lower()
            if tag_lower in self._tag_index:
                if neuron_id in self._tag_index[tag_lower]:
                    self._tag_index[tag_lower].remove(neuron_id)
                if not self._tag_index[tag_lower]:
                    del self._tag_index[tag_lower]
        if meta['type'] in self._type_index:
            if neuron_id in self._type_index[meta['type']]:
                self._type_index[meta['type']].remove(neuron_id)
            if not self._type_index[meta['type']]:
                del self._type_index[meta['type']]
        del self._index[neuron_id]
    
    def search_by_name(self, name: str) -> List[str]:
        return self._name_index.get(name.lower(), [])
    
    def search_by_tag(self, tag: str) -> List[str]:
        return self._tag_index.get(tag.lower(), [])
    
    def search_by_type(self, type: str) -> List[str]:
        return self._type_index.get(type, [])
    
    def get_all_ids(self) -> List[str]:
        return list(self._index.keys())
    
    def get_meta(self, neuron_id: str) -> Optional[Dict]:
        return self._index.get(neuron_id)
    
    def size(self) -> int:
        return len(self._index)


def get_default_base_path():
    """Get default base path for neural memory storage.
    获取神经记忆存储的默认路径。
    """
    import os
    from pathlib import Path
    
    # Check environment variable first
    if "NEURAL_MEMORY_PATH" in os.environ:
        return os.environ["NEURAL_MEMORY_PATH"]
    
    # Check OpenClaw state directory
    if "OPENCLAW_STATE_DIR" in os.environ:
        return os.path.join(os.environ["OPENCLAW_STATE_DIR"], "neural-memory")
    
    # Default to user home
    return os.path.join(Path.home(), ".openclaw", "neural-memory")


class LazyStorageManager:
    """按需加载存储管理器 - On-demand loading storage manager"""
    
    def __init__(self, base_path: str = None, config: Dict = None):
        if base_path is None:
            base_path = get_default_base_path()
        self.base_path = base_path
        self.config = config or {}
        self.neurons_file = os.path.join(base_path, "memory_long_term", "neurons.json")
        self.synapses_dir = os.path.join(base_path, "memory_long_term", "synapses")
        self.activation_logs_dir = os.path.join(base_path, "memory_long_term", "activation_logs")
        self.protected_neuron_types = {'preference', 'personality', 'identity', 'user_profile', 'user_preference'}
        
        cache_size = self.config.get('hot_cache_size', 100)
        self._hot_cache = LRUCache(max_size=cache_size)
        self._neuron_index = NeuronIndex()
        self._synapses_cache: Dict[str, List[Synapse]] = {}
        self._synapses_by_to: Dict[str, List[Synapse]] = {}
        self._neuron_file_map: Dict[str, str] = {}
        
        self._load_index()
        self._load_synapses()
        self._warm_up_cache()
        
        print(f"[LazyStorage] 初始化完成 - 索引: {self._neuron_index.size()}, 缓存: {cache_size}")
    
    def _load_index(self):
        if not os.path.exists(self.neurons_file):
            return
        try:
            with open(self.neurons_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for neuron_data in data.get('neurons', []):
                    neuron = Neuron.from_dict(neuron_data)
                    self._neuron_index.add(neuron)
                    self._neuron_file_map[neuron.id] = self.neurons_file
        except Exception as e:
            print(f"[LazyStorage] 加载索引失败: {e}")
    
    def _warm_up_cache(self):
        protected_ids = []
        for ntype in self.protected_neuron_types:
            protected_ids.extend(self._neuron_index.search_by_type(ntype))
        for nid in protected_ids[:20]:
            neuron = self._load_neuron_from_file(nid)
            if neuron:
                self._hot_cache.put(nid, neuron)
    
    def _load_synapses(self):
        self._synapses_cache.clear()
        self._synapses_by_to.clear()
        if not os.path.exists(self.synapses_dir):
            return
        for filename in os.listdir(self.synapses_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.synapses_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        synapses = [Synapse.from_dict(s) for s in data.get('synapses', [])]
                        for synapse in synapses:
                            if synapse.fromNeuron not in self._synapses_cache:
                                self._synapses_cache[synapse.fromNeuron] = []
                            self._synapses_cache[synapse.fromNeuron].append(synapse)
                            if synapse.toNeuron not in self._synapses_by_to:
                                self._synapses_by_to[synapse.toNeuron] = []
                            self._synapses_by_to[synapse.toNeuron].append(synapse)
                except Exception as e:
                    pass
    
    def _load_neuron_from_file(self, neuron_id: str) -> Optional[Neuron]:
        meta = self._neuron_index.get_meta(neuron_id)
        if not meta:
            return None
        file_path = self._neuron_file_map.get(neuron_id)
        if not file_path or not os.path.exists(file_path):
            return None
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for neuron_data in data.get('neurons', []):
                    if neuron_data['id'] == neuron_id:
                        return Neuron.from_dict(neuron_data)
        except Exception as e:
            pass
        return None
    
    def get_neuron(self, neuron_id: str) -> Optional[Neuron]:
        cached = self._hot_cache.get(neuron_id)
        if cached:
            return cached
        if not self._neuron_index.get_meta(neuron_id):
            return None
        neuron = self._load_neuron_from_file(neuron_id)
        if neuron:
            self._hot_cache.put(neuron_id, neuron)
        return neuron
    
    def get_neuron_by_name(self, name: str) -> List[Neuron]:
        ids = self._neuron_index.search_by_name(name)
        return [self.get_neuron(nid) for nid in ids if self.get_neuron(nid)]
    
    def get_neuron_by_name_and_type(self, name: str, type: str) -> Optional[Neuron]:
        ids = self._neuron_index.search_by_name(name)
        for nid in ids:
            meta = self._neuron_index.get_meta(nid)
            if meta and meta['type'] == type:
                return self.get_neuron(nid)
        return None
    
    def find_neurons_by_tags(self, tags: List[str]) -> List[Neuron]:
        result_ids = set()
        for tag in tags:
            result_ids.update(self._neuron_index.search_by_tag(tag))
        return [self.get_neuron(nid) for nid in result_ids if self.get_neuron(nid)]
    
    def get_all_neurons(self) -> List[Neuron]:
        all_ids = self._neuron_index.get_all_ids()
        return [self.get_neuron(nid) for nid in all_ids if self.get_neuron(nid)]
    
    def get_all_neuron_ids(self) -> List[str]:
        return self._neuron_index.get_all_ids()
    
    def get_neuron_names(self) -> List[str]:
        return list(self._neuron_index._name_index.keys())
    
    def get_protected_neurons(self) -> List[Neuron]:
        result = []
        for ntype in self.protected_neuron_types:
            ids = self._neuron_index.search_by_type(ntype)
            for nid in ids:
                neuron = self.get_neuron(nid)
                if neuron:
                    result.append(neuron)
        return result
    
    def get_synapses_from(self, neuron_id: str) -> List[Synapse]:
        return self._synapses_cache.get(neuron_id, [])
    
    def get_synapses_to(self, neuron_id: str) -> List[Synapse]:
        return self._synapses_by_to.get(neuron_id, [])
    
    def add_neuron(self, neuron: Neuron) -> bool:
        if neuron.type in self.protected_neuron_types:
            existing = self.get_neuron_by_name_and_type(neuron.name, neuron.type)
            if existing:
                return False
        self._neuron_index.add(neuron)
        self._neuron_file_map[neuron.id] = self.neurons_file
        self._hot_cache.put(neuron.id, neuron)
        self._save_neurons()
        return True
    
    def update_neuron(self, neuron_id: str, **kwargs) -> bool:
        neuron = self.get_neuron(neuron_id)
        if not neuron:
            return False
        if neuron.type in self.protected_neuron_types:
            allowed = {'content', 'metadata'}
            for key in kwargs:
                if key not in allowed:
                    return False
        for key, value in kwargs.items():
            if hasattr(neuron, key):
                setattr(neuron, key, value)
        self._neuron_index.add(neuron)
        self._hot_cache.put(neuron_id, neuron)
        self._save_neurons()
        return True
    
    def delete_neuron(self, neuron_id: str) -> bool:
        neuron = self.get_neuron(neuron_id)
        if neuron and neuron.type in self.protected_neuron_types:
            return False
        self._neuron_index.remove(neuron_id)
        if self._hot_cache.contains(neuron_id):
            self._hot_cache._cache.pop(neuron_id, None)
        self._delete_synapses_by_from(neuron_id)
        self._delete_synapses_by_to(neuron_id)
        self._save_neurons()
        return True
    
    def add_synapse(self, synapse: Synapse) -> bool:
        if synapse.fromNeuron not in self._synapses_cache:
            self._synapses_cache[synapse.fromNeuron] = []
        self._synapses_cache[synapse.fromNeuron].append(synapse)
        if synapse.toNeuron not in self._synapses_by_to:
            self._synapses_by_to[synapse.toNeuron] = []
        self._synapses_by_to[synapse.toNeuron].append(synapse)
        self._save_synapses_for_neuron(synapse.fromNeuron)
        return True
    
    def _save_neurons(self):
        all_neurons = self.get_all_neurons()
        neurons_data = {
            'neurons': [n.to_dict() for n in all_neurons],
            'lastUpdated': datetime.now().isoformat()
        }
        with open(self.neurons_file, 'w', encoding='utf-8') as f:
            json.dump(neurons_data, f, ensure_ascii=False, indent=2)
    
    def _save_synapses_for_neuron(self, from_neuron_id: str):
        synapses = self._synapses_cache.get(from_neuron_id, [])
        filepath = os.path.join(self.synapses_dir, f"{from_neuron_id}.json")
        data = {
            'fromNeuron': from_neuron_id,
            'synapses': [s.to_dict() for s in synapses],
            'lastUpdated': datetime.now().isoformat()
        }
        os.makedirs(self.synapses_dir, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _delete_synapses_by_from(self, neuron_id: str):
        if neuron_id in self._synapses_cache:
            del self._synapses_cache[neuron_id]
            filepath = os.path.join(self.synapses_dir, f"{neuron_id}.json")
            if os.path.exists(filepath):
                os.remove(filepath)
    
    def _delete_synapses_by_to(self, neuron_id: str):
        for from_id in list(self._synapses_cache.keys()):
            self._synapses_cache[from_id] = [s for s in self._synapses_cache[from_id] if s.toNeuron != neuron_id]
            self._save_synapses_for_neuron(from_id)
        if neuron_id in self._synapses_by_to:
            del self._synapses_by_to[neuron_id]
    
    def save_all(self):
        self._save_neurons()
        for from_id in self._synapses_cache:
            self._save_synapses_for_neuron(from_id)
    
    def get_stats(self) -> Dict:
        return {
            'total_neurons': self._neuron_index.size(),
            'hot_cache_size': self._hot_cache.size(),
            'synapses_count': sum(len(s) for s in self._synapses_cache.values()),
            'protected_types': list(self.protected_neuron_types)
        }
