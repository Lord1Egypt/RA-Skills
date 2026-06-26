import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import shutil
import os

def generate_fake_data(output_path='data/spare_parts.xlsx', seed=42):
    np.random.seed(seed)
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    parts_info = pd.DataFrame({
        '配件ID': [f'P{i:03d}' for i in range(1, 21)],
        '配件名称': [
            '曳引机', '控制柜', '门机', '导轨', '钢丝绳',
            '缓冲器', '安全钳', '限速器', '对重块', '轿厢',
            '层门', '门锁', '按钮', '显示板', '随行电缆',
            '制动器', '减速器', '传感器', '接触器', '变频器'
        ],
        '规格': [
            '5吨', '32层', '中分', 'T89', 'Φ13mm',
            '液压', '渐进式', '1.5m/s', '500kg', '1000kg',
            '中分', '机械式', '不锈钢', 'LED', '24芯',
            '盘式', '蜗轮', '光电', '380V', '15kW'
        ],
        '单价': np.random.randint(50, 500, 20)
    })
    
    inventory_data = []
    for i in range(1, 21):
        part_id = f'P{i:03d}'
        safety_stock = np.random.randint(10, 30)
        max_stock = safety_stock * np.random.randint(3, 6)
        
        if i <= 3:
            current_stock = 0
        elif i <= 6:
            current_stock = safety_stock - np.random.randint(1, 5)
        elif i <= 10:
            current_stock = max_stock + np.random.randint(1, 10)
        else:
            current_stock = np.random.randint(safety_stock, max_stock)
        
        inventory_data.append({
            '配件ID': part_id,
            '当前库存': current_stock,
            '安全库存': safety_stock,
            '最大库存': max_stock
        })
    
    inventory = pd.DataFrame(inventory_data)
    
    orders_data = []
    start_date = datetime.now() - timedelta(days=90)
    
    for i in range(1, 681):
        part_id = f'P{np.random.randint(1, 21):03d}'
        order_date = start_date + timedelta(days=np.random.randint(0, 90))
        
        base_demand = np.random.randint(1, 5)
        if part_id in ['P001', 'P002', 'P003']:
            if order_date > (datetime.now() - timedelta(days=7)):
                base_demand = base_demand * np.random.randint(3, 6)
        
        quantity = base_demand + np.random.randint(-1, 2)
        quantity = max(1, quantity)
        
        orders_data.append({
            '订单ID': f'ORD{i:06d}',
            '配件ID': part_id,
            '数量': quantity,
            '日期': order_date
        })
    
    orders = pd.DataFrame(orders_data)
    orders = orders.sort_values('日期')
    
    temp_path = output_path + '.tmp'
    with pd.ExcelWriter(temp_path, engine='openpyxl') as writer:
        parts_info.to_excel(writer, sheet_name='配件信息', index=False)
        inventory.to_excel(writer, sheet_name='库存', index=False)
        orders.to_excel(writer, sheet_name='订单历史', index=False)
    
    shutil.move(temp_path, output_path)
    
    print(f'Fake数据生成完成！')
    print(f'配件信息: {len(parts_info)} 条记录')
    print(f'库存: {len(inventory)} 条记录')
    print(f'订单历史: {len(orders)} 条记录')
    
   严重缺货 = len(inventory[inventory['当前库存'] == 0])
    库存不足 = len(inventory[(inventory['当前库存'] > 0) & (inventory['当前库存'] < inventory['安全库存'])])
    库存超量 = len(inventory[inventory['当前库存'] > inventory['最大库存']])
    正常库存 = len(inventory) - 严重缺货 - 库存不足 - 库存超量
    
    print(f'\n数据分布:')
    print(f'  - 严重缺货(库存=0): {严重缺货}个配件 (P001-P003)')
    print(f'  - 库存不足: {库存不足}个配件 (P004-P006)')
    print(f'  - 库存超量: {库存超量}个配件 (P007-P010)')
    print(f'  - 正常库存: {正常库存}个配件 (P011-P020)')
    print(f'  - 需求异常增多: 3个配件 (P001-P003，最近一周)')

if __name__ == '__main__':
    generate_fake_data()