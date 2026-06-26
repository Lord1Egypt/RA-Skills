#!/usr/bin/env python3
"""
技能测试脚本
测试招标项目分析技能的各项功能
"""

import sys
import os
import json
import subprocess

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_configuration():
    """测试配置文件"""
    print("🔧 测试配置文件...")
    
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    
    if not os.path.exists(config_path):
        print("❌ config.json 文件不存在")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        required_sections = ['database', 'skill', 'parsing']
        for section in required_sections:
            if section not in config:
                print(f"❌ 配置缺少必要部分: {section}")
                return False
        
        print("✅ 配置文件测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 配置文件读取失败: {e}")
        return False

def test_dependencies():
    """测试依赖包"""
    print("📦 测试Python依赖包...")
    
    required_packages = ['pandas', 'mysql.connector', 'openpyxl']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'mysql.connector':
                __import__('mysql.connector')
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {', '.join(missing_packages)}")
        print("💡 请运行: pip install pandas mysql-connector-python openpyxl")
        return False
    
    print("✅ 所有依赖包已安装")
    return True

def test_database_connection():
    """测试数据库连接"""
    print("🗄️ 测试数据库连接...")
    
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        import mysql.connector
        from mysql.connector import Error
        
        db_config = config['database']
        connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password']
        )
        
        if connection.is_connected():
            print(f"✅ 数据库连接成功: {db_config['host']}:{db_config['port']}")
            
            # 检查数据库是否存在
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES LIKE %s", (db_config['database'],))
            result = cursor.fetchone()
            
            if result:
                print(f"✅ 数据库存在: {db_config['database']}")
            else:
                print(f"⚠️ 数据库不存在: {db_config['database']}")
                print("💡 将自动创建数据库")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ 数据库连接失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试数据库时出错: {e}")
        return False

def test_scripts():
    """测试脚本文件"""
    print("📜 测试脚本文件...")
    
    scripts_dir = os.path.dirname(__file__)
    required_scripts = ['analyze.py', 'import.py', 'query.py']
    
    for script in required_scripts:
        script_path = os.path.join(scripts_dir, script)
        if not os.path.exists(script_path):
            print(f"❌ 脚本文件不存在: {script}")
            return False
        
        # 检查脚本是否可执行
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                if not first_line.startswith('#!/usr/bin/env python3'):
                    print(f"⚠️ 脚本缺少shebang: {script}")
        except:
            pass
    
    print("✅ 所有脚本文件存在")
    return True

def test_skill_structure():
    """测试技能结构"""
    print("📁 测试技能目录结构...")
    
    skill_dir = os.path.dirname(os.path.dirname(__file__))
    required_files = ['SKILL.md', 'README.md', 'package.json', 'config.json']
    
    for file in required_files:
        file_path = os.path.join(skill_dir, file)
        if not os.path.exists(file_path):
            print(f"❌ 必要文件不存在: {file}")
            return False
    
    # 检查目录结构
    required_dirs = ['scripts', 'references']
    for dir_name in required_dirs:
        dir_path = os.path.join(skill_dir, dir_name)
        if not os.path.exists(dir_path):
            print(f"⚠️ 目录不存在: {dir_name}")
            os.makedirs(dir_path, exist_ok=True)
            print(f"📁 已创建目录: {dir_name}")
    
    print("✅ 技能目录结构完整")
    return True

