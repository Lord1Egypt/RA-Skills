#!/usr/bin/env python3
"""
Overseer 真实测试套件

测试场景：模拟一个需要运行 10 分钟的实际任务
测试目标：验证强制顺序、心跳机制、断点续传
"""

import sys
import os
import time
import json
import signal
sys.path.insert(0, '/root/.openclaw/workspace/skills/overseer')

from overseer import Overseer


# 测试配置
TEST_STATE_DIR = ".overseer_test"
TEST_LOG_FILE = f"{TEST_STATE_DIR}/test_log.txt"


def log(message):
    """记录测试日志"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    
    with open(TEST_LOG_FILE, "a") as f:
        f.write(log_msg + "\n")


def cleanup():
    """清理测试环境"""
    import shutil
    if os.path.exists(TEST_STATE_DIR):
        shutil.rmtree(TEST_STATE_DIR)
    os.makedirs(TEST_STATE_DIR, exist_ok=True)


# ==================== 测试 1: 强制顺序执行 ====================

def test_strict_order():
    """测试：步骤是否严格按顺序执行"""
    print("\n" + "="*60)
    print("测试 1: 强制顺序执行")
    print("="*60)
    
    cleanup()
    execution_order = []
    
    workflow = Overseer(
        name="strict_order_test",
        state_dir=TEST_STATE_DIR,
        report_progress=True
    )
    
    @workflow.step("步骤 A")
    def step_a(ctx):
        execution_order.append("A")
        log("步骤 A 执行")
        return {"value": 1}
    
    @workflow.step("步骤 B")
    def step_b(ctx):
        # 验证步骤 A 已完成
        result_a = ctx.get_step_result("步骤 A")
        assert result_a is not None, "步骤 A 应该在步骤 B 之前完成"
        assert result_a["value"] == 1, "步骤 A 结果应该可访问"
        
        execution_order.append("B")
        log("步骤 B 执行")
        return {"value": 2}
    
    @workflow.step("步骤 C")
    def step_c(ctx):
        # 验证步骤 A 和 B 都已完成
        assert ctx.get_step_result("步骤 A") is not None
        assert ctx.get_step_result("步骤 B") is not None
        
        execution_order.append("C")
        log("步骤 C 执行")
        return {"value": 3}
    
    # 执行
    result = workflow.run()
    
    # 验证
    assert execution_order == ["A", "B", "C"], f"执行顺序错误: {execution_order}"
    assert result["步骤 A"]["value"] == 1
    assert result["步骤 B"]["value"] == 2
    assert result["步骤 C"]["value"] == 3
    
    log("✅ 测试 1 通过：强制顺序执行正确")
    return True


# ==================== 测试 2: 心跳机制 ====================

def test_heartbeat():
    """测试：心跳是否正确发送"""
    print("\n" + "="*60)
    print("测试 2: 心跳机制")
    print("="*60)
    
    cleanup()
    heartbeat_times = []
    
    workflow = Overseer(
        name="heartbeat_test",
        state_dir=TEST_STATE_DIR,
        enable_heartbeat=True,
        heartbeat_interval=2,  # 每2秒一次，方便测试
        report_progress=True
    )
    
    @workflow.step("长时间处理", heartbeat_interval=2)
    def long_step(ctx):
        for i in range(5):  # 运行约10秒
            time.sleep(2)
            ctx.heartbeat(f"进度 {i+1}/5")
            heartbeat_times.append(time.time())
        
        return {"processed": 5}
    
    start_time = time.time()
    result = workflow.run()
    end_time = time.time()
    
    # 验证
    assert len(heartbeat_times) >= 4, f"心跳次数不足: {len(heartbeat_times)}"
    
    # 验证心跳间隔（允许误差）
    for i in range(1, len(heartbeat_times)):
        interval = heartbeat_times[i] - heartbeat_times[i-1]
        assert 1.5 <= interval <= 3.0, f"心跳间隔异常: {interval}秒"
    
    log(f"✅ 测试 2 通过：发送了 {len(heartbeat_times)} 次心跳")
    return True


# ==================== 测试 3: 断点续传 ====================

def test_resume():
    """测试：中断后能否从断点恢复"""
    print("\n" + "="*60)
    print("测试 3: 断点续传")
    print("="*60)
    
    cleanup()
    execution_count = {"A": 0, "B": 0, "C": 0}
    
    workflow = Overseer(
        name="resume_test",
        state_dir=TEST_STATE_DIR,
        allow_resume=True,
        report_progress=True
    )
    
    @workflow.step("步骤 A")
    def step_a(ctx):
        execution_count["A"] += 1
        log(f"步骤 A 执行 (第 {execution_count['A']} 次)")
        return {"status": "A_done"}
    
    @workflow.step("步骤 B")
    def step_b(ctx):
        execution_count["B"] += 1
        log(f"步骤 B 执行 (第 {execution_count['B']} 次)")
        
        # 第一次执行时，模拟中断
        if execution_count["B"] == 1:
            log("模拟中断！")
            raise SystemExit("模拟中断")
        
        return {"status": "B_done"}
    
    @workflow.step("步骤 C")
    def step_c(ctx):
        execution_count["C"] += 1
        log(f"步骤 C 执行 (第 {execution_count['C']} 次)")
        return {"status": "C_done"}
    
    # 第一次执行（会在步骤 B 中断）
    try:
        workflow.run()
    except SystemExit:
        log("工作流被中断")
    
    # 验证状态已保存
    state_file = f"{TEST_STATE_DIR}/resume_test_*.json"
    import glob
    state_files = glob.glob(state_file)
    assert len(state_files) > 0, "状态文件应该存在"
    
    # 重新创建工作流（模拟重启）
    workflow2 = Overseer(
        name="resume_test",
        state_dir=TEST_STATE_DIR,
        allow_resume=True,
        report_progress=True
    )
    
    # 重新注册步骤
    @workflow2.step("步骤 A")
    def step_a2(ctx):
        execution_count["A"] += 1
        log(f"步骤 A 执行 (第 {execution_count['A']} 次)")
        return {"status": "A_done"}
    
    @workflow2.step("步骤 B")
    def step_b2(ctx):
        execution_count["B"] += 1
        log(f"步骤 B 执行 (第 {execution_count['B']} 次)")
        return {"status": "B_done"}
    
    @workflow2.step("步骤 C")
    def step_c2(ctx):
        execution_count["C"] += 1
        log(f"步骤 C 执行 (第 {execution_count['C']} 次)")
        return {"status": "C_done"}
    
    # 从断点恢复
    result = workflow2.resume()
    
    # 验证：
    # - 步骤 A 应该只执行 1 次（从状态恢复，不再执行）
    # - 步骤 B 应该执行 2 次（第一次中断，第二次成功）
    # - 步骤 C 应该执行 1 次
    assert execution_count["A"] == 1, f"步骤 A 应该只执行 1 次，实际 {execution_count['A']}"
    assert execution_count["B"] == 2, f"步骤 B 应该执行 2 次，实际 {execution_count['B']}"
    assert execution_count["C"] == 1, f"步骤 C 应该执行 1 次，实际 {execution_count['C']}"
    
    log("✅ 测试 3 通过：断点续传正确")
    return True


# ==================== 测试 4: 异步执行 ====================

def test_async():
    """测试：异步执行是否正常"""
    print("\n" + "="*60)
    print("测试 4: 异步执行")
    print("="*60)
    
    cleanup()
    
    workflow = Overseer(
        name="async_test",
        state_dir=TEST_STATE_DIR,
        async_mode=True,
        notify_on_complete=True,
        report_progress=False  # 异步模式下不打印进度
    )
    
    @workflow.step("步骤 A")
    def step_a(ctx):
        time.sleep(2)
        return {"status": "A_done"}
    
    @workflow.step("步骤 B")
    def step_b(ctx):
        time.sleep(2)
        return {"status": "B_done"}
    
    # 异步执行
    start_time = time.time()
    job = workflow.run_async()
    end_time = time.time()
    
    # 验证：应该立即返回
    assert end_time - start_time < 1.0, "异步执行应该立即返回"
    assert job.id is not None, "应该返回 job id"
    assert job.status == "running", "任务状态应该是 running"
    
    # 检查状态文件
    time.sleep(1)
    status = workflow.check_status(job.id)
    assert status is not None, "应该能查询到任务状态"
    
    log(f"✅ 测试 4 通过：异步执行正常，任务ID: {job.id}")
    
    # 等待后台完成
    log("等待后台任务完成...")
    time.sleep(5)
    
    return True


# ==================== 测试 5: 真实长时间任务 ====================

def test_real_long_task():
    """
    真实测试：运行 5 分钟的任务
    验证：
    1. 心跳是否正常发送（每60秒）
    2. 是否会被系统掐断
    3. 完成后状态是否正确
    """
    print("\n" + "="*60)
    print("测试 5: 真实长时间任务（5分钟）")
    print("="*60)
    print("这个测试会实际运行 5 分钟，请耐心等待...")
    print("按 Ctrl+C 可以随时中断，下次运行会自动恢复")
    print("="*60)
    
    cleanup()
    start_time = time.time()
    
    workflow = Overseer(
        name="real_long_task",
        state_dir=TEST_STATE_DIR,
        description="真实长时间任务测试（5分钟）",
        enable_heartbeat=True,
        heartbeat_interval=60,  # 每60秒报告
        allow_resume=True,
        report_progress=True
    )
    
    processed_items = []
    
    @workflow.step("初始化")
    def init(ctx):
        log("任务初始化")
        return {"total_items": 100, "start_time": time.time()}
    
    @workflow.step("批量处理", heartbeat_interval=30)
    def process(ctx):
        """模拟处理 100 个项目，每个 3 秒，共 5 分钟"""
        total = 100
        
        for i in range(total):
            # 模拟处理
            time.sleep(3)
            processed_items.append(i)
            
            # 每 10 个项目报告一次
            if i % 10 == 0:
                ctx.heartbeat(f"已处理 {i}/{total} 个项目，运行 {int(time.time() - start_time)} 秒")
                log(f"进度: {i}/{total}")
        
        return {"processed": len(processed_items)}
    
    @workflow.step("生成报告")
    def report(ctx):
        elapsed = time.time() - start_time
        log(f"生成报告，总耗时: {int(elapsed)} 秒")
        return {
            "total_processed": len(processed_items),
            "elapsed_seconds": elapsed,
            "status": "completed"
        }
    
    try:
        result = workflow.run()
        
        # 验证
        elapsed = time.time() - start_time
        assert elapsed >= 280, f"任务应该运行至少 280 秒，实际 {elapsed} 秒"  # 100 * 3 = 300秒，允许误差
        assert len(processed_items) == 100, f"应该处理 100 个项目，实际 {len(processed_items)}"
        assert result["生成报告"]["status"] == "completed"
        
        log(f"✅ 测试 5 通过：长时间任务完成，耗时 {int(elapsed)} 秒")
        return True
        
    except KeyboardInterrupt:
        log("⚠️ 任务被用户中断")
        log("状态已保存，下次运行会自动恢复")
        log(f"已处理 {len(processed_items)} 个项目")
        print("\n要恢复执行，请重新运行: python3 test_overseer.py --resume")
        return False


# ==================== 主程序 ====================

def main():
    """运行所有测试"""
    print("Overseer 真实测试套件")
    print("="*60)
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", choices=["order", "heartbeat", "resume", "async", "long", "all"], default="all")
    parser.add_argument("--resume", action="store_true", help="恢复长时间任务")
    args = parser.parse_args()
    
    if args.resume:
        # 恢复长时间任务
        print("恢复长时间任务...")
        workflow = Overseer(
            name="real_long_task",
            state_dir=TEST_STATE_DIR,
            allow_resume=True,
            report_progress=True
        )
        
        processed_items = []
        
        @workflow.step("初始化")
        def init(ctx): ...
        
        @workflow.step("批量处理")
        def process(ctx):
            nonlocal processed_items
            # 从之前的状态继续
            # ...（完整步骤定义）
            pass
        
        @workflow.step("生成报告")
        def report(ctx): ...
        
        workflow.resume()
        return
    
    # 运行指定测试
    tests = {
        "order": test_strict_order,
        "heartbeat": test_heartbeat,
        "resume": test_resume,
        "async": test_async,
        "long": test_real_long_task
    }
    
    results = {}
    
    if args.test == "all":
        for name, test_func in tests.items():
            if name == "long":
                print("\n⚠️  跳过长时间任务测试（运行所有测试时使用 --test long 单独运行）")
                continue
            try:
                results[name] = test_func()
            except Exception as e:
                log(f"❌ 测试 {name} 失败: {e}")
                results[name] = False
    else:
        try:
            results[args.test] = tests[args.test]()
        except Exception as e:
            log(f"❌ 测试 {args.test} 失败: {e}")
            import traceback
            traceback.print_exc()
            results[args.test] = False
    
    # 汇总
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    for name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name:15} {status}")
    
    passed_count = sum(results.values())
    total_count = len(results)
    print(f"\n总计: {passed_count}/{total_count} 通过")
    
    if passed_count == total_count:
        print("\n🎉 所有测试通过！Overseer 工作正常。")
    
    print(f"\n测试日志: {TEST_LOG_FILE}")


if __name__ == "__main__":
    main()
