"""
HSS 主机安全服务模块

提供漏洞查询、状态管理、修复触发等能力。
遵循 huawei_cloud 模块规范：
  - 函数命名：无前缀（如 list_vul_host_hosts）
  - 响应格式：{"success": True, "action": "xxx", ...}
  - 错误处理：ClientRequestException + Exception 两层
"""

from .common import *
from huaweicloudsdkcore.exceptions.exceptions import ClientRequestException


# ──────────────────────────────────────────────────────────────
# HSS 错误码解释表
# ──────────────────────────────────────────────────────────────

HSS_ERROR_CODES = {
    "HSS.0001": {
        "meaning": "The service is unavailable.",
        "cause": "HSS 服务未开通、已欠费或已到期",
        "suggestion": "确认 HSS 主机安全服务已开通且账号未欠费",
    },
    "HSS.0002": {
        "meaning": "Failed to parse the request.",
        "cause": "请求参数格式错误或缺少必要参数（如 operate_type 不支持）",
        "suggestion": "检查 operate_type、type 参数组合是否正确",
    },
    "HSS.0003": {
        "meaning": "Incorrect request parameters.",
        "cause": "enterprise_project_id 不存在或值不合法",
        "suggestion": "使用 'all_granted_eps' 查询所有授权企业项目",
    },
    "HSS.0004": {
        "meaning": "Database operation failed.",
        "cause": "华为云 HSS 服务端数据库异常（服务端故障）",
        "suggestion": "非请求问题，等待华为云修复或提交工单",
    },
    "HSS.0005": {
        "meaning": "Request throttled.",
        "cause": "API 请求频率超限",
        "suggestion": "降低 API 调用频率",
    },
    "HSS.0006": {
        "meaning": "Request size exceeds the limit.",
        "cause": "data_list 或 host_data_list 超过500条上限",
        "suggestion": "分批处理，每批不超过500条",
    },
    "HSS.0190": {
        "meaning": "No host agent installed.",
        "cause": "目标主机未安装 HSS Agent",
        "suggestion": "在主机上安装 HSS Agent 后再操作",
    },
    "HSS.0191": {
        "meaning": "Host is not under protection.",
        "cause": "主机未开启防护",
        "suggestion": "先通过 CCE 集成防护或手动方式为主机开启防护",
    },
    "HSS.0192": {
        "meaning": "Feature is not supported for this host.",
        "cause": "HSS 版本不支持该操作（如 Windows 漏洞不支持等）",
        "suggestion": "确认主机防护版本是否支持对应功能",
    },
    "HSS.0193": {
        "meaning": "Host is offline.",
        "cause": "主机不在线或网络不通",
        "suggestion": "检查主机网络状态，确保 Agent 可连通",
    },
    "HSS.0201": {
        "meaning": "Vulnerability does not exist.",
        "cause": "指定的漏洞不存在",
        "suggestion": "使用 list_host_vuls 重新查询漏洞 ID",
    },
    "HSS.0203": {
        "meaning": "Vulnerability does not exist or has been handled.",
        "cause": "漏洞已被修复/忽略/加入白名单",
        "suggestion": "使用 list_host_vuls 重新查询漏洞状态",
    },
    "HSS.0204": {
        "meaning": "Vulnerability cannot be repaired automatically.",
        "cause": "该漏洞不支持自动修复，需要人工介入",
        "suggestion": "查看漏洞详情中的 repair_type 和 repair_cmd 手动处理",
    },
    "HSS.0205": {
        "meaning": "Vulnerability repair failed.",
        "cause": "修复失败（可能修复命令执行失败或需要备份）",
        "suggestion": "检查 repair_cmd 是否正确，确认主机状态，或先手动备份",
    },
    "HSS.1059": {
        "meaning": "Vulnerability operation is not allowed.",
        "cause": "漏洞当前状态不允许此操作（如已修复/已忽略/正在修复中）",
        "suggestion": "使用 list_host_vuls 确认漏洞当前状态，仅对 unhandled 状态执行修复",
    },
    "HSS.1060": {
        "meaning": "Vulnerability fix failed.",
        "cause": "漏洞修复失败（可能修复命令执行失败/权限不足/主机网络异常）",
        "suggestion": "检查主机状态，确认 HSS Agent 正常运行",
    },
    "HSS.1061": {
        "meaning": "Vulnerability is in fixing state.",
        "cause": "漏洞正在修复中，不允许重复操作",
        "suggestion": "等待当前修复完成，或使用 verify 操作验证状态",
    },
    "APIGW.0301": {
        "meaning": "Incorrect IAM authentication information.",
        "cause": "AK/SK 认证失败（格式错误/Token 失效）",
        "suggestion": "检查 HUAWEI_AK/HUAWEI_SK 环境变量是否正确",
    },
    "APIGW.0302": {
        "meaning": "Access denied.",
        "cause": "IAM 权限不足",
        "suggestion": "确认 AK/SK 对应账号具有 HSS 操作权限",
    },
    "APIGW.0305": {
        "meaning": "The requested version does not exist.",
        "cause": "API 版本不存在（endpoint 路径错误）",
        "suggestion": "确认使用的是 v5 版本 API",
    },
}


