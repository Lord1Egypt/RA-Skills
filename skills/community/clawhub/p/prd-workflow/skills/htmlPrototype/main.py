#!/usr/bin/env python3
"""
HTML Prototype Generator - Main Entry Point

Usage:
    python3 main.py "创建一个产品列表页"
    python3 main.py --page list --output ~/Desktop/prototype
    python3 main.py "产品原型" --design-tokens design.json
"""

import sys
import os
import argparse
import json
from pathlib import Path
from datetime import datetime

# 添加路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from generator.templates import get_template, apply_design_tokens
from parser.requirement_parser import parse_requirement_doc, RequirementParser

def generate_html(page_type: str, keywords: list = None, design_tokens: dict = None) -> str:
    """生成 HTML，支持设计系统注入"""
    template = get_template(page_type)

    html = template
    if keywords:
        if '产品' in keywords:
            html = html.replace('管理系统', '产品管理系统')
            html = html.replace('列表', '产品列表')
        elif '用户' in keywords:
            html = html.replace('管理系统', '用户管理系统')
        elif '订单' in keywords:
            html = html.replace('管理系统', '订单管理系统')

    # 应用设计系统
    if design_tokens:
        html = apply_design_tokens(html, design_tokens)

    return html

def load_design_tokens(tokens_path: str) -> dict:
    """加载设计系统 JSON 文件"""
    try:
        with open(tokens_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ 无法加载设计系统：{e}")
        return None

from screenshot.capture import screenshot

# 页面类型映射（v2.8.6 扩展）
PAGE_TYPES = {
    'list': '列表页',
    'form': '表单页',
    'dashboard': '仪表盘',
    'detail': '详情页',
    'login': '登录页',
    'landing': '落地页',
    'checkout': '支付页'
}

def parse_user_input(user_input: str, doc_file: str = None) -> dict:
    """
    解析用户输入
    
    Args:
        user_input: 用户输入文本
        doc_file: 需求文档路径（可选）
    
    Returns:
        解析结果
    """
    # 如果有文档文件，优先从文档解析
    if doc_file:
        try:
            print(f"\n📄 正在读取需求文档：{doc_file}")
            doc_result = parse_requirement_doc(doc_file)
            
            return {
                'page_type': doc_result['page_type'],
                'keywords': doc_result['keywords'],
                'components': doc_result['components'],
                'features': doc_result['features'],
                'style': doc_result['style_preference'],
                'original_input': f"[文档] {doc_file}",
                'source_file': doc_file,
                'suggestions': doc_result.get('suggestions', [])
            }
        except Exception as e:
            print(f"⚠️ 文档解析失败：{e}，回退到文本解析")
    
    # 从文本解析
    input_lower = user_input.lower()
    
    # 检测页面类型（v2.8.6 扩展）
    page_type = 'list'  # 默认
    if '列表' in input_lower or 'list' in input_lower:
        page_type = 'list'
    elif '表单' in input_lower or 'form' in input_lower or '填写' in input_lower:
        page_type = 'form'
    elif '仪表' in input_lower or 'dashboard' in input_lower or '看板' in input_lower:
        page_type = 'dashboard'
    elif '详情' in input_lower or 'detail' in input_lower:
        page_type = 'detail'
    elif '登录' in input_lower or 'login' in input_lower or '认证' in input_lower:
        page_type = 'login'
    elif '落地' in input_lower or 'landing' in input_lower or '营销' in input_lower:
        page_type = 'landing'
    elif '支付' in input_lower or 'checkout' in input_lower or '结算' in input_lower or '收银' in input_lower:
        page_type = 'checkout'
    
    # 提取关键词
    keywords = []
    if '产品' in user_input:
        keywords.append('产品')
    if '用户' in user_input:
        keywords.append('用户')
    if '订单' in user_input:
        keywords.append('订单')
    if '销售' in user_input or '电商' in user_input:
        keywords.append('电商')
    
    return {
        'page_type': page_type,
        'keywords': keywords,
        'original_input': user_input
    }

def generate_clarifying_questions(parsed: dict) -> list:
    """
    生成澄清问题列表
    
    Args:
        parsed: 解析后的用户需求
    
    Returns:
        问题列表
    """
    page_type = parsed['page_type']
    keywords = parsed['keywords']
    
    questions = []
    
    # 通用问题
    questions.append({
        'id': 'style',
        'question': '您希望使用什么风格？\n1️⃣ 现代简约（默认）\n2️⃣ 商务专业\n3️⃣ 活泼清新',
        'default': '1'
    })
    
    # 根据页面类型提问
    if page_type == 'list':
        questions.append({
            'id': 'columns',
            'question': '表格需要显示哪些列？（用逗号分隔，例如：名称，价格，库存，状态）',
            'default': '名称，价格，状态，创建时间，操作'
        })
        questions.append({
            'id': 'filters',
            'question': '需要哪些筛选条件？\n1️⃣ 搜索框\n2️⃣ 下拉选择\n3️⃣ 日期选择\n4️⃣ 都需要（默认）',
            'default': '4'
        })
        questions.append({
            'id': 'actions',
            'question': '需要哪些操作按钮？\n1️⃣ 新建\n2️⃣ 导出\n3️⃣ 批量删除\n4️⃣ 都需要（默认）',
            'default': '4'
        })
    
    elif page_type == 'form':
        questions.append({
            'id': 'fields',
            'question': '表单需要哪些字段？（用逗号分隔，例如：名称，编码，价格，描述）',
            'default': '名称，编码，价格，描述'
        })
        questions.append({
            'id': 'buttons',
            'question': '底部按钮？\n1️⃣ 保存 + 取消（默认）\n2️⃣ 提交 + 重置\n3️⃣ 只有保存',
            'default': '1'
        })
    
    elif page_type == 'dashboard':
        questions.append({
            'id': 'stats',
            'question': '需要几个数据卡片？\n1️⃣ 4 个（默认）\n2️⃣ 6 个\n3️⃣ 8 个',
            'default': '1'
        })
        questions.append({
            'id': 'charts',
            'question': '需要哪些图表？\n1️⃣ 折线图 + 饼图（默认）\n2️⃣ 柱状图\n3️⃣ 只要数据卡片',
            'default': '1'
        })

    elif page_type == 'landing':
        questions.append({
            'id': 'hero_style',
            'question': 'Hero 区域风格？\n1️⃣ 大标题 + CTA（默认）\n2️⃣ 图片 + 文案\n3️⃣ 视频 + 文案',
            'default': '1'
        })
        questions.append({
            'id': 'cta_text',
            'question': 'CTA 按钮文案？（例如：立即体验、免费注册）',
            'default': '立即体验'
        })
        questions.append({
            'id': 'sections',
            'question': '需要哪些区块？\n1️⃣ 特性 + 价格 + FAQ（默认）\n2️⃣ 特性 + 案例\n3️⃣ 只要特性',
            'default': '1'
        })

    elif page_type == 'checkout':
        questions.append({
            'id': 'payment_methods',
            'question': '支付方式？\n1️⃣ 支付宝 + 微信（默认）\n2️⃣ 银行卡\n3️⃣ 全部',
            'default': '1'
        })
        questions.append({
            'id': 'order_summary',
            'question': '订单摘要显示？\n1️⃣ 商品 + 价格 + 总计（默认）\n2️⃣ 简洁版\n3️⃣ 详细版（含优惠）',
            'default': '1'
        })
    
    # 根据业务领域提问
    if '产品' in keywords:
        questions.append({
            'id': 'product_type',
            'question': '产品类型？\n1️⃣ 实物商品（默认）\n2️⃣ 虚拟商品\n3️⃣ 服务',
            'default': '1'
        })
    elif '用户' in keywords:
        questions.append({
            'id': 'user_type',
            'question': '用户类型？\n1️⃣ 普通用户（默认）\n2️⃣ 企业用户\n3️⃣ 混合',
            'default': '1'
        })
    
    return questions

def collect_answers(questions: list) -> dict:
    """
    收集用户回答（交互式）
    
    Args:
        questions: 问题列表
    
    Returns:
        答案字典
    """
    answers = {}
    
    print("\n" + "=" * 60)
    print("📋 让我问几个问题，帮您更好地定制原型：")
    print("=" * 60)
    
    for i, q in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}] {q['question']}")
        
        # 模拟用户输入（实际使用时从命令行读取）
        try:
            answer = input("您的选择 [回车使用默认]: ").strip()
        except EOFError:
            answer = ''
        
        if not answer:
            answer = q['default']
        
        answers[q['id']] = answer
    
    print("\n✅ 好的，马上为您生成！")
    print("=" * 60 + "\n")
    
    return answers

