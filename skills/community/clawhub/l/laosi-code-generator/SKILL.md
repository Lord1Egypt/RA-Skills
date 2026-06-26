---
name: code-generator
version: 1.0.0
description: 代码生成 - 项目脚手架/函数模板/配置文件生成，支持Python/JS/Go多语言，自动创建目录结构
tags: [code, generation, scaffolding, template, development]
author: laosi
source: original
---

# Code Generator - 代码生成器

> 激活词: 生成代码 / code generate / 项目脚手架

## 功能

- 项目脚手架生成（Python/JS/Go）
- 函数模板（API handler/CronJob/CLI）
- 配置文件生成（YAML/JSON/TOML）
- 自动创建目录结构
- 代码片段库

## Python 实现

```python
import os, json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class FileSpec:
    """文件规格"""
    path: str          # 相对路径, e.g. "src/main.py"
    content: str       # 文件内容
    overwrite: bool = False  # 是否允许覆盖
    
@dataclass
class ProjectTemplate:
    """项目模板"""
    name: str
    language: str
    description: str
    files: List[FileSpec] = field(default_factory=list)
    
    def add_file(self, path: str, content: str, overwrite: bool = False):
        self.files.append(FileSpec(path=path, content=content, overwrite=overwrite))
    
    def generate(self, output_dir: str) -> Dict:
        """生成项目到指定目录"""
        results = {"created": [], "skipped": [], "errors": []}
        for file_spec in self.files:
            full_path = os.path.join(output_dir, file_spec.path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            if os.path.exists(full_path) and not file_spec.overwrite:
                results["skipped"].append(file_spec.path)
                continue
            
            try:
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(file_spec.content)
                results["created"].append(file_spec.path)
            except Exception as e:
                results["errors"].append(f"{file_spec.path}: {e}")
        
        return results

class CodeGenerator:
    def __init__(self):
        self.templates: Dict[str, ProjectTemplate] = {}
        self._register_defaults()
    
    def _register_defaults(self):
        """注册内置模板"""
        # Python CLI项目
        py_cli = ProjectTemplate(
            name="python-cli",
            language="python",
            description="Python CLI application with argparse"
        )
        py_cli.add_file("main.py", """#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(description="CLI tool")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose")
    args = parser.parse_args()
    
    if args.verbose:
        print("Verbose mode enabled")
    print("Hello from CLI!")

if __name__ == "__main__":
    main()
""")
        py_cli.add_file("requirements.txt", "# Dependencies\n# requests>=2.28.0\n")
        py_cli.add_file(".gitignore", "*.pyc\n__pycache__/\n.env\nvenv/\n")
        py_cli.add_file("README.md", f"# CLI Tool\n\nAuto-generated Python CLI project\n")
        self.templates["python-cli"] = py_cli
        
        # FastAPI服务
        fastapi_t = ProjectTemplate(
            name="fastapi-service",
            language="python",
            description="FastAPI REST API service"
        )
        fastapi_t.add_file("main.py", """from fastapi import FastAPI
app = FastAPI(title="API Service")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/items")
def list_items():
    return {"items": []}
""")
        fastapi_t.add_file("requirements.txt", "fastapi==0.110.0\nuvicorn==0.29.0\n")
        self.templates["fastapi-service"] = fastapi_t
        
        # JS项目
        js_t = ProjectTemplate(
            name="node-express",
            language="javascript",
            description="Node.js Express API"
        )
        js_t.add_file("index.js", """const express = require('express');
const app = express();
app.use(express.json());

app.get('/health', (req, res) => {
    res.json({ status: 'ok' });
});

app.listen(3000, () => console.log('Server running on :3000'));
""")
        js_t.add_file("package.json", json.dumps({
            "name": "api-service",
            "version": "1.0.0",
            "main": "index.js",
            "dependencies": {"express": "^4.18.0"}
        }, indent=2))
        self.templates["node-express"] = js_t
    
    def list_templates(self) -> List[Dict]:
        return [
            {"name": t.name, "language": t.language,
             "description": t.description, "files": len(t.files)}
            for t in self.templates.values()
        ]
    
    def generate_from_template(self, template_name: str, output_dir: str) -> Dict:
        """从模板生成项目"""
        if template_name not in self.templates:
            return {"error": f"Unknown template: {template_name}. Available: {list(self.templates.keys())}"}
        
        template = self.templates[template_name]
        os.makedirs(output_dir, exist_ok=True)
        return template.generate(output_dir)
    
    def generate_api_handler(self, name: str, methods: List[str]) -> str:
        """生成API handler代码"""
        method_handlers = "\n\n".join([
            f"async def {m.lower()}_{name}(request):\n    \"\"\"{m} /api/{name}\"\"\"\n    return {{'method': '{m}', 'handler': '{name}'}}"
            for m in methods
        ])
        return f"""
from typing import Dict, Any

# Auto-generated API handler: {name}
{method_handlers}

def register_routes(app):
    \"\"\"Register all routes for {name}\"\"\"
    pass
"""
    
    def generate_config(self, config_type: str = "yaml") -> str:
        """生成配置文件"""
        configs = {
            "yaml": """# Auto-generated config
app:
  name: my-app
  version: 0.1.0
  debug: true
  env: development

server:
  host: 0.0.0.0
  port: 8080

database:
  url: sqlite:///data.db
  pool_size: 5
  timeout: 30

logging:
  level: info
  format: json
""",
            "json": json.dumps({
                "app": {"name": "my-app", "version": "0.1.0", "debug": True},
                "server": {"host": "0.0.0.0", "port": 8080},
                "database": {"url": "sqlite:///data.db", "pool_size": 5}
            }, indent=2),
            "toml": """[app]
name = "my-app"
version = "0.1.0"

[server]
host = "0.0.0.0"
port = 8080

[database]
url = "sqlite:///data.db"
"""
        }
        return configs.get(config_type, configs["yaml"])

# 使用示例
gen = CodeGenerator()

# 列出可用模板
print("可用模板:")
for t in gen.list_templates():
    print(f"  [{t['language']}] {t['name']}: {t['description']} ({t['files']}个文件)")

# 生成Python CLI项目
result = gen.generate_from_template("python-cli", "./my-cli-tool")
print(f"\n生成结果: created={result['created']}, skipped={result['skipped']}")

# 生成API handler
handler_code = gen.generate_api_handler("users", ["GET", "POST", "PUT", "DELETE"])
print(f"\nHandler代码 ({len(handler_code)} chars):")
print(handler_code[:200] + "...")

# 生成配置
config = gen.generate_config("yaml")
print(f"\n配置文件 ({len(config)} chars)")
```

## 支持的模板

| 模板名 | 语言 | 用途 | 文件数 |
|--------|------|------|--------|
| python-cli | Python | CLI工具 | 4 |
| fastapi-service | Python | REST API | 2 |
| node-express | JavaScript | Web API | 2 |

## 使用场景

1. **项目启动**: 新项目一键生成标准目录结构
2. **API开发**: 快速生成增删改查handler
3. **微服务**: 统一的服务模板，保证团队一致性
4. **学习实验**: 快速生成实验项目脚手架

## 依赖

- Python 3.8+
- 无第三方依赖
