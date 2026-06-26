"""
记忆同步演示
展示 PAO 系统的记忆同步功能
"""

import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.memory import MemorySystem, MemoryItem, MemoryType, MemoryPriority, MemoryQuery
from src.core.sync import SyncEngine, SyncStrategy
from src.core.device import DeviceInfo, DeviceType, DeviceCapability


async def create_sample_memories(memory_system: MemorySystem, device_id: str) -> None:
    """创建示例记忆"""
    
    # 对话记忆
    conversation_memory = MemoryItem(
        type=MemoryType.CONVERSATION,
        content={
            "user": "你好，今天天气怎么样？",
            "assistant": "今天天气晴朗，温度适宜。",
            "context": "天气查询对话"
        },
        priority=MemoryPriority.MEDIUM,
        device_id=device_id
    )
    conversation_memory.metadata.tags = ["天气", "对话", "日常"]
    conversation_memory.metadata.source = "user:alice"
    
    await memory_system.save(conversation_memory)
    print(f"创建对话记忆: {conversation_memory.id}")
    
    # 知识记忆
    knowledge_memory = MemoryItem(
        type=MemoryType.KNOWLEDGE,
        content={
            "topic": "Python 异步编程",
            "content": "asyncio 是 Python 的异步编程库，使用 async/await 语法。",
            "source": "官方文档"
        },
        priority=MemoryPriority.HIGH,
        device_id=device_id
    )
    knowledge_memory.metadata.tags = ["Python", "编程", "异步"]
    knowledge_memory.metadata.source = "system:learning"
    
    await memory_system.save(knowledge_memory)
    print(f"创建知识记忆: {knowledge_memory.id}")
    
    # 任务记忆
    task_memory = MemoryItem(
        type=MemoryType.TASK,
        content={
            "title": "完成 PAO 系统第二阶段",
            "description": "实现本地记忆系统和基本同步功能",
            "status": "in_progress",
            "deadline": "2026-04-16"
        },
        priority=MemoryPriority.CRITICAL,
        device_id=device_id
    )
    task_memory.metadata.tags = ["任务", "PAO", "开发"]
    task_memory.metadata.source = "user:developer"
    
    await memory_system.save(task_memory)
    print(f"创建任务记忆: {task_memory.id}")
    
    print(f"总共创建了 3 个示例记忆")


async def demonstrate_memory_operations(memory_system: MemorySystem) -> None:
    """演示记忆操作"""
    
    print("\n=== 记忆操作演示 ===")
    
    # 查询所有记忆
    all_memories = await memory_system.query(MemoryQuery(limit=10))
    print(f"总记忆数量: {len(all_memories)}")
    
    # 按类型查询
    conversation_query = MemoryQuery(
        type=MemoryType.CONVERSATION,
        limit=5
    )
    conversations = await memory_system.query(conversation_query)
    print(f"对话记忆数量: {len(conversations)}")
    
    # 按标签查询
    tag_query = MemoryQuery(
        tags=["Python"],
        limit=5
    )
    python_memories = await memory_system.query(tag_query)
    print(f"Python相关记忆数量: {len(python_memories)}")
    
    # 获取记忆详情
    if all_memories:
        first_memory = all_memories[0]
        print(f"\n第一个记忆详情:")
        print(f"  ID: {first_memory.id}")
        print(f"  类型: {first_memory.type.value}")
        print(f"  内容: {first_memory.content}")
        print(f"  优先级: {first_memory.priority.value}")
        print(f"  标签: {first_memory.metadata.tags}")
        print(f"  创建时间: {first_memory.created_at}")
        print(f"  设备ID: {first_memory.device_id}")
    
    # 记忆统计
    stats = memory_system.get_stats()
    print(f"\n记忆统计:")
    print(f"  总记忆数: {stats['total_memories']}")
    print(f"  按类型分布: {stats['by_type']}")
    if stats.get('by_device'):
        print(f"  按设备分布: {stats['by_device']}")


async def demonstrate_sync_operations(memory_system: MemorySystem, local_device_id: str) -> None:
    """演示同步操作"""
    
    print("\n=== 同步操作演示 ===")
    
    # 创建同步引擎
    sync_engine = SyncEngine(memory_system, local_device_id)
    
    # 模拟远程设备
    remote_device = DeviceInfo(
        device_id="remote-pc-001",
        name="远程办公电脑",
        device_type=DeviceType.DESKTOP,
        ip_address="192.168.1.100",
        port=8765,
        capabilities=[DeviceCapability.MEMORY_SYNC, DeviceCapability.FILE_SHARING]
    )
    
    # 添加设备
    await sync_engine.add_device(remote_device)
    print(f"添加设备: {remote_device.name} ({remote_device.device_id})")
    
    # 启动同步引擎
    await sync_engine.start()
    print("同步引擎已启动")
    
    # 执行同步
    print(f"开始与设备 {remote_device.device_id} 同步...")
    session = await sync_engine.sync_with_device(
        remote_device.device_id,
        strategy=SyncStrategy.LAST_WRITE_WINS
    )
    
    print(f"同步会话已创建: {session.id}")
    print(f"同步策略: {session.strategy.value}")
    
    # 等待同步完成
    print("等待同步完成...")
    for i in range(10):  # 最多等待10秒
        await asyncio.sleep(1)
        
        updated_session = await sync_engine.get_sync_status(session.id)
        if updated_session and updated_session.status.value in ["completed", "failed"]:
            print(f"\n同步完成!")
            print(f"  状态: {updated_session.status.value}")
            print(f"  总记忆数: {updated_session.total_memories}")
            print(f"  已同步: {updated_session.synced_memories}")
            print(f"  失败数: {updated_session.failed_memories}")
            print(f"  冲突数: {updated_session.conflict_memories}")
            print(f"  耗时: {updated_session.end_time - updated_session.start_time:.2f}秒")
            break
        else:
            print(f".", end="", flush=True)
    
    # 显示同步统计
    sync_stats = sync_engine.get_stats()
    print(f"\n同步引擎统计:")
    print(f"  已连接设备: {sync_stats['connected_devices']}")
    print(f"  总同步会话: {sync_stats['total_sessions']}")
    print(f"  成功会话: {sync_stats['completed_sessions']}")
    print(f"  失败会话: {sync_stats['failed_sessions']}")
    print(f"  总操作数: {sync_stats['total_operations']}")
    print(f"  成功操作: {sync_stats['completed_operations']}")
    print(f"  失败操作: {sync_stats['failed_operations']}")
    print(f"  冲突操作: {sync_stats['conflict_operations']}")
    
    # 停止同步引擎
    await sync_engine.stop()
    print("同步引擎已停止")


