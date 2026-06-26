"""
OpenClaw技能包装器
将智能数据采集器包装为OpenClaw技能
"""

import logging
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from datetime import datetime

from ..core import DataHarvester
from ..config import Config
from ..exceptions import IntegrationError

logger = logging.getLogger(__name__)


@dataclass
class SkillConfig:
    """技能配置"""
    name: str = "智能数据采集器"
    description: str = "自动化数据采集、处理和导出工具"
    version: str = "1.0.0"
    author: str = "OpenClaw Wealth Guide"
    category: str = "data-collection"
    icon: str = "📊"
    tags: List[str] = field(default_factory=lambda: ["data", "collection", "analysis", "automation"])
    min_claw_version: str = "0.8.0"
    required_scopes: List[str] = field(default_factory=lambda: [
        "files:read",
        "files:write",
        "web:fetch",
        "web:search",
        "browser:automate"
    ])
    dependencies: List[str] = field(default_factory=lambda: [
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "pandas>=2.0.0",
        "APScheduler>=3.10.0"
    ])
    pricing: Dict[str, Any] = field(default_factory=lambda: {
        "basic": 299,      # 基础版价格（元）
        "professional": 899,  # 专业版价格
        "enterprise": 2999    # 企业版价格
    })
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "category": self.category,
            "icon": self.icon,
            "tags": self.tags,
            "min_claw_version": self.min_claw_version,
            "required_scopes": self.required_scopes,
            "dependencies": self.dependencies,
            "pricing": self.pricing
        }


