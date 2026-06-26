from flask import Flask, render_template, jsonify, request
from database import (
    init_db, get_all_projects, get_project, create_project,
    update_project, delete_project, search_projects_similar,
    get_all_lanes, create_lane, get_metrics, get_change_log,
    get_lane_by_id, update_lane_by_id, delete_lane_by_id
)
from nlp_parser import parse_command
from datetime import datetime
import json

app = Flask(__name__)

# 初始化数据库
init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/kanban')
def get_kanban():
    """获取完整看板数据"""
    projects = get_all_projects()
    lanes = get_all_lanes()
    metrics = get_metrics()
    
    # 清理嵌入字段
    for p in projects:
        p.pop('name_embedding', None)
        p.pop('description_embedding', None)
    
    return jsonify({
        'projects': projects,
        'lanes': lanes,
        'metrics': metrics
    })


@app.route('/api/metrics')
def get_metrics_endpoint():
    """获取统计指标"""
    return jsonify(get_metrics())


@app.route('/api/projects')
def get_projects():
    """获取所有项目"""
    projects = get_all_projects()
    for p in projects:
        p.pop('name_embedding', None)
        p.pop('description_embedding', None)
    return jsonify(projects)


@app.route('/api/lanes')
def get_lanes():
    """获取所有泳道"""
    return jsonify(get_all_lanes())


