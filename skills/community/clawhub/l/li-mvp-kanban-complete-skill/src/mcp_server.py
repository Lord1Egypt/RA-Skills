"""
看板系统 MCP Server
提供 LLM 原生工具接口
"""
from mcp.server.fastmcp import FastMCP
from database import (
    init_db, get_all_projects, get_project, create_project, 
    update_project, delete_project, search_projects_similar,
    get_all_lanes, create_lane, get_metrics, get_change_log
)
import json

# 初始化 MCP Server
mcp = FastMCP("Kanban Board")

# 初始化数据库
init_db()


@mcp.tool()
def list_projects(status: str = None, lane: str = None) -> str:
    """
    列出看板中的所有项目/任务
    
    Args:
        status: 过滤状态 (todo, in_progress, done)
        lane: 过滤泳道 (feature, security, devops, bugfix)
    
    Returns:
        JSON 格式的项目列表
    """
    projects = get_all_projects()
    
    if status:
        projects = [p for p in projects if p['status'] == status]
    if lane:
        projects = [p for p in projects if p['lane'] == lane]
    
    # 清理嵌入字段
    for p in projects:
        p.pop('name_embedding', None)
        p.pop('description_embedding', None)
    
    return json.dumps(projects, ensure_ascii=False, indent=2)


@mcp.tool()
def get_project_details(project_id: int) -> str:
    """
    获取单个项目的详细信息
    
    Args:
        project_id: 项目 ID
    
    Returns:
        JSON 格式的项目详情
    """
    project = get_project(project_id)
    if not project:
        return json.dumps({'error': '项目不存在'}, ensure_ascii=False)
    
    project.pop('name_embedding', None)
    project.pop('description_embedding', None)
    
    return json.dumps(project, ensure_ascii=False, indent=2)


@mcp.tool()
def add_project(name: str, lane: str = 'feature', status: str = 'todo',
                assignee: str = '', priority: str = 'medium',
                tasks: int = 0, description: str = '', tags: list = None) -> str:
    """
    添加新项目/任务到看板
    
    Args:
        name: 项目名称（必填）
        lane: 泳道 (feature, security, devops, bugfix)
        status: 状态 (todo, in_progress, done)
        assignee: 负责人
        priority: 优先级 (high, medium, low)
        tasks: 任务总数
        description: 项目描述
        tags: 标签列表
    
    Returns:
        JSON 格式的新建项目
    """
    project = create_project({
        'name': name,
        'lane': lane,
        'status': status,
        'assignee': assignee,
        'priority': priority,
        'tasks': tasks,
        'description': description,
        'tags': tags or []
    })
    
    return json.dumps(project, ensure_ascii=False, indent=2)


@mcp.tool()
def update_project_status(project_id: int, status: str) -> str:
    """
    更新项目状态
    
    Args:
        project_id: 项目 ID
        status: 新状态 (todo, in_progress, done)
    
    Returns:
        JSON 格式的更新后项目
    """
    if status not in ['todo', 'in_progress', 'done']:
        return json.dumps({'error': '无效状态，必须是 todo, in_progress 或 done'}, ensure_ascii=False)
    
    project = update_project(project_id, {'status': status})
    if not project:
        return json.dumps({'error': '项目不存在'}, ensure_ascii=False)
    
    return json.dumps(project, ensure_ascii=False, indent=2)


@mcp.tool()
def move_project(project_id: int, lane: str, status: str = None) -> str:
    """
    移动项目到不同泳道或状态
    
    Args:
        project_id: 项目 ID
        lane: 目标泳道 (feature, security, devops, bugfix)
        status: 目标状态（可选）
    
    Returns:
        JSON 格式的更新后项目
    """
    valid_lanes = ['feature', 'security', 'devops', 'bugfix']
    if lane not in valid_lanes:
        return json.dumps({'error': f'无效泳道，必须是 {valid_lanes}'}, ensure_ascii=False)
    
    update_data = {'lane': lane}
    if status:
        update_data['status'] = status
    
    project = update_project(project_id, update_data)
    if not project:
        return json.dumps({'error': '项目不存在'}, ensure_ascii=False)
    
    return json.dumps(project, ensure_ascii=False, indent=2)


@mcp.tool()
def delete_project(project_id: int) -> str:
    """
    删除项目
    
    Args:
        project_id: 项目 ID
    
    Returns:
        删除结果
    """
    project = delete_project(project_id)
    if not project:
        return json.dumps({'error': '项目不存在'}, ensure_ascii=False)
    
    return json.dumps({'success': True, 'deleted': project['name']}, ensure_ascii=False)


