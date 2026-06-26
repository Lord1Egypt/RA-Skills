#!/usr/bin/env python3
"""小佩设备监控 - 获取宠物设备状态"""

import asyncio
import json
import os
import sys
from datetime import datetime

# Patch FEEDER_LIST to include additional feeder models
from petkitaio import constants
additional_feeders = ['D4H', 'S0HO', 'SOHO', 'D4HSOLO', 'D3', 'D4', 'D4s', 'Feeder', 'FeederMini']
for m in additional_feeders:
    if m not in constants.FEEDER_LIST:
        constants.FEEDER_LIST.append(m)

try:
    from petkitaio import PetKitClient
except ImportError:
    print("Error: petkitaio not installed. Run: pip3 install petkitaio")
    sys.exit(1)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

def load_config():
    """加载配置"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}

def save_config(config):
    """保存配置"""
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

async def get_petkit_status(username, password):
    """获取小佩设备状态"""
    client = PetKitClient(username, password, region='China')
    
    try:
        await client.login()
        data = await client.get_petkit_data()
        
        results = []
        
        # 处理喂食器
        for feeder_id, feeder in data.feeders.items():
            state = feeder.data.get('state', {})
            feed_state = state.get('feedState', {})
            food = state.get('food', -1)  # 食物状态: 0=没粮, 1=不足, 2=有粮
            bowl = state.get('bowl', -1)  # 碗状态
            
            # food 字段表示粮桶状态：2=有粮, 1=不足, 0=没粮
            food_status_map = {0: '没粮', 1: '不足', 2: '有粮'}
            food_level_text = food_status_map.get(food, f'未知({food})')
            
            # bowl 字段含义不明，显示原始值
            bowl_status = f'bowl={bowl}'
            
            # 今日已吃量
            today_eaten = feed_state.get('realAmountTotal', 0)  # 今日已吃克数
            today_plan = feed_state.get('planAmountTotal', 0)   # 今日计划克数
            
            # 判断是否需要加粮：food=0 没粮时需要加
            need_food = food == 0
            
            device_info = {
                'name': feeder.data.get('name', '未知喂食器'),
                'model': feeder.data.get('type', 'SOLO').upper(),
                'type': 'feeder',
                'online': True,
                'food_level': food_level_text,
                'bowl_status': bowl_status,
                'today_eaten': today_eaten,
                'today_plan': today_plan,
                'need_food': need_food,
                'power': '正常' if state.get('overall', 0) == 1 else '异常',
            }
            results.append(device_info)
        
        # 处理猫砂盆
        for litter_id, litter in data.litter_boxes.items():
            device_info = {
                'name': litter.data.get('name', '未知猫砂盆'),
                'model': getattr(litter, 'type', 'Unknown'),
                'type': 'litterbox',
                'online': True,
            }
            results.append(device_info)
        
        # 处理饮水机
        for fountain_id, fountain in data.water_fountains.items():
            fountain_data = fountain.data
            device_info = {
                'name': fountain_data.get('name', '未知饮水机'),
                'model': 'W5 Eversweet',
                'type': 'fountain',
                'online': fountain_data.get('powerStatus', 0) == 1,
                'power': fountain_data.get('powerStatus', 0),
                'water_level': '正常' if fountain_data.get('lackWarning', 1) == 0 else '缺水',
                'filter_percent': fountain_data.get('filterPercent', 0),
                'filter_warning': fountain_data.get('filterWarning', 0),
            }
            results.append(device_info)
        
        # 处理净化器
        for purifier_id, purifier in data.purifiers.items():
            device_info = {
                'name': purifier.data.get('name', '未知净化器'),
                'model': getattr(purifier, 'type', 'Unknown'),
                'type': 'purifier',
                'online': True,
            }
            results.append(device_info)
        
        if hasattr(client, 'session') and client.session:
            await client.session.close()
        return results
        
    except Exception as e:
        if hasattr(client, 'session') and client.session:
            await client.session.close()
        return {'error': str(e)}

def format_status(data):
    """格式化输出"""
    if isinstance(data, dict) and 'error' in data:
        return f"❌ 错误: {data['error']}"
    
    if not data:
        return "未找到设备"
    
    output = ["📱 小佩设备状态\n"]
    
    for i, device in enumerate(data, 1):
        name = device.get('name', '未知设备')
        model = device.get('model', 'Unknown')
        
        output.append(f"### {i}. {name}")
        output.append(f"   型号: {model}")
        
        # 设备类型特定信息
        dev_type = device.get('type', '')
        if dev_type == 'feeder':
            food_level = device.get('food_level', 'N/A')
            power = device.get('power', 'N/A')
            need_food = device.get('need_food', False)
            today_eaten = device.get('today_eaten', 0)
            today_plan = device.get('today_plan', 0)
            
            # 判断是否需要加粮
            output.append(f"   🍚 粮桶: {food_level} {'⚠️ 请加粮！' if need_food else '✅'}")
            output.append(f"   🐱 今日已吃: {today_eaten}g / 计划 {today_plan}g")
            output.append(f"   🔌 电源: {power}")
            
        elif dev_type == 'litterbox':
            output.append(f"   🚽 猫砂盆在线")
            
        elif dev_type == 'fountain':
            water_level = device.get('water_level', 'N/A')
            power = device.get('power', 'N/A')
            filter_percent = device.get('filter_percent', 'N/A')
            filter_warning = device.get('filter_warning', 0)
            
            output.append(f"   💧 水量: {water_level}")
            output.append(f"   🔌 电源: {'已插入' if power == 1 else '未插入' if power == 0 else power}")
            output.append(f"   🔴 滤芯: {filter_percent}% {'⚠️ 请更换' if filter_warning == 1 else '✅ 正常'}")
            
        elif dev_type == 'purifier':
            output.append(f"   🪄 净化器在线")
        
        output.append("")
    
    return "\n".join(output)

def main():
    config = load_config()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--configure':
            # 配置账号
            if len(sys.argv) > 3:
                config['username'] = sys.argv[2]
                config['password'] = sys.argv[3]
                save_config(config)
                print(f"✅ 配置已保存: {config['username']}")
            else:
                print("Usage: petkit-monitor.py --configure <username> <password>")
            return
    
    # 检查配置
    if 'username' not in config or 'password' not in config:
        print("❌ 请先配置账号")
        print("Usage: petkit-monitor.py --configure <username> <password>")
        print("\n示例: petkit-monitor.py --configure 18055988330 your_password")
        sys.exit(1)
    
    # 获取状态
    print("🔄 正在获取小佩设备状态...")
    result = asyncio.run(get_petkit_status(config['username'], config['password']))
    print(format_status(result))

if __name__ == "__main__":
    main()
