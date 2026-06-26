# Storage Manager - 神经元和突触的存储管理
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Set
from ..core.models import Neuron, Synapse, ActivationRecord

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


class StorageManager:
    """存储管理器 - 管理神经元和突触的持久化 / Storage manager for neurons and synapses"""

    def __init__(self, base_path: str = None):
        if base_path is None:
            base_path = get_default_base_path()
        self.base_path = base_path
        self.neurons_file = os.path.join(base_path, "memory_long_term", "neurons.json")
        self.synapses_dir = os.path.join(base_path, "memory_long_term", "synapses")
        self.activation_logs_dir = os.path.join(base_path, "memory_long_term", "activation_logs")
        self.protected_neuron_types = {
            'preference', 'personality', 'identity',
            'user_profile', 'user_preference'
        }
        self._neurons_cache: Dict[str, Neuron] = {}
        self._synapses_cache: Dict[str, List[Synapse]] = {}  # from_neuron_id -> [synapses]
        self._synapses_by_to: Dict[str, List[Synapse]] = {}  # to_neuron_id -> [synapses]

        self._ensure_directories()
        self._load_neurons()
        self._load_synapses()

    def _ensure_directories(self):
        """确保必要的目录存在"""
        os.makedirs(self.synapses_dir, exist_ok=True)
        os.makedirs(self.activation_logs_dir, exist_ok=True)

    def _load_neurons(self):
        """从文件加载所有神经元"""
        if os.path.exists(self.neurons_file):
            try:
                with open(self.neurons_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for neuron_data in data.get('neurons', []):
                        neuron = Neuron.from_dict(neuron_data)
                        self._neurons_cache[neuron.id] = neuron
            except Exception as e:
                print(f"加载神经元文件失败: {e}")
                self._neurons_cache = {}

    def _load_synapses(self):
        """从文件加载所有突触"""
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
                            # 按起始神经元索引
                            if synapse.fromNeuron not in self._synapses_cache:
                                self._synapses_cache[synapse.fromNeuron] = []
                            self._synapses_cache[synapse.fromNeuron].append(synapse)
                            # 按目标神经元索引
                            if synapse.toNeuron not in self._synapses_by_to:
                                self._synapses_by_to[synapse.toNeuron] = []
                            self._synapses_by_to[synapse.toNeuron].append(synapse)
                except Exception as e:
                    print(f"加载突触文件 {filename} 失败: {e}")

    def save_all(self):
        """保存所有神经元和突触到文件"""
        self._save_neurons()
        self._save_all_synapses()

    def _save_neurons(self):
        """保存神经元到文件"""
        neurons_data = {
            'neurons': [n.to_dict() for n in self._neurons_cache.values()],
            'lastUpdated': datetime.now().isoformat()
        }
        with open(self.neurons_file, 'w', encoding='utf-8') as f:
            json.dump(neurons_data, f, ensure_ascii=False, indent=2)

    def _save_all_synapses(self):
        """将所有突触分片保存到文件"""
        for from_neuron_id, synapses in self._synapses_cache.items():
            filepath = os.path.join(self.synapses_dir, f"{from_neuron_id}.json")
            data = {
                'fromNeuron': from_neuron_id,
                'synapses': [s.to_dict() for s in synapses],
                'lastUpdated': datetime.now().isoformat()
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    # 神经元管理
    def add_neuron(self, neuron: Neuron) -> bool:
        """添加神经元"""
        if neuron.type in self.protected_neuron_types:
            # 保护类型需要特殊检查
            existing = self.get_neuron_by_name_and_type(neuron.name, neuron.type)
            if existing:
                return False  # 已存在，不允许重复创建

        self._neurons_cache[neuron.id] = neuron
        self._save_neurons()
        return True

    def get_neuron(self, neuron_id: str) -> Optional[Neuron]:
        """获取神经元"""
        return self._neurons_cache.get(neuron_id)

    def get_neuron_by_name(self, name: str) -> List[Neuron]:
        """根据名称查找神经元"""
        return [n for n in self._neurons_cache.values() if n.name == name]

    def get_neuron_by_name_and_type(self, name: str, type: str) -> Optional[Neuron]:
        """根据名称和类型查找神经元"""
        for n in self._neurons_cache.values():
            if n.name == name and n.type == type:
                return n
        return None

    def find_neurons_by_tags(self, tags: List[str]) -> List[Neuron]:
        """根据标签查找神经元"""
        results = []
        for neuron in self._neurons_cache.values():
            if any(tag in neuron.tags for tag in tags):
                results.append(neuron)
        return results

    def update_neuron(self, neuron_id: str, **kwargs) -> bool:
        """更新神经元"""
        neuron = self._neurons_cache.get(neuron_id)
        if not neuron:
            return False

        # 保护类型仅允许特定字段更新
        if neuron.type in self.protected_neuron_types:
            allowed_fields = {'content', 'metadata'}
            for key, value in kwargs.items():
                if key not in allowed_fields:
                    print(f"警告: 受保护的神经元类型 '{neuron.type}' 不允许修改字段 '{key}'")
                    return False

        for key, value in kwargs.items():
            if hasattr(neuron, key):
                setattr(neuron, key, value)

        self._save_neurons()
        return True

    def delete_neuron(self, neuron_id: str) -> bool:
        """删除神经元（受保护的不能删）"""
        neuron = self._neurons_cache.get(neuron_id)
        if neuron and neuron.type in self.protected_neuron_types:
            print(f"错误: 受保护的神经元类型 '{neuron.type}' 不允许删除")
            return False

        if neuron_id in self._neurons_cache:
            del self._neurons_cache[neuron_id]
            # 同时删除相关突触
            self._delete_synapses_by_from(neuron_id)
            self._delete_synapses_by_to(neuron_id)
            self._save_neurons()
            self._save_all_synapses()
            return True
        return False

    # 突触管理
    def add_synapse(self, synapse: Synapse) -> bool:
        """添加突触"""
        # 检查关联的神经元是否受保护
        from_neuron = self._neurons_cache.get(synapse.fromNeuron)
        to_neuron = self._neurons_cache.get(synapse.toNeuron)

        if from_neuron and from_neuron.type in self.protected_neuron_types:
            print(f"警告: 突触起始神经元是受保护类型，可能需要限制创建")
        if to_neuron and to_neuron.type in self.protected_neuron_types:
            print(f"警告: 突触目标神经元是受保护类型，可能需要限制创建")

        if synapse.fromNeuron not in self._synapses_cache:
            self._synapses_cache[synapse.fromNeuron] = []
        self._synapses_cache[synapse.fromNeuron].append(synapse)

        if synapse.toNeuron not in self._synapses_by_to:
            self._synapses_by_to[synapse.toNeuron] = []
        self._synapses_by_to[synapse.toNeuron].append(synapse)

        self._save_synapses_for_neuron(synapse.fromNeuron)
        return True

    def get_synapses_from(self, neuron_id: str) -> List[Synapse]:
        """获取从指定神经元出发的所有突触"""
        return self._synapses_cache.get(neuron_id, [])

    def get_synapses_to(self, neuron_id: str) -> List[Synapse]:
        """获取指向指定神经元的所有突触"""
        return self._synapses_by_to.get(neuron_id, [])

    def _delete_synapses_by_from(self, neuron_id: str):
        """删除从指定神经元出发的所有突触"""
        if neuron_id in self._synapses_cache:
            del self._synapses_cache[neuron_id]
            filepath = os.path.join(self.synapses_dir, f"{neuron_id}.json")
            if os.path.exists(filepath):
                os.remove(filepath)

    def _delete_synapses_by_to(self, neuron_id: str):
        """删除指向指定神经元的所有突触"""
        # 需要遍历所有起始神经元
        for from_id, synapses in list(self._synapses_cache.items()):
            self._synapses_cache[from_id] = [s for s in synapses if s.toNeuron != neuron_id]
            self._save_synapses_for_neuron(from_id)

        if neuron_id in self._synapses_by_to:
            del self._synapses_by_to[neuron_id]

    def _save_synapses_for_neuron(self, from_neuron_id: str):
        """保存指定起始神经元的突触"""
        synapses = self._synapses_cache.get(from_neuron_id, [])
        filepath = os.path.join(self.synapses_dir, f"{from_neuron_id}.json")
        data = {
            'fromNeuron': from_neuron_id,
            'synapses': [s.to_dict() for s in synapses],
            'lastUpdated': datetime.now().isoformat()
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def reinforce_synapse(self, synapse_id: str) -> bool:
        """强化突触"""
        # 查找并强化
        for synapses in self._synapses_cache.values():
            for synapse in synapses:
                if synapse.id == synapse_id:
                    synapse.reinforce()
                    self._save_synapses_for_neuron(synapse.fromNeuron)
                    return True
        return False

    def delete_synapse(self, synapse_id: str) -> bool:
        """删除突触"""
        for from_id, synapses in list(self._synapses_cache.items()):
            for i, synapse in enumerate(synapses):
                if synapse.id == synapse_id:
                    # 检查是否受保护
                    from_neuron = self._neurons_cache.get(from_id)
                    to_neuron = self._neurons_cache.get(synapse.toNeuron)
                    if from_neuron and from_neuron.type in self.protected_neuron_types:
                        print(f"错误: 受保护神经元的突触不允许删除")
                        return False
                    if to_neuron and to_neuron.type in self.protected_neuron_types:
                        print(f"错误: 指向受保护神经元的突触不允许删除")
                        return False

                    del synapses[i]
                    self._save_synapses_for_neuron(from_id)
                    return True
        return False

    def get_all_neurons(self) -> List[Neuron]:
        """获取所有神经元"""
        return list(self._neurons_cache.values())

    def get_protected_neurons(self) -> List[Neuron]:
        """获取所有受保护的神经元"""
        return [n for n in self._neurons_cache.values()
                if n.type in self.protected_neuron_types]

    # 激活日志
    def log_activation(self, record: ActivationRecord):
        """记录激活日志"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self.activation_logs_dir, f"{date_str}.json")

        logs = []
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f).get('records', [])
            except:
                logs = []

        logs.append(record.to_dict())

        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump({'records': logs, 'date': date_str}, f, ensure_ascii=False, indent=2)

    def get_recent_activations(self, days: int = 7) -> List[ActivationRecord]:
        """获取最近的激活记录"""
        records = []
        import glob

        for log_file in glob.glob(os.path.join(self.activation_logs_dir, "*.json")):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for record_data in data.get('records', []):
                        records.append(ActivationRecord.from_dict(record_data))
            except:
                continue

        # 按时间排序，最近的在前面
        records.sort(key=lambda r: r.timestamp, reverse=True)
        return records[:days * 10]  # 每天最多10条记录