def _explain_hss_error(error_code: str, http_status: int = None, operate_type: str = None) -> Dict[str, Any]:
    """解释 HSS 错误码，返回详细信息字典"""
    info = HSS_ERROR_CODES.get(error_code, {})
    result = {
        "error_code": error_code,
        "http_status": http_status,
        "meaning": info.get("meaning", "Unknown error"),
        "cause": info.get("cause", "Unknown cause"),
        "suggestion": info.get("suggestion", "请参考华为云 HSS 文档或提交工单"),
    }
    if error_code == "HSS.0002" and operate_type == "repair":
        result["cause"] = "repair 操作需要更多参数或权限"
        result["suggestion"] = "尝试使用 immediate_repair，或确认漏洞是否支持自动修复"
    elif error_code == "HSS.0004":
        result["note"] = "HSS.0004 是服务端数据库故障，与请求格式无关"
    return result


def _format_hss_error(e: Exception, operate_type: str = None) -> str:
    """格式化 HSS 异常，返回带解释的错误字符串"""
    error_code = getattr(e, "error_code", None)
    http_status = getattr(e, "status_code", None)
    error_msg = getattr(e, "error_msg", None)
    request_id = getattr(e, "request_id", None)
    lines = []
    if error_code:
        info = _explain_hss_error(error_code, http_status, operate_type)
        lines.extend([
            f"错误码: {error_code}",
            f"含义: {info['meaning']}",
            f"原因: {info['cause']}",
            f"建议: {info['suggestion']}",
        ])
        if "note" in info:
            lines.append(f"备注: {info['note']}")
    else:
        lines.append(f"错误: {str(e)}")
    if request_id:
        lines.append(f"RequestId: {request_id}")
    return " | ".join(lines)


def _create_hss_client(region: str, access_key: str, secret_key: str):
    """创建 HSS v5 client"""
    from huaweicloudsdkhss.v5 import HssClient
    from huaweicloudsdkhss.v5.region.hss_region import HssRegion
    credentials = BasicCredentials(ak=access_key, sk=secret_key)
    return HssClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(HssRegion.value_of(region)) \
        .build()


def _get_host_unfix_counts(host_id: str, region: str, access_key: str, secret_key: str,
                            enterprise_project_id: str = "all_granted_eps") -> Dict[str, int]:
    """获取主机的 vul_status_unfix 漏洞数量（按严重度统计）"""
    try:
        from huaweicloudsdkhss.v5 import ListHostVulsRequest
        client = _create_hss_client(region, access_key, secret_key)
        request = ListHostVulsRequest(
            enterprise_project_id=enterprise_project_id,
            host_id=host_id,
            status="vul_status_unfix",
            limit="200",
            offset="0",
        )
        response = client.list_host_vuls(request)
        counts = {"unfix_total": 0, "unfix_serious": 0, "unfix_high": 0, "unfix_medium": 0, "unfix_low": 0}
        for v in (response.data_list or []):
            sev = getattr(v, "severity_level", "")
            counts["unfix_total"] += 1
            if sev == "Critical":
                counts["unfix_serious"] += 1
            elif sev == "High":
                counts["unfix_high"] += 1
            elif sev == "Medium":
                counts["unfix_medium"] += 1
            elif sev == "Low":
                counts["unfix_low"] += 1
        return counts
    except Exception:
        return {"unfix_total": 0, "unfix_serious": 0, "unfix_high": 0, "unfix_medium": 0, "unfix_low": 0}


