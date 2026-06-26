#!/usr/bin/env python3
"""
OpenClaw集成示例
展示如何将智能数据采集器集成到OpenClaw平台
"""

import os
import sys
from pathlib import Path

# 添加src目录到Python路径
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from data_harvester.openclaw_integration import (
    OpenClawSkillWrapper,
    SkillManifest
)
from data_harvester.config import Config, SourceConfig, DataSourceType


def demonstrate_skill_wrapper():
    """演示技能包装器"""
    print("=" * 60)
    print("OpenClaw技能包装器演示")
    print("=" * 60)
    
    print("\n1. 创建OpenClaw技能包装器实例...")
    
    # 创建示例配置
    config = Config(name="OpenClaw集成演示")
    
    # 添加一个示例数据源
    config.sources["demo_web"] = SourceConfig(
        name="演示网站",
        type=DataSourceType.WEB,
        url="https://httpbin.org/html",
        enabled=True
    )
    
    # 保存配置文件
    config_path = Path("config") / "openclaw_demo_config.yaml"
    config_path.parent.mkdir(exist_ok=True)
    config.save(config_path)
    
    print(f"配置文件已创建: {config_path}")
    
    # 创建技能包装器
    skill = OpenClawSkillWrapper(str(config_path))
    
    print("\n2. 初始化技能...")
    skill.initialize()
    
    print("\n3. 获取技能状态...")
    status = skill.get_status()
    print(f"   技能初始化状态: {status['skill']['initialized']}")
    print(f"   采集器就绪状态: {status['skill']['harvester_ready']}")
    print(f"   技能名称: {status['config']['name']}")
    print(f"   技能版本: {status['config']['version']}")
    
    print("\n4. 生成技能清单...")
    manifest = skill.get_skill_manifest()
    print(f"   技能名称: {manifest['name']}")
    print(f"   技能描述: {manifest['description']}")
    print(f"   技能版本: {manifest['version']}")
    print(f"   技能类别: {manifest['category']}")
    print(f"   技能标签: {', '.join(manifest['tags'])}")
    print(f"   支持的操作: {', '.join(manifest['operations'].keys())}")
    
    print("\n5. 保存技能清单...")
    skill.save_skill_manifest(Path("output") / "skill_manifest")
    
    json_path = Path("output/skill_manifest.json")
    yaml_path = Path("output/skill_manifest.yaml")
    
    if json_path.exists():
        print(f"   JSON清单已保存: {json_path}")
    if yaml_path.exists():
        print(f"   YAML清单已保存: {yaml_path}")
    
    print("\n6. 演示数据采集...")
    try:
        result = skill.collect_data("demo_web")
        if result["success"]:
            print(f"   数据采集成功!")
            print(f"   数据源: {result['source']}")
            print(f"   数据大小: {len(str(result['data'])) if result['data'] else 0} 字符")
            print(f"   时间戳: {result['timestamp']}")
        else:
            print(f"   数据采集失败!")
            print(f"   错误: {result['errors']}")
    except Exception as e:
        print(f"   数据采集演示失败（无网络连接或测试网站不可访问）: {e}")
    
    print("\n7. 创建技能安装包...")
    try:
        package_dir = skill.create_skill_package(Path("output") / "skill_package")
        print(f"   技能包已创建: {package_dir}")
        print(f"   包内文件:")
        for file in package_dir.rglob("*"):
            if file.is_file():
                print(f"     - {file.relative_to(package_dir)}")
    except Exception as e:
        print(f"   创建技能包失败: {e}")
    
    print("\n8. 关闭技能...")
    skill.shutdown()
    
    print("\n演示完成!")
    
    # 清理临时文件
    if config_path.exists():
        config_path.unlink()


