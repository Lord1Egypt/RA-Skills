"""
Adobe UMAPI 客户端模块
封装所有 Adobe UMAPI 调用
"""
import requests
import logging
import time
import json

logger = logging.getLogger(__name__)


class AdobeAPIError(Exception):
    """Adobe API 调用错误"""
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class AdobeClient:
    """
    Adobe UMAPI 客户端（生产级版本）
    
    特性：
    - Token 缓存（24小时）
    - 速率限制（防止触发限流）
    - 指数退避重试（429自动处理）
    - 批量操作支持（减少API调用）
    - 结构化错误处理
    """
    
    # Adobe UMAPI 速率限制（保守设置）
    MAX_REST_CALLS_PER_MIN = 20  # REST API 每分钟最多20次
    MAX_ACTION_CALLS_PER_MIN = 5  # Action API 每分钟最多5次
    
    def __init__(self, token_manager, org_id: str, base_url: str, default_domain: str = None):
        """
        初始化 AdobeClient
        
        Args:
            token_manager: AdobeTokenManager 实例
            org_id: Adobe 组织 ID（如 YOUR_ORG_ID@AdobeOrg）
            base_url: UMAPI 基础 URL
            default_domain: 默认域名（如 example.com），用于自动补全邮箱
        """
        self.token_manager = token_manager
        self.org_id = org_id
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.client_id = self.token_manager.client_id
        self.default_domain = default_domain  # 默认域名，用于自动补全邮箱

        # 速率限制跟踪
        self._rest_call_times = []  # REST API 调用时间戳
        self._action_call_times = []  # Action API 调用时间戳

        # Product Profile id -> name 缓存（用于 add/remove group 命令）
        self._profile_name_cache: dict = {}

    def _mask_value(self, value: str, visible: int = 8) -> str:
        """脱敏日志中的敏感字符串"""
        if not value:
            return ""
        if len(value) <= visible:
            return "*" * len(value)
        return f"{value[:visible]}...***"

    def _format_json_preview(self, data, max_length: int = 2000) -> str:
        """格式化并截断 JSON，避免日志过长"""
        try:
            text = json.dumps(data, ensure_ascii=False, indent=2)
        except Exception:
            text = str(data)
        if len(text) > max_length:
            return f"{text[:max_length]}... (已截断)"
        return text
    
    def _rate_limit_wait(self, api_type: str = 'rest'):
        """
        速率限制：确保不超过 Adobe UMAPI 的限制
        
        Args:
            api_type: 'rest' 或 'action'
        """
        now = time.time()
        call_times = self._rest_call_times if api_type == 'rest' else self._action_call_times
        max_calls = self.MAX_REST_CALLS_PER_MIN if api_type == 'rest' else self.MAX_ACTION_CALLS_PER_MIN
        
        # 清理1分钟前的记录
        call_times[:] = [t for t in call_times if now - t < 60]
        
        # 如果超过限制，等待
        if len(call_times) >= max_calls:
            oldest_call = min(call_times)
            wait_time = 60 - (now - oldest_call) + 0.5  # 多等0.5秒确保安全
            if wait_time > 0:
                logger.warning(f"{api_type.upper()} API 速率限制：等待 {wait_time:.1f} 秒")
                time.sleep(wait_time)
                # 重新清理
                now = time.time()
                call_times[:] = [t for t in call_times if now - t < 60]
        
        # 记录本次调用
        call_times.append(time.time())
    
    def _normalize_user_identifier(self, user_identifier: str) -> str:
        """
        规范化用户标识符，如果只提供用户名则自动添加默认域名
        
        此方法用于简化用户输入，参考 Office 365 模块的实现方式。
        默认域名从 .env 文件中的 ADOBE_DEFAULT_DOMAIN 配置读取。
        
        支持：
        - 输入 "user01" -> 自动补全为 "user01@{ADOBE_DEFAULT_DOMAIN}"
        - 输入 "user01@example.com" -> 直接返回，不进行补全
        
        Args:
            user_identifier: 用户标识符（用户名或完整邮箱）
        
        Returns:
            str: 完整的邮箱地址
        """
        # 如果已经包含 @ 符号，说明是完整邮箱，直接返回
        if '@' in user_identifier:
            return user_identifier
        
        # 如果没有 @ 符号且配置了默认域名，则添加域名后缀
        if self.default_domain:
            return f"{user_identifier}@{self.default_domain}"
        
        # 如果没有默认域名，返回原值
        return user_identifier
    
    def _resolve_group_names(self, tokens) -> list:
        """
        将 Product Profile ID 或名称统一解析为 Adobe Action API `group` 命令要求的名称。

        UMAPI v2 的 add/remove 命令使用 profile 名称，不是 ID。优先从本地 state 缓存
        查找 id->name 映射；其次用实例内存缓存；最后调用 list_profiles 刷新缓存。
        若传入的已经是名称（未命中 id 映射），直接透传。
        """
        if not tokens:
            return []
        if isinstance(tokens, str):
            tokens = [tokens]

        # Lazy 加载：先从 state 文件读取缓存
        if not self._profile_name_cache:
            try:
                from app.core import state as state_helpers
                cached = state_helpers.read_state("adobe") or {}
                for item in cached.get("products") or []:
                    pid = item.get("id")
                    name = item.get("name")
                    if pid and name:
                        self._profile_name_cache[str(pid)] = name
            except Exception as exc:
                logger.debug(f"state 缓存读取失败，忽略: {exc}")

        resolved = []
        need_refresh = []
        for tok in tokens:
            tok_str = str(tok)
            if tok_str in self._profile_name_cache:
                resolved.append(self._profile_name_cache[tok_str])
            else:
                need_refresh.append(tok_str)

        # 有未命中的 ID 才刷新一次
        if need_refresh:
            try:
                profiles = self.list_profiles()
                for p in profiles or []:
                    pid = p.get("id") or p.get("groupId") or p.get("productProfileId")
                    name = p.get("name") or p.get("groupName")
                    if pid and name:
                        self._profile_name_cache[str(pid)] = name
            except Exception as exc:
                logger.warning(f"list_profiles 失败，无法刷新 profile 名称缓存: {exc}")

            for tok in need_refresh:
                resolved.append(self._profile_name_cache.get(tok, tok))

        return resolved

    def _parse_username(self, username: str) -> tuple:
        """
        从用户名中提取名字和姓氏
        
        此方法用于自动拆分姓名，参考 Office 365 模块的实现方式。
        如果用户未提供 firstname 和 lastname，系统会自动从用户名拆分。
        
        拆分规则：
        - 如果用户名长度 >= 3，前3个字符作为姓氏（lastname），其余作为名字（firstname）
        - 例如: "user01" -> ("ke01", "sun") -> (firstname, lastname)
        - 例如: "testuser01" -> ("tuser01", "tes") -> (firstname, lastname)
        - 如果用户名长度 < 3，全部作为名字，姓氏为空
        
        Args:
            username: 用户名（邮箱前缀或完整用户名，如 "user01" 或 "user01@example.com"）
        
        Returns:
            tuple: (firstname, lastname)
        """
        # 如果包含 @，提取 @ 之前的部分
        if '@' in username:
            username = username.split('@')[0]
        
        # 如果用户名长度 >= 3，前3个字符作为姓氏，其余作为名字
        if len(username) >= 3:
            lastname = username[:3]  # 前3个字符作为姓氏
            firstname = username[3:]  # 其余作为名字
        else:
            # 如果用户名太短，全部作为名字，姓氏为空
            firstname = username
            lastname = ""
        
        return (firstname, lastname)
    
    def _make_request(self, method: str, endpoint: str, payload: dict = None, headers: dict = None, 
                     retry: int = 0, max_retries: int = 3, api_type: str = 'action') -> dict:
        """
        通用 HTTP 请求方法（生产级版本）
        
        重要：Adobe UMAPI 要求使用 json= 参数，而不是 data=
        这确保请求体被正确序列化为 JSON 字符串，Content-Type 自动设置为 application/json
        
        包含：
        - 速率限制（防止触发限流）
        - 429 自动重试（指数退避）
        - 结构化错误处理
        
        Args:
            method: HTTP 方法 (GET, POST, PUT, DELETE)
            endpoint: API 端点（不包含基础 URL）
            payload: 请求体数据（字典，将使用 json= 参数自动转换为 JSON）
            headers: 额外的请求头
            retry: 当前重试次数
            max_retries: 最大重试次数
            api_type: 'rest' 或 'action'（用于速率限制）
        
        Returns:
            dict: 响应 JSON 数据，如果是 204 响应则返回空字典
        
        Raises:
            AdobeAPIError: 如果请求失败
        """
        # 速率限制（只在第一次调用时检查，重试时不检查）
        if retry == 0:
            self._rate_limit_wait(api_type)
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"完整请求 URL: {url} (重试: {retry})")
        if payload:
            logger.debug(f"请求体 (payload): {json.dumps(payload, indent=2, ensure_ascii=False)}")
        
        # 获取访问令牌（Token 缓存24小时，这里不会频繁请求）
        token = self.token_manager.get_access_token()
        
        # 构建请求头
        # 注意：不要手动设置 Content-Type，使用 json= 参数时 requests 会自动设置
        request_headers = {
            'Authorization': f'Bearer {token}',
            'X-Api-Key': self.token_manager.client_id
        }
        
        if headers:
            request_headers.update(headers)
        masked_headers = {
            "Authorization": f"Bearer {self._mask_value(token)}" if token else "",
            "X-Api-Key": self._mask_value(self.token_manager.client_id),
        }
        logger.info(self._format_json_preview({
            "action": "umapi_http_request",
            "method": method.upper(),
            "apiType": api_type,
            "url": url,
            "headers": masked_headers,
            "payload": payload or {}
        }))
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=request_headers, timeout=10)
            elif method.upper() == 'POST':
                # 使用 json= 参数时，requests 会自动：
                # 1. 将字典序列化为 JSON 字符串
                # 2. 设置 Content-Type: application/json
                # 3. 发送正确的请求体
                if payload is None:
                    response = self.session.post(url, headers=request_headers, timeout=10)
                else:
                    # 调试：打印实际发送的请求信息
                    logger.debug(f"POST 请求 URL: {url}")
                    logger.debug(f"POST 请求头: {request_headers}")
                    logger.debug(f"POST 请求体 (payload dict): {payload}")
                    # 验证 JSON 序列化
                    try:
                        json_str = json.dumps(payload, ensure_ascii=False)
                        logger.debug(f"POST 请求体 (JSON 字符串): {json_str}")
                    except Exception as e:
                        logger.error(f"JSON 序列化失败: {str(e)}")
                    
                    response = self.session.post(url, headers=request_headers, json=payload, timeout=10)
                    
                    # 调试：打印响应信息
                    logger.debug(f"响应状态码: {response.status_code}")
                    logger.debug(f"响应头: {dict(response.headers)}")
                    if response.status_code >= 400:
                        logger.debug(f"错误响应体: {response.text[:500]}")
            elif method.upper() == 'PUT':
                response = self.session.put(url, headers=request_headers, json=payload, timeout=10)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, headers=request_headers, timeout=10)
            else:
                raise AdobeAPIError(f"不支持的 HTTP 方法: {method}")
            logger.info(self._format_json_preview({
                "action": "umapi_http_response",
                "method": method.upper(),
                "url": url,
                "status": response.status_code,
                "xRequestId": response.headers.get("X-Request-Id"),
                "retryAfter": response.headers.get("Retry-After")
            }))
            
            # 处理 429 Rate Limit（指数退避重试）
            if response.status_code == 429:
                if retry >= max_retries:
                    raise AdobeAPIError(
                        f"API 调用失败: {method} {endpoint} - HTTP 429 (Rate Limit)，已重试 {max_retries} 次",
                        429,
                        {"error": "Rate limit exceeded"}
                    )
                
                # 从响应头获取 Retry-After，如果没有则使用指数退避
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    wait_time = int(retry_after)
                else:
                    wait_time = 2 ** retry  # 指数退避：1秒、2秒、4秒、8秒
                
                logger.warning(f"遇到 429 Rate Limit，等待 {wait_time} 秒后重试 ({retry + 1}/{max_retries})")
                time.sleep(wait_time)
                
                # 递归重试
                return self._make_request(method, endpoint, payload, headers, retry + 1, max_retries, api_type)
            
            # 处理 204 No Content 响应
            if response.status_code == 204:
                logger.info(f"{method} {endpoint} - 成功 (204)")
                return {}
            
            # 检查其他错误状态
            if not response.ok:
                error_detail = {}
                try:
                    error_detail = response.json()
                except:
                    error_detail = {'error': response.text}
                
                error_msg = f"Adobe API 调用失败: {method} {endpoint} - HTTP {response.status_code}"
                logger.error(f"{error_msg} - {error_detail}")
                raise AdobeAPIError(
                    error_msg,
                    status_code=response.status_code,
                    response=error_detail
                )
            
            # 解析 JSON 响应
            result = response.json()
            logger.info(self._format_json_preview({
                "action": "umapi_http_response_body",
                "method": method.upper(),
                "url": url,
                "status": response.status_code,
                "body": result
            }))
            return result
            
        except AdobeAPIError:
            raise
        except requests.exceptions.RequestException as e:
            error_msg = f"请求异常: {method} {endpoint} - {str(e)}"
            logger.error(error_msg)
            raise AdobeAPIError(error_msg) from e
    
    # ==================== 产品与 Profile 查询 ====================
    
    def _action_request(self, commands: list, user: str = "") -> dict:
        """
        执行 User Management Action API 请求（支持批量操作）
        
        根据官方文档，所有查询操作（products/profiles/groups）都使用 POST /action/{orgId}
        而不是 GET 请求
        
        Adobe Action API 要求的 payload 格式：
        {
          "user": "email@example.com" 或 "",
          "do": [
            { "commandName1": {...} },
            { "commandName2": {...} }
          ]
        }
        
        批量操作示例（一次请求完成多个操作）：
        {
          "user": "user@example.com",
          "do": [
            {"createFederatedID": {...}},
            {"add": {"product": "...", "productProfile": "..."}}
          ]
        }
        
        Args:
            commands: 命令列表，如 [{"queryProducts": {}}] 或 [{"createFederatedID": {...}}, {"add": {...}}]
            user: 用户邮箱（对于用户操作），查询操作可以为空字符串
        
        Returns:
            dict: API 响应
        """
        # 速率限制
        self._rate_limit_wait('action')
        
        endpoint = f"/action/{self.org_id}"
        
        # Adobe Action API 要求 body 是 action 对象的数组，外层必须 [ ... ]
        payload = [{
            "user": user,
            "do": commands,
        }]
        
        logger.info(f"Action API 请求 payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")
        response = self._make_request('POST', endpoint, payload, api_type='action')
        logger.info(self._format_json_preview({
            "action": "action_api_response",
            "endpoint": endpoint,
            "user": user,
            "commands": commands,
            "response": response
        }))
        return response
    
    def _rest_get(self, endpoint: str, retry: int = 0, max_retries: int = 3) -> dict:
        """
        REST GET 请求方法（用于 v2 REST 接口）
        
        包含 429 Rate Limit 自动重试机制
        
        Args:
            endpoint: API 端点（不包含基础 URL）
            retry: 当前重试次数
            max_retries: 最大重试次数
        
        Returns:
            dict: 响应 JSON 数据
        
        Raises:
            AdobeAPIError: 如果请求失败
        """
        # 速率限制（只在第一次调用时检查）
        if retry == 0:
            self._rate_limit_wait('rest')
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        token = self.token_manager.get_access_token()
        
        headers = {
            "Authorization": f"Bearer {token}",
            "x-api-key": self.client_id,
        }
        masked_headers = {
            "Authorization": f"Bearer {self._mask_value(token)}" if token else "",
            "X-Api-Key": self._mask_value(self.client_id),
        }
        
        logger.info(self._format_json_preview({
            "action": "umapi_rest_get_request",
            "url": url,
            "endpoint": endpoint,
            "orgId": self.org_id,
            "headers": masked_headers,
            "retry": retry
        }))
        logger.debug(f"REST GET URL: {url} (重试次数: {retry})")
        
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            logger.info(self._format_json_preview({
                "action": "umapi_rest_get_response_meta",
                "url": url,
                "status": resp.status_code,
                "xRequestId": resp.headers.get("X-Request-Id"),
                "retryAfter": resp.headers.get("Retry-After")
            }))
            
            # 处理 429 Rate Limit
            if resp.status_code == 429:
                if retry >= max_retries:
                    raise AdobeAPIError(
                        f"REST GET 调用失败: /{endpoint} - HTTP 429 (Rate Limit)，已重试 {max_retries} 次",
                        429,
                        {"error": "Rate limit exceeded"}
                    )
                
                # 从响应头获取 Retry-After，如果没有则默认等待 2 秒
                retry_after = resp.headers.get("Retry-After")
                if retry_after:
                    wait_time = int(retry_after)
                else:
                    wait_time = 2 * (retry + 1)  # 指数退避：2秒、4秒、6秒
                
                logger.warning(f"遇到 429 Rate Limit，等待 {wait_time} 秒后重试 ({retry + 1}/{max_retries})")
                time.sleep(wait_time)
                
                # 递归重试
                return self._rest_get(endpoint, retry + 1, max_retries)
            
            # 处理其他错误状态
            if resp.status_code >= 400:
                # 尝试解析错误响应
                try:
                    error_data = resp.json()
                except Exception:
                    # 429 或其他错误可能返回空 body
                    error_data = {"error": resp.text or f"HTTP {resp.status_code}"}
                
                logger.error(f"REST GET 失败: {resp.status_code} - {error_data}")
                raise AdobeAPIError(
                    f"REST GET 调用失败: /{endpoint} - HTTP {resp.status_code}",
                    resp.status_code,
                    error_data,
                )
            
            # 成功响应，解析 JSON
            try:
                data = resp.json()
            except Exception as e:
                # 如果响应不是 JSON（理论上不应该发生，但处理边界情况）
                logger.error(f"REST GET 非 JSON 响应: {resp.status_code} - {resp.text}")
                raise AdobeAPIError(
                    f"Invalid JSON response: {str(e)}",
                    resp.status_code,
                    {"error": resp.text}
                )
            
            logger.info(self._format_json_preview({
                "action": "umapi_rest_get_response_body",
                "endpoint": endpoint,
                "status": resp.status_code,
                "body": data
            }))
            return data
            
        except AdobeAPIError:
            raise
        except requests.exceptions.RequestException as e:
            error_msg = f"REST GET 请求异常: {endpoint} - {str(e)}"
            logger.error(error_msg)
            raise AdobeAPIError(error_msg)
    
    def get_groups_and_profiles(self, page: int = 0) -> dict:
        """
        使用 v2 REST 接口查询组织下所有用户组+产品 Profile
        
        GET /v2/usermanagement/groups/{orgId}/{page}
        
        这是当前官方文档中明确存在的接口，用于替代已废弃的 Action API 查询方法
        
        Args:
            page: 页码，从 0 开始
        
        Returns:
            dict: 包含 userGroups/groups 列表的响应数据
        """
        endpoint = f"groups/{self.org_id}/{page}"
        return self._rest_get(endpoint)
    
    def get_products_rest(self) -> list:
        """
        获取产品列表（使用 REST API）
        
        根据 PRD 文档：GET /v2/usermanagement/products/{orgId}
        
        文档: https://adobe-apiplatform.github.io/umapi-documentation/en/api/QueryProducts.html
        
        Returns:
            list: 产品列表
        """
        logger.info("查询所有产品（REST API）")
        endpoint = f"products/{self.org_id}"
        result = self._rest_get(endpoint)
        
        # REST API 可能直接返回列表，也可能返回包含 products 的对象
        if isinstance(result, list):
            products = result
        else:
            products = result.get('products', result.get('value', []))
        
        logger.info(f"成功获取 {len(products)} 个产品")
        return products
    
    def list_profiles(self) -> list:
        """
        获取所有 Product Profiles 列表（使用 REST API - 唯一推荐方式）
        
        根据用户诊断：REST /productprofiles/{orgId} 不存在（404）
        正确方式：从 GET /groups/{orgId}/{page} 获取并筛选 type == "PRODUCT_PROFILE"
        
        GET /v2/usermanagement/groups/{orgId}/{page}
        
        这是当前官方文档中明确存在的接口，用于获取所有 Product Profiles
        
        Returns:
            list: Product Profiles 列表，每个 Profile 包含 id, name, type 等信息
        """
        logger.info("查询所有 Product Profiles（从 /groups/{orgId}/{page} 筛选）")
        
        all_profiles = []
        page = 0
        
        while True:
            result = self.get_groups_and_profiles(page=page)
            
            # 提取 userGroups 或 groups 字段
            groups = result.get('userGroups', result.get('groups', []))
            
            # 筛选出 type == "PRODUCT_PROFILE" 的条目
            for group in groups:
                group_type = group.get('type', group.get('groupType', ''))
                if group_type == "PRODUCT_PROFILE":
                    all_profiles.append(group)
            
            # 检查是否还有下一页
            last_page = result.get('lastPage', True)
            if last_page:
                break
            
            page += 1
        
        logger.info(f"成功获取 {len(all_profiles)} 个 Product Profiles")
        for idx, profile in enumerate(all_profiles, start=1):
            profile_id = profile.get('id') or profile.get('groupId') or profile.get('productProfileId')
            profile_name = profile.get('name') or profile.get('groupName')
            logger.info(self._format_json_preview({
                "action": "list_profiles_entry",
                "index": idx,
                "name": profile_name,
                "id": profile_id,
                "type": profile.get('type') or profile.get('groupType'),
                "productId": profile.get('productId') or profile.get('productID'),
                "raw": profile
            }))
        return all_profiles
    
    def get_product_profiles_rest(self) -> list:
        """
        获取 Product Profiles 列表（已废弃，请使用 list_profiles）
        
        此方法已废弃，因为 REST /productprofiles/{orgId} 接口不存在（404）
        请使用 list_profiles() 方法，它从 /groups/{orgId}/{page} 获取并筛选
        
        Returns:
            list: Product Profiles 列表
        """
        logger.warning("get_product_profiles_rest() 已废弃，请使用 list_profiles()")
        return self.list_profiles()
    
    def get_profile_users(self, profile_id: str) -> list:
        """
        获取指定 Product Profile 下的用户列表
        
        根据 PRD 文档：GET /v2/usermanagement/productprofiles/{orgId}/{profileId}/users
        
        Args:
            profile_id: Product Profile ID
        
        Returns:
            list: 用户列表
        """
        logger.info(f"查询 Product Profile {profile_id} 下的用户")
        endpoint = f"productprofiles/{self.org_id}/{profile_id}/users"
        result = self._rest_get(endpoint)
        
        # REST API 可能直接返回列表，也可能返回包含 users 的对象
        if isinstance(result, list):
            users = result
        else:
            users = result.get('users', result.get('value', []))
        
        logger.info(f"成功获取 {len(users)} 个用户")
        return users
    
    def get_products(self) -> list:
        """
        查询组织下所有产品
        
        使用 User Management Action API: queryProducts
        文档: https://adobe-apiplatform.github.io/umapi-documentation/en/api/product.html
        
        Returns:
            list: 产品列表，每个产品包含 id 和 name
        """
        logger.info("查询所有产品（使用 queryProducts 命令）")
        result = self._action_request([{"queryProducts": {}}])
        
        # 解析响应
        if result.get('result') == 'success':
            products = result.get('products', [])
            logger.info(f"成功获取 {len(products)} 个产品")
            return products
        else:
            logger.error(f"查询产品失败: {result}")
            return []
    
    def get_all_profiles_for_org(self, sub_orgs: bool = False) -> list:
        """
        查询组织下所有产品的所有 profiles
        
        使用 User Management Action API: getAllProfiles
        文档: https://adobe-apiplatform.github.io/umapi-documentation/en/api/getAllProfilesForOrg.html
        
        Args:
            sub_orgs: 是否包含子组织，默认为 False
        
        Returns:
            list: Profile 列表，每个 profile 包含产品信息和 profile 信息
        """
        logger.info("查询所有 Product Profiles（使用 getAllProfiles 命令）")
        result = self._action_request([{
            "getAllProfiles": {
                "subOrgs": sub_orgs
            }
        }])
        
        # 解析响应
        if result.get('result') == 'success':
            profiles = result.get('profiles', [])
            logger.info(f"成功获取 {len(profiles)} 个 Profiles")
            return profiles
        else:
            logger.error(f"查询 Profiles 失败: {result}")
            return []
    
    def get_user_groups(self) -> list:
        """
        查询组织下所有用户组（User Groups）
        
        使用 User Management Action API: queryUserGroups
        文档: https://adobe-apiplatform.github.io/umapi-documentation/en/api/getUserGroups.html
        
        Returns:
            list: 用户组列表
        """
        logger.info("查询所有用户组（使用 queryUserGroups 命令）")
        result = self._action_request([{"queryUserGroups": {}}])
        
        # 解析响应
        if result.get('result') == 'success':
            groups = result.get('groups', [])
            logger.info(f"成功获取 {len(groups)} 个用户组")
            return groups
        else:
            logger.error(f"查询用户组失败: {result}")
            return []
    
    def get_product_profiles(self, product_id: str = None) -> list:
        """
        查询指定产品的所有 profiles
        
        注意：此方法通过 getAllProfiles 获取所有 profiles，然后过滤指定产品
        如果未提供 product_id，返回所有 profiles
        
        Args:
            product_id: 产品 ID（可选）
        
        Returns:
            list: Profile 列表，每个 profile 包含 id 和 name
        """
        all_profiles = self.get_all_profiles_for_org()
        
        if not product_id:
            return all_profiles
        
        # 过滤指定产品的 profiles
        filtered_profiles = [
            profile for profile in all_profiles
            if profile.get('productId') == product_id or profile.get('productID') == product_id
        ]
        
        return filtered_profiles
    
    # ==================== 用户管理 ====================
    
    def create_user(self, email: str, firstname: str = None, lastname: str = None,
                   user_type: str = "federatedID", country: str = "CN",
                   product_profile_ids: list = None) -> dict:
        """
        创建用户（支持 Adobe ID / Enterprise ID / Federated ID）
        
        根据 PRD 文档，支持三种用户类型，并可同时分配产品授权
        
        支持自动处理：
        - 邮箱自动补全：输入 "user01" 自动补全为 "user01@example.com"
        - 姓名自动拆分：如果未提供 firstname/lastname，从邮箱前缀自动拆分
        
        POST /v2/usermanagement/action/{orgId}
        
        Args:
            email: 用户邮箱（支持只输入用户名，如 "user01"）
            firstname: 名字（可选，如果未提供则从邮箱前缀自动拆分）
            lastname: 姓氏（可选，如果未提供则从邮箱前缀自动拆分）
            user_type: 用户类型，可选值：'adobeID', 'enterpriseID', 'federatedID'（默认）
            country: 国家代码，默认为 CN
            product_profile_ids: Product Profile ID 列表，如果提供则创建后自动授权
        
        Returns:
            dict: API 响应
        """
        # 规范化邮箱（自动补全域名）
        email = self._normalize_user_identifier(email)
        
        # 如果未提供姓名，从邮箱前缀自动拆分
        if firstname is None or lastname is None:
            auto_firstname, auto_lastname = self._parse_username(email)
            if firstname is None:
                firstname = auto_firstname
            if lastname is None:
                lastname = auto_lastname

        request_summary = {
            "email": email,
            "firstname": firstname,
            "lastname": lastname,
            "userType": user_type,
            "country": country,
            "productProfileIds": product_profile_ids or []
        }
        logger.info(f"[create_user] 请求参数: {json.dumps(request_summary, ensure_ascii=False, default=str)}")
        commands = []
        
        # 根据用户类型选择创建命令
        if user_type.lower() == "adobeid":
            # UMAPI v2: 正确命令是 addAdobeID（邀请已存在的 Adobe ID 加入组织），不是 createAdobeID
            commands.append({
                "addAdobeID": {
                    "email": email,
                    "country": country,
                    "firstname": firstname,
                    "lastname": lastname,
                    "option": "ignoreIfAlreadyExists",
                }
            })
        elif user_type.lower() == "enterpriseid":
            commands.append({
                "createEnterpriseID": {
                    "email": email,
                    "country": country,
                    "firstname": firstname,
                    "lastname": lastname,
                    "option": "ignoreIfAlreadyExists"  # 如果用户已存在则跳过（UMAPI v2 正确值）
                }
            })
        else:  # federatedID (默认)
            commands.append({
                "createFederatedID": {
                    "email": email,
                    "country": country,
                    "firstname": firstname,
                    "lastname": lastname,
                    "option": "ignoreIfAlreadyExists"  # 如果用户已存在则跳过（UMAPI v2 正确值）
                }
            })
        
        # 如果提供了 product_profile_ids，添加授权命令（UMAPI v2 使用 add + group 名称）
        if product_profile_ids:
            group_names = self._resolve_group_names(product_profile_ids)
            if group_names:
                commands.append({"add": {"group": group_names}})
        
        logger.info(f"[create_user] 构造命令: {json.dumps(commands, ensure_ascii=False, indent=2, default=str)}")
        try:
            response = self._action_request(commands, user=email)
            logger.info(f"[create_user] API 响应: {json.dumps(response, ensure_ascii=False, indent=2, default=str)}")
            return response
        except AdobeAPIError as e:
            if e.response is not None:
                logger.error(f"[create_user] API 响应 (失败): {json.dumps(e.response, ensure_ascii=False, indent=2, default=str)}")
            raise
    
    def assign_product_profiles(self, email: str, product_profile_ids: list) -> dict:
        """
        为用户分配产品授权（使用 productProfileIds）
        
        根据 PRD 文档，使用 assignProductProfiles 命令
        
        支持邮箱自动补全：输入 "user01" 自动补全为 "user01@example.com"
        
        POST /v2/usermanagement/action/{orgId}
        
        Args:
            email: 用户邮箱（支持只输入用户名，如 "user01"）
            product_profile_ids: Product Profile ID 列表
        
        Returns:
            dict: API 响应
        """
        # 规范化邮箱（自动补全域名）
        email = self._normalize_user_identifier(email)

        group_names = self._resolve_group_names(product_profile_ids)
        commands = [{"add": {"group": group_names}}]
        return self._action_request(commands, user=email)

    def remove_product_profiles(self, email: str, product_profile_ids: list) -> dict:
        """
        移除用户的产品授权（使用 productProfileIds）
        
        根据 PRD 文档，使用 removeProductProfiles 命令
        
        支持邮箱自动补全：输入 "user01" 自动补全为 "user01@example.com"
        
        POST /v2/usermanagement/action/{orgId}
        
        Args:
            email: 用户邮箱（支持只输入用户名，如 "user01"）
            product_profile_ids: Product Profile ID 列表
        
        Returns:
            dict: API 响应
        """
        # 规范化邮箱（自动补全域名）
        email = self._normalize_user_identifier(email)

        group_names = self._resolve_group_names(product_profile_ids)
        commands = [{"remove": {"group": group_names}}]
        return self._action_request(commands, user=email)
    
    def get_user(self, email: str, domain: str = None) -> dict:
        """
        查询用户信息（使用 REST API）
        
        根据 Adobe 官方文档：GET /v2/usermanagement/organizations/{orgId}/users/{userString}
        这是 REST API，不是 Action API！
        
        文档: https://adobe-apiplatform.github.io/umapi-documentation/en/api/getUserInfo.html
        
        支持邮箱自动补全：输入 "user01" 自动补全为 "user01@example.com"
        
        Args:
            email: 用户邮箱（支持只输入用户名，如 "user01"）
            domain: 域名（可选，对于 AdobeID 用户使用 "AdobeID"）
        
        Returns:
            dict: 用户信息（从响应中的 'user' 字段提取）
        
        Raises:
            AdobeAPIError: 如果用户不存在（404）或其他错误
        """
        # 规范化邮箱（自动补全域名）
        email = self._normalize_user_identifier(email)
        
        # 使用 REST API（正确的方式）
        # GET /v2/usermanagement/organizations/{orgId}/users/{userString}
        endpoint = f"organizations/{self.org_id}/users/{email}"
        
        # 如果有 domain 参数，添加到查询字符串
        if domain:
            endpoint += f"?domain={domain}"
        
        request_info = {
            "email": email,
            "domain": domain,
            "url": f"{self.base_url}/{endpoint}"
        }
        logger.info(f"[get_user] 请求参数: {json.dumps(request_info, ensure_ascii=False, default=str)}")
        
        try:
            result = self._rest_get(endpoint)
            logger.info(f"[get_user] API 响应: {json.dumps(result, ensure_ascii=False, indent=2, default=str)}")
        except AdobeAPIError as e:
            if e.response is not None:
                logger.error(f"[get_user] API 响应 (失败): {json.dumps(e.response, ensure_ascii=False, indent=2, default=str)}")
            raise
       
        # REST API 返回格式：{"result": "success", "user": {...}}
        if result.get('result') == 'success' and 'user' in result:
            return result['user']
        elif result.get('result') == 'error.user.not_found':
            # 用户不存在，返回 None 或抛出异常（根据业务需求）
            raise AdobeAPIError(f"用户不存在: {email}", 404, result)
        else:
            raise AdobeAPIError(f"查询用户失败: {result.get('message', '未知错误')}", response=result)
    
    def get_users(self, page: int = 0) -> dict:
        """
        查询组织下所有用户（使用 REST API - 推荐用于导出）
        
        根据 PRD 文档：GET /v2/usermanagement/users/{orgId}/{page}
        注意：路径参数格式，不是查询参数
        
        文档: https://adobe-apiplatform.github.io/umapi-documentation/en/api/getUsersREST.html
        
        Args:
            page: 页码，从 0 开始
        
        Returns:
            dict: 包含 users 列表和分页信息的响应，格式如：
                {
                    "users": [...],
                    "lastPage": false,
                    "page": 0
                }
        """
        logger.info(f"查询用户列表（REST API，页码: {page}）")
        
        # 正确的路径格式：/users/{orgId}/{page}（路径参数）
        endpoint = f"users/{self.org_id}/{page}"
        result = self._rest_get(endpoint)
        
        # REST API 返回格式
        users = result.get('users', result.get('value', []))
        last_page = result.get('lastPage', True)  # 如果没有 lastPage 字段，假设是最后一页
        
        logger.info(f"成功获取 {len(users)} 个用户（页码: {page}, 是否最后一页: {last_page}）")
        
        return {
            'users': users,
            'lastPage': last_page,
            'page': page
        }
    
    def get_all_users(self) -> list:
        """
        导出所有用户（自动处理分页，循环直到 lastPage=true）
        
        根据 PRD 文档，用于导出功能
        
        Returns:
            list: 所有用户的列表
        """
        logger.info("开始导出所有用户（自动分页）")
        all_users = []
        page = 0
        
        while True:
            result = self.get_users(page)
            users = result.get('users', [])
            all_users.extend(users)
            
            if result.get('lastPage', True):
                break
            
            page += 1
            # 分页之间稍作延迟，避免触发限流
            time.sleep(0.5)
        
        logger.info(f"导出完成，共 {len(all_users)} 个用户")
        return all_users
    
    def add_product_profile(self, email: str, product_profile_id: str) -> dict:
        """
        为用户添加产品授权（使用 productProfileId）
        
        根据用户诊断：必须使用 addProductProfile 命令，需要 productProfileId
        不能使用 product 和 productProfile 名称
        
        POST /v2/usermanagement/action/{orgId}
        
        支持邮箱自动补全：输入 "user01" 自动补全为 "user01@example.com"
        
        Args:
            email: 用户邮箱（支持只输入用户名，如 "user01"）
            product_profile_id: Product Profile ID（从 list_profiles() 获取）
        
        Returns:
            dict: API 响应
        
        示例：
            # 先获取所有 Profiles
            profiles = adobe_client.list_profiles()
            ps_profile = [p for p in profiles if 'Photoshop' in p.get('name', '')][0]
            
            # 使用 Profile ID 添加授权
            adobe_client.add_product_profile("user01", ps_profile['id'])
        """
        # 规范化邮箱（自动补全域名）
        email = self._normalize_user_identifier(email)
        
        group_names = self._resolve_group_names([product_profile_id])
        commands = [{"add": {"group": group_names}}]
        return self._action_request(commands, user=email)

    def remove_product_profile(self, email: str, product_profile_id: str) -> dict:
        """
        移除用户的产品授权（使用 productProfileId）
        
        根据用户诊断：必须使用 removeProductProfile 命令，需要 productProfileId
        不能使用 product 和 productProfile 名称
        
        POST /v2/usermanagement/action/{orgId}
        
        支持邮箱自动补全：输入 "user01" 自动补全为 "user01@example.com"
        
        Args:
            email: 用户邮箱（支持只输入用户名，如 "user01"）
            product_profile_id: Product Profile ID（从 list_profiles() 获取）
        
        Returns:
            dict: API 响应
        
        示例：
            # 先获取所有 Profiles
            profiles = adobe_client.list_profiles()
            ps_profile = [p for p in profiles if 'Photoshop' in p.get('name', '')][0]
            
            # 使用 Profile ID 移除授权
            adobe_client.remove_product_profile("user01", ps_profile['id'])
        """
        # 规范化邮箱（自动补全域名）
        email = self._normalize_user_identifier(email)
        
        group_names = self._resolve_group_names([product_profile_id])
        commands = [{"remove": {"group": group_names}}]
        return self._action_request(commands, user=email)
    
    def delete_user(self, email: str) -> dict:
        """
        移除用户（从组织移除，自动移除全部授权）
        
        根据 PRD 文档，使用 removeFromOrg 命令（会自动移除全部授权）
        
        支持邮箱自动补全：输入 "user01" 自动补全为 "user01@example.com"
        
        POST /v2/usermanagement/action/{orgId}
        
        注意：目录用户必须从 Azure/Google 删除，否则会被同步回来。
        
        Args:
            email: 用户邮箱（支持只输入用户名，如 "user01"）
        
        Returns:
            dict: API 响应
        """
        # 规范化邮箱（自动补全域名）
        email = self._normalize_user_identifier(email)
        
        commands = [{"removeFromOrg": {}}]
        return self._action_request(commands, user=email)
    
    def reset_password(self, email: str) -> dict:
        """
        强制用户重置密码（仅适用于 Adobe ID 类型）
        
        根据 PRD 文档，使用 update 命令的 forcePasswordReset 选项
        
        支持邮箱自动补全：输入 "user01" 自动补全为 "user01@example.com"
        
        POST /v2/usermanagement/action/{orgId}
        
        Args:
            email: 用户邮箱（支持只输入用户名，如 "user01"，必须是 Adobe ID 类型）
        
        Returns:
            dict: API 响应
        """
        # 规范化邮箱（自动补全域名）
        email = self._normalize_user_identifier(email)
        
        commands = [{
            "update": {
                "option": "forcePasswordReset"
            }
        }]
        return self._action_request(commands, user=email)
    
    def batch_user_operations(self, email: str, operations: list) -> dict:
        """
        批量用户操作（一次请求完成多个操作，减少API调用）
        
        支持邮箱自动补全：输入 "user01" 自动补全为 "user01@example.com"
        
        示例：
        operations = [
            {"createFederatedID": {"email": "user@example.com", "country": "CN", "firstname": "Test", "lastname": "User"}},
            {"add": {"product": "Creative Cloud All Apps", "productProfile": "Default CC All Apps"}}
        ]
        
        Args:
            email: 用户邮箱（支持只输入用户名，如 "user01"）
            operations: 操作列表，每个操作是一个命令字典
        
        Returns:
            dict: API 响应
        """
        # 规范化邮箱（自动补全域名）
        email = self._normalize_user_identifier(email)
        
        return self._action_request(operations, user=email)
