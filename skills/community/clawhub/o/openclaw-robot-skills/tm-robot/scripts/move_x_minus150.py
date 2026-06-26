#!/usr/bin/env python3
import asyncio
from techmanpy import connect_sct

async def move():
    async with connect_sct(robot_ip='192.168.1.13') as conn:
        await conn.move_to_relative_point_line([-150, 0, 0, 0, 0, 0], 0.2, 50)
        print('[OK] X -150mm')

asyncio.run(move())
