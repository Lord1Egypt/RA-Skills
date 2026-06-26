# coding: utf-8
"""
华为云 Python SDK 方法与入参查询工具

此脚本可以：
1. 列出所有已安装的 huaweicloudsdk 包
2. 查询某个服务的所有 Client 类
3. 查询某个 Client 的所有 API 方法
4. 查询某个方法的入参（Request 类的属性列表和类型）

用法:
    python query_sdk_methods.py                              # 列出所有 SDK 包
    python query_sdk_methods.py --service vpc                # 列出 VPC SDK 的所有 Client
    python query_sdk_methods.py --service vpc --v3           # 列出 VPC v3 的所有 Client
    python query_sdk_methods.py --service vpc --v3 --client VpcClient  # 列出 VpcClient 的所有方法
    python query_sdk_methods.py --service vpc --v3 --client VpcClient --method list_vpcs  # 列出方法的入参
    python query_sdk_methods.py --service vpc --v3 --client VpcClient --search list      # 搜索包含关键字的方法
    python query_sdk_methods.py --all-clients                # 列出所有 SDK 的所有 Client（耗时较长）
"""

import argparse
import importlib
import inspect
import json
import pkgutil
import sys
import re
from typing import List, Dict, Optional


def get_installed_sdk_packages() -> List[str]:
    """获取所有已安装的 huaweicloudsdk 包（排除 core 和 all）"""
    sdks = []
    sys_path = [p for p in sys.path if p]

    for site_pkg in sys_path:
        try:
            entries = list(pkgutil.iter_modules([site_pkg]))
            found_any = False
            for info in entries:
                if info.name.startswith('huaweicloudsdk') and info.name not in ('huaweicloudsdkcore', 'huaweicloudsdkall'):
                    sdks.append(info.name)
                    found_any = True
            if found_any:
                break  # 在第一个包含 SDK 包的 site-packages 中停止
        except Exception:
            continue

    return sorted(set(sdks))


def get_sdk_version_prefix() -> str:
    """获取已安装 SDK 的版本号前缀，用于确定 v3/v5 等子模块"""
    # 通过查看一个已知包来获取版本前缀
    sdks = get_installed_sdk_packages()
    # 使用 VPC 包作为参考（因为 VPC 有 v2 和 v3）
    if 'huaweicloudsdkvpc' in sdks:
        try:
            vpc_pkg = importlib.import_module('huaweicloudsdkvpc')
            vpc_path = getattr(vpc_pkg, '__path__', [])
            versions = [d for d in pkgutil.iter_modules(vpc_path) if d.name.startswith('v') and d.name[1:].isdigit()]
            return [v.name for v in sorted(versions, key=lambda x: x.name, reverse=True)]
        except Exception:
            pass
    return ['v3', 'v5']


def discover_clients_in_package(package_name: str, version: str = 'v3') -> List[Dict]:
    """
    发现某个 SDK 包中的所有 Client 类

    Args:
        package_name: SDK 包名，如 huaweicloudsdkvpc
        version: 版本模块名，如 v3

    Returns:
        列表，每个元素包含 {'name': str, 'module': str, 'full_name': str}
    """
    clients = []
    try:
        # 导入包的 version 子模块（通过 __init__.py 访问所有导出）
        full_module_name = f"{package_name}.{version}"
        mod = importlib.import_module(full_module_name)

        # 遍历 version 模块的 __init__ 导出的所有对象，查找以 Client 结尾的类
        for name in dir(mod):
            if not name.endswith('Client'):
                continue
            obj = getattr(mod, name)
            # 只保留类，排除 AsyncClient（后续按需求可单独处理）
            # 这里先收集所有 Client
            if inspect.isclass(obj):
                client_module = getattr(obj, '__module__', '')
                full_class_name = f"{client_module}.{name}"
                clients.append({
                    'name': name,
                    'module': full_module_name,
                    'full_name': full_class_name,
                    'define_module': client_module
                })
    except Exception as e:
        pass

    return clients


