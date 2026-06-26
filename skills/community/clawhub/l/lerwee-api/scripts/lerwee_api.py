#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lerwee API Client
乐维监控平台 API 客户端
"""

import hashlib
import json
import time
from typing import Any, Dict, List, Optional
import requests


class LerweeAPI:
    """乐维监控平台 API 客户端"""

    def __init__(self, base_url: str, secret: str):
        """
        初始化客户端

        Args:
            base_url: API 基础地址 (如: http://192.168.1.79:8081/api/v6)
            secret: API 密钥
        """
        self.base_url = base_url.rstrip('/')
        self.secret = secret
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _make_sign(self, params: Dict[str, Any]) -> str:
        """
        生成签名

        Args:
            params: 请求参数

        Returns:
            签名字符串
        """
        # 按字母顺序排序
        sorted_items = sorted(params.items())

        # 拼接参数（跳过 sign 字段、空值和数组）
        str_to_sign = ''
        for k, v in sorted_items:
            if k == 'sign':
                continue
            if v != "" and v is not None and not isinstance(v, (list, dict)):
                str_to_sign += f"{k}{v}"

        # 加密钥前缀并 SHA1 加密
        sign_str = self.secret + str_to_sign
        return hashlib.sha1(sign_str.encode('utf-8')).hexdigest().lower()

    def _request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        发送请求

        Args:
            endpoint: API 端点（如 /monitor/host-list）
            params: 请求参数

        Returns:
            响应数据
        """
        if params is None:
            params = {}

        # 添加时间戳和签名
        params['timestamp'] = int(time.time())
        params['sign'] = self._make_sign(params)

        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=params, timeout=30)
        response.raise_for_status()

        return response.json()

    # ==================== 监控中心 ====================

    def get_host_list(self, keyword: Optional[str] = None, ip: Optional[str] = None,
                      true_ip: Optional[int] = None, classification: Optional[int] = None,
                      subtype: Optional[int] = None, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """
        获取监控对象列表

        Args:
            keyword: 关键词搜索
            ip: IP 地址
            true_ip: 精确查询IP (1-是, 0-否)
            classification: 监控类型
            subtype: 监控子类型
            page: 页码
            page_size: 每页数量

        Returns:
            监控对象列表
        """
        params = {
            'page': page,
            'pageSize': page_size
        }
        if keyword:
            params['keyword'] = keyword
        if ip:
            params['ip'] = ip
        if true_ip is not None:
            params['true_ip'] = true_ip
        if classification is not None:
            params['classification'] = classification
        if subtype is not None:
            params['subtype'] = subtype

        return self._request('/monitor/host-list', params)

    def create_host(self, template_id: int, host: str, name: str,
                    group_ids: List[int], status: int = 0,
                    description: Optional[str] = None,
                    proxy_hostid: Optional[int] = None,
                    tag_ids: Optional[List[int]] = None,
                    agent: Optional[Dict[str, Any]] = None,
                    snmp: Optional[Dict[str, Any]] = None,
                    ipmi: Optional[Dict[str, Any]] = None,
                    jmx: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        创建监控对象

        Args:
            template_id: 模板ID
            host: 对象名称（唯一标识且不支持中文）
            name: 业务名称（唯一）
            group_ids: 分组ID数组
            status: 对象状态 (0-启用, 1-禁用)
            description: 描述信息
            proxy_hostid: 代理ID
            tag_ids: 标签ID数组
            agent: Agent接口参数
            snmp: SNMP接口参数
            ipmi: IPMI接口参数
            jmx: JMX接口参数

        Returns:
            创建结果
        """
        params = {
            'template_id': template_id,
            'host': host,
            'name': name,
            'status': status,
            'group_ids': group_ids
        }

        if description:
            params['description'] = description
        if proxy_hostid is not None:
            params['proxy_hostid'] = proxy_hostid
        if tag_ids:
            params['tag_ids'] = tag_ids
        if agent:
            params['agent'] = agent
        if snmp:
            params['snmp'] = snmp
        if ipmi:
            params['ipmi'] = ipmi
        if jmx:
            params['jmx'] = jmx

        return self._request('/monitor/host-create', params)

    def update_host(self, hostid: int, template_id: Optional[int] = None,
                    host: Optional[str] = None, name: Optional[str] = None,
                    status: Optional[int] = None, description: Optional[str] = None,
                    proxy_hostid: Optional[int] = None,
                    group_ids: Optional[List[int]] = None,
                    tag_ids: Optional[List[int]] = None,
                    agent: Optional[Dict[str, Any]] = None,
                    snmp: Optional[Dict[str, Any]] = None,
                    ipmi: Optional[Dict[str, Any]] = None,
                    jmx: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        更新监控对象

        Args:
            hostid: 对象ID
            template_id: 模板ID
            host: 对象名称
            name: 业务名称
            status: 对象状态 (0-启用, 1-禁用)
            description: 描述信息
            proxy_hostid: 代理ID
            group_ids: 分组ID数组
            tag_ids: 标签ID数组
            agent: Agent接口参数
            snmp: SNMP接口参数
            ipmi: IPMI接口参数
            jmx: JMX接口参数

        Returns:
            更新结果
        """
        params = {'hostid': hostid}
        if template_id is not None:
            params['template_id'] = template_id
        if host:
            params['host'] = host
        if name:
            params['name'] = name
        if status is not None:
            params['status'] = status
        if description:
            params['description'] = description
        if proxy_hostid is not None:
            params['proxy_hostid'] = proxy_hostid
        if group_ids:
            params['group_ids'] = group_ids
        if tag_ids:
            params['tag_ids'] = tag_ids
        if agent:
            params['agent'] = agent
        if snmp:
            params['snmp'] = snmp
        if ipmi:
            params['ipmi'] = ipmi
        if jmx:
            params['jmx'] = jmx

        return self._request('/monitor/host-update', params)

    def delete_hosts(self, hostids: List[int]) -> Dict[str, Any]:
        """
        删除监控对象

        Args:
            hostids: 对象ID数组

        Returns:
            删除结果
        """
        params = {'hostids': hostids}
        return self._request('/monitor/host-delete', params)

    def get_host_metrics(self, hostid: int, keyword: Optional[str] = None,
                         item_status: Optional[int] = None,
                         with_latest: Optional[int] = None) -> Dict[str, Any]:
        """
        获取监控对象指标

        Args:
            hostid: 对象ID
            keyword: 关键词(指标名称)
            item_status: 指标状态 (alert-告警指标, empty-空值指标)
            with_latest: 关联最新值 (1-关联, 0-不关联)

        Returns:
            指标列表
        """
        params = {'hostid': hostid}
        if keyword:
            params['keyword'] = keyword
        if item_status:
            params['item_status'] = item_status
        if with_latest is not None:
            params['with_latest'] = with_latest

        return self._request('/monitor/host-metric', params)

    def get_metric_history(self, itemid: int, clock_begin: Optional[int] = None,
                           clock_end: Optional[int] = None,
                           history_type: int = 0, limit: int = 100) -> Dict[str, Any]:
        """
        获取指标历史数据

        Args:
            itemid: 指标ID
            clock_begin: 开始时间（Unix时间戳）
            clock_end: 结束时间（Unix时间戳）
            history_type: 类型 (0-最新, 1-趋势)
            limit: 限制数量

        Returns:
            历史数据
        """
        params = {
            'itemid': itemid,
            'type': history_type,
            'limit': limit
        }
        if clock_begin:
            params['clock_begin'] = clock_begin
        if clock_end:
            params['clock_end'] = clock_end

        return self._request('/monitor/metric-history', params)

    def get_host_macros(self, hostid: int, keyword: Optional[str] = None) -> Dict[str, Any]:
        """
        获取监控对象宏

        Args:
            hostid: 对象ID
            keyword: 关键词

        Returns:
            宏列表
        """
        params = {'hostid': hostid}
        if keyword:
            params['keyword'] = keyword
        return self._request('/monitor/host-macro', params)

    def get_host_form(self, hostid: Optional[int] = None) -> Dict[str, Any]:
        """
        监控对象表单数据

        Args:
            hostid: 对象ID（不传则返回创建表单）

        Returns:
            表单数据
        """
        if hostid:
            params = {'hostid': hostid}
        else:
            params = {}
        return self._request('/monitor/host-form', params)

    def get_host_view(self, hostid: int, view_type: Optional[str] = None) -> Dict[str, Any]:
        """
        监控对象视图

        Args:
            hostid: 对象ID
            view_type: 视图类型

        Returns:
            视图数据
        """
        params = {'hostid': hostid}
        if view_type:
            params['view_type'] = view_type
        return self._request('/monitor/host-view', params)

    def get_host_report(self, hostids: List[int], report_type: Optional[str] = None) -> Dict[str, Any]:
        """
        监控对象报表

        Args:
            hostids: 对象ID数组
            report_type: 报表类型

        Returns:
            报表数据
        """
        params = {'hostids': hostids}
        if report_type:
            params['report_type'] = report_type
        return self._request('/monitor/host-report', params)

    def get_classifications(self) -> Dict[str, Any]:
        """
        获取监控类型列表

        Returns:
            监控类型列表
        """
        return self._request('/monitor/classification', {})

    def get_profile(self, profile_type: Optional[str] = None) -> Dict[str, Any]:
        """
        配置文件

        Args:
            profile_type: 配置类型

        Returns:
            配置数据
        """
        if profile_type:
            params = {'type': profile_type}
        else:
            params = {}
        return self._request('/monitor/profile', params)

    # ==================== 设备探测 ====================

    def get_agent_list(self, page: int = 1, pagesize: int = 10,
                       ip: Optional[str] = None,
                       subtype: Optional[int] = None,
                       agent_install_status: Optional[str] = None,
                       agent_status: Optional[str] = None) -> Dict[str, Any]:
        """
        获取 Agent 列表

        Args:
            page: 页码
            pagesize: 每页数量
            ip: IP地址
            subtype: 系统类型 (101001-Linux, 101003-AIX)
            agent_install_status: 安装状态 (DOING, SUCCESS)
            agent_status: Agent状态 (UP, DOWN)

        Returns:
            Agent 列表
        """
        params = {
            'page': page,
            'pagesize': pagesize
        }
        if ip:
            params['ip'] = ip
        if subtype is not None:
            params['subtype'] = subtype
        if agent_install_status:
            params['agent_install_status'] = agent_install_status
        if agent_status:
            params['agent_status'] = agent_status

        return self._request('/detection/agent-list', params)

    def create_agent_task(self, ips: List[str], username: str,
                          port: int = 22, password: Optional[str] = None,
                          key_path: Optional[str] = None,
                          agent_port: int = 10073,
                          agent_path: Optional[str] = None,
                          server_ip: Optional[str] = None,
                          server_port: Optional[int] = None) -> Dict[str, Any]:
        """
        创建 Agent 安装任务

        Args:
            ips: IP地址数组
            username: SSH用户名
            port: SSH端口（默认: 22）
            password: SSH密码
            key_path: SSH密钥路径
            agent_port: Agent端口（默认: 10073）
            agent_path: Agent安装路径
            server_ip: 服务器IP
            server_port: 服务器端口

        Returns:
            创建结果
        """
        params = {
            'ips': ips,
            'username': username,
            'port': port,
            'agent_port': agent_port
        }
        if password:
            params['password'] = password
        if key_path:
            params['key_path'] = key_path
        if agent_path:
            params['agent_path'] = agent_path
        if server_ip:
            params['server_ip'] = server_ip
        if server_port:
            params['server_port'] = server_port

        return self._request('/detection/agent-create', params)

    def get_agent_install_info(self, task_id: int) -> Dict[str, Any]:
        """
        获取 Agent 安装详情

        Args:
            task_id: 任务ID

        Returns:
            安装详情
        """
        params = {'id': task_id}
        return self._request('/detection/agent-install', params)

    def delete_agents(self, ids: List[int]) -> Dict[str, Any]:
        """
        删除 Agent

        Args:
            ids: 记录ID数组

        Returns:
            删除结果
        """
        params = {'ids': ids}
        return self._request('/detection/agent-delete', params)

    # ==================== 告警管理 ====================

    def get_alarm_list(self, page: int = 1, page_size: int = 20,
                       status: Optional[int] = None,
                       level: Optional[int] = None,
                       clock_begin: Optional[int] = None,
                       clock_end: Optional[int] = None) -> Dict[str, Any]:
        """
        获取告警列表

        Args:
            page: 页码
            page_size: 每页数量
            status: 告警状态
            level: 告警等级
            clock_begin: 开始时间（Unix时间戳）
            clock_end: 结束时间（Unix时间戳）

        Returns:
            告警列表
        """
        params = {
            'page': page,
            'pageSize': page_size
        }
        if status is not None:
            params['status'] = status
        if level is not None:
            params['level'] = level
        if clock_begin:
            params['clock_begin'] = clock_begin
        if clock_end:
            params['clock_end'] = clock_end

        return self._request('/alert/problem-list', params)

    def get_problem_list(self, page: int = 1, page_size: int = 20,
                         status: Optional[int] = None,
                         severity: Optional[int] = None,
                         clock_begin: Optional[int] = None,
                         clock_end: Optional[int] = None) -> Dict[str, Any]:
        """
        获取问题列表

        Args:
            page: 页码
            page_size: 每页数量
            status: 问题状态
            severity: 严重程度
            clock_begin: 开始时间（Unix时间戳）
            clock_end: 结束时间（Unix时间戳）

        Returns:
            问题列表
        """
        params = {
            'page': page,
            'pageSize': page_size
        }
        if status is not None:
            params['status'] = status
        if severity is not None:
            params['severity'] = severity
        if clock_begin:
            params['clock_begin'] = clock_begin
        if clock_end:
            params['clock_end'] = clock_end

        return self._request('/alert/problem-list', params)

    # ==================== 事件平台 ====================

    def get_event_list(self, page: int = 1, page_size: int = 20,
                       clock_begin: Optional[int] = None,
                       clock_end: Optional[int] = None,
                       level: Optional[int] = None,
                       source: Optional[str] = None) -> Dict[str, Any]:
        """
        获取事件列表

        Args:
            page: 页码
            page_size: 每页数量
            clock_begin: 开始时间（Unix时间戳）
            clock_end: 结束时间（Unix时间戳）
            level: 事件级别
            source: 事件来源

        Returns:
            事件列表
        """
        params = {
            'page': page,
            'pageSize': page_size
        }
        if clock_begin:
            params['clock_begin'] = clock_begin
        if clock_end:
            params['clock_end'] = clock_end
        if level is not None:
            params['level'] = level
        if source:
            params['source'] = source

        return self._request('/aialert/list', params)

    def get_ai_alert_list(self, page: int = 1, page_size: int = 20,
                          clock_begin: Optional[int] = None,
                          clock_end: Optional[int] = None,
                          status: Optional[int] = None,
                          title: Optional[str] = None,
                          user_id: Optional[str] = None,
                          platform_id: Optional[str] = None,
                          true_ip: Optional[int] = None,
                          ip: Optional[str] = None,
                          object_name: Optional[str] = None,
                          object_type: Optional[str] = None,
                          object_group: Optional[str] = None,
                          object_group_cluster: Optional[str] = None,
                          object_tag: Optional[str] = None) -> Dict[str, Any]:
        """
        获取事件平台告警列表

        Args:
            page: 页码
            page_size: 每页数量
            clock_begin: 开始时间
            clock_end: 结束时间
            status: 告警状态 (0-待处理, 1-处理中, 2-已处理)
            title: 告警标题
            user_id: 参与人ID
            platform_id: 平台AppId
            true_ip: 是否精确匹配IP (1-是, 0-否)
            ip: 告警IP
            object_name: 告警对象
            object_type: 对象类型
            object_group: 对象分组
            object_group_cluster: 对象分组集群
            object_tag: 对象标签

        Returns:
            事件平台告警列表
        """
        data_params = {
            'page': page,
            'pageSize': page_size
        }
        if clock_begin:
            data_params['clock_begin'] = clock_begin
        if clock_end:
            data_params['clock_end'] = clock_end
        if status is not None:
            data_params['status'] = status
        if title:
            data_params['title'] = title
        if user_id:
            data_params['user_id'] = user_id
        if platform_id:
            data_params['platform_id'] = platform_id
        if true_ip is not None:
            data_params['true_ip'] = true_ip
        if ip:
            data_params['ip'] = ip
        if object_name:
            data_params['object'] = object_name
        if object_type:
            data_params['object_type'] = object_type
        if object_group:
            data_params['object_group'] = object_group
        if object_group_cluster:
            data_params['object_group_cluster'] = object_group_cluster
        if object_tag:
            data_params['object_tag'] = object_tag

        params = {
            'data': json.dumps(data_params, separators=(',', ':'))
        }

        return self._request('/aialert/list', params)

    def get_event_info(self, eventid: int) -> Dict[str, Any]:
        """
        获取事件详情

        Args:
            eventid: 事件ID

        Returns:
            事件详情
        """
        params = {'eventid': eventid}
        return self._request('/aialert/info', params)

    def close_events(self, eventids: List[int]) -> Dict[str, Any]:
        """
        关闭事件

        Args:
            eventids: 事件ID数组

        Returns:
            关闭结果
        """
        params = {'eventids': eventids}
        return self._request('/aialert/close', params)

    def update_alert_status(self, alert_id: int, status: int) -> Dict[str, Any]:
        """
        更新告警处理状态

        Args:
            alert_id: 告警ID
            status: 状态 (1-处理中, 2-已处理)

        Returns:
            更新结果
        """
        params = {
            'id': alert_id,
            'status': status
        }
        return self._request('/aialert/update-status', params)

    def receive_events(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        接收外部事件数据

        Args:
            events: 事件数据数组
                - title: 事件标题
                - level: 事件级别
                - object: 告警对象
                - ip: IP地址
                - description: 描述
                - event_time: 事件时间

        Returns:
            接收结果
        """
        params = {'events': events}
        return self._request('/aialert/receive', params)

    def get_problem_report(self, page: int = 1, page_size: int = 20,
                           clock_begin: Optional[str] = None,
                           clock_end: Optional[str] = None,
                           ip: Optional[str] = None,
                           is_ip: Optional[bool] = None,
                           keyword: Optional[str] = None,
                           is_maintenanced: Optional[bool] = None,
                           is_acked: Optional[bool] = None,
                           status: Optional[int] = None,
                           classification: Optional[int] = None,
                           subtype: Optional[int] = None,
                           groupid: Optional[int] = None) -> Dict[str, Any]:
        """
        获取告警数量统计

        Args:
            page: 页码
            page_size: 每页数量
            clock_begin: 开始时间（格式: 2022-04-16 10:48:38）
            clock_end: 结束时间（格式: 2022-05-16 10:48:38）
            ip: IP模糊查询
            is_ip: 是否精确IP查询
            keyword: 关键字
            is_maintenanced: 是否维护
            is_acked: 是否已确认
            status: 告警恢复 (1-未恢复, 2-已恢复)
            classification: 大类ID（如: 操作系统=101）
            subtype: 子类ID（如: LINUX=101001）
            groupid: 对象分组ID

        Returns:
            告警统计
        """
        params = {
            'searchtype': 'history',
            'page': page,
            'pageSize': page_size
        }
        if clock_begin:
            params['clock_begin'] = clock_begin
        if clock_end:
            params['clock_end'] = clock_end
        if ip:
            params['ip'] = ip
        if is_ip is not None:
            params['is_ip'] = is_ip
        if keyword:
            params['keyword'] = keyword
        if is_maintenanced is not None:
            params['isMaintenanced'] = is_maintenanced
        if is_acked is not None:
            params['isAcked'] = is_acked
        if status is not None:
            params['status'] = status
        if classification is not None:
            params['classification'] = classification
        if subtype is not None:
            params['subtype'] = subtype
        if groupid is not None:
            params['groupid'] = groupid

        return self._request('/alert/problem-report', params)

    def ack_problem(self, eventid: int, message: Optional[str] = None) -> Dict[str, Any]:
        """
        确认问题

        Args:
            eventid: 事件ID
            message: 确认消息

        Returns:
            确认结果
        """
        params = {'eventid': eventid}
        if message:
            params['message'] = message
        return self._request('/alert/problem-ack', params)

    # ==================== 用户管理 ====================

    def get_user_list(self, page: int = 1, page_size: int = 20,
                      keyword: Optional[str] = None,
                      status: Optional[int] = None) -> Dict[str, Any]:
        """
        获取用户列表

        Args:
            page: 页码
            page_size: 每页数量
            keyword: 关键词搜索
            status: 用户状态

        Returns:
            用户列表
        """
        params = {
            'page': page,
            'pageSize': page_size
        }
        if keyword:
            params['keyword'] = keyword
        if status is not None:
            params['status'] = status

        return self._request('/auth/user-list', params)

    def create_user(self, username: str, realname: str, password: str,
                    email: Optional[str] = None, phone: Optional[str] = None,
                    role_id: Optional[int] = None, group_ids: Optional[List[int]] = None,
                    status: int = 1) -> Dict[str, Any]:
        """
        创建用户

        Args:
            username: 用户名
            realname: 真实姓名
            password: 密码
            email: 邮箱
            phone: 手机号
            role_id: 角色ID
            group_ids: 分组ID数组
            status: 状态 (1-启用, 0-禁用)

        Returns:
            创建结果
        """
        params = {
            'username': username,
            'realname': realname,
            'password': password,
            'status': status
        }
        if email:
            params['email'] = email
        if phone:
            params['phone'] = phone
        if role_id is not None:
            params['role_id'] = role_id
        if group_ids:
            params['group_ids'] = group_ids

        return self._request('/auth/user-create', params)

    def update_user(self, userid: int, username: Optional[str] = None,
                    realname: Optional[str] = None, password: Optional[str] = None,
                    email: Optional[str] = None, phone: Optional[str] = None,
                    role_id: Optional[int] = None,
                    group_ids: Optional[List[int]] = None,
                    status: Optional[int] = None) -> Dict[str, Any]:
        """
        更新用户

        Args:
            userid: 用户ID
            username: 用户名
            realname: 真实姓名
            password: 密码
            email: 邮箱
            phone: 手机号
            role_id: 角色ID
            group_ids: 分组ID数组
            status: 状态

        Returns:
            更新结果
        """
        params = {'userid': userid}
        if username:
            params['username'] = username
        if realname:
            params['realname'] = realname
        if password:
            params['password'] = password
        if email:
            params['email'] = email
        if phone:
            params['phone'] = phone
        if role_id is not None:
            params['role_id'] = role_id
        if group_ids:
            params['group_ids'] = group_ids
        if status is not None:
            params['status'] = status

        return self._request('/auth/user-update', params)

    def delete_users(self, userids: List[int]) -> Dict[str, Any]:
        """
        删除用户

        Args:
            userids: 用户ID数组

        Returns:
            删除结果
        """
        params = {'userids': userids}
        return self._request('/auth/user-delete', params)

    # ==================== 监控资源 ====================

    def get_monitor_resources(self, page: int = 1, page_size: int = 20,
                              resource_type: Optional[str] = None) -> Dict[str, Any]:
        """
        获取监控资源列表

        Args:
            page: 页码
            page_size: 每页数量
            resource_type: 资源类型

        Returns:
            监控资源列表
        """
        params = {
            'page': page,
            'pageSize': page_size
        }
        if resource_type:
            params['type'] = resource_type

        return self._request('/monitor/host-list', params)


# 示例用法
if __name__ == '__main__':
    # 初始化客户端
    api = LerweeAPI(
        base_url='http://192.168.1.79:8081/api/v6',
        secret=''
    )

    # 获取监控对象列表
    hosts = api.get_host_list(keyword='linux', page=1, page_size=10)
    print(json.dumps(hosts, indent=2, ensure_ascii=False))

    # 获取告警列表
    alarms = api.get_alarm_list(page=1, page_size=10)
    print(json.dumps(alarms, indent=2, ensure_ascii=False))
