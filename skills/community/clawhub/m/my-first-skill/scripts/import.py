#!/usr/bin/env python3
"""
数据导入脚本
将Excel数据导入MySQL数据库
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
import json
import sys
import os
import re
from datetime import datetime

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_chinese_date(date_str):
    """解析中文日期格式"""
    if pd.isna(date_str) or not date_str:
        return None
    
    try:
        # 尝试多种日期格式
        date_formats = [
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',  # 2026年3月20日
            r'(\d{4})-(\d{1,2})-(\d{1,2})',      # 2026-03-20
            r'(\d{4})/(\d{1,2})/(\d{1,2})',      # 2026/03/20
            r'(\d{4})\.(\d{1,2})\.(\d{1,2})'     # 2026.03.20
        ]
        
        for date_format in date_formats:
            match = re.search(date_format, str(date_str))
            if match:
                year = int(match.group(1))
                month = int(match.group(2))
                day = int(match.group(3))
                return f"{year:04d}-{month:02d}-{day:02d}"
        
        return None
    except:
        return None

def parse_price(price_str):
    """解析价格字符串"""
    if pd.isna(price_str) or not price_str:
        return None
    
    try:
        # 移除逗号和货币符号
        price = str(price_str).replace(',', '').replace('¥', '').replace('￥', '').replace('元', '').strip()
        
        # 如果是"待开标"等文本
        if price in ['待开标', '待定', '未知', 'None', 'null']:
            return None
        
        # 转换为浮点数
        return float(price)
    except:
        return None

def create_database_connection(config):
    """创建数据库连接"""
    try:
        db_config = config['database']
        connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            charset=db_config.get('charset', 'utf8mb4')
        )
        
        if connection.is_connected():
            print(f"✅ 成功连接到数据库: {db_config['database']}")
            return connection
            
    except Error as e:
        print(f"❌ 数据库连接失败: {e}")
        return None

def create_tables_if_not_exist(connection):
    """创建数据表（如果不存在）"""
    try:
        cursor = connection.cursor()
        
        # 创建项目信息表
        create_project_table_sql = """
        CREATE TABLE IF NOT EXISTS project_bid_info (
            id INT AUTO_INCREMENT PRIMARY KEY,
            project_name VARCHAR(500) NOT NULL COMMENT '项目名称',
            publish_date DATE COMMENT '发布日期',
            bid_unit VARCHAR(200) COMMENT '招标单位',
            bid_estimate DECIMAL(15,2) COMMENT '招标估价(元)',
            winning_company VARCHAR(200) DEFAULT '待开标' COMMENT '中标公司',
            winning_price DECIMAL(15,2) DEFAULT NULL COMMENT '中标价格(元)',
            province VARCHAR(50) COMMENT '省',
            city VARCHAR(50) COMMENT '市',
            county VARCHAR(50) COMMENT '县',
            project_level VARCHAR(50) COMMENT '项目级别',
            project_type VARCHAR(100) COMMENT '项目类型',
            project_analysis TEXT COMMENT '项目分析及后续机会',
            market_suggestion TEXT COMMENT '下一步市场安排建议',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            
            INDEX idx_project_name (project_name(100)),
            INDEX idx_publish_date (publish_date),
            INDEX idx_bid_unit (bid_unit),
            INDEX idx_province (province),
            INDEX idx_city (city),
            INDEX idx_project_level (project_level)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='招标项目信息表'
        """
        cursor.execute(create_project_table_sql)
        
        # 创建时间节点表
        create_timeline_table_sql = """
        CREATE TABLE IF NOT EXISTS project_timeline (
            id INT AUTO_INCREMENT PRIMARY KEY,
            project_id INT,
            event_name VARCHAR(100) NOT NULL COMMENT '事件名称',
            event_date DATETIME COMMENT '事件时间',
            event_location VARCHAR(200) COMMENT '事件地点',
            remarks TEXT COMMENT '备注',
            status VARCHAR(20) DEFAULT 'pending' COMMENT '状态: pending/completed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (project_id) REFERENCES project_bid_info(id) ON DELETE CASCADE,
            INDEX idx_event_date (event_date),
            INDEX idx_status (status)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='项目时间节点表'
        """
        cursor.execute(create_timeline_table_sql)
        
        print("✅ 数据表创建/验证完成")
        cursor.close()
        
    except Error as e:
        print(f"❌ 创建表失败: {e}")

def import_excel_data(connection, file_path, config):
    """导入Excel数据到数据库"""
    try:
        print(f"📖 正在读取Excel文件: {file_path}")
        
        # 读取Excel文件
        df = pd.read_excel(file_path)
        print(f"✅ 读取成功，共 {len(df)} 条记录")
        
        cursor = connection.cursor()
        imported_count = 0
        updated_count = 0
        
        # 字段映射配置（可以从config.json读取）
        field_mapping = {
            'project_name': '项目名称（统一）',
            'publish_date': '发布日期',
            'bid_unit': '招标单位',
            'bid_estimate': '招标估价',
            'winning_company': '中标公司',
            'winning_price': '中标价格（元）',
            'province': '省',
            'city': '市',
            'county': '县',
            'project_level': '项目级别',
            'project_type': '项目类型',
            'project_analysis': '项目分析及后续机会',
            'market_suggestion': '下一步市场安排建议'
        }
        
        # 处理每一行数据
        for index, row in df.iterrows():
            try:
                # 提取数据
                project_name = row.get(field_mapping['project_name'], '')
                
                if not project_name or pd.isna(project_name):
                    print(f"⚠️ 第 {index+1} 行缺少项目名称，跳过")
                    continue
                
                # 检查是否已存在
                check_sql = "SELECT id FROM project_bid_info WHERE project_name = %s"
                cursor.execute(check_sql, (project_name,))
                existing = cursor.fetchone()
                
                # 准备数据
                publish_date = parse_chinese_date(row.get(field_mapping['publish_date']))
                bid_estimate = parse_price(row.get(field_mapping['bid_estimate']))
                winning_price = parse_price(row.get(field_mapping['winning_price']))
                
                data = (
                    project_name,
                    publish_date,
                    row.get(field_mapping['bid_unit'], ''),
                    bid_estimate,
                    row.get(field_mapping['winning_company'], '待开标'),
                    winning_price,
                    row.get(field_mapping['province'], ''),
                    row.get(field_mapping['city'], ''),
                    row.get(field_mapping['county'], ''),
                    row.get(field_mapping['project_level'], ''),
                    row.get(field_mapping['project_type'], ''),
                    row.get(field_mapping['project_analysis'], ''),
                    row.get(field_mapping['market_suggestion'], '')
                )
                
                if existing:
                    # 更新现有记录
                    update_sql = """
                    UPDATE project_bid_info SET
                        publish_date = %s,
                        bid_unit = %s,
                        bid_estimate = %s,
                        winning_company = %s,
                        winning_price = %s,
                        province = %s,
                        city = %s,
                        county = %s,
                        project_level = %s,
                        project_type = %s,
                        project_analysis = %s,
                        market_suggestion = %s,
                        updated_at = NOW()
                    WHERE project_name = %s
                    """
                    cursor.execute(update_sql, data + (project_name,))
                    updated_count += 1
                    project_id = existing[0]
                else:
                    # 插入新记录
                    insert_sql = """
                    INSERT INTO project_bid_info (
                        project_name, publish_date, bid_unit, bid_estimate,
                        winning_company, winning_price, province, city, county,
                        project_level, project_type, project_analysis, market_suggestion
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_sql, data)
                    project_id = cursor.lastrowid
                    imported_count += 1
                
                # 插入时间节点数据（示例）
                if not existing:
                    insert_timeline_data(cursor, project_id, project_name)
                
                if (index + 1) % 10 == 0:
                    print(f"📊 已处理 {index + 1}/{len(df)} 条记录")
                    
            except Exception as e:
                print(f"❌ 处理第 {index+1} 行数据失败: {e}")
                continue
        
        # 提交事务
        connection.commit()
        
        print(f"\n✅ 数据导入完成！")
        print(f"📥 新增记录: {imported_count} 条")
        print(f"🔄 更新记录: {updated_count} 条")
        print(f"📊 总计处理: {imported_count + updated_count} 条")
        
        cursor.close()
        return True
        
    except Exception as e:
        print(f"❌ 导入数据失败: {e}")
        connection.rollback()
        return False

def insert_timeline_data(cursor, project_id, project_name):
    """插入时间节点数据"""
    try:
        # 基于项目信息创建默认时间节点
        timeline_data = [
            ("获取招标文件", "2026-03-20 08:30:00", "招标代理机构", "电话报名确认", "pending"),
            ("获取招标文件截止", "2026-03-30 17:00:00", "招标代理机构", "只剩6天", "pending"),
            ("投标截止", "2026-04-10 09:30:00", "招标代理机构", "北京时间", "pending"),
            ("开标", "2026-04-10 09:30:00", "招标代理机构二楼开标室", "与投标截止同时", "pending"),
        ]
        
        insert_sql = """
        INSERT INTO project_timeline (project_id, event_name, event_date, event_location, remarks, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        for event in timeline_data:
            cursor.execute(insert_sql, (project_id, *event))
        
    except Exception as e:
        print(f"⚠️ 插入时间节点失败: {e}")

def main():
    """主函数"""
    print("🚀 招标数据导入工具")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("使用方法: python import.py <Excel文件路径>")
        print("示例: python import.py /path/to/bid_file.xlsx")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        sys.exit(1)
    
    # 加载配置
    config = load_config()
    
    # 连接数据库
    connection = create_database_connection(config)
    if not connection:
        sys.exit(1)
    
    try:
        # 创建表
        create_tables_if_not_exist(connection)
        
        # 导入数据
        success = import_excel_data(connection, file_path, config)
        
        if success:
            print("\n🎉 导入成功！")
            print("\n下一步操作:")
            print("1. 运行 query.py 查询导入的数据")
            print("2. 运行 analyze.py 分析更多文件")
            print("3. 查看数据库: SELECT * FROM project_bid_info")
        else:
            print("\n❌ 导入失败")
            
    finally:
        if connection.is_connected():
            connection.close()
            print("\n🔒 数据库连接已关闭")

if __name__ == "__main__":
    main()