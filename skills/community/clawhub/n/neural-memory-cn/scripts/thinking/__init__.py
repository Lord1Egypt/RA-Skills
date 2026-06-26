# Main Thinking Module - 思考模块主入口
import os
import yaml
from typing import List, Dict, Optional
from pathlib import Path


def get_default_base_path():
    """Get default base path for neural memory storage.
    获取神经记忆存储的默认路径。
    """
    # Check environment variable first
    if "NEURAL_MEMORY_PATH" in os.environ:
        return os.environ["NEURAL_MEMORY_PATH"]
    
    # Check OpenClaw state directory
    if "OPENCLAW_STATE_DIR" in os.environ:
        return os.path.join(os.environ["OPENCLAW_STATE_DIR"], "neural-memory")
    
    # Default to user home
    return os.path.join(Path.home(), ".openclaw", "neural-memory")


def load_config():
    """Load configuration file.
    加载配置文件。
    """
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"[ThinkingModule] Failed to load config / 加载配置失败: {e}")
    return {}

_config = load_config()
_use_enhanced = _config.get('thinking', {}).get('enhanced', {}).get('use_intent_layer', True)

if _use_enhanced:
    from .enhanced_init import EnhancedThinkingModule as ThinkingModule
    print("[ThinkingModule] Enhanced mode: intent understanding + semantic similarity + on-demand loading")
    print("[ThinkingModule] 增强模式：意图理解 + 语义相似度 + 按需加载")
else:
    from .storage.manager import StorageManager
    from .core.engine import ActivationSpreadingEngine
    from .core.synapse_manager import SynapseManager
    from .core.neuron_builder import NeuronBuilder
    
    class ThinkingModule:
        def __init__(self, base_path: str = None):
            """Initialize basic thinking module.
            初始化基础思考模块。
            
            Args:
                base_path: Storage path, auto-detected if None
                          存储路径，为空时自动检测
            """
            if base_path is None:
                base_path = get_default_base_path()
            
            print(f"[ThinkingModule] Initializing basic mode / 初始化基础模式...")
            print(f"[ThinkingModule] Storage path / 存储路径: {base_path}")
            
            self.storage = StorageManager(base_path)
            self.engine = ActivationSpreadingEngine(self.storage)
            self.synapse_manager = SynapseManager(self.storage)
            self.neuron_builder = NeuronBuilder(self.storage)
            self.is_initialized = False
            print(f"[OK] Basic mode initialized / 基础模式初始化完成")
        
        def think(self, concept: str, mode: str = 'associative', max_depth: int = 3) -> Dict:
            neurons = self.storage.get_neuron_by_name(concept)
            if not neurons:
                return {'query': concept, 'error': 'concept_not_found'}
            main_neuron = max(neurons, key=lambda n: n.activationCount)
            return self.engine.spread(main_neuron.id, max_depth=max_depth)
        
        def get_thinking_stats(self):
            return {'neurons_count': len(self.storage.get_all_neurons())}
        
        def save(self):
            self.storage.save_all()
    
    print("[ThinkingModule] Basic mode / 基础模式")

# Export functions / 导出函数
def get_config():
    return _config

def get_base_path():
    """Get current base path for neural memory.
    获取神经记忆的当前基础路径。
    """
    return get_default_base_path()

__all__ = ['ThinkingModule', 'get_config', 'get_base_path', 'get_default_base_path']