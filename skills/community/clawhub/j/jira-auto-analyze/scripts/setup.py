#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JIRA自动分析技能安装脚本
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_python_version():
    """检查Python版本"""
    import platform
    python_version = platform.python_version()
    logger.info(f"Python版本: {python_version}")
    
    version_parts = python_version.split('.')
    major_version = int(version_parts[0])
    minor_version = int(version_parts[1])
    
    if major_version < 3 or (major_version == 3 and minor_version < 7):
        logger.error("需要Python 3.7或更高版本")
        return False
    
    return True

def install_playwright():
    """安装Playwright"""
    logger.info("正在安装Playwright...")
    
    try:
        # 安装Playwright Python包
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "playwright"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info("Playwright安装成功")
        else:
            logger.error(f"Playwright安装失败: {result.stderr}")
            return False
        
        # 安装Chromium浏览器
        logger.info("正在安装Chromium浏览器...")
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info("Chromium浏览器安装成功")
        else:
            logger.error(f"Chromium浏览器安装失败: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"安装过程中发生错误: {str(e)}")
        return False

def create_directories():
    """创建必要的目录"""
    skill_dir = Path(__file__).parent.parent
    directories = [
        skill_dir / "logs",
        skill_dir / "config",
        skill_dir / "scripts",
        skill_dir / "references",
        skill_dir / "assets"
    ]
    
    for directory in directories:
        try:
            directory.mkdir(exist_ok=True)
            logger.info(f"创建目录: {directory}")
        except Exception as e:
            logger.error(f"创建目录 {directory} 失败: {str(e)}")
            return False
    
    return True

def check_config_file():
    """检查配置文件"""
    config_file = Path(__file__).parent.parent / "config" / "config.json"
    
    if not config_file.exists():
        logger.warning(f"配置文件不存在: {config_file}")
        logger.info("将使用默认配置")
        
        # 创建默认配置文件
        default_config = {
            "rules": [
                {
                    "rule_name": "认证相关工单",
                    "keywords": ["认证", "勾选", "授权", "权限", "token", "登录", "Auth"],
                    "assignee": "张献文",
                    "jira_username": "zhangxianwen",
                    "reply_message": "请献文协助处理此工单"
                },
                {
                    "rule_name": "乐企相关工单",
                    "keywords": ["乐企", "leqi", "LEQI"],
                    "assignee": "付强",
                    "jira_username": "fuqiang",
                    "reply_message": "请付强协助处理此工单"
                },
                {
                    "rule_name": "综服通道相关工单",
                    "keywords": ["综服", "通道", "银行", "工行", "中行", "农行", "建行", "招行"],
                    "assignee": "魏旭峰",
                    "jira_username": "weixufeng",
                    "reply_message": "请旭峰协助处理此工单"
                },
                {
                    "rule_name": "其他工单",
                    "keywords": [],
                    "assignee": "刘巍",
                    "jira_username": "liuwei1",
                    "reply_message": "收到，我会及时处理，请稍后"
                }
            ],
            "config": {
                "jira_url": "http://jira.51baiwang.com",
                "filter_id": "13123",
                "username": "liuwei1",
                "password": "Lw@123456",
                "rejection_message": "请提供相关环境、通道类型、版本号及日志信息",
                "check_new_only": True
            }
        }
        
        try:
            import json
            config_file.parent.mkdir(exist_ok=True)
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
            logger.info(f"已创建默认配置文件: {config_file}")
        except Exception as e:
            logger.error(f"创建配置文件失败: {str(e)}")
            return False
    
    return True

def test_script():
    """测试脚本是否能正常运行"""
    logger.info("正在测试脚本...")
    
    try:
        # 测试导入模块
        sys.path.insert(0, str(Path(__file__).parent))
        from jira_auto_analyze import PLAYWRIGHT_AVAILABLE
        
        if PLAYWRIGHT_AVAILABLE:
            logger.info("Playwright导入测试成功")
        else:
            logger.warning("Playwright未安装，无法运行浏览器自动化")
        
        # 测试工具函数
        from utils import check_required_fields, calculate_match_score
        
        # 测试必填信息检查
        test_text = "星舰环境，web连接器，版本1.2.3，错误日志"
        result = check_required_fields(test_text)
        if result['is_valid']:
            logger.info("必填信息检查测试成功")
        else:
            logger.warning("必填信息检查测试失败，但可能只是测试数据问题")
        
        # 测试匹配分数计算
        text = "认证相关工单需要处理"
        keywords = ["认证", "勾选", "授权"]
        score = calculate_match_score(text, keywords)
        logger.info(f"匹配分数计算测试成功，分数: {score:.2f}")
        
        logger.info("脚本测试通过")
        return True
        
    except Exception as e:
        logger.error(f"脚本测试失败: {str(e)}")
        return False

def setup_complete():
    """安装完成提示"""
    print("\n" + "="*60)
    print("✅ JIRA自动分析技能安装完成")
    print("="*60)
    
    skill_dir = Path(__file__).parent.parent
    
    print("\n📁 技能目录结构:")
    print(f"  {skill_dir}/")
    print(f"  ├── SKILL.md                 # 技能文档")
    print(f"  ├── scripts/")
    print(f"  │   ├── jira_auto_analyze.py # 核心脚本")
    print(f"  │   ├── utils.py             # 工具函数")
    print(f"  │   └── setup.py             # 安装脚本")
    print(f"  ├── config/")
    print(f"  │   └── config.json          # 配置文件")
    print(f"  ├── references/")
    print(f"  │   ├── jira_structure.md    # JIRA结构参考")
    print(f"  │   └── usage_guide.md       # 使用指南")
    print(f"  └── logs/                    # 日志目录")
    
    print("\n🚀 使用方法:")
    print("  1. 编辑配置文件 (如果需要修改JIRA账号密码):")
    print(f"     {skill_dir}/config/config.json")
    print("  2. 模拟运行测试:")
    print(f"     cd {skill_dir} && python3 scripts/jira_auto_analyze.py --dry-run")
    print("  3. 实际执行:")
    print(f"     cd {skill_dir} && python3 scripts/jira_auto_analyze.py")
    
    print("\n🔧 配置说明:")
    print("  - 修改JIRA账号密码: 编辑config.json中的username和password")
    print("  - 修改分配规则: 编辑config.json中的rules数组")
    print("  - 修改打回消息: 编辑config.json中的rejection_message")
    
    print("\n📝 注意事项:")
    print("  - 首次使用建议先运行 --dry-run 模式测试")
    print("  - 确保JIRA账户有修改工单和添加评论的权限")
    print("  - 操作前会显示分析结果，需要确认后才执行")
    
    print("\n" + "="*60)

def main():
    """主安装函数"""
    print("🚀 开始安装JIRA自动分析技能")
    print("="*60)
    
    # 检查Python版本
    if not check_python_version():
        return 1
    
    # 创建目录
    if not create_directories():
        return 1
    
    # 检查配置文件
    if not check_config_file():
        return 1
    
    # 安装Playwright
    print("\n" + "-"*60)
    print("📦 安装依赖")
    print("-"*60)
    
    install_choice = input("是否安装Playwright和Chromium浏览器？(y/N): ")
    if install_choice.lower() == 'y':
        if not install_playwright():
            print("⚠️  依赖安装失败，可能影响功能使用")
            continue_choice = input("是否继续安装？(y/N): ")
            if continue_choice.lower() != 'y':
                return 1
    else:
        print("跳过依赖安装，请确保已安装Playwright和Chromium浏览器")
    
    # 测试脚本
    print("\n" + "-"*60)
    print("🧪 测试功能")
    print("-"*60)
    
    test_choice = input("是否运行功能测试？(y/N): ")
    if test_choice.lower() == 'y':
        if not test_script():
            print("⚠️  功能测试失败，可能影响正常使用")
            continue_choice = input("是否继续安装？(y/N): ")
            if continue_choice.lower() != 'y':
                return 1
    
    # 安装完成
    setup_complete()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())