def get_api_methods(client_class) -> List[Dict]:
    """
    获取 Client 类的所有 API 方法（通过 docstring 识别，排除内部方法）
    
    Args:
        client_class: Client 类
    
    Returns:
        列表，每个元素包含 {
            'name': str,              # 方法名
            'description': str,       # 方法描述
            'request_type': str,      # Request 类型
            'response_type': str      # Response 类型
        }
    """
    methods = []
    # 内置方法排除列表
    internal_methods = {
        'new_builder', 'add_file_logger', 'add_stream_logger', 
        'with_stream_log', 'with_file_log', '_call_api',
        '_update_invoke_statistics', '_set_cluster_id', '_set_target_service'
    }
    
    for name, method in inspect.getmembers(client_class, predicate=inspect.isfunction):
        # 跳过内部方法、构建器方法、log方法、_invoker 方法
        if name.startswith('_'):
            continue
        if name in internal_methods:
            continue
        if name.endswith('_invoker') or name.endswith('_async'):
            continue
        
        doc = inspect.getdoc(method) or ''
        
        # 检查是否有 docstring（API 方法有 docstring）
        if not doc or not doc.strip():
            continue
        
        # 从 docstring 中提取 request 和 response 类型
        request_match = re.search(r':class:`([^`]+Request)`', doc)
        response_match = re.search(r':class:`([^`]+Response)`', doc)
        
        # 提取描述（第一行）
        description = doc.split('\n')[0].strip() if doc else ''
        # 清理描述中的 "添加"、"删除"、"查询" 等前缀，保留简洁描述
        
        request_type = request_match.group(1) if request_match else 'Unknown'
        response_type = response_match.group(1) if response_match else 'Unknown'
        
        methods.append({
            'name': name,
            'description': description,
            'request_type': request_type,
            'response_type': response_type
        })
    
    return sorted(methods, key=lambda x: x['name'])


def get_request_params(request_type: str, source_module: str) -> List[Dict]:
    """
    获取 Request 类的参数（属性）列表
    
    Args:
        request_type: Request 类的完整模块路径，如 huaweicloudsdkvpc.v3.model.ListVpcsRequest
        source_module: 来源模块，用于导入
    
    Returns:
        列表，每个元素包含 {'name': str, 'type': str, 'description': str}
    """
    params = []
    try:
        # 尝试从不同的位置导入 Request 类
        module_to_import = None
        
        # 方式1: 直接使用 request_type 作为模块路径
        if request_type.startswith(source_module.rsplit('.', 1)[0]):
            module_to_import = request_type.rsplit('.', 1)[0]
            class_name = request_type.rsplit('.', 1)[1]
        else:
            # 方式2: 从 source_module 的同级 model 模块导入
            parts = source_module.rsplit('.', 1)
            if len(parts) == 2:
                module_to_import = f"{parts[0]}.{parts[1]}"  # v3
                class_name = request_type.split('.')[-1]
            else:
                return params
        
        # 先尝试在 source_module 中查找
        try:
            mod = importlib.import_module(source_module)
            if hasattr(mod, class_name):
                req_class = getattr(mod, class_name)
            else:
                # 尝试从 model 子模块
                try:
                    model_mod = importlib.import_module(f"{module_to_import}.model")
                    if hasattr(model_mod, class_name):
                        req_class = getattr(model_mod, class_name)
                    else:
                        return params
                except Exception:
                    # 尝试直接请求类作为属性
                    req_class = getattr(mod, class_name, None)
                    if not req_class:
                        return params
        except Exception:
            return params
        
        if req_class is None or not inspect.isclass(req_class):
            return params
        
        # 从 openapi_types 获取属性类型
        openapi_types = getattr(req_class, 'openapi_types', {})
        attribute_map = getattr(req_class, 'attribute_map', {})
        
        for attr_name, attr_type in openapi_types.items():
            # 获取属性描述（如果有 setter docstring）
            # 尝试获取 getter/setter
            setter = getattr(req_class, f'{attr_name}', None)
            prop_type = attr_type if isinstance(attr_type, str) else str(attr_type)
            
            # 查找 setter 的 docstring
            setter_doc = ''
            prop = getattr(req_class, attr_name, None)
            if hasattr(prop, 'fset') and prop.fset:
                setter_doc = inspect.getdoc(prop.fset) or ''
            
            params.append({
                'name': attr_name,
                'type': prop_type,
                'description': setter_doc.split('\n')[0].strip() if setter_doc else ''
            })
    except Exception as e:
        # 静默失败
        pass
    
    return params