def create_sample_data():
    """创建示例数据"""
    print("📊 创建示例数据...")
    
    skill_dir = os.path.dirname(os.path.dirname(__file__))
    sample_file = os.path.join(skill_dir, 'references', 'sample_data.xlsx')
    
    try:
        import pandas as pd
        
        # 创建示例数据
        sample_data = [
            {
                "项目名称（统一）": "示例项目1 - 智慧校园建设",
                "发布日期": "2026-03-25",
                "招标单位": "某市教育局",
                "招标估价": "1500000.00",
                "中标公司": "待开标",
                "中标价格（元）": "待开标",
                "省": "江苏省",
                "市": "南京市",
                "县": "鼓楼区",
                "项目级别": "市级",
                "项目类型": "教育信息化",
                "项目分析及后续机会": "智慧校园建设项目，包含网络设备、教学平台等",
                "下一步市场安排建议": "关注后续维护和升级项目"
            },
            {
                "项目名称（统一）": "示例项目2 - 医院信息化系统",
                "发布日期": "2026-03-26",
                "招标单位": "某市人民医院",
                "招标估价": "2800000.00",
                "中标公司": "待开标",
                "中标价格（元）": "待开标",
                "省": "浙江省",
                "市": "杭州市",
                "县": "西湖区",
                "项目级别": "市级",
                "项目类型": "医疗信息化",
                "项目分析及后续机会": "医院HIS系统升级，包含硬件和软件",
                "下一步市场安排建议": "关注医疗数据平台建设"
            }
        ]
        
        df = pd.DataFrame(sample_data)
        df.to_excel(sample_file, index=False)
        
        print(f"✅ 示例数据已创建: {sample_file}")
        return sample_file
        
    except Exception as e:
        print(f"❌ 创建示例数据失败: {e}")
        return None

def run_integration_test():
    """运行集成测试"""
    print("🚀 运行集成测试...")
    
    skill_dir = os.path.dirname(os.path.dirname(__file__))
    sample_file = os.path.join(skill_dir, 'references', 'sample_data.xlsx')
    
    if not os.path.exists(sample_file):
        print("❌ 示例数据文件不存在")
        return False
    
    try:
        # 测试分析功能
        print("\n1. 测试分析功能...")
        analyze_result = subprocess.run(
            ['python3', 'analyze.py', sample_file],
            cwd=os.path.join(skill_dir, 'scripts'),
            capture_output=True,
            text=True
        )
        
        if analyze_result.returncode == 0:
            print("✅ 分析功能测试通过")
        else:
            print(f"❌ 分析功能测试失败: {analyze_result.stderr}")
            return False
        
        # 测试导入功能
        print("\n2. 测试导入功能...")
        import_result = subprocess.run(
            ['python3', 'import.py', sample_file],
            cwd=os.path.join(skill_dir, 'scripts'),
            capture_output=True,
            text=True
        )
        
        if import_result.returncode == 0:
            print("✅ 导入功能测试通过")
        else:
            print(f"❌ 导入功能测试失败: {import_result.stderr}")
            return False
        
        # 测试查询功能
        print("\n3. 测试查询功能...")
        query_result = subprocess.run(
            ['python3', 'query.py', 'all'],
            cwd=os.path.join(skill_dir, 'scripts'),
            capture_output=True,
            text=True
        )
        
        if query_result.returncode == 0:
            print("✅ 查询功能测试通过")
        else:
            print(f"❌ 查询功能测试失败: {query_result.stderr}")
            return False
        
        print("\n🎉 所有集成测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 招标项目分析技能测试套件")
    print("=" * 60)
    
    tests = [
        ("配置测试", test_configuration),
        ("依赖测试", test_dependencies),
        ("数据库测试", test_database_connection),
        ("脚本测试", test_scripts),
        ("结构测试", test_skill_structure),
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed_tests += 1
    
    print(f"\n📊 测试结果: {passed_tests}/{total_tests} 通过")
    
    if passed_tests == total_tests:
        print("\n✅ 基础测试全部通过！")
        
        # 创建示例数据
        sample_file = create_sample_data()
        
        if sample_file:
            # 询问是否运行集成测试
            response = input("\n是否运行集成测试? (y/n): ").strip().lower()
            if response == 'y':
                if run_integration_test():
                    print("\n🎉 技能测试完成，可以发布到ClawHub！")
                else:
                    print("\n⚠️ 集成测试失败，请检查问题")
            else:
                print("\n📝 技能测试完成，可以发布到ClawHub")
        else:
            print("\n⚠️ 无法创建示例数据，请手动测试")
    else:
        print("\n❌ 基础测试失败，请修复问题后再试")
    
    print("\n💡 下一步:")
    print("1. 修改 config.json 中的数据库配置")
    print("2. 更新 SKILL.md 中的作者信息")
    print("3. 运行: clawhub publish 发布技能")

if __name__ == "__main__":
    main()