# Hermes 智能体集成示例

这个文件展示了如何将 Photo Search Skill 集成到 Hermes 智能体中。

## 基本集成

```python
import subprocess
import json

class PhotoSearchSkill:
    """Photo Search Skill for Hermes Agent"""
    
    def __init__(self, skill_path: str = "G:\\python\\PhotoIndexWithLLM\\skills\\photo-search"):
        self.skill_path = skill_path
    
    def scan(self, directories: list = None, force: bool = False) -> dict:
        """扫描照片"""
        cmd = ["python", f"{self.skill_path}/skill.py", "scan"]
        
        if directories:
            cmd.extend(["--dir"] + directories)
        
        if force:
            cmd.append("--force")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }
    
    def search(self, query: str, **kwargs) -> dict:
        """搜索照片"""
        cmd = [
            "python", f"{self.skill_path}/skill.py",
            "search", query,
            "--format", "json"
        ]
        
        if kwargs.get("tags"):
            cmd.extend(["--tags", kwargs["tags"]])
        
        if kwargs.get("scene"):
            cmd.extend(["--scene", kwargs["scene"]])
        
        if kwargs.get("date_from"):
            cmd.extend(["--date-from", kwargs["date_from"]])
        
        if kwargs.get("date_to"):
            cmd.extend(["--date-to", kwargs["date_to"]])
        
        if kwargs.get("limit"):
            cmd.extend(["--limit", str(kwargs["limit"])])
        
        if kwargs.get("no_vector"):
            cmd.append("--no-vector")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            try:
                return {
                    "success": True,
                    "data": json.loads(result.stdout)
                }
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error": "Failed to parse JSON output",
                    "output": result.stdout
                }
        else:
            return {
                "success": False,
                "error": result.stderr
            }
    
    def scan_and_search(self, directories: list, query: str, **kwargs) -> dict:
        """扫描并搜索"""
        cmd = [
            "python", f"{self.skill_path}/skill.py",
            "scan_and_search",
            "--query", query,
            "--format", "json"
        ]
        
        if directories:
            cmd.extend(["--dir"] + directories)
        
        if kwargs.get("tags"):
            cmd.extend(["--tags", kwargs["tags"]])
        
        if kwargs.get("scene"):
            cmd.extend(["--scene", kwargs["scene"]])
        
        if kwargs.get("limit"):
            cmd.extend(["--limit", str(kwargs["limit"])])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            try:
                return {
                    "success": True,
                    "data": json.loads(result.stdout)
                }
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error": "Failed to parse JSON output",
                    "output": result.stdout
                }
        else:
            return {
                "success": False,
                "error": result.stderr
            }
    
    def stats(self) -> dict:
        """获取统计信息"""
        cmd = [
            "python", f"{self.skill_path}/skill.py",
            "stats", "--format", "json"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            try:
                return {
                    "success": True,
                    "data": json.loads(result.stdout)
                }
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error": "Failed to parse JSON output"
                }
        else:
            return {
                "success": False,
                "error": result.stderr
            }
    
    def annotate(self, photo_path: str, label_type: str, label_name: str, label_value: str = "") -> dict:
        """添加标注"""
        cmd = [
            "python", f"{self.skill_path}/skill.py",
            "annotate",
            "--photo", photo_path,
            "--type", label_type,
            "--name", label_name,
            "--format", "json"
        ]
        
        if label_value:
            cmd.extend(["--value", label_value])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            try:
                return {
                    "success": True,
                    "data": json.loads(result.stdout)
                }
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error": "Failed to parse JSON output"
                }
        else:
            return {
                "success": False,
                "error": result.stderr
            }
    
    def train(self, force: bool = False) -> dict:
        """训练模型"""
        cmd = [
            "python", f"{self.skill_path}/skill.py",
            "train", "--format", "json"
        ]
        
        if force:
            cmd.append("--force")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            try:
                return {
                    "success": True,
                    "data": json.loads(result.stdout)
                }
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error": "Failed to parse JSON output"
                }
        else:
            return {
                "success": False,
                "error": result.stderr
            }


# 使用示例
if __name__ == "__main__":
    skill = PhotoSearchSkill()
    
    # 扫描照片
    result = skill.scan(directories=["D:\\Photos"])
    print(result)
    
    # 搜索照片
    result = skill.search("海滩日落", limit=10)
    print(result)
    
    # 添加标注
    result = skill.annotate("D:\\Photos\\img001.jpg", "person", "张三")
    print(result)
    
    # 训练模型
    result = skill.train()
    print(result)
```

## Hermes 智能体工具注册

```python
from hermes import Agent, Tool

class PhotoSearchAgent(Agent):
    def __init__(self):
        super().__init__(name="PhotoSearchAgent")
        self.skill = PhotoSearchSkill()
        
        # 注册工具
        self.register_tool(Tool(
            name="search_photos",
            description="Search for photos by keywords, tags, or descriptions",
            parameters={
                "query": {"type": "string", "required": True, "description": "Search query"},
                "tags": {"type": "string", "required": False, "description": "Tags filter (comma-separated)"},
                "scene": {"type": "string", "required": False, "description": "Scene type filter"},
                "limit": {"type": "integer", "required": False, "description": "Number of results", "default": 20}
            },
            handler=self.search_photos
        ))
        
        self.register_tool(Tool(
            name="scan_photos",
            description="Scan and index photos from a directory",
            parameters={
                "directories": {"type": "array", "required": True, "description": "Directories to scan"},
                "force": {"type": "boolean", "required": False, "description": "Force re-indexing", "default": False}
            },
            handler=self.scan_photos
        ))
        
        self.register_tool(Tool(
            name="annotate_photo",
            description="Add labels to a photo for better search",
            parameters={
                "photo_path": {"type": "string", "required": True, "description": "Path to the photo"},
                "label_type": {"type": "string", "required": True, "enum": ["person", "scene", "activity", "custom"]},
                "label_name": {"type": "string", "required": True, "description": "Label name"},
                "label_value": {"type": "string", "required": False, "description": "Label description"}
            },
            handler=self.annotate_photo
        ))
    
    def search_photos(self, query: str, **kwargs):
        """搜索照片工具处理"""
        return self.skill.search(query, **kwargs)
    
    def scan_photos(self, directories: list, force: bool = False):
        """扫描照片工具处理"""
        return self.skill.scan(directories, force)
    
    def annotate_photo(self, photo_path: str, label_type: str, label_name: str, **kwargs):
        """标注照片工具处理"""
        return self.skill.annotate(photo_path, label_type, label_name, kwargs.get("label_value", ""))
```

## 对话示例

```
用户: 帮我找一下海边的照片

Hermes: [调用 search_photos 工具]
       skill.search("海边")
       
Hermes: 找到了 5 张海边的照片:
       1. beach_sunset_001.jpg - 海边日落
       2. beach_walk_002.jpg - 沙滩漫步
       ...

用户: 这张照片里有谁？(指向 beach_walk_002.jpg)

Hermes: [调用 annotate_photo 工具]
       skill.annotate("D:\\Photos\\beach_walk_002.jpg", "person", "张三")
       
Hermes: 我已经为这张照片添加了"张三"的标签。
       现在你可以通过搜索"张三"找到这张照片。

用户: 扫描我D盘的所有照片

Hermes: [调用 scan_photos 工具]
       skill.scan(["D:\\Photos"])
       
Hermes: 扫描完成，已索引 1234 张照片。
```