@mcp.tool()
def get_board_metrics() -> str:
    """
    获取看板统计指标
    
    Returns:
        JSON 格式的统计指标
    """
    metrics = get_metrics()
    lanes = get_all_lanes()
    
    return json.dumps({
        'metrics': metrics,
        'lanes': lanes
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def search_similar_projects(query: str, limit: int = 5) -> str:
    """
    搜索相似项目（向量搜索）
    
    Args:
        query: 搜索关键词
        limit: 返回数量限制
    
    Returns:
        JSON 格式的相似项目列表
    """
    projects = search_projects_similar(query, limit)
    
    for p in projects:
        p.pop('name_embedding', None)
        p.pop('description_embedding', None)
    
    return json.dumps(projects, ensure_ascii=False, indent=2)


@mcp.tool()
def get_project_history(project_id: int, limit: int = 20) -> str:
    """
    获取项目变更历史
    
    Args:
        project_id: 项目 ID
        limit: 返回记录数
    
    Returns:
        JSON 格式的变更历史
    """
    logs = get_change_log(project_id, limit)
    return json.dumps(logs, ensure_ascii=False, indent=2)


@mcp.tool()
def add_lane(lane_id: str, name: str, color: str = '#667eea', icon: str = '📌') -> str:
    """
    添加新泳道
    
    Args:
        lane_id: 泳道 ID（英文标识）
        name: 泳道名称
        color: 颜色（十六进制）
        icon: 图标 emoji
    
    Returns:
        JSON 格式的新建泳道
    """
    lane = create_lane({
        'id': lane_id,
        'name': name,
        'color': color,
        'icon': icon
    })
    
    return json.dumps(lane, ensure_ascii=False, indent=2)


@mcp.tool()
def update_lane(lane_id: str, name: str = None, color: str = None, icon: str = None) -> str:
    """
    更新泳道信息
    
    Args:
        lane_id: 泳道 ID
        name: 新名称（可选）
        color: 新颜色（可选）
        icon: 新图标（可选）
    
    Returns:
        JSON 格式的更新后泳道
    """
    from database import update_lane_by_id
    
    update_data = {}
    if name: update_data['name'] = name
    if color: update_data['color'] = color
    if icon: update_data['icon'] = icon
    
    lane = update_lane_by_id(lane_id, update_data)
    if not lane:
        return json.dumps({'error': '泳道不存在'}, ensure_ascii=False)
    
    return json.dumps(lane, ensure_ascii=False, indent=2)


@mcp.tool()
def delete_lane(lane_id: str) -> str:
    """
    删除泳道
    
    Args:
        lane_id: 泳道 ID
    
    Returns:
        删除结果
    """
    from database import delete_lane_by_id
    
    try:
        result = delete_lane_by_id(lane_id)
        if result:
            return json.dumps({'success': True, 'deleted': lane_id}, ensure_ascii=False)
        else:
            return json.dumps({'error': '泳道不存在'}, ensure_ascii=False)
    except ValueError as e:
        return json.dumps({'error': str(e)}, ensure_ascii=False)


@mcp.tool()
def list_lanes() -> str:
    """
    列出所有泳道
    
    Returns:
        JSON 格式的泳道列表
    """
    lanes = get_all_lanes()
    return json.dumps(lanes, ensure_ascii=False, indent=2)


@mcp.tool()
def batch_create_projects(projects: list) -> str:
    """
    批量创建项目
    
    Args:
        projects: 项目数组，每个项目包含 name, lane, status, assignee, priority, tasks 等字段
    
    Returns:
        JSON 格式的创建结果
    """
    from database import create_project
    
    results = []
    for proj in projects:
        result = create_project(proj)
        results.append(result)
    
    return json.dumps({
        'success': True,
        'created': len(results),
        'projects': results
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def batch_update_projects(updates: list) -> str:
    """
    批量更新项目
    
    Args:
        updates: 更新数组，每个更新包含 id 和要修改的字段
    
    Returns:
        JSON 格式的更新结果
    """
    from database import update_project
    
    results = []
    for update in updates:
        project_id = update.get('id')
        if not project_id:
            continue
        changes = {k: v for k, v in update.items() if k != 'id'}
        result = update_project(project_id, changes)
        if result:
            results.append(result)
    
    return json.dumps({
        'success': True,
        'updated': len(results),
        'projects': results
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def batch_delete_projects(ids: list) -> str:
    """
    批量删除项目
    
    Args:
        ids: 项目 ID 数组
    
    Returns:
        JSON 格式的删除结果
    """
    from database import delete_project
    
    deleted = []
    for project_id in ids:
        result = delete_project(project_id)
        if result:
            deleted.append(project_id)
    
    return json.dumps({
        'success': True,
        'deleted': len(deleted),
        'ids': deleted
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def update_project_full(project_id: int, name: str = None, lane: str = None,
                        status: str = None, priority: str = None,
                        assignee: str = None, tasks: int = None,
                        description: str = None, tags: list = None) -> str:
    """
    完整更新任务信息（支持所有字段）
    
    Args:
        project_id: 项目 ID
        name: 名称（可选）
        lane: 泳道（可选）
        status: 状态（可选）
        priority: 优先级（可选）
        assignee: 负责人（可选）
        tasks: 任务数（可选）
        description: 描述（可选）
        tags: 标签列表（可选）
    
    Returns:
        JSON 格式的更新后项目
    """
    from database import update_project as db_update_project
    
    update_data = {}
    if name: update_data['name'] = name
    if lane: update_data['lane'] = lane
    if status: update_data['status'] = status
    if priority: update_data['priority'] = priority
    if assignee: update_data['assignee'] = assignee
    if tasks is not None: update_data['tasks'] = tasks
    if description: update_data['description'] = description
    if tags: update_data['tags'] = tags
    
    project = db_update_project(project_id, update_data)
    if not project:
        return json.dumps({'error': '项目不存在'}, ensure_ascii=False)
    
    return json.dumps(project, ensure_ascii=False, indent=2)


@mcp.tool()
def get_lane_details(lane_id: str) -> str:
    """
    获取泳道详细信息（包含任务列表）
    
    Args:
        lane_id: 泳道 ID
    
    Returns:
        JSON 格式的泳道详情
    """
    from database import get_lane, get_all_projects
    
    lane = get_lane(lane_id)
    if not lane:
        return json.dumps({'error': '泳道不存在'}, ensure_ascii=False)
    
    # 获取该泳道的所有任务
    all_projects = get_all_projects()
    lane_projects = [p for p in all_projects if p['lane'] == lane_id]
    
    result = dict(lane)
    result['projects'] = lane_projects
    result['project_count'] = len(lane_projects)
    
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def nlp_command(command: str) -> str:
    """
    执行自然语言命令
    
    Args:
        command: 自然语言命令（如："添加一个高优先级安全任务"）
    
    Returns:
        JSON 格式的执行结果
    """
    import requests
    try:
        response = requests.post(
            "http://localhost:9999/api/llm/command",
            json={"command": command},
            timeout=10
        )
        return response.text
    except Exception as e:
        return json.dumps({'error': str(e)}, ensure_ascii=False)


@mcp.tool()
def llm_search(query: str, limit: int = 5) -> str:
    """
    向量搜索相似任务
    
    Args:
        query: 搜索关键词
        limit: 返回数量限制
    
    Returns:
        JSON 格式的搜索结果
    """
    import requests
    try:
        response = requests.post(
            "http://localhost:9999/api/llm/search",
            json={"query": query, "limit": limit},
            timeout=10
        )
        return response.text
    except Exception as e:
        return json.dumps({'error': str(e)}, ensure_ascii=False)


@mcp.tool()
def analyze_board() -> str:
    """
    分析看板状态，识别瓶颈和风险
    
    Returns:
        JSON 格式的分析报告
    """
    projects = get_all_projects()
    metrics = get_metrics()
    
    # 分析逻辑
    analysis = {
        'summary': {
            'total_projects': metrics['total_projects'],
            'completion_rate': f"{metrics['success_rate']}%",
            'in_progress_count': metrics['in_progress'],
            'todo_count': metrics['todo']
        },
        'bottlenecks': [],
        'risks': [],
        'suggestions': []
    }
    
    # 识别瓶颈：进行中的项目过多
    if metrics['in_progress'] > metrics['completed'] * 2:
        analysis['bottlenecks'].append({
            'type': 'wip_too_high',
            'message': f'进行中的项目 ({metrics["in_progress"]}) 远多于已完成项目 ({metrics["completed"]})',
            'severity': 'medium'
        })
        analysis['suggestions'].append('考虑减少并行工作，优先完成现有任务')
    
    # 识别风险：高优先级任务未完成
    high_priority_todo = [p for p in projects 
                         if p['priority'] == 'high' and p['status'] != 'done']
    if high_priority_todo:
        analysis['risks'].append({
            'type': 'high_priority_pending',
            'message': f'有 {len(high_priority_todo)} 个高优先级任务未完成',
            'projects': [p['name'] for p in high_priority_todo],
            'severity': 'high'
        })
        analysis['suggestions'].append('优先处理高优先级任务')
    
    # 识别风险：任务长期未更新
    # （简化版，实际应检查时间戳）
    
    # 泳道负载分析
    lane_load = {}
    for p in projects:
        lane = p['lane']
        if lane not in lane_load:
            lane_load[lane] = {'total': 0, 'done': 0}
        lane_load[lane]['total'] += 1
        if p['status'] == 'done':
            lane_load[lane]['done'] += 1
    
    analysis['lane_analysis'] = {}
    for lane, load in lane_load.items():
        rate = round(load['done'] / max(load['total'], 1) * 100)
        analysis['lane_analysis'][lane] = {
            'total': load['total'],
            'completed': load['done'],
            'completion_rate': f"{rate}%"
        }
    
    return json.dumps(analysis, ensure_ascii=False, indent=2)


# MCP Server 入口
if __name__ == '__main__':
    # 启动 MCP Server (stdio 模式)
    mcp.run()