@app.route('/api/projects/<int:project_id>')
def get_project_endpoint(project_id):
    """获取单个项目"""
    project = get_project(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    project.pop('name_embedding', None)
    project.pop('description_embedding', None)
    return jsonify(project)


@app.route('/api/projects', methods=['POST'])
def add_project():
    """创建项目"""
    data = request.json
    project = create_project(data)
    return jsonify(project), 201


@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project_endpoint(project_id):
    """更新项目"""
    data = request.json
    project = update_project(project_id, data)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    return jsonify(project)


@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project_endpoint(project_id):
    """删除项目"""
    project = delete_project(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    return jsonify(project)


@app.route('/api/lanes', methods=['POST'])
def add_lane():
    """创建泳道"""
    data = request.json
    lane = create_lane(data)
    return jsonify(lane), 201


# ============ 新增 AI 接口 ============

@app.route('/api/llm/command', methods=['POST'])
def llm_command():
    """
    自然语言命令接口
    LLM 可直接调用此接口执行看板操作
    
    Request Body:
    {
        "command": "添加一个高优先级的安全任务给张三"
    }
    
    或 MCP 风格:
    {
        "tool": "add_project",
        "params": {
            "name": "安全加固",
            "lane": "security",
            "priority": "high",
            "assignee": "张三"
        }
    }
    """
    data = request.json
    
    if not data:
        return jsonify({'error': '请求体不能为空'}), 400
    
    # 支持两种调用方式
    if 'command' in data:
        # 自然语言模式
        result = parse_command(data['command'])
    elif 'tool' in data:
        # MCP 工具调用模式
        result = _execute_tool(data['tool'], data.get('params', {}))
    else:
        return jsonify({'error': '需要提供 command 或 tool 参数'}), 400
    
    # 执行操作
    if result.get('success'):
        action_result = _execute_action(result)
        return jsonify({
            'success': True,
            'action': result['action'],
            'result': action_result
        })
    else:
        return jsonify({
            'success': False,
            'error': result.get('error', '执行失败'),
            'examples': result.get('examples', [])
        }), 400


@app.route('/api/llm/analyze', methods=['GET', 'POST'])
def llm_analyze():
    """
    AI 看板分析接口
    返回瓶颈、风险和建议
    """
    projects = get_all_projects()
    metrics = get_metrics()
    
    analysis = {
        'generated_at': datetime.now().isoformat(),
        'summary': {
            'total_projects': metrics['total_projects'],
            'completion_rate': f"{metrics['success_rate']}%",
            'in_progress': metrics['in_progress'],
            'todo': metrics['todo'],
            'completed': metrics['completed']
        },
        'bottlenecks': [],
        'risks': [],
        'suggestions': [],
        'lane_analysis': {}
    }
    
    # 瓶颈分析：WIP 过高
    if metrics['in_progress'] > metrics['completed'] * 2:
        analysis['bottlenecks'].append({
            'type': 'wip_too_high',
            'message': f'进行中的项目 ({metrics["in_progress"]}) 远多于已完成项目 ({metrics["completed"]})',
            'severity': 'medium',
            'suggestion': '考虑减少并行工作，优先完成现有任务'
        })
    
    # 风险分析：高优先级任务
    high_priority_pending = [p for p in projects 
                            if p['priority'] == 'high' and p['status'] != 'done']
    if high_priority_pending:
        analysis['risks'].append({
            'type': 'high_priority_pending',
            'message': f'有 {len(high_priority_pending)} 个高优先级任务未完成',
            'projects': [p['name'] for p in high_priority_pending],
            'severity': 'high',
            'suggestion': '优先处理高优先级任务'
        })
    
    # 风险分析：长期未更新
    # （简化版，实际应检查时间戳）
    
    # 泳道负载分析
    lane_load = {}
    for p in projects:
        lane = p['lane']
        if lane not in lane_load:
            lane_load[lane] = {'total': 0, 'done': 0, 'in_progress': 0}
        lane_load[lane]['total'] += 1
        if p['status'] == 'done':
            lane_load[lane]['done'] += 1
        elif p['status'] == 'in_progress':
            lane_load[lane]['in_progress'] += 1
    
    for lane, load in lane_load.items():
        rate = round(load['done'] / max(load['total'], 1) * 100)
        analysis['lane_analysis'][lane] = {
            'total': load['total'],
            'completed': load['done'],
            'in_progress': load['in_progress'],
            'completion_rate': f"{rate}%",
            'wip_ratio': round(load['in_progress'] / max(load['total'], 1) * 100)
        }
    
    # 生成建议
    if not analysis['bottlenecks'] and not analysis['risks']:
        analysis['suggestions'].append('看板状态良好，继续保持！')
    
    return jsonify(analysis)


@app.route('/api/llm/search', methods=['POST'])
def llm_search():
    """
    向量搜索接口
    搜索相似任务
    """
    data = request.json
    query = data.get('query', '')
    limit = data.get('limit', 5)
    
    if not query:
        return jsonify({'error': '需要提供搜索关键词'}), 400
    
    projects = search_projects_similar(query, limit)
    
    for p in projects:
        p.pop('name_embedding', None)
        p.pop('description_embedding', None)
    
    return jsonify({
        'query': query,
        'results': projects,
        'count': len(projects)
    })


@app.route('/api/history')
def get_history():
    """获取变更历史"""
    project_id = request.args.get('project_id', type=int)
    limit = request.args.get('limit', 50, type=int)
    
    logs = get_change_log(project_id, limit)
    return jsonify(logs)


@app.route('/api/health')
def health():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': 'v3.0.0',
        'features': {
            'sqlite': True,
            'vector_search': True,
            'nlp': True,
            'mcp': True
        }
    })


# ============ 泳道管理接口 ============

@app.route('/api/lanes/<lane_id>', methods=['GET'])
def get_lane(lane_id):
    """获取单个泳道详情"""
    lane = get_lane_by_id(lane_id)
    if not lane:
        return jsonify({'error': '泳道不存在'}), 404
    return jsonify(lane)


@app.route('/api/lanes/<lane_id>', methods=['PUT'])
def update_lane(lane_id):
    """更新泳道信息"""
    data = request.json
    lane = update_lane_by_id(lane_id, data)
    if not lane:
        return jsonify({'error': '泳道不存在'}), 404
    return jsonify(lane)


