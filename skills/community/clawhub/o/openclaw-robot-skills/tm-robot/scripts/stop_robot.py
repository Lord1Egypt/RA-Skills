#!/usr/bin/env python3
"""
TM Robot - Stop Motion
"""

import asyncio


ROBOT_IP = "192.168.1.13"


async def stop_robot():
    """Stop robot motion"""
    from techmanpy import connect_sct
    
    print("=" * 50)
    print("TM Robot - Stop Motion")
    print("=" * 50)
    
    try:
        async with connect_sct(robot_ip=ROBOT_IP, conn_timeout=5) as conn:
            print("[OK] Connected!")
            await conn.stop_motion()
            print("[OK] Motion stopped")
            
    except Exception as e:
        print(f"[FAIL] {e}")


def main():
    asyncio.run(stop_robot())


if __name__ == "__main__":
    main()
