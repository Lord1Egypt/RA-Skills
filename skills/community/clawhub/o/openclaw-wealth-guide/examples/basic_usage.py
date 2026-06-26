#!/usr/bin/env python3
"""
基本使用示例
展示智能数据采集器的基本功能
"""

import os
import sys
from pathlib import Path

# 添加src目录到Python路径
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from data_harvester import DataHarvester
from data_harvester.config import Config, SourceConfig, ProcessingConfig, ExportConfig
from data_harvester.config import DataSourceType, ExportFormat, ProcessingStrategy


def create_sample_config():
    """创建示例配置"""
    config = Config(
        name="示例数据采集器",
        version="1.0.0",
        description="智能数据采集器使用示例",
        log_level="INFO"
    )
    
    # 添加数据源配置
    config.sources["sample_web"] = SourceConfig(
        name="示例网站",
        type=DataSourceType.WEB,
        url="https://httpbin.org/html",  # 测试用的公共API
        extract_rules={
            "title": "h1",
            "content": "p"
        },
        headers={
            "User-Agent": "Mozilla/5.0 (智能数据采集器示例)"
        },
        timeout=30,
        retry_count=2
    )
    
    # 配置处理管道
    config.processing = ProcessingConfig(
        enabled=True,
        strategy=[
            ProcessingStrategy.CLEAN,
            ProcessingStrategy.TRANSFORM
        ],
        clean_options={
            "remove_null": True,
            "trim_whitespace": True
        },
        transform_options={
            "date_format": "%Y-%m-%d",
            "number_precision": 2
        }
    )
    
    # 配置导出器
    config.exports.append(
        ExportConfig(
            name="json_output",
            format=ExportFormat.JSON,
            output_path="output/sample_data.json",
            indent=2,
            ensure_ascii=False
        )
    )
    
    config.exports.append(
        ExportConfig(
            name="csv_output",
            format=ExportFormat.CSV,
            output_path="output/sample_data.csv",
            encoding="utf-8",
            write_header=True
        )
    )
    
    # 配置调度器（可选）
    config.scheduler.enabled = False  # 示例中禁用调度器
    
    return config


def basic_collection_demo():
    """基础采集演示"""
    print("=" * 60)
    print("智能数据采集器 - 基础使用示例")
    print("=" * 60)
    
    # 创建采集器实例
    print("\n1. 创建数据采集器实例...")
    harvester = DataHarvester()
    
    # 加载配置（使用代码创建的配置）
    print("2. 加载配置...")
    config = create_sample_config()
    harvester.config = config
    
    # 初始化采集器
    print("3. 初始化采集器组件...")
    harvester.initialize()
    
    # 显示采集器状态
    print("\n4. 采集器状态:")
    status = harvester.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # 执行数据采集
    print("\n5. 执行数据采集...")
    result = harvester.collect("sample_web")
    
    if result.success:
        print(f"   采集成功!")
        print(f"   数据源: {result.source}")
        print(f"   数据量: {result.metadata.get('data_size', 'N/A')}")
        print(f"   处理时间: {result.timestamp}")
        
        # 显示部分数据
        print(f"\n   示例数据预览:")
        if isinstance(result.data, dict):
            for key, value in list(result.data.items())[:3]:  # 只显示前3项
                print(f"     {key}: {str(value)[:50]}..." if len(str(value)) > 50 else f"     {key}: {value}")
        elif isinstance(result.data, list):
            for item in result.data[:2]:  # 只显示前2项
                print(f"     {str(item)[:80]}...")
        else:
            print(f"     {str(result.data)[:100]}...")
    else:
        print(f"   采集失败!")
        print(f"   错误: {result.errors}")
    
    # 导出数据
    print("\n6. 导出数据...")
    if result.success and result.data:
        # 导出为JSON
        json_success = harvester.export(result.data, "json_output")
        print(f"   JSON导出: {'成功' if json_success else '失败'}")
        
        # 导出为CSV
        csv_success = harvester.export(result.data, "csv_output")
        print(f"   CSV导出: {'成功' if csv_success else '失败'}")
    
    # 关闭采集器
    print("\n7. 关闭采集器...")
    harvester.shutdown()
    
    print("\n示例完成!")
    print("输出文件:")
    print("  - output/sample_data.json")
    print("  - output/sample_data.csv")


def file_based_config_demo():
    """基于文件的配置演示"""
    print("\n" + "=" * 60)
    print("基于文件的配置示例")
    print("=" * 60)
    
    # 创建配置目录
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    # 创建配置文件
    config_path = config_dir / "demo_config.yaml"
    
    config_content = """
# 智能数据采集器演示配置
name: "文件配置示例"
version: "1.0.0"
description: "使用YAML配置文件的示例"
log_level: "INFO"

sources:
  demo_api:
    name: "演示API接口"
    type: "api"
    url: "https://httpbin.org/json"
    enabled: true
    headers:
      User-Agent: "智能数据采集器演示/1.0"
    timeout: 20

processing:
  enabled: true
  strategy:
    - "clean"
    - "transform"
  
  clean_options:
    remove_null: true
    trim_whitespace: true
  
  transform_options:
    date_format: "%Y-%m-%d %H:%M:%S"
    encoding: "utf-8"

exports:
  - name: "demo_json"
    format: "json"
    output_path: "output/demo_data.json"
    indent: 2
    ensure_ascii: false

scheduler:
  enabled: false
  timezone: "Asia/Shanghai"
"""
    
    config_path.write_text(config_content, encoding="utf-8")
    print(f"\n配置文件已创建: {config_path}")
    
    # 从文件加载配置
    print("\n从文件加载配置...")
    try:
        config = Config.load(str(config_path))
        print(f"配置加载成功: {config.name}")
        print(f"数据源数量: {len(config.sources)}")
        print(f"导出器数量: {len(config.exports)}")
    except Exception as e:
        print(f"配置加载失败: {e}")
    
    # 清理
    if config_path.exists():
        config_path.unlink()


if __name__ == "__main__":
    # 确保输出目录存在
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    print("智能数据采集器示例程序")
    print("开始执行示例...\n")
    
    try:
        # 运行基础采集演示
        basic_collection_demo()
        
        # 运行文件配置演示
        file_based_config_demo()
        
    except Exception as e:
        print(f"\n示例执行出错: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n示例程序结束!")