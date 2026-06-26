"""
技能清单生成器
生成符合OpenClaw规范的技能清单
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SkillManifest:
    """OpenClaw技能清单"""
    
    # 基本信息
    name: str = "智能数据采集器"
    slug: str = "data-harvester"
    description: str = "自动化数据采集、处理和导出工具"
    version: str = "1.0.0"
    author: str = "OpenClaw Wealth Guide"
    homepage: str = "https://github.com/openclaw-wealth-guide/data-harvester"
    license: str = "MIT"
    
    # 分类和标签
    category: str = "data-collection"
    subcategory: Optional[str] = "automation"
    tags: List[str] = field(default_factory=lambda: [
        "data", "collection", "analysis", "automation", "web-scraping"
    ])
    
    # 技术信息
    min_claw_version: str = "0.8.0"
    python_version: str = ">=3.12"
    dependencies: List[str] = field(default_factory=lambda: [
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "pandas>=2.0.0",
        "APScheduler>=3.10.0",
        "pydantic>=2.0.0",
        "cryptography>=42.0.0",
        "SQLAlchemy>=2.0.0"
    ])
    
    # 运行时信息
    entrypoint: str = "data_harvester.openclaw_integration:OpenClawSkillWrapper"
    config_schema: Dict[str, Any] = field(default_factory=lambda: {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "采集器名称",
                "default": "智能数据采集器"
            },
            "log_level": {
                "type": "string",
                "enum": ["DEBUG", "INFO", "WARNING", "ERROR"],
                "description": "日志级别",
                "default": "INFO"
            },
            "sources": {
                "type": "object",
                "description": "数据源配置",
                "additionalProperties": {
                    "type": "object",
                    "required": ["name", "type", "url"],
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string", "enum": ["web", "api", "file", "database"]},
                        "url": {"type": "string"},
                        "enabled": {"type": "boolean", "default": True}
                    }
                }
            },
            "processing": {
                "type": "object",
                "properties": {
                    "enabled": {"type": "boolean", "default": True},
                    "strategy": {
                        "type": "array",
                        "items": {"type": "string", "enum": ["clean", "transform", "validate", "deduplicate"]}
                    }
                }
            },
            "exports": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name", "format"],
                    "properties": {
                        "name": {"type": "string"},
                        "format": {"type": "string", "enum": ["csv", "json", "excel"]},
                        "enabled": {"type": "boolean", "default": True}
                    }
                }
            }
        }
    })
    
    # 权限和范围
    required_scopes: List[str] = field(default_factory=lambda: [
        "files:read",
        "files:write",
        "web:fetch",
        "web:search",
        "browser:automate",
        "network:outbound"
    ])
    
    # 操作定义
    operations: Dict[str, Any] = field(default_factory=lambda: {
        "collect": {
            "name": "collect",
            "description": "从指定数据源收集数据",
            "method": "POST",
            "path": "/api/v1/collect/{source_name}",
            "parameters": [
                {
                    "name": "source_name",
                    "type": "string",
                    "description": "数据源名称",
                    "required": True,
                    "in": "path"
                },
                {
                    "name": "force_refresh",
                    "type": "boolean",
                    "description": "强制刷新数据",
                    "required": False,
                    "in": "query",
                    "default": False
                }
            ],
            "response": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "data": {"type": ["object", "array", "null"]},
                    "source": {"type": "string"},
                    "metadata": {"type": "object"},
                    "errors": {"type": "array", "items": {"type": "string"}}
                }
            }
        },
        "collect_all": {
            "name": "collect_all",
            "description": "从所有数据源收集数据",
            "method": "POST",
            "path": "/api/v1/collect/all",
            "response": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "results": {"type": "object"},
                    "total_sources": {"type": "integer"},
                    "successful_sources": {"type": "integer"},
                    "failed_sources": {"type": "integer"}
                }
            }
        },
        "export": {
            "name": "export",
            "description": "导出数据到指定格式",
            "method": "POST",
            "path": "/api/v1/export",
            "parameters": [
                {
                    "name": "data",
                    "type": "any",
                    "description": "要导出的数据",
                    "required": True,
                    "in": "body"
                },
                {
                    "name": "exporter_name",
                    "type": "string",
                    "description": "导出器名称",
                    "required": True,
                    "in": "query"
                }
            ],
            "response": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "exporter": {"type": "string"},
                    "timestamp": {"type": "string"}
                }
            }
        },
        "status": {
            "name": "status",
            "description": "获取技能状态",
            "method": "GET",
            "path": "/api/v1/status",
            "response": {
                "type": "object",
                "properties": {
                    "skill": {"type": "object"},
                    "harvester": {"type": "object"},
                    "config": {"type": "object"},
                    "timestamp": {"type": "string"}
                }
            }
        }
    })
    
    # UI界面定义
    ui: Dict[str, Any] = field(default_factory=lambda: {
        "dashboard": {
            "title": "数据采集器仪表板",
            "description": "监控和管理数据采集任务",
            "widgets": [
                {
                    "type": "stats",
                    "title": "采集统计",
                    "metrics": ["total_collections", "successful_collections", "total_exports"]
                },
                {
                    "type": "chart",
                    "title": "最近采集活动",
                    "chart_type": "line",
                    "data_source": "/api/v1/activity"
                },
                {
                    "type": "list",
                    "title": "数据源状态",
                    "data_source": "/api/v1/sources"
                }
            ]
        },
        "config_editor": {
            "title": "配置编辑器",
            "schema": "$.config_schema",
            "ui_schema": {
                "log_level": {
                    "ui:widget": "select",
                    "ui:help": "选择日志详细程度"
                },
                "sources": {
                    "ui:options": {
                        "orderable": True
                    }
                }
            }
        }
    })
    
    # 文档链接
    documentation: Dict[str, str] = field(default_factory=lambda: {
        "getting_started": "https://github.com/openclaw-wealth-guide/data-harvester/blob/main/docs/getting-started.md",
        "api_reference": "https://github.com/openclaw-wealth-guide/data-harvester/blob/main/docs/api-reference.md",
        "examples": "https://github.com/openclaw-wealth-guide/data-harvester/blob/main/examples/",
        "faq": "https://github.com/openclaw-wealth-guide/data-harvester/blob/main/docs/faq.md"
    })
    
    # 商业信息
    pricing: Dict[str, Any] = field(default_factory=lambda: {
        "tiers": [
            {
                "name": "basic",
                "price": 299,
                "currency": "CNY",
                "description": "基础版，适合个人用户",
                "features": [
                    "支持2个数据源",
                    "基础数据处理",
                    "CSV/JSON导出",
                    "社区支持"
                ],
                "period": "一次性"
            },
            {
                "name": "professional",
                "price": 899,
                "currency": "CNY",
                "description": "专业版，适合开发者和小型团队",
                "features": [
                    "支持10个数据源",
                    "高级数据处理管道",
                    "CSV/JSON/Excel导出",
                    "定时调度",
                    "优先级支持"
                ],
                "period": "一次性"
            },
            {
                "name": "enterprise",
                "price": 2999,
                "currency": "CNY",
                "description": "企业版，适合商业用途",
                "features": [
                    "无限数据源",
                    "完整功能套件",
                    "定制开发支持",
                    "优先技术支持",
                    "培训和部署协助"
                ],
                "period": "年度"
            }
        ],
        "revenue_sharing": {
            "platform": 0.30,  # OpenClaw平台分成30%
            "author": 0.70     # 开发者获得70%
        }
    })
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            # 基本信息
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "homepage": self.homepage,
            "license": self.license,
            "created_at": datetime.now().isoformat(),
            
            # 分类和标签
            "category": self.category,
            "subcategory": self.subcategory,
            "tags": self.tags,
            
            # 技术信息
            "min_claw_version": self.min_claw_version,
            "python_version": self.python_version,
            "dependencies": self.dependencies,
            
            # 运行时信息
            "entrypoint": self.entrypoint,
            "config_schema": self.config_schema,
            
            # 权限和范围
            "required_scopes": self.required_scopes,
            
            # 操作定义
            "operations": self.operations,
            
            # UI界面
            "ui": self.ui,
            
            # 文档
            "documentation": self.documentation,
            
            # 商业信息
            "pricing": self.pricing
        }
    
    def to_json(self, indent: int = 2) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)
    
    def to_yaml(self) -> str:
        """转换为YAML字符串"""
        return yaml.dump(self.to_dict(), allow_unicode=True, default_flow_style=False)
    
    def save(self, output_path: Path, format: str = "json") -> None:
        """
        保存技能清单到文件
        
        Args:
            output_path: 输出文件路径
            format: 文件格式（json或yaml）
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if format.lower() == "json":
                content = self.to_json()
                file_path = output_path.with_suffix('.json')
            elif format.lower() == "yaml":
                content = self.to_yaml()
                file_path = output_path.with_suffix('.yaml')
            else:
                raise ValueError(f"不支持的格式: {format}")
            
            file_path.write_text(content, encoding="utf-8")
            
        except Exception as e:
            raise RuntimeError(f"保存技能清单失败: {e}") from e
    
    @classmethod
    def load(cls, file_path: Path) -> "SkillManifest":
        """
        从文件加载技能清单
        
        Args:
            file_path: 文件路径
            
        Returns:
            SkillManifest实例
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        try:
            content = file_path.read_text(encoding="utf-8")
            
            if file_path.suffix.lower() in ['.json', '.jsonld']:
                data = json.loads(content)
            elif file_path.suffix.lower() in ['.yaml', '.yml']:
                data = yaml.safe_load(content)
            else:
                raise ValueError(f"不支持的格式: {file_path.suffix}")
            
            # 创建SkillManifest实例
            manifest = cls()
            
            # 更新字段（这里简化处理，实际应该逐个字段处理）
            for key, value in data.items():
                if hasattr(manifest, key):
                    setattr(manifest, key, value)
            
            return manifest
            
        except Exception as e:
            raise RuntimeError(f"加载技能清单失败: {e}") from e
    
    def validate(self) -> List[str]:
        """
        验证技能清单的有效性
        
        Returns:
            错误消息列表（如果为空则表示验证通过）
        """
        errors = []
        
        # 验证必需字段
        required_fields = ["name", "slug", "description", "version", "author"]
        for field in required_fields:
            if not getattr(self, field):
                errors.append(f"必需字段缺失或为空: {field}")
        
        # 验证版本格式
        if not self.version or len(self.version.split('.')) != 3:
            errors.append(f"版本格式无效，应为X.Y.Z格式: {self.version}")
        
        # 验证分类
        valid_categories = [
            "data-collection", "automation", "analysis", 
            "productivity", "integration", "monitoring"
        ]
        if self.category not in valid_categories:
            errors.append(f"分类无效，应为: {', '.join(valid_categories)}")
        
        # 验证Python版本
        if not self.python_version or not self.python_version.startswith(">="):
            errors.append(f"Python版本格式无效，应为>=X.Y格式: {self.python_version}")
        
        # 验证依赖
        for dep in self.dependencies:
            if not isinstance(dep, str) or len(dep.strip()) == 0:
                errors.append(f"依赖项格式无效: {dep}")
        
        return errors