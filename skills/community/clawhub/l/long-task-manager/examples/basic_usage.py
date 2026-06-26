#!/usr/bin/env python3
"""
Long Task Manager - 基础使用示例
"""

import sys
import time
sys.path.insert(0, '../lib')

from long_task_manager import LongTaskManager, TaskWorker


def example_basic():
    """基础示例"""
    print("=" * 60)
    print("示例1: 基础任务提交与查询")
    print("=" * 60)
    
    # 1. 初始化管理器
    manager = LongTaskManager(task_dir="/tmp/example_tasks")
    
    # 2. 提交任务
    task_id = manager.submit(
        agent_id="code_gen_ali",
        task_config={
            "name": "生成API接口",
            "type": "code_gen",
            "total_items": 10,
            "params": {"module": "Test.API"}
        }
    )
    
    print(f"\n任务已提交: {task_id}\n")
    
    # 3. 模拟Agent内部执行
    def simulate_agent_work():
        worker = TaskWorker(task_id, "/tmp/example_tasks")
        
        for i in range(10):
            # 模拟工作
            time.sleep(0.5)
            
            # 上报进度
            worker.update_progress(
                progress=f"{(i+1)*10}%",
                current_item=f"Api{i+1}Controller",
                detail=f"正在生成第{i+1}个API...",
                completed=i+1
            )
        
        # 完成任务
        worker.complete({
            "files": [f"Api{i}Controller.cs" for i in range(1, 11)],
            "summary": "成功生成10个API接口"
        })
    
    # 启动模拟工作 (在另一个线程中)
    import threading
    thread = threading.Thread(target=simulate_agent_work)
    thread.start()
    
    # 4. 主程序轮询查询
    print("轮询查询进度:\n")
    while True:
        status = manager.get_status(task_id)
        
        print(f"[{status['status']}] {status['progress']} - {status['current_item']}")
        
        if status['status'] in ['completed', 'failed', 'cancelled']:
            break
        
        time.sleep(1)
    
    # 5. 获取结果
    result = manager.get_result(task_id)
    print(f"\n✅ 任务完成!")
    print(f"   生成文件: {len(result['files'])} 个")
    print(f"   摘要: {result['summary']}")
    
    thread.join()


def example_cancel():
    """取消任务示例"""
    print("\n" + "=" * 60)
    print("示例2: 取消任务")
    print("=" * 60)
    
    manager = LongTaskManager(task_dir="/tmp/example_tasks")
    
    # 提交长时间任务
    task_id = manager.submit(
        agent_id="data_miner",
        task_config={
            "name": "数据分析",
            "type": "data_process",
            "total_items": 100
        }
    )
    
    print(f"\n任务已提交: {task_id}")
    
    # 2秒后取消
    time.sleep(2)
    print("\n⏱️ 2秒后取消任务...")
    
    cancelled = manager.cancel(task_id)
    print(f"取消结果: {'成功' if cancelled else '失败'}")
    
    # 查询状态
    status = manager.get_status(task_id)
    print(f"任务状态: {status['status']}")


def example_list_tasks():
    """列表示例"""
    print("\n" + "=" * 60)
    print("示例3: 列出所有任务")
    print("=" * 60)
    
    manager = LongTaskManager(task_dir="/tmp/example_tasks")
    
    # 列出所有任务
    tasks = manager.list_tasks()
    
    print(f"\n共 {len(tasks)} 个任务:\n")
    print(f"{'任务ID':<30} {'状态':<12} {'进度':<8} {'更新时间'}")
    print("-" * 70)
    
    for task in tasks[:5]:  # 显示前5个
        print(f"{task['task_id'][:30]:<30} "
              f"{task['status']:<12} "
              f"{task['progress']:<8} "
              f"{task.get('updated_at', 'N/A')[:19]}")


if __name__ == "__main__":
    # 运行示例
    example_basic()
    example_cancel()
    example_list_tasks()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
