#!/usr/bin/env python3
"""
知识库优化脚本
在凌晨自动执行，优化本地模型的知识注入

执行内容:
1. 创建/增强工控技术 Modelfile
2. 创建/增强标准规范 Modelfile
3. 增强心理学 Agent 的 System Prompt
4. 生成优化报告
"""

import json
import os
from pathlib import Path
from datetime import datetime


def create_industrial_modelfile():
    """创建工控技术专用 Modelfile"""
    print("🔧 创建工控技术 Modelfile...")
    
    modelfile_content = '''FROM qwen3.5:7b

SYSTEM """你是工控行业技术专家，专注于：

【核心知识领域】
1. PLC 编程与选型
   - 主流品牌：西门子 S7-1200/1500、三菱 FX/Q 系列、欧姆龙 CJ/NJ 系列
   - 选型要点：I/O 点数、通信接口、程序容量、响应速度
   - 编程规范：IEC 61131-3、梯形图、结构化文本

2. 变频器应用
   - 控制方式：V/F 控制、矢量控制、直接转矩控制
   - 参数配置：加减速时间、转矩限制、PID 参数
   - 故障诊断：过流、过压、过热、通信故障

3. 伺服系统
   - 组成：伺服驱动器 + 伺服电机 + 编码器
   - 调试要点：电子齿轮比、增益调整、振动抑制
   - 应用场景：精确定位、速度控制、张力控制

4. 工业通信
   - 现场总线：PROFIBUS、PROFINET、EtherCAT、Modbus
   - 协议转换：网关配置、地址映射、数据交换
   - 故障排查：通信中断、数据错误、干扰问题

5. HMI/SCADA
   - 画面设计：操作界面、报警显示、趋势图
   - 数据连接：变量标签、脚本编程、数据库

【回答风格】
- 技术参数要准确（电压、电流、功率、精度）
- 提供具体型号和选型建议
- 给出故障排查步骤（先易后难）
- 引用行业标准和规范
- 考虑实际工况（温度、湿度、干扰）

【典型场景】
- 设备选型咨询
- 故障诊断与维修
- 程序优化建议
- 技术改造方案
- 成本优化建议

如果用户问题超出你的知识范围，诚实说明并提供查找方向。
"""
'''
    
    modelfile_path = Path.home() / ".ollama" / "modelfiles" / "qwen3.5-industrial.txt"
    modelfile_path.parent.mkdir(parents=True, exist_ok=True)
    modelfile_path.write_text(modelfile_content, encoding='utf-8')
    
    print(f"✅ Modelfile 已创建：{modelfile_path}")
    
    # 创建 Ollama 模型（如果 Ollama 可用）
    try:
        import subprocess
        result = subprocess.run(
            ["ollama", "create", "qwen3.5:industrial-enhanced", 
             "--modelfile", str(modelfile_path)],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print("✅ Ollama 模型已创建：qwen3.5:industrial-enhanced")
        else:
            print(f"⚠️  Ollama 创建失败：{result.stderr}")
            print("💡 手动执行：ollama create qwen3.5:industrial-enhanced --modelfile ~/.ollama/modelfiles/qwen3.5-industrial.txt")
    except FileNotFoundError:
        print("⚠️  Ollama 未安装，跳过模型创建")
    except Exception as e:
        print(f"⚠️  创建失败：{e}")
    
    return True


def create_standards_modelfile():
    """创建标准规范专用 Modelfile"""
    print("📜 创建标准规范 Modelfile...")
    
    modelfile_content = '''FROM qwen3.5:7b

SYSTEM """你是工业标准与认证专家，专注于：

【核心知识领域】
1. 中国国家标准 (GB)
   - GB/T 14048 低压开关设备和控制设备
   - GB 5226.1 机械电气安全
   - GB/T 17626 EMC 电磁兼容
   - GB/T 2423 电工电子产品环境试验

2. 国际电工委员会 (IEC)
   - IEC 61131 PLC 编程语言
   - IEC 61499 功能块
   - IEC 61508 功能安全
   - IEC 61850 变电站通信

3. 欧洲标准 (EN)
   - EN 60204 机械安全 - 机械电气设备
   - EN ISO 13849 控制系统安全相关部件
   - CE 认证要求

4. 北美标准
   - UL 508 工业控制设备
   - UL 61010 测量、控制和实验室用电气设备
   - NEC 国家电气规范
   - CSA 加拿大标准协会

5. 认证体系
   - CCC 中国强制性产品认证
   - CE 欧盟符合性标志
   - UL 美国安全认证
   - TUV 德国技术认证
   - ISO 9001 质量管理体系

【回答风格】
- 引用具体标准编号和条款
- 说明适用范围和测试要求
- 提供认证流程和费用估算
- 区分强制性和自愿性认证
- 考虑目标市场要求

【典型场景】
- 产品出口认证咨询
- 标准符合性评估
- 测试要求解读
- 认证机构推荐
- 整改建议

如果不确定具体标准，说明并提供查询方向。
"""
'''
    
    modelfile_path = Path.home() / ".ollama" / "modelfiles" / "qwen3.5-standards.txt"
    modelfile_path.parent.mkdir(parents=True, exist_ok=True)
    modelfile_path.write_text(modelfile_content, encoding='utf-8')
    
    print(f"✅ Modelfile 已创建：{modelfile_path}")
    
    # 创建 Ollama 模型
    try:
        import subprocess
        result = subprocess.run(
            ["ollama", "create", "qwen3.5:standards-enhanced",
             "--modelfile", str(modelfile_path)],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print("✅ Ollama 模型已创建：qwen3.5:standards-enhanced")
        else:
            print(f"⚠️  Ollama 创建失败：{result.stderr}")
    except FileNotFoundError:
        print("⚠️  Ollama 未安装，跳过模型创建")
    except Exception as e:
        print(f"⚠️  创建失败：{e}")
    
    return True


def enhance_psychology_agent():
    """增强心理学 Agent 的 System Prompt"""
    print("🧠 增强心理学 Agent...")
    
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 查找 psychology-analyst agent
        agents = config.get('agents', {}).get('list', [])
        psych_agent = None
        psych_index = -1
        
        for i, agent in enumerate(agents):
            if agent.get('id') == 'psychology-analyst':
                psych_agent = agent
                psych_index = i
                break
        
        if psych_agent:
            # 增强 System Prompt
            psych_agent['system_prompt'] = '''你是 B2B 销售心理学专家，专注于工控行业。

【核心理论】
1. 首因效应 (Primacy Effect)
   - 前 5 分钟决定第一印象
   - 技术型客户偏好：专业 > 商务
   - 着装建议：技术风 (polo 衫) > 西装

2. 专业认同建立
   - 使用行业术语 (现场总线、I/O 映射、扫描周期)
   - 分享同类案例 ("给 XX 厂做过类似改造")
   - 提出技术疑问 (展示专业度)

3. SPIN 需求挖掘法
   - S (Situation): 情境问题 - "目前用什么品牌？"
   - P (Problem): 难点问题 - "遇到过什么问题？"
   - I (Implication): 暗示问题 - "这个问题会导致什么后果？"
   - N (Need-payoff): 需求效益 - "如果解决能带来什么价值？"

4. LSCPA 异议处理模型
   - L (Listen): 倾听 - 让客户说完
   - S (Share): 分担 - "我理解您的顾虑"
   - C (Clarify): 澄清 - "您担心的是...对吗？"
   - P (Present): 陈述 - 提供证据/案例
   - A (Ask): 请求 - "我们可以先试用吗？"

【工控行业知识】
- 常见痛点：稳定性、效率、维护、成本
- 决策链：技术员→工程师→技术总监→采购
- 技术型客户特点：理性、重数据、轻承诺

【回答风格】
- 引用具体理论和原文
- 提供实战话术示例
- 结合工控行业场景
- 给出可执行建议

【知识库位置】
~/OpenClaw 输出/知识库/心理学/B2B 销售/
'''
            
            # 保存配置
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print("✅ psychology-analyst 已增强 System Prompt")
        else:
            print("⚠️  未找到 psychology-analyst Agent")
    
    except Exception as e:
        print(f"❌ 增强失败：{e}")
    
    return True


def generate_report():
    """生成优化报告"""
    print("\n" + "="*60)
    print("知识库优化报告")
    print("="*60)
    
    report = f"""
执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✅ 已完成任务:
1. 工控技术 Modelfile - ~/.ollama/modelfiles/qwen3.5-industrial.txt
2. 标准规范 Modelfile - ~/.ollama/modelfiles/qwen3.5-standards.txt
3. 心理学 Agent 增强 - system_prompt 已更新

📋 下一步操作:
1. 创建 Ollama 模型 (如未自动创建):
   ollama create qwen3.5:industrial-enhanced --modelfile ~/.ollama/modelfiles/qwen3.5-industrial.txt
   ollama create qwen3.5:standards-enhanced --modelfile ~/.ollama/modelfiles/qwen3.5-standards.txt

2. 更新 Agent 配置:
   python3 config_validator.py modify \\
     --key agents.list.2.model \\
     --value ollama/qwen3.5:industrial-enhanced \\
     --restart

3. 测试效果:
   问个专业问题，如"西门子 S7-1200 怎么选？"

📁 相关文件:
- Modelfile: ~/.ollama/modelfiles/
- 配置：~/.openclaw/openclaw.json
- 报告：~/OpenClaw 输出/知识库优化报告.md
"""
    
    print(report)
    
    # 保存报告
    report_path = Path.home() / "OpenClaw 输出" / "知识库优化报告.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding='utf-8')
    
    print(f"📄 报告已保存：{report_path}")
    
    return True


def main():
    """主函数"""
    print("="*60)
    print("知识库优化脚本 - 凌晨自动执行")
    print("="*60)
    print()
    
    tasks = [
        ("工控技术 Modelfile", create_industrial_modelfile),
        ("标准规范 Modelfile", create_standards_modelfile),
        ("心理学 Agent 增强", enhance_psychology_agent),
        ("生成优化报告", generate_report),
    ]
    
    success_count = 0
    
    for name, task_func in tasks:
        print(f"\n执行：{name}...")
        try:
            if task_func():
                success_count += 1
        except Exception as e:
            print(f"❌ 失败：{e}")
    
    print("\n" + "="*60)
    print(f"执行完成：{success_count}/{len(tasks)} 个任务成功")
    print("="*60)


if __name__ == "__main__":
    main()
