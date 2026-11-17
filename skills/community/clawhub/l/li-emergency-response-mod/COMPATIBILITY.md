# 企业应急响应指导 Skill - 多智能体适配配置

## 技能描述

```yaml
skill:
  id: corporate-emergency-response-guidance
  name: 企业应急响应指导
  version: 1.0.0
  category: security
  subcategory: incident-response
  
  description: |
    帮助企业在突发网络安全事件中快速建立可控、可审计、可复盘、可持续进化的应急响应作业体系。
    支持Linux/Windows/数据库等多场景，覆盖挖矿、勒索、暴力破解、钓鱼、隧道等常见事件类型。
    
  capabilities:
    - 事件分流与研判
    - 证据固定与取证
    - IOC提取与时间线重建
    - 低影响遏制与清除
    - 善后与横向定损
    - CTF应急题解题
    - 经验沉淀与自进化
    
  requirements:
    - python3.8+
    - 文件系统访问权限
    - 命令行执行权限（可选）
    
  constraints:
    - 仅限授权与合规场景
    - 先取证后处置
    - VBR（Verify Before Reporting）
    - 高风险动作需HITL确认
```

## 各智能体平台适配说明

### 1. OpenCode（已适配）

**配置文件位置**：`.opencode/opencode.json`

**使用方式**：
```python
# 在OpenCode中使用
skill.load("corporate-emergency-response-guidance")
```

**工具调用**：
```python
# 记录证据
opencode.tool.call("note.py", [
  "验证：发现异常高CPU进程",
  "--phase", "triage",
  "--action", "verify",
  "--verdict", "pass",
  "--evidence", "./evidence/top.txt"
])
```

### 2. Hermes Agent（需适配层）

**适配要求**：
- Hermes不支持直接执行本地Python脚本
- 需要将Python脚本封装为Hermes工具插件
- 或提供HTTP API接口

**建议适配方案**：

#### 方案A：工具插件封装
```python
# hermes_tools/ir_note.py
from hermes import Tool

@Tool.register
def ir_note(text: str, phase: str, **kwargs):
    """
    企业应急响应记录工具
    
    Args:
        text: 记录文本
        phase: 阶段（detect/triage/contain/eradicate/recover/postmortem/report）
        **kwargs: 其他参数（evidence/ioc/timeline等）
    """
    # 调用原始note.py逻辑
    import sys
    sys.path.append("/path/to/skill/scripts")
    from note import main
    return main([text, "--phase", phase] + kwargs_to_args(kwargs))
```

#### 方案B：HTTP API封装
```python
# api_server.py（需要额外实现）
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/api/note', methods=['POST'])
def note():
    data = request.json
    cmd = ["python3", "scripts/note.py"] + dict_to_args(data)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return jsonify({"output": result.stdout})

# 其他API端点...
```

**Hermes配置文件**（建议新增）：
```json
{
  "skill": "corporate-emergency-response-guidance",
  "adapter": "hermes",
  "tools": {
    "note": {
      "type": "http_api",
      "endpoint": "http://localhost:5000/api/note",
      "description": "记录应急响应证据"
    }
  }
}
```

### 3. OpenClaw（需适配层）

**适配要求**：
- OpenClaw基于任务编排
- 需要将应急流程拆分为独立任务节点
- 每个playbook对应一个任务模板

**建议适配方案**：

#### 任务模板定义
```yaml
# openclaw_tasks/detect.yaml
task:
  name: 事件检测与分流
  phase: detect
  steps:
    - name: 接收告警
      action: input
      fields:
        - alert_source
        - alert_time
        - affected_assets
    
    - name: 事件类型判断
      action: classify
      categories:
        - 挖矿/木马/远控
        - 勒索
        - 暴力破解
        - 钓鱼
        - 隧道
        - 数据库事件
    
    - name: 初始化会话
      action: execute
      script: scripts/note.py
      args:
        - "--phase"
        - "detect"
        - "--set"
        - "incident_name={{incident_name}}"
```

**OpenClaw工作流定义**（建议新增）：
```yaml
# openclaw_workflows/ir_full.yaml
workflow:
  name: 企业应急响应全流程
  phases:
    - detect
    - triage
    - contain
    - eradicate
    - recover
    - postmortem
    - report
  
  transitions:
    detect_to_triage:
      condition: "事件确认真实"
      required_evidence: ["告警详情", "初步范围"]
    
    triage_to_contain:
      condition: "根因明确"
      required_evidence: ["IOC清单", "时间线"]
      hitl_required: true
```

### 4. Cursor / Trae（已适配）

**使用方式**：参考`使用指南与提示词示例.md`