# ──────────────────────────────────────────────────────────────
# 漏洞查询
# ──────────────────────────────────────────────────────────────

def list_vul_host_hosts(
    region: str,
    enterprise_project_id: str = "all_granted_eps",
    machine_type: str = None,
    limit: int = 100,
    offset: int = 0,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
) -> Dict[str, Any]:
    """查询所有主机的漏洞概览

    Returns:
        {
            "success": True,
            "hosts": [...],
            "count": int,
            "total": int,
            "limit": int,
            "offset": int
        }
    """
    access_key, secret_key, _ = get_credentials(ak, sk)
    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters.",
        }

    try:
        from huaweicloudsdkhss.v5 import ListVulHostHostsRequest
        client = _create_hss_client(region, access_key, secret_key)

        kwargs: Dict[str, Any] = {
            "enterprise_project_id": enterprise_project_id,
            "limit": str(limit),
            "offset": str(offset),
        }
        if machine_type:
            kwargs["machine_type"] = machine_type

        request = ListVulHostHostsRequest(**kwargs)
        response = client.list_vul_host_hosts(request)

        hosts = []
        for h in (response.data_list or []):
            host_id = h.host_id

            # Parse vul_num_with_repair_priority_list for vul_status_unhandled counts
            # (HSS can auto-repair these; severity is "repair_priority" field)
            unhandled_total = 0
            unhandled_serious = 0
            unhandled_high = 0
            unhandled_medium = 0
            unhandled_low = 0
            for item in (h.vul_num_with_repair_priority_list or []):
                p = getattr(item, 'repair_priority', '')
                n = getattr(item, 'vul_num', 0) or 0
                unhandled_total += n
                if p == 'Critical':
                    unhandled_serious = n
                elif p == 'High':
                    unhandled_high = n
                elif p == 'Medium':
                    unhandled_medium = n
                elif p == 'Low':
                    unhandled_low = n

            # vul_status_unfix counts (require manual repair) - separate API call per host
            unfix = _get_host_unfix_counts(host_id, region, access_key, secret_key, enterprise_project_id)

            hosts.append({
                "host_id": host_id,
                "host_name": getattr(h, "host_name", ""),
                "private_ip": getattr(h, "private_ip", ""),
                "os_type": getattr(h, "os_type", ""),
                "agent_status": getattr(h, "agent_status", ""),
                "protect_status": getattr(h, "protect_status", ""),
                # vul_status_unhandled counts (HSS can auto-repair; from vul_num_with_repair_priority_list)
                # These match the Huawei Console vulnerability display exactly
                "total_vul_num": unhandled_total,
                "serious_vul_num": unhandled_serious,
                "high_vul_num": unhandled_high,
                "medium_vul_num": unhandled_medium,
                "low_vul_num": unhandled_low,
                # vul_status_unfix counts (require manual repair; from list_host_vuls status=unfix)
                "unfix_total": unfix["unfix_total"],
                "unfix_serious": unfix["unfix_serious"],
                "unfix_high": unfix["unfix_high"],
                "unfix_medium": unfix["unfix_medium"],
                "unfix_low": unfix["unfix_low"],
            })

        return {
            "success": True,
            "action": "list_vul_host_hosts",
            "hosts": hosts,
            "count": len(hosts),
            "total": getattr(response, "total_num", len(hosts)),
            "limit": limit,
            "offset": offset,
        }

    except ClientRequestException as e:
        return {
            "success": False,
            "error": _format_hss_error(e),
            "error_code": e.error_code,
            "request_id": getattr(e, "request_id", None),
        }
    except Exception as e:
        return {
            "success": False,
            "error": _format_hss_error(e),
            "error_type": type(e).__name__,
        }