async def demonstrate_conflict_resolution() -> None:
    """演示冲突解决"""
    
    print("\n=== 冲突解决演示 ===")
    
    from src.core.sync import ConflictResolver
    
    # 创建两个有冲突的记忆（模拟本地和远程）
    local_memory = MemoryItem(
        type=MemoryType.CONVERSATION,
        content={
            "user": "今天吃什么？",
            "assistant": "建议吃中餐，比如宫保鸡丁。",
            "context": "午餐建议"
        },
        priority=MemoryPriority.MEDIUM,
        device_id="local-pc-001"
    )
    local_memory.updated_at = time.time() - 3600  # 1小时前
    
    remote_memory = MemoryItem(
        type=MemoryType.CONVERSATION,
        content={
            "user": "今天吃什么？",
            "assistant": "建议吃西餐，比如意大利面。",  # 冲突内容
            "context": "午餐建议"
        },
        priority=MemoryPriority.HIGH,  # 冲突优先级
        device_id="remote-pc-001"
    )
    remote_memory.updated_at = time.time() - 1800  # 30分钟前（更新）
    
    print("冲突检测:")
    print(f"  本地记忆更新时间: {local_memory.updated_at}")
    print(f"  远程记忆更新时间: {remote_memory.updated_at}")
    print(f"  本地记忆优先级: {local_memory.priority.value}")
    print(f"  远程记忆优先级: {remote_memory.priority.value}")
    print(f"  本地记忆内容: {local_memory.content['assistant']}")
    print(f"  远程记忆内容: {remote_memory.content['assistant']}")
    
    # 检测冲突
    has_conflict = ConflictResolver.detect_conflict(local_memory, remote_memory)
    print(f"\n是否存在冲突: {has_conflict}")
    
    if has_conflict:
        print("\n不同策略的解决结果:")
        
        # 最后写入获胜
        last_write_wins = ConflictResolver.resolve_last_write_wins(local_memory, remote_memory)
        print(f"  最后写入获胜: {last_write_wins.content['assistant']} (设备: {last_write_wins.device_id})")
        
        # 源设备优先（假设源设备是本地）
        source_priority = ConflictResolver.resolve_source_priority(local_memory, remote_memory, "local-pc-001")
        print(f"  源设备优先: {source_priority.content['assistant']} (设备: {source_priority.device_id})")
        
        # 自动合并
        auto_merged = ConflictResolver.auto_merge(local_memory, remote_memory)
        print(f"  自动合并: {auto_merged.content['assistant']}")
        print(f"  合并后优先级: {auto_merged.priority.value}")
        print(f"  合并后标签数: {len(auto_merged.metadata.tags)}")


async def main() -> None:
    """主演示函数"""
    
    print("=== PAO 系统记忆同步演示 ===")
    print("第二阶段：本地记忆系统与基本同步")
    print()
    
    # 创建记忆系统
    memory_system = MemorySystem()
    await memory_system.load()
    
    # 本地设备ID
    local_device_id = "demo-pc-001"
    
    # 1. 创建示例记忆
    print("1. 创建示例记忆...")
    await create_sample_memories(memory_system, local_device_id)
    
    # 2. 演示记忆操作
    await demonstrate_memory_operations(memory_system)
    
    # 3. 演示同步操作
    await demonstrate_sync_operations(memory_system, local_device_id)
    
    # 4. 演示冲突解决
    await demonstrate_conflict_resolution()
    
    # 5. 清理演示数据（可选）
    print("\n5. 清理演示数据...")
    # 在实际使用中，这里可以删除演示创建的记忆
    
    print("\n=== 演示完成 ===")
    print("PAO 系统记忆同步功能演示完毕。")
    print("第二阶段核心功能已实现：")
    print("  ✓ 本地记忆存储和管理")
    print("  ✓ 记忆查询和检索")
    print("  ✓ 跨设备同步引擎")
    print("  ✓ 冲突检测和解决")
    print("  ✓ 多种同步策略")


if __name__ == "__main__":
    import time
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n演示被用户中断")
    except Exception as e:
        print(f"演示出错: {e}")
        import traceback
        traceback.print_exc()