class OpenClawSkillWrapper:
    """OpenClaw技能包装器"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化技能包装器
        
        Args:
            config_path: 数据采集器配置文件路径（可选）
        """
        self.skill_config = SkillConfig()
        self.harvester: Optional[DataHarvester] = None
        self.initialized = False
        
        # 初始化数据采集器
        if config_path:
            try:
                self.harvester = DataHarvester(config_path=config_path)
                logger.info(f"从配置文件加载数据采集器: {config_path}")
            except Exception as e:
                logger.error(f"加载数据采集器配置失败: {e}")
                raise IntegrationError(f"加载数据采集器配置失败: {e}") from e
        else:
            self.harvester = DataHarvester()
            logger.info("使用默认配置创建数据采集器")
        
        # 技能状态
        self.status = {
            "initialized": False,
            "harvester_ready": False,
            "tasks_running": 0,
            "last_collection": None,
            "total_collections": 0,
            "total_exports": 0
        }
        
        logger.debug("OpenClaw技能包装器初始化完成")
    
    def initialize(self) -> None:
        """
        初始化技能
        
        Raises:
            IntegrationError: 初始化失败
        """
        if self.initialized:
            logger.warning("技能已经初始化")
            return
        
        try:
            if self.harvester:
                self.harvester.initialize()
                self.status["harvester_ready"] = True
                logger.info("数据采集器初始化成功")
            
            self.initialized = True
            self.status["initialized"] = True
            self.status["start_time"] = datetime.now()
            
            logger.info("OpenClaw技能初始化完成")
            
        except Exception as e:
            logger.error(f"技能初始化失败: {e}")
            raise IntegrationError(f"技能初始化失败: {e}") from e
    
    def shutdown(self) -> None:
        """关闭技能"""
        if not self.initialized:
            logger.warning("技能未初始化")
            return
        
        try:
            if self.harvester:
                self.harvester.shutdown()
                self.status["harvester_ready"] = False
                logger.info("数据采集器已关闭")
            
            self.initialized = False
            self.status["initialized"] = False
            self.status["shutdown_time"] = datetime.now()
            
            logger.info("OpenClaw技能已关闭")
            
        except Exception as e:
            logger.error(f"技能关闭失败: {e}")
            raise IntegrationError(f"技能关闭失败: {e}") from e
    
    def collect_data(self, source_name: str, **kwargs) -> Dict[str, Any]:
        """
        收集数据（OpenClaw API接口）
        
        Args:
            source_name: 数据源名称
            **kwargs: 额外参数
            
        Returns:
            采集结果
        """
        if not self.initialized:
            self.initialize()
        
        if not self.harvester:
            raise IntegrationError("数据采集器未初始化")
        
        try:
            result = self.harvester.collect(source_name, **kwargs)
            
            # 更新状态
            self.status["last_collection"] = datetime.now()
            self.status["total_collections"] += 1
            
            # 转换为OpenClaw格式
            return {
                "success": result.success,
                "data": result.data if result.success else None,
                "source": result.source,
                "metadata": result.metadata,
                "errors": result.errors,
                "timestamp": result.timestamp.isoformat() if result.timestamp else None,
                "message": "数据采集成功" if result.success else "数据采集失败"
            }
            
        except Exception as e:
            logger.error(f"数据采集失败 {source_name}: {e}")
            raise IntegrationError(f"数据采集失败: {e}") from e
    
    def collect_all(self) -> Dict[str, Any]:
        """
        收集所有数据源的数据
        
        Returns:
            所有数据源的采集结果
        """
        if not self.initialized:
            self.initialize()
        
        if not self.harvester:
            raise IntegrationError("数据采集器未初始化")
        
        try:
            results = self.harvester.collect_all()
            
            # 更新状态
            self.status["last_collection"] = datetime.now()
            self.status["total_collections"] += len(results)
            
            # 转换为OpenClaw格式
            openclaw_results = {}
            for source_name, result in results.items():
                openclaw_results[source_name] = {
                    "success": result.success,
                    "data": result.data if result.success else None,
                    "metadata": result.metadata,
                    "errors": result.errors,
                    "timestamp": result.timestamp.isoformat() if result.timestamp else None
                }
            
            return {
                "success": True,
                "results": openclaw_results,
                "total_sources": len(results),
                "successful_sources": sum(1 for r in results.values() if r.success),
                "failed_sources": sum(1 for r in results.values() if not r.success),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"批量数据采集失败: {e}")
            raise IntegrationError(f"批量数据采集失败: {e}") from e
    
    def export_data(self, data: Any, exporter_name: str, **kwargs) -> Dict[str, Any]:
        """
        导出数据
        
        Args:
            data: 要导出的数据
            exporter_name: 导出器名称
            **kwargs: 额外参数
            
        Returns:
            导出结果
        """
        if not self.initialized:
            self.initialize()
        
        if not self.harvester:
            raise IntegrationError("数据采集器未初始化")
        
        try:
            success = self.harvester.export(data, exporter_name, **kwargs)
            
            # 更新状态
            if success:
                self.status["total_exports"] += 1
            
            return {
                "success": success,
                "exporter": exporter_name,
                "timestamp": datetime.now().isoformat(),
                "message": "数据导出成功" if success else "数据导出失败"
            }
            
        except Exception as e:
            logger.error(f"数据导出失败 {exporter_name}: {e}")
            raise IntegrationError(f"数据导出失败: {e}") from e
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取技能状态
        
        Returns:
            技能状态信息
        """
        harvester_status = {}
        if self.harvester:
            harvester_status = self.harvester.get_status()
        
        return {
            "skill": self.status,
            "harvester": harvester_status,
            "config": self.skill_config.to_dict(),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_skill_manifest(self) -> Dict[str, Any]:
        """
        获取技能清单（用于OpenClaw技能注册）
        
        Returns:
            技能清单数据
        """
        manifest = self.skill_config.to_dict()
        
        # 添加操作定义
        manifest["operations"] = {
            "collect": {
                "description": "从指定数据源收集数据",
                "parameters": {
                    "source_name": {
                        "type": "string",
                        "description": "数据源名称",
                        "required": True
                    }
                }
            },
            "collect_all": {
                "description": "从所有数据源收集数据"
            },
            "export": {
                "description": "导出数据到指定格式",
                "parameters": {
                    "data": {
                        "type": "any",
                        "description": "要导出的数据",
                        "required": True
                    },
                    "exporter_name": {
                        "type": "string",
                        "description": "导出器名称",
                        "required": True
                    }
                }
            },
            "status": {
                "description": "获取技能状态"
            }
        }
        
        # 添加示例配置
        manifest["example_config"] = {
            "sources": {
                "example_web": {
                    "name": "示例网站",
                    "type": "web",
                    "url": "https://example.com",
                    "enabled": True
                }
            },
            "processing": {
                "enabled": True,
                "strategy": ["clean", "transform"]
            },
            "exports": [
                {
                    "name": "json_output",
                    "format": "json",
                    "output_path": "data/output.json"
                }
            ]
        }
        
        return manifest
    
    def save_skill_manifest(self, output_path: Union[str, Path]) -> None:
        """
        保存技能清单到文件
        
        Args:
            output_path: 输出文件路径
        """
        manifest = self.get_skill_manifest()
        
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 保存为JSON
            with open(output_path.with_suffix('.json'), 'w', encoding='utf-8') as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)
            
            # 保存为YAML
            with open(output_path.with_suffix('.yaml'), 'w', encoding='utf-8') as f:
                yaml.dump(manifest, f, allow_unicode=True, default_flow_style=False)
            
            logger.info(f"技能清单已保存: {output_path}")
            
        except Exception as e:
            logger.error(f"保存技能清单失败: {e}")
            raise IntegrationError(f"保存技能清单失败: {e}") from e
    
    def register_to_openclaw(self, openclaw_api_url: str, api_key: str) -> Dict[str, Any]:
        """
        注册技能到OpenClaw平台
        
        Args:
            openclaw_api_url: OpenClaw API URL
            api_key: API密钥
            
        Returns:
            注册结果
        """
        # TODO: 实现OpenClaw API调用
        manifest = self.get_skill_manifest()
        
        logger.info(f"准备注册技能到OpenClaw: {manifest['name']}")
        logger.debug(f"API URL: {openclaw_api_url}")
        
        # 模拟注册成功
        return {
            "success": True,
            "skill_id": f"data-harvester-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "manifest": manifest,
            "message": "技能注册成功（模拟）",
            "timestamp": datetime.now().isoformat()
        }
    
    def create_skill_package(self, output_dir: Union[str, Path]) -> Path:
        """
        创建技能安装包
        
        Args:
            output_dir: 输出目录
            
        Returns:
            技能包路径
        """
        try:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 创建技能包目录结构
            skill_dir = output_dir / f"data_harvester_skill_v{self.skill_config.version}"
            skill_dir.mkdir(parents=True, exist_ok=True)
            
            # 创建SKILL.md文件
            skill_md_content = f"""# {self.skill_config.name}

