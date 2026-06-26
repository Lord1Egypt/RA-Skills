# Photo Search Skill

📸 智能照片搜索技能 - 基于 VL 大模型的照片索引和语义搜索

## 📋 概述

Photo Search Skill 是一个**独立的**智能技能程序，用于扫描、索引和搜索照片。它利用 VL（Vision-Language）大模型分析照片内容，建立结构化索引，并支持通过自然语言进行语义搜索。

### ✨ 特性

- 🔍 **完全独立**：可以从任何目录调用，无需设置环境变量
- 🤖 **智能体友好**：专为 hermes、openclaw 等智能体设计
- 📦 **零配置调用**：自动定位主项目，无需手动配置路径
- 🌐 **JSON 输出**：支持结构化输出，便于智能体解析

### 核心能力

- 🔍 **照片扫描**：扫描指定目录的所有照片文件
- 🤖 **VL 分析**：使用本地/远程 VL 模型智能解读照片内容
- 📊 **自动索引**：生成场景、物体、人物、标签等结构化数据
- 🔎 **语义搜索**：支持自然语言查询，理解搜索意图
- 🏷️ **人工标注**：用户可自定义标签，训练个性化识别
- 🌐 **CLI 接口**：通过命令行调用，易于集成到智能体

## 🚀 快速使用

### 智能体调用方式

智能体（如 hermes, openclaw 等）可以通过命令行直接调用此技能：

```bash
# 从任何目录调用（使用绝对路径）
python G:\python\PhotoIndexWithLLM\skills\photo-search\skill.py search "海滩日落"

# 扫描照片
python G:\python\PhotoIndexWithLLM\skills\photo-search\skill.py scan --dir D:\Photos

# 扫描并搜索（一步完成）
python G:\python\PhotoIndexWithLLM\skills\photo-search\skill.py scan_and_search --dir D:\Photos --query "海边"

# JSON 格式输出（便于智能体解析）
python G:\python\PhotoIndexWithLLM\skills\photo-search\skill.py search "海滩" --format json
```

### 在项目目录中调用

```bash
cd G:\python\PhotoIndexWithLLM

# 扫描照片
python skills/photo-search/skill.py scan --dir D:\Photos

# 搜索照片
python skills/photo-search/skill.py search "海滩日落"

# 扫描并搜索
python skills/photo-search/skill.py scan_and_search --dir D:\Photos --query "海边"
```

## 📖 智能体调用指南

### 环境要求

**主项目需要配置好：**
- Python 3.10+
- 已安装依赖：`pip install -r requirements.txt`
- 已配置 `.env` 文件
- LM Studio 运行在端口 1234（如需本地模型）

**Skill 本身无需额外配置！**

### 基本调用模式

```bash
# 1. 扫描并索引照片
python <skill路径> scan --dir <照片目录>

# 2. 搜索照片
python <skill路径> search "<搜索关键词>"

# 3. 扫描并搜索（组合命令）
python <skill路径> scan_and_search --dir <目录> --query "<关键词>"
```

### 智能体工作流程

```
用户请求："帮我找一下海边的照片"
    ↓
智能体执行：
    python G:\python\PhotoIndexWithLLM\skills\photo-search\skill.py search "海边"
    ↓
返回结果：
    {
      "results": [...],
      "total": 5,
      "search_type": "hybrid"
    }
    ↓
智能体回复用户：
    "找到了5张海边的照片..."
```

## 🎯 完整命令参考

### 扫描照片

```bash
# 扫描指定目录
python skill.py scan --dir D:\MyPhotos

# 扫描多个目录
python skill.py scan --dir D:\Photos E:\Pictures

# 强制重新索引
python skill.py scan --force --dir D:\Photos
```

### 搜索照片

```bash
# 关键词搜索
python skill.py search "海滩 日落"

# 语义搜索（自然语言）
python skill.py search "蓝色的海边风景"

# 带标签过滤
python skill.py search "旅行" --tags 风景,人物

# 按场景过滤
python skill.py search "风景" --scene 户外

# 按日期范围
python skill.py search "旅行" --date-from 2024-01-01 --date-to 2024-12-31

# 限制返回数量
python skill.py search "海滩" --limit 10

# JSON 格式输出
python skill.py search "海滩" --format json
```

### 扫描并搜索（组合命令）

```bash
# 一步完成：先扫描，再搜索
python skill.py scan_and_search --dir D:\Photos --query "海边"

# JSON 输出
python skill.py scan_and_search --dir D:\Photos --query "海边" --format json
```

### 人工标注

```bash
# 为照片添加标签
python skill.py annotate --photo D:\Photos\img001.jpg --type person --name 张三

# 添加场景标签
python skill.py annotate --photo D:\Photos\img002.jpg --type scene --name 海边

# JSON 输出
python skill.py annotate --photo D:\Photos\img001.jpg --type person --name 张三 --format json
```

### 训练模型

```bash
# 训练个性化模型
python skill.py train

# JSON 输出
python skill.py train --format json
```

### 其他命令

```bash
# 查看统计信息
python skill.py stats

# 测试 LLM 连接
python skill.py test

# 列出照片
python skill.py list --limit 20
```

## 🤖 智能体集成示例

### 示例 1：Python 智能体（Hermes、OpenClaw 等）

```python
import subprocess
import json

def search_photos(query: str, limit: int = 20) -> dict:
    """搜索照片"""
    skill_path = r"G:\python\PhotoIndexWithLLM\skills\photo-search\skill.py"
    
    result = subprocess.run(
        ["python", skill_path, "search", query, "--limit", str(limit), "--format", "json"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        return {"error": result.stderr}

# 使用
photos = search_photos("海滩日落")
print(f"找到 {photos['total']} 张照片")
```

