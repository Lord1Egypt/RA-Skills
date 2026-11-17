#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模板库管理器 - 多Agent协作编排引擎 v5.5

功能：预置流水线模板的注册、探测、渲染 + newbie 向导
- 预置 10 类高频流水线模板（政采日报/视频分析/周报/巡检/竞对监控/发票批量/文件整理/考试刷题/直播复盘/知识库周更）
- 模板元数据声明建议安装的外部 skill + 三要素声明（耗时/依赖/产物）
- 运行时探测依赖 skill 是否存在，缺失则标灰 + 附安装链接
- 绝不自动安装或隐式依赖，保持单包合规
- newbie 向导：交互式选模板 → 填参数 → dry-run 预览 → 确认生成

零第三方依赖，仅使用 Python 标准库
"""

import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'templates')


def _load_template(template_path):
    """加载模板 JSON 文件"""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def _check_skill_available(skill_id):
    """
    检查外部 skill 是否已安装。

    探测方式（按优先级）：
    1. 检查 ~/.workbuddy/skills/<skill_id>/SKILL.md 是否存在
    2. 检查当前工作区 .workbuddy/skills/<skill_id>/SKILL.md 是否存在
    3. 尝试 import 对应的 Python 模块（如 skill_id 可映射为模块名）

    返回 (bool, str) - (是否可用, 探测依据说明)
    """
    # 检查用户级 skill 目录
    home_skills_dir = os.path.expanduser('~/.workbuddy/skills')
    skill_path = os.path.join(home_skills_dir, skill_id, 'SKILL.md')
    if os.path.exists(skill_path):
        return True, f'已安装（用户级：{skill_path}）'

    # 检查工作区级 skill 目录
    workspace_dir = os.environ.get('WORKSPACE_DIR', '')
    if workspace_dir:
        workspace_skill_path = os.path.join(workspace_dir, '.workbuddy', 'skills', skill_id, 'SKILL.md')
        if os.path.exists(workspace_skill_path):
            return True, f'已安装（工作区级）'

    # 尝试 import（如果 skill_id 可映射为 Python 模块）
    try:
        __import__(skill_id.replace('-', '_'))
        return True, '已安装（Python 模块可导入）'
    except ImportError:
        pass

    return False, '未安装'


def list_templates():
    """列出所有可用的预置模板"""
    if not os.path.exists(TEMPLATES_DIR):
        print("模板目录不存在")
        return []

    templates = []
    for fname in os.listdir(TEMPLATES_DIR):
        if not fname.endswith('.json') or fname == 'template_schema.json' or fname == 'state_schema.json':
            continue
        if fname in ('pipeline_dag_template.json', 'control_flow_template.json',
                     'sub_pipeline_template.json', 'parent_pipeline_template.json'):
            continue

        fpath = os.path.join(TEMPLATES_DIR, fname)
        tpl = _load_template(fpath)
        if tpl and 'name' in tpl:
            three_elems = tpl.get('three_elements', {})
            templates.append({
                'file': fname,
                'name': tpl.get('name', ''),
                'description': tpl.get('description', ''),
                'category': tpl.get('category', ''),
                'version': tpl.get('version', ''),
                'tags': tpl.get('tags', []),
                'dependency_count': len(tpl.get('dependencies', [])),
                'time_estimate': three_elems.get('time_estimate', '-'),
                'api_key_required': three_elems.get('api_key_required', '-'),
                'output_files': three_elems.get('output_files', []),
            })

    return templates


def show_template(template_file):
    """显示模板详细信息 + 依赖状态 + 三要素"""
    fpath = os.path.join(TEMPLATES_DIR, template_file)
    tpl = _load_template(fpath)

    if not tpl:
        print(f"错误：无法加载模板文件 {template_file}")
        return

    print("=" * 60)
    print(f"  模板：{tpl.get('name', '未命名')}")
    print("=" * 60)
    print(f"  描述：{tpl.get('description', '无描述')}")
    print(f"  分类：{tpl.get('category', '未分类')}")
    print(f"  版本：{tpl.get('version', '未知')}")
    print(f"  标签：{', '.join(tpl.get('tags', []))}")
    print()

    # 三要素展示
    three_elems = tpl.get('three_elements', {})
    if three_elems:
        print("  ┌─────────────────────────────────────")
        print(f"  │ ⏱️  耗时预估：{three_elems.get('time_estimate', '-')}")
        print(f"  │ 🔑 API Key：{three_elems.get('api_key_required', '-')}")
        outputs = three_elems.get('output_files', [])
        if outputs:
            print(f"  │ 📄 产物清单：{', '.join(outputs)}")
        print("  └─────────────────────────────────────")
        print()

    # 依赖检查
    deps = tpl.get('dependencies', [])
    if deps:
        print("  依赖 skill（建议安装，非强制）：")
        for dep in deps:
            skill_id = dep.get('skill_id', '')
            desc = dep.get('description', '')
            install_link = dep.get('install_link', '')
            required = dep.get('required', False)

            available, reason = _check_skill_available(skill_id)
            status_icon = '✅' if available else '⚠️'
            req_tag = ' [必需]' if required else ' [可选]'

            print(f"    {status_icon} [{skill_id}]{req_tag}")
            print(f"      用途：{desc}")
            if not available:
                print(f"      安装：{install_link}")
                print(f"      状态：缺失 — 对应节点将标灰，可先安装后重新运行")
            else:
                print(f"      状态：{reason}")
            print()
    else:
        print("  无外部依赖")
        print()

    # 流水线结构预览
    pipeline = tpl.get('pipeline', {})
    agents = pipeline.get('agents', [])
    if agents:
        print("  流水线节点：")
        for i, agent in enumerate(agents, 1):
            aid = agent.get('id', '')
            name = agent.get('name', '')
            atype = agent.get('type', 'task')
            role = agent.get('role', '')
            print(f"    {i}. [{aid}] {name} (type: {atype})")
            print(f"       角色：{role}")
            if i < len(agents):
                print(f"       ↓")
        print()

    print(f"  模板文件：{fpath}")
    print("=" * 60)


def check_dependencies(template_file):
    """
    检查模板依赖是否全部满足。

    返回：
    - missing_required: 缺失的必需依赖列表
    - missing_optional: 缺失的可选依赖列表
    """
    fpath = os.path.join(TEMPLATES_DIR, template_file)
    tpl = _load_template(fpath)

    if not tpl:
        return [], []

    missing_required = []
    missing_optional = []

    for dep in tpl.get('dependencies', []):
        skill_id = dep.get('skill_id', '')
        required = dep.get('required', False)
        install_link = dep.get('install_link', '')
        desc = dep.get('description', '')

        available, _ = _check_skill_available(skill_id)
        if not available:
            item = {
                'skill_id': skill_id,
                'description': desc,
                'install_link': install_link,
            }
            if required:
                missing_required.append(item)
            else:
                missing_optional.append(item)

    return missing_required, missing_optional


def render_pipeline(template_file, check_deps=True):
    """
    渲染模板为可执行的 pipeline.json 格式。
    """
    fpath = os.path.join(TEMPLATES_DIR, template_file)
    tpl = _load_template(fpath)

    if not tpl:
        print(f"错误：无法加载模板文件 {template_file}")
        return None

    pipeline = tpl.get('pipeline', {})
    if not pipeline:
        print(f"错误：模板 {template_file} 缺少 pipeline 定义")
        return None

    if check_deps and tpl.get('dependencies'):
        missing_required, missing_optional = check_dependencies(template_file)
        if missing_required or missing_optional:
            print()
            print("⚠️  依赖检查结果：")
            if missing_required:
                print(f"  缺失必需依赖：{', '.join(d['skill_id'] for d in missing_required)}")
            if missing_optional:
                print(f"  缺失可选依赖：{', '.join(d['skill_id'] for d in missing_optional)}")
            print("  对应节点将在执行时标灰并提示安装，不会自动安装")
            print()

    return pipeline


def validate_template(template_file):
    """
    CI 校验：检查模板是否符合 schema 规范（三要素齐全 + 结构完整）。
    返回 (is_valid, errors_list)
    """
    fpath = os.path.join(TEMPLATES_DIR, template_file)
    tpl = _load_template(fpath)

    if not tpl:
        return False, [f"无法加载模板文件 {template_file}"]

    errors = []

    # 检查必需字段
    for field in ['name', 'description', 'category', 'version']:
        if field not in tpl:
            errors.append(f"缺少必需字段: {field}")

    # 检查三要素
    three_elems = tpl.get('three_elements', {})
    if not three_elems:
        errors.append("缺少三要素声明 (three_elements)")
    else:
        for field in ['time_estimate', 'api_key_required', 'output_files']:
            if field not in three_elems:
                errors.append(f"三要素缺少字段: {field}")

    # 检查 pipeline 结构
    pipeline = tpl.get('pipeline', {})
    if not pipeline:
        errors.append("缺少 pipeline 定义")
    elif 'agents' not in pipeline or not pipeline['agents']:
        errors.append("pipeline 缺少 agents 列表")

    return len(errors) == 0, errors


def newbie_wizard():
    """
    newbie 向导：交互式问答（选模板 → 填参数 → dry-run 预览 → 确认生成）
    """
    print()
    print("=" * 60)
    print("  🚀 multi-agent-orchestrator 新手向导")
    print("=" * 60)
    print()
    print("  本向导将帮助你在 5 分钟内创建第一条流水线。")
    print("  流程：选模板 → 填参数 → 预览 → 确认生成")
    print()

    # Step 1: 列出模板
    templates = list_templates()
    if not templates:
        print("❌ 模板库为空，无法继续")
        return

    print("📋 可用模板列表：")
    print()
    for i, tpl in enumerate(templates, 1):
        print(f"  {i}. {tpl['name']}")
        print(f"     ⏱️ {tpl['time_estimate']} | 🔑 {tpl['api_key_required']} | 📄 {', '.join(tpl['output_files'][:2])}")
        print(f"     {tpl['description'][:50]}...")
        print()

    # Step 2: 选模板
    while True:
        try:
            choice = input(f"  请选择模板 (1-{len(templates)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(templates):
                selected = templates[idx]
                break
            else:
                print(f"  请输入 1 到 {len(templates)} 的数字")
        except (ValueError, EOFError):
            print("  请输入有效的数字")

    print()
    print(f"  ✅ 已选择：{selected['name']}")
    print()

    # Step 3: 显示模板详情
    show_template(selected['file'])

    # Step 4: 收集参数
    print("📝 填写流水线参数（直接回车使用默认值）：")
    print()

    pipeline = _load_template(os.path.join(TEMPLATES_DIR, selected['file']))['pipeline']
    default_name = pipeline.get('pipeline_name', selected['name'])

    pipeline_name = input(f"  流水线名称 [{default_name}]: ").strip()
    if not pipeline_name:
        pipeline_name = default_name

    output_dir = input(f"  输出目录 [./]: ").strip()
    if not output_dir:
        output_dir = "./"

    # Step 5: Dry-run 预览
    print()
    print("🔍 Dry-run 预览：")
    print(f"  流水线名称：{pipeline_name}")
    print(f"  输出目录：{output_dir}")
    print(f"  节点序列：")

    agents = pipeline.get('agents', [])
    for i, agent in enumerate(agents, 1):
        aid = agent.get('id', '')
        name = agent.get('name', '')
        atype = agent.get('type', 'task')
        print(f"    {i}. [{aid}] {name} (type: {atype})")

    # 依赖检查
    deps = _load_template(os.path.join(TEMPLATES_DIR, selected['file'])).get('dependencies', [])
    if deps:
        print()
        print("  依赖状态：")
        for dep in deps:
            skill_id = dep.get('skill_id', '')
            available, _ = _check_skill_available(skill_id)
            icon = '✅' if available else '⚠️'
            print(f"    {icon} {skill_id}")

    # Step 6: 确认生成
    print()
    while True:
        confirm = input("  确认生成 pipeline.json? (y/n): ").strip().lower()
        if confirm in ('y', 'yes', '是'):
            break
        elif confirm in ('n', 'no', '否'):
            print("  已取消")
            return
        else:
            print("  请输入 y 或 n")

    # Step 7: 生成文件
    output_path = os.path.join(output_dir, 'pipeline.json')
    rendered = render_pipeline(selected['file'])
    if rendered:
        rendered['pipeline_name'] = pipeline_name
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(rendered, f, ensure_ascii=False, indent=2)
        print()
        print(f"  ✅ 已生成：{output_path}")
        print()
        print("  下一步：")
        print(f"    python orchestrator.py run {output_path}")
        print()
    else:
        print("  ❌ 生成失败")


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("模板库管理器 - 多Agent协作编排引擎 v5.5")
        print("=" * 50)
        print("命令：")
        print("  python template_lib.py list               列出所有预置模板")
        print("  python template_lib.py show <template>    显示模板详情 + 依赖状态 + 三要素")
        print("  python template_lib.py check <template>   检查依赖是否满足")
        print("  python template_lib.py render <template>  渲染为可执行 pipeline JSON")
        print("  python template_lib.py validate <template> CI 校验（三要素 + 结构）")
        print("  python template_lib.py init               新手向导（交互式）")
        print()
        print("示例：")
        print("  python template_lib.py list")
        print("  python template_lib.py show gov_procurement_daily.json")
        print("  python template_lib.py render gov_procurement_daily.json")
        print("  python template_lib.py validate competitor_monitor_daily.json")
        print("  python template_lib.py init")
        sys.exit(0)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == 'list':
        templates = list_templates()
        if not templates:
            print("暂无预置模板")
        else:
            print("=" * 60)
            print("  预置流水线模板库")
            print("=" * 60)
            for tpl in templates:
                print(f"\n  📋 {tpl['name']} ({tpl['category']}) v{tpl['version']}")
                print(f"     ⏱️ {tpl['time_estimate']} | 🔑 {tpl['api_key_required']}")
                print(f"     {tpl['description'][:60]}...")
                print(f"     文件：{tpl['file']} | 标签：{', '.join(tpl['tags'])} | 依赖：{tpl['dependency_count']} 个")
            print(f"\n共 {len(templates)} 个模板")
            print("=" * 60)

    elif cmd == 'show':
        if not args:
            print("错误：请指定模板文件名")
            print("用法：python template_lib.py show <template_file>")
            sys.exit(1)
        show_template(args[0])

    elif cmd == 'check':
        if not args:
            print("错误：请指定模板文件名")
            print("用法：python template_lib.py check <template_file>")
            sys.exit(1)
        req, opt = check_dependencies(args[0])
        if not req and not opt:
            print("✅ 所有依赖均已满足")
        else:
            if req:
                print(f"❌ 缺失必需依赖：{', '.join(d['skill_id'] for d in req)}")
            if opt:
                print(f"⚠️ 缺失可选依赖：{', '.join(d['skill_id'] for d in opt)}")

    elif cmd == 'render':
        if not args:
            print("错误：请指定模板文件名")
            print("用法：python template_lib.py render <template_file> [output.json]")
            sys.exit(1)
        output_path = args[1] if len(args) > 1 else None
        pipeline = render_pipeline(args[0])
        if pipeline:
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(pipeline, f, ensure_ascii=False, indent=2)
                print(f"✅ 已渲染到 {output_path}")
            else:
                print(json.dumps(pipeline, ensure_ascii=False, indent=2))

    elif cmd == 'validate':
        if not args:
            # 校验所有模板
            all_valid = True
            for fname in os.listdir(TEMPLATES_DIR):
                if not fname.endswith('.json') or fname in ('template_schema.json', 'state_schema.json'):
                    continue
                if fname in ('pipeline_dag_template.json', 'control_flow_template.json',
                             'sub_pipeline_template.json', 'parent_pipeline_template.json'):
                    continue
                valid, errors = validate_template(fname)
                if not valid:
                    all_valid = False
                    print(f"❌ {fname}: {', '.join(errors)}")
            if all_valid:
                print("✅ 所有模板校验通过")
            else:
                sys.exit(1)
        else:
            valid, errors = validate_template(args[0])
            if valid:
                print(f"✅ {args[0]} 校验通过")
            else:
                print(f"❌ {args[0]} 校验失败：{', '.join(errors)}")
                sys.exit(1)

    elif cmd == 'init':
        newbie_wizard()

    else:
        print(f"未知命令：{cmd}")
        sys.exit(1)
