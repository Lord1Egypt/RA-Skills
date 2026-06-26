"""
多机器人协同示例

复现 demo_multi_agent.py 的功能，展示如何使用 MultiRobotSkill 进行多机器人协同控制。
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multi_robot_skill import MultiRobotSkill


def main():
    print("=" * 60)
    print("          多机器人协同控制示例")
    print("=" * 60)
    print()

    # 创建 Skill
    skill = MultiRobotSkill(max_workers=4, log_level="INFO")

    # 注册机器人
    print("正在注册机器人...")
    skill.register_robot("vansbot", "http://192.168.3.113:5000", robot_type="vansbot")
    skill.register_robot("dog1", "http://localhost:8000", robot_type="puppypi", robot_id=1)
    skill.register_robot("dog2", "http://localhost:8000", robot_type="puppypi", robot_id=2)
    print(f"已注册机器人: {', '.join(skill.list_robots())}")
    print()

    # 创建任务计划
    print("创建任务计划...")
    plan = skill.create_plan(
        name="物流协同任务",
        description="机械臂抓取物体并放入机器狗篮筐，机器狗运送到卸货区"
    )

    # 步骤1: 机械臂识别物体
    task1 = skill.create_task(
        robot="vansbot",
        action="detect_objects",
        params={"move_to_capture": True, "include_image": False},
        name="识别物体",
        description="机械臂识别桌面物体"
    )
    plan.add_task(task1)

    # 步骤2: 机械臂移动到绿色方块
    task2 = skill.create_task(
        robot="vansbot",
        action="move_to_object",
        params={"object_no": 0},
        name="移动到物体",
        description="移动到绿色方块上方",
        depends_on=[task1.id]
    )
    plan.add_task(task2)

    # 步骤3: 机械臂抓取
    task3 = skill.create_task(
        robot="vansbot",
        action="grab",
        name="抓取物体",
        description="抓取绿色方块",
        depends_on=[task2.id]
    )
    plan.add_task(task3)

    # 步骤4: 机械臂抬升
    task4 = skill.create_task(
        robot="vansbot",
        action="move_to_place",
        params={"place_name": "capture"},
        name="抬升机械臂",
        description="抬升到安全位置",
        depends_on=[task3.id]
    )
    plan.add_task(task4)

    # 步骤5: 并行任务 - 狗2去充电区，狗1去装货区
    task5_1 = skill.create_task(
        robot="dog2",
        action="move_to_zone",
        params={"target_zone": "charging"},
        name="狗2去充电区",
        description="狗2前往充电区"
    )

    task5_2 = skill.create_task(
        robot="dog1",
        action="move_to_zone",
        params={"target_zone": "loading"},
        name="狗1去装货区",
        description="狗1前往装货区"
    )

    task5 = skill.create_parallel_tasks(
        [task5_1, task5_2],
        name="并行移动",
        description="狗2去充电区，狗1去装货区",
        depends_on=[task4.id]
    )
    plan.add_task(task5)

    # 步骤6: 狗1调整装货姿势
    task6 = skill.create_task(
        robot="dog1",
        action="load",
        params={"target_zone": "loading"},
        name="调整装货姿势",
        description="狗1调整为装货姿态",
        depends_on=[task5.id]
    )
    plan.add_task(task6)

    # 步骤7: 机械臂拍摄定位篮筐
    task7 = skill.create_task(
        robot="vansbot",
        action="capture_for_dog",
        params={"move_to_capture": True, "include_image": False},
        name="定位篮筐",
        description="拍摄网格图定位狗1篮筐",
        depends_on=[task6.id]
    )
    plan.add_task(task7)

    # 步骤8: 机械臂放置物体到篮筐
    # 注意：这里需要用户输入点位ID，在实际使用中可以通过视觉识别自动获取
    task8 = skill.create_task(
        robot="vansbot",
        action="release_to_dog",
        params={"point_id": 5},  # 假设点位ID为5
        name="放置到篮筐",
        description="将物体放入狗1篮筐",
        depends_on=[task7.id]
    )
    plan.add_task(task8)

    # 步骤9: 机械臂复位
    task9 = skill.create_task(
        robot="vansbot",
        action="move_to_place",
        params={"place_name": "capture"},
        name="机械臂复位",
        description="机械臂返回拍照位置",
        depends_on=[task8.id]
    )
    plan.add_task(task9)

    # 步骤10: 狗1前往卸货区
    task10 = skill.create_task(
        robot="dog1",
        action="move_to_zone",
        params={"target_zone": "unloading"},
        name="前往卸货区",
        description="狗1前往卸货区",
        depends_on=[task9.id]
    )
    plan.add_task(task10)

    # 步骤11: 狗1卸货
    task11 = skill.create_task(
        robot="dog1",
        action="unload",
        name="执行卸货",
        description="狗1执行卸货动作",
        depends_on=[task10.id]
    )
    plan.add_task(task11)

    # 步骤12: 狗1前往停靠区
    task12 = skill.create_task(
        robot="dog1",
        action="move_to_zone",
        params={"target_zone": "parking"},
        name="前往停靠区",
        description="狗1前往停靠区",
        depends_on=[task11.id]
    )
    plan.add_task(task12)

    print(f"任务计划创建完成，共 {len(plan.tasks)} 个任务")
    print()

    # 注册事件回调
    def on_task_started(event):
        print(f"[开始] {event['task_name']}")

    def on_task_completed(event):
        print(f"[完成] 任务ID: {event['task_id']}, 耗时: {event['execution_time']:.2f}秒")

    def on_task_failed(event):
        print(f"[失败] 任务ID: {event['task_id']}, 错误: {event['error']}")

    skill.on_event("task_started", on_task_started)
    skill.on_event("task_completed", on_task_completed)
    skill.on_event("task_failed", on_task_failed)

    # 执行任务计划
    print("开始执行任务计划...")
    print("=" * 60)
    print()

    try:
        results = skill.execute_plan(plan)

        # 统计结果
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful

        print()
        print("=" * 60)
        print(f"任务执行完成！")
        print(f"成功: {successful}/{len(results)}")
        print(f"失败: {failed}/{len(results)}")
        print()

        # 显示失败的任务
        if failed > 0:
            print("失败的任务:")
            for result in results:
                if not result.success:
                    print(f"  - {result.task_name}: {result.message}")
            print()

        # 显示系统状态
        status = skill.get_status()
        print("系统状态:")
        print(f"  状态: {status['system']['status']}")
        print(f"  完成任务数: {status['system']['completed_tasks']}")
        print(f"  失败任务数: {status['system']['failed_tasks']}")
        print()

        print("机器人状态:")
        for robot_name, robot_state in status['robots'].items():
            print(f"  {robot_name}:")
            print(f"    连接: {robot_state['connected']}")
            print(f"    忙碌: {robot_state['busy']}")
            if robot_state.get('battery'):
                print(f"    电量: {robot_state['battery']}")

    except Exception as e:
        print(f"执行失败: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # 关闭 Skill
        skill.shutdown()

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