### 示例 2：Shell 脚本智能体

```bash
#!/bin/bash
# photo_agent.sh - 智能体照片搜索脚本

SKILL="G:\python\PhotoIndexWithLLM\skills\photo-search\skill.py"

# 搜索照片
search_photos() {
    local query="$1"
    local limit="${2:-20}"
    
    python "$SKILL" search "$query" --limit "$limit" --format json
}

# 扫描照片
scan_photos() {
    local dir="$1"
    python "$SKILL" scan --dir "$dir"
}

# 使用
search_photos "海滩" 10
```

### 示例 3：通用智能体封装

```python
class PhotoSearchSkill:
    """照片搜索技能封装"""
    
    def __init__(self, skill_path: str):
        self.skill_path = skill_path
    
    def search(self, query: str, **kwargs) -> dict:
        """搜索照片"""
        cmd = ["python", self.skill_path, "search", query]
        
        if kwargs.get("format") == "json":
            cmd.append("--format")
            cmd.append("json")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(result.stdout) if result.returncode == 0 else None
    
    def scan(self, directories: list) -> bool:
        """扫描照片"""
        cmd = ["python", self.skill_path, "scan", "--dir"] + directories
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    
    def annotate(self, photo: str, type: str, name: str) -> bool:
        """添加标注"""
        cmd = [
            "python", self.skill_path, "annotate",
            "--photo", photo,
            "--type", type,
            "--name", name
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
```

## 📊 输出格式

### JSON 输出示例

```json
{
  "results": [
    {
      "file_name": "beach_sunset_001.jpg",
      "file_path": "D:\\Photos\\2024\\beach_sunset_001.jpg",
      "scene_type": "风景",
      "description": "海边的日落，天空呈现橙红色",
      "tags": ["海滩", "日落", "风景", "海洋"],
      "confidence_score": 0.92
    }
  ],
  "total": 5,
  "search_type": "hybrid"
}
```

### 文本输出示例

```
🔍 搜索查询: '海滩 日落'
📊 找到 5 条结果

1. beach_sunset_001.jpg
   📁 D:\Photos\2024\beach_sunset_001.jpg
   🏷️ 场景: 风景
   📝 描述: 海边的日落，天空呈现橙红色
   🔖 标签: 海滩, 日落, 风景, 海洋
   ⭐ 置信度: 0.92
```

## ⚙️ 配置说明

### 主项目配置

Skill 依赖于主项目的配置（`.env` 文件），主要包括：

```ini
# 本地 LLM
LOCAL_LLM_ENDPOINT=http://localhost:1234/v1
LOCAL_LLM_MODEL=qwen3-vl-8b-q4_k_m

# 远程 LLM（可选）
REMOTE_LLM_API_KEY=your-api-key
REMOTE_LLM_MODEL=nvidia/nemotron-nano-12b-v2-vl:free

# 照片目录
PHOTO_SCAN_DIRS=D:\Photos
```

### Skill 参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `query` | 搜索关键词 | "海滩" |
| `--dir` | 扫描目录 | "D:\Photos" |
| `--tags` | 标签过滤 | "风景,人物" |
| `--scene` | 场景类型 | "户外" |
| `--date-from` | 起始日期 | "2024-01-01" |
| `--date-to` | 结束日期 | "2024-12-31" |
| `--limit` | 返回数量 | 20 |
| `--format` | 输出格式 | json 或 text |
| `--no-vector` | 禁用向量搜索 | - |

## 🔧 故障排除

### 问题 1：找不到 skill.py

**解决方案：**
```bash
# 使用绝对路径
python G:\python\PhotoIndexWithLLM\skills\photo-search\skill.py search "海滩"
```

### 问题 2：找不到项目根目录

**解决方案：**
```bash
# 确保主项目存在
ls G:\python\PhotoIndexWithLLM\config.py
```

### 问题 3：本地模型连接失败

```bash
# 测试连接
python skill.py test

# 检查 LM Studio 是否运行
netstat -ano | findstr :1234
```

### 问题 4：搜索无结果

```bash
# 1. 确认已索引照片
python skill.py stats

# 2. 重新扫描
python skill.py scan --force --dir D:\Photos

# 3. 尝试不同关键词
python skill.py search "海边"
```

## 🌟 高级用法

### 批量搜索

```bash
# 搜索多个关键词
python skill.py search "海滩" --format json > beach.json
python skill.py search "山脉" --format json > mountain.json
python skill.py search "城市" --format json > city.json
```

### 智能体管道

```bash
# 搜索 → 过滤 → 发送
python skill.py search "海滩" --format json | jq '.results[] | .file_path' | send_to_user
```

### 定时任务

```bash
# Windows 任务计划程序
# 每天凌晨2点扫描新照片
0 2 * * * python G:\python\PhotoIndexWithLLM\skills\photo-search\skill.py scan --dir D:\Photos
```

## 📝 注意事项

1. **独立性**：Skill 是独立程序，但依赖主项目的配置和功能
2. **路径**：建议使用绝对路径调用 skill.py
3. **首次使用**：需要先扫描并索引照片才能搜索
4. **本地模型**：需要 LM Studio 运行在端口 1234
5. **JSON 输出**：智能体解析时务必使用 `--format json`

## 📞 获取帮助

- 查看帮助：`python skill.py --help`
- 查看文档：`SKILL.md`（本文件）
- 查看主项目文档：`README.md`, `USAGE.md`

---

**Skill 版本**: v1.0  
**独立版本**: ✅  
**兼容智能体**: hermes, openclaw, 所有支持 CLI 的智能体  
**更新日期**: 2026-05-16