def list_host_vuls(
    region: str,
    host_id: str = None,
    host_name: str = None,
    status: str = None,
    repair_priority: str = None,
    severity_level: str = None,
    limit: int = 100,
    offset: int = 0,
    enterprise_project_id: str = "all_granted_eps",
    ak: Optional[str] = None,
    sk: Optional[str] = None,
) -> Dict[str, Any]:
    """查询主机漏洞详情

    Args:
        region: 区域ID
        host_id: 主机ID（与 host_name 二选一，host_id 优先）
        host_name: 主机名称
        status: 漏洞状态（vul_status_unhandled / vul_status_unfix /
              vul_status_fix / vul_status_reboot / vul_status_ignored / vul_status_fixing）
        repair_priority: 修复优先级（Critical/High/Medium/Low）
        severity_level: 严重程度（Critical/High/Medium/Low）
        limit: 每页数量
        offset: 偏移量

    Returns:
        {
            "success": True,
            "vulnerabilities": [...],
            "count": int,
            "total": int,
            "limit": int,
            "offset": int
        }
    """
    access_key, secret_key, _ = get_credentials(ak, sk)
    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters.",
        }

    try:
        from huaweicloudsdkhss.v5 import ListHostVulsRequest
        client = _create_hss_client(region, access_key, secret_key)

        kwargs: Dict[str, Any] = {
            "enterprise_project_id": enterprise_project_id,
            "limit": str(limit),
            "offset": str(offset),
        }
        if host_id:
            kwargs["host_id"] = host_id
        if host_name:
            kwargs["host_name"] = host_name
        if status:
            kwargs["status"] = status
        if repair_priority:
            kwargs["repair_priority"] = repair_priority
        if severity_level:
            kwargs["severity_level"] = severity_level

        request = ListHostVulsRequest(**kwargs)
        response = client.list_host_vuls(request)

        vulns = []
        for v in (response.data_list or []):
            vulns.append({
                "vul_id": getattr(v, "vul_id", ""),
                "vul_name": getattr(v, "vul_name", ""),
                "severity_level": getattr(v, "severity_level", ""),
                "repair_priority": getattr(v, "repair_priority", ""),
                "status": getattr(v, "status", ""),
                "repair_type": getattr(v, "repair_type", ""),
                "repair_cmd": getattr(v, "repair_cmd", ""),
                "is_affect_business": getattr(v, "is_affect_business", False),
                "host_id": getattr(v, "host_id", ""),
                "host_name": getattr(v, "host_name", ""),
                "cve_id": getattr(v, "cve_id", ""),
                "nvd_id": getattr(v, "nvd_id", ""),
                "fixed_version": getattr(v, "fixed_version", ""),
            })

        return {
            "success": True,
            "action": "list_host_vuls",
            "vulnerabilities": vulns,
            "count": len(vulns),
            "total": getattr(response, "total_num", len(vulns)),
            "limit": limit,
            "offset": offset,
        }

    except ClientRequestException as e:
        return {
            "success": False,
            "error": _format_hss_error(e),
            "error_code": e.error_code,
            "request_id": getattr(e, "request_id", None),
        }
    except Exception as e:
        return {
            "success": False,
            "error": _format_hss_error(e),
            "error_type": type(e).__name__,
        }


def list_host_vuls_all(
    region: str,
    host_id: str = None,
    host_name: str = None,
    status: str = None,
    repair_priority: str = None,
    severity_level: str = None,
    limit: int = 100,
    enterprise_project_id: str = "all_granted_eps",
    ak: Optional[str] = None,
    sk: Optional[str] = None,
) -> Dict[str, Any]:
    """查询主机漏洞详情（全量，自动翻页）

    Returns:
        {
            "success": True,
            "vulnerabilities": [...],
            "total": int,
            "pages": int,
            "page_count": int
        }
    """
    all_vuls = []
    offset = 0
    page_count = 0
    total = 0

    while True:
        r = list_host_vuls(
            region=region,
            host_id=host_id,
            host_name=host_name,
            status=status,
            repair_priority=repair_priority,
            severity_level=severity_level,
            limit=limit,
            offset=offset,
            enterprise_project_id=enterprise_project_id,
            ak=ak,
            sk=sk,
        )
        if not r.get("success"):
            return r
        all_vuls.extend(r.get("vulnerabilities", []))
        total = r.get("total", 0)
        page_count += 1
        if offset + limit >= total:
            break
        offset += limit

    return {
        "success": True,
        "action": "list_host_vuls_all",
        "vulnerabilities": all_vuls,
        "total": total,
        "pages": (total + limit - 1) // limit if total > 0 else 0,
        "page_count": page_count,
    }


