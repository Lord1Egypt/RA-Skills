#!/usr/bin/env python3
"""
广州日报/融媒云测试用例生成器
Usage: python3 generate_cases.py <platform> [--type smoke|full]
Platforms: app_rmy, app_xhc, cms, h5, mini, api
"""
import sys
import json
from datetime import datetime

PLATFORM_CASES = {
    "app_rmy": {
        "name": "融媒云APP（Android/iOS/HarmonyOS）",
        "cases": [
            {"id": "APP-LOGIN-001", "module": "登录", "title": "正常账号密码登录", "level": "P0"},
            {"id": "APP-LOGIN-002", "module": "登录", "title": "错误密码登录", "level": "P1"},
            {"id": "APP-LOGIN-003", "module": "登录", "title": "无账号登录", "level": "P1"},
            {"id": "APP-LOGIN-004", "module": "登录", "title": "微信第三方登录", "level": "P1"},
            {"id": "APP-NEWS-001", "module": "新闻", "title": "刷新首页新闻列表", "level": "P0"},
            {"id": "APP-NEWS-002", "module": "新闻", "title": "查看新闻详情", "level": "P0"},
            {"id": "APP-NEWS-003", "module": "新闻", "title": "新闻搜索", "level": "P1"},
            {"id": "APP-NEWS-004", "module": "新闻", "title": "分享新闻", "level": "P2"},
            {"id": "APP-NEWS-005", "module": "新闻", "title": "收藏新闻", "level": "P2"},
            {"id": "APP-TASK-001", "module": "任务", "title": "查看任务列表", "level": "P0"},
            {"id": "APP-TASK-002", "module": "任务", "title": "接收新任务通知", "level": "P0"},
            {"id": "APP-TASK-003", "module": "任务", "title": "任务状态更新", "level": "P1"},
            {"id": "APP-IM-001", "module": "即时通讯", "title": "发送文本消息", "level": "P0"},
            {"id": "APP-IM-002", "module": "即时通讯", "title": "发送图片消息", "level": "P1"},
            {"id": "APP-IM-003", "module": "即时通讯", "title": "群聊@提及功能", "level": "P2"},
            {"id": "APP-PUSH-001", "module": "推送", "title": "接收新闻推送通知", "level": "P1"},
            {"id": "APP-SET-001", "module": "设置", "title": "修改个人信息", "level": "P2"},
            {"id": "APP-SET-002", "module": "设置", "title": "清除缓存", "level": "P3"},
            {"id": "APP-UP-001", "module": "版本更新", "title": "检测新版本", "level": "P1"},
            {"id": "APP-UP-002", "module": "版本更新", "title": "强制更新场景", "level": "P0"},
        ]
    },
    "app_xhc": {
        "name": "新花城APP（Android/iOS/HarmonyOS）",
        "cases": [
            {"id": "XHC-HOME-001", "module": "首页", "title": "启动APP进入首页", "level": "P0"},
            {"id": "XHC-HOME-002", "module": "首页", "title": "新闻分类Tab切换", "level": "P1"},
            {"id": "XHC-HOME-003", "module": "首页", "title": "视频新闻播放", "level": "P1"},
            {"id": "XHC-SVC-001", "module": "服务", "title": "进入服务板块", "level": "P0"},
            {"id": "XHC-SVC-002", "module": "服务", "title": "寻医问诊入口", "level": "P1"},
            {"id": "XHC-SVC-003", "module": "服务", "title": "垃圾分类查询", "level": "P2"},
            {"id": "XHC-SVC-004", "module": "服务", "title": "党员服务", "level": "P2"},
            {"id": "XHC-COMM-001", "module": "问政", "title": "提交问政内容", "level": "P1"},
            {"id": "XHC-COMM-002", "module": "互动", "title": "用户投稿", "level": "P1"},
            {"id": "XHC-COMM-003", "module": "互动", "title": "社区话题参与", "level": "P2"},
            {"id": "XHC-AUTH-001", "module": "登录", "title": "微信/粤省事登录", "level": "P0"},
            {"id": "XHC-AUTH-002", "module": "登录", "title": "实名认证", "level": "P1"},
            {"id": "XHC-AUTH-003", "module": "登录", "title": "青少年模式", "level": "P2"},
        ]
    },
    "cms": {
        "name": "融媒云后台管理系统",
        "cases": [
            {"id": "CMS-LOGIN-001", "module": "登录", "title": "管理员正常登录", "level": "P0"},
            {"id": "CMS-LOGIN-002", "module": "登录", "title": "无权限账号登录", "level": "P1"},
            {"id": "CMS-LOGIN-003", "module": "登录", "title": "会话超时处理", "level": "P1"},
            {"id": "CMS-NEWS-001", "module": "新闻管理", "title": "创建新闻稿件", "level": "P0"},
            {"id": "CMS-NEWS-002", "module": "新闻管理", "title": "审核新闻稿件", "level": "P0"},
            {"id": "CMS-NEWS-003", "module": "新闻管理", "title": "发布新闻", "level": "P0"},
            {"id": "CMS-NEWS-004", "module": "新闻管理", "title": "撤稿操作", "level": "P1"},
            {"id": "CMS-NEWS-005", "module": "新闻管理", "title": "批量发布", "level": "P1"},
            {"id": "CMS-TASK-001", "module": "任务管理", "title": "创建选题任务", "level": "P0"},
            {"id": "CMS-TASK-002", "module": "任务管理", "title": "任务分配", "level": "P1"},
            {"id": "CMS-USER-001", "module": "用户管理", "title": "新增用户", "level": "P1"},
            {"id": "CMS-USER-002", "module": "用户管理", "title": "编辑用户角色", "level": "P1"},
            {"id": "CMS-USER-003", "module": "用户管理", "title": "禁用/启用账号", "level": "P1"},
            {"id": "CMS-DATA-001", "module": "数据统计", "title": "查看运营数据", "level": "P2"},
            {"id": "CMS-DATA-002", "module": "数据统计", "title": "导出数据报表", "level": "P2"},
            {"id": "CMS-SYS-001", "module": "系统设置", "title": "操作日志审计", "level": "P2"},
            {"id": "CMS-WX-001", "module": "微信管理", "title": "公众号数据统计", "level": "P2"},
        ]
    },
    "h5": {
        "name": "H5页面/活动链接",
        "cases": [
            {"id": "H5-001", "module": "微信", "title": "微信内置浏览器打开", "level": "P0"},
            {"id": "H5-002", "module": "浏览器", "title": "系统浏览器打开", "level": "P1"},
            {"id": "H5-003", "module": "WebView", "title": "APP内嵌WebView打开", "level": "P1"},
            {"id": "H5-004", "module": "分享", "title": "分享到朋友圈", "level": "P1"},
            {"id": "H5-005", "module": "适配", "title": "横竖屏切换适配", "level": "P2"},
            {"id": "H5-006", "module": "网络", "title": "弱网环境加载", "level": "P1"},
            {"id": "H5-007", "module": "表单", "title": "输入表单提交", "level": "P0"},
            {"id": "H5-008", "module": "媒体", "title": "音频/视频播放", "level": "P1"},
            {"id": "H5-009", "module": "图片", "title": "长按图片保存", "level": "P2"},
            {"id": "H5-010", "module": "性能", "title": "首屏加载时间", "level": "P1"},
        ]
    },
    "mini": {
        "name": "微信/支付宝小程序",
        "cases": [
            {"id": "MINI-001", "module": "启动", "title": "首次启动小程序", "level": "P0"},
            {"id": "MINI-002", "module": "导航", "title": "小程序内Tab切换", "level": "P1"},
            {"id": "MINI-003", "module": "新闻", "title": "新闻阅读", "level": "P0"},
            {"id": "MINI-004", "module": "分享", "title": "分享功能", "level": "P1"},
            {"id": "MINI-005", "module": "授权", "title": "授权登录", "level": "P0"},
            {"id": "MINI-006", "module": "支付", "title": "支付场景", "level": "P0"},
            {"id": "MINI-007", "module": "搜索", "title": "搜索功能", "level": "P1"},
            {"id": "MINI-008", "module": "缓存", "title": "缓存清理后重开", "level": "P2"},
            {"id": "MINI-009", "module": "多任务", "title": "多任务切换", "level": "P2"},
        ]
    },
    "api": {
        "name": "接口API测试",
        "cases": [
            {"id": "API-001", "module": "新闻", "title": "获取新闻列表（正常）", "level": "P0"},
            {"id": "API-002", "module": "新闻", "title": "分页参数测试", "level": "P1"},
            {"id": "API-003", "module": "新闻", "title": "必填参数缺失", "level": "P1"},
            {"id": "API-004", "module": "新闻", "title": "获取新闻详情", "level": "P0"},
            {"id": "API-005", "module": "新闻", "title": "不存在ID查询", "level": "P2"},
            {"id": "API-006", "module": "用户", "title": "正确账号登录", "level": "P0"},
            {"id": "API-007", "module": "用户", "title": "错误密码登录", "level": "P1"},
            {"id": "API-008", "module": "用户", "title": "SQL注入防御测试", "level": "P0"},
            {"id": "API-009", "module": "评论", "title": "正常提交评论", "level": "P0"},
            {"id": "API-010", "module": "评论", "title": "未带Token提交", "level": "P0"},
            {"id": "API-011", "module": "上传", "title": "正常上传图片", "level": "P1"},
            {"id": "API-012", "module": "上传", "title": "上传超大文件", "level": "P1"},
            {"id": "API-013", "module": "活动", "title": "正常活动报名", "level": "P0"},
            {"id": "API-014", "module": "活动", "title": "活动已截止报名", "level": "P1"},
            {"id": "API-015", "module": "性能", "title": "并发请求测试", "level": "P1"},
        ]
    }
}