{self.skill_config.description}

## 特性
- 多源数据采集（Web、API、文件、数据库）
- 智能数据处理管道（清洗、转换、验证）
- 多种导出格式（CSV、JSON、Excel）
- 自动化调度和监控
- 完整的错误处理和恢复机制

## 安装

```bash
pip install -r requirements.txt
```

## 配置

参考 `config/examples/` 目录中的示例配置文件。

## 使用

```python
from data_harvester.openclaw_integration import OpenClawSkillWrapper

# 创建技能实例
skill = OpenClawSkillWrapper()

# 初始化技能
skill.initialize()

# 收集数据
result = skill.collect_data("your_source_name")

# 获取技能状态
status = skill.get_status()

# 关闭技能
skill.shutdown()
```

## 许可证

MIT License

## 支持

如有问题，请提交Issue或联系作者。
"""
            
            (skill_dir / "SKILL.md").write_text(skill_md_content, encoding="utf-8")
            
            # 保存技能清单
            self.save_skill_manifest(skill_dir / "skill_manifest")
            
            logger.info(f"技能包已创建: {skill_dir}")
            return skill_dir
            
        except Exception as e:
            logger.error(f"创建技能包失败: {e}")
            raise IntegrationError(f"创建技能包失败: {e}") from e
    
    def __enter__(self):
        """上下文管理器入口"""
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.shutdown()