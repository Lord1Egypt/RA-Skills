#!/usr/bin/env python3
"""
TM Robot - Reset Alarm / Error
"""

import asyncio


ROBOT_IP = "192.168.1.13"


async def reset_alarm():
    """Reset robot alarm/error state"""
    from techmanpy import connect_sct
    
    print("=" * 50)
    print("TM Robot - Reset Alarm")
    print("=" * 50)
    
    try:
        async with connect_sct(robot_ip=ROBOT_IP, conn_timeout=5) as conn:
            print("[OK] Connected!")
            
            # Try to stop motion first
            print("[INFO] Stopping motion...")
            await conn.stop_motion()
            
            print("[INFO] Motion stopped")
            print("[INFO] Robot should be reset from alarm")
            
    except Exception as e:
        print(f"[FAIL] {e}")


async def check_error():
    """Try to read error code via SVR"""
    try:
        from techmanpy import connect_svr
        
        async with connect_svr(robot_ip=ROBOT_IP, conn_timeout=5) as conn:
            print("\n[INFO] Checking error state...")
            try:
                err_code = await conn.get_value("RobotErrCode")
                print(f"    Error Code: {err_code}")
            except:
                pass
            try:
                robot_mode = await conn.get_value("RobotMode")
                print(f"    Robot Mode: {robot_mode}")
            except:
                pass
    except Exception as e:
        print(f"[SVR] {e}")


def main():
    asyncio.run(reset_alarm())
    asyncio.run(check_error())


if __name__ == "__main__":
    main()
