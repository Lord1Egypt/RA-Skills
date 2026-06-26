"""
Web Dashboard API Routes
"""

from flask import jsonify, request

from .config import LOCATION_MAP, REVERSE_LOCATION_MAP
from .utils import run_script, get_default_storage


def register_routes(app, get_user_func):
    """Register all API routes."""

    def get_user():
        return get_user_func()

    @app.route('/api/summary')
    def api_summary():
        daily = run_script(get_user(), 'meal_logger.py', 'daily-summary')
        weekly = run_script(get_user(), 'report_generator.py', 'nutrition', '--days', '7')
        weight = run_script(get_user(), 'body_metrics.py', 'trend', '--days', '30')
        return jsonify({"daily": daily, "weekly": weekly, "weight": weight})

    @app.route('/api/weight-history')
    def api_weight_history():
        days = request.args.get('days', '30')
        result = run_script(get_user(), 'body_metrics.py', 'list', '--days', days)
        return jsonify(result)

    @app.route('/api/nutrition-history')
    def api_nutrition_history():
        days = request.args.get('days', '7')
        result = run_script(get_user(), 'meal_logger.py', 'list', '--days', days)
        return jsonify(result)

    @app.route('/api/profile')
    def api_profile():
        result = run_script(get_user(), 'user_profile.py', 'get')
        return jsonify(result)

    @app.route('/api/pantry')
    def api_pantry():
        result = run_script(get_user(), 'pantry_manager.py', 'remaining')
        if result.get('status') == 'success':
            items = result['data']['items']
            grouped = {'冰箱': [], '冷冻': [], '干货区': [], '台面': []}
            by_category = {'蛋白质': [], '蔬菜': [], '碳水': [], '水果': [], '乳制品': [], '脂肪': [], '其他': []}
            category_map = {
                'protein': '蛋白质', 'vegetable': '蔬菜', 'carb': '碳水',
                'fruit': '水果', 'dairy': '乳制品', 'fat': '脂肪'
            }
            for item in items:
                loc = REVERSE_LOCATION_MAP.get(item.get('location', '冰箱'), item.get('location', '冰箱'))
                if loc in grouped:
                    grouped[loc].append(item)
                cat = category_map.get(item.get('category', '其他'), '其他')
                by_category[cat].append(item)
            result['data']['grouped'] = grouped
            result['data']['by_category'] = by_category
        return jsonify(result)

    @app.route('/api/pantry/use', methods=['POST'])
    def api_pantry_use():
        data = request.json
        result = run_script(get_user(), 'pantry_manager.py', 'use',
                           '--item-id', str(data.get('item_id')),
                           '--amount', str(data.get('amount')),
                           '--notes', data.get('notes', ''))
        return jsonify(result)

    @app.route('/api/pantry/update', methods=['POST'])
    def api_pantry_update():
        data = request.json
        args = ['--item-id', str(data.get('item_id'))]
        if data.get('purchase'):
            args.extend(['--purchase', data.get('purchase')])
        if data.get('shelf_life'):
            args.extend(['--shelf-life', str(data.get('shelf_life'))])
        if data.get('location'):
            args.extend(['--location', LOCATION_MAP.get(data.get('location'), data.get('location'))])
        if data.get('notes'):
            args.extend(['--notes', data.get('notes')])
        result = run_script(get_user(), 'pantry_manager.py', 'update', *args)
        return jsonify(result)

    @app.route('/api/pantry/add', methods=['POST'])
    def api_pantry_add():
        data = request.json
        location = data.get('location', 'auto')
        if location == 'auto':
            location = get_default_storage(data.get('food', ''))
        args = ['--food', data.get('food'), '--quantity', str(data.get('quantity')),
                '--location', LOCATION_MAP.get(location, location)]
        if data.get('expiry'):
            args.extend(['--expiry', data.get('expiry')])
        result = run_script(get_user(), 'pantry_manager.py', 'add', *args)
        return jsonify(result)

    @app.route('/api/pantry/delete', methods=['POST'])
    def api_pantry_delete():
        data = request.json
        result = run_script(get_user(), 'pantry_manager.py', 'remove', 
                           '--item-id', str(data.get('item_id')))
        return jsonify(result)
