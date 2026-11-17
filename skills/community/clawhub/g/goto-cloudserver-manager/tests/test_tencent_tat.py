"""验证腾讯云 TAT 适配器构造的请求字段名与真实 SDK 模型一致。

get_command_result 曾经错误地给 DescribeInvocationTasksRequest 赋值一个不存在的
InvocationId 属性——这个属性名错误不会在赋值时报错（Python 允许给任意对象设置
任意实例属性），只会在序列化成 HTTP 请求时静默丢失/错位，导致查询结果一直查不到。
用 MagicMock 替换 SDK 无法暴露这类问题，因此这里直接用真实安装的
tencentcloud-sdk-python-tat 模型类来断言实际构造出的请求对象。
"""

from __future__ import annotations

from unittest.mock import MagicMock

from providers.tencent.tat import TencentTAT
from tencentcloud.tat.v20201028 import models as tat_models


def _tat(monkeypatch, describe_response):
    client = MagicMock()
    client.DescribeInvocationTasks.return_value = describe_response
    tat = TencentTAT("id", "key")
    monkeypatch.setattr(tat, "_get_client", lambda region: client)
    return tat, client


def _make_task(status: str, output_b64: str = "", exit_code: int = 0) -> tat_models.InvocationTask:
    task = tat_models.InvocationTask()
    task.TaskStatus = status
    result = tat_models.TaskResult()
    result.Output = output_b64
    result.ExitCode = exit_code
    task.TaskResult = result
    return task


def _make_response(tasks: list) -> tat_models.DescribeInvocationTasksResponse:
    resp = tat_models.DescribeInvocationTasksResponse()
    resp.InvocationTaskSet = tasks
    return resp


def test_get_command_result_filters_by_invocation_id(monkeypatch):
    """请求必须用 Filters（invocation-id 键）传 invocation_id，而不是不存在的 InvocationId 字段。"""
    tat, client = _tat(monkeypatch, _make_response([_make_task("SUCCESS")]))

    tat.get_command_result("inv-123")

    sent_req = client.DescribeInvocationTasks.call_args[0][0]
    assert isinstance(sent_req, tat_models.DescribeInvocationTasksRequest)
    assert not hasattr(sent_req, "InvocationId")
    assert sent_req.Filters is not None
    assert len(sent_req.Filters) == 1
    assert sent_req.Filters[0].Name == "invocation-id"
    assert sent_req.Filters[0].Values == ["inv-123"]


def test_get_command_result_parses_success_task(monkeypatch):
    import base64
    output = base64.b64encode("hello".encode("utf-8")).decode("utf-8")
    tat, _ = _tat(monkeypatch, _make_response([_make_task("SUCCESS", output_b64=output, exit_code=0)]))

    result = tat.get_command_result("inv-123")

    assert result.status == "Finished"
    assert result.stdout == "hello"
    assert result.exit_code == 0


def test_get_command_result_no_tasks_yet_reports_running(monkeypatch):
    tat, _ = _tat(monkeypatch, _make_response([]))

    result = tat.get_command_result("inv-123")

    assert result.status == "Running"