def apply_answers(template_html: str, answers: dict, page_type: str) -> str:
    """
    根据答案应用定制
    
    Args:
        template_html: 模板 HTML
        answers: 用户答案
        page_type: 页面类型
    
    Returns:
        定制后的 HTML
    """
    html = template_html
    
    # 应用风格选择
    if answers.get('style') == '2':
        # 商务专业风格（蓝色系）
        html = html.replace('#667eea', '#2c5282')
        html = html.replace('#764ba2', '#2b6cb0')
    elif answers.get('style') == '3':
        # 活泼清新风格（绿色系）
        html = html.replace('#667eea', '#38a169')
        html = html.replace('#764ba2', '#48bb78')
    
    # 应用表格列定制
    if page_type == 'list' and answers.get('columns'):
        # 这里可以根据用户选择的列动态生成表头
        # 简化版本：保持默认
        pass

    # 应用落地页定制（v2.8.6 新增）
    if page_type == 'landing':
        # Hero 风格
        if answers.get('hero_style') == '2':
            html = html.replace('Hero 大标题', '图片 + 文案 Hero')
        elif answers.get('hero_style') == '3':
            html = html.replace('Hero 大标题', '视频 + 文案 Hero')

        # CTA 文案
        cta_text = answers.get('cta_text', '立即体验')
        html = html.replace('立即体验', cta_text)
        html = html.replace('免费注册', cta_text)

    # 应用支付页定制（v2.8.6 新增）
    if page_type == 'checkout':
        # 支付方式
        if answers.get('payment_methods') == '2':
            html = html.replace('支付宝', '银行卡')
            html = html.replace('微信支付', '银联支付')
        elif answers.get('payment_methods') == '3':
            # 全部支付方式已包含
            pass
    
    return html

