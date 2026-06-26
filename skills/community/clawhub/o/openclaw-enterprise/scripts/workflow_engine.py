#!/usr/bin/env python3
"""OpenClaw Enterprise - Agent工作流执行器 v1.2.4
   安全增强版：路径验证、危险模式检测、安全日志
"""

import json
import asyncio
import re
import logging
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

# 配置安全日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================================
# 路径验证模块 - 增强安全性 v1.2.4
# ============================================================
class PathValidator:
    """路径访问验证器，确保文件操作在允许范围内"""
    
    ALLOWED_READ_DIRS = [
        "./data/openclaw-enterprise/",
        "./skills/openclaw-enterprise/scripts/",
        "./skills/openclaw-enterprise/templates/",
        "./skills/openclaw-enterprise/references/",
    ]
    ALLOWED_WRITE_DIRS = [
        "./data/openclaw-enterprise/output/",
        "./data/openclaw-enterprise/logs/",
    ]
    DENY_PATHS = [
        "/etc/", "/root/", "/home/", "/var/", "/.ssh/",
        "/usr/bin/", "/usr/sbin/", "/bin/", "/sbin/",
    ]
    
    # 新增：禁止的危险模式（安全加固）
    DANGEROUS_PATTERNS = [
        r'\.\.',           # 防止目录遍历
        r'^/',             # 绝对路径
        r'~',              # home目录
        r'\$',             # 环境变量
        r'[;&|`$]',        # Shell特殊字符
    ]
    
    @classmethod
    def validate_path(cls, path: str, require_write: bool = False) -> bool:
        """验证路径是否在允许范围内 - 增强版 v1.2.4"""
        # 1. 检查危险模式
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, path):
                logger.warning(f"Path validation failed: dangerous pattern '{pattern}' detected")
                return False
        
        # 2. 检查禁止访问的路径
        try:
            resolved = Path(path).resolve()
        except Exception:
            logger.warning(f"Path resolve failed: {path[:50]}...")
            return False
            
        for deny in cls.DENY_PATHS:
            if str(resolved).startswith(deny):
                logger.warning(f"Path validation failed: denied path prefix '{deny}'")
                return False
        
        # 3. 检查允许的目录
        allowed = cls.ALLOWED_WRITE_DIRS if require_write else cls.ALLOWED_READ_DIRS + cls.ALLOWED_WRITE_DIRS
        for allowed_dir in allowed:
            try:
                allowed_resolved = Path(allowed_dir).resolve()
                resolved.relative_to(allowed_resolved)
                return True
            except ValueError:
                continue
        
        return False
    
    @classmethod
    def safe_read(cls, path: str) -> Optional[Dict]:
        """安全读取JSON文件 - 增强版 v1.2.4"""
        if not cls.validate_path(path, require_write=False):
            return None
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            logger.error("JSON file read error occurred")
            return None
    
    @classmethod
    def safe_write(cls, path: str, data: Dict) -> bool:
        """安全写入JSON文件 - 增强版 v1.2.4"""
        if not cls.validate_path(path, require_write=True):
            return False
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            logger.error("JSON file write error occurred")
            return False


class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class WorkflowStep:
    step_id: str
    agent_name: str
    instruction: str
    dependencies: List[str] = field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.PENDING
    result: Optional[Dict] = None

@dataclass
class Workflow:
    workflow_id: str
    name: str
    description: str
    steps: List[WorkflowStep]
    status: WorkflowStatus = WorkflowStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)

# 预定义工作流模板
WORKFLOW_TEMPLATES = {
    "采购审批流程": {
        "name": "采购审批流程",
        "description": "从需求分析到成本参考方案的完整流程",
        "steps": [
            {"step_id": "analyze", "agent_name": "原料采购Agent", "instruction": "分析采购需求"},
            {"step_id": "supplier", "agent_name": "仓储管理Agent", "instruction": "生成库存规划建议", "dependencies": ["analyze"]},
            {"step_id": "decision", "agent_name": "成本核算Agent", "instruction": "生成成本核算建议", "dependencies": ["supplier"]}
        ]
    },
    "订单履约流程": {
        "name": "订单履约流程",
        "description": "从订单到发货建议的完整流程",
        "steps": [
            {"step_id": "order", "agent_name": "订单履约Agent", "instruction": "解析订单需求"},
            {"step_id": "production", "agent_name": "生产调度Agent", "instruction": "生成生产计划建议", "dependencies": ["order"]},
            {"step_id": "logistics", "agent_name": "物流调度Agent", "instruction": "生成发货规划建议", "dependencies": ["production"]}
        ]
    },
    "客户服务流程": {
        "name": "客户服务流程",
        "description": "客户问题处理建议流程",
        "steps": [
            {"step_id": "support", "agent_name": "客服支持Agent", "instruction": "分析问题需求"},
            {"step_id": "data", "agent_name": "数据分析Agent", "instruction": "生成分析建议", "dependencies": ["support"]},
            {"step_id": "report", "agent_name": "报告生成Agent", "instruction": "生成报告建议", "dependencies": ["data"]}
        ]
    }
}

async def run_workflow(template_name: str, context: Dict = None) -> Dict:
    """运行工作流"""
    if template_name not in WORKFLOW_TEMPLATES:
        return {"error": f"模板 {template_name} 不存在"}
    
    template = WORKFLOW_TEMPLATES[template_name]
    steps = [WorkflowStep(**s) for s in template["steps"]]
    
    workflow = Workflow(
        workflow_id=f"wf_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        name=template["name"],
        description=template["description"],
        steps=steps
    )
    
    # 模拟执行
    workflow.status = WorkflowStatus.RUNNING
    results = {}
    
    for step in steps:
        # 检查依赖
        deps_ok = all(d in results for d in step.dependencies)
        if not deps_ok:
            step.status = WorkflowStatus.FAILED
            continue
        
        step.status = WorkflowStatus.RUNNING
        step.result = {
            "agent": step.agent_name,
            "instruction": step.instruction,
            "status": "completed"
        }
        step.status = WorkflowStatus.COMPLETED
        results[step.step_id] = step.result
    
    workflow.status = WorkflowStatus.COMPLETED
    
    return {
        "workflow_id": workflow.workflow_id,
        "name": workflow.name,
        "version": "1.2.4",
        "status": "completed",
        "steps": len(steps),
        "results": results
    }

if __name__ == "__main__":
    import sys
    template = sys.argv[1] if len(sys.argv) > 1 else "采购审批流程"
    result = asyncio.run(run_workflow(template))
    print(json.dumps(result, ensure_ascii=False, indent=2))
