#!/usr/bin/env python3
"""
数据库查询脚本
提供多种查询方式分析招标数据
"""

import mysql.connector
from mysql.connector import Error
import json
import sys
import os
from datetime import datetime, timedelta
import pandas as pd

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

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
            return connection
            
    except Error as e:
        print(f"❌ 数据库连接失败: {e}")
        return None

def execute_query(connection, query, params=None):
    """执行SQL查询"""
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        cursor.close()
        return results
    except Error as e:
        print(f"❌ 查询执行失败: {e}")
        return []

def display_results(results, title=None):
    """显示查询结果"""
    if not results:
        print("📭 没有找到数据")
        return
    
    if title:
        print(f"\n📊 {title}")
        print("=" * 80)
    
    # 转换为DataFrame以便更好显示
    df = pd.DataFrame(results)
    print(df.to_string(index=False))
    print(f"\n📈 总计: {len(results)} 条记录")

def query_all_projects(connection):
    """查询所有项目"""
    query = """
    SELECT 
        id,
        project_name as '项目名称',
        DATE_FORMAT(publish_date, '%Y-%m-%d') as '发布日期',
        bid_unit as '招标单位',
        FORMAT(bid_estimate, 2) as '招标估价(元)',
        winning_company as '中标公司',
        province as '省',
        city as '市',
        county as '县',
        project_level as '项目级别',
        project_type as '项目类型'
    FROM project_bid_info
    ORDER BY publish_date DESC
    """
    return execute_query(connection, query)

def query_pending_tasks(connection, days=7):
    """查询待办任务"""
    query = """
    SELECT 
        p.project_name as '项目名称',
        t.event_name as '事件名称',
        DATE_FORMAT(t.event_date, '%Y-%m-%d %H:%i') as '时间',
        DATEDIFF(t.event_date, NOW()) as '剩余天数',
        t.event_location as '地点',
        t.remarks as '备注'
    FROM project_timeline t
    JOIN project_bid_info p ON t.project_id = p.id
    WHERE t.status = 'pending'
    AND t.event_date BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL %s DAY)
    ORDER BY t.event_date
    """
    return execute_query(connection, query, (days,))

def query_statistics(connection):
    """查询统计信息"""
    queries = [
        ("项目总数", "SELECT COUNT(*) as count FROM project_bid_info"),
        ("总招标金额", "SELECT FORMAT(SUM(bid_estimate), 2) as total FROM project_bid_info"),
        ("平均招标金额", "SELECT FORMAT(AVG(bid_estimate), 2) as average FROM project_bid_info"),
        ("最大招标金额", "SELECT FORMAT(MAX(bid_estimate), 2) as max_amount FROM project_bid_info"),
        ("待开标项目", "SELECT COUNT(*) as count FROM project_bid_info WHERE winning_company = '待开标'"),
        ("已完成项目", "SELECT COUNT(*) as count FROM project_bid_info WHERE winning_company != '待开标'"),
        ("待办事项", "SELECT COUNT(*) as count FROM project_timeline WHERE status = 'pending'"),
    ]
    
    stats = []
    for name, query in queries:
        result = execute_query(connection, query)
        if result:
            value = list(result[0].values())[0]
            stats.append({"统计项": name, "数值": value})
    
    return stats

def query_by_province(connection, province=None):
    """按省份查询"""
    if province:
        query = """
        SELECT 
            province as '省份',
            COUNT(*) as '项目数量',
            FORMAT(SUM(bid_estimate), 2) as '总金额(元)',
            FORMAT(AVG(bid_estimate), 2) as '平均金额(元)'
        FROM project_bid_info 
        WHERE province = %s
        GROUP BY province
        """
        return execute_query(connection, query, (province,))
    else:
        query = """
        SELECT 
            province as '省份',
            COUNT(*) as '项目数量',
            FORMAT(SUM(bid_estimate), 2) as '总金额(元)',
            FORMAT(AVG(bid_estimate), 2) as '平均金额(元)'
        FROM project_bid_info 
        GROUP BY province
        ORDER BY SUM(bid_estimate) DESC
        """
        return execute_query(connection, query)

def query_high_value_projects(connection, threshold=1000000):
    """查询高价值项目"""
    query = """
    SELECT 
        project_name as '项目名称',
        FORMAT(bid_estimate, 2) as '招标估价(元)',
        province as '省',
        city as '市',
        DATE_FORMAT(publish_date, '%Y-%m-%d') as '发布日期',
        bid_unit as '招标单位'
    FROM project_bid_info 
    WHERE bid_estimate >= %s
    ORDER BY bid_estimate DESC
    """
    return execute_query(connection, query, (threshold,))

