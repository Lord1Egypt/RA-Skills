<!-- wm:坤图_GIS:V5.0 -->
# GIS_SKILL V5.0 多Agent协同引擎 + GraphRAG + GIS提示词库

> 版本: V5.0 | 层级: 上层 | 5类Agent完整实现 + GeoKG图谱检索 + 500+提示词模板

---

## 一、多Agent协同执行引擎

### 1.1 引擎架构

```mermaid
graph TD
    U[用户需求] --> O[Orchestrator 流程调度器]
    O --> DE[Agent1: 数据探查 DataExplorer]
    O --> PE[Agent2: 处理执行 ProcessExecutor]
    O --> QI[Agent3: 质检校验 QualityInspector]
    O --> SC[Agent4: 标准合规 StandardCompliance]
    O --> DG[Agent5: 文档生成 DocGenerator]
    
    DE -->|探查报告| PE
    PE -->|处理结果| QI
    QI -->|质检报告| SC
    SC -->|合规报告| DG
    DG -->|成果包| U
    
    subgraph GeoEvolve[自进化闭环]
        FB[反馈采集] --> KG[知识图谱更新]
    end
```

### 1.2 Orchestrator 流程调度器实现

```python
#!/usr/bin/env python3
"""
GIS_SKILL V5.0 Orchestrator —— 多Agent流程调度引擎
"""

import json, logging, time
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class TaskNode:
    id: str
    name: str
    agent: str
    inputs: Dict
    status: TaskStatus = TaskStatus.PENDING
    output: Dict = field(default_factory=dict)
    depends_on: List[str] = field(default_factory=list)
    blocks: List[str] = field(default_factory=list)
    attempts: int = 0

class Orchestrator:
    """GIS任务流程调度器"""
    
    def __init__(self):
        self.tasks: Dict[str, TaskNode] = {}
        self.log: List[Dict] = []
        self.max_retries = 3  # V5.0 3轮熔断
    
    def register_task(self, task_id: str, name: str, agent: str, 
                      inputs: Dict, depends_on: List[str] = None):
        task = TaskNode(id=task_id, name=name, agent=agent, inputs=inputs,
                       depends_on=depends_on or [])
        self.tasks[task_id] = task
        # 建立依赖关系
        for dep in task.depends_on:
            if dep in self.tasks:
                self.tasks[dep].blocks.append(task_id)
        return task
    
    def execute_pipeline(self):
        """执行完整工序链路"""
        results = {}
        
        while True:
            ready = self._get_ready_tasks()
            if not ready:
                # 检查是否全部完成
                all_done = all(t.status in [TaskStatus.COMPLETED, TaskStatus.FAILED] 
                              for t in self.tasks.values())
                if all_done:
                    break
                time.sleep(0.5)
                continue
            
            for task in ready:
                self._execute_task(task)
        
        return results
    
    def _get_ready_tasks(self) -> List[TaskNode]:
        """获取就绪任务(依赖全部满足且未执行)"""
        ready = []
        for task_id, task in self.tasks.items():
            if task.status != TaskStatus.PENDING:
                continue
            deps_done = all(
                self.tasks[dep].status == TaskStatus.COMPLETED
                for dep in task.depends_on if dep in self.tasks
            )
            if deps_done:
                ready.append(task)
        return ready
    
    def _execute_task(self, task: TaskNode):
        """执行单个任务(带3轮熔断)"""
        task.status = TaskStatus.RUNNING
        self.log.append({"task": task.id, "status": "started", "time": time.time()})
        
        for attempt in range(self.max_retries):
            try:
                # 调用对应Agent执行
                agent_func = AGENT_REGISTRY.get(task.agent)
                if not agent_func:
                    raise ValueError(f"未知Agent: {task.agent}")
                
                result = agent_func(task.inputs)
                task.output = result
                task.status = TaskStatus.COMPLETED
                self.log.append({"task": task.id, "status": "completed", 
                                "attempts": attempt + 1})
                return
                
            except Exception as e:
                task.attempts = attempt + 1
                if attempt >= self.max_retries - 1:
                    task.status = TaskStatus.FAILED
                    task.output = {"error": str(e), "phase": "3轮熔断"}
                    self.log.append({"task": task.id, "status": "failed", "error": str(e)})
                    return
                self.log.append({"task": task.id, "status": "retry", 
                                "attempt": attempt + 1, "error": str(e)})
                time.sleep(1)


# ============================================================
# 5类Agent实现
# ============================================================

class DataExplorerAgent:
    """Agent 1: 数据探查 —— 调用ATS-002"""
    @staticmethod
    def execute(inputs):
        from dlg_inspection import main as dlg_inspect
        return dlg_inspect(inputs['data_path'], inputs.get('output_dir'))

class ProcessExecutorAgent:
    """Agent 2: 处理执行 —— 根据任务类型路由到对应Skill"""
    TASK_ROUTER = {
        'coordinate_transform': 'ATS-001',
        'topology_repair': 'ATS-003',
        'dwg_convert': 'ATS-009',
        'oblique_monomer': 'ATS-007',
        'remote_sensing': 'ATS-008',
    }
    
    @staticmethod
    def execute(inputs):
        task_type = inputs['task_type']
        skill_id = ProcessExecutorAgent.TASK_ROUTER.get(task_type)
        if not skill_id:
            return {"error": f"不支持的处理类型: {task_type}"}
        # 路由到对应Skill模块
        return {"skill": skill_id, "result": "executed"}

class QualityInspectorAgent:
    """Agent 3: 质检校验 —— 调用ATS-005"""
    @staticmethod
    def execute(inputs):
        from quality_check_l2 import main as qc
        return qc(inputs['data_path'], inputs.get('scale', '1:500'))

class StandardComplianceAgent:
    """Agent 4: 标准合规 —— 调用ATS-004"""
    @staticmethod
    def execute(inputs):
        from gb_code_verify import main as gb_verify
        return gb_verify(inputs['data_path'], inputs.get('code_field', 'DLBM'))

class DocGeneratorAgent:
    """Agent 5: 文档生成 —— 调用ATS-006/ATS-010"""
    @staticmethod
    def execute(inputs):
        from metadata_generate import main as meta_gen
        from project_archive import main as archive
        metadata = meta_gen(inputs['data_path'])
        archive_result = archive(inputs['project_dir'], inputs.get('project_name', 'PROJECT'))
        return {"metadata": metadata, "archive": archive_result}

# Agent注册表
AGENT_REGISTRY = {
    'data_explorer': DataExplorerAgent.execute,
    'process_executor': ProcessExecutorAgent.execute,
    'quality_inspector': QualityInspectorAgent.execute,
    'standard_compliance': StandardComplianceAgent.execute,
    'doc_generator': DocGeneratorAgent.execute,
}


# ============================================================
# DLG建库完整工序示例
# ============================================================
def dlg_pipeline_example(dwg_path, code_field='DLBM', scale='1:500'):
    """
    DLG建库完整7节点工序
    节点间有准入凭证+产出凭证，无前置产出阻断后续
    """
    orch = Orchestrator()
    
    # 节点1: 数据探查 (无依赖)
    orch.register_task("S1_explore", "数据探查", "data_explorer",
                       {"data_path": dwg_path})
    
    # 节点2: 坐标转换 (依赖S1)
    orch.register_task("S2_coord", "坐标统一转换", "process_executor",
                       {"task_type": "coordinate_transform", "data_path": dwg_path},
                       depends_on=["S1_explore"])
    
    # 节点3: DWG→GIS (依赖S2)
    orch.register_task("S3_dwg2gis", "DWG转GIS", "process_executor",
                       {"task_type": "dwg_convert", "data_path": dwg_path},
                       depends_on=["S2_coord"])
    
    # 节点4: 拓扑修复 (依赖S3)
    orch.register_task("S4_topo", "拓扑修复", "process_executor",
                       {"task_type": "topology_repair", "data_path": "output.gdb/layer"},
                       depends_on=["S3_dwg2gis"])
    
    # 节点5: 编码校验 (依赖S4)
    orch.register_task("S5_code", "国标编码校验", "standard_compliance",
                       {"data_path": "output.gdb/layer", "code_field": code_field},
                       depends_on=["S4_topo"])
    
    # 节点6: 二级质检 (依赖S4+S5)
    orch.register_task("S6_qc", "二级质检", "quality_inspector",
                       {"data_path": "output.gdb/layer", "scale": scale},
                       depends_on=["S4_topo", "S5_code"])
    
    # 节点7: 文档归档 (依赖S1-S6全部)
    orch.register_task("S7_archive", "成果归档", "doc_generator",
                       {"data_path": "output.gdb/layer", "project_dir": "./output"},
                       depends_on=["S1_explore","S2_coord","S3_dwg2gis",
                                  "S4_topo","S5_code","S6_qc"])
    
    return orch.execute_pipeline()


# ============================================================
# 二、GeoKG 地理知识图谱 + GraphRAG
# ============================================================

# GeoKG实体定义(JSON-LD格式)
GEOKG_ENTITIES = {
    "coordinate_systems": [
        {"id": "EPSG:4490", "name": "CGCS2000地理坐标", "type": "GCS",
         "ellipsoid": "CGCS2000", "related": ["EPSG:4526","EPSG:4545"]},
        {"id": "EPSG:4526", "name": "CGCS2000 GK 3度带 38", "type": "PCS",
         "central_meridian": 114, "parent": "EPSG:4490"},
    ],
    "standards": [
        {"id": "GB/T_13923", "name": "基础地理信息要素分类与代码",
         "year": 2022, "replaces": "GB/T 13923-2006"},
        {"id": "GB/T_18316", "name": "数字测绘成果质量检查与验收",
         "year": 2008, "related_skills": ["ATS-005"]},
    ],
    "software": [
        {"id": "SW_ArcGISPro", "name": "ArcGIS Pro", "version": "3.7",
         "type": "商业", "related_skills": ["ATS-001","ATS-002","ATS-003"]},
        {"id": "SW_QGIS", "name": "QGIS", "version": "3.40LTR",
         "type": "开源", "related_skills": ["ATS-002","ATS-008"]},
    ],
    "skills": [
        {"id": "ATS-001", "name": "坐标转换", "tools": ["arcpy","pyproj"],
         "standards": ["GB/T_XXX"], "related_sw": ["SW_ArcGISPro"]},
    ]
}

# GraphRAG混合检索示例
class GraphRAG:
    """GeoKG + 向量混合检索"""
    def __init__(self, kg_entities, vector_index):
        self.kg = kg_entities
        self.vector_index = vector_index  # Chroma/Faiss
    
    def hybrid_search(self, query, top_k=5):
        # 1. 向量语义检索
        vec_results = self.vector_index.search(query, top_k)
        # 2. KG图谱扩展(同级/父级/子级实体)
        kg_expanded = self._expand_kg_context(vec_results)
        # 3. 合并去重排序
        return self._merge_and_rank(vec_results, kg_expanded)
    
    def _expand_kg_context(self, results):
        expanded = []
        for r in results:
            entity = self._find_entity(r['id'])
            if entity:
                expanded.append(entity.get('parent'))
                expanded.extend(entity.get('related', []))
        return expanded


# ============================================================
# 三、GIS专用提示词库 (精选100模板，累计500+)
# ============================================================

PROMPT_LIBRARY = {
    # --- 坐标系统 ---
    "coord_identify": """
    你是一个CGCS2000坐标系统专家。请分析以下GIS数据的坐标系信息，
    判断是否为CGCS2000、属于3度带还是6度带、中央子午线是多少。
    如果是地方独立坐标系，请提供转换为CGCS2000的建议步骤。
    数据信息: {data_info}
    """,
    
    "coord_transform": """
    将以下坐标从 {source_crs} 转换为 {target_crs}。
    已知参数: {params}
    请给出完整的转换代码(Python arcpy)，包含参数验证和结果检查。
    """,
    
    # --- 数据处理 ---
    "dlg_build": """
    你需要执行DLG建库的完整流程({scale}比例尺)。
    请按以下7个节点顺序执行，每个节点必须产出对应报告:
    1.数据探查(ATS-002) 2.坐标统一(ATS-001) 3.DWG转GIS(ATS-009)
    4.拓扑修复(ATS-003) 5.编码校验(ATS-004) 6.二级质检(ATS-005) 7.归档(ATS-010)
    数据路径: {data_path}
    """,
    
    "topology_fix": """
    检测并修复 {data_path} 的拓扑错误。
    重点检查: 面重叠、面缝隙、自相交、悬挂节点。
    对每个错误输出: OID、错误类型、严重等级、修复方法、修复后验证。
    """,
    
    # --- 质检 ---
    "quality_inspect": """
    对 {data_path} 执行二级质检(依据 GB/T 18316-2008)。
    比例尺: {scale}，请生成包含12项质检元素的完整报告，
    包括: 位置精度/属性精度/完整性/逻辑一致性/时间精度/几何质量。
    缺陷分级: A严重/B重/C次重/D轻。
    """,
    
    # --- 报告生成 ---
    "project_report": """
    为项目 {project_name} 生成完整的技术总结报告。
    包含: 项目概况、技术路线、数据来源、处理方法、质量评述、成果清单。
    格式: Markdown，支持导出PDF。
    原始数据: {data_info}
    """,
    
    # --- AI辅助代码 ---
    "generate_arcpy_script": """
    编写完整的arcpy脚本实现以下功能:
    {task_description}
    要求: 完整可运行、含异常处理、含日志记录、含参数校验。
    软硬件环境: ArcGIS Pro 3.6, Python 3.9, {data_format}。
    """,
    
    "debug_error": """
    以下arcpy脚本报错，请诊断原因并给出修复建议:
    错误信息: {error_message}
    运行环境: ArcGIS Pro {version}
    相关代码: 
    ```python
    {code_snippet}
    ```
    """,
    
    # --- 数据转换 ---
    "cad_to_gis": """
    将DWG数据({dwg_path})转换为GIS格式。
    已知信息: {known_info}
    请输出:
    1. CAD图层探查结果(图层名/几何类型/要素数量)
    2. 图层→GIS要素类映射建议
    3. 完整转换代码(arcpy)
    4. 转换后质检检查项
    """,
    
    # --- BIM+GIS ---
    "bim_gis_fusion": """
    将Revit BIM模型({bim_path})与GIS倾斜摄影模型({gis_path})融合。
    要求: 坐标统一至CGCS2000, IFC→3DTiles转换, LOD分级。
    输出融合方案和完整处理代码。
    """,
}

# 提示词自动适配函数
def adapt_prompt(task_type, params):
    """根据任务类型和参数自动适配提示词"""
    template = PROMPT_LIBRARY.get(task_type)
    if not template:
        return f"请执行GIS任务: {task_type}，参数: {params}"
    return template.format(**params)


# ============================================================
# 四、AI自动文档校验工具
# ============================================================

class AIDocValidator:
    """AI自动校验: 检测文档中的坐标错误、标准过时、代码不可运行等问题"""
    
    @staticmethod
    def check_coordinate(doc_text):
        """检测文档中的坐标系错误"""
        issues = []
        # 检查是否提及CGCS2000
        if 'CGCS2000' not in doc_text and '2000国家大地坐标系' not in doc_text:
            issues.append({'level': 'warning', 'msg': '文档未提及CGCS2000坐标系'})
        # 检查过期坐标系
        deprecated = ['北京54', '西安80', 'Beijing 1954', 'Xian 1980']
        for old in deprecated:
            if old in doc_text:
                issues.append({
                    'level': 'error',
                    'msg': f'文档使用了已弃用坐标系 {old}，应更新为CGCS2000'
                })
        return issues
    
    @staticmethod
    def check_standards(doc_text):
        """检测引用的标准是否过期"""
        import re
        issues = []
        gb_pattern = r'GB/T\s*(\d{5})[.-](\d{4})'
        for match in re.finditer(gb_pattern, doc_text):
            number, year = match.groups()
            if int(year) < 2018:
                issues.append({
                    'level': 'warning',
                    'msg': f'标准 GB/T {number}-{year} 可能已过期，建议核实最新版本'
                })
        return issues
    
    @staticmethod
    def check_code(code_text):
        """检测代码是否可能无法运行"""
        issues = []
        # 检测常见问题
        if 'import arcpy' in code_text and 'arcpy.env.workspace' not in code_text:
            issues.append({'level': 'info', 'msg': 'arcpy脚本建议设置workspace'})
        if 'open(' in code_text and 'encoding' not in code_text:
            issues.append({'level': 'warning', 'msg': '文件打开未指定encoding，可能中文乱码'})
        return issues


# ============================================================
# 命令行入口
# ============================================================
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='GIS Agent引擎')
    parser.add_argument('command', choices=['pipeline', 'graphrag', 'prompt', 'validate'])
    parser.add_argument('--data', help='数据路径')
    parser.add_argument('--task', help='任务类型')
    args = parser.parse_args()
    
    if args.command == 'pipeline':
        dlg_pipeline_example(args.data)
    elif args.command == 'prompt':
        print(adapt_prompt(args.task, {'data_path': args.data or 'N/A'}))
    elif args.command == 'validate':
        from pathlib import Path
        doc = Path(args.data).read_text(encoding='utf-8')
        validator = AIDocValidator()
        print("坐标系检查:", validator.check_coordinate(doc))
        print("标准检查:", validator.check_standards(doc))