def demonstrate_skill_manifest():
    """演示技能清单"""
    print("\n" + "=" * 60)
    print("技能清单生成演示")
    print("=" * 60)
    
    print("\n1. 创建技能清单...")
    manifest = SkillManifest(
        name="高级数据采集器",
        slug="advanced-data-harvester",
        description="专业级多源数据采集和处理工具",
        version="2.0.0",
        author="OpenClaw专业开发者",
        homepage="https://github.com/openclaw-pro/advanced-data-harvester",
        category="data-collection",
        subcategory="enterprise",
        tags=["data", "enterprise", "automation", "analytics", "big-data"]
    )
    
    print(f"   技能名称: {manifest.name}")
    print(f"   技能ID: {manifest.slug}")
    print(f"   技能版本: {manifest.version}")
    print(f"   技能类别: {manifest.category}")
    print(f"   技能子类别: {manifest.subcategory}")
    print(f"   技能标签: {', '.join(manifest.tags)}")
    
    print("\n2. 验证技能清单...")
    errors = manifest.validate()
    if errors:
        print(f"   验证发现 {len(errors)} 个错误:")
        for error in errors:
            print(f"     - {error}")
    else:
        print("   技能清单验证通过!")
    
    print("\n3. 生成JSON清单...")
    json_output = manifest.to_json()
    print(f"   JSON大小: {len(json_output)} 字符")
    print(f"   JSON片段:")
    print(json_output[:200] + "..." if len(json_output) > 200 else json_output)
    
    print("\n4. 保存技能清单...")
    output_dir = Path("output") / "manifest_demo"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    manifest.save(output_dir / "advanced_skill", format="json")
    manifest.save(output_dir / "advanced_skill", format="yaml")
    
    print(f"   清单已保存到: {output_dir}")
    print(f"     - advanced_skill.json")
    print(f"     - advanced_skill.yaml")
    
    print("\n5. 商业信息...")
    print(f"   价格层级:")
    for tier in manifest.pricing["tiers"]:
        print(f"     - {tier['name']}: ￥{tier['price']} ({tier['description']})")
    
    revenue_sharing = manifest.pricing["revenue_sharing"]
    print(f"   收入分成:")
    print(f"     - 平台分成: {revenue_sharing['platform'] * 100:.0f}%")
    print(f"     - 开发者分成: {revenue_sharing['author'] * 100:.0f}%")


def demonstrate_api_client():
    """演示API客户端（模拟）"""
    print("\n" + "=" * 60)
    print("OpenClaw API客户端演示（模拟）")
    print("=" * 60)
    
    print("\n注意：以下演示使用模拟API响应，实际使用时需要真实的OpenClaw API URL和密钥")
    
    print("\n1. 创建API客户端...")
    print("   客户端配置:")
    print("     - Base URL: https://api.openclaw.ai")
    print("     - API Key: ************")
    print("     - Timeout: 30秒")
    
    print("\n2. 模拟技能注册流程...")
    print("   a. 创建技能清单")
    print("   b. 调用 register_skill() API")
    print("   c. 接收技能ID和注册确认")
    
    print("\n3. 模拟技能安装流程...")
    print("   a. 用户选择技能")
    print("   b. 系统调用 install_skill() API")
    print("   c. 技能安装到用户的工作空间")
    
    print("\n4. 模拟技能使用流程...")
    print("   a. 用户配置数据源")
    print("   b. 用户启动采集任务")
    print("   c. 系统调用 execute_skill_operation() API")
    print("   d. 返回采集结果")
    
    print("\n5. 模拟技能监控...")
    print("   a. 获取技能指标数据")
    print("   b. 监控技能运行状态")
    print("   c. 收集使用统计")
    
    print("\n提示：在实际环境中，这些API调用将由OpenClaw平台自动处理")