def format_client_methods(service: str, version: str, client_name: str, 
                           methods: List[Dict], source_module: str,
                           search_keyword: Optional[str] = None) -> str:
    """格式化输出 Client 的方法列表"""
    lines = []
    lines.append(f"\n{'='*80}")
    lines.append(f"Client: {client_name}")
    lines.append(f"Module: {source_module}")
    lines.append(f"Total API Methods: {len(methods)}")
    lines.append(f"{'='*80}\n")
    
    filtered_methods = methods
    if search_keyword:
        filtered_methods = [
            m for m in methods 
            if search_keyword.lower() in m['name'].lower() 
            or search_keyword.lower() in m['description'].lower()
        ]
        lines.append(f"搜索关键字: '{search_keyword}' - 找到 {len(filtered_methods)} 个匹配\n")
    
    for i, method in enumerate(filtered_methods, 1):
        lines.append(f"  [{i}] {method['name']}:")
        lines.append(f"      描述: {method['description']}")
        lines.append(f"      Request: {method['request_type']}")
        lines.append(f"      Response: {method['response_type']}")
        lines.append("")
    
    return '\n'.join(lines)


def get_class_help_info(class_name: str, source_module: str, search_packages: Optional[List[str]] = None) -> Dict:
    """
    获取 SDK 类的详细帮助信息，包括 __init__ 参数、openapi_types、attribute_map 及属性描述。
    
    Args:
        class_name: 类名，如 CreateUserReqBody
        source_module: 来源模块，如 huaweicloudsdkiam.v5
        search_packages: 可选的搜索包列表，用于跨模块查找类
    
    Returns:
        字典，包含类的详细信息
    """
    result = {
        'class_name': class_name,
        'found': False,
        'module_path': '',
        'init_params': [],
        'openapi_types': {},
        'attribute_map': {},
        'properties': []
    }
    
    # 构建搜索的模块列表
    modules_to_try = [source_module]
    
    # 尝试 model 子模块
    parts = source_module.rsplit('.', 1)
    if len(parts) == 2:
        modules_to_try.append(f"{parts[0]}.{parts[1]}.model")
    
    # 如果提供了额外的搜索包，也加入
    if search_packages:
        for pkg in search_packages:
            modules_to_try.append(f"{pkg}.model")
    
    # 尝试查找并导入类
    target_class = None
    target_module_path = ''
    
    for mod_name in modules_to_try:
        try:
            mod = importlib.import_module(mod_name)
            if hasattr(mod, class_name):
                target_class = getattr(mod, class_name)
                target_module_path = f"{mod_name}.{class_name}"
                break
        except Exception:
            continue
    
    # 如果在已知模块中没找到，尝试直接通过完整类名导入
    if not target_class and '.' in class_name:
        try:
            module_path = '.'.join(class_name.split('.')[:-1])
            cls_name = class_name.split('.')[-1]
            mod = importlib.import_module(module_path)
            target_class = getattr(mod, cls_name, None)
            if target_class:
                target_module_path = class_name
        except Exception:
            pass
    
    if not target_class or not inspect.isclass(target_class):
        # 最后尝试：在所有已安装的 SDK 中搜索
        if search_packages:
            for pkg in search_packages:
                try:
                    # 尝试 v3 和 v5 版本
                    for ver in ['v5', 'v3']:
                        try:
                            mod = importlib.import_module(f"{pkg}.{ver}")
                            if hasattr(mod, class_name):
                                target_class = getattr(mod, class_name)
                                target_module_path = f"{pkg}.{ver}.{class_name}"
                                break
                        except Exception:
                            # 尝试 model 子模块
                            try:
                                model_mod = importlib.import_module(f"{pkg}.{ver}.model")
                                if hasattr(model_mod, class_name):
                                    target_class = getattr(model_mod, class_name)
                                    target_module_path = f"{pkg}.{ver}.model.{class_name}"
                                    break
                            except Exception:
                                continue
                    if target_class:
                        break
                except Exception:
                    continue
    
    if not target_class:
        return result
    
    result['found'] = True
    result['module_path'] = target_module_path
    
    # 获取 openapi_types
    openapi_types = getattr(target_class, 'openapi_types', {})
    result['openapi_types'] = openapi_types
    
    # 获取 attribute_map
    attribute_map = getattr(target_class, 'attribute_map', {})
    result['attribute_map'] = attribute_map
    
    # 从 __init__ docstring 提取 :param name: 描述
    # __init__ docstring 格式示例:
    #   :param name: IAM用户名，长度为1到64个字符...
    #   :type name: str
    param_descriptions = {}
    init_doc = inspect.getdoc(target_class.__init__) or ''
    for line in init_doc.split('\n'):
        line = line.strip()
        param_match = re.match(r':param\s+(\w+):\s*(.+)', line)
        if param_match:
            param_name = param_match.group(1)
            param_desc = param_match.group(2).strip()
            # 清理 HTML 转义字符和多余的转义（SDK docstring 中的转义格式）
            import html
            param_desc = html.unescape(param_desc)
            # 清理 HTML unescape 后残留的多余反斜杠（如 \" -> "）
            param_desc = param_desc.replace('\\"', '"')
            # 清理双反斜杠转义
            param_desc = param_desc.replace('\\\\', '\\')
            param_descriptions[param_name] = param_desc
    
    # 获取 __init__ 签名
    try:
        sig = inspect.signature(target_class.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            default = '无默认值' if param.default == inspect.Parameter.empty else repr(param.default)
            result['init_params'].append({
                'name': param_name,
                'default': default,
                'kind': str(param.kind).split('.')[-1]
            })
    except Exception:
        pass
    
    # 获取每个属性的描述信息
    for attr_name, attr_type in openapi_types.items():
        prop_info = {
            'name': attr_name,
            'type': attr_type if isinstance(attr_type, str) else str(attr_type),
            'json_key': attribute_map.get(attr_name, attr_name),
            'description': ''
        }
        
        # 优先使用 __init__ docstring 中的 :param 描述
        if attr_name in param_descriptions:
            prop_info['description'] = param_descriptions[attr_name]
        
        # 简化类型字符串
        type_str = prop_info['type']
        if type_str.startswith("'") and type_str.endswith("'"):
            type_str = type_str[1:-1]
        if '.' in type_str:
            type_str = type_str.split('.')[-1]
        prop_info['type'] = type_str
        
        result['properties'].append(prop_info)
    
    return result


def format_class_help(class_info: Dict) -> str:
    """格式化输出类的详细帮助信息"""
    lines = []
    
    if not class_info['found']:
        lines.append(f"❌ 未找到类: {class_info['class_name']}")
        lines.append("\n提示: 可以在 SDK 模块的 model 子模块中查找，或直接使用完整的类路径")
        return '\n'.join(lines)
    
    lines.append(f"\n{'='*80}")
    lines.append(f"类详情: {class_info['class_name']}")
    lines.append(f"{'='*80}")
    lines.append(f"  完整路径: {class_info['module_path']}")
    lines.append("")
    
    # 显示 __init__ 参数
    if class_info['init_params']:
        lines.append(f"  __init__ 参数 ({len(class_info['init_params'])} 个):")
        lines.append(f"  {'-'*60}")
        for param in class_info['init_params']:
            default_str = f" = {param['default']}" if param['default'] != '无默认值' else ''
            lines.append(f"    {param['name']}{default_str}")
        lines.append("")
    
    # 显示属性列表
    if class_info['properties']:
        lines.append(f"  属性列表 ({len(class_info['properties'])} 个):")
        lines.append(f"  {'-'*60}")
        for prop in class_info['properties']:
            desc = f" - {prop['description']}" if prop['description'] else ''
            json_info = f" (JSON: {prop['json_key']})" if prop['json_key'] != prop['name'] else ''
            lines.append(f"    {prop['name']}: {prop['type']}{json_info}{desc}")
        lines.append("")
    
    # 显示 openapi_types
    if class_info['openapi_types']:
        lines.append(f"  openapi_types (SDK 内部类型定义):")
        lines.append(f"  {'-'*60}")
        for attr_name, attr_type in class_info['openapi_types'].items():
            type_str = attr_type if isinstance(attr_type, str) else str(attr_type)
            if type_str.startswith("'") and type_str.endswith("'"):
                type_str = type_str[1:-1]
            lines.append(f"    {attr_name}: {type_str}")
        lines.append("")
    
    return '\n'.join(lines)


def format_request_params(method_info: Dict, params: List[Dict], class_info: Optional[Dict] = None) -> str:
    """格式化输出方法入参详情"""
    lines = []
    lines.append(f"\n{'='*80}")
    lines.append(f"方法入参详解: {method_info['name']}")
    lines.append(f"{'='*80}")
    lines.append(f"  描述: {method_info['description']}")
    lines.append(f"  Request 类型: {method_info['request_type']}")
    lines.append(f"  Response 类型: {method_info['response_type']}")
    lines.append("")
    
    if params:
        lines.append(f"  入参列表 ({len(params)} 个):")
        lines.append(f"  {'-'*60}")
        for param in params:
            # 清理类型字符串
            type_str = param['type']
            if type_str.startswith("'") and type_str.endswith("'"):
                type_str = type_str[1:-1]
            # 简化完整类名
            if '.' in type_str:
                type_str = type_str.split('.')[-1]
            
            desc = f" - {param['description']}" if param['description'] else ''
            lines.append(f"    {param['name']}: {type_str}{desc}")
    else:
        lines.append("  无入参 / 无法获取入参信息")
    
    return '\n'.join(lines)


def detect_sdk_versions(package_name: str) -> List[str]:
    """
    探测某个 SDK 包中可用的版本模块（如 v3, v5, v2）
    
    Args:
        package_name: SDK 包名，如 huaweicloudsdkecs
    
    Returns:
        可用的版本列表，按版本排序，如 ['v3', 'v5']
    """
    try:
        pkg = importlib.import_module(package_name)
        pkg_path = getattr(pkg, '__path__', None)
        if not pkg_path:
            return ['v3']
        version_dirs = [d for d in pkgutil.iter_modules(pkg_path) if d.name.startswith('v') and d.name[1:].isdigit()]
        if version_dirs:
            return sorted([d.name for d in version_dirs], reverse=True)
    except Exception:
        pass
    return ['v3']


def resolve_sdk_version(sdk_name: str, requested_version: Optional[str]) -> str:
    """
    解析并验证 SDK 版本，支持自动回退到可用版本
    
    Args:
        sdk_name: 包名，如 huaweicloudsdkecs
        requested_version: 请求的版本，如 v3
    
    Returns:
        实际可用的版本
    """
    available_versions = detect_sdk_versions(sdk_name)
    if requested_version == 'v3' and requested_version not in available_versions and available_versions:
        return available_versions[0]
    return requested_version or (available_versions[0] if available_versions else 'v3')


def main():
    parser = argparse.ArgumentParser(
        description='华为云 Python SDK 方法与入参查询工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    # 列出所有已安装的 SDK 包
    python query_sdk_methods.py
    
    # 列出 VPC SDK 的所有 Client 类
    python query_sdk_methods.py --service vpc
    
    # 列出 VPC v3 VpcClient 的所有方法
    python query_sdk_methods.py --service vpc --v3 --client VpcClient
    
    # 查询某个方法的入参详情
    python query_sdk_methods.py --service vpc --v3 --client VpcClient --method list_vpcs
    
    # 搜索包含关键字的方法
    python query_sdk_methods.py --service vpc --v3 --client VpcClient --search firewall
    
    # 查询 SDK 类（如 Request Body）的详细帮助信息
    python query_sdk_methods.py --service iam --v5 --class CreateUserReqBody
    
    # 列出所有 SDK 的所有 Client（耗时较长）
    python query_sdk_methods.py --all-clients
    
    # 输出 JSON 格式
    python query_sdk_methods.py --service vpc --client VpcClient --json
        """
    )
    
    parser.add_argument('--service', type=str, help='服务名称，如 vpc、iam、ecs')
    parser.add_argument('--v3', dest='version', action='store_const', const='v3', default=None,
                        help='使用 v3 版本（默认）')
    parser.add_argument('--v5', dest='version', action='store_const', const='v5',
                        help='使用 v5 版本')
    parser.add_argument('--client', type=str, help='Client 类名，如 VpcClient')
    parser.add_argument('--method', type=str, help='方法名，如 list_vpcs')
    parser.add_argument('--search', type=str, help='搜索方法名或描述中包含的关键字')
    parser.add_argument('--class', dest='class_name', type=str, help='查询 SDK Request/Response 类的详细帮助信息，如 CreateUserReqBody。支持只传类名（自动搜索所有SDK包），或传入完整路径如 huaweicloudsdkiam.v5.CreateUserReqBody')
    parser.add_argument('--all-clients', action='store_true', help='列出所有 SDK 的所有 Client 类')
    parser.add_argument('--json', action='store_true', help='以 JSON 格式输出')
    
    args = parser.parse_args()
    
    # 模式1: 列出所有 SDK 包（不带参数）
    if not args.service and not args.all_clients:
        print("📦 列出所有已安装的华为云 SDK 包:\n")
        sdks = get_installed_sdk_packages()
        if not sdks:
            print("未找到已安装的 huaweicloudsdk 包。请先安装: pip install huaweicloudsdkall")
            sys.exit(1)
        print(f"共找到 {len(sdks)} 个 SDK 包:\n")
        for i, sdk in enumerate(sdks, 1):
            service_name = sdk.replace('huaweicloudsdk', '').replace('all', '')
            print(f"  [{i:3d}] {sdk:40s} ({service_name})")
        print(f"\n提示: 使用 --service {sdks[0].replace('huaweicloudsdk', '')} 查看该服务的 Client 类")
        return
    
    # 模式2: 列出所有 SDK 的所有 Client（耗时较长）
    if args.all_clients:
        sdks = get_installed_sdk_packages()
        print(f"🔍 扫描 {len(sdks)} 个 SDK 包的所有 Client 类...\n")
        
        results = {}
        for sdk in sdks:
            # 自动检测 SDK 的版本
            versions = detect_sdk_versions(sdk)
            for ver in versions:
                clients = discover_clients_in_package(sdk, ver)
                if clients:
                    service_name = sdk.replace('huaweicloudsdk', '')
                    results[service_name] = {'version': ver, 'clients': [c['name'] for c in clients]}
                    break
        
        if args.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            total_clients = sum(len(v['clients']) for v in results.values())
            print(f"共找到 {len(results)} 个服务，{total_clients} 个 Client 类:\n")
            for service in sorted(results.keys()):
                info = results[service]
                client_names = info['clients']
                ver = info.get('version', '?')
                print(f"  {service} ({ver}): {', '.join(client_names)}")
        return
    
    # 验证 service 参数
    if not args.service:
        parser.error("请指定 --service 参数")
    
    sdk_name = f"huaweicloudsdk{args.service}"
    
    # 导入 SDK 包验证是否存在
    try:
        importlib.import_module(sdk_name)
    except ImportError:
        print(f"❌ 未找到 SDK 包: {sdk_name}")
        print("可用的 SDK 包:")
        sdks = get_installed_sdk_packages()
        matching = [s for s in sdks if args.service.lower() in s.lower()]
        for s in matching[:10]:
            print(f"  - {s}")
        sys.exit(1)
    
    # 自动解析版本
    version = resolve_sdk_version(sdk_name, args.version)
    full_module_name = f"{sdk_name}.{version}"
    
    # 模式0: 查询特定类的详细帮助信息 (独立模式，不需要 client)
    if args.class_name and not args.client:
        sdks = get_installed_sdk_packages()
        class_info = get_class_help_info(args.class_name, full_module_name, search_packages=sdks)
        if args.json:
            print(json.dumps(class_info, indent=2, ensure_ascii=False))
        else:
            print(format_class_help(class_info))
        return
    
    # 模式3: 列出某个服务的所有 Client
    if not args.client:
        print(f"🔍 查询 {sdk_name}.{version} 的 Client 类:\n")
        clients = discover_clients_in_package(sdk_name, version)
        if not clients:
            print(f"未找到 {sdk_name}.{version} 中的 Client 类")
            # 尝试其他版本
            available = detect_sdk_versions(sdk_name)
            for trial_ver in available:
                if trial_ver != version:
                    clients = discover_clients_in_package(sdk_name, trial_ver)
                    if clients:
                        print(f"提示: 可在 {trial_ver} 版本中找到 {len(clients)} 个 Client")
            sys.exit(1)
        
        if args.json:
            print(json.dumps(clients, indent=2, ensure_ascii=False))
        else:
            print(f"找到 {len(clients)} 个 Client 类:\n")
            for i, client in enumerate(clients, 1):
                print(f"  [{i}] {client['name']}")
            print(f"\n提示: 使用 --client {clients[0]['name']} 查看该 Client 的所有方法")
        return
    
    # 模式4: 列出某个 Client 的所有方法
    full_module_name = f"{sdk_name}.{version}"
    try:
        mod = importlib.import_module(full_module_name)
        client_class = getattr(mod, args.client, None)
        if not client_class:
            print(f"❌ 在 {full_module_name} 中未找到 Client 类: {args.client}")
            # 尝试列出可用的 Client
            clients = discover_clients_in_package(sdk_name, version)
            if clients:
                print(f"可用的 Client 类:")
                for c in clients:
                    print(f"  - {c['name']}")
            sys.exit(1)
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        sys.exit(1)
    
    methods = get_api_methods(client_class)
    
    if args.json:
        output = {'module': full_module_name, 'client': args.client, 'methods': []}
        for m in methods:
            output['methods'].append({
                'name': m['name'],
                'description': m['description'],
                'request_type': m['request_type'],
                'response_type': m['response_type']
            })
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return
    
    # 查询类详情 (与 client 一起使用时)
    if args.class_name:
        class_info = get_class_help_info(args.class_name, full_module_name)
        if args.json:
            print(json.dumps(class_info, indent=2, ensure_ascii=False))
        else:
            print(format_class_help(class_info))
        return
    
    if not args.method and not args.search:
        print(format_client_methods(args.service, version, args.client, methods, full_module_name))
        print(f"\n提示: 使用 --method <方法名> 查看入参详情")
        print(f"      使用 --search <关键字> 搜索方法")
        print(f"      使用 --class <类名> 查看SDK类的详细帮助信息")
        return
    
    # 模式5: 查询特定方法的入参
    if args.method:
        target_method = next((m for m in methods if m['name'] == args.method), None)
        if not target_method:
            print(f"❌ 在 {args.client} 中未找到方法: {args.method}")
            # 尝试模糊匹配
            similar = [m['name'] for m in methods if args.method in m['name']]
            if similar:
                print(f"相似的方法:")
                for s in similar[:10]:
                    print(f"  - {s}")
            sys.exit(1)
        
        print(format_client_methods(args.service, version, args.client, methods, full_module_name, search_keyword=f"精确查询: {args.method}"))
        params = get_request_params(target_method['request_type'], full_module_name)
        print(format_request_params(target_method, params))
    
    # 模式6: 搜索方法
    if args.search:
        filtered = [m for m in methods if args.search.lower() in m['name'].lower() or args.search.lower() in m['description'].lower()]
        print(format_client_methods(args.service, version, args.client, methods, full_module_name, search_keyword=args.search))


if __name__ == "__main__":
    main()