def generate_cases(platforms, case_type="full"):
    """生成测试用例"""
    if isinstance(platforms, str):
        platforms = [platforms]

    output = []
    output.append("# 测试用例文档")
    output.append(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("")

    total = 0
    p0 = p1 = p2 = p3 = 0

    for plat in platforms:
        if plat not in PLATFORM_CASES:
            output.append(f"\n⚠️ 未知平台：`{plat}`，跳过。")
            continue

        info = PLATFORM_CASES[plat]
        cases = info["cases"]

        if case_type == "smoke":
            cases = [c for c in cases if c["level"] in ("P0", "P1")]

        output.append(f"## {info['name']}")
        output.append("")
        output.append("| 用例编号 | 模块 | 用例标题 | 严重级别 | 前置条件 | 测试步骤 | 预期结果 |")
        output.append("|---------|------|---------|---------|---------|---------|---------|")

        for c in cases:
            steps = get_steps(c)
            pre = get_precondition(c)
            result = get_expected(c)
            output.append(
                f"| {c['id']} | {c['module']} | {c['title']} | {c['level']} | {pre} | {steps} | {result} |"
            )
            total += 1
            if c["level"] == "P0":
                p0 += 1
            elif c["level"] == "P1":
                p1 += 1
            elif c["level"] == "P2":
                p2 += 1
            else:
                p3 += 1

        output.append("")

    output.insert(2, f"**总计：{total} 条用例 | P0:{p0} P1:{p1} P2:{p2} P3:{p3}**")
    output.insert(3, "")
    return "\n".join(output)


def get_steps(case):
    """生成测试步骤（简版）"""
    steps_map = {
        "APP-LOGIN-001": "输入正确账号密码，点击登录",
        "APP-LOGIN-002": "输入正确账号，错误密码，点击登录",
        "APP-LOGIN-003": "不输入任何内容，点击登录",
        "APP-NEWS-001": "首页下拉刷新",
        "APP-NEWS-002": "点击新闻进入详情页",
        "APP-TASK-001": "进入任务模块查看列表",
        "APP-IM-001": "进入会话，发送文本消息",
        "H5-001": "微信内置浏览器打开链接",
        "H5-007": "填写表单内容，提交",
        "API-001": "GET请求 /api/news/list",
        "API-006": "POST请求 /api/user/login，json含正确账号密码",
        "API-008": "POST请求，payload含SQL注入字符串",
        "API-015": "使用JMeter/curl并发100QPS请求",
    }
    return steps_map.get(case["id"], "按业务流程执行")


def get_precondition(case):
    """前置条件"""
    if "LOGIN" in case["id"] and "001" in case["id"]:
        return "账号有效且已激活"
    elif "LOGIN" in case["id"]:
        return "-"
    elif "APP" in case["id"]:
        return "已登录"
    elif "API" in case["id"]:
        return "测试环境可用"
    elif "H5" in case["id"]:
        return "链接已生成"
    return "已登录或已授权"


def get_expected(case):
    """预期结果"""
    if "错误" in case["title"] or "不存在" in case["title"] or "缺失" in case["title"]:
        return "返回错误提示，功能不生效"
    elif "SQL" in case["title"] or "注入" in case["title"]:
        return "防御成功，不执行注入"
    elif "Token" in case["title"]:
        return "返回401未授权"
    elif "并发" in case["title"]:
        return "系统不崩溃，响应正常"
    elif "登录" in case["title"] and "正常" not in case["title"]:
        return "登录失败，提示原因"
    return "功能正常，符合预期"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate_cases.py <platform> [--type smoke|full]")
        print("Platforms: app_rmy, app_xhc, cms, h5, mini, api, all")
        sys.exit(1)

    platform_arg = sys.argv[1]
    case_type = "smoke" if "--type" in sys.argv and "smoke" in sys.argv else "full"

    if platform_arg == "all":
        platforms = list(PLATFORM_CASES.keys())
    else:
        platforms = [platform_arg]

    result = generate_cases(platforms, case_type)
    print(result)