@app.route('/api/lanes/<lane_id>', methods=['DELETE'])
def delete_lane(lane_id):
    """删除泳道"""
    result = delete_lane_by_id(lane_id)
    if not result:
        return jsonify({'error': '泳道不存在'}), 404
    return jsonify({'success': True, 'deleted': lane_id})


# ============ 批量操作接口 ============

@app.route('/api/batch/create', methods=['POST'])
def batch_create():
    """批量创建任务"""
    data = request.json
    projects = data.get('projects', [])
    
    if not projects:
        return jsonify({'error': '需要提供 projects 数组'}), 400
    
    results = []
    for proj in projects:
        result = create_project(proj)
        results.append(result)
    
    return jsonify({
        'success': True,
        'created': len(results),
        'projects': results
    })


@app.route('/api/batch/update', methods=['POST'])
def batch_update():
    """批量更新任务"""
    data = request.json
    updates = data.get('updates', [])
    
    if not updates:
        return jsonify({'error': '需要提供 updates 数组'}), 400
    
    results = []
    for update in updates:
        project_id = update.get('id')
        if not project_id:
            continue
        changes = {k: v for k, v in update.items() if k != 'id'}
        result = update_project(project_id, changes)
        if result:
            results.append(result)
    
    return jsonify({
        'success': True,
        'updated': len(results),
        'projects': results
    })


@app.route('/api/batch/delete', methods=['POST'])
def batch_delete():
    """批量删除任务"""
    data = request.json
    ids = data.get('ids', [])
    
    if not ids:
        return jsonify({'error': '需要提供 ids 数组'}), 400
    
    deleted = []
    for project_id in ids:
        result = delete_project(project_id)
        if result:
            deleted.append(project_id)
    
    return jsonify({
        'success': True,
        'deleted': len(deleted),
        'ids': deleted
    })


# ============ 辅助函数 ============

def _execute_tool(tool_name: str, params: dict) -> dict:
    """执行 MCP 风格工具调用"""
    tool_map = {
        'add_project': lambda p: parse_command(f"添加任务 \"{p.get('name', 'New Task')}\""),
        'update_project_status': lambda p: parse_command(f"把项目 {p.get('project_id')} 改为 {p.get('status')}"),
        'move_project': lambda p: parse_command(f"把项目 {p.get('project_id')} 移到 {p.get('lane')}"),
        'delete_project': lambda p: parse_command(f"删除项目 {p.get('project_id')}"),
        'list_projects': lambda p: parse_command("查看所有任务"),
        'analyze_board': lambda p: parse_command("分析看板"),
    }
    
    if tool_name in tool_map:
        return tool_map[tool_name](params)
    else:
        return {
            'success': False,
            'error': f'未知工具：{tool_name}'
        }


def _execute_action(parsed_result: dict):
    """执行解析后的操作"""
    action = parsed_result['action']
    params = parsed_result['params']
    
    if action == 'add_project':
        return create_project(params)
    elif action == 'update_project_status':
        return update_project(params['project_id'], {'status': params['status']})
    elif action == 'move_project':
        update_data = {'lane': params['lane']}
        if params.get('status'):
            update_data['status'] = params['status']
        return update_project(params['project_id'], update_data)
    elif action == 'delete_project':
        return delete_project(params['project_id'])
    elif action == 'list_projects':
        projects = get_all_projects()
        if params.get('status'):
            projects = [p for p in projects if p['status'] == params['status']]
        if params.get('lane'):
            projects = [p for p in projects if p['lane'] == params['lane']]
        for p in projects:
            p.pop('name_embedding', None)
            p.pop('description_embedding', None)
        return {'projects': projects, 'count': len(projects)}
    elif action == 'analyze_board':
        # 复用分析逻辑
        projects = get_all_projects()
        metrics = get_metrics()
        return {
            'summary': metrics,
            'project_count': len(projects)
        }
    else:
        return {'error': f'未知操作：{action}'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
