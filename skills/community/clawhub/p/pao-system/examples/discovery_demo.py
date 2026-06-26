#!/usr/bin/env python3
"""
设备发现演示
演示 PAO 系统的设备发现功能
"""

import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.device import DeviceRegistry, DeviceInfo, DeviceType
from src.core.discovery import DeviceDiscoveryService
from src.core.config import PAOConfig, get_config_manager


async def simple_discovery_demo():
    """简单设备发现演示"""
    print("=== PAO 设备发现演示 ===")
    print()
    
    # 创建配置
    config = PAOConfig(device_name="Demo-Device")
    
    # 创建设备注册表
    device_registry = DeviceRegistry()
    
    # 定义回调函数
    def on_device_discovered(device: DeviceInfo):
        print(f"🎯 发现新设备: {device.name}")
        print(f"   类型: {device.device_type.value}")
        print(f"   地址: {device.ip_address}:{device.port}")
        print(f"   能力: {[cap.value for cap in device.capabilities]}")
        print()
    
    def on_device_lost(device_id: str):
        print(f"⚠️  设备丢失: {device_id}")
        print()
    
    # 创建设备发现服务
    discovery_service = DeviceDiscoveryService(
        config=config,
        device_registry=device_registry,
        on_device_discovered=on_device_discovered,
        on_device_lost=on_device_lost
    )
    
    print(f"本地设备: {discovery_service.local_device.name}")
    print(f"IP地址: {discovery_service.local_device.ip_address}")
    print(f"设备ID: {discovery_service.local_device.device_id}")
    print()
    
    # 启动发现服务
    print("启动设备发现服务...")
    await discovery_service.start()
    
    try:
        # 等待一段时间发现设备
        print("等待发现设备 (10秒)...")
        await asyncio.sleep(10)
        
        # 显示发现的设备
        devices = device_registry.list_devices()
        print(f"\n📊 总共发现 {len(devices)} 个设备:")
        
        for i, device in enumerate(devices, 1):
            print(f"{i}. {device.name} ({device.device_type.value})")
            print(f"   ID: {device.device_id}")
            print(f"   主机名: {device.hostname}")
            print(f"   IP: {device.ip_address}:{device.port}")
            print(f"   能力: {[cap.value for cap in device.capabilities]}")
            print(f"   首次发现: {device.first_seen.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
        
        # 保持运行，等待更多设备
        print("持续监听网络设备...")
        print("按 Ctrl+C 停止")
        
        while True:
            # 显示在线设备数量
            online_devices = device_registry.list_online_devices()
            print(f"\r在线设备: {len(online_devices)}", end="", flush=True)
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n接收到停止信号")
    finally:
        # 停止发现服务
        print("停止设备发现服务...")
        await discovery_service.stop()
        print("演示结束")


async def advanced_discovery_demo():
    """高级设备发现演示"""
    print("=== PAO 高级设备发现演示 ===")
    print()
    
    # 使用配置管理器
    config_manager = get_config_manager()
    config = config_manager.config
    
    # 更新配置
    config.device_name = "Advanced-Demo"
    config.network.discovery_port = 8888
    config_manager.save_config(config)
    
    # 创建设备注册表
    device_registry = DeviceRegistry()
    
    # 手动添加一些模拟设备
    mock_device1 = DeviceInfo(
        name="Mock-Laptop",
        device_type=DeviceType.LAPTOP,
        ip_address="192.168.1.100",
        port=8765,
        capabilities=["compute", "storage", "display", "input"]
    )
    
    mock_device2 = DeviceInfo(
        name="Mock-Phone",
        device_type=DeviceType.PHONE,
        ip_address="192.168.1.101",
        port=8765,
        capabilities=["compute", "storage", "sensors"]
    )
    
    device_registry.register_device(mock_device1)
    device_registry.register_device(mock_device2)
    
    print("已注册模拟设备:")
    for device in device_registry.list_devices():
        print(f"  - {device.name}: {device.device_type.value}")
    print()
    
    # 创建设备发现服务
    discovery_service = DeviceDiscoveryService(
        config=config,
        device_registry=device_registry
    )
    
    # 启动服务
    print("启动高级发现服务...")
    await discovery_service.start()
    
    try:
        # 模拟网络发现
        print("模拟网络发现过程...")
        
        for i in range(5):
            print(f"扫描周期 {i+1}/5...")
            
            # 模拟发现新设备
            if i == 2:
                new_device = DeviceInfo(
                    name=f"New-Device-{i}",
                    device_type=DeviceType.IOT,
                    ip_address=f"192.168.1.{150 + i}",
                    port=8765
                )
                device_registry.register_device(new_device)
                print(f"  发现新设备: {new_device.name}")
            
            # 显示设备统计
            online_count = len(device_registry.list_online_devices())
            total_count = len(device_registry.list_devices())
            print(f"  在线: {online_count}/{total_count} 设备")
            
            await asyncio.sleep(2)
        
        # 测试设备查找功能
        print("\n测试设备查找功能:")
        
        # 查找有计算能力的设备
        compute_devices = device_registry.find_device_by_capability("compute")
        print(f"计算设备: {len(compute_devices)} 个")
        
        # 查找有显示能力的设备
        display_devices = device_registry.find_device_by_capability("display")
        print(f"显示设备: {len(display_devices)} 个")
        
        # 清理离线设备
        print("\n清理离线设备...")
        device_registry.cleanup_offline_devices(timeout_seconds=1)
        
        final_count = len(device_registry.list_devices())
        print(f"清理后剩余设备: {final_count} 个")
        
    except KeyboardInterrupt:
        print("\n演示中断")
    finally:
        await discovery_service.stop()
        print("高级演示结束")


async def network_scan_demo():
    """网络扫描演示"""
    print("=== PAO 网络扫描演示 ===")
    print()
    
    from src.core.discovery import discovery_service
    
    config = PAOConfig(device_name="Scanner-Device")
    device_registry = DeviceRegistry()
    
    print("开始网络扫描...")
    
    # 使用上下文管理器
    async with discovery_service(config, device_registry) as service:
        print(f"扫描设备: {service.local_device.name}")
        print(f"扫描端口: {service.discovery_config.port}")
        print()
        
        # 执行主动扫描
        print("执行主动扫描 (5秒)...")
        devices = await service.discover_devices(timeout=5)
        
        if devices:
            print(f"\n扫描结果 ({len(devices)} 个设备):")
            for device in devices:
                status = "🟢 在线" if device.last_seen.timestamp() > 0 else "⚪ 离线"
                print(f"{status} {device.name} - {device.ip_address}")
        else:
            print("\n未发现任何设备")
        
        print("\n扫描完成")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PAO 设备发现演示")
    parser.add_argument("--demo", choices=["simple", "advanced", "scan", "all"],
                       default="simple", help="选择演示类型")
    
    args = parser.parse_args()
    
    try:
        if args.demo == "simple":
            asyncio.run(simple_discovery_demo())
        elif args.demo == "advanced":
            asyncio.run(advanced_discovery_demo())
        elif args.demo == "scan":
            asyncio.run(network_scan_demo())
        elif args.demo == "all":
            print("运行所有演示...")
            asyncio.run(simple_discovery_demo())
            print("\n" + "="*50 + "\n")
            asyncio.run(advanced_discovery_demo())
            print("\n" + "="*50 + "\n")
            asyncio.run(network_scan_demo())
    except KeyboardInterrupt:
        print("\n演示被用户中断")
    except Exception as e:
        print(f"演示出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()