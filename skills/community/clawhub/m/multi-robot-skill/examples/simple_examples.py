"""
简单示例

展示如何用简洁的方式使用 MultiRobotSkill。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multi_robot_skill import MultiRobotSkill


def example_1_simple_action():
    """示例1: 简单的单机器人动作"""
    print("\n=== 示例1: 简单的单机器人动作 ===\n")

    with MultiRobotSkill() as skill:
        # 注册机械臂
        skill.register_robot("vansbot", "http://192.168.3.113:5000")

        # 创建并执行简单任务
        plan = skill.create_plan("检测物体")
        task = skill.create_task("vansbot", "detect_objects")
        plan.add_task(task)

        results = skill.execute_plan(plan)
        print(f"检测结果: {results[0].data}")


def example_2_sequential_tasks():
    """示例2: 顺序执行多个任务"""
    print("\n=== 示例2: 顺序执行多个任务 ===\n")

    with MultiRobotSkill() as skill:
        skill.register_robot("vansbot", "http://192.168.3.113:5000")

        plan = skill.create_plan("抓取物体")

        # 创建顺序任务
        detect = skill.create_task("vansbot", "detect_objects")
        move = skill.create_task("vansbot", "move_to_object", {"object_no": 0}, depends_on=[detect.id])
        grab = skill.create_task("vansbot", "grab", depends_on=[move.id])

        plan.add_task(detect)
        plan.add_task(move)
        plan.add_task(grab)

        results = skill.execute_plan(plan)
        print(f"执行了 {len(results)} 个任务")


def example_3_parallel_tasks():
    """示例3: 并行执行任务"""
    print("\n=== 示例3: 并行执行任务 ===\n")

    with MultiRobotSkill() as skill:
        skill.register_robot("dog1", "http://localhost:8000", robot_type="puppypi", robot_id=1)
        skill.register_robot("dog2", "http://localhost:8000", robot_type="puppypi", robot_id=2)

        plan = skill.create_plan("并行移动")

        # 创建并行任务
        task1 = skill.create_task("dog1", "move_to_zone", {"target_zone": "loading"})
        task2 = skill.create_task("dog2", "move_to_zone", {"target_zone": "charging"})

        parallel_task = skill.create_parallel_tasks([task1, task2], name="两只狗同时移动")
        plan.add_task(parallel_task)

        results = skill.execute_plan(plan)
        print("两只狗已同时到达目标位置")


def example_4_coordination():
    """示例4: 机械臂和机器狗协同"""
    print("\n=== 示例4: 机械臂和机器狗协同 ===\n")

    with MultiRobotSkill() as skill:
        # 注册所有机器人
        skill.register_robot("vansbot", "http://192.168.3.113:5000")
        skill.register_robot("dog1", "http://localhost:8000", robot_type="puppypi", robot_id=1)

        plan = skill.create_plan("协同运输")

        # 机械臂任务
        detect = skill.create_task("vansbot", "detect_objects", name="检测物体")
        grab = skill.create_task("vansbot", "grab", name="抓取", depends_on=[detect.id])

        # 机器狗任务（与抓取并行）
        dog_move = skill.create_task("dog1", "move_to_zone", {"target_zone": "loading"}, name="狗移动到装货区")
        dog_load = skill.create_task("dog1", "load", name="狗调整姿势", depends_on=[dog_move.id])

        # 放置任务（需要等待机械臂抓取和狗准备好）
        place = skill.create_task(
            "vansbot",
            "release_to_dog",
            {"point_id": 5},
            name="放置到篮筐",
            depends_on=[grab.id, dog_load.id]
        )

        # 运输任务
        transport = skill.create_task(
            "dog1",
            "move_to_zone",
            {"target_zone": "unloading"},
            name="运输到卸货区",
            depends_on=[place.id]
        )

        unload = skill.create_task("dog1", "unload", name="卸货", depends_on=[transport.id])

        # 添加所有任务
        for task in [detect, grab, dog_move, dog_load, place, transport, unload]:
            plan.add_task(task)

        # 执行
        results = skill.execute_plan(plan)
        successful = sum(1 for r in results if r.success)
        print(f"协同任务完成: {successful}/{len(results)} 成功")


def example_5_with_events():
    """示例5: 使用事件回调"""
    print("\n=== 示例5: 使用事件回调 ===\n")

    with MultiRobotSkill() as skill:
        skill.register_robot("vansbot", "http://192.168.3.113:5000")

        # 注册事件回调
        skill.on_event("task_started", lambda e: print(f"▶ 开始: {e['task_name']}"))
        skill.on_event("task_completed", lambda e: print(f"✓ 完成: {e['task_id']} ({e['execution_time']:.2f}s)"))
        skill.on_event("task_failed", lambda e: print(f"✗ 失败: {e['error']}"))

        plan = skill.create_plan("带事件的任务")
        task = skill.create_task("vansbot", "detect_objects")
        plan.add_task(task)

        results = skill.execute_plan(plan)


def example_6_error_handling():
    """示例6: 错误处理"""
    print("\n=== 示例6: 错误处理 ===\n")

    with MultiRobotSkill() as skill:
        # 配置错误处理
        skill.configure_error_handling({
            "max_retries": 3,
            "retry_delay": 1.0,
            "default_strategy": "retry"
        })

        skill.register_robot("vansbot", "http://192.168.3.113:5000")

        plan = skill.create_plan("带重试的任务")
        task = skill.create_task("vansbot", "detect_objects", timeout=30.0)
        plan.add_task(task)

        results = skill.execute_plan(plan)
        print(f"任务状态: {'成功' if results[0].success else '失败'}")


if __name__ == "__main__":
    print("=" * 60)
    print("     MultiRobotSkill 使用示例")
    print("=" * 60)

    # 运行所有示例
    examples = [
        example_1_simple_action,
        example_2_sequential_tasks,
        example_3_parallel_tasks,
        example_4_coordination,
        example_5_with_events,
        example_6_error_handling,
    ]

    for i, example in enumerate(examples, 1):
        try:
            example()
        except Exception as e:
            print(f"示例 {i} 执行失败: {e}")

    print("\n" + "=" * 60)
    print("所有示例执行完成")
    print("=" * 60)