def query_today_reminders(connection):
    """查询今日提醒"""
    query = """
    SELECT 
        p.project_name as '项目',
        t.event_name as '事项',
        DATE_FORMAT(t.event_date, '%Y-%m-%d %H:%i') as '时间',
        t.remarks as '备注'
    FROM project_timeline t
    JOIN project_bid_info p ON t.project_id = p.id
    WHERE DATE(t.event_date) = CURDATE()
    AND t.status = 'pending'
    ORDER BY t.event_date
    """
    return execute_query(connection, query)

def export_to_excel(connection, output_path):
    """导出数据到Excel"""
    try:
        # 查询所有项目
        projects = query_all_projects(connection)
        
        if not projects:
            print("📭 没有数据可导出")
            return False
        
        # 转换为DataFrame
        df = pd.DataFrame(projects)
        
        # 保存为Excel
        df.to_excel(output_path, index=False)
        
        print(f"✅ 数据已导出到: {output_path}")
        print(f"📊 导出记录数: {len(df)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 导出失败: {e}")
        return False

def interactive_query(connection):
    """交互式查询界面"""
    while True:
        print("\n📋 查询选项:")
        print("1. 查看所有项目")
        print("2. 查看待办任务")
        print("3. 查看统计信息")
        print("4. 按省份查询")
        print("5. 查看高价值项目(100万以上)")
        print("6. 查看今日提醒")
        print("7. 导出数据到Excel")
        print("8. 自定义SQL查询")
        print("0. 退出")
        
        choice = input("\n请选择操作 (0-8): ").strip()
        
        if choice == '0':
            print("👋 再见！")
            break
        elif choice == '1':
            results = query_all_projects(connection)
            display_results(results, "所有项目")
        elif choice == '2':
            days = input("查看未来几天的待办? (默认7天): ").strip()
            days = int(days) if days.isdigit() else 7
            results = query_pending_tasks(connection, days)
            display_results(results, f"未来{days}天待办任务")
        elif choice == '3':
            stats = query_statistics(connection)
            display_results(stats, "统计信息")
        elif choice == '4':
            province = input("请输入省份 (留空查看所有): ").strip()
            results = query_by_province(connection, province if province else None)
            title = f"{province}的项目" if province else "按省份统计"
            display_results(results, title)
        elif choice == '5':
            threshold = input("请输入金额阈值 (默认1000000): ").strip()
            threshold = int(threshold) if threshold.isdigit() else 1000000
            results = query_high_value_projects(connection, threshold)
            display_results(results, f"高价值项目({threshold:,}元以上)")
        elif choice == '6':
            results = query_today_reminders(connection)
            display_results(results, "今日提醒")
        elif choice == '7':
            output_path = input("请输入输出文件路径 (默认: /tmp/projects_export.xlsx): ").strip()
            output_path = output_path if output_path else "/tmp/projects_export.xlsx"
            export_to_excel(connection, output_path)
        elif choice == '8':
            sql = input("请输入SQL查询语句: ").strip()
            if sql:
                results = execute_query(connection, sql)
                display_results(results, "自定义查询结果")
        else:
            print("⚠️ 无效的选择，请重新输入")

def main():
    """主函数"""
    print("🔍 招标数据查询工具")
    print("=" * 60)
    
    # 加载配置
    config = load_config()
    
    # 连接数据库
    connection = create_database_connection(config)
    if not connection:
        sys.exit(1)
    
    try:
        # 检查命令行参数
        if len(sys.argv) > 1:
            command = sys.argv[1]
            
            if command == 'all':
                results = query_all_projects(connection)
                display_results(results, "所有项目")
            elif command == 'stats':
                stats = query_statistics(connection)
                display_results(stats, "统计信息")
            elif command == 'pending':
                days = sys.argv[2] if len(sys.argv) > 2 else 7
                days = int(days) if str(days).isdigit() else 7
                results = query_pending_tasks(connection, days)
                display_results(results, f"未来{days}天待办任务")
            elif command == 'province':
                province = sys.argv[2] if len(sys.argv) > 2 else None
                results = query_by_province(connection, province)
                title = f"{province}的项目" if province else "按省份统计"
                display_results(results, title)
            elif command == 'highvalue':
                threshold = sys.argv[2] if len(sys.argv) > 2 else 1000000
                threshold = int(threshold) if str(threshold).isdigit() else 1000000
                results = query_high_value_projects(connection, threshold)
                display_results(results, f"高价值项目({threshold:,}元以上)")
            elif command == 'today':
                results = query_today_reminders(connection)
                display_results(results, "今日提醒")
            elif command == 'export':
                output_path = sys.argv[2] if len(sys.argv) > 2 else "/tmp/projects_export.xlsx"
                export_to_excel(connection, output_path)
            else:
                print("未知命令，使用交互模式")
                interactive_query(connection)
        else:
            interactive_query(connection)
            
    finally:
        if connection.is_connected():
            connection.close()
            print("\n🔒 数据库连接已关闭")

if __name__ == "__main__":
    main()