def create_openclaw_skill_guide():
    """创建OpenClaw技能指南"""
    print("\n" + "=" * 60)
    print("OpenClaw技能集成指南")
    print("=" * 60)
    
    guide_path = Path("output") / "openclaw_skill_guide.md"
    guide_path.parent.mkdir(parents=True, exist_ok=True)
    
    guide_content = """# OpenClaw技能集成指南

## 概述
本文档指导您如何将智能数据采集器集成到OpenClaw平台作为可安装技能。

## 技能要求

### 1. 技能清单 (Skill Manifest)
技能清单是描述技能元数据的JSON/YAML文件，包含以下必需字段：

```json
{
  "name": "技能名称",
  "slug": "技能标识符",
  "description": "技能描述",
  "version": "1.0.0",
  "author": "开发者名称",
  "category": "data-collection",
  "entrypoint": "模块路径:类名"
}
```

### 2. 技能包装器 (Skill Wrapper)
技能包装器是连接技能和OpenClaw平台的适配器类：

```python
class OpenClawSkillWrapper:
    def initialize(self) -> None:
        # 初始化技能
        
    def shutdown(self) -> None:
        # 关闭技能
        
    def collect_data(self, source_name: str) -> Dict:
        # 收集数据
        
    def get_status(self) -> Dict:
        # 获取技能状态
```

### 3. 配置文件 (Configuration)
技能应该支持配置文件管理：

- 支持YAML/JSON格式
- 包含数据源配置
- 包含处理管道配置
- 包含导出器配置

## 集成步骤

### 步骤1: 创建技能清单
```python
from data_harvester.openclaw_integration import SkillManifest

manifest = SkillManifest(
    name="智能数据采集器",
    slug="data-harvester",
    description="自动化数据采集工具",
    version="1.0.0",
    category="data-collection"
)

manifest.save("skill_manifest")
```

### 步骤2: 创建技能包装器
```python
from data_harvester.openclaw_integration import OpenClawSkillWrapper

skill = OpenClawSkillWrapper("config.yaml")
skill.initialize()
```

### 步骤3: 测试技能功能
```python
# 测试数据采集
result = skill.collect_data("example_source")

# 测试技能状态
status = skill.get_status()

# 测试技能关闭
skill.shutdown()
```

### 步骤4: 打包技能
```python
# 创建技能安装包
package_dir = skill.create_skill_package("output/skill_package")
```

### 步骤5: 发布到OpenClaw
1. 登录OpenClaw开发者控制台
2. 上传技能包
3. 填写技能信息
4. 设置价格和许可
5. 发布技能

## API集成

### OpenClaw API端点

```
POST   /api/v1/skills/register      # 注册技能
PUT    /api/v1/skills/{id}          # 更新技能
GET    /api/v1/skills/{id}          # 获取技能信息
POST   /api/v1/skills/{id}/install  # 安装技能
POST   /api/v1/skills/{id}/execute/{operation}  # 执行操作
```

### 错误处理
技能应该返回标准化的错误响应：

```json
{
  "success": false,
  "error": "错误描述",
  "code": "ERROR_CODE"
}
```

## 最佳实践

1. **清晰的文档**: 提供完整的API文档和使用示例
2. **完善的错误处理**: 处理所有可能的错误情况
3. **配置验证**: 验证用户输入的配置
4. **资源管理**: 合理管理内存和网络连接
5. **日志记录**: 记录关键操作和错误
6. **性能优化**: 确保技能运行效率

## 调试技巧

1. 使用日志级别控制详细程度
2. 测试所有数据源类型
3. 验证导出文件格式
4. 测试并发处理
5. 验证错误恢复机制

## 常见问题

### Q: 技能注册失败怎么办？
A: 检查技能清单格式，确保所有必需字段都已填写。

### Q: 技能安装后无法执行操作？
A: 检查技能包装器的initialize()方法是否正确初始化。

### Q: 如何调试技能运行问题？
A: 启用DEBUG日志级别，查看详细日志信息。

## 支持

如需帮助，请联系：
- 邮箱: support@openclaw.ai
- 文档: https://docs.openclaw.ai
- 社区: https://discord.gg/openclaw
"""
    
    guide_path.write_text(guide_content, encoding="utf-8")
    print(f"\n技能集成指南已保存到: {guide_path}")


def main():
    """主函数"""
    print("OpenClaw技能集成演示程序")
    print("开始执行演示...\n")
    
    # 确保输出目录存在
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    try:
        # 演示技能包装器
        demonstrate_skill_wrapper()
        
        # 演示技能清单
        demonstrate_skill_manifest()
        
        # 演示API客户端
        demonstrate_api_client()
        
        # 创建集成指南
        create_openclaw_skill_guide()
        
    except Exception as e:
        print(f"\n演示执行出错: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n演示程序结束!")
    print("输出文件位于 'output/' 目录中")


if __name__ == "__main__":
    main()