def get_output_path(page_type: str, custom_output: str = None) -> tuple:
    """获取输出路径"""
    if custom_output:
        output_dir = Path(custom_output).parent
        base_name = Path(custom_output).stem
    else:
        # 默认输出到桌面
        output_dir = Path.home() / "Desktop"
        base_name = f"prototype_{page_type}"
    
    html_path = output_dir / f"{base_name}.html"
    png_path = output_dir / f"{base_name}.png"
    
    return html_path, png_path

def main():
    parser = argparse.ArgumentParser(description="HTML 原型生成器")
    parser.add_argument("input", nargs="?", help="用户描述，例如：'创建一个产品列表页'")
    parser.add_argument("--page", "-p", choices=['list', 'form', 'dashboard', 'detail', 'login', 'landing', 'checkout'],
                       help="页面类型（可选，自动检测）")
    parser.add_argument("--output", "-o", help="输出文件路径（不含扩展名）")
    parser.add_argument("--no-screenshot", action="store_true", help="不生成截图")
    parser.add_argument("--width", type=int, default=1440, help="截图宽度")
    parser.add_argument("--height", type=int, default=900, help="截图高度")
    parser.add_argument("--open", action="store_true", help="生成后自动打开 HTML")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式（多轮问答）")
    parser.add_argument("--doc", "-d", help="需求文档路径（.md/.txt/.docx）")

    # ⭐ 新增：设计系统参数
    parser.add_argument("--design-tokens", "-t", help="设计系统 JSON 文件路径")
    parser.add_argument("--primary-color", help="主色调（例如：#1677FF）")
    parser.add_argument("--secondary-color", help="辅助色")
    parser.add_argument("--font-family", help="字体（例如：system-ui）")

    args = parser.parse_args()
    
    # 检查输入
    if not args.input and not args.doc:
        print("❌ 请提供页面描述或需求文档")
        print("示例：")
        print("  python3 main.py '创建一个产品列表页'")
        print("  python3 main.py --doc requirements.md")
        print("  python3 main.py '补充说明' --doc requirements.md")
        sys.exit(1)
    
    print(f"🎨 正在生成原型...")
    
    # 解析用户输入（支持文档）
    parsed = parse_user_input(args.input or "", args.doc)
    
    if args.doc:
        print(f"📄 源文件：{args.doc}")
    else:
        print(f"📝 描述：{args.input}")
    
    page_type = args.page or parsed['page_type']
    
    print(f"📄 类型：{PAGE_TYPES.get(page_type, page_type)}")
    
    # 显示解析结果
    if 'source_file' in parsed:
        print(f"\n📋 从文档提取:")
        print(f"   关键词：{', '.join(parsed.get('keywords', []))}")
        print(f"   组件：{', '.join(parsed.get('components', []))}")
        print(f"   功能：{', '.join(parsed.get('features', []))}")
        
        if parsed.get('suggestions'):
            print(f"\n💡 建议:")
            for sug in parsed['suggestions'][:3]:
                print(f"   - {sug}")
    
    # 交互模式：多轮问答
    answers = {}
    if args.interactive:
        questions = generate_clarifying_questions(parsed)
        answers = collect_answers(questions)

    # ⭐ 新增：加载设计系统
    design_tokens = None

    # 优先级 1：从 JSON 文件加载
    if args.design_tokens:
        design_tokens = load_design_tokens(args.design_tokens)
        if design_tokens:
            print(f"✅ 加载设计系统：{args.design_tokens}")

    # 优先级 2：从命令行参数构建
    if not design_tokens and (args.primary_color or args.font_family):
        design_tokens = {
            'colors': {
                'primary': args.primary_color or '#667eea',
                'secondary': args.secondary_color or '#764ba2',
            },
            'typography': {
                'fontFamily': args.font_family or 'system-ui, -apple-system, sans-serif'
            }
        }
        print(f"✅ 使用命令行设计系统：主色={design_tokens['colors']['primary']}")

    # 生成 HTML
    print("\n📄 生成 HTML...")
    html_content = generate_html(page_type, parsed['keywords'], design_tokens)
    
    # 应用用户答案
    if answers:
        print("🎨 应用定制选项...")
        html_content = apply_answers(html_content, answers, page_type)
    
    # 获取输出路径
    html_path, png_path = get_output_path(page_type, args.output)
    
    # 保存 HTML
    html_path.parent.mkdir(parents=True, exist_ok=True)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML 已保存：{html_path}")
    print(f"📁 文件大小：{html_path.stat().st_size / 1024:.1f} KB")
    
    # 生成截图
    if not args.no_screenshot:
        print("\n📸 生成截图...")
        try:
            success = screenshot(str(html_path), str(png_path), 
                               width=args.width, height=args.height)
            if success:
                print(f"✅ 截图已保存：{png_path}")
                print(f"📁 文件大小：{png_path.stat().st_size / 1024:.1f} KB")
        except Exception as e:
            print(f"⚠️ 截图失败：{e}")
            print("💡 可以手动打开 HTML 文件截图")
    
    # 自动打开
    if args.open:
        print(f"\n🌐 打开 HTML...")
        os.system(f"open {html_path}")
    
    # 完成总结
    print("\n" + "=" * 60)
    print("✅ 原型生成完成！")
    print("=" * 60)
    print(f"📄 HTML: {html_path}")
    if not args.no_screenshot:
        print(f"🖼️  截图：{png_path}")
    print("\n💡 提示:")
    print(f"   - 用浏览器打开：open {html_path}")
    print(f"   - 在 Framer 中参考此原型")
    print("=" * 60)

if __name__ == "__main__":
    main()
