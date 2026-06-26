# Core Module Init
# 核心模块初始化

from .models import Neuron, Synapse, ActivationRecord
from .engine import ActivationSpreadingEngine
from .synapse_manager import SynapseManager
from .neuron_builder import NeuronBuilder

# 导入意图理解模块
try:
    from .intent import IntentUnderstandingLayer, SemanticSimilarityEngine, RelatedNeuron
except ImportError:
    pass  # 意图理解模块可能不存在

__all__ = [
    'Neuron',
    'Synapse', 
    'ActivationRecord',
    'ActivationSpreadingEngine',
    'SynapseManager',
    'NeuronBuilder',
]
