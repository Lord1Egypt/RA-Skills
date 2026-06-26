#!/usr/bin/env python3
"""
TM Robot - Move 100mm along X axis
"""

import asyncio


ROBOT_IP = "192.168.1.13"


async def move_x_100():
    """Move 100mm along X axis (relative)"""
    from techmanpy import connect_sct
    
    print("=" * 50)
    print("TM Robot - Move X +100mm")
    print("=" * 50)
    
    try:
        async with connect_sct(robot_ip=ROBOT_IP) as conn:
            print("[OK] Connected!")
            
            # Move relative in Cartesian space
            # Parameters: [dX, dY, dZ, dRx, dRy, dRz], speed_percentage, acceleration_duration
            relative_target = [100, 0, 0, 0, 0, 0]  # X +100mm
            
            print(f"\n[INFO] Relative move: X +100mm")
            print(f"[INFO] Speed: 20%")
            print("\n[WARNING] Robot will move! Keep clear!\n")
            
            # Line move (Cartesian space) - speed is percentage
            await conn.move_to_relative_point_line(
                relative_point_goal=relative_target,
                speed=0.2,              # 20% speed
                acceleration_duration=50  # percentage
            )
            
            print("[OK] Motion command sent!")
            print("[INFO] Moving X +100mm")
            
    except Exception as e:
        print(f"[FAIL] {e}")


def main():
    print("\n" + "=" * 50)
    print("SAFETY WARNING")
    print("=" * 50)
    print("Robot will move 100mm along X axis.")
    print("Keep clear of the robot's working area!")
    print("=" * 50 + "\n")
    
    asyncio.run(move_x_100())


if __name__ == "__main__":
    main()
