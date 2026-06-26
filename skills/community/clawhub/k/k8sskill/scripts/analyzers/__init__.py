"""
文件功能：K8sSkill分析器模块包
主要类/函数：
    - PodAnalyzer - Pod分析器
    - DeploymentAnalyzer - Deployment分析器
    - ServiceAnalyzer - Service分析器
    - StatefulSetAnalyzer - StatefulSet分析器
    - JobAnalyzer - Job分析器
    - CronJobAnalyzer - CronJob分析器
    - ReplicaSetAnalyzer - ReplicaSet分析器
    - HPAAnalyzer - HPA分析器
    - PVCAnalyzer - PVC分析器
    - NodeAnalyzer - Node分析器
    - IngressAnalyzer - Ingress分析器
    - EventAnalyzer - Event分析器
    - ConfigMapAnalyzer - ConfigMap分析器
    - SecretAnalyzer - Secret分析器
    - NetworkPolicyAnalyzer - NetworkPolicy分析器
    - PDBAnalyzer - PDB分析器
    - StorageAnalyzer - Storage分析器
    - SecurityAnalyzer - Security分析器
    - GatewayAnalyzer - Gateway分析器
    - HTTPRouteAnalyzer - HTTPRoute分析器
    - WebhookAnalyzer - Webhook分析器
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 每个分析器独立成模块，便于维护和扩展
IMPORTANT: 所有分析器继承自BaseAnalyzer
"""

# 核心分析器
from .pod import PodAnalyzer
from .deployment import DeploymentAnalyzer
from .service import ServiceAnalyzer

# 工作负载分析器
from .statefulset import StatefulSetAnalyzer
from .job import JobAnalyzer
from .cronjob import CronJobAnalyzer
from .replicaset import ReplicaSetAnalyzer
from .hpa import HPAAnalyzer

# 存储和网络分析器
from .pvc import PVCAnalyzer
from .ingress import IngressAnalyzer
from .gateway import GatewayAnalyzer
from .httproute import HTTPRouteAnalyzer
from .networkpolicy import NetworkPolicyAnalyzer

# 集群分析器
from .node import NodeAnalyzer
from .event import EventAnalyzer
from .storage import StorageAnalyzer
from .security import SecurityAnalyzer
from .webhook import WebhookAnalyzer

# 配置分析器
from .configmap import ConfigMapAnalyzer
from .secret import SecretAnalyzer
from .pdb import PDBAnalyzer

__all__ = [
    # 核心
    "PodAnalyzer",
    "DeploymentAnalyzer",
    "ServiceAnalyzer",
    # 工作负载
    "StatefulSetAnalyzer",
    "JobAnalyzer",
    "CronJobAnalyzer",
    "ReplicaSetAnalyzer",
    "HPAAnalyzer",
    # 存储和网络
    "PVCAnalyzer",
    "IngressAnalyzer",
    "GatewayAnalyzer",
    "HTTPRouteAnalyzer",
    "NetworkPolicyAnalyzer",
    # 集群
    "NodeAnalyzer",
    "EventAnalyzer",
    "StorageAnalyzer",
    "SecurityAnalyzer",
    "WebhookAnalyzer",
    # 配置
    "ConfigMapAnalyzer",
    "SecretAnalyzer",
    "PDBAnalyzer",
]