**会话第一条提示词**：
```text
你是单位的应急响应协作助手，必须遵守"企业应急响应指导Skill/SKILL.md"和playbooks。
你需要把处置过程做成可审计的作业系统，而不是聊天。
...
```

### 5. 其他智能体平台通用适配

**最小适配要求**：
1. 支持加载Markdown文档作为上下文
2. 支持执行外部Python脚本或提供替代方案
3. 支持结构化数据存储（JSON）

**通用适配检查清单**：
- [ ] 是否支持加载本地文件？
- [ ] 是否支持执行Python脚本？
- [ ] 是否支持结构化输出？
- [ ] 是否支持多轮对话上下文？
- [ ] 是否支持人工确认闸门（HITL）？

## 跨平台API规范建议

为了实现真正的跨智能体兼容，建议实现统一的API接口：

### RESTful API设计

```yaml
openapi: 3.0.0
info:
  title: 企业应急响应指导API
  version: 1.0.0

paths:
  /api/session/init:
    post:
      summary: 初始化应急会话
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                incident_name:
                  type: string
                scope:
                  type: string
                phase:
                  type: string
                  enum: [detect, triage, contain, eradicate, recover, postmortem, report]
      responses:
        200:
          description: 会话已初始化
          
  /api/note:
    post:
      summary: 记录应急响应事实
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                text:
                  type: string
                phase:
                  type: string
                action:
                  type: string
                  enum: [verify, collect, analyze, contain, eradicate, recover]
                evidence:
                  type: array
                  items:
                    type: string
                ioc:
                  type: object
                  properties:
                    ip:
                      type: array
                    domain:
                      type: array
                    hash:
                      type: array
  
  /api/report:
    get:
      summary: 生成应急响应报告
      parameters:
        - name: format
          in: query
          schema:
            type: string
            enum: [markdown, json, html]
      responses:
        200:
          description: 报告内容
```

### SDK封装

```python
# sdk/ir_client.py
class EmergencyResponseClient:
    """统一应急响应客户端SDK"""
    
    def __init__(self, endpoint="http://localhost:5000"):
        self.endpoint = endpoint
    
    def init_session(self, incident_name: str, scope: str, **kwargs):
        """初始化应急会话"""
        pass
    
    def record_action(self, text: str, phase: str, **kwargs):
        """记录应急动作"""
        pass
    
    def add_ioc(self, ip=None, domain=None, hash=None, **kwargs):
        """添加IOC"""
        pass
    
    def add_timeline(self, event: str, timestamp: str):
        """添加时间线事件"""
        pass
    
    def generate_report(self, format="markdown"):
        """生成报告"""
        pass
    
    def detect_loop(self):
        """检测是否卡住/打转"""
        pass
```

## 部署架构建议

### 单机部署（适合OpenCode/Cursor）
```
本地文件系统
├── SKILL.md
├── scripts/*.py
└── memory/
```

### 客户端-服务器部署（适合Hermes/OpenClaw）
```
客户端（智能体）
  ↓ HTTP API
服务器（API网关）
  ├── scripts/
  ├── memory/
  └── playbooks/
```

### 云端部署（适合云端智能体）
```
云函数（AWS Lambda/阿里云函数计算）
  ├── 应急响应函数
  └── 对象存储（证据/报告）
```

## 兼容性矩阵

| 智能体平台 | 当前状态 | 适配难度 | 建议方案 |
|----------|---------|---------|---------|
| OpenCode | ✅ 已适配 | 低 | 直接使用 |
| Cursor | ✅ 已适配 | 低 | 提示词模式 |
| Trae | ✅ 已适配 | 低 | 提示词模式 |
| Hermes Agent | ⚠️ 需适配 | 中 | HTTP API + 工具插件 |
| OpenClaw | ⚠️ 需适配 | 中 | 任务模板 + 工作流编排 |
| AutoGPT | ⚠️ 需适配 | 高 | 重新设计prompt + 插件 |
| LangChain | ⚠️ 需适配 | 中 | Chain + Tool封装 |
| 其他云端智能体 | ⚠️ 需适配 | 高 | 云函数 + API网关 |

## 后续优化建议

### 优先级1（立即补充）
1. 添加`.opencode/opencode.json`配置 ✅ 已完成
2. 创建跨平台API规范文档
3. 提供SDK封装示例

### 优先级2（中期优化）
1. 实现HTTP API服务器
2. 提供Docker容器化部署方案
3. 补充Hermes/OpenClaw适配示例

### 优先级3（长期优化）
1. 实现云端部署版本
2. 提供Web UI界面
3. 集成到更多智能体平台
