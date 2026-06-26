#!/usr/bin/env python3
"""
C4Context 架构图生成器 - mermaid-flow v2.0
使用 Mermaid 原生 block 语法（mermaid 10+ 支持）

支持 C4 模型：Context(上下文), Container(容器), Component(组件)
"""

import argparse
import json


# C4 模板 - 使用 Mermaid 原生 flowchart 语法
# 注意：使用 {{ }} 转义花括号
C4_TEMPLATES = {
    'context': '''%%{{init: {{'theme': 'base'}}}}%%
flowchart TD
    subgraph system["📦 {system_name}"]
        style system fill:#E3F2FD,stroke:#1976D2,stroke-width:3px
    end
    
    user[("👤 用户<br/>理财经理")]
    wechat[("💬 企业微信<br/>企业 IM 平台")]
    bailian[("☁️ 阿里云百炼<br/>AI 模型服务")]
    product_db[("🗄️ 产品数据库<br/>金融机构产品库")]
    
    user -->|使用 HTTPS| system
    system -->|集成 API| wechat
    system -->|调用 AI 模型| bailian
    system -->|查询产品| product_db
    
    classDef systemClass fill:#E3F2FD,stroke:#1976D2,stroke-width:3px
    classDef externalClass fill:#FFF3E0,stroke:#F57C00,stroke-width:2px
    classDef userClass fill:#E8F5E9,stroke:#388E3C,stroke-width:2px
    
    class system systemClass
    class wechat,bailian,product_db externalClass
    class user userClass
''',

    'container': '''%%{{init: {{'theme': 'base'}}}}%%
flowchart TD
    user[("👤 用户<br/>理财经理")]
    
    subgraph system["📦 {system_name}"]
        direction TB
        web_app["🌐 Web 应用<br/>Vue3 + TypeScript<br/>对话式交互界面"]
        api["⚙️ API 服务<br/>NestJS<br/>RESTful API"]
        ai_service["🤖 AI 服务<br/>Python<br/>养老测算引擎"]
        database[("💾 数据库<br/>MySQL + MongoDB")]
    end
    
    wechat[("💬 企业微信<br/>企业 IM")]
    bailian[("☁️ 阿里云百炼<br/>AI 模型")]
    
    user -->|使用 HTTPS| web_app
    web_app -->|调用 REST| api
    api -->|调用 RPC| ai_service
    api -->|读写 SQL| database
    ai_service -->|调用模型 API| bailian
    web_app -->|集成 SDK| wechat
    
    classDef systemClass fill:#E3F2FD,stroke:#1976D2,stroke-width:3px
    classDef appClass fill:#E8F5E9,stroke:#388E3C,stroke-width:2px
    classDef dbClass fill:#FFF3E0,stroke:#F57C00,stroke-width:2px
    classDef externalClass fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px
    classDef userClass fill:#E1F5FE,stroke:#0288D1,stroke-width:2px
    
    class system systemClass
    class web_app,api,ai_service appClass
    class database dbClass
    class wechat,bailian externalClass
    class user userClass
''',

    'component': '''%%{{init: {{'theme': 'base'}}}}%%
flowchart TD
    subgraph api["⚙️ API 服务"]
        direction TB
        auth["🔐 认证模块<br/>JWT<br/>用户认证和授权"]
        planner["📊 规划引擎<br/>Python<br/>养老测算和方案生成"]
        recommender["🎯 推荐引擎<br/>ML<br/>产品组合推荐"]
        report["📄 报告生成<br/>PDF<br/>建议书导出"]
    end
    
    auth -->|验证用户 | planner
    planner -->|请求推荐 | recommender
    recommender -->|生成报告 | report
    
    classDef containerClass fill:#E3F2FD,stroke:#1976D2,stroke-width:3px
    classDef componentClass fill:#E8F5E9,stroke:#388E3C,stroke-width:2px
    
    class api containerClass
    class auth,planner,recommender,report componentClass
''',
}


def generate_c4(level: str, output_path: str, title: str = None, system_name: str = None):
    """生成 C4 图"""
    
    if level not in C4_TEMPLATES:
        print(f"❌ 不支持的 C4 级别：{level}")
        print(f"   支持的级别：{', '.join(C4_TEMPLATES.keys())}")
        return False
    
    # 默认值
    if not title:
        title = f"C4 {level.capitalize()} Diagram - AI 养老规划助手"
    if not system_name:
        system_name = "AI 养老规划助手"
    
    # 获取模板并替换变量
    template = C4_TEMPLATES[level]
    content = template.format(title=title, system_name=system_name)
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ C4 {level} 图已生成：{output_path}")
    print(f"   标题：{title}")
    print(f"   系统：{system_name}")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='C4Context 架构图生成器 - mermaid-flow v2.0',
        epilog="""
C4 模型说明:
  context   - 系统上下文图
  container - 容器图
  component - 组件图

示例:
  python c4_generator.py --level context -o c4_context.mmd
  python c4_generator.py --level container -o c4_container.mmd
        """
    )
    
    parser.add_argument('--level', '-l', type=str, required=True,
        choices=['context', 'container', 'component'])
    parser.add_argument('--output', '-o', type=str, required=True)
    parser.add_argument('--title', '-t', type=str, default=None)
    parser.add_argument('--system-name', '-s', type=str, default=None)
    
    args = parser.parse_args()
    
    if generate_c4(args.level, args.output, args.title, args.system_name):
        print(f"\n📊 渲染命令:")
        print(f"   python mermaid_render.py -i {args.output} -o {args.output.replace('.mmd', '.png')} -w 1600 -b white")
        return 0
    return 1


if __name__ == '__main__':
    exit(main())