def change_vul_status(
    region: str,
    operate_type: str,
    vul_ids: List[str] = None,
    host_ids: List[str] = None,
    vul_type: str = "linux_vul",
    remark: str = None,
    select_type: str = None,
    confirm: bool = False,
    enterprise_project_id: str = "all_granted_eps",
    ak: Optional[str] = None,
    sk: Optional[str] = None,
) -> Dict[str, Any]:
    """修改漏洞状态（忽略/修复/验证/加入白名单）

    视图规则：
      - 传入 host_ids → 使用 host_data_list（主机视图，优先）
      - 仅传 vul_ids   → 使用 data_list（漏洞视图）

    operate_type 可选值：
      - immediate_repair: 立即修复
      - manual_repair: 人工修复
      - verify: 验证漏洞
      - ignore: 忽略漏洞
      - not_ignore: 取消忽略
      - add_to_whitelist: 加入白名单

    Args:
        confirm: 是否确认执行（默认 False，仅预览）
    """
    access_key, secret_key, _ = get_credentials(ak, sk)
    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided.",
        }

    # 预览模式
    if not confirm:
        view = "host" if host_ids else "vul"
        return {
            "success": True,
            "action": "change_vul_status",
            "preview": True,
            "confirm_required": True,
            "message": "危险操作，需要 confirm=True 才会真正执行",
            "operate_type": operate_type,
            "vul_type": vul_type,
            "view": view,
            "vul_ids_count": len(vul_ids) if vul_ids else 0,
            "host_ids_count": len(host_ids) if host_ids else 0,
            "select_type": select_type,
            "note": "data_list 与 host_data_list 二选一（host_ids 优先）",
        }

    try:
        from huaweicloudsdkhss.v5 import (
            ChangeVulStatusRequest,
            ChangeVulStatusRequestInfo,
            HostVulOperateInfo,
            VulOperateInfo,
        )
        client = _create_hss_client(region, access_key, secret_key)

        # data_list 和 host_data_list 互斥：host_ids 优先
        data_list = None
        host_data_list = None

        if host_ids:
            host_data_list = [
                HostVulOperateInfo(host_id=_hid, vul_id_list=vul_ids)
                for _hid in host_ids
            ]
        elif vul_ids:
            data_list = [VulOperateInfo(vul_id=_vid) for _vid in vul_ids]

        body = ChangeVulStatusRequestInfo(
            operate_type=operate_type,
            type=vul_type,
            data_list=data_list,
            host_data_list=host_data_list,
            select_type=select_type,
            remark=remark,
        )
        request = ChangeVulStatusRequest(
            enterprise_project_id=enterprise_project_id,
            body=body,
        )
        response = client.change_vul_status(request)

        return {
            "success": True,
            "action": "change_vul_status",
            "region": region,
            "operate_type": operate_type,
            "vul_type": vul_type,
            "view": "host" if host_ids else "vul",
            "affected_vulns": len(vul_ids) if vul_ids else 0,
            "affected_hosts": len(host_ids) if host_ids else 0,
            "response": str(response),
        }

    except ClientRequestException as e:
        return {
            "success": False,
            "error": _format_hss_error(e, operate_type=operate_type),
            "error_code": e.error_code,
            "request_id": getattr(e, "request_id", None),
        }
    except Exception as e:
        return {
            "success": False,
            "error": _format_hss_error(e, operate_type=operate_type),
            "error_type": type(e).__name__,
        }
