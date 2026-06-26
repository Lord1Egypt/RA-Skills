# OpenClaw 智能体集成示例

这个文件展示了如何将 Photo Search Skill 集成到 OpenClaw 智能体中。

## Shell 脚本集成

```bash
#!/bin/bash
# photo_search_skill.sh - OpenClaw 智能体照片搜索技能

SKILL_DIR="G:\\python\\PhotoIndexWithLLM\\skills\\photo-search"

# 搜索照片
search_photos() {
    local query="$1"
    local limit="${2:-20}"
    
    python "$SKILL_DIR/skill.py" search "$query" --limit $limit --format json
}

# 扫描照片
scan_photos() {
    local dir="$1"
    local force="${2:-false}"
    
    if [ "$force" = "true" ]; then
        python "$SKILL_DIR/skill.py" scan --dir "$dir" --force
    else
        python "$SKILL_DIR/skill.py" scan --dir "$dir"
    fi
}

# 添加标注
annotate_photo() {
    local photo_path="$1"
    local label_type="$2"
    local label_name="$3"
    local label_value="$4"
    
    python "$SKILL_DIR/skill.py" annotate \
        --photo "$photo_path" \
        --type "$label_type" \
        --name "$label_name" \
        --value "$label_value" \
        --format json
}

# 训练模型
train_model() {
    python "$SKILL_DIR/skill.py" train --format json
}

# 获取统计
get_stats() {
    python "$SKILL_DIR/skill.py" stats --format json
}

# 命令行接口
case "$1" in
    search)
        search_photos "$2" "$3"
        ;;
    scan)
        scan_photos "$2" "$3"
        ;;
    annotate)
        annotate_photo "$2" "$3" "$4" "$5"
        ;;
    train)
        train_model
        ;;
    stats)
        get_stats
        ;;
    *)
        echo "Usage: $0 {search|scan|annotate|train|stats} [args...]"
        exit 1
        ;;
esac
```

## OpenClaw 智能体配置

```yaml
# openclaw_config.yaml
skills:
  photo_search:
    enabled: true
    path: "G:\\python\\PhotoIndexWithLLM\\skills\\photo-search"
    commands:
      search: "python skill.py search {query} --format json"
      scan: "python skill.py scan --dir {directory}"
      annotate: "python skill.py annotate --photo {photo} --type {type} --name {name}"
      train: "python skill.py train --format json"
      stats: "python skill.py stats --format json"
```

## OpenClaw 智能体插件

```python
# openclaw_photo_plugin.py

import subprocess
import json
from typing import Dict, Any

class PhotoSearchPlugin:
    """OpenClaw 照片搜索插件"""
    
    def __init__(self, skill_path: str = "G:\\python\\PhotoIndexWithLLM\\skills\\photo-search"):
        self.skill_path = skill_path
        self.name = "photo_search"
        self.description = "Search and manage photos using VL models"
    
    def execute(self, command: str, **kwargs) -> Dict[str, Any]:
        """执行命令"""
        cmd = ["python", f"{self.skill_path}/skill.py", command]
        
        # 添加参数
        for key, value in kwargs.items():
            if isinstance(value, bool):
                if value:
                    cmd.append(f"--{key.replace('_', '-')}")
            elif isinstance(value, list):
                cmd.append(f"--{key.replace('_', '-')}")
                cmd.extend(value)
            else:
                cmd.append(f"--{key.replace('_', '-')}")
                cmd.append(str(value))
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse output",
                "output": result.stdout,
                "stderr": result.stderr
            }
    
    def search(self, query: str, **kwargs) -> Dict[str, Any]:
        """搜索照片"""
        return self.execute("search", query=query, format="json", **kwargs)
    
    def scan(self, directories: list, **kwargs) -> Dict[str, Any]:
        """扫描照片"""
        return self.execute("scan", dir=directories, **kwargs)
    
    def annotate(self, photo_path: str, label_type: str, label_name: str, **kwargs) -> Dict[str, Any]:
        """标注照片"""
        return self.execute(
            "annotate",
            photo=photo_path,
            type=label_type,
            name=label_name,
            **kwargs
        )
    
    def train(self, **kwargs) -> Dict[str, Any]:
        """训练模型"""
        return self.execute("train", format="json", **kwargs)
    
    def stats(self) -> Dict[str, Any]:
        """获取统计"""
        return self.execute("stats", format="json")


# OpenClaw 注册
def register(agent):
    """注册到 OpenClaw 智能体"""
    plugin = PhotoSearchPlugin()
    
    agent.register_skill(
        name="photo_search",
        description="Search, scan, and annotate photos",
        plugin=plugin,
        commands={
            "search": plugin.search,
            "scan": plugin.scan,
            "annotate": plugin.annotate,
            "train": plugin.train,
            "stats": plugin.stats
        }
    )
```

## OpenClaw 对话示例

```yaml
conversation:
  - user: "Find photos of the beach sunset"
    agent:
      skill: photo_search
      action: search
      params:
        query: "beach sunset"
        limit: 10
      response: |
        I found 5 photos of beach sunsets:
        1. beach_sunset_001.jpg - Beautiful sunset over the ocean
        2. beach_sunset_002.jpg - Walking on the beach at dusk
        ...

  - user: "Label the first photo with 'John and Mary'"
    agent:
      skill: photo_search
      action: annotate
      params:
        photo_path: "D:\\Photos\\beach_sunset_001.jpg"
        label_type: "person"
        label_name: "John and Mary"
      response: "I've added the label 'John and Mary' to the photo."

  - user: "Scan my Photos folder"
    agent:
      skill: photo_search
      action: scan
      params:
        directories: ["D:\\Photos"]
      response: "Scanning complete. Indexed 1,234 photos